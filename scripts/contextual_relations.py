"""Source-bound teaching and unspecified kinship; no lineage reconstruction."""
def _parts(a, paragraphs):
    e, = a['evidence']; cid,p=paragraphs[e['paragraph_id']]
    if e['chapter_id']!=cid or e['quote']!=p['text'] or a.get('status')!='source_attested' or a.get('human_reviewed')is not False:
        raise ValueError('Unbound source')
    ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
    for m,k in [(s,'subject_person_id'),(o,'object_person_id')]:
        if (m['kind']!='person'or m['person_id']!=a[k]or type(m['start'])is not int or type(m['end'])is not int
                or not 0<=m['start']<m['end']<=len(p['text'])or p['text'][m['start']:m['end']]!=m['surface']):
            raise ValueError('Wrong endpoint')
    if s['person_id']==o['person_id']:raise ValueError('Self relation')
    return e,p,ms,s,o

def teaching_clause_valid(a,paragraphs):
    try:
        e,p,ms,learner,instructor=_parts(a,paragraphs);t=p['text'];q=a['qualifiers'];b=q['teaching_clause_binding'];tr=ms[b['transition_mention_id']];start,end=b['start'],b['end']
        return (a['predicate']=='teacher'and set(q)=={'source_term','relationship_basis','teaching_clause_binding'}
                and q['relationship_basis']=='teaching'
                and set(b)=={'kind','start','end','transition_mention_id'}
                and b['kind']=='biographical_subject_teaches_after_accession_office'
                and type(start)is int and type(end)is int and 0<=start<end<=len(t)
                and instructor['start']==0 and t[instructor['end']:].startswith('字')
                and tr['kind']=='person'and tr['person_id']==learner['person_id']
                and t[tr['start']:tr['end']]==tr['surface']and tr['surface']==learner['surface']
                and instructor['end']<tr['start']<tr['end']<=start
                and not any(c in t[instructor['end']:start]for c in '曰云：「『')
                and t[tr['end']:start]=='初拜博士祭酒賜爵武城子'
                and q['source_term']==t[start:end]=='常授'+learner['surface']+'經書'
                and learner['start']==start+2 and learner['end']==end-2)
    except(KeyError,TypeError,ValueError,StopIteration):return False

def weiqin_pair_valid(a,paragraphs):
    try:
        e,p,ms,s,o=_parts(a,paragraphs);t=p['text'];q=a['qualifiers'];b=q['kinship_clause_binding'];start,end=b['start'],b['end']
        return (a['predicate']=='kinship_unspecified'
                and set(q)=={'source_term','kinship_basis','generation_difference','exact_distance','lineage','common_ancestor_person_id','connecting_person_ids','kinship_clause_binding'}
                and q['kinship_basis']=='explicit_weiqin_pair'
                and all(q[k]is None for k in ['generation_difference','exact_distance','lineage','common_ancestor_person_id','connecting_person_ids'])
                and set(b)=={'kind','start','end'}and b['kind']=='biezu_weiqin_pair'
                and type(start)is int and type(end)is int and 5<=start<end<=len(t)
                and t[start-5:start]=='三人别祖而'
                and q['source_term']==t[start:end]==s['surface']+o['surface']+'為親'
                and s['start']==start and s['end']==o['start']and o['end']==end-2)
    except(KeyError,TypeError,ValueError,StopIteration):return False
