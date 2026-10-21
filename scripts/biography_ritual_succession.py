"""A named biography head accepts its younger brother's named eldest son as ritual heir."""
def valid(a,paragraphs,assertions):
 try:
  q=a['qualifiers'];b=q['source_clause_binding'];e=a['evidence'][0];hit=paragraphs[e['paragraph_id']];p=hit[1];t=p['text'];ms={m['id']:m for m in p['mentions']};child=ms[e['subject_person_mention_id']];head=ms[e['object_person_mention_id']];father=ms[b['father_person_mention_id']]
  if (a['predicate']!='ritual_successor_of' or a['status']!='source_attested' or type(a.get('human_reviewed')) is not bool or len(a['evidence'])!=1
      or set(q)!={'source_term','succession_kind','legal_adoption_status','parentage_inference','source_clause_binding'}
      or q['succession_kind']!='biography_head_younger_brother_eldest_son_weisi' or q['legal_adoption_status']!='not_stated' or q['parentage_inference']!='not_inferred'
      or set(b)!={'kind','start','end','father_person_mention_id','father_assertion_id'} or b['kind']!='same_paragraph_named_head_wuzi_di_changzi_weisi'
      or e['chapter_id']!=hit[0] or e['quote']!=t or len({child['person_id'],head['person_id'],father['person_id']})!=3
      or any(m['kind']!='person'for m in [child,head,father]) or child['person_id']!=a['subject_person_id'] or head['person_id']!=a['object_person_id']
      or head['start']!=0 or not t.startswith(head['surface']+'字')
      or type(b['start'])is not int or type(b['end'])is not int or not 0<=b['start']<b['end']<=len(t)):return False
  term='無子，以弟'+father['surface']+'長子'+child['surface']+'為嗣'
  if (q['source_term']!=term or t[b['start']:b['end']]!=term or (b['start'] and t[b['start']-1]not in'。！？') or t[b['end']:b['end']+1]!='。'
      or father['start']!=b['start']+len('無子，以弟') or child['start']!=father['end']+len('長子') or child['end']+len('為嗣')!=b['end']):return False
  # A separate source-attested father record, with identical literal anchors and whole paragraph.
  f=next((x for x in assertions if x.get('id')==b['father_assertion_id']),None)
  return (bool(f)and f.get('predicate')=='father'and f.get('status')=='source_attested'and f.get('subject_person_id')==child['person_id']and f.get('object_person_id')==father['person_id']
          and f.get('qualifiers',{}).get('source_term')=='長子'and any(fe.get('paragraph_id')==p['id']and fe.get('chapter_id')==hit[0]and fe.get('quote')==t
          and fe.get('source_id')==e.get('source_id') and fe.get('work_id')==e.get('work_id') and fe.get('book_id')==e.get('book_id')
          and fe.get('subject_person_mention_id')==child['id']and fe.get('object_person_mention_id')==father['id']for fe in f.get('evidence',[])))
 except(KeyError,TypeError,ValueError,StopIteration,IndexError):return False
