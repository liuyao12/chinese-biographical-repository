"""Two different collateral generations in Wang Zhan's received introduction."""

def valid(claim, paragraphs):
    try:
        q=claim['qualifiers']; evidence,=claim['evidence']; cid,p=paragraphs[evidence['paragraph_id']]; t=p['text']; marks={m['id']:m for m in p['mentions'] if m['kind']=='person'}; junior=marks[evidence['subject_person_mention_id']]; senior=marks[evidence['object_person_mention_id']]; anchor=evidence['relationship_anchor']
        if (cid!='c-nanshi-021-wangzhan' or p['source_position']['revision_id']!=1752646 or p['text_layer']!='received_chapter' or evidence['quote']!=t or cid!=evidence['chapter_id'] or claim['predicate']!='agnatic_senior_kin' or junior['person_id']!=claim['subject_person_id'] or senior['person_id']!=claim['object_person_id'] or t[senior['start']:senior['end']]!=senior['surface'] or not t.startswith('瞻字思範，弘從孫也。祖柳字休季，') or not any(m['start']==0 and m['end']==1 and m['surface']=='瞻' and m['person_id']==junior['person_id'] for m in marks.values()) or not any(m['start']==2 and m['end']==4 and m['surface']=='思範' and m['person_id']==junior['person_id'] for m in marks.values())):return False
        if q['source_term']=='弘從孫也':distance=-2;ok=senior['surface']=='弘' and senior['start']==5 and senior['end']==6
        elif q['source_term']=='從父僧達':distance=-1;ok=senior['surface']=='僧達' and t[senior['start']-2:].startswith('從父僧達聞而異之，謂其父猷曰：「大宗不衰，寄之此子。」')
        else:return False
        return (ok and q['kinship_structure']==dict(lineage='paternal',generation_difference=distance,collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age='unknown') and anchor['paragraph_id']==p['id'] and t[anchor['start']:anchor['end']]==anchor['surface']==q['source_term'] and t.count(anchor['surface'])==1)
    except (ValueError,TypeError,KeyError,IndexError):return False
