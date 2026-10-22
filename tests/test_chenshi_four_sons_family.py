"""Qualified later named fathers, compatible earlier count; no mother/ordinal inference."""
from pathlib import Path
import unittest,json,copy,tempfile
from unittest.mock import patch
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts,assert_not_retired
from scripts.person_ids import allocate_child_id
R=Path(__file__).resolve().parents[1];ROOT='9w8_tqh_ysn';FAMILY='family-sanguozhi022-shi';KEYS=('kui','qia','xiu','guang');OLD=('54t_d9k_y56','gbv_pus_rwo','k0p_zxr_j50','uhf_53t_16u');NEW=tuple(ROOT+'_'+c for c in' CDEF'.strip())
class FourSons(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog(R);cls.fams=json.loads((R/'registry/family-assemblies.json').read_text());cls.decisions=json.loads((R/'corpus/xintangshu/family-tree-decisions.json').read_text())['decisions'];cls.assertions=json.loads((R/'corpus/xintangshu/071xia-chen-preface-assertions.json').read_text())['assertions']
 def test_four_qualified_selected_fathers_same_root(self):
  ss,aa=load_assemblies(R,self.catalog)
  for key,pid in zip(KEYS,NEW):
   d=next(x for x in self.decisions if x['id']=='ft-xintangshu071xia-chen-'+key);self.assertEqual(d['preferred_parent_person_id'],ROOT);self.assertEqual(d['excluded_assertion_ids'],[]);self.assertEqual(d['confidence_level'],'moderate');self.assertIn('not_independent_name_attestation',d['confidence_scope']);self.assertEqual(d['preferred_assertion_id'],'a-xintangshu071xia-chen-'+key+'-father');self.assertEqual(aa[pid]['parent_person_id'],ROOT);p=self.catalog[0][pid];self.assertEqual(p['family_path']['status'],'contextual_provisional');self.assertEqual(p['family_path']['evidence'][0]['source_id'],'s-xintangshu-071xia-chen-preface');self.assertEqual(len(p['family_path']['evidence']),1)
 def test_hhs_support_is_count_only_not_new_named_anchors(self):
  c=json.loads((R/'corpus/houhanshu/062.json').read_text());p=next(p for p in c['paragraphs']if p['id']=='c-houhanshu-062-xunhan-zhongchen:chen:chen-shi-body');self.assertIn('有六子紀諶最賢',p['text']);self.assertFalse(any(m.get('person_id')in NEW for m in p['mentions']))
  for key in KEYS:
   d=next(x for x in self.decisions if x['id'].endswith('-'+key));self.assertEqual({e['source_id']for e in d['evidence']},{'s-xintangshu-071xia-chen-preface','s-houhanshu-062-xunhan-zhongchen'})
 def test_no_new_ranks_mothers_or_life_facts(self):
  for key,pid in zip(KEYS,NEW):
   a=next(a for a in self.assertions if a['id']=='a-xintangshu071xia-chen-'+key+'-father');self.assertEqual(set(a['qualifiers']),{'source_term','lineage','source_clause_binding'});b=bundle(pid,root=R,catalog=self.catalog);self.assertEqual(b['title_holdings'],[]);self.assertEqual(b['date_normalizations'],[]);self.assertFalse(any(r['predicate']=='mother'for r in b['relations']));self.assertEqual(b['birth_order_constraints'],[])
 def test_existing_parents_and_middle_gaps_preserved(self):
  expected={'ji':'a-houhanshu062-chen-001','chen':'a-houhanshu062-chen-002','zhun':'a-sanguozhi022-chen-017'}
  for key,aid in expected.items():self.assertEqual(next(x for x in self.decisions if x['id'].endswith('-'+key))['preferred_assertion_id'],aid)
  for key in ['zhong','zuo','he','hui']:self.assertIsNone(next(x for x in self.decisions if x['id'].endswith('-'+key))['preferred_assertion_id'])
  ss,aa=load_assemblies(R,self.catalog);self.assertIsNone(aa[ROOT+'_B*A']['parent_person_id']);self.assertEqual(aa[ROOT+'_B*A']['ancestor_person_id'],ROOT+'_B');self.assertIsNone(aa[ROOT+'_B*B']['parent_person_id'])
 def test_public_old_ids_no_alias_and_allocator_prefix_guard(self):
  retired=retired_person_ids(R);self.assertTrue(set(OLD)<=retired)
  for old in OLD:
   self.assertNotIn(old,self.catalog[0]);self.assertTrue(allocation_conflicts(old+'_A',retired))
   with self.assertRaises(ValueError):assert_not_retired(old,R)
   with self.assertRaises(ValueError):allocate_child_id(old,set(self.catalog[0]),root=R)
   with self.assertRaises((KeyError,ValueError)):bundle(old,root=R,catalog=self.catalog)
  for p in self.catalog[0].values():self.assertTrue(set(OLD).isdisjoint(p.get('id_aliases',[])))
 def reject_member_change(self,change):
  x=copy.deepcopy(self.fams);g=next(x for x in x['assemblies']if x['id']==FAMILY);change({m['person_id']:m for m in g['members']});original=Path.read_text
  def read(p,*a,**kw):return json.dumps(x,ensure_ascii=False)if p==R/'registry/family-assemblies.json'else original(p,*a,**kw)
  with patch.object(Path,'read_text',read):
   with self.assertRaises(ValueError):load_assemblies(R,self.catalog)
 def test_wrong_father_rejected(self):self.reject_member_change(lambda rows:rows[NEW[0]].update(parent_person_id=ROOT+'_A'))
 def test_other_child_assertion_not_matching_rejected(self):self.reject_member_change(lambda rows:rows[NEW[0]].update(source_assertion_id='a-xintangshu071xia-chen-qia-father'))
 def test_brother_not_father_rejected(self):self.reject_member_change(lambda rows:rows[NEW[0]].update(source_assertion_id='a-houhanshu062-chen-004'))
 def test_later_name_not_relabelled_early_explicit_father(self):
  from scripts.validate_corpus import validate
  reg=json.loads((R/'registry/persons.json').read_text());h=json.loads((R/'corpus/houhanshu/062.json').read_text());p=next(p for p in h['paragraphs']if p['id']=='c-houhanshu-062-xunhan-zhongchen:chen:chen-shi-body');row=next(p for p in reg['persons']if p['id']==NEW[0]);row['family_path']['evidence']=[{'work_id':h['work_id'],'book_id':h['book_id'],'chapter_id':h['id'],'source_id':h['source_id'],'paragraph_id':p['id'],'quote':p['text'],'source_term':'有六子紀諶最賢'}];original=Path.read_text
  def read(q,*a,**kw):return json.dumps(reg,ensure_ascii=False)if q==R/'registry/persons.json'else original(q,*a,**kw)
  with patch.object(Path,'read_text',read):errors=validate(R)
  self.assertIn('家族路徑缺少相符的來源親屬陳述',errors)
if __name__=='__main__':unittest.main()
