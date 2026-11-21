"""核王祥父母之死與固定傳文中的親稱，不將親稱當作二人的姓名。"""
from pathlib import Path
import json
def valid(event,evidence,chapter,root):
    try:
        key=evidence['person_reference_id']
        ref=next(r for r in chapter['annotation']['person_reference_occurrences'] if r['id']==key)
        p=next(p for p in chapter['paragraphs'] if p['id']==ref['paragraph_id']==evidence['paragraph_id'])
        rule={'father':('祥喪父之後','父'),'stepmother':('母終','母')}
        kin=json.loads((Path(root)/'corpus/jinshu/033-assertions.json').read_text())['assertions']
        a=next(a for a in kin if a['id']==evidence['relative_assertion_id'])
        term,surface=rule[a['predicate']]
        subject=next(m for m in p['mentions'] if m['id']==evidence['relative_subject_mention_id'])
        i=p['text'].index(term)
        return (chapter['id']=='c-jinshu-033-wanglan-family' and event['event_type']=='death'
                and p['text'].count(term)==1 and term==event['source_term'] and term in evidence['quote']
                and p['text']==evidence['quote'] and ref['surface']==surface and ref['start']==i+term.index(surface)
                and ref['end']==ref['start']+len(surface) and ref['referent_role']=='third_person'
                and subject['surface']=='祥' and subject['person_id']==a['subject_person_id']
                and a['object_person_id']==ref['person_id']==event['person_id'])
    except (KeyError,TypeError,ValueError,StopIteration,OSError):return False
