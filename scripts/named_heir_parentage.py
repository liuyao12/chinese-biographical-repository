"""窄式：傳主無子，以具名弟之具名子為嗣；不泛化嗣爵或奉祀。"""
def named_brother_son_heir_valid(a, paragraphs, assertions):
    q=a.get('qualifiers',{});es=a.get('evidence',[])
    if (a.get('predicate')!='adoptive_father' or a.get('status')!='source_attested'
        or q.get('adoption_basis')!='named_younger_brother_son_as_heir'
        or q.get('modern_legal_status')!='not_inferred' or len(es)!=1):return False
    e=es[0];hit=paragraphs.get(e.get('paragraph_id'))
    if not hit or hit[0]!=e.get('chapter_id'):return False
    p=hit[1]
    if p.get('text_layer')!='received_chapter':return False
    text=p.get('text','');ms={m['id']:m for m in p.get('mentions',[])}
    if e.get('quote')!=text:return False
    child=ms.get(e.get('subject_person_mention_id'),{});heirfather=ms.get(e.get('object_person_mention_id'),{})
    if (child.get('kind')!='person' or heirfather.get('kind')!='person'
        or child.get('person_id')!=a.get('subject_person_id') or heirfather.get('person_id')!=a.get('object_person_id')
        or child.get('person_id')==heirfather.get('person_id') or heirfather.get('start')!=0):return False
    # 傳主身分必須來自段首名字，不從最近出現的人名猜省略主語。
    if not text.startswith(heirfather['surface']) or not text[heirfather['end']:].startswith(('字','無子')):return False
    bio=next((r for r in assertions if r.get('id')==q.get('biological_father_assertion_id')),None)
    if not bio or bio.get('predicate')!='father' or bio.get('status')!='source_attested' or bio.get('subject_person_id')!=child['person_id'] or len(bio.get('evidence',[]))!=1:return False
    be=bio['evidence'][0];father=ms.get(be.get('object_person_mention_id'),{})
    if (father.get('kind')!='person' or father.get('person_id')!=bio.get('object_person_id')
        or father.get('person_id') in (child['person_id'],heirfather['person_id'])
        or be.get('subject_person_mention_id')!=child['id'] or be.get('paragraph_id')!=p['id']
        or be.get('chapter_id')!=e.get('chapter_id') or be.get('source_id')!=e.get('source_id')
        or be.get('quote')!=text or bio.get('qualifiers',{}).get('lineage')!='paternal'):return False
    term=q.get('source_term')
    if not isinstance(term,str) or not term:return False
    for i in range(len(text)):
        if not text.startswith(term,i):continue
        if (text[:i].endswith('無子，') and heirfather['end']<=i
            and text[i:father['start']]=='以弟'
            and text[father['end']:child['start']]=='子'
            and text[child['end']:i+len(term)] in ('爲嗣','為嗣')
            and i<father['start']<father['end']<child['start']<child['end']<=i+len(term)
            and not any(m.get('kind')=='person' and m['id'] not in (father['id'],child['id']) and i<=m['start']<i+len(term) for m in ms.values())):return True
    return False
