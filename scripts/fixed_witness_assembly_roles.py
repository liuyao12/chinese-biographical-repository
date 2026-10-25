"""Trusted finite witness roles for editorial assembly; never source father facts."""
from pathlib import Path
import json
BASES=('fixed_complete_witness_zu_fu_sequence','shared_father_with_estate')
def valid(member,rows,assertions,chapters,root):
 try:
  try:from scripts.fixed_kanripo_fact_slots import grammar,expand,strict
  except ImportError:from fixed_kanripo_fact_slots import grammar,expand,strict
  root=Path(root).resolve();cfgpath=root/'scripts/fixed_witness_assembly_roles.json'
  assert cfgpath.resolve()==cfgpath
  cfg=json.loads(cfgpath.read_text());assert cfg['format_version']=='0.1'
  c=member['parent_connection'];basis=c['interpretation_basis']
  assert basis in BASES and c['status']=='contextual_provisional'and c['human_reviewed']is False and isinstance(c['rationale'],str)and c['rationale'].strip()and member['source_assertion_id']is None
  binding=cfg['bindings'][c['fixed_witness_assembly_key']];assert binding['basis']==basis
  ch=chapters[binding['chapter_id']];recipe,roles=grammar(ch,root)
  assert recipe['key']==binding['recipe_key']
  expected={v['record']['id']:expand(v['record'],roles)for v in recipe['slots']}
  proof=[]
  for aid in binding['assertion_ids']:
   a=assertions[aid];assert strict(a,expected[aid])and a['status']=='source_attested'
   q=a['qualifiers'];assert not any(q.get(k)for k in('adoptive','sworn','same_mother_only'))and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal')
   proof.append(a)
  for marker in binding['work_markers']:
   p=ch['paragraphs'][marker['paragraph_index']];assert p['text_layer']==marker['text_layer']
   hits=[m for m in p['mentions']if m['start']==marker['start']and m['end']==marker['end']]
   assert len(hits)==1 and all(hits[0].get(k)==marker[k]for k in('kind','surface','work_id'))and p['text'][marker['end']:marker['end']+1]=='曰'
  parent=set(rows[member['parent_person_id']]['source_person_ids']);child=set(member['source_person_ids'])
  assert len(parent)==len(child)==1 and not parent&child
  if basis=='fixed_complete_witness_zu_fu_sequence':
   assert c['type']=='parent_between_consecutive_ancestors'
   n,g=proof;assert (n['predicate'],g['predicate'])==('father','grandfather')
   assert n['subject_person_id']==g['subject_person_id']and n['subject_person_id']in rows[c['chain_subject_person_id']]['source_person_ids']and n['object_person_id']in child and g['object_person_id']in parent
   assert len({n['subject_person_id'],n['object_person_id'],g['object_person_id']})==3
   assert c['nearer_ancestor_assertion_id']==n['id']and c['farther_ancestor_assertion_id']==g['id']
   assert len(n['evidence'])==len(g['evidence'])==1 and all(n['evidence'][0][k]==g['evidence'][0][k]for k in('work_id','book_id','source_id','chapter_id','paragraph_id','quote'))
  else:
   assert c['type']=='shared_father_through_sibling'
   s,f=proof;assert s['predicate']=='brother'and f['predicate']=='father'
   sib=rows[c['sibling_person_id']];assert sib['parent_person_id']==member['parent_person_id']
   other=set(sib['source_person_ids']);assert len(other)==1 and not(child&other or parent&other)
   assert s['subject_person_id']in child and s['object_person_id']in other and f['subject_person_id']in other and f['object_person_id']in parent
   assert c['sibling_assertion_id']==s['id']and c['sibling_father_assertion_id']==f['id']
   assert s['qualifiers']['shared_maternal_origin']['not_proof_of_same_father_by_itself']is True
   # Literal requirements are trusted static frame data, not record-supplied regex.
   p=ch['paragraphs'][binding['estate_frame']['paragraph_index']]
   assert all(p['text'][v['start']:v['end']]==v['surface']for v in binding['estate_frame']['literal_spans'])
  assert not any(a.get('predicate')=='father'and a.get('subject_person_id')in child and a.get('object_person_id')not in parent for a in assertions.values())
  refs=c['references'];assert len(refs)==len(proof)and {r['assertion_id']for r in refs}=={a['id']for a in proof}
  for ref in refs:
   a=next(a for a in proof if a['id']==ref['assertion_id']);assert ref['scope']and ref['url']in(ch['source'].get('url'),ch['source'].get('permalink'))and any(all(ref[k]==e[k]for k in('work_id','book_id','source_id','chapter_id','paragraph_id','quote'))for e in a['evidence'])
  return True
 except(AssertionError,KeyError,TypeError,ValueError,AttributeError,IndexError,StopIteration,OSError):return False
