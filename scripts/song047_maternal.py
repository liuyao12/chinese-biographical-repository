"""Explicit mother references without inferring birth or marriage."""
def clause_valid(a, paragraphs):
    try:
        q=a['qualifiers']; e,=a['evidence']; cid,p=paragraphs[e['paragraph_id']]; text=p['text']; ms={m['id']:m for m in p['mentions']}
        s=ms[e['subject_person_mention_id']]; o=ms[e['object_person_mention_id']]; clause=q['maternal_clause']
        if (a['predicate']!='maternal_role' or a['human_reviewed'] is not False or a['status']!='source_attested'
            or set(q)!={'source_term','role','biological_mother','father_person_id','maternal_clause'}
            or q['role']!='mother_unspecified' or q['biological_mother'] is not None or q['father_person_id'] is not None
            or set(clause)!={'kind','start','end'} or e['chapter_id']!=cid or e['quote']!=text
            or s['kind']!='person' or o['kind']!='person' or s['person_id']!=a['subject_person_id']
            or o['person_id']!=a['object_person_id'] or s['person_id']==o['person_id']):return False
        start,end=clause['start'],clause['end']
        if type(start)is not int or type(end)is not int or not 0<=start<end<=len(text) or text[start:end]!=q['source_term']:return False
        if any(text[m['start']:m['end']]!=m['surface'] for m in (s,o)):return False
        if clause['kind']=='named_child_killer_qimu':
            killers=[m for m in p['mentions']if m['kind']=='person' and m['start']==s['end']+2 and m['person_id']not in (s['person_id'],o['person_id'])]
            return (o['surface']=='其母' and start==s['start'] and end==o['end']+2
                    and text[s['end']:s['end']+2]=='出奔' and text[o['end']:end]=='以徇'
                    and any(text[k['end']:o['start']]=='殺' for k in killers))
        if clause['kind']=='named_child_birth_huangbi_died':
            return (o['surface']=='皇妣' and start==s['start'] and end==o['end']+1
                    and text[s['end']:o['start']]=='產而' and text[o['end']:end]=='殂')
        return False
    except (KeyError,TypeError,ValueError):return False
