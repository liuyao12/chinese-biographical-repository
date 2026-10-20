import copy
import json
import unittest
from pathlib import Path
from scripts.person_bundle import bundle, load_catalog
ROOT=Path(__file__).resolve().parents[1]
PID='84w_57j_1n6'
class DeHouName(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.catalog=load_catalog()
 def test_table_name_has_fixed_source_and_person_cell(self):
  b=bundle(PID,catalog=self.catalog);n=next(n for n in b['name_components']if n['person_id']==PID);self.assertEqual((n['title'],n['surname'],n['ming']),('德侯',None,'通'));self.assertEqual(n['kind'],'table_cell');self.assertEqual(n['source_revision'],'9484995');self.assertNotIn('paragraph_id',n);self.assertTrue(any(p['id']==n['table_cell_id']and p['text']==n['quote']for p in b['table_passages']))
 def test_alternative_name_is_not_unconditional_alias_or_father(self):
  b=bundle(PID,catalog=self.catalog);d=next(d for d in b['identity_decisions']if d['id']=='d-shiji106-040'and d['person_id']==PID);self.assertEqual(d['name_identification']['alternative_reported_ming'],['廣']);p=next(p for p in b['persons']if p['id']==PID);self.assertNotIn('廣',[a['surface']for a in p['aliases']]);self.assertFalse(any(r['predicate']=='father'and r['subject_person_id']==PID for r in b['relations']))
 def changed_name(self, fn):
  c=copy.deepcopy(self.catalog);n=next(n for r in c[1]if r.get('record_type')=='person_name_component_set'for n in r['records']if n['person_id']==PID);fn(n);return c
 def test_wrong_fixed_revision_rejected(self):
  with self.assertRaisesRegex(ValueError,'姓名組件'):bundle(PID,catalog=self.changed_name(lambda n:n.update(source_revision='1')))
 def test_another_persons_named_cell_rejected(self):
  def change(n):
   t=next(r['table']for r in self.catalog[1]if r.get('record_type')=='historical_table_source'and r['table']['id']=='shiji-018');c=next(c for f in t['fragments']for r in f['rows']for c in r['cells']if c['id']=='shiji-018-t1-r129-c02');n.update(table_cell_id=c['id'],quote=c['text'],person_mention_id=c['person_mentions'][0]['id'],surname='劉',ming='廣')
  with self.assertRaisesRegex(ValueError,'姓名組件'):bundle(PID,catalog=self.changed_name(change))
 def test_invented_name_rejected(self):
  with self.assertRaisesRegex(ValueError,'姓名組件'):bundle(PID,catalog=self.changed_name(lambda n:n.update(ming='廣')))
 def test_partial_cell_quote_rejected(self):
  with self.assertRaisesRegex(ValueError,'姓名組件'):bundle(PID,catalog=self.changed_name(lambda n:n.update(quote='通')))
