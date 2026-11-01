"""A typed, provisional parent bridge from one child's mother and maternal grandfather.
Input source assertions stay primary; this derived edge is not a literal father sentence.
"""
def valid(assertion,assertions):
 try:
  assert type(assertion)is dict and type(assertions)is list
  a=assertion;q=a['qualifiers'];b=q['source_composed_parent_bridge'];assert isinstance(b,dict)and b['kind']=='mother_and_maternal_grandfather_same_child'
  assert a['predicate']=='father'and a['status']=='contextual_provisional'and a['human_reviewed']is False and a['evidence']
  assert q['parentage_role']=='assembly_inferred'and q['identity_status']=='contextual_provisional'
  assert b['derived']is True and b['literal_father_sentence']is False and b['same_child']is True and b['same_mother']is True and b['lineage']=='maternal'and b['status']=='contextual_provisional'and b['identity_status']=='contextual_provisional'
  assert b['basis_kind']=='editorial_input_labels_not_literal_quotes'
  for k in('mother_assertion_id','maternal_grandfather_assertion_id','child_person_id','mother_person_id','maternal_grandfather_person_id'):assert isinstance(b[k],str)and b[k]
  mm=[x for x in assertions if isinstance(x,dict)and x.get('id')==b['mother_assertion_id']];gg=[x for x in assertions if isinstance(x,dict)and x.get('id')==b['maternal_grandfather_assertion_id']];assert len(mm)==len(gg)==1;m,g=mm[0],gg[0]
  assert m['predicate']=='mother'and g['predicate']=='grandfather'and m['status']==g['status']=='source_attested'and m['human_reviewed']is False and g['human_reviewed']is False
  assert m['subject_person_id']==g['subject_person_id']==b['child_person_id']and m['object_person_id']==a['subject_person_id']==b['mother_person_id']and g['object_person_id']==a['object_person_id']==b['maternal_grandfather_person_id']
  assert len({b['child_person_id'],b['mother_person_id'],b['maternal_grandfather_person_id']})==3
  assert g['qualifiers']['lineage']=='maternal'and type(g['qualifiers']['generation_difference'])is int and g['qualifiers']['generation_difference']==-2 and g['qualifiers']['mother_person_id']==b['mother_person_id']and g['qualifiers']['identity_status']=='contextual_provisional'
  assert all(type(x['evidence'])is list and len(x['evidence'])==1 for x in(m,g,a))
  assert all(type(x['evidence'][0])is dict for x in(m,g,a))
  me,ge,ae=m['evidence'][0],g['evidence'][0],a['evidence'][0]
  for k in('work_id','book_id','source_id','chapter_id','paragraph_id','quote'):assert isinstance(me[k],str)and me[k]and me[k]==ge[k]==ae[k]
  assert me['object_person_mention_id']==ae['subject_person_mention_id']and ge['object_person_mention_id']==ae['object_person_mention_id']
  return True
 except(AssertionError,KeyError,TypeError,ValueError):return False
