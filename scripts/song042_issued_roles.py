"""Verify released source MIDs that moved from aliases to their referential layer."""
ALLOWED={
    ('c-songshu-042-wanghong:line059',0,'少帝'):'0ab_f5d_337',
    ('c-songshu-042-wanghong:line059',20,'太祖'):'3bh_k4m_fg4',
    ('c-songshu-042-wanghong:line087',305,'王太保'):'7r6_k52_qji_ABAAAAA',
}


def verified_roles(ch,p):
    if ch.get('id')!='c-songshu-042-wanghong' or ch.get('source',{}).get('revision_id')!=1478172:
        return []
    found=[]
    for ref in ch.get('annotation',{}).get('person_reference_occurrences',[]):
        key=(p['id'],ref['start'],ref['surface']);pid=ALLOWED.get(key)
        if (pid and ref['paragraph_id']==p['id'] and ref['id']==p['id']+f":m{ref['start']:04d}" and ref['person_id']==pid
                and ref['end']==ref['start']+len(ref['surface']) and p['text'][ref['start']:ref['end']]==ref['surface']
                and ref['quote']==p['text'] and ref['referent_role']=='third_person'):
            found.append(dict(ref,kind='person',original_layer='person_reference'))
    return found


def known(ch,p,mid):
    rows=[m for m in p['mentions']+verified_roles(ch,p) if m['id']==mid]
    if len(rows)!=1:raise ValueError('來源MID必須且只可於姓名或核定指涉層出現一次')
    return rows[0]


def alias_or_reference(person, marker):
    if marker.get('original_layer')!='person_reference':
        return any(a['surface']==marker['surface'] and marker['id'] in a.get('mention_ids',[])for a in person['aliases'])
    return (not any(marker['id'] in a.get('mention_ids',[]) for a in person['aliases'])
            and any(e.get('kind')=='person_reference' and e.get('mention_id')==marker['id'] and e.get('paragraph_id')==marker['paragraph_id'] and e.get('quote')==marker['surface'] for e in person['evidence']))
