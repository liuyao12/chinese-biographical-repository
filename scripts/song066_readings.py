"""Bind named/anonymous family and the son’s unassumed appointment to fixed biography clauses."""
import hashlib
from pathlib import Path

def kin_valid(assertion,evidence,chapter,root):
    try:
        if chapter['book_id']!='b-songshu-066' or chapter['source']['revision_id']!=2069104:return False
        src=chapter['source'];raw=(Path(root)/src['raw_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=src['raw_file_sha256']:return False
        raw=raw.decode();b=assertion['qualifiers']['reading_basis']
        p=next(p for p in chapter['paragraphs']if p['id']==evidence['paragraph_id'])
        if p['text']!=''.join(raw[i] for i in p['source_position']['raw_character_offsets']):return False
        ref=next(r for r in chapter['annotation']['person_reference_occurrences']if r['id']==b['subject_anchor_id'])
        m=next(m for m in p['mentions']if m['id']==b['object_anchor_id']);f=b['source_quote']
        cases={('敬弘妻，桓玄姊也。','spouse'):('妻','敬弘',2,0),
               ('敬弘妻，桓玄姊也。','sister'):('妻','桓玄',2,4),
               ('女適尚書僕射何尚之弟述之，敬弘嘗往何氏看女','father'):('女','敬弘',0,13),
               ('女適尚書僕射何尚之弟述之，敬弘嘗往何氏看女','spouse'):('女','述之',0,10)}
        rs,ms,ri,mi=cases[(f,assertion['predicate'])];start=p['text'].index(f)
        return (p['text'].count(f)==1 and p['text'][b['start']:b['end']]==f and b['start']==start and
                evidence['quote']==p['text'] and (ref['surface'],m['surface'])==(rs,ms) and
                ref['paragraph_id']==p['id'] and ref['referent_role']=='third_person' and
                (ref['start'],m['start'])==(start+ri,start+mi) and ref['person_id']==assertion['subject_person_id'] and
                m['person_id']==assertion['object_person_id'] and m['kind']=='person')
    except (KeyError,StopIteration,ValueError,OSError,TypeError,IndexError):
        return False

def proposed_valid(a,c):
    try:
        if c['id']!='c-songshu-066-wangjinghong' or c['source']['revision_id']!=2069104:return False
        e,=a['evidence'];p=next(p for p in c['paragraphs']if p['id']==e['paragraph_id']);text=p['text']
        fixed='子恢之被召為祕書郎，敬弘為求奉朝請，與恢之書曰：「祕書有限，故有競。朝請無限，故無競。吾欲使汝處於不競之地。」太祖嘉而許之。'
        pos=text.index(fixed)
        person=next(m for m in p['mentions']if m['id']==a['person_mention_id'])
        if text.count(fixed)!=1 or a['source_frame']!=fixed or person['start']!=pos+1 or person['surface']!='恢之' or person['person_id']!=a['person_id'] or e['person_mention_id']!=person['id'] or e['quote']!=text:return False
        for k,t in [('appointment_anchor','被召為'),('role_anchor','祕書郎'),('non_assumption_anchor','太祖嘉而許之')]:
            anchor=a[k];begin=pos+fixed.index(t)
            if (anchor['paragraph_id'],anchor['start'],anchor['end'],anchor['surface'])!=(p['id'],begin,begin+len(t),t):return False
        return (a['title']=='祕書郎' and a['outcome']=='not_assumed' and a['non_assumption_kind']=='superseded_by_accepted_alternative' and a['proposal_kind']=='unassumed_appointment')
    except (KeyError,StopIteration,ValueError,TypeError,IndexError):
        return False
