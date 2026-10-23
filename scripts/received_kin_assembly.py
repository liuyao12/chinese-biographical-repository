"""Editorial assembly only, after fully role-bound received source kinship.
No new source father assertions, family-name guesses or inferred generations.
"""
def valid(member,rows,assertions,chapters,root):
 try:
  c=member['parent_connection'];basis=c['interpretation_basis'];assert c['status']=='contextual_provisional'and c['human_reviewed']is False and c['rationale']and member['source_assertion_id']is None
  try:from .received_quoted_family import valid as kin_valid
  except ImportError:from received_quoted_family import valid as kin_valid
  ps={p['id']:(ch['id'],p)for ch in chapters.values()for p in ch['paragraphs']};parent=rows[member['parent_person_id']];ids=set(member['source_person_ids']);proof=[]
  def source(id):
   a=assertions[id];q=a['qualifiers'];assert not any(q.get(k)for k in('adoptive','sworn','same_mother_only'))and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal')
   if basis=='fixed_complete_witness_shared_father':
    cids={e['chapter_id']for e in a['evidence']};assert len(cids)==1;cid=next(iter(cids));ch=chapters[cid];assert ch.get('annotation',{}).get('fixed_wikisource_unit_ref')
    if a.get('fixed_source_fact_binding',{}).get('kind')=='fixed_witness_person_fact_slots':
     try:from scripts.fixed_witness_fact_slots import valid as witness_valid
     except ImportError:from fixed_witness_fact_slots import valid as witness_valid
     assert witness_valid(a,ch,root)
    elif 'received_family_frame'in q:
     try:from scripts.punctuated_family_frames import valid as frame_valid
     except ImportError:from punctuated_family_frames import valid as frame_valid
     assert frame_valid(a,ps,chapters,root)
    else:raise AssertionError('No validated complete-witness family role')
   else:assert kin_valid(a,ps,chapters,root)
   proof.append(a);return a
  if basis=='fixed_received_zu_fu_sequence':
   assert c['type']=='parent_between_consecutive_ancestors';n=source(c['nearer_ancestor_assertion_id']);g=source(c['farther_ancestor_assertion_id']);assert n['predicate']=='father'and g['predicate']=='grandfather'and n['subject_person_id']==g['subject_person_id']and n['subject_person_id']in rows[c['chain_subject_person_id']]['source_person_ids']and n['object_person_id']in ids and g['object_person_id']in parent['source_person_ids'];assert n['qualifiers']['source_kinship_frame']==g['qualifiers']['source_kinship_frame']and n['qualifiers']['source_kinship_frame']['rule']=='annotated_head_ancestor_offices'and len({n['subject_person_id'],n['object_person_id'],g['object_person_id']})==3
  elif basis in('fixed_received_shared_father','fixed_complete_witness_shared_father'):
   if c['type']=='shared_father_through_sibling':siblings=[c['sibling_person_id']];edges=[c['sibling_assertion_id']]
   else:assert c['type']=='shared_father_through_sibling_chain';siblings=c['sibling_person_ids'];edges=c['sibling_assertion_ids'];assert len(siblings)==len(edges)and 2<=len(edges)<=3
   current=ids;seen=set(ids)
   for sid,edge in zip(siblings,edges):
    row=rows[sid];a=source(edge);other=set(row['source_person_ids']);assert a['predicate']=='brother'and row['parent_person_id']==member['parent_person_id']and not(seen&other);assert(a['subject_person_id']in current and a['object_person_id']in other)or(a['object_person_id']in current and a['subject_person_id']in other);current=other;seen|=other
   f=source(c['sibling_father_assertion_id']);assert f['predicate']=='father'and f['subject_person_id']in current and f['object_person_id']in parent['source_person_ids']
  else:raise AssertionError('unsupported received assembly basis')
  assert not any(a['predicate']=='father'and a['subject_person_id']in ids and a['object_person_id']not in parent['source_person_ids']for a in assertions.values())
  refs=c['references'];assert len(refs)==len(proof)and{r['assertion_id']for r in refs}=={a['id']for a in proof}
  for r in refs:
   a=next(a for a in proof if a['id']==r['assertion_id']);assert r['scope']and any(all(r[k]==e[k]for k in('work_id','book_id','source_id','chapter_id','paragraph_id','quote'))and r['url']in[chapters[e['chapter_id']]['source'].get('url'),chapters[e['chapter_id']]['source'].get('permalink')]for e in a['evidence'])
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration,IndexError,AttributeError):return False
