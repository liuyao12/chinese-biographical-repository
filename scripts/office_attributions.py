# coding: utf-8
"""Keep an office attribution from punctuation separate from the received text."""
import re

def punctuation_attribution_errors(holding, paragraphs, mentions):
    basis=holding.get('punctuation_attribution')
    if not isinstance(basis,dict):return ['官職句讀判讀須有結構化依據']
    term=basis.get('source_term');selected=mentions.get(basis.get('person_mention_id'));other=mentions.get(basis.get('alternative_person_mention_id'))
    valid=(basis.get('kind')=='punctuation_resegmentation' and basis.get('status')=='editorial_provisional'
           and basis.get('human_reviewed') is False and isinstance(basis.get('rationale'),str) and bool(basis['rationale'].strip())
           and holding.get('appointment_role')=='acting' and holding.get('kind')=='office' and holding.get('mode')=='attestation'
           and isinstance(holding.get('title'),str) and term=='行'+holding['title']+'事'
           and selected and other and selected[0]==other[0] and selected[1]==other[1]
           and selected[2].get('kind')=='person' and selected[2].get('person_id')==holding.get('person_id')
           and other[2].get('kind')=='person' and other[2].get('person_id')!=holding.get('person_id'))
    if not valid:return ['代理官職句讀須分存同段首選與另一讀法的人物錨點，不得跨人或暗作正式授職']
    paragraph=paragraphs.get(selected[1]);segment=basis.get('received_segment');preferred=basis.get('preferred_segmentation')
    if not paragraph or not isinstance(segment,str) or not isinstance(preferred,str):return ['句讀缺少收到片段及首選分讀']
    text=paragraph[1]['text'];starts=[i for i in range(len(text))if text.startswith(segment,i)]
    if not (term in segment and any(i<=other[2]['start']<other[2]['end']<=i+len(segment) for i in starts)
            and selected[2]['surface']+term in preferred
            and any(a.get('person_mention_id')==selected[2]['id'] and a.get('surface')==holding['title'] for a in holding.get('attestations',[]))):
        return ['句讀原片段、另一讀法錨點及代理官職原稱不符']
    fixed=False
    for ref in basis.get('references',[]):
        if not isinstance(ref,dict):continue
        raw=ref.get('quote');commit=ref.get('source_commit');url=ref.get('url');blob=ref.get('source_blob')
        if not all(isinstance(x,str) for x in [raw,commit,url,blob]):continue
        plain=re.sub(r'\s|¶|/','',re.sub(r'<pb:[^>]*>','',raw))
        if 'display_quote' in ref and ref['display_quote']!=plain:
            return ['官職引文顯示只能移除數位分行與頁標，不得另改原字']
        if (re.fullmatch('[0-9a-f]{40}',commit) and re.fullmatch('[0-9a-f]{40}',blob)
                and url.startswith('https://') and commit in url and ref.get('image_verified') is False
                and selected[2]['surface']+term in plain and '與宗正廷尉雜' in plain):fixed=True
    return [] if fixed else ['代理者首選須有固定平行原文直接支持，不得只依編者改標點']
