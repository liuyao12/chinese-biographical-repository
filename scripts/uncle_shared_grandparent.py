# coding:utf-8
"""Editorial father of an explicit paternal uncle via nephew's named father+grandfather.
No source father is synthesized; only already validated complete-witness roles qualify.
"""
def valid(member,rows,assertions,chapters,root):
 try:
  c=member['parent_connection'];assert c['type']=='parent_from_nephew_named_father_and_grandfather'and c['status']=='contextual_provisional'and c['human_reviewed']is False and c['rationale']and member['source_assertion_id']is None
  n=rows[c['nephew_person_id']];f=rows[c['nephew_father_person_id']];g=rows[member['parent_person_id']]
  ids=[set(x['source_person_ids'])for x in(member,n,f,g)];assert all(ids)and all(not x&y for j,x in enumerate(ids)for y in ids[j+1:])
  u=assertions[c['paternal_uncle_assertion_id']];nf=assertions[c['nephew_father_assertion_id']];ng=assertions[c['nephew_grandfather_assertion_id']]
  assert u['predicate']=='paternal_uncle'and nf['predicate']=='father'and ng['predicate']=='grandfather'and u['subject_person_id']==nf['subject_person_id']==ng['subject_person_id']in ids[1]
  assert u['object_person_id']in ids[0]and nf['object_person_id']in ids[2]and ng['object_person_id']in ids[3]
  assert u['qualifiers']['lineage']==nf['qualifiers']['lineage']==ng['qualifiers']['lineage']=='paternal'and u['qualifiers']['generation_difference']==-1 and ng['qualifiers']['generation_difference']==-2
  assert u['qualifiers']['father_person_id']is None and u['qualifiers']['source_seniority']in('older_than_subject_father','younger_than_subject_father')
  assert n['parent_person_id']==f['person_id']and n['source_assertion_id']==nf['id']and f['parent_person_id']==g['person_id']
  assert not any(a['predicate']=='father'and a['subject_person_id']in(ids[0]|ids[2])and a['object_person_id']not in ids[3]for a in assertions.values())
  proofs=[u,nf,ng];cid=None;shared=None;recipe_key=None
  try:from scripts.fixed_witness_fact_slots import valid as source_valid
  except ImportError:from fixed_witness_fact_slots import valid as source_valid
  for a in proofs:
   assert a['status']=='source_attested'and a['human_reviewed']is False and a['fixed_source_fact_binding']['kind']=='fixed_witness_person_fact_slots'
   q=a['qualifiers'];assert q.get('adopted_for_family_tree')is not False and not any(q.get(k)for k in('adoptive','sworn','same_mother_only'))
   key=a['fixed_source_fact_binding']['key'];recipe_key=key if recipe_key is None else recipe_key;assert key==recipe_key
   evidence=a['evidence'];cids={e['chapter_id']for e in evidence};assert len(cids)==1
   ac=next(iter(cids));cid=ac if cid is None else cid;assert ac==cid and source_valid(a,chapters[cid],root)
   ekeys={(e['chapter_id'],e['paragraph_id'],e['source_id'],e['quote'])for e in evidence}
   if a is not u:shared=ekeys if shared is None else shared&ekeys
  assert shared # named father+grandfather share a head; uncle may occur later in this fully bound same biography.
  refs=c['references'];assert len(refs)==3 and{r['assertion_id']for r in refs}=={a['id']for a in proofs}
  for ref in refs:
   a=next(a for a in proofs if a['id']==ref['assertion_id']);assert ref['scope']and any(all(ref[k]==e[k]for k in('work_id','book_id','source_id','chapter_id','paragraph_id','quote'))and ref['url']in(chapters[cid]['source'].get('url'),chapters[cid]['source'].get('permalink'))for e in a['evidence'])
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):return False
