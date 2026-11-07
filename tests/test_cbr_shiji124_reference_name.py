import copy,json,unittest
from pathlib import Path
from scripts import fixed_shiji124_zhaotayu_reference_name as h
from scripts.person_bundle import load_catalog
ROOT=Path(__file__).resolve().parents[1]
class Shiji124ReferenceNameTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter,cls.pid,cls.case,cls.docs=h.state(ROOT);cls.name=cls.docs[h.NP]['records'][0];cls.people,cls.records=load_catalog(ROOT)
 def test_actual_complete_owner_and_catalog(self):
  self.assertTrue(h.component_valid(self.name,self.chapter,ROOT));self.assertTrue(h.catalog_valid(ROOT,self.people,self.records))
 def test_original_two_mids_and_literal_punctuation(self):
  p=self.chapter['paragraphs'][14];self.assertEqual(p['text'][96:102],'趙他、羽公子');self.assertEqual([m['surface']for m in p['mentions']if m['id']in self.name['component_source_binding']['source_mention_ids']],['趙他','羽公子']);self.assertIsNone(self.name['component_source_binding']['source_literal_full_name'])
 def test_no_unapproved_component_or_reference(self):
  for field,value in [('ming','他'),('zi','羽公子'),('surname','佗')]:
   n=copy.deepcopy(self.name);n[field]=value;self.assertFalse(h.component_valid(n,self.chapter,ROOT))
  n=copy.deepcopy(self.name);n['references'][0]['quote']='字他羽';self.assertFalse(h.component_valid(n,self.chapter,ROOT))
 def test_reject_changed_or_incomplete_caller_chapter(self):
  c=copy.deepcopy(self.chapter);c['paragraphs'][14]['text']=c['paragraphs'][14]['text'].replace('趙他、羽公子','趙他羽公子');self.assertFalse(h.component_valid(self.name,c,ROOT));self.assertFalse(h.component_valid(self.name,dict(self.chapter,paragraphs=self.chapter['paragraphs'][14:15]),ROOT))
 def test_reject_missing_name_or_address_catalog(self):
  for kind in ('person_name_component_set','person_address_assertion_set'):
   records=[r for r in self.records if not(r.get('record_type')==kind and r.get('chapter_id')==h.CID)]
   with self.assertRaises(ValueError):h.catalog_valid(ROOT,self.people,records)
 def test_only_exact_same_chapter_retirement_owner(self):
  dec=copy.deepcopy(self.docs[h.IP]['decisions'][0]);self.assertTrue(h.same_source_retirement_valid(ROOT,dec,[h.RETIRED]));dec['rationale']='同名'
  self.assertFalse(h.same_source_retirement_valid(ROOT,dec,[h.RETIRED]));self.assertFalse(h.same_source_retirement_valid(ROOT,self.docs[h.IP]['decisions'][0],[]))
if __name__=='__main__':unittest.main()
