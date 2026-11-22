"""Bind 溫 and 石虔 to the two independently attested 弟子 clauses."""


def valid(assertion, paragraphs):
    clauses={
        'c-jinshu-098-huanwen:p023':('溫遣桓伊及弟子石虔', '溫', '石虔'),
        'c-zizhitongjian-102-jin098-huanwen-fangtou:south':('石虔，溫之弟子也', '溫', '石虔'),
    }
    evs=assertion.get('evidence',[])
    if assertion.get('predicate')!='paternal_uncle' or len(evs)!=1:
        return False
    ev=evs[0]
    pid=ev.get('paragraph_id')
    hit=paragraphs.get(pid)
    if pid not in clauses or not hit or ev.get('chapter_id')!=hit[0]:
        return False
    term,uncle,nephew=clauses[pid]
    p=hit[1]
    if p['text'].count(term)!=1 or term not in ev.get('quote','') or assertion['qualifiers'].get('source_term')!=term:
        return False
    start=p['text'].index(term)
    names={m['id']:m for m in p['mentions'] if m.get('kind')=='person'}
    for role,surface in (('subject',nephew),('object',uncle)):
        m=names.get(ev.get(role+'_person_mention_id'),{})
        offset=start+term.index(surface)
        if (m.get('start'),m.get('end'),m.get('surface'),m.get('person_id'))!=(offset,offset+len(surface),surface,assertion.get(role+'_person_id')):
            return False
    return assertion['subject_person_id']!=assertion['object_person_id']
