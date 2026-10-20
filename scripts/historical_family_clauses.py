"""Literal historical 收養, 奉後 and 從弟 clauses retain distinct meanings."""
def _parts(a, paragraphs):
    e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text'];q=a['qualifiers'];b=q['source_clause_binding'];ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']];start,end=b['start'],b['end']
    if (e['chapter_id']!=cid or e['quote']!=t or a.get('status')!='source_attested'or a.get('human_reviewed')is not False
            or s['person_id']!=a['subject_person_id']or o['person_id']!=a['object_person_id']or s['person_id']==o['person_id']
            or type(start)is not int or type(end)is not int or not 0<=start<end<=len(t)or t[start:end]!=q['source_term']):raise ValueError('Unbound clause')
    for m in [s,o]:
        if (m['kind']!='person'or type(m['start'])is not int or type(m['end'])is not int or not 0<=m['start']<m['end']<=len(t)or t[m['start']:m['end']]!=m['surface']):raise ValueError('Bad anchor')
    return t,q,b,ms,s,o,start,end

def explicit_shouyang_valid(a,paragraphs):
    try:
        t,q,b,ms,s,o,start,end=_parts(a,paragraphs)
        if (a['predicate']!='adoptive_father'or set(q)!={'source_term','adoption_basis','adoption_kind','modern_legal_status','parentage_inference','source_clause_binding'}
                or q['adoption_basis']!='explicit_shouyang'or q['adoption_kind']!='historical_shouyang'
                or q['modern_legal_status']!='not_inferred'or q['parentage_inference']!='not_inferred'
                or set(b)!={'kind','start','end'}or o['start']!=start):return False
        if b['kind']=='named_orphan_shouyang':
            return (q['source_term']==o['surface']+'哀'+s['surface']+'少孤収養'
                    and s['start']==o['end']+1 and t[s['end']:end]=='少孤収養'
                    and t[end:].startswith('與諸子同使與'))
        if b['kind']=='named_mother_received_child_shouyang':
            at=o['end']+len('為司空時納');embedded=next((m for m in ms.values()if m['start']==at and m['end']==at+len(s['surface'])),None)
            return (q['source_term']==o['surface']+'為司空時納'+s['surface']+'母并収養'+s['surface']
                    and s['end']==end and t[s['start']-2:s['start']]=='収養'
                    and embedded is not None and embedded['kind']=='person'and embedded['person_id']==s['person_id']
                    and t[embedded['start']:embedded['end']]==embedded['surface']==s['surface']
                    and embedded['id']!=s['id'] and t[end:].startswith('其時'))
        return False
    except(KeyError,TypeError,ValueError,StopIteration):return False

def named_zusun_fenghou_valid(a,paragraphs):
    try:
        t,q,b,ms,s,o,start,end=_parts(a,paragraphs);ante=ms[b['antecedent_mention_id']]
        return (a['predicate']=='ritual_successor_of'
                and set(q)=={'source_term','succession_kind','legal_adoption_status','parentage_inference','source_clause_binding'}
                and q['succession_kind']=='named_zusun_feng_hou'and q['legal_adoption_status']=='not_stated'and q['parentage_inference']=='not_inferred'
                and set(b)=={'kind','start','end','antecedent_mention_id'}and b['kind']=='feng_named_zusun_yifenghou'
                and q['source_term']=='以奉'+o['surface']+'後'and o['start']==start+2 and o['end']==end-1
                and ante['kind']=='person'and ante['person_id']==o['person_id']and ante['surface']==o['surface']
                and t[ante['start']:ante['end']]==ante['surface']and t[:ante['start']].endswith('封')
                and not any(c in t[:ante['start']]for c in '不未非曰云：「『')
                and t[ante['end']:s['start']]=='族孫'and t[s['end']:start]=='為新昌亭侯邑三百戸')
    except(KeyError,TypeError,ValueError,StopIteration):return False

def explicit_congdi_valid(a,paragraphs):
    try:
        t,q,b,ms,s,o,start,end=_parts(a,paragraphs);k=q['kinship_structure']
        return (a['predicate']=='agnatic_cousin'and set(q)=={'source_term','kinship_structure','source_clause_binding'}
                and set(k)=={'lineage','generation_difference','collateral','distance','common_ancestor_person_id','subject_relative_age'}
                and k['lineage']=='paternal'and type(k['generation_difference'])is int and k['generation_difference']==0
                and k['collateral']is True and k['distance']is None and k['common_ancestor_person_id']is None and k['subject_relative_age']=='younger'
                and set(b)=={'kind','start','end'}and b['kind']=='named_object_congdi_subject'
                and q['source_term']==o['surface']+'從弟'+s['surface']and o['start']==start
                and s['start']==o['end']+2 and s['end']==end)
    except(KeyError,TypeError,ValueError,StopIteration):return False
