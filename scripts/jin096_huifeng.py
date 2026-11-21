"""Bind the divorce petition and the elder daughter to their own source clauses."""
def elder_valid(a, evidence, chapter):
    if (chapter['id']!='c-jinshu-053-jin096-huifeng' or a.get('predicate')!='father'
            or a['qualifiers'].get('source_term')!='衍長女'):
        return False
    p=next((p for p in chapter['paragraphs'] if p['id']==evidence.get('paragraph_id')),None)
    if (not p or evidence.get('quote')!=p['text'] or evidence.get('source_id')!=chapter['source_id']
            or p['text']!='而為太子聘王衍小女惠風。太子聞衍長女美，而賈后為謐聘之，心不能平，頗以為言。'):
        return False
    elder=next((x for x in chapter['annotation']['person_reference_occurrences']
                if x['id']==evidence.get('subject_person_reference_id') and x['paragraph_id']==p['id']),{})
    father=next((m for m in p['mentions'] if m['id']==evidence.get('object_person_mention_id')), {})
    return (elder.get('person_id')==a['subject_person_id'] and father.get('person_id')==a['object_person_id']
            and elder.get('surface')=='長女' and father.get('surface')=='衍'
            and elder['start']==father['end'] and p['text'][father['start']:elder['end']]=='衍長女'
            and any(m['surface']=='王衍' and m['person_id']==father['person_id'] for m in p['mentions']))

def petition_valid(a, paragraphs):
    if a.get('predicate')!='spouse' or len(a.get('evidence',[]))!=1:
        return False
    ev=a['evidence'][0];hit=paragraphs.get(ev.get('paragraph_id'))
    if not hit or hit[0]!=ev.get('chapter_id') or hit[0] not in ('c-jinshu-096-wanghuifeng','c-jinshu-096-wanghuifeng-wyd'):
        return False
    p=hit[1];q=a['qualifiers'].get('dissolution_petition',{});names={m['id']:m for m in p['mentions'] if m['kind']=='person'}
    try:
        petition=q['source'];returned=q['return_source'];father=names[q['petitioner_mention_id']]
        wife=names[ev['subject_person_mention_id']];husband=names[ev['object_person_mention_id']]
        return (q['formal_decision_date'] is None and q['formal_decision_reported'] is False and ev['quote']==p['text']
                and wife['person_id']==a['subject_person_id'] and wife['surface']=='王氏'
                and husband['person_id']==a['object_person_id'] and husband['surface'] in ('湣懷太子','愍懷太子')
                and father['person_id']==q['petitioner_person_id']=='b0c_13f_c3a' and father['surface']=='衍'
                and father['start']==petition['start'] and petition['paragraph_id']==returned['paragraph_id']==p['id']
                and p['text'][petition['start']:petition['end']]==petition['surface'] in ('衍請絕婚','衍請絶婚')
                and p['text'][returned['start']:returned['end']]==returned['surface']=='惠風號哭而歸'
                and p['text'][petition['end']:returned['start']] in ('','，')
                and any(m['start']==returned['start'] and m['person_id']==wife['person_id'] for m in names.values()))
    except (KeyError,TypeError):
        return False
