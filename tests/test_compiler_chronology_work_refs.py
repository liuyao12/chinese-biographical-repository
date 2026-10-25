# coding:utf-8
import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
try:from scripts import fixed_compiler_chronology as model
except ImportError:import fixed_compiler_chronology as model
ROOT=Path(__file__).resolve().parents[1]
class ChronologyWorkReference(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/043-wangcheng.json').read_text());cls.d=json.loads((ROOT/'corpus/jinshu/043-wangcheng-compiler-chronology.json').read_text())['records'][0]
 def test_existing_work_and_provenance_are_directly_linked_without_new_dates(self):
  self.assertTrue(model.valid(self.d,self.ch,ROOT));s=self.d['external_evidence']['source'];self.assertEqual(s['work_id'],'w-zizhitongjian');self.assertEqual(s['work_provenance_ref'],'registry/work-provenance.json#/works/w-zizhitongjian');self.assertEqual(s['volume'],'088');self.assertNotIn('book_id',s);self.assertNotIn('chapter_id',s)
 def test_missing_or_wrong_work_and_dangling_provenance_are_rejected(self):
  original=model._read
  for kind in ['no_work','wrong_title','no_provenance','wrong_provenance_work','wrong_provenance_title']:
   def read(root,path):
    b=original(root,path)
    if path=='registry/works.json' and kind in ['no_work','wrong_title']:
     d=json.loads(b)
     if kind=='no_work':d['works']=[w for w in d['works']if w['id']!='w-zizhitongjian']
     else:next(w for w in d['works']if w['id']=='w-zizhitongjian')['title']='別一同題書'
     return json.dumps(d).encode()
    if path=='registry/work-provenance.json' and kind not in ['no_work','wrong_title']:
     d=json.loads(b)
     if kind=='no_provenance':del d['works']['w-zizhitongjian']
     elif kind=='wrong_provenance_work':d['works']['w-zizhitongjian']['work_id']='w-other'
     else:d['works']['w-zizhitongjian']['title']='別書'
     return json.dumps(d).encode()
    return b
   with self.subTest(kind=kind),patch.object(model,'_read',read):self.assertFalse(model.valid(self.d,self.ch,ROOT))
 def test_record_metadata_missing_id_wrong_id_or_dangling_pointer_rejected(self):
  for key,value in [('work_id',None),('work_id','w-other'),('work_provenance_ref','registry/work-provenance.json#/works/missing')]:
   d=copy.deepcopy(self.d)
   if value is None:del d['external_evidence']['source'][key]
   else:d['external_evidence']['source'][key]=value
   self.assertFalse(model.valid(d,self.ch,ROOT))
