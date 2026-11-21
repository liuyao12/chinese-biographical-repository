"""The biographical subject married the princess in the same fixed paragraph."""
from hashlib import sha256
def valid(a,e,c,root):
    try:
        p,=c['paragraphs'];s=c['source'];raw=(root/s['raw_path']).read_bytes();t=p['text'];src=raw.decode()
        b=a['qualifiers']['reading_basis'];m=next(m for m in p['mentions']if m['id']==b['subject_anchor_id'])
        o=next(m for m in c['annotation']['person_reference_occurrences']if m['id']==b['object_anchor_id'])
        clause='弱冠選尚淮南長公主，拜駙馬都尉'
        return (c['id']=='c-nanshi-022-wangjian-sihui' and s['revision_id']==1477957
                and sha256(raw).hexdigest()==s['raw_file_sha256'] and t==''.join(src[i]for i in p['source_position']['raw_character_offsets'])
                and e['paragraph_id']==p['id'] and e['quote']==t and t.count(clause)==1 and t.startswith('暕字思晦')
                and a['predicate']=='spouse' and a['qualifiers']['source_term']=='選尚淮南長公主'
                and m['start']==0 and m['surface']=='暕' and m['person_id']==a['subject_person_id']
                and o['paragraph_id']==p['id'] and o['surface']=='淮南長公主' and o['person_id']==a['object_person_id']
                and o['start']==t.index(clause)+4 and t[o['start']:o['end']]==o['surface'])
    except (KeyError,ValueError,IndexError,TypeError,StopIteration):return False
