#!/usr/bin/env python3
"""檢查穩定 ID、字元錨點、人物證據、身份判斷及 XML／JSON 一致性。"""
from pathlib import Path
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]

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
        check(all(__import__('re').fullmatch(r'cbr-p[0-9]{6}', pid) for pid in pids), '人物 ID 格式不符')
        check(registry['next_number'] > max(int(pid[5:]) for pid in pids), '人物 ID 分配游標會重用 ID')
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
                xm=list(x)
                check(len(xm)==len(p['mentions']), 'XML 提及數不符')
                check(all(e.tag in ('persName','rs') for e in x),'XML 含未知正文標籤')
                for e,m in zip(xm,p['mentions']):
                    check(e.get('id')==m['id'] and e.text==m['surface'], 'XML 提及錨點不符')
                    check(e.tag==('persName' if m['kind']=='person' else 'rs'), 'XML 提及類型不符')
                    check(e.get('ref')==m['person_id'], 'XML 人物引用不符')
                    if m['kind']=='unresolved': check(e.get('type')=='unresolved','XML 未定類型不符')
        check(set(chapter_books)==set(chapters), '著作目錄與文本篇清單不符')
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
        aids=set()
        for path in (root/'corpus').glob('*/*-assertions.json'):
            d=json.loads(path.read_text(encoding='utf-8'))
            check(d['record_type']=='person_assertion_set','人物陳述集類型不符')
            check(d['chapter_id'] in chapters,'人物陳述集篇不存在')
            for a in d['assertions']:
                check(a['id'] not in aids,'人物陳述 ID 重複');aids.add(a['id'])
                check(a['subject_person_id'] in pids and a['object_person_id'] in pids,'人物陳述引用未知人物')
                check(a['subject_person_id']!=a['object_person_id'],'人物陳述關係自環')
                check(a['predicate'] in ('father','mother','spouse','brother','sister','grandfather','great_grandfather','ancestor'),'人物陳述關係類型未知')
                check(a['status']=='source_attested' and bool(a['evidence']),'人物陳述未有來源證據')
                for e in a['evidence']:
                    hit=paragraphs.get(e['paragraph_id'])
                    check(bool(hit) and hit[0]==d['chapter_id']==e['chapter_id'] and e['quote'] in hit[1]['text'],'人物陳述引句與所屬篇不符')
                    check(chapters.get(e['chapter_id'],{}).get('source_id')==e['source_id'],'人物陳述來源 ID 不符')
                    if hit:
                        local={m['person_id'] for m in hit[1]['mentions'] if m['kind']=='person'}
                        check(a['subject_person_id'] in local and a['object_person_id'] in local,'人物陳述端點未見於证據段落'.replace('证','證'))
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
