"""Explicit 'X者Y小字也' only; never infer a personal alias from generic source forms."""
def validate_childhood_name(name,paragraph=None):
    value=name.get('xiaozhi');basis=name.get('xiaozhi_basis')
    if isinstance(basis,dict)and basis.get('kind')=='explicit_subject_xiaozhi':
        return validate_subject_xiaozhi(name,paragraph)
    if value is None and basis is None:return
    def fail():raise ValueError('小字須有原文小字也、同人雙錨點及精確字位，不得冒作字或從泛稱推定')
    if not isinstance(value,str)or not value or value!=value.strip()or not isinstance(paragraph,dict)or name.get('quote')!=paragraph.get('text'):fail()
    required={'kind','source_term','value_anchor','subject_anchor','marker_anchor','status','human_reviewed','rationale'}
    if not isinstance(basis,dict)or set(basis)!=required or basis.get('kind')!='explicit_xiaozhi_statement'or basis.get('status')!='source_attested'or basis.get('human_reviewed')is not False or not basis.get('rationale'):fail()
    text=paragraph['text'];pid=name.get('person_id');anchors=[basis.get(k)for k in ('value_anchor','subject_anchor','marker_anchor')]
    for i,a in enumerate(anchors):
        keys={'paragraph_id','start','end','surface'}|({'person_mention_id'}if i<2 else set())
        if not isinstance(a,dict)or set(a)!=keys or a.get('paragraph_id')!=name.get('paragraph_id')or a.get('paragraph_id')!=paragraph.get('id')or type(a.get('start'))is not int or type(a.get('end'))is not int or not(0<=a['start']<a['end']<=len(text))or text[a['start']:a['end']]!=a.get('surface'):fail()
        if i<2:
            m=next((m for m in paragraph.get('mentions',[])if m.get('id')==a.get('person_mention_id')),None)
            if not m or m.get('person_id')!=pid or any(m.get(k)!=a[k]for k in ('start','end','surface')):fail()
    val,subject,marker=anchors
    term=value+'者'+subject['surface']+'小字也'
    if (val['surface']!=value or marker['surface']!='小字'or val['end']+1!=subject['start']or text[val['end']:subject['start']]!='者'or subject['end']!=marker['start']or basis['source_term']!=term or text[val['start']:marker['end']+1]!=term):fail()


def validate_subject_xiaozhi(name,paragraph):
    """Source X又小字Y, with two same-person anchors; not a nearby song alias."""
    def fail():raise ValueError('小字須完整同人主語又小字原句、雙錨點及原詞位置')
    b=name.get('xiaozhi_basis');v=name.get('xiaozhi')
    if not isinstance(b,dict)or set(b)!={'kind','source_term','value_anchor','subject_anchor','marker_anchor','status','human_reviewed','rationale'}or b['kind']!='explicit_subject_xiaozhi'or b['status']!='source_attested'or b['human_reviewed']is not False or not b['rationale']or not isinstance(paragraph,dict)or name.get('quote')!=paragraph.get('text')or not isinstance(v,str)or not v:fail()
    t=paragraph['text'];anchors=[b[k]for k in('subject_anchor','value_anchor','marker_anchor')]
    for i,a in enumerate(anchors):
        keys={'paragraph_id','start','end','surface'}|({'person_mention_id'}if i<2 else set())
        if not isinstance(a,dict)or set(a)!=keys or a['paragraph_id']!=paragraph['id']or a['paragraph_id']!=name.get('paragraph_id')or type(a['start'])is not int or type(a['end'])is not int or not 0<=a['start']<a['end']<=len(t)or t[a['start']:a['end']]!=a['surface']:fail()
        if i<2:
            m=next((m for m in paragraph.get('mentions',[])if m['id']==a['person_mention_id']),None)
            if not m or m.get('kind')!='person'or m.get('person_id')!=name.get('person_id')or any(m.get(k)!=a[k]for k in('start','end','surface')):fail()
    s,a,k=anchors
    term=s['surface']+'又小字'+v
    if a['surface']!=v or k['surface']!='小字'or t[s['end']:k['start']]!='又'or k['end']!=a['start']or t[s['start']:a['end']]!=term or b['source_term']!=term or t[a['end']:a['end']+1]not in('', '，','。','；'):fail()
