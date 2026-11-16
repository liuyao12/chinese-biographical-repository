"""Editorial ancestor above an unnamed sibling's explicitly counted descendant.
Source claims remain unchanged; no missing person or source parent is created.
"""
def valid(member, rows, assertions, chapters, root):
 try:
  c=member['ancestor_connection'];assert c['type']=='ancestor_above_unnamed_sibling_descendant' and c['status']=='contextual_provisional' and c['human_reviewed'] is False and c['rationale']
  assert member['parent_person_id'] is None and member['source_assertion_id'] is None and member['connection']=='ancestor'
  ref=rows[c['reference_person_id']];father=rows[member['ancestor_person_id']];grand=rows[c['reference_grandfather_person_id']]
  groups=[set(r['source_person_ids'])for r in(member,ref,father,grand)];assert all(groups)and all(not x&y for i,x in enumerate(groups)for y in groups[i+1:])
  k=assertions[c['collateral_descendant_assertion_id']];f=assertions[c['reference_father_assertion_id']];g=assertions[c['reference_grandfather_assertion_id']];q=k['qualifiers']
  assert k['predicate']=='kinship_unspecified'and k['subject_person_id']in groups[0]and k['object_person_id']in groups[1]
  assert q['kinship_basis']=='fixed_received_collateral_appellation'and q['lineage']=='paternal'and q['lineage_interpretation']=='received_family_context_provisional'
  steps=q['source_generation_steps'];assert steps==[{'source_term':'玄孫','generation_distance':4},{'source_term':'之子','generation_distance':1}]
  n=sum(x['generation_distance']for x in steps);assert q['descendant_generation_distance_from_unnamed_sibling']==n and q['object_generation_relative_to_subject']==-n
  assert q['unnamed_ancestor_role']=={'relation_to_reference':'older_brother','reference_person_id':k['object_person_id'],'person_id':None} and q['exact_distance'] is None and q['connecting_person_ids'] is None
  assert member['generation_distance']==n+1 and member['intermediate_person_ids']==[None]*n
  assert f['predicate']=='father'and g['predicate']=='grandfather'and f['subject_person_id']==g['subject_person_id']==k['object_person_id']and f['object_person_id']in groups[2]and g['object_person_id']in groups[3]
  assert f['qualifiers']['lineage']==g['qualifiers']['lineage']=='paternal'and g['qualifiers']['generation_difference']==-2
  assert ref['parent_person_id']==father['person_id']and ref['source_assertion_id']==f['id']and father['parent_person_id']==grand['person_id']
  assert not any(a.get('predicate')=='father'and a.get('subject_person_id')in groups[0]for a in assertions.values())
  assert not any(a.get('predicate')=='father'and a.get('subject_person_id')in groups[1]and a.get('object_person_id')not in groups[2]for a in assertions.values())
  proofs=[k,f,g];cid=None;key=None;head=None
  try:from scripts.fixed_witness_fact_slots import valid as source_valid
  except ImportError:from fixed_witness_fact_slots import valid as source_valid
  for a in proofs:
   assert a['status']=='source_attested'and a['human_reviewed']is False
   aq=a['qualifiers'];assert not any(aq.get(t)for t in('adoptive','sworn','same_mother_only'))and aq.get('shared_father')is not False
   b=a['fixed_source_fact_binding'];assert b['kind']=='fixed_witness_person_fact_slots';key=b['key']if key is None else key;assert b['key']==key
   cs={e['chapter_id']for e in a['evidence']};assert len(cs)==1;ac=next(iter(cs));cid=ac if cid is None else cid;assert cid==ac and source_valid(a,chapters[cid],root)
   es={(e['chapter_id'],e['paragraph_id'],e['source_id'],e['quote'])for e in a['evidence']}
   if a is not k:head=es if head is None else head&es
  assert head
  refs=c['references'];assert len(refs)==3 and{r['assertion_id']for r in refs}=={a['id']for a in proofs}
  for r in refs:
   a=next(a for a in proofs if a['id']==r['assertion_id']);assert r['scope']and any(all(r[t]==e[t]for t in('work_id','book_id','source_id','chapter_id','paragraph_id','quote'))and r['url']in(chapters[cid]['source'].get('url'),chapters[cid]['source'].get('permalink'))for e in a['evidence'])
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):return False
