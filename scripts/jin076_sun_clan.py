"""Bind Sun's 族孫女 to Sun Quan in the received biography."""
def valid(a,paragraphs):
    try:
        e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];q=a['qualifiers']
        if (p['id']!='c-jinshu-096-jin076-yutan:house' or cid!=e['chapter_id'] or e['quote']!=p['text']
            or a['predicate']!='kinship_unspecified' or q!={'source_term':'孫權族孫女也','kinship_basis':'jin096_shi_yu_sunquan','father_person_id':None,'connecting_person_ids':None}
            or not p['text'].startswith('虞潭母孫氏，吳郡富春人，孫權族孫女也。')):
            return False
        ms={m['id']:m for m in p['mentions']if m['kind']=='person'}
        for role,form in [('subject','孫氏'),('object','孫權')]:
            m=ms[e[role+'_person_mention_id']];start=p['text'].index(form)
            if (m['person_id'],m['surface'],m['start'],m['end'])!=(a[role+'_person_id'],form,start,start+len(form)):return False
        return a['subject_person_id']!=a['object_person_id']
    except (KeyError,ValueError,TypeError):
        return False
