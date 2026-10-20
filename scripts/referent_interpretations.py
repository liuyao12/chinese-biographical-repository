# coding: utf-8
"""Attributed readings can concern people, groups or literary roles."""
import re
from urllib.parse import urlparse
KINDS = {'historical_person', 'legendary_person', 'unspecified_person',
         'generic_group', 'multiple_allusions', 'divinity', 'natural_phenomenon', 'mythical_creature'}

def strings(value, nonempty=True):
    return (isinstance(value,list) and (bool(value) or not nonempty)
            and all(isinstance(x,str) and x for x in value)
            and len(set(value)) == len(value))

def hex_string(value, size):
    return isinstance(value,str) and bool(re.fullmatch('[0-9a-f]{'+str(size)+'}',value))

def http_reference(url):
    if not isinstance(url,str): return False
    try:
        parts=urlparse(url)
        return parts.scheme in {'http','https'} and bool(parts.netloc)
    except ValueError:
        return False

def interpretation_errors(chapter, person_ids):
    errors = []
    paragraphs = {p['id']: p for p in chapter['paragraphs']}
    cases = chapter.get('annotation', {}).get('referent_interpretations', [])
    if not isinstance(cases,list): return ['指稱異說須為案件陣列']
    case_ids = set()
    for case in cases:
        if not isinstance(case,dict):
            errors.append('指稱異說案件須為物件'); continue
        def check(condition, message):
            if not condition: errors.append(f"{case.get('id', '?')}: {message}")
        cid = case.get('id')
        check(isinstance(cid,str) and bool(cid) and cid not in case_ids, '指稱異說案件 ID 無效或重複')
        if isinstance(cid,str): case_ids.add(cid)
        status=case.get('status')
        check(status in ('unresolved','editorial_provisional'), '指稱判讀狀態無效')
        if status=='unresolved':
            check(case.get('default_alternative_id') is None and not case.get('selection'),
                  '未決異說不得預設選人或默認採納一說')
        check(isinstance(case.get('reviewer'),str) and bool(case['reviewer'])
              and case.get('human_reviewed') is False and bool(case.get('note')),
              '異說須有代理署名、限制及未經人工覆核狀態')
        paragraph_id = case.get('paragraph_id')
        p = paragraphs.get(paragraph_id) if isinstance(paragraph_id,str) else None
        check(p is not None, '異說段落不存在')
        targets = case.get('target_mention_ids')
        valid_targets = strings(targets)
        check(valid_targets, '異說須連到唯一的來源錨點')
        if not valid_targets: targets = []
        anchors = {m['id']: m for m in p['mentions']} if p else {}
        check(bool(targets) and all(mid in anchors and anchors[mid].get('person_id') is None
                  and anchors[mid]['kind'] == 'unresolved' for mid in targets),
              '未決異說不能作已解身份或附到別段人物')
        check(case.get('source_terms') == [anchors[mid]['surface'] for mid in targets if mid in anchors],
              '異說原稱須逐一對應來源錨點')
        ev = case.get('evidence', {})
        if not isinstance(ev,dict): ev = {}
        quote = ev.get('quote')
        offsets = [i for i in range(len(p['text'])) if p['text'].startswith(quote,i)] if p and isinstance(quote,str) and quote else []
        covered = any(all(mid in anchors and i <= anchors[mid]['start']
                      and anchors[mid]['end'] <= i+len(quote) for mid in targets) for i in offsets)
        check(p is not None and ev.get('chapter_id') == chapter['id']
              and ev.get('work_id') == chapter['work_id'] and ev.get('book_id') == chapter['book_id']
              and ev.get('source_id') == chapter['source_id'] and ev.get('paragraph_id') == paragraph_id
              and bool(offsets) and covered and ev.get('mention_ids') == targets,
              '異說須保留本篇正文、來源及受解錨點的確切引句')
        refs = case.get('references', [])
        if not isinstance(refs,list) or not all(isinstance(r,dict) for r in refs):
            check(False,'古注參考須為物件陣列'); refs = []
        ref_ids = [r.get('id') for r in refs]
        valid_refs = strings(ref_ids)
        check(valid_refs, '古注參考 ID 缺失或重複')
        for ref in refs:
            url = ref.get('url'); commit = ref.get('source_commit')
            check(isinstance(url,str) and hex_string(commit,40)
                  and hex_string(ref.get('source_blob'),40)
                  and http_reference(url) and commit in url
                  and isinstance(ref.get('quote'),str) and bool(ref['quote'])
                  and ref.get('image_verified') is False
                  and hex_string(ref.get('cached_response_sha256'),64),
                  '古注須有固定提交、blob、實讀引句及未核書影狀態')
            extent = ref.get('read_line_range')
            check(isinstance(extent,list) and len(extent)==2 and all(type(x)is int for x in extent)
                  and 1 <= extent[0] <= extent[1], '古注須記已讀行範圍')
        alternatives = case.get('alternatives', [])
        if not isinstance(alternatives,list) or not all(isinstance(a,dict) for a in alternatives):
            check(False,'異說須為解釋物件陣列'); alternatives = []
        check(len(alternatives)>=(2 if status=='unresolved' else 1) and strings([a.get('id')for a in alternatives]), '未決異說至少兩項；判讀項目 ID 不得重複')
        for alt in alternatives:
            kind, candidates = alt.get('referent_kind'), alt.get('candidate_person_ids')
            check(isinstance(kind,str) and kind in KINDS and bool(alt.get('attribution'))
                  and bool(alt.get('interpretation')), '解釋須有署名、指稱種類及內容')
            check(strings(candidates,False) and all(pid in person_ids for pid in candidates), '異說人物候選未登記')
            check(not candidates or (isinstance(kind,str) and kind in {'historical_person','legendary_person','multiple_allusions'}),
                  '泛稱或未定角色不得自動連個人')
            source_ids = alt.get('source_reference_ids')
            check(strings(source_ids) and valid_refs and all(rid in ref_ids for rid in source_ids),
                  '各說須連到其古注參考')
        if status=='editorial_provisional':
            default=case.get('default_alternative_id')
            chosen=next((a for a in alternatives if a.get('id')==default),None)if isinstance(default,str)else None
            check(chosen is not None and chosen.get('referent_kind') in ('divinity','natural_phenomenon','generic_group','mythical_creature')
                  and chosen.get('candidate_person_ids')==[], '採用判讀只分類非個人指稱；個人身份須另有身份判斷與正文標記')
            selection=case.get('selection');selection=selection if isinstance(selection,dict)else{}
            selected_refs=selection.get('source_reference_ids')
            check(isinstance(selection.get('rationale'),str) and bool(selection['rationale'])
                  and strings(selected_refs) and chosen is not None and strings(chosen.get('source_reference_ids'))
                  and set(selected_refs).issubset(chosen['source_reference_ids']), '採用判讀須有理由與該讀法的來源依據')
        if 'witness_wording' in case:
            wording=case['witness_wording'];wording=wording if isinstance(wording,dict)else{}
            received,parallel=wording.get('received_phrase'),wording.get('parallel_phrase')
            ref=next((r for r in refs if r.get('id')==wording.get('reference_id')),None)
            check(isinstance(received,str) and bool(received) and isinstance(quote,str) and received in quote
                  and isinstance(parallel,str) and bool(parallel) and ref is not None and isinstance(ref.get('quote'),str) and parallel in ref['quote']
                  and wording.get('adopted_as_text_correction')is False, '平行見證用字須各有原句，不得冒作已採校字')

    return errors
