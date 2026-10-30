# -*- coding: utf-8 -*-
"""Actual source-root tests; no reduced fixture, disk mutation, or source guard bypass."""
from pathlib import Path
import unittest,copy,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import fixed_jin036_wei_ner as owner,person_bundle
class WeiCloseKinTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=person_bundle.load_catalog(ROOT);cls.b,cls.roles,cls.actual,cls.ch=owner.close_kin_state(ROOT);cls.ids=set(cls.roles.values());cls.paragraphs={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.assertions=owner.expand(cls.b['expected_documents']['corpus/jinshu/036-wei-comparison-assertions.json'],cls.roles)['assertions']
 def counts(self,records=None,people=None):return owner.close_kin_counts(self.records if records is None else records,self.people if people is None else people,ROOT,self.ids)
 def test_actual_complete_phase(self):
  self.assertEqual(len(self.assertions),28);self.assertTrue(all(owner.close_kin_valid(a,self.paragraphs,ROOT)for a in self.assertions));self.assertEqual(len(self.counts()),4)
 def test_all_authoring_rows_accounted(self):self.assertEqual(len({x['research_row_id']for x in self.b['authoring_coverage']}),36)
 def test_caller_role_missing(self):
  people=self.people.copy();people.pop(self.roles['guan'])
  with self.assertRaises(ValueError):self.counts(people=people)
 def test_caller_wrong_uid_one_end(self):
  people=self.people.copy();p=copy.deepcopy(people.pop(self.roles['guan']));p['id']='z9x_0aa_0bb';people[p['id']]=p
  with self.assertRaises(ValueError):self.counts(people=people)
 def test_caller_reverse_missing(self):
  people=self.people.copy();p=copy.deepcopy(people[self.roles['guan']]);p['evidence']=[e for e in p['evidence']if e.get('chapter_id')!=self.ch['id']];people[p['id']]=p
  with self.assertRaises(ValueError):self.counts(people=people)
 def test_caller_source_sidecar_missing(self):
  records=[r for r in self.records if not(r.get('record_type')=='person_assertion_set'and r.get('chapter_id')==self.ch['id'])]
  with self.assertRaises(ValueError):self.counts(records=records)
 def test_caller_same_uid_wrong_span(self):
  records=copy.deepcopy(self.records);ch=next(c for c in records if c.get('id')==self.ch['id']);ch['paragraphs'][0]['mentions'][0]['start']+=1
  with self.assertRaises(ValueError):self.counts(records=records)
 def test_count_mutations(self):
  for mutate in [lambda r:r.update(reported_count=7),lambda r:r.update(normalized_date={'year':291}),lambda r:r.update(known_member_person_ids=[]),lambda r:r.update(count_scope='sons_of_reference')]:
   records=copy.deepcopy(self.records);d=next(d for d in records if d.get('record_type')=='source_family_count_report_set'and d.get('owner')=='fixed_jin036_wei_ner');mutate(d['reports'][-1])
   with self.assertRaises(ValueError):self.counts(records=records)
 def test_unknown_or_cross_claimed_count_owner_rejected(self):
  for owner,chapter in [('counterfeit','c-counterfeit'),('fixed_jin034_yanghu_ner',self.ch['id']),('fixed_jin036_wei_ner','c-counterfeit')]:
   records=self.records+[{'record_type':'source_family_count_report_set','owner':owner,'chapter_id':chapter,'reports':[]}]
   with self.assertRaises(ValueError):self.counts(records=records)
 def test_wrong_relation_semantics(self):
  for a in self.assertions:
   bad=copy.deepcopy(a);bad['subject_person_id'],bad['object_person_id']=bad['object_person_id'],bad['subject_person_id'];self.assertFalse(owner.close_kin_valid(bad,self.paragraphs,ROOT))
  a=copy.deepcopy(next(a for a in self.assertions if a['predicate']=='maternal_role'));a['predicate']='mother';self.assertFalse(owner.close_kin_valid(a,self.paragraphs,ROOT))
  a=copy.deepcopy(next(a for a in self.assertions if a['predicate']=='agnatic_cousin'));a['qualifiers']['kinship_structure']['distance']=2;self.assertFalse(owner.close_kin_valid(a,self.paragraphs,ROOT))
  a=copy.deepcopy(next(a for a in self.assertions if a['qualifiers'].get('affinal_relation')));a['qualifiers']['connecting_spouse_person_id']=self.roles['shi'];self.assertFalse(owner.close_kin_valid(a,self.paragraphs,ROOT))
 def test_count_not_lifetime_inventory_or_witness_rows(self):
  reports=self.counts();self.assertTrue(all(c['lifetime_child_inventory_complete']is None for c in reports));heng=next(c for c in reports if c['reference_person_id']==self.roles['heng']);self.assertTrue(heng['named_list_complete_for_reported_count']);self.assertEqual(len(heng['evidence']),2);self.assertEqual(heng['reported_count'],2);self.assertTrue(all('authoring_coverage'not in r and 'expected_documents'not in r for r in reports))
 def test_mutable_return_isolation(self):
  reports=self.counts();reports[0]['known_member_person_ids'].clear();self.assertTrue(self.counts()[0]['known_member_person_ids'])
if __name__=='__main__':unittest.main()
