"""Read the named cousin's son and the direction of 舅甥 in the transmitted account."""

def verify(assertion, paragraphs, assertions=()):
    try:
        e, = assertion['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        q = assertion['qualifiers']
        term = q['source_term']
        t = p['text']
        marks = {m['id']: m for m in p['mentions'] if m['kind'] == 'person'}
        a, b = (marks[e[k+'_person_mention_id']] for k in ('subject', 'object'))
        if (e['chapter_id'] != cid or e['quote'] != t or t.count(term) != 1
                or (a['person_id'], b['person_id']) != (assertion['subject_person_id'], assertion['object_person_id'])
                or a['person_id'] == b['person_id']):
            return False
        start=t.index(term)
        if assertion['predicate']=='maternal_uncle':
            return (term == '王獻之兄弟，自超未亡，見愔，常躡履問訊，甚修舅甥之禮'
                    and a['start']==start and a['surface']=='王獻之'
                    and b['start']==start+term.index('見愔')+1 and b['surface']=='愔'
                    and q['lineage']=='maternal' and q['generation_difference']==-1)
        father=marks[q['birth_father_mention_id']]
        lead=b['surface']+'無子，從弟'+father['surface']+'以子'
        birth=next(row for row in assertions if row['id']==q['birth_father_assertion_id'])
        return (assertion['predicate']=='ritual_successor_of' and q['succession_kind']=='cousin_gives_named_son_to_succeed'
                and q['parentage_inference']=='not_inferred' and q['legal_adoption_status']=='not_stated'
                and term==lead+a['surface']+'嗣' and b['start']==start
                and father['start']==b['end']+len('無子，從弟') and a['start']==start+len(lead)
                and len({a['person_id'],b['person_id'],father['person_id']})==3 and birth['predicate']=='father'
                and (birth['subject_person_id'],birth['object_person_id'])==(a['person_id'],father['person_id'])
                and any(f['paragraph_id']==p['id'] and f['quote']==t
                        and f['subject_person_mention_id']==a['id'] and f['object_person_mention_id']==father['id']
                        for f in birth['evidence']))
    except (KeyError,TypeError,ValueError,StopIteration,IndexError):
        return False
