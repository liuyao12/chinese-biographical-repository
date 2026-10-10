#!/usr/bin/env python3
"""檢查穩定 ID、字元錨點、人物證據、身份判斷及 XML／JSON 一致性。"""
from pathlib import Path
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]

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
        mentions = {}; paragraphs = {}; chapters = {}; files = {}
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
                    if m['kind'] == 'person': check(m['person_id'] in pids, '提及引用未知人物 ID')
                    elif m['kind'] == 'unresolved': check(m['person_id'] is None and m['status']=='unresolved', '未定提及不得暗選人物')
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
                check(len(candidates)>=2 and len(set(candidates))==len(candidates) and all(pid in pids for pid in candidates),'未決身份候選人物無效')
                check(case.get('status')=='unresolved' and bool(case.get('note')),'未決身份狀態或說明缺失')
                refs=case.get('paragraph_ids',[])
                local={p['id']:p for p in d['paragraphs']}
                check(bool(refs) and all(ref in local for ref in refs),'未決身份段落引用無效')
                supported={m['person_id'] for ref in refs if ref in local for m in local[ref]['mentions'] if m['kind']=='person'}
                check(set(candidates)<=supported,'未決身份缺少各候選人物的段落證據')
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
                if 'text_layer' in p: check(p['text_layer'] in ('received_chapter','witness_appended_bangu_note','witness_appended_suoyin_zan','witness_appended_chu_note','witness_appended_zhengyi_note'),'文字層次無效')
                xm=list(x)
                check(len(xm)==len(p['mentions']), 'XML 提及數不符')
                check(all(e.tag in ('persName','rs') for e in x),'XML 含未知正文標籤')
                for e,m in zip(xm,p['mentions']):
                    check(e.get('id')==m['id'] and e.text==m['surface'], 'XML 提及錨點不符')
                    check(e.tag==('persName' if m['kind']=='person' else 'rs'), 'XML 提及類型不符')
                    check(e.get('ref')==m['person_id'], 'XML 人物引用不符')
                    if m['kind']=='unresolved': check(e.get('type')=='unresolved','XML 未定類型不符')
        check(set(chapter_books)==set(chapters), '著作目錄與文本篇清單不符')
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
        for person in people:
            path = person.get('family_path')
            if path is None:
                check(not (FAMILY.fullmatch(person['id']) and len(person['id']) > 11), '家族後代 ID 缺少有來源的親屬路徑')
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
            expected={mid for mid,hit in mentions.items() if hit[2]['person_id']==p['id']}
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
                check(len(ids)>=2 and len(set(ids))==len(ids) and set(ids).issubset(pids),'同指決定端點無效或重複')
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
                for pid in ids:
                    if pid==canonical:continue
                    check(pid not in canonical_links or canonical_links[pid]==canonical,'同指決定代表衝突')
                    canonical_links[pid]=canonical
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
        for path in (root/'corpus').glob('*/*-titles.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='title_holding_assertion_set','稱號持有集類型不符')
            check(d['chapter_id'] in chapters,'稱號持有篇不存在')
            for h in d['holdings']:
                check(h['id'] not in title_ids,'稱號持有 ID 重複');title_ids.add(h['id'])
                check(h['person_id'] in pids and bool(h['title']),'稱號持有人或用稱無效')
                check(h['status']=='source_attested','稱號持有狀態無效')
                check(h['kind'] in ('royal_rank','imperial_rank','noble_rank','office','honorific','unclassified'),'稱號種類無效')
                check(h['mode'] in ('grant','self_proclamation','demotion','attestation'),'稱號事件種類無效')
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
                period=h['effective_period']
                for endpoint in ('start','end'):
                    boundary=period[endpoint]
                    check(boundary['status'] in ('unknown','source_event'),'稱號時段端點狀態無效')
                    expected={'status','date_expression','evidence'}
                    if boundary['status']=='source_event':
                        expected.add('event_type')
                        if 'normalized_date' in boundary:expected.add('normalized_date')
                    check(set(boundary)==expected,'稱號端點含未定義欄位，不能暗補正規化日期')
                    if boundary['status']=='unknown':
                        check(boundary['date_expression'] is None and not boundary['evidence'] and 'event_type' not in boundary,'未知稱號端點不得暗補日期或事件')
                    else:
                        check(bool(boundary['evidence']),'稱號時段事件缺少證據')
                        allowed=('grant','self_proclamation','demotion') if endpoint=='start' else ('deposition','renunciation','abolition','explicit_end')
                        check(boundary['event_type'] in allowed,'稱號端點事件類型無效，死亡或首次用稱不得自動替代起訖')
                        for e in boundary['evidence']:title_evidence(e)
                        date=boundary['date_expression']
                        check(date is None or isinstance(date,str) and bool(date) and any(date in e['quote'] for e in boundary['evidence']),'稱號日期表述不在端點證據')
                        if 'normalized_date' in boundary:
                            check(isinstance(date, str) and bool(date), '稱號數字紀年須有原始日期表述')
                            validate_date_evidence(boundary['normalized_date'], boundary['evidence'], date)
                check(period['start']['status']==('unknown' if h['mode']=='attestation' else 'source_event'),'稱號起點與授予／用稱種類不符')
                if h['mode']!='attestation':check(period['start'].get('event_type')==h['mode'],'稱號起點與事件種類不符')
        aids=set()
        for path in (root/'corpus').glob('*/*-assertions.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_assertion_set','人物陳述集類型不符')
            check(d['chapter_id'] in chapters,'人物陳述集篇不存在')
            for a in d['assertions']:
                check(a['id'] not in aids,'人物陳述 ID 重複');aids.add(a['id'])
                check(a['subject_person_id'] in pids and a['object_person_id'] in pids,'人物陳述引用未知人物')
                check(a['subject_person_id']!=a['object_person_id'],'人物陳述關係自環')
                check(a['predicate'] in ('father','mother','spouse','brother','sister','paternal_uncle','agnatic_cousin','grandfather','great_grandfather','ancestor'),'人物陳述關係類型未知')
                check(a['status']=='source_attested' and bool(a['evidence']),'人物陳述未有來源證據')
                qualifiers = a.get('qualifiers', {})
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
        address_ids = set()
        for path in (root / 'corpus').glob('*/*-addresses.json'):
            record = json.loads(path.read_text(encoding='utf-8'))
            check(record['record_type'] == 'person_address_assertion_set' and record['chapter_id'] in chapters, '地址主張集格式或篇不存在')
            for address in record['assertions']:
                check(address['id'] not in address_ids, '地址主張 ID 重複'); address_ids.add(address['id'])
                check(address['person_id'] in pids and address['status'] == 'source_attested', '地址人物或狀態無效')
                check(address['relation'] in ('biographical_origin', 'ancestral_origin', 'native_place', 'birth_place', 'residence', 'death_place', 'migration_origin', 'migration_destination', 'burial_place'), '地址關係類型未知')
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
                        check(any(m.get('person_id') == address['person_id'] for m in hit[1]['mentions']), '地址人物未見於證據段')
                        check(chapters[hit[0]]['source_id'] == evidence['source_id'], '地址來源 ID 不符')
        try:
            from .family_assemblies import load_assemblies
            from .person_bundle import load_catalog
        except ImportError:
            from family_assemblies import load_assemblies
            from person_bundle import load_catalog
        load_assemblies(root, load_catalog(root))
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
