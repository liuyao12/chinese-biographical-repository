# coding:utf-8
import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
try:from scripts import fixed_compiler_chronology as model
except ImportError:import fixed_compiler_chronology as model
ROOT=Path(__file__).resolve().parents[1]
class CompilerChronology(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/043-wangcheng.json').read_text())
  cls.d=json.loads((ROOT/'corpus/jinshu/043-wangcheng-compiler-chronology.json').read_text())['records'][0]
 def test_valid_qualified_placement_keeps_local_date_unknown(self):
  self.assertTrue(model.valid(self.d,self.ch,ROOT));self.assertEqual(self.d['placement']['year'],312)
  e=json.loads((ROOT/'corpus/jinshu/043-wangcheng-life-events.json').read_text())['events'][0]
  self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e)
 def test_record_semantic_mutations_rejected(self):
  for path,value in [(('placement','year'),313),(('placement','year'),306),(('placement','month'),12),(('placement','human_reviewed'),True),(('placement','selection_status'),'source_explicit'),(('timeline_use','must_display_qualification'),False),(('timeline_use','birth_year_inference_permitted'),True),(('person_id',),'different_person'),(('linked_life_event_id',),'different_death')]:
   with self.subTest(path=path,value=value):
    d=copy.deepcopy(self.d);v=d
    for k in path[:-1]:v=v[k]
    v[path[-1]]=value;self.assertFalse(model.valid(d,self.ch,ROOT))
 def test_external_evidence_cannot_be_truncated_relayered_or_co_shifted(self):
  original=model._read
  for kind in ['missing_note','co_shift','wrong_layer','wrong_raw','wrong_calendar']:
   def read(root,path):
    b=original(root,path)
    if path==self.d['external_chronology_proof']['path']:
     q=json.loads(b)
     if kind=='missing_note':q['anchors']=q['anchors'][:2]
     elif kind=='co_shift':q['unit']['start']+=1;q['unit']['end']+=1
     elif kind=='wrong_layer':q['layers']['qualification']='received_tongjian_annal_body'
     elif kind=='wrong_raw':q['source']['sha256']='0'*64
     elif kind=='wrong_calendar':q['calendar']['first_year']=308
     return json.dumps(q).encode()
    return b
   with self.subTest(kind=kind),patch.object(model,'_read',read):self.assertFalse(model.valid(self.d,self.ch,ROOT))
 def test_linked_event_date_or_subject_change_rejected(self):
  original=model._read
  for kind in ['dated','foreign','title_event','truncated_quote']:
   def read(root,path):
    b=original(root,path)
    if path=='corpus/jinshu/043-wangcheng-life-events.json':
     q=json.loads(b);e=q['events'][0]
     if kind=='dated':e['normalized_date']={'year':312}
     elif kind=='foreign':e['person_id']='foreign'
     elif kind=='title_event':e['event_type']='enfeoffment'
     else:e['evidence'][0]['quote']=e['evidence'][0]['quote'][:20]
     return json.dumps(q).encode()
    return b
   with self.subTest(kind=kind),patch.object(model,'_read',read):self.assertFalse(model.valid(self.d,self.ch,ROOT))
 def test_root_is_required_and_not_global_cached(self):
  self.assertFalse(model.valid(self.d,self.ch,ROOT/'missing'))
  self.assertTrue(model.valid(self.d,self.ch,ROOT))
 def test_duplicate_event_placement_rejected(self):
  row={'record_type':'biographical_source_detail_set','chapter_id':self.ch['id'],'records':[self.d,self.d]}
  self.assertTrue(model.errors(ROOT,[self.ch,row]))
 def test_bundle_boundary_rechecks_copied_catalog_link(self):
  try:from scripts.person_bundle import load_catalog,bundle
  except ImportError:from person_bundle import load_catalog,bundle
  people,records=load_catalog(ROOT)
  rows=copy.deepcopy(list(records))
  e,=[e for row in rows for e in row.get('events',[])if e.get('id')==self.d['linked_life_event_id']]
  e['normalized_date']={'year':312}
  with self.assertRaises(ValueError):bundle(self.d['person_id'],ROOT,catalog=(people,rows))
