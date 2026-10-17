#!/usr/bin/env python3
"""檢查穩定 ID、字元錨點、人物證據、身份判斷及 XML／JSON 一致性。"""
from pathlib import Path
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]

def source_age_number(number):
    digits = '一二三四五六七八九'
    if not isinstance(number, str): return None
    if number in digits and len(number) == 1: return digits.index(number) + 1
    if re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?', number):
        tens, ones = number.split('十')
        return (digits.index(tens) + 1 if tens else 1) * 10 + (digits.index(ones) + 1 if ones else 0)
    match = re.fullmatch('([一二三四五六七八九]?)百(?:有?([一二三四五六七八九]?十[一二三四五六七八九]?))?', number)
    if match:
        return (digits.index(match[1]) + 1 if match[1] else 1) * 100 + (source_age_number(match[2]) if match[2] else 0)
    return None

def named_office_end_valid(holding, paragraphs, mentions):
    """明言終於此職的終期，不能以一般死亡替代所有官爵終期。"""
    basis = holding.get('end_basis'); end = holding.get('effective_period',{}).get('end',{})
    if (not isinstance(basis,dict) or set(basis)!={'kind','source_term','evidence'}
            or holding.get('kind')!='office' or basis.get('kind')!='died_in_named_office'
            or basis.get('source_term')!='竟以'+holding.get('title','')+'終'
            or end.get('status')!='source_event' or end.get('event_type')!='explicit_end'
            or not basis.get('evidence') or basis['evidence']!=end.get('evidence')):
        return False
    for e in basis['evidence']:
        hit=paragraphs.get(e.get('paragraph_id')); m=mentions.get(e.get('person_mention_id'))
        quote=e.get('quote','');term=basis['source_term']
        if (not hit or not m or m[1]!=e.get('paragraph_id')
                or m[2].get('person_id')!=holding.get('person_id')
                or not quote or quote not in hit[1]['text'] or term not in quote):return False
        positions=[i for i in range(len(hit[1]['text']))if hit[1]['text'].startswith(term,i)]
        if not any(m[2]['end']<=i and not any(other.get('person_id') not in (None,holding['person_id'])
                    and m[2]['end']<=other['start']<i+len(term) for other in hit[1]['mentions'])for i in positions):return False
    return True


def reported_appointment_count_valid(count, title):
    return (isinstance(count, dict)
             and set(count) == {'value', 'unit', 'source_number', 'source_term', 'status', 'evidence'}
             and type(count.get('value')) is int and count['value'] > 0
             and count.get('unit') == 'appointment'
             and count.get('status') == 'source_attested'
             and source_age_number(count.get('source_number')) == count['value']
             and count.get('source_term') == count['source_number'] + '為' + title
             and isinstance(count.get('evidence'), list) and bool(count['evidence'])
             and all(isinstance(e, dict) and isinstance(e.get('quote'), str)
                     and count['source_term'] in e['quote'] for e in count['evidence']))

def reported_office_event_count_valid(count, event_type):
    verbs = {'departure': '去相', 'reinstatement': '復位'}
    return (event_type in verbs and isinstance(count, dict)
            and set(count) == {'value', 'unit', 'source_number', 'source_term', 'status', 'evidence'}
            and type(count.get('value')) is int and count['value'] > 0
            and count.get('unit') == 'office_event' and count.get('status') == 'source_attested'
            and source_age_number(count.get('source_number')) == count['value']
            and count.get('source_term') == count['source_number'] + verbs[event_type]
            and isinstance(count.get('evidence'), list) and bool(count['evidence'])
            and all(isinstance(e, dict) and isinstance(e.get('quote'), str)
                    and count['source_term'] in e['quote'] for e in count['evidence']))

try:
    from scripts.date_ranges import parallel_event_date
except ImportError:
    from date_ranges import parallel_event_date


def normalized_date_errors(date):
    errors = []
    if not isinstance(date, dict):
        return ['紀年換算須為物件']
    era, year, number = date.get('era'), date.get('year'), date.get('era_year')
    if era not in ('BCE', 'CE') or type(year) is not int or type(number) is not int or number <= 0:
        errors.append('紀年換算須有數字年份與正整數時代年')
    elif year != (number if era == 'CE' else 1 - number):
        errors.append('紀年換算天文年與時代年不一致')
    if date.get('year_numbering') != 'astronomical' or date.get('precision') != 'year':
        errors.append('紀年換算年編號或精度無效')
    if date.get('status') != 'editorial_provisional' or not date.get('original_quote') or not date.get('evidence') or not date.get('references'):
        errors.append('紀年換算原句、證據、參考或判讀狀態缺失')
    if not date.get('rationale') or not date.get('reviewer') or date.get('human_reviewed') is not False:
        errors.append('紀年换算判讀或覆核狀態無效'.replace('换','換'))
    if 'basis' in date and not parallel_event_date(date):
        errors.append('平行事件定年缺少原句或分層參考證據')
    return errors


def title_proposal_errors(proposal, chapter, person_ids):
    """未實行稱號提議不計入人物提及或已持有稱號。"""
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    check(proposal.get('person_id') in person_ids, '稱號提議人物未知')
    check(isinstance(proposal.get('title'), str) and bool(proposal['title']), '稱號提議缺原稱')
    check(proposal.get('outcome') == 'not_enacted', '稱號提議須明示未實行')
    check(proposal.get('status') == 'contextual_provisional'
          and bool(proposal.get('interpretation_note')) and bool(proposal.get('reviewer'))
          and proposal.get('human_reviewed') is False, '稱號提議缺判讀或冒作人工覆核')
    evidence = proposal.get('evidence')
    check(isinstance(evidence, list) and bool(evidence), '稱號提議缺來源證據')
    for e in evidence if isinstance(evidence, list) else []:
        p = next((p for p in chapter['paragraphs'] if p['id'] == e.get('paragraph_id')), None)
        check(bool(p) and e.get('chapter_id') == chapter['id'] and e.get('source_id') == chapter['source_id'], '稱號提議來源不符')
        if not p: continue
        quote = e.get('quote'); starts = [i for i in range(len(p['text']) + 1) if isinstance(quote, str) and quote and p['text'].startswith(quote, i)]
        check(bool(starts), '稱號提議引句不符')
        mentions = {m['id']: m for m in p['mentions']}
        role = mentions.get(proposal.get('role_mention_id')); person = mentions.get(proposal.get('person_mention_id'))
        check(bool(role) and role.get('kind') == 'unresolved' and role.get('person_id') is None
              and role.get('surface') == proposal.get('title'), '稱號提議職稱不得當人物')
        check(bool(person) and person.get('kind') == 'person' and person.get('person_id') == proposal.get('person_id'), '稱號提議人物錨點不符')
        check(bool(role) and bool(person) and any(i <= min(role['start'], person['start'])
              and max(role['end'], person['end']) <= i + len(quote) for i in starts), '稱號提議引句須涵蓋人物及職稱')
    return errors


def validate(root=ROOT):
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    def read(path):
        return json.loads((root / path).read_text(encoding='utf-8'))
    try:
        registry = read('registry/persons.json')
        catalogue = read('registry/works.json')
        progress = read('corpus/progress.json')
        people = registry['persons']
        pids = [p['id'] for p in people]
        check(len(pids) == len(set(pids)), '人物 ID 重複')
        pids = set(pids)
        try:
            from scripts.person_ids import valid_person_id, LEGACY, FAMILY, LEGACY_FAMILY, family_path_errors
        except ModuleNotFoundError:
            from person_ids import valid_person_id, LEGACY, FAMILY, LEGACY_FAMILY, family_path_errors
        check(all(valid_person_id(pid) for pid in pids), '人物 ID 格式不符')
        check(not any(LEGACY_FAMILY.fullmatch(pid) for pid in pids), '舊連字號家族 ID 只可作別名')
        id_aliases = [alias for person in people for alias in person.get('id_aliases', [])]
        check(len(id_aliases) == len(set(id_aliases)) and not set(id_aliases).intersection(pids), '人物 ID 別名重複或占用正式 ID')
        check(all(valid_person_id(alias) for alias in id_aliases), '人物 ID 別名格式不符')
        migration_path = root / 'registry/person-id-migrations.json'
        if migration_path.exists():
            migration = json.loads(migration_path.read_text())
            alias_targets = {alias: person['id'] for person in people for alias in person.get('id_aliases', [])}
            entries = migration.get('mapping', [])
            check(len(entries) == len(alias_targets)
                  and {e['previous_id']: e['person_id'] for e in entries} == alias_targets,
                  '人物 ID 遷移對照與相容別名不符')
            retirement = migration.get('alias_retirement')
            if retirement:
                check(retirement.get('status') == 'retired_after_reference_update'
                      and retirement.get('active_reference_count') == 0
                      and type(retirement.get('retired_alias_count')) is int
                      and retirement['retired_alias_count'] > 0
                      and not alias_targets and not entries,
                      '舊 ID 撤除後不得殘留相容別名或遷移對照')
            migration_count = migration.get('person_count')
            check(type(migration_count) is int
                  and len(set(alias_targets.values())) <= migration_count <= len(people)
                  and migration.get('person_count_scope', 'at_migration') == 'at_migration'
                  and migration.get('identity_merges_performed') is False
                  and all(FAMILY.fullmatch(pid) for pid in pids), '人物 ID 全面遷移範圍或身份政策不符')
        legacy_numbers = [int(pid[5:]) for pid in pids if isinstance(pid, str) and LEGACY.fullmatch(pid)]
        check(registry['next_number'] > max(legacy_numbers, default=0), '舊人物 ID 分配游標會重用 ID')
        works = {w['id']: w for w in catalogue['works']}
        check(len(works) == len(catalogue['works']), '著作 ID 重複')
        books = {}
        chapter_books = {}
        for wid, w in works.items():
            for b in w['books']:
                check(b['id'] not in books, '卷 ID 重複')
                books[b['id']] = b
                check(b['work_id'] == wid, '卷的著作 ID 不符')
                for cid in b['chapter_ids']:
                    check(cid not in chapter_books, '篇 ID 屬於多卷')
                    chapter_books[cid] = b['id']
        try:
            from scripts.table_evidence import load_tables, table_evidence_errors, table_title_range_errors, table_regnal_range_errors
        except ModuleNotFoundError:
            from table_evidence import load_tables, table_evidence_errors, table_title_range_errors, table_regnal_range_errors
        tables = load_tables(root)
        table_chapters = {table['source']['chapter_id']: table for table in tables.values()}
        check(len(table_chapters) == len(tables), '表格證據篇ID重複')
        for table in tables.values():
            source = table['source']
            check(source['work_id'] in works
                  and chapter_books.get(source['chapter_id']) == source['book_id']
                  and books.get(source['book_id'], {}).get('work_id') == source['work_id'],
                  '表格證據著作卷篇未登記或歸屬不符')
        mentions = {}; paragraphs = {}; chapters = {}; files = {}
        case_paragraphs = {}
        for candidate_path in sorted((root / 'corpus').glob('*/*.json')):
            candidate = json.loads(candidate_path.read_text(encoding='utf-8'))
            if candidate.get('record_type') == 'marked_chapter':
                case_paragraphs.update({p['id']: p for p in candidate['paragraphs']})
        for path in sorted((root / 'corpus').glob('*/*.json')):
            d = json.loads(path.read_text(encoding='utf-8'))
            if d.get('record_type') != 'marked_chapter': continue
            cid = d['id']; files[cid] = path
            check(cid not in chapters, '篇 ID 重複')
            chapters[cid] = d
            check(d['work_id'] in works, f'{cid}: 著作不存在')
            check(chapter_books.get(cid) == d['book_id'], f'{cid}: 卷篇歸屬不符')
            check(books.get(d['book_id'], {}).get('work_id') == d['work_id'], f'{cid}: 卷著作歸屬不符')
            for key in ('url','permalink','license_url'):
                u=urlparse(d['source'][key]); check(u.scheme in ('http','https') and bool(u.netloc), f'{cid}: 來源網址無效')
            digest = hashlib.sha256('\n\n'.join(p['text'] for p in d['paragraphs']).encode('utf-8')).hexdigest()
            check(digest == d['text_sha256'], f'{cid}: 文本 SHA-256 不符')
            for p in d['paragraphs']:
                check(p['id'] not in paragraphs, '段落 ID 重複')
                check(p['id'].startswith(cid + ':'), '段落 ID 不屬於篇')
                paragraphs[p['id']] = (cid,p)
                last=0
                for m in p['mentions']:
                    check(m['id'] not in mentions, '提及 ID 重複')
                    mentions[m['id']] = (cid,p['id'],m)
                    check(isinstance(m['start'],int) and isinstance(m['end'],int) and 0 <= m['start'] < m['end'] <= len(p['text']), '提及字元位置無效')
                    check(m['start'] >= last, '提及位置重疊或未排序')
                    check(p['text'][m['start']:m['end']] == m['surface'], '提及引句與位置不符')
                    last=m['end']
                    if m['kind'] == 'person':
                        check(m['person_id'] in pids, '提及引用未知人物 ID')
                        check(any(ch.isalnum() for ch in m['surface']), '人物提及不得僅為標點或空白')
                    elif m['kind'] == 'unresolved': check(m['person_id'] is None and m['status']=='unresolved', '未定提及不得暗選人物')
                    elif m['kind'] == 'work':
                        check(m.get('person_id') is None and m.get('work_id') in works and m.get('status') in ('source_explicit', 'contextual_provisional'), '著作提及須引用已登記著作且不得連人物')
                    else: check(False,'未知提及類型')
            if any('annotation_status' in p for p in d['paragraphs']):
                for p in d['paragraphs']:
                    check(p.get('annotation_status') in ('pending','in_progress','named_mentions_first_pass','reviewed'),'段落標註狀態無效或缺失')
                    if p.get('annotation_status')=='pending':check(not p['mentions'],'待標註段落不得混入已接受的提及')
                if any(p.get('annotation_status') in ('pending','in_progress') for p in d['paragraphs']):
                    check(d['annotation']['status']=='in_progress','篇仍有待標註段落，不得宣稱首輪完成')
            case_ids=set()
            for case in d['annotation'].get('unresolved_identity_cases',[]):
                check(case.get('id') and case['id'] not in case_ids,'未決身份 ID 無效或重複')
                case_ids.add(case.get('id'))
                candidates=case.get('candidate_person_ids',[])
                unknown = case.get('unknown_identity_possible') is True
                check(len(candidates)>=(1 if unknown or case.get('candidate_list_exhaustive') is False else 2) and len(set(candidates))==len(candidates) and all(pid in pids for pid in candidates),'未決身份候選人物無效')
                check(case.get('status')=='unresolved' and bool(case.get('note')),'未決身份狀態或說明缺失')
                if 'candidate_list_exhaustive' in case:
                    check(type(case['candidate_list_exhaustive']) is bool, '候選名單是否窮盡須明示布林值')
                refs=case.get('paragraph_ids',[])
                local={p['id']:p for p in d['paragraphs']}
                check(bool(refs) and any(ref in local for ref in refs) and all(ref in case_paragraphs for ref in refs),'未決身份段落引用無效')
                supported={m['person_id'] for ref in refs if ref in case_paragraphs for m in case_paragraphs[ref]['mentions'] if m['kind']=='person'}
                check(set(candidates)<=supported,'未決身份缺少各候選人物的段落證據')
                if unknown:
                    unresolved = case.get('unresolved_mention_ids', [])
                    anchors = {m['id']: m for ref in refs if ref in case_paragraphs for m in case_paragraphs[ref]['mentions']}
                    check(bool(unresolved) and len(unresolved)==len(set(unresolved))
                          and all(mid in anchors and anchors[mid]['kind']=='unresolved'
                                  and anchors[mid].get('person_id') is None for mid in unresolved),
                          '未知敘者可能須有未連人物的原文錨點')
            xml=ET.parse(path.with_suffix('.xml')).getroot()
            check(xml.tag=='text', 'XML 根元素不符')
            for attr,key in [('work-id','work_id'),('book-id','book_id'),('chapter-id','id'),('source-id','source_id')]:
                check(xml.get(attr)==d[key], 'XML 著作卷篇來源 ID 不符')
            xp=xml.findall('p')
            check(len(xp)==len(d['paragraphs']), 'XML 段落數不符')
            for x,p in zip(xp,d['paragraphs']):
                check(x.get('id')==p['id'] and ''.join(x.itertext())==p['text'], 'XML 正文還原與 JSON 不符')
                check(x.get('annotation-status')==p.get('annotation_status'),'XML 段落標註狀態不符')
                check(x.get('text-layer')==p.get('text_layer'),'XML 文字層次不符')
                if 'text_layer' in p: check(p['text_layer'] in ('received_chapter','witness_appended_bangu_note','witness_appended_suoyin_zan','witness_appended_chu_note','witness_appended_zhengyi_note','witness_appended_edict'),'文字層次無效')
                xm=list(x)
                check(len(xm)==len(p['mentions']), 'XML 提及數不符')
                check(all(e.tag in ('persName','rs','title') for e in x),'XML 含未知正文標籤')
                for e,m in zip(xm,p['mentions']):
                    check(e.get('id')==m['id'] and e.text==m['surface'], 'XML 提及錨點不符')
                    check(e.tag==({'person':'persName','work':'title'}.get(m['kind'], 'rs')), 'XML 提及類型不符')
                    check(e.get('ref')==(m.get('work_id') if m['kind']=='work' else m['person_id']), 'XML 人物或著作引用不符')
                    if m['kind']=='unresolved': check(e.get('type')=='unresolved','XML 未定類型不符')
        check(not set(chapters).intersection(table_chapters), '正文與表格篇ID不得重複')
        check(set(chapter_books)==set(chapters) | set(table_chapters), '著作目錄與文本篇清單不符')
        for wid, work in works.items():
            if work.get('status') != 'referenced_only':
                continue
            evidence = work.get('reference_attestations', [])
            check(bool(evidence) and not work['books'], '僅被引用著作須有原文證據且不得冒作已匯入正文')
            for item in evidence:
                hit = mentions.get(item.get('mention_id'))
                check(bool(hit) and hit[0] == item.get('chapter_id')
                      and hit[1] == item.get('paragraph_id')
                      and hit[2].get('kind') == 'work' and hit[2].get('work_id') == wid
                      and chapters.get(hit[0], {}).get('source_id') == item.get('source_id')
                      and paragraphs.get(hit[1], (None, {}))[1].get('text') == item.get('quote'),
                      '著作登記證據須對應同一書名錨點及完整原文')
        kinship_case_ids = set()
        for chapter in chapters.values():
            for case in chapter['annotation'].get('kinship_interpretation_cases', []):
                check(case['id'] not in kinship_case_ids, '親屬詮釋案例ID重複'); kinship_case_ids.add(case['id'])
                endpoints = {case['subject_person_id'], case['object_person_id']}
                check(len(endpoints) == 2 and endpoints.issubset(pids), '親屬詮釋端點無效')
                check(case['status'] == 'interpretation_disputed' and case['human_reviewed'] is False, '親屬分歧不得冒作人工審閱')
                check(len(case['alternatives']) >= 2 and len({a['id'] for a in case['alternatives']}) == len(case['alternatives']), '親屬詮釋選項不足或重複')
                if case['default_alternative_id'] is not None:
                    selection = case.get('selection', {})
                    check(case['default_alternative_id'] in {a['id'] for a in case['alternatives']}
                          and selection.get('status') == 'editorial_preferred'
                          and selection.get('confidence_level') in ('high', 'moderate', 'low')
                          and bool(selection.get('rationale')) and bool(selection.get('reviewer'))
                          and selection.get('human_reviewed') is False, '親屬預設選項須匹配候選並附編輯判斷')
                    for evidence in selection.get('comparative_evidence', []):
                        hit = paragraphs.get(evidence['paragraph_id'])
                        check(bool(hit) and hit[0] == evidence['chapter_id']
                              and evidence['quote'] in hit[1]['text']
                              and chapters[hit[0]]['source_id'] == evidence['source_id'], '親屬語義比較引句或來源不符')
                check(bool(case['evidence']) and bool(case['source_term']) and bool(case['interpretation_note']), '親屬詮釋缺少原詞或證據')
                for evidence in case['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id'])
                    check(bool(hit) and hit[0] == chapter['id'] == evidence['chapter_id']
                          and evidence['quote'] == hit[1]['text'] and case['source_term'] in evidence['quote']
                          and evidence['source_id'] == chapter['source_id'], '親屬詮釋引句或篇來源不符')
                    if hit:
                        local = {m['person_id'] for m in hit[1]['mentions'] if m['kind'] == 'person'}
                        check(endpoints.issubset(local), '親屬詮釋兩端未見於正文證據')
                for alternative in case['alternatives']:
                    predicate = alternative['predicate']; qualifiers = alternative['qualifiers']; reference = alternative['reference']
                    check(predicate in ('maternal_uncle', 'brother'), '親屬詮釋關係未知')
                    check(type(qualifiers.get('object_generation_relative_to_subject')) is int
                          and qualifiers['object_generation_relative_to_subject'] == (-1 if predicate == 'maternal_uncle' else 0), '親屬詮釋世代方向不符')
                    check(bool(reference.get('quote')) and bool(reference.get('commentator'))
                          and reference.get('url', '').startswith(('https://', 'http://'))
                          and reference.get('image_verified') is False, '親屬詮釋注語署名來源不完整')
            for variant in chapter['annotation'].get('reported_variants', []):
                hit = paragraphs.get(variant['paragraph_id'])
                check(bool(hit) and hit[0] == chapter['id'] and variant['source_term'] in hit[1]['text'], '所報異文原詞與正文不符')
                check(set(variant['person_ids']).issubset(pids) and bool(variant['person_ids']), '所報異文人物無效')
                check(variant['status'] == 'reported_not_collated' and variant['adopted'] is False
                      and variant['received_reading'] in variant['source_term']
                      and variant['reported_reading'] in variant['quote'], '所報異文未區分原文或冒作採用')
                check(bool(variant['commentator']) and variant['url'].startswith(('https://', 'http://')), '所報異文缺注家來源')
        family_relations = [a for path in (root / 'corpus').glob('*/*-assertions.json')
                            for a in json.loads(path.read_text()).get('assertions', [])]
        assertion_index = {a['id']: a for a in family_relations}
        equivalence_index = {d['id']: d for path in (root / 'corpus').glob('*/*-equivalences.json')
                             for d in json.loads(path.read_text()).get('decisions', [])}
        tree_decision_ids = set()
        for path in (root / 'corpus').glob('*/family-tree-decisions.json'):
            record = json.loads(path.read_text())
            check(record.get('record_type') == 'family_tree_decision_set', '編輯世系集類型無效')
            for decision in record['decisions']:
                check(decision['id'] not in tree_decision_ids, '編輯世系決定 ID 重複'); tree_decision_ids.add(decision['id'])
                check(decision['subject_person_id'] in pids
                      and decision['subject_person_id'] in decision['participant_person_ids']
                      and set(decision['participant_person_ids']).issubset(pids), '編輯世系人物端點無效')
                check(decision['status'] == 'editorial_preferred' and decision['human_reviewed'] is False
                      and bool(decision['rationale']) and bool(decision['reviewer'])
                      and decision['confidence_level'] in ('high', 'moderate', 'low', 'inconclusive'), '編輯世系缺少判斷或可信程度')
                preferred = assertion_index.get(decision['preferred_assertion_id'])
                subject_ids = set(decision.get('subject_person_ids', [decision['subject_person_id']]))
                check(decision['subject_person_id'] in subject_ids and subject_ids.issubset(set(decision['participant_person_ids'])), '編輯世系同指端點無效')
                if len(subject_ids) > 1:
                    eqs = [equivalence_index.get(eid) for eid in decision.get('identity_equivalence_decision_ids', [])]
                    check(bool(eqs) and all(eqs) and any(subject_ids.issubset(set(eq['person_ids'])) for eq in eqs if eq), '編輯世系跨候選須有同指依據')
                if decision['preferred_assertion_id'] is not None:
                    check(bool(preferred) and preferred['subject_person_id'] == decision['subject_person_id']
                          and preferred['object_person_id'] == decision['preferred_parent_person_id']
                          and decision['default_view'] in ('use_preferred_parent_edge', 'use_preferred_legal_parent_edge'), '預設世系未匹配來源陳述')
                    if decision['default_view'] == 'use_preferred_legal_parent_edge':
                        check(decision['parentage_role'] == 'legal_or_dynastic' and decision.get('biological_parent_status') == 'unknown', '王室父子不得混同已核生父')
                else:
                    check(decision['preferred_parent_person_id'] is None
                          and decision['default_view'] == 'omit_unproven_biological_parent_edge', '生父未定決定不得暗補父親')
                for aid in decision['excluded_assertion_ids']:
                    assertion = assertion_index.get(aid)
                    check(bool(assertion) and assertion['subject_person_id'] in subject_ids
                          and aid != decision['preferred_assertion_id'], '預設世系排除主張端點不符')
                check(bool(decision['evidence']), '編輯世系缺少來源證據')
                for evidence in decision['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id'])
                    check(bool(hit) and hit[0] == evidence['chapter_id']
                          and evidence['quote'] in hit[1]['text']
                          and chapters[hit[0]]['source_id'] == evidence['source_id'], '編輯世系引句或來源不符')
        assembly_path = root / 'registry/family-assemblies.json'
        assembled_ids = {m['person_id'] for a in json.loads(assembly_path.read_text())['assemblies'] for m in a['members']} if assembly_path.exists() else set()
        for person in people:
            path = person.get('family_path')
            if path is None:
                check(not (FAMILY.fullmatch(person['id']) and len(person['id']) > 11) or person['id'] in assembled_ids, '家族後代 ID 缺少有來源的親屬路徑')
                continue
            parent = path.get('ancestor_person_id', path.get('parent_person_id'))
            check(parent in pids and person['id'] != parent, '家族路徑所據親屬不存在或自環')
            errors.extend(family_path_errors(person['id'], path))
            check(path.get('status') == 'contextual_provisional'
                  and path.get('human_reviewed') is False, '家族路徑關係或審閱狀態無效')
            if 'family_tree_decision_id' in path:
                check(path['family_tree_decision_id'] in tree_decision_ids, '家族路徑所據編輯決定不存在')
            check(bool(path.get('evidence')) and bool(path.get('interpretation_note')), '家族路徑缺少證據或判讀')
            for evidence in path.get('evidence', []):
                hit = paragraphs.get(evidence.get('paragraph_id'))
                check(bool(hit) and hit[0] == evidence.get('chapter_id')
                      and evidence.get('quote') == hit[1]['text']
                      and evidence.get('source_term', '') in hit[1]['text']
                      and chapters[hit[0]]['source_id'] == evidence.get('source_id'), '家族路徑來源與原文不符')
                check(any(a['predicate'] == path.get('connection') and a['subject_person_id'] == person['id']
                          and a['object_person_id'] == parent
                          and (a['predicate'] != 'ancestor' or a.get('qualifiers', {}).get('generation_distance') == path.get('generation_distance'))
                          and any(e['paragraph_id'] == evidence.get('paragraph_id') for e in a['evidence'])
                          for a in family_relations), '家族路徑缺少相符的來源親屬陳述')
        mention_ids_by_person = {}
        for mid, hit in mentions.items():
            mention_ids_by_person.setdefault(hit[2]['person_id'], set()).add(mid)
        for p in people:
            check(bool(p['evidence']), f'{p["id"]}: 人物沒有原文證據')
            evidenced=set()
            for e in p['evidence']:
                hit=mentions.get(e['mention_id'])
                check(bool(hit) and hit[0]==e['chapter_id'] and hit[1]==e['paragraph_id'] and hit[2]['person_id']==p['id'] and hit[2]['surface']==e['quote'], '人物證據與提及不符')
                evidenced.add(e['mention_id'])
            for alias in p['aliases']:
                check(bool(alias['mention_ids']), '異稱沒有證據')
                for mid in alias['mention_ids']:
                    hit=mentions.get(mid)
                    check(mid in evidenced and bool(hit) and hit[2]['surface']==alias['surface'], '異稱證據不符')
            expected=mention_ids_by_person.get(p['id'], set())
            check(expected==evidenced, '人物提及與證據雙向索引不完整')
        dids=set()
        for path in (root/'corpus').glob('*/*-identities.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            for decision in d['decisions']:
                check(decision['id'] not in dids,'身份判斷 ID 重複');dids.add(decision['id'])
                check(decision['person_id'] in pids,'身份判斷引用未知人物')
                check(bool(decision['evidence']),'身份判斷無證據')
                scope=decision.get('scope','same_chapter')
                allowed=decision.get('chapter_ids',[d['chapter_id']])
                check(scope in ('same_chapter','cross_chapter'),'身份判斷範圍未知')
                check(len(allowed)==len(set(allowed)) and set(allowed).issubset(chapters),'身份判斷引用未知或重複篇 ID')
                check(d['chapter_id'] in allowed,'身份判斷未包含所屬篇')
                check(len(allowed)==1 if scope=='same_chapter' else len(allowed)>=2,'身份判斷範圍與篇數不符')
                observed=set()
                for e in decision['evidence']:
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and hit[0] in allowed and e['quote'] in hit[1]['text'],'身份判斷引句不在所屬正文')
                    if hit:
                        observed.add(hit[0])
                        check(any(m['person_id']==decision['person_id'] for m in hit[1]['mentions']),'身份判斷段落未提及該人物')
                check(set(allowed).issubset(observed),'跨篇身份判斷未列各篇證據')
                reading = decision.get('preferred_reading')
                if reading is not None:
                    anchor = mentions.get(reading.get('person_mention_id')) if isinstance(reading, dict) else None
                    variants = [v for cid in allowed for v in chapters[cid]['annotation'].get('reported_variants', [])]
                    variant = next((v for v in variants if isinstance(reading, dict) and v['id'] == reading.get('variant_id')), None)
                    check(isinstance(reading, dict) and set(reading) == {'person_mention_id', 'received_surface', 'preferred_surface', 'source_spelling_is_not_alias', 'variant_id', 'status', 'rationale'}
                          and bool(anchor) and bool(variant)
                          and anchor[1] == variant['paragraph_id']
                          and anchor[2]['person_id'] == decision['person_id']
                          and anchor[2]['surface'] == reading['received_surface'] == variant['received_reading']
                          and reading['preferred_surface'] == variant['reported_reading']
                          and decision['person_id'] in variant['person_ids']
                          and reading['source_spelling_is_not_alias'] is True
                          and reading['status'] == 'editorial_provisional' and bool(reading['rationale'])
                          and decision.get('human_reviewed') is False, '人物首選校讀須有同段異文、人物錨點及明示別名限制')
                target=next((p for p in people if p['id']==decision['person_id']),None)
                if target: check(set(decision['surfaces']).issubset({a['surface'] for a in target['aliases']}),'身份判斷包含未見異稱')
        for path in (root/'corpus').glob('*/*-distinctions.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_distinction_set','人物區分集類型不符')
            check(d['chapter_id'] in chapters,'人物區分集篇不存在')
            for distinction in d['distinctions']:
                check(distinction['id'] not in dids,'身份判斷 ID 重複');dids.add(distinction['id'])
                ids=distinction['person_ids']
                check(len(ids)>=2 and len(set(ids))==len(ids) and set(ids).issubset(pids),'人物區分端點無效或重複')
                check(distinction['status'] in ('contextual_provisional','source_explicit'),'人物區分狀態無效')
                check(bool(distinction['evidence']) and bool(distinction['rationale']),'人物區分無證據或理由')
                supported=set();own=False
                for e in distinction['evidence']:
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and e['quote'] in hit[1]['text'],'人物區分引句不在正文')
                    if hit:
                        own=own or hit[0]==d['chapter_id']
                        supported.update(m['person_id'] for m in hit[1]['mentions'] if m['person_id'] in ids)
                check(own,'人物區分未包含所屬篇證據')
                check(set(ids).issubset(supported),'人物區分未有各端點證據')
        canonical_links={}
        for path in (root/'corpus').glob('*/*-equivalences.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_equivalence_set','同指決定集類型不符')
            check(d['chapter_id'] in chapters,'同指決定篇不存在')
            for decision in d['decisions']:
                check(decision['id'] not in dids,'身份判斷 ID 重複');dids.add(decision['id'])
                ids=decision['person_ids'];canonical=decision['canonical_person_id']
                check((len(ids)>=2 and not decision.get('identity_materialized')) or (len(ids)==1 and decision.get('identity_materialized') is True), '同指決定端點無效或重複')
                check(len(set(ids))==len(ids) and set(ids).issubset(pids),'同指決定端點無效或重複')
                check(canonical in ids,'同指決定代表不在端點中')
                check(decision['status'] in ('source_explicit','contextual_provisional'),'同指決定狀態無效')
                check(bool(decision['evidence']) and bool(decision['rationale']),'同指決定缺少證據或理由')
                scope=decision.get('scope','same_chapter')
                scope_chapters=decision.get('chapter_ids',[d['chapter_id']])
                check(scope in ('same_chapter','cross_chapter'),'同指決定範圍無效')
                check(isinstance(scope_chapters,list) and len(set(scope_chapters))==len(scope_chapters) and d['chapter_id'] in scope_chapters and set(scope_chapters).issubset(chapters),'同指決定範圍篇無效或重複')
                check((scope=='same_chapter' and scope_chapters==[d['chapter_id']]) or (scope=='cross_chapter' and len(scope_chapters)>=2),'同指決定範圍與篇數不符')
                supported=set();evidence_chapters=set()
                for e in decision['evidence']:
                    hit=paragraphs.get(e['paragraph_id']);quote=e['quote']
                    check(bool(hit) and hit[0]==e['chapter_id'] and e['chapter_id'] in scope_chapters and bool(quote) and quote in hit[1]['text'],'同指決定引句與所屬篇不符')
                    check(chapters.get(e['chapter_id'],{}).get('source_id')==e['source_id'],'同指決定來源 ID 不符')
                    evidence_chapters.add(e['chapter_id'])
                    mids=e['mention_ids'];check(bool(mids) and len(mids)==len(set(mids)),'同指決定提及錨點缺失或重複')
                    selected=[]
                    for mid in mids:
                        mention=mentions.get(mid)
                        check(bool(mention) and mention[1]==e['paragraph_id'] and mention[2]['person_id'] in ids,'同指決定提及不屬於證據段落或端點')
                        if mention:selected.append(mention[2])
                    if hit and quote:
                        starts=[i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(quote,i)]
                        enclosed=any(all(i<=m['start'] and m['end']<=i+len(quote) for m in selected) for i in starts)
                        check(enclosed,'同指決定提及不在精確引句範圍')
                    supported.update(m['person_id'] for m in selected)
                check(set(scope_chapters).issubset(evidence_chapters),'同指決定缺少各篇證據')
                check(set(ids).issubset(supported),'同指決定未有各端點提及證據')
                if decision.get('identity_materialized'):
                    check(len({mid for e in decision['evidence'] for mid in e['mention_ids']}) >= 2, '已整併身份仍須有不同來源提及錨點證據')
                for pid in ids:
                    if pid==canonical:continue
                    check(pid not in canonical_links or canonical_links[pid]==canonical,'同指決定代表衝突')
                    canonical_links[pid]=canonical
        applied_decisions = {d['id']: d for path in (root/'corpus').glob('*/*-equivalences.json') for d in json.loads(path.read_text())['decisions']}
        for chapter in chapters.values():
            seen_cases = {c['id'] for c in chapter.get('annotation', {}).get('unresolved_identity_cases', [])}
            for case in chapter.get('annotation', {}).get('resolved_identity_cases', []):
                pid = case.get('person_id')
                check(case.get('id') and case['id'] not in seen_cases and pid in pids and case.get('status') == 'contextual_provisional' and bool(case.get('note')), '已接合身份案件缺少人物、狀態或說明')
                seen_cases.add(case.get('id'))
                references = [applied_decisions.get(i) for i in case.get('identity_equivalence_decision_ids', [])]
                check(bool(references) and all(d and d.get('identity_materialized') is True and d['person_ids'] == [pid] for d in references), '已接合身份案件缺少已套用的同指證據')
                refs = case.get('paragraph_ids', [])
                check(bool(refs) and all(ref in paragraphs for ref in refs) and any(m['person_id'] == pid for ref in refs if ref in paragraphs for m in paragraphs[ref][1]['mentions']), '已接合身份案件缺少原段落人物提及')
        for start in canonical_links:
            seen=set();current=start
            while current in canonical_links:
                if current in seen:
                    check(False,'同指決定代表循環');break
                seen.add(current);current=canonical_links[current]
        def validate_date_evidence(date, context_evidence, expression=None):
            errors.extend(normalized_date_errors(date))
            if not isinstance(date, dict):
                return
            context_ids = {e['paragraph_id'] for e in context_evidence}
            anchored = False
            for evidence in date.get('evidence', []):
                hit = paragraphs.get(evidence['paragraph_id'])
                valid = bool(hit) and hit[0] == evidence['chapter_id']
                check(valid and evidence['quote'] in hit[1]['text'], '紀年換算證據篇段不符')
                if valid:
                    check(chapters[hit[0]]['source_id'] == evidence['source_id'], '紀年換算來源 ID 不符')
                    original = date.get('original_quote')
                    anchored |= (evidence['paragraph_id'] in context_ids
                                 and isinstance(original, str) and original in evidence['quote'])
            check(anchored, '紀年換算原句未見於本筆事件證據')
            if expression is not None:
                check(isinstance(date.get('original_quote'), str)
                      and expression in date['original_quote'], '紀年換算原句未含本筆日期表述')

        title_ids=set();title_occurrence_ids=set()
        title_records = {h['id']: h for path in (root/'corpus').glob('*/*-titles.json')
                         for h in json.loads(path.read_text(encoding='utf-8'))['holdings']}
        for path in (root/'corpus').glob('*/*-titles.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='title_holding_assertion_set','稱號持有集類型不符')
            check(d['chapter_id'] in chapters,'稱號持有篇不存在')
            for h in d['holdings']:
                check(h['id'] not in title_ids,'稱號持有 ID 重複');title_ids.add(h['id'])
                check(h['person_id'] in pids and bool(h['title']),'稱號持有人或用稱無效')
                check(h['status']=='source_attested','稱號持有狀態無效')
                check(h['kind'] in ('royal_rank','imperial_rank','noble_rank','office','honorific','unclassified'),'稱號種類無效')
                check(h['mode'] in ('grant','posthumous_grant','posthumous_naming','self_proclamation','accession','demotion','attestation'),'稱號事件種類無效')
                check(bool(h['evidence']) and bool(h['attestations']),'稱號缺少來源或用稱錨點')
                def title_evidence(e):
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and hit[0]==d['chapter_id']==e['chapter_id'] and bool(e['quote']) and e['quote'] in hit[1]['text'],'稱號引句與所屬篇不符')
                    check(chapters.get(e['chapter_id'],{}).get('source_id')==e['source_id'],'稱號來源 ID 不符')
                    if hit:
                        if 'context' not in e:
                            check(any(m['person_id']==h['person_id'] for m in hit[1]['mentions']),'稱號引句段落未提及持有人')
                        else:
                            context=e['context']
                            valid=isinstance(context,dict)
                            if valid:
                                previous=paragraphs.get(context.get('paragraph_id'))
                                mention=mentions.get(context.get('person_mention_id'))
                                order=[p['id'] for p in chapters.get(d['chapter_id'],{}).get('paragraphs',[])]
                                quote=context.get('quote')
                                valid=(context.get('kind')=='previous_paragraph_subject' and bool(previous)
                                       and previous[0]==d['chapter_id'] and context['paragraph_id'] in order
                                       and e['paragraph_id'] in order and order.index(e['paragraph_id'])==order.index(context['paragraph_id'])+1
                                       and bool(mention) and mention[1]==context['paragraph_id'] and mention[2]['person_id']==h['person_id']
                                       and isinstance(quote,str) and bool(quote) and quote in previous[1]['text'])
                                if valid:
                                    anchor=mention[2];text=previous[1]['text']
                                    valid=any(i<=anchor['start'] and anchor['end']<=i+len(quote)
                                              for i in range(len(text)) if text.startswith(quote,i))
                            check(valid,'稱號省略主語的前段錨點或引句無效')
                for e in h['evidence']:title_evidence(e)
                if 'end_basis' in h:
                    check(named_office_end_valid(h, paragraphs, mentions), '明示終職須綁同人此職原詞，不得以一般死亡補所有職爵')
                if 'inheritance' in h:
                    inheritance = h['inheritance']
                    valid = isinstance(inheritance, dict) and set(inheritance) - {'predecessor_relation'} == {
                        'predecessor_person_id', 'predecessor_holding_id', 'resolved_title',
                        'source_term', 'status', 'evidence', 'rationale', 'human_reviewed'}
                    if valid:
                        predecessor = title_records.get(inheritance['predecessor_holding_id'])
                        cursor = predecessor
                        visited = {h['id']}
                        inherited_chain_valid = True
                        while isinstance(cursor, dict) and 'inheritance' in cursor:
                            link = cursor['inheritance']
                            if (cursor['id'] in visited or cursor.get('kind') != h['kind']
                                or cursor.get('mode') != 'accession' or not isinstance(link, dict)
                                or link.get('resolved_title') != inheritance['resolved_title']):
                                inherited_chain_valid = False
                                break
                            visited.add(cursor['id'])
                            cursor = title_records.get(link.get('predecessor_holding_id'))
                        inherited_chain_valid = (inherited_chain_valid and isinstance(cursor, dict)
                            and cursor['id'] not in visited
                            and cursor.get('kind') == h['kind']
                            and cursor.get('title') == inheritance['resolved_title'])
                        valid = (h['kind'] in ('noble_rank', 'royal_rank') and h['mode'] == 'accession'
                            and bool(predecessor) and predecessor['kind'] == h['kind']
                            and predecessor['person_id'] == inheritance['predecessor_person_id']
                            and predecessor['person_id'] != h['person_id']
                            and inherited_chain_valid
                            and inheritance['status'] == 'contextual_provisional'
                            and inheritance['human_reviewed'] is False
                            and bool(inheritance['rationale'])
                            and isinstance(inheritance['source_term'], str)
                            and bool(inheritance['source_term'])
                            and isinstance(inheritance['evidence'], list) and bool(inheritance['evidence'])
                            and all(inheritance['source_term'] in e.get('quote', '')
                                    for e in inheritance['evidence'])
                            and inheritance.get('predecessor_relation', 'father') in ('father', 'brother')
                            and any(a['predicate'] == inheritance.get('predecessor_relation', 'father')
                                    and a['subject_person_id'] == h['person_id']
                                    and a['object_person_id'] == predecessor['person_id']
                                    and any(e['paragraph_id'] == ie.get('paragraph_id')
                                            for e in a['evidence'] for ie in inheritance['evidence'])
                                    for a in family_relations))
                    check(valid, '承爵判讀缺少相符的前任爵位、父子或原詞證據')
                    if valid:
                        for e in inheritance['evidence']:title_evidence(e)
                if h['mode']=='posthumous_grant' or 'posthumous_basis' in h:
                    basis=h.get('posthumous_basis')
                    explicit_retrospective=(isinstance(basis,dict)
                        and set(basis)=={'source_term','evidence'}
                        and isinstance(basis.get('source_term'),str) and '追尊' in basis['source_term'])
                    death_then_grant=(isinstance(basis,dict)
                        and set(basis)=={'source_term','death_term','grant_term','evidence'}
                        and all(isinstance(basis.get(k),str) and basis[k] for k in ('source_term','death_term','grant_term'))
                        and bool(re.search(r'[死卒薨崩]',basis['death_term']))
                        and basis['grant_term'] in ('賜夫人為'+h['title'], '號為'+h['title'])
                        and basis['death_term'] in basis['source_term']
                        and basis['grant_term'] in basis['source_term']
                        and basis['source_term'].index(basis['death_term'])+len(basis['death_term'])<=basis['source_term'].index(basis['grant_term']))
                    valid=(h['mode']=='posthumous_grant' and (explicit_retrospective or death_then_grant)
                           and isinstance(basis['evidence'],list) and bool(basis['evidence'])
                           and basis['evidence']==h['effective_period']['start']['evidence']
                           and all(isinstance(e,dict) and isinstance(e.get('quote'),str)
                                   and basis['source_term'] in e['quote'] for e in basis['evidence']))
                    check(valid,'追尊授號缺少相符原詞與起點證據')
                    if valid:
                        for e in basis['evidence']:title_evidence(e)
                if h['mode']=='posthumous_naming' or 'naming_basis' in h:
                    basis=h.get('naming_basis')
                    explicit_naming = False
                    if isinstance(basis, dict) and isinstance(basis.get('source_term'), str):
                        term = basis['source_term']
                        explicit_naming = bool(re.search(r'(?:諡|謚)(?:為|爲|曰)?' + re.escape(h['title']), term))
                        named = re.search(r'立號曰[「『]?' + re.escape(h['title']) + r'[」』]?', term)
                        death = basis.get('death_term')
                        if named and isinstance(death, str) and death and death in term:
                            explicit_naming |= term.index(death) + len(death) <= named.start()
                    valid=(h['mode']=='posthumous_naming' and isinstance(basis,dict)
                           and set(basis)=={'source_term','death_term','evidence'}
                           and isinstance(basis['source_term'],str)
                           and explicit_naming
                           and h['title'] in basis['source_term']
                           and isinstance(basis['death_term'],str)
                           and bool(re.search(r'卒|薨|死',basis['death_term']))
                           and isinstance(basis['evidence'],list) and bool(basis['evidence'])
                           and basis['evidence']==h['effective_period']['start']['evidence']
                           and all(isinstance(e,dict) and isinstance(e.get('quote'),str)
                                   and basis['source_term'] in e['quote'] and basis['death_term'] in e['quote']
                                   for e in basis['evidence']))
                    check(valid,'死後諡名缺少相符命名詞、死亡詞與起點證據')
                    if valid:
                        for e in basis['evidence']:title_evidence(e)
                if 'reported_office_event_counts' in h:
                    counts = h['reported_office_event_counts']
                    valid = (h['kind'] == 'office' and isinstance(counts, dict) and bool(counts)
                             and all(reported_office_event_count_valid(c, key) for key, c in counts.items()))
                    check(valid, '離相或復位次數缺少相符原詞與來源證據')
                    if valid:
                        for count in counts.values():
                            for e in count['evidence']: title_evidence(e)
                if 'reported_appointment_count' in h:
                    count = h['reported_appointment_count']
                    valid = reported_appointment_count_valid(count, h['title'])
                    check(valid, '任用次數缺少相符數詞、稱號與來源證據')
                    if valid:
                        for e in count['evidence']: title_evidence(e)
                if 'reported_duration' in h:
                    duration=h['reported_duration']
                    required={'value','unit','source_term','source_number','counting','status','evidence'}
                    bounded=isinstance(duration,dict) and 'bounds' in duration
                    approximate=isinstance(duration,dict) and 'approximation' in duration
                    valid=isinstance(duration,dict) and set(duration)==required | ({'bounds'} if bounded else set()) | ({'approximation'} if approximate else set())
                    if valid:
                        number=duration['source_number']; digits='一二三四五六七八九'; parsed=None
                        if isinstance(number,str):
                            if number in digits and len(number)==1:parsed=digits.index(number)+1
                            elif re.fullmatch('[一二三四五六七八九]?十[一二三四五六七八九]?',number):
                                tens,ones=number.split('十')
                                parsed=(digits.index(tens)+1 if tens else 1)*10+(digits.index(ones)+1 if ones else 0)
                        common=(duration['unit'] in ('regnal_year','title_year','title_month')
                            and duration['counting'] in ('inclusive_regnal_years','unspecified_source_years','unspecified_source_months')
                            and ((duration['unit']=='title_month')==(duration['counting']=='unspecified_source_months'))
                            and (duration['unit']!='title_year' or duration['counting']=='unspecified_source_years')
                            and duration['status']=='source_attested' and isinstance(duration['source_term'],str)
                            and isinstance(duration['evidence'],list) and bool(duration['evidence'])
                            and all(isinstance(e,dict) and isinstance(e.get('quote'),str)
                                    and duration['source_term'] in e['quote'] for e in duration['evidence']))
                        if approximate:
                            approximation=duration['approximation']
                            numbers=approximation.get('numbers') if isinstance(approximation,dict) else None
                            source_numbers=([digits.index(c)+1 for c in number]
                                if isinstance(number,str) and len(number)==2 and all(c in digits for c in number) else None)
                            valid=(common and not bounded and duration['unit']=='title_year'
                                and duration['value'] is None
                                and isinstance(approximation,dict) and set(approximation)=={'kind','numbers'}
                                and approximation['kind']=='adjacent_year_numbers'
                                and isinstance(numbers,list) and len(numbers)==2
                                and all(type(n) is int for n in numbers) and numbers==source_numbers
                                and numbers[1]==numbers[0]+1
                                and re.search(r'(?<![零〇一二三四五六七八九十百千萬億廿卅卌兩])'
                                    +re.escape(number)+r'(?:年|歲|歳)',duration['source_term']) is not None)
                            check(valid,'稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字')
                        elif bounded:
                            implicit_month = (duration['unit']=='title_month' and number is None
                                and duration['source_term'] in ('居月餘','月餘'))
                            if implicit_month:parsed=1
                            bounds=duration['bounds']
                            literal=(implicit_month or isinstance(number,str) and (
                                duration['unit']=='title_month' and duration['source_term']==number+'餘月'
                                or duration['unit']=='title_year' and duration['source_term'] in
                                    (number+'餘年',number+'餘歲',number+'餘歳')))
                            valid=(common and duration['unit'] in ('title_month','title_year')
                                and duration['value'] is None and parsed is not None
                                and isinstance(bounds,dict) and type(bounds.get('lower')) is int
                                and bounds=={'lower':parsed,'lower_inclusive':False,'upper':None,'upper_inclusive':None}
                                and literal)
                            check(valid,'稱號時長界限須保留餘字、未知精確值及排他下界')
                        else:
                            valid=(common and type(duration['value']) is int and parsed is not None
                                and duration['value']==parsed
                                and re.search(r'(?<![零〇一二三四五六七八九十百千萬億廿卅卌兩])'
                                    +re.escape(number)+(r'月' if duration['unit']=='title_month' else r'(?:年|歲|歳)'),duration['source_term']) is not None)
                    check(valid,'稱號來源在位年數或原詞證據無效')
                    if valid:
                        for e in duration['evidence']:title_evidence(e)
                if 'duration_scope' in h:
                    scope = h['duration_scope']
                    ids = scope.get('holding_ids') if isinstance(scope, dict) else None
                    valid = (isinstance(scope, dict)
                        and set(scope) == {'kind', 'holding_ids', 'relation', 'rationale'}
                        and scope['kind'] == 'multiple_holdings'
                        and isinstance(ids, list) and len(ids) >= 2
                        and all(isinstance(i, str) for i in ids) and len(set(ids)) == len(ids)
                        and h['id'] in ids and bool(scope['rationale'])
                        and scope['relation'] in ('successive', 'unspecified')
                        and isinstance(h.get('reported_duration'), dict)
                        and h['reported_duration'].get('unit') == 'title_year'
                        and all(i in title_records and title_records[i]['person_id'] == h['person_id']
                                and title_records[i]['kind'] == h['kind'] for i in ids))
                    check(valid, '跨稱號任事年數缺少同人同類稱號與明示範圍')
                if 'granting_polity' in h:
                    polity = h['granting_polity']; valid = isinstance(polity, dict)
                    check(valid and polity.get('authority_person_id') in pids
                          and polity.get('place_id') is None and polity.get('modern_identification') is None
                          and bool(polity.get('source_name')) and bool(polity.get('evidence')),
                          '授予政體須有原國名、授予者與證據，不補現代位置')
                    if valid:
                        for e in polity.get('evidence', []):
                            hit = paragraphs.get(e.get('paragraph_id')); anchor = mentions.get(e.get('person_mention_id'))
                            quote = e.get('quote'); name = polity.get('source_name')
                            check(bool(hit) and hit[0] == d['chapter_id'] == e.get('chapter_id')
                                  and e.get('source_id') == chapters[d['chapter_id']]['source_id']
                                  and isinstance(quote, str) and quote in hit[1]['text']
                                  and isinstance(name, str) and name in quote and bool(anchor)
                                  and anchor[1] == e.get('paragraph_id') and name in anchor[2]['surface']
                                  and anchor[2]['person_id'] == polity.get('authority_person_id')
                                  and any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                          for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(quote, i)),
                                  '授予政體原國名與授予者錨點或引句不符')
                if 'service_realization' in h:
                    service = h['service_realization']
                    check(isinstance(service, dict) and set(service) == {'status', 'source_term', 'evidence'}
                          and h['mode'] == 'grant' and service.get('status') == 'not_taken_up'
                          and '不往' in service.get('source_term', '') and bool(service.get('evidence')),
                          '授予未赴任須保留不往原詞與證據，不改成已實任')
                    if isinstance(service, dict):
                        for e in service.get('evidence', []):
                            hit = paragraphs.get(e.get('paragraph_id')); anchor = mentions.get(e.get('person_mention_id'))
                            check(bool(hit) and hit[0] == d['chapter_id'] == e.get('chapter_id')
                                  and e.get('source_id') == chapters[d['chapter_id']]['source_id']
                                  and e.get('quote', '') in hit[1]['text']
                                  and service.get('source_term', '') in e.get('quote', '')
                                  and bool(anchor) and anchor[1] == e.get('paragraph_id')
                                  and anchor[2]['person_id'] == h['person_id'], '未赴任人物、來源原詞或證據不符')
                if 'jurisdictions' in h:
                    places=h['jurisdictions']
                    valid=(h['kind'] in ('office','royal_rank') and isinstance(places,list) and bool(places)
                           and all(isinstance(place,dict) and isinstance(place.get('source_name'),str)
                                   and bool(place['source_name'])
                                   and any(place['source_name'] in e.get('quote','') for e in h['evidence'])
                                   and place.get('place_id') is None and place.get('modern_identification') is None
                                   for place in places))
                    check(valid,'稱號所屬原地名缺少引句或未保留未知定位')
                    if h['kind']=='royal_rank':
                        royal=(h['title']=='王' and isinstance(places,list) and bool(places)
                               and all(isinstance(place,dict) and isinstance(place.get('source_name'),str)
                                       and any('王'+place['source_name'] in e.get('quote','') for e in h['evidence'])
                                       for place in places))
                        check(royal,'王國範圍須保留王某地原句，不得由任意地名補入')
                for a in h['attestations']:
                    check(a['id'] not in title_occurrence_ids,'稱號用稱 ID 重複');title_occurrence_ids.add(a['id'])
                    hit=paragraphs.get(a['paragraph_id']);m=mentions.get(a['person_mention_id'])
                    check(bool(hit) and hit[0]==d['chapter_id'],'稱號用稱段落不符')
                    check(bool(m) and m[1]==a['paragraph_id'] and m[2]['person_id']==h['person_id'],'稱號用稱人物提及不符')
                    check(a['surface']==h['title'] and a['usage'] in ('narrative','retrospective','posthumous_usage'),'稱號用稱文字或種類不符')
                    if hit:
                        check(isinstance(a['start'],int) and isinstance(a['end'],int) and 0<=a['start']<a['end']<=len(hit[1]['text']) and hit[1]['text'][a['start']:a['end']]==a['surface'],'稱號用稱字元位置不符')
                        enclosed=False
                        for e in h['evidence']:
                            if e['paragraph_id']!=a['paragraph_id']:continue
                            starts=[i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(e['quote'],i)]
                            if m and any(i<=a['start'] and a['end']<=i+len(e['quote']) and i<=m[2]['start'] and m[2]['end']<=i+len(e['quote']) for i in starts):enclosed=True
                        check(enclosed,'稱號用稱及持有人不在精確引句範圍')
                    if 'normalized_date' in a:
                        expression = a.get('date_expression')
                        check(expression is None or isinstance(expression, str) and bool(expression), '用稱日期表述無效')
                        validate_date_evidence(a['normalized_date'], h['evidence'], expression)
                    if 'normalized_date_range' in a:
                        try:
                            from scripts.date_ranges import year_range_errors
                        except ImportError:
                            from date_ranges import year_range_errors
                        check('normalized_date' not in a, '用稱跨年範圍不得另填確定單年')
                        expression = a.get('date_expression')
                        errors.extend(year_range_errors(a['normalized_date_range'], h['evidence'], expression))
                        errors.extend(table_regnal_range_errors(a['normalized_date_range'], expression, tables, mentions))
                period=h['effective_period']
                for endpoint in ('start','end'):
                    boundary=period[endpoint]
                    check(boundary['status'] in ('unknown','source_event'),'稱號時段端點狀態無效')
                    expected={'status','date_expression','evidence'}
                    if boundary['status']=='source_event':
                        expected.add('event_type')
                        if 'normalized_date' in boundary:expected.add('normalized_date')
                        if 'normalized_date_range' in boundary:expected.add('normalized_date_range')
                    check(set(boundary)==expected,'稱號端點含未定義欄位，不能暗補正規化日期')
                    if boundary['status']=='unknown':
                        check(boundary['date_expression'] is None and not boundary['evidence'] and 'event_type' not in boundary,'未知稱號端點不得暗補日期或事件')
                    else:
                        check(bool(boundary['evidence']),'稱號時段事件缺少證據')
                        allowed=('grant','posthumous_grant','posthumous_naming','self_proclamation','accession','demotion') if endpoint=='start' else ('deposition','renunciation','abolition','explicit_end')
                        check(boundary['event_type'] in allowed,'稱號端點事件類型無效，死亡或首次用稱不得自動替代起訖')
                        for e in boundary['evidence']:title_evidence(e)
                        date=boundary['date_expression']
                        check(date is None or isinstance(date,str) and bool(date) and any(date in e['quote'] for e in boundary['evidence']),'稱號日期表述不在端點證據')
                        if 'normalized_date' in boundary:
                            check(isinstance(date, str) and bool(date) or parallel_event_date(boundary['normalized_date']), '稱號數字紀年須有原始日期表述')
                            validate_date_evidence(boundary['normalized_date'], boundary['evidence'], date)
                        if 'normalized_date_range' in boundary:
                            try:
                                from scripts.date_ranges import year_range_errors
                            except ModuleNotFoundError:
                                from date_ranges import year_range_errors
                            check('normalized_date' not in boundary, '稱號單年與範圍不可同時採用')
                            year_window = boundary['normalized_date_range']
                            range_expression = date
                            if isinstance(year_window, dict) and 'parallel_event' in year_window:
                                parallel = dict(year_window, basis=year_window['parallel_event'])
                                valid = date is None and parallel_event_date(parallel)
                                check(valid, '稱號跨年範圍平行事件對讀無效')
                                errors.extend(table_title_range_errors(year_window, h, endpoint, tables, boundary))
                                if valid:
                                    range_expression = year_window['parallel_event']['source_event_quote']
                            errors.extend(year_range_errors(year_window, boundary['evidence'], range_expression))
                            errors.extend(table_regnal_range_errors(year_window, date, tables, mentions))
                check(period['start']['status']==('unknown' if h['mode']=='attestation' else 'source_event'),'稱號起點與授予／用稱種類不符')
                if h['mode']!='attestation':check(period['start'].get('event_type')==h['mode'],'稱號起點與事件種類不符')
        aids=set()
        # Table-native title assertions retain cells and composed column dates.
        for path in (root/'corpus').glob('*/*-table-title-events.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            table=tables.get(d.get('table_id'))
            check(d.get('record_type')=='table_title_holding_assertion_set' and bool(table)
                  and d.get('chapter_id')==table['source']['chapter_id'], '表格原生稱號集來源或篇ID不符')
            try:
                from scripts.table_title_holdings import table_title_errors
            except ImportError:
                from table_title_holdings import table_title_errors
            for h in d.get('holdings',[]):
                check(h.get('table_title_basis',{}).get('table_id')==d.get('table_id'),'表格稱號不得跨集換來源')
                check(h.get('id') not in title_ids,'稱號持有 ID 重複');title_ids.add(h.get('id'))
                errors.extend(table_title_errors(h,tables,pids))
                for a in h.get('attestations',[]):
                    check(a.get('id') not in title_occurrence_ids,'稱號用稱 ID 重複');title_occurrence_ids.add(a.get('id'))

        for path in (root/'corpus').glob('*/*-assertions.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_assertion_set','人物陳述集類型不符')
            check(d['chapter_id'] in chapters or d['chapter_id'] in table_chapters,'人物陳述集篇不存在')
            for a in d['assertions']:
                check(a['id'] not in aids,'人物陳述 ID 重複');aids.add(a['id'])
                check(a['subject_person_id'] in pids and a['object_person_id'] in pids,'人物陳述引用未知人物')
                check(a['subject_person_id']!=a['object_person_id'],'人物陳述關係自環')
                check(a['predicate'] in ('father','mother','stepmother','adoptive_mother','spouse','brother','sister','paternal_uncle','maternal_uncle','kinship_generation','agnatic_cousin','grandfather','grandmother','great_grandfather','ancestor','kinship_unspecified','affinity_unspecified','teacher'),'人物陳述關係類型未知')
                check(a['status']=='source_attested' and bool(a['evidence']),'人物陳述未有來源證據')
                qualifiers = a.get('qualifiers', {})
                if a['predicate'] == 'teacher' or qualifiers.get('relationship_basis') == 'teaching':
                    term = qualifiers.get('source_term')
                    valid = (a['predicate'] == 'teacher' and qualifiers.get('relationship_basis') == 'teaching'
                             and isinstance(term, str) and bool(term)
                             and any(marker in term for marker in ('學', '教', '受', '傳', '弟子', '師')))
                    for e in a['evidence']:
                        hit = paragraphs.get(e.get('paragraph_id'))
                        if not hit:
                            valid = False
                            continue
                        quote = e.get('quote', '')
                        starts = [i for i in range(len(hit[1]['text']) + 1) if quote and hit[1]['text'].startswith(quote, i)]
                        valid = valid and isinstance(term, str) and term in quote
                        for role, endpoint in (('subject', 'subject_person_id'), ('object', 'object_person_id')):
                            anchors = [m for m in hit[1]['mentions'] if m['id'] == e.get(role + '_person_mention_id')]
                            valid = valid and len(anchors) == 1 and anchors[0].get('person_id') == a[endpoint] and any(
                                i <= anchors[0]['start'] and anchors[0]['end'] <= i + len(quote) for i in starts)
                    check(valid, '師承須有學教原詞及同引句學生老師雙錨點，不得改作親屬')
                if 'succession' in qualifiers:
                    try:
                        from scripts.title_successions import succession_valid
                    except ModuleNotFoundError:
                        from title_successions import succession_valid
                    check(succession_valid(a, title_records, paragraphs),
                          '嗣位原詞須有父子、前任爵位及同段人物錨點，不得虛構爵名或起訖')
                if a['predicate'] == 'maternal_uncle':
                    check(qualifiers.get('source_term') == '姊子'
                          and qualifiers.get('generation_difference') == -1
                          and qualifiers.get('lineage') == 'maternal'
                          and qualifiers.get('mother_person_id') is None
                          and any('姊子' in e.get('quote', '') for e in a['evidence']),
                          '姊子甥舅關係須保留母系世代與未名母親')
                if a['predicate'] == 'grandmother':
                    check(qualifiers.get('source_term') == '外孫'
                          and qualifiers.get('generation_difference') == -2
                          and qualifiers.get('lineage') == 'maternal'
                          and qualifiers.get('mother_person_id') is None
                          and any('外孫' in e.get('quote', '') for e in a['evidence']),
                          '外孫祖母關係須保留母系兩代與原句未名母親')
                if a['predicate'] == 'kinship_generation' or qualifiers.get('source_term') == '大父行':
                    check(a['predicate'] == 'kinship_generation'
                          and qualifiers.get('source_term') == '大父行'
                          and qualifiers.get('generation_difference') == -2
                          and qualifiers.get('lineage') == 'unspecified'
                          and qualifiers.get('direct_ancestor') is None
                          and qualifiers.get('exact_distance') is None
                          and any('大父行' in e.get('quote', '') for e in a['evidence']),
                          '大父行只記祖父輩，不得補直系祖父或親等')
                if a['predicate'] == 'adoptive_mother':
                    check('所母' in qualifiers.get('source_term', '') and any(qualifiers.get('source_term', '') in e.get('quote', '') for e in a['evidence']), '所母關係須保存原詞，不得由一般母稱推定')
                if a['predicate'] == 'stepmother':
                    check(qualifiers.get('source_term') == '後母' and any('後母' in e.get('quote', '') for e in a['evidence']), '後母關係須有原詞證據')
                if 'posthumous_birth' in qualifiers:
                    check(a['predicate'] == 'father' and qualifiers['posthumous_birth'] is True
                          and '遺腹' in qualifiers.get('source_term', ''), '遺腹子欄位須有父親與原詞證據')
                if 'shared_mother' in qualifiers:
                    terms = ('異母',) if qualifiers['shared_mother'] is False else ('同母', '母弟', '母兄')
                    check(a['predicate'] in ('brother', 'sister') and type(qualifiers['shared_mother']) is bool
                          and any(term in qualifiers.get('source_term', '')
                                  and any(term in e.get('quote', '') for e in a['evidence']) for term in terms),
                          '同母或異母關係須有相符原詞與布林值，不補母親端點')
                if qualifiers.get('shared_father') is not None:
                    terms = ('異父',) if qualifiers['shared_father'] is False else ('同父',)
                    check(a['predicate'] in ('brother', 'sister') and type(qualifiers['shared_father']) is bool
                          and any(term in qualifiers.get('source_term', '')
                                  and any(term in e.get('quote', '') for e in a['evidence']) for term in terms),
                          '同父或異父關係須有相符原詞與布林值，不補父親端點')
                if a['predicate'] == 'kinship_unspecified':
                    if qualifiers.get('kinship_basis') == 'external_clan_affiliation':
                        check('外族' in qualifiers.get('source_term', '')
                              and qualifiers.get('lineage') == 'unspecified'
                              and all(key in qualifiers and qualifiers[key] is None for key in
                                      ('generation_difference', 'exact_distance', 'connecting_person_ids'))
                              and not qualifiers.get('kinship_structure')
                              and any(qualifiers.get('source_term', '') in e.get('quote', '') for e in a['evidence']),
                              '外族關係須保留原詞及未知世代、親等與連接人物')
                    else:
                        check(qualifiers.get('source_term') == '有親' and not qualifiers.get('kinship_structure')
                              and any('有親' in e.get('quote', '') for e in a['evidence']),
                              '未定親屬不得補具體親等')
                if a['predicate'] == 'affinity_unspecified':
                    check(qualifiers.get('relationship_basis') == 'marriage_affinity'
                          and qualifiers.get('source_term') and '婚' in qualifiers['source_term']
                          and all(key in qualifiers and qualifiers[key] is None for key in
                                  ('spouse_person_ids', 'connecting_person_ids', 'generation_difference'))
                          and any(qualifiers.get('source_term', '') in e.get('quote', '') for e in a['evidence']),
                          '未明姻親須保存婚原詞，不得補配偶、連接人物或世代')
                if 'kinship_structure' in qualifiers:
                    structure = qualifiers['kinship_structure']
                    check(a['predicate'] == 'agnatic_cousin' and structure.get('lineage') == 'paternal' and structure.get('generation_difference') == 0 and structure.get('collateral') is True, '同世代父系旁親結構無效')
                    check(structure.get('distance') is None and structure.get('common_ancestor_person_id') is None, '未定從親不可補親等或共同祖先')
                    check(structure.get('subject_relative_age') in ('younger', 'older', 'unknown'), '從親長幼欄位無效')
                if 'birth_order' in qualifiers:
                    order = qualifiers['birth_order']
                    check(a['predicate'] in ('father', 'mother') and order.get('parent_person_id') == a['object_person_id'], '排行父母端點不符')
                    check(order.get('scope') in ('sons_of_parent', 'daughters_of_parent', 'children_of_parent'), '排行序列範圍未知')
                    ordinal = order.get('ordinal')
                    check(ordinal is None or type(ordinal) is int and ordinal > 0, '排行序號須為正整數或未知')
                    check(order.get('position') in ('eldest', 'youngest', 'younger_or_youngest', 'unspecified'), '排行位置未知')
                    if order.get('position') == 'eldest': check(ordinal == 1, '長子排行須為一')
                    check(order.get('interpretation_status') in ('source_attested', 'ambiguous'), '排行判讀狀態無效')
                if 'relative_birth_order' in qualifiers:
                    order = qualifiers['relative_birth_order']
                    check(a['predicate'] in ('brother', 'sister', 'agnatic_cousin'), '相對排行須為同輩親屬')
                    check({order.get('older_person_id'), order.get('younger_person_id')} == {a['subject_person_id'], a['object_person_id']}, '相對排行端點不符')
                    check(order.get('operator') == 'lt' and order.get('scope') == ('agnatic_cousins' if a['predicate'] == 'agnatic_cousin' else 'siblings'), '相對排行運算或範圍未知')
                    for key in ('older_ordinal', 'younger_ordinal'):
                        value = order.get(key)
                        check(value is None or type(value) is int and value > 0, '相對排行序號無效')
                context=a.get('context')
                adjacent=None
                quoted_endpoints=[]
                if context is not None:
                    check(isinstance(context,dict),'人物陳述承接格式無效')
                    if isinstance(context,dict):
                        ids=context.get('paragraph_ids')
                        order=[p['id'] for p in chapters.get(d['chapter_id'],{}).get('paragraphs',[])]
                        valid=(context.get('kind')=='adjacent_paragraphs' and isinstance(ids,list)
                               and len(ids)==2 and all(isinstance(i,str) and i in order for i in ids)
                               and ids==[e['paragraph_id'] for e in a['evidence']]
                               and order.index(ids[1])==order.index(ids[0])+1)
                        check(valid,'人物陳述承接須為同篇依原序相鄰兩段證據')
                        if valid:adjacent=ids
                for e in a['evidence']:
                    if e.get('kind') == 'table_cell':
                        errors.extend(table_evidence_errors(e, tables, a['subject_person_id'], a['object_person_id']))
                        check(e.get('chapter_id') == d['chapter_id'] and adjacent is None,
                              '親屬表格證據須屬同一表篇，不得冒作段落承接')
                        term = qualifiers.get('source_term')
                        check(isinstance(term, str) and bool(term) and term in e.get('quote', ''),
                              '親屬表格證據缺少相符關係原詞')
                        continue
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and hit[0]==d['chapter_id']==e['chapter_id'] and e['quote'] in hit[1]['text'],'人物陳述引句與所屬篇不符')
                    check(chapters.get(e['chapter_id'],{}).get('source_id')==e['source_id'],'人物陳述來源 ID 不符')
                    if hit:
                        local={m['person_id'] for m in hit[1]['mentions'] if m['kind']=='person'}
                        if adjacent is None:
                            check(a['subject_person_id'] in local and a['object_person_id'] in local,'人物陳述端點未見於證據段落')
                        else:
                            quote=e['quote'];text=hit[1]['text']
                            starts=[i for i in range(len(text)+1) if text.startswith(quote,i)]
                            quoted={m['person_id'] for m in hit[1]['mentions'] if m['kind']=='person'
                                    and any(i<=m['start'] and m['end']<=i+len(quote) for i in starts)}
                            quoted_endpoints.append(quoted)
                if adjacent is not None:
                    check(len(quoted_endpoints)==2 and a['object_person_id'] in quoted_endpoints[0]
                          and a['subject_person_id'] in quoted_endpoints[1],
                          '人物陳述承接的前段客體及後段主體未見於引句')
        proposal_ids = set()
        for chapter in chapters.values():
            for proposal in chapter['annotation'].get('title_proposals', []):
                check(proposal.get('id') and proposal['id'] not in proposal_ids, '稱號提議 ID 缺失或重複')
                proposal_ids.add(proposal.get('id'))
                errors.extend(title_proposal_errors(proposal, chapter, set(pids)))
        age_ids = set(); age_report_groups = {}
        for chapter in chapters.values():
            for age in chapter['annotation'].get('age_assertions', []):
                check(age['id'] not in age_ids, '年齡記錄 ID 重複'); age_ids.add(age['id'])
                number = age.get('source_number'); parsed = source_age_number(number)
                if 'bounds' in age:
                    bounds = age.get('bounds'); group = age.get('group_reference')
                    if group is not None:
                        check(age.get('value') is None and parsed is not None and isinstance(bounds, dict)
                              and bounds == {'lower': parsed, 'lower_inclusive': False, 'upper': None, 'upper_inclusive': None}
                              and age.get('source_term') in ('年皆' + str(number) + '有餘', '年' + str(number) + '餘'), '來源年齡界限與有餘原詞不符')
                        keys = set(group) if isinstance(group, dict) else set()
                        ids = group.get('person_ids') if isinstance(group, dict) else None
                        members = ids if isinstance(ids, list) else []
                        complete_four = (keys == {'source_term', 'naming_term', 'person_ids'}
                                         and group.get('source_term') == '四人從太子' and len(members) == 4)
                        named_subset = (keys == {'source_term', 'naming_term', 'person_ids', 'additional_members_unknown'}
                                        and group.get('additional_members_unknown') is True
                                        and isinstance(group.get('source_term'), str) and group['source_term'].endswith('等')
                                        and isinstance(group.get('naming_term'), str) and bool(group['naming_term'])
                                        and group['naming_term'] in group['source_term'])
                        check((complete_four or named_subset) and bool(members)
                              and all(isinstance(i, str) for i in members)
                              and len(set(members)) == len(members) and age['person_id'] in members,
                              '群體報齡具名範圍或未名成員不符')
                        for evidence in age.get('evidence', []):
                            hit = paragraphs.get(evidence.get('paragraph_id'))
                            if isinstance(group, dict) and hit:
                                phrase = group.get('naming_term')
                                starts = [i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(phrase, i)] if isinstance(phrase, str) and phrase else []
                                named = {m['person_id'] for m in hit[1]['mentions'] if m['kind'] == 'person'
                                         and any(i <= m['start'] and m['end'] <= i + len(phrase) for i in starts)}
                                check(isinstance(phrase, str) and bool(phrase) and phrase in evidence.get('quote', '')
                                      and isinstance(group.get('source_term'), str) and group['source_term'] in evidence.get('quote', '')
                                      and named == {i for i in members if isinstance(i, str)}, '群體報齡具名名單未見於引句')
                    elif age.get('reporting_status') == 'upper_bound_report':
                        check(age.get('value') is None and parsed is not None
                              and bounds == {'lower': None, 'lower_inclusive': None, 'upper': parsed, 'upper_inclusive': False}
                              and age.get('source_term') in ('年未滿' + str(number), '未滿' + str(number) + '歲', '未滿' + str(number) + '歳')
                              and age.get('source_qualification') is None and not age.get('report_group_id'),
                              '來源未滿報齡須保存開放上界及原詞，不得補確切歲數')
                    elif age.get('reporting_status') == 'direct_report':
                        check(age.get('value') is None and parsed is not None
                              and bounds == {'lower': parsed, 'lower_inclusive': False, 'upper': None, 'upper_inclusive': None}
                              and age.get('source_term') in (str(number) + '餘歲', str(number) + '有餘歲', '年' + str(number) + '餘')
                              and age.get('source_qualification') is None and not age.get('report_group_id'),
                              '直接報齡餘歲須保存開放下界及原詞，不得補限定詞或傳聞分組')
                    else:
                        check(age.get('value') is None and parsed is not None
                              and bounds == {'lower': parsed, 'lower_inclusive': False, 'upper': None, 'upper_inclusive': None}
                              and age.get('source_term') == str(number) + '餘歲', '個人報齡餘歲界限與原詞不符')
                        marker = age.get('source_qualification')
                        report_id = age.get('report_group_id')
                        if isinstance(report_id, str) and report_id:
                            report_scope = (age.get('person_id'), chapter['id'],
                                tuple(sorted((e.get('source_id', ''), e.get('paragraph_id', '')) for e in age.get('evidence', []))))
                            existing = age_report_groups.setdefault(report_id, {'scope': report_scope, 'statuses': []})
                            check(existing['scope'] == report_scope, '同組報齡須同人物及來源段落')
                            existing['statuses'].append(age.get('reporting_status'))
                        else:
                            check(False, '個人報齡分組ID無效')
                        check(bool(age.get('report_group_id')) and (marker, age.get('reporting_status')) in
                              (('蓋', 'qualified_report'), ('或言', 'alternative_report'))
                              and isinstance(age.get('qualified_source_term'), str)
                              and age['qualified_source_term'].startswith(str(marker))
                              and age['qualified_source_term'].endswith(str(age.get('source_term')))
                              and any(age['qualified_source_term'] in e.get('quote', '') for e in age.get('evidence', [])), '個人報齡缺來源限定詞或傳聞狀態')
                else:
                    check(type(age.get('value')) is int and parsed is not None and age['value'] == parsed
                          and age.get('source_term') in ('年' + str(number), str(number) + '歲', str(number) + '歳'), '來源年齡數值與原詞不符')
                check(age.get('counting') == 'unspecified_source_age' and age.get('unit') == 'source_age_years'
                      and age.get('birth_year') is None and age.get('status') == 'source_attested',
                      '來源年齡不得推定計歲方式或出生年')
                check(age['person_id'] in pids and bool(age['evidence']), '來源年齡缺人物或證據')
                for evidence in age['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id']); mention = mentions.get(evidence.get('person_mention_id'))
                    check(bool(hit) and hit[0] == chapter['id'] == evidence['chapter_id']
                          and evidence['source_id'] == chapter['source_id'] and evidence['quote'] in hit[1]['text']
                          and age['source_term'] in evidence['quote'], '來源年齡引句不符')
                    check(bool(mention) and mention[1] == evidence['paragraph_id'] and mention[2]['person_id'] == age['person_id'], '來源年齡人物錨點不符')
                if 'report_repetition_of' in age:
                    reports = chapter['annotation']['age_assertions']
                    target = next((r for r in reports[:reports.index(age)] if r['id'] == age['report_repetition_of']), None)
                    check(bool(target) and target['person_id'] == age['person_id']
                          and target.get('value') == age.get('value') and target.get('bounds') == age.get('bounds')
                          and target.get('unit') == age.get('unit') and target.get('counting') == age.get('counting')
                          and bool(age.get('interpretation_note')), '報齡重述須指同篇前筆同人物及相同年數，不得補年齡變化')
                if 'normalized_date_range' in age:
                    try:
                        from scripts.date_ranges import year_range_errors
                    except ImportError:
                        from date_ranges import year_range_errors
                    check('normalized_date' not in age, '來源報齡跨年範圍不得另填確定單年')
                    errors.extend(year_range_errors(age['normalized_date_range'], age['evidence'], age.get('date_expression')))
                    errors.extend(table_regnal_range_errors(age['normalized_date_range'], age.get('date_expression'), tables, mentions))
                if 'normalized_date' in age:
                    errors.extend(normalized_date_errors(age['normalized_date']))
                    check(age['normalized_date'].get('original_quote') in [e['quote'] for e in age['evidence']], '來源年齡紀年原句不符')
            for age in chapter['annotation'].get('age_difference_assertions', []):
                check(age['id'] not in age_ids, '年齡差記錄ID重複'); age_ids.add(age['id'])
                parsed = source_age_number(age.get('source_number'))
                check(type(age.get('value')) is int and parsed is not None and age['value'] == parsed and parsed > 0
                      and age.get('comparison') == 'younger_than', '年齡差數值或方向不符')
                check(age.get('person_id') in pids and age.get('reference_person_id') in pids
                      and age.get('person_id') != age.get('reference_person_id'), '年齡差須有兩個不同人物')
                check(age.get('unit') == 'source_age_years' and age.get('counting') == 'unspecified_source_age'
                      and age.get('birth_year') is None and age.get('date_expression') is None
                      and 'normalized_date' not in age and age.get('status') == 'source_attested', '年齡差不得推生年日期或計歲方式')
                check(bool(age.get('evidence')) and bool(age.get('interpretation_note')) and bool(age.get('reviewer'))
                      and age.get('human_reviewed') is False, '年齡差缺來源或判讀')
                for evidence in age.get('evidence', []):
                    hit = paragraphs.get(evidence.get('paragraph_id'))
                    subject = mentions.get(evidence.get('person_mention_id'))
                    reference = mentions.get(evidence.get('reference_person_mention_id'))
                    quote = evidence.get('quote')
                    valid = bool(hit) and hit[0] == chapter['id'] == evidence.get('chapter_id') and evidence.get('source_id') == chapter['source_id']
                    check(valid and isinstance(quote, str) and bool(quote) and quote in hit[1]['text'], '年齡差来源引句不符'.replace('来源','來源'))
                    for anchor, pid in [(subject, age.get('person_id')), (reference, age.get('reference_person_id'))]:
                        check(bool(anchor) and anchor[1] == evidence.get('paragraph_id') and anchor[2].get('person_id') == pid, '年齡差人物錨點不符')
                        if valid and anchor and isinstance(quote, str):
                            check(any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                      for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(quote, i)), '年齡差人物未在引句中')
                    if reference and isinstance(quote, str):
                        terms = ['少' + reference[2]['surface'] + str(age.get('source_number')) + suffix for suffix in ('歲', '歳')]
                        check(age.get('source_term') in terms and age.get('source_term') in quote, '年齡差原詞與參考人物不符')
        for report in age_report_groups.values():
            check('qualified_report' in report['statuses'], '報齡替代傳聞缺同組主報齡')
        address_ids = set()
        for path in (root / 'corpus').glob('*/*-addresses.json'):
            record = json.loads(path.read_text(encoding='utf-8'))
            check(record['record_type'] == 'person_address_assertion_set' and record['chapter_id'] in chapters, '地址主張集格式或篇不存在')
            for address in record['assertions']:
                check(address['id'] not in address_ids, '地址主張 ID 重複'); address_ids.add(address['id'])
                check(address['person_id'] in pids and address['status'] == 'source_attested', '地址人物或狀態無效')
                check(address['relation'] in ('biographical_origin', 'ancestral_origin', 'native_place', 'birth_place', 'residence', 'death_place', 'migration_origin', 'migration_destination', 'burial_place', 'polity_lineage_affiliation', 'source_locality_designation', 'service_location', 'fief'), '地址關係類型未知')
                if address['relation'] == 'fief' or 'fief_kind' in address.get('qualifiers', {}):
                    kind = address.get('qualifiers', {}).get('fief_kind')
                    word = {'tangmu_estate':'湯沐邑', 'maintenance_allocation':'奉', 'territorial_grant':'賜', 'approved_enfeoffment':'許之', 'household_revenue':'食'}.get(kind)
                    if kind == 'household_revenue':
                        check(bool(re.fullmatch(r'食.+[萬千百十〇零一二三四五六七八九兩0-9]+戶', address.get('source_term', ''))), '食戶地望須保存食地名與戶數原語，不得當人口或居處')
                    if kind == 'approved_enfeoffment':
                        check('封' in address.get('source_term', '') and '許之' in address.get('source_term', ''), '准封地望須保存提請與明示允許，不得只據請封記實授')
                    check(address['relation'] == 'fief' and bool(word)
                          and isinstance(address.get('source_term'), str) and word in address['source_term'],
                          '食邑主張須保存湯沐邑或奉原詞及類型，不得改為籍貫')
                if 'reported_duration' in address:
                    duration = address['reported_duration']
                    check(address['relation'] == 'residence' and isinstance(duration, dict)
                          and duration.get('unit') == 'residence_year'
                          and duration.get('counting') == 'unspecified_source_years'
                          and duration.get('status') == 'source_attested'
                          and type(duration.get('value')) is int and duration['value'] > 0
                          and source_age_number(duration.get('source_number')) == duration['value']
                          and isinstance(duration.get('source_term'), str)
                          and duration['source_term'].endswith(duration['source_number'] + '年')
                          and duration.get('evidence') == address['evidence']
                          and all(duration['source_term'] in e['quote'] for e in address['evidence']),
                          '居留來源年數須有數值、原數詞與同項證據，不得當官爵任期或推曆日')
                if address['relation'] == 'source_locality_designation':
                    scope = address.get('qualifiers', {})
                    check(scope.get('designation_kind') == 'geographical_person_reference'
                          and 'origin_or_residence' in scope and scope['origin_or_residence'] is None
                          and address['place']['source_name'] in address['source_term'],
                          '來源地稱須保留未明籍貫或居所，不得轉成出生地')
                if address['relation'] == 'service_location':
                    position = address.get('qualifiers', {}).get('source_position')
                    check(bool(position) and position in address['source_term']
                          and address['place']['source_name'] in address['source_term'], '任事地須有來源職位及原地名，不作居所')
                if address['relation'] == 'polity_lineage_affiliation':
                    check(address.get('qualifiers', {}).get('affiliation_kind') == 'royal_lineage'
                          and address['place']['source_name']+'之' in address['source_term']
                          and re.search('公子|公孫|宗室', address['source_term']) is not None, '宗族政體地望須有來源身份詞，不改作出生籍貫')
                if address['relation'] == 'ancestral_origin':
                    scope = address.get('qualifiers', {})
                    check(scope.get('subject_scope') == 'ancestors_unspecified'
                          and scope.get('ancestor_person_id') is None
                          and scope.get('generation_distance') is None, '祖先出身不得暗補具名祖先或世代，須明示範圍')
                check(bool(address['place']['source_name']) and bool(address['evidence']), '地址原地名或證據缺失')
                if 'normalized_date' in address:
                    date = address['normalized_date']
                    errors.extend(normalized_date_errors(date))
                    if isinstance(date, dict):
                        for evidence in date.get('evidence', []):
                            hit = paragraphs.get(evidence['paragraph_id'])
                            valid = bool(hit) and hit[0] == evidence['chapter_id']
                            check(valid and evidence['quote'] in hit[1]['text'], '紀年換算證據篇段不符')
                            if valid: check(chapters[hit[0]]['source_id'] == evidence['source_id'], '紀年換算來源 ID 不符')
                        check(any(date.get('original_quote') in e['quote'] for e in date.get('evidence', [])), '紀年換算原句未見於證據')
                for evidence in address['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id'])
                    valid = bool(hit) and hit[0] == record['chapter_id'] == evidence['chapter_id']
                    check(valid and evidence['quote'] in hit[1]['text'], '地址證據篇段不符')
                    if valid:
                        check(address['place']['source_name'] in evidence['quote'] and address['source_term'] in evidence['quote'], '地址原詞不在證據')
                        check(address['date_expression'] is None or address['date_expression'] in evidence['quote'], '地址日期不在證據')
                        context = evidence.get('context'); carried = False
                        if context is not None:
                            previous = paragraphs.get(context.get('paragraph_id')) if isinstance(context, dict) else None
                            anchor = mentions.get(context.get('person_mention_id')) if isinstance(context, dict) else None
                            order = [p['id'] for p in chapters[record['chapter_id']]['paragraphs']]
                            quote = context.get('quote') if isinstance(context, dict) else None
                            ids = context.get('intervening_paragraph_ids') if isinstance(context, dict) else None
                            adjacent = (isinstance(context, dict)
                                and set(context) == {'kind', 'paragraph_id', 'person_mention_id', 'quote'}
                                and context.get('kind') == 'previous_paragraph_subject'
                                and bool(previous) and context['paragraph_id'] in order
                                and order.index(evidence['paragraph_id']) == order.index(context['paragraph_id']) + 1)
                            continuous = (isinstance(context, dict)
                                and set(context) == {'kind', 'paragraph_id', 'person_mention_id', 'quote', 'intervening_paragraph_ids'}
                                and context.get('kind') == 'prior_paragraph_subject' and bool(previous)
                                and context['paragraph_id'] in order and isinstance(ids, list)
                                and order.index(context['paragraph_id']) < order.index(evidence['paragraph_id'])
                                and ids == order[order.index(context['paragraph_id']) + 1:order.index(evidence['paragraph_id'])])
                            carried = ((adjacent or continuous) and bool(anchor)
                                and previous[0] == record['chapter_id']
                                and anchor[1] == context['paragraph_id'] and anchor[2]['person_id'] == address['person_id']
                                and isinstance(quote, str) and bool(quote) and quote in previous[1]['text']
                                and any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                        for i in range(len(previous[1]['text'])) if previous[1]['text'].startswith(quote, i))
                                and bool(address.get('interpretation_note')))
                            check(carried, '地址主語承接須有同篇人物錨點、引句及完整中間段落')
                        check(carried or any(m.get('person_id') == address['person_id'] for m in hit[1]['mentions']), '地址人物未見於證據段')
                        check(chapters[hit[0]]['source_id'] == evidence['source_id'], '地址來源 ID 不符')
        life_event_ids = set()
        for path in list((root / 'corpus').glob('*/*-life-events.json')) + list((root / 'corpus').glob('*/*-person-events.json')):
            record = json.loads(path.read_text(encoding='utf-8'))
            check(record.get('record_type') in ('person_life_event_assertion_set', 'person_event_assertion_set') and record.get('chapter_id') in chapters, '生卒事件集類型或篇不存在')
            for event in record['events']:
                check(event['id'] not in life_event_ids, '生卒事件ID重複'); life_event_ids.add(event['id'])
                check(event['person_id'] in pids and event['event_type'] in (('birth', 'death') if record.get('record_type') == 'person_life_event_assertion_set' else ('recruitment', 'burial', 'office_non_reinstatement', 'office_restoration', 'diplomatic_service')), '生卒事件人物或類型無效')
                check(event.get('status') == 'source_attested' and bool(event.get('evidence')) and bool(event.get('interpretation_note')) and bool(event.get('reviewer')) and event.get('human_reviewed') is False, '生卒事件缺少來源或判讀')
                if record.get('record_type') == 'person_event_assertion_set' and event['event_type'] == 'recruitment':
                    check(any('徵' in e.get('quote', '') for e in event.get('evidence', [])), '徵召事件缺少原文徵召用語')
                if event['event_type'] == 'diplomatic_service':
                    duration = event.get('reported_duration', {}); number = duration.get('source_number')
                    place = event.get('polity_source_name'); term = duration.get('source_term')
                    check(isinstance(place, str) and bool(place) and isinstance(number, str)
                          and type(duration.get('value')) is int and duration['value'] > 0
                          and source_age_number(number) == duration['value']
                          and duration.get('unit') == 'service_year'
                          and duration.get('counting') == 'unspecified_source_years'
                          and duration.get('status') == 'source_attested'
                          and term == '事' + str(place) + str(number) + '年'
                          and term in event.get('source_term', '')
                          and duration.get('evidence') == event.get('evidence')
                          and any(event.get('source_term', '') in e.get('quote', '') for e in event.get('evidence', [])),
                          '使外任事年數須有事國原詞、相符數字及任務單位，不作爵位任期')
                if event['event_type'] == 'burial':
                    term = event.get('source_term')
                    check(isinstance(term, str) and '葬' in term and any(term in e.get('quote', '') for e in event.get('evidence', [])), '埋葬事件須有原文明示葬詞及相符引句')
                if event['event_type'] in ('office_non_reinstatement', 'office_restoration'):
                    term = event.get('source_term')
                    required = '不復官' if event['event_type'] == 'office_non_reinstatement' else '復就故官'
                    check(isinstance(term, str) and required in term
                          and all(key in event and event[key] is None for key in ('office_title', 'title_holding_id'))
                          and any(term in e.get('quote', '') for e in event.get('evidence', [])),
                          '未名官職不復任或恢復須保留原詞，不得補官名或已知持職連結')
                expression = event.get('date_expression')
                check(expression is None or isinstance(expression, str) and bool(expression), '生卒日期表述無效')
                date_context = event.get('date_context')
                continuous_date = False
                if date_context is not None:
                    order = [p['id'] for p in chapters.get(record['chapter_id'], {}).get('paragraphs', [])]
                    ids = date_context.get('paragraph_ids') if isinstance(date_context, dict) else None
                    date_paragraph_id = (date_context.get('date_paragraph_id', ids[0] if isinstance(ids, list) and ids else None)
                                         if isinstance(date_context, dict) else None)
                    continuous_date = (isinstance(date_context, dict)
                        and date_context.get('kind') == 'continuous_paragraphs'
                        and isinstance(ids, list) and 2 <= len(ids) <= 4
                        and ids == [e['paragraph_id'] for e in event['evidence']]
                        and all(pid in order for pid in ids)
                        and all(order.index(ids[i]) + 1 == order.index(ids[i + 1]) for i in range(len(ids) - 1))
                        and isinstance(expression, str) and bool(expression)
                        and date_paragraph_id in ids
                        and expression in next((e['quote'] for e in event['evidence'] if e['paragraph_id'] == date_paragraph_id), '')
                        and bool(date_context.get('rationale')))
                    if isinstance(date_context, dict) and date_context.get('kind') == 'same_event_attestation':
                        primary = event['evidence'][0]
                        continuous_date = (set(date_context) == {'kind', 'paragraph_ids', 'date_paragraph_id', 'rationale'}
                            and isinstance(ids, list) and len(ids) >= 2 and len(set(ids)) == len(ids)
                            and ids == [e['paragraph_id'] for e in event['evidence']]
                            and all(pid in order for pid in ids)
                            and date_context.get('date_paragraph_id') == primary['paragraph_id']
                            and isinstance(expression, str) and bool(expression) and expression in primary['quote']
                            and bool(event.get('source_term')) and event['source_term'] in primary['quote']
                            and bool(date_context.get('rationale')))
                        check(continuous_date, '同一生卒事件回述須以首筆明示事件引句作紀年錨點')
                    else:
                        check(continuous_date, '生卒紀年承接須有連續同篇段落與明示日期段')
                for evidence in event['evidence']:
                    hit = paragraphs.get(evidence['paragraph_id']); mention = mentions.get(evidence.get('person_mention_id'))
                    valid = bool(hit) and hit[0] == evidence['chapter_id'] == record['chapter_id']
                    check(valid and evidence['quote'] in hit[1]['text'] and chapters.get(evidence['chapter_id'], {}).get('source_id') == evidence['source_id'], '生卒事件來源引句不符')
                    carried_subject = False
                    context = evidence.get('context')
                    if context is not None:
                        order = [p['id'] for p in chapters.get(record['chapter_id'], {}).get('paragraphs', [])]
                        previous = paragraphs.get(context.get('paragraph_id')) if isinstance(context, dict) else None
                        anchor = mentions.get(context.get('person_mention_id')) if isinstance(context, dict) else None
                        quote = context.get('quote') if isinstance(context, dict) else None
                        ids = context.get('intervening_paragraph_ids') if isinstance(context, dict) else None
                        carried_subject = (isinstance(context, dict) and set(context) == {'kind', 'paragraph_id', 'person_mention_id', 'quote', 'intervening_paragraph_ids'}
                            and context.get('kind') == 'prior_paragraph_subject' and bool(previous) and bool(anchor)
                            and bool(hit) and previous[0] == hit[0] == record['chapter_id']
                            and context['paragraph_id'] in order and evidence['paragraph_id'] in order
                            and isinstance(ids, list) and len(ids) <= 1
                            and order.index(evidence['paragraph_id']) - order.index(context['paragraph_id']) == len(ids) + 1
                            and ids == order[order.index(context['paragraph_id']) + 1:order.index(evidence['paragraph_id'])]
                            and anchor[1] == context['paragraph_id'] and anchor[2]['person_id'] == event['person_id']
                            and isinstance(quote, str) and bool(quote) and quote in previous[1]['text']
                            and any(i <= anchor[2]['start'] and anchor[2]['end'] <= i + len(quote)
                                    for i in range(len(previous[1]['text'])) if previous[1]['text'].startswith(quote, i))
                            and bool(event.get('source_term')) and event['source_term'] in evidence['quote'])
                        check(carried_subject, '生卒主語承接須有近前同篇人物錨點、引句及完整中間段落')
                    check(carried_subject or bool(mention) and mention[1] == evidence['paragraph_id'] and mention[2]['person_id'] == event['person_id'], '生卒事件人物錨點不符')
                    if valid and mention:
                        starts = [i for i in range(len(hit[1]['text'])) if hit[1]['text'].startswith(evidence['quote'], i)]
                        check(any(i <= mention[2]['start'] and mention[2]['end'] <= i + len(evidence['quote']) for i in starts), '生卒人物錨點不在引句中')
                    check(expression is None or continuous_date or expression in evidence['quote'], '生卒日期未見於事件引句')
                if 'normalized_date_range' in event:
                    try:
                        from scripts.date_ranges import year_range_errors
                    except ImportError:
                        from date_ranges import year_range_errors
                    check('normalized_date' not in event, '生卒或事件跨年範圍不得另填確定單年')
                    year_window = event['normalized_date_range']
                    range_expression = expression
                    if isinstance(year_window, dict) and 'parallel_event' in year_window:
                        parallel = dict(year_window, basis=year_window['parallel_event'])
                        valid = expression is None and parallel_event_date(parallel)
                        check(valid, '生卒跨年範圍平行事件對讀無效')
                        if valid:
                            range_expression = year_window['parallel_event']['source_event_quote']
                    errors.extend(year_range_errors(year_window, event['evidence'], range_expression))
                    errors.extend(table_regnal_range_errors(year_window, expression, tables, mentions))
                if 'normalized_date' in event:
                    date = event['normalized_date']; errors.extend(normalized_date_errors(date))
                    check(isinstance(expression, str) and bool(expression) or parallel_event_date(date), '生卒數字紀年缺原日期表述')
                    if isinstance(date, dict):
                        check(date.get('original_quote') in [e['quote'] for e in event['evidence']], '生卒數字紀年原句不符')
                        check(date.get('evidence') == event['evidence'], '生卒数值證據與事件不符'.replace('数','數'))
        try:
            from scripts.life_event_dates import date_decision_errors, date_record_scope_errors
        except ImportError:
            from life_event_dates import date_decision_errors, date_record_scope_errors
        dated_events = {e['id']: e for path in (root / 'corpus').glob('*/*-life-events.json')
                        for e in json.loads(path.read_text())['events']}
        date_equivalences = [e for path in (root / 'corpus').glob('*/*-equivalences.json')
                             for e in json.loads(path.read_text())['decisions']]
        date_decision_ids = set(); date_candidate_scopes = set()
        for path in (root / 'corpus').glob('*/*-date-decisions.json'):
            record = json.loads(path.read_text())
            check(record['record_type'] == 'life_event_date_decision_set' and record['work_id'] in works,
                  '生卒紀年取捨集格式或著作無效')
            errors.extend(date_record_scope_errors(record, chapters, works))
            for decision in record['decisions']:
                check(decision['id'] not in date_decision_ids, '生卒紀年取捨 ID 重複')
                date_decision_ids.add(decision['id'])
                errors.extend(date_decision_errors(decision, dated_events, date_equivalences, pids))
                candidates = set(decision['candidate_event_ids'])
                check(not date_candidate_scopes.intersection(candidates), '同一生卒事件不得有多項紀年預設')
                date_candidate_scopes.update(candidates)
        try:
            from .family_assemblies import load_assemblies
            from .person_bundle import load_catalog
        except ImportError:
            try:
                from scripts.family_assemblies import load_assemblies
                from scripts.person_bundle import load_catalog
            except ModuleNotFoundError:
                from family_assemblies import load_assemblies
                from person_bundle import load_catalog
        catalog = load_catalog(root)
        load_assemblies(root, catalog)
        def citation_dimensions(value):
            if isinstance(value, dict):
                if all(key in value for key in ('paragraph_id','chapter_id','source_id')):
                    hit = paragraphs.get(value['paragraph_id'])
                    if hit:
                        chapter = chapters[hit[0]]
                        check(all(value[key] == chapter[key] for key in ('work_id','book_id') if key in value),
                              '引文著作卷ID與實際來源不符')
                for item in value.values(): citation_dimensions(item)
            elif isinstance(value, list):
                for item in value: citation_dimensions(item)
        for record in catalog[1]: citation_dimensions(record)
        check(progress['active_work_id'] in works,'進度的著作不存在')
        for b in progress['books']:
            check(chapter_books.get(b['chapter_id'])==b['book_id'],'進度卷篇不符')
            chapter=chapters.get(b['chapter_id'],{})
            if any(p.get('annotation_status') in ('pending','in_progress') for p in chapter.get('paragraphs',[])):
                check(b['person_status']=='in_progress' and not b['complete'],'有待標註段落的進度不得標為完成或首輪完成')
            if b['complete']: check(b['person_status']=='reviewed','初步標註不得宣稱完成')
    except (KeyError,ValueError,TypeError,OSError,ET.ParseError) as exc:
        errors.append(f'資料結構或 XML 無效：{exc}')
    return errors

def main():
    errors=validate()
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 1
    print('卷篇標註驗證通過：人物與文字引用一致。');return 0
if __name__=='__main__':sys.exit(main())
