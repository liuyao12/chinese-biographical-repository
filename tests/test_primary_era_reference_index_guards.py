# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.primary_era_abbreviation import valid
from scripts.validate_corpus import normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class EraReferenceIndexGuards(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=json.loads((ROOT/'corpus/weishu-weishou/038-wanghuilong.json').read_text());events=json.loads((ROOT/'corpus/weishu-weishou/038-wanghuilong-life-events.json').read_text())['events'];cls.date=next(e['normalized_date']for e in events if e['id']=='le-weishu038-wf44-277');cls.chapters={cls.chapter['id']:cls.chapter}
 def rejected(self,date):
  self.assertIs(valid(date,self.chapters,ROOT),False);self.assertTrue(normalized_date_errors(date,self.chapters,root=ROOT))
 def test_positive_reference_zero(self):self.assertTrue(valid(self.date,self.chapters,ROOT));self.assertEqual(normalized_date_errors(self.date,self.chapters,root=ROOT),[])
 def test_invalid_reference_indices(self):
  for index in [999,-1,True,'0',None]:
   with self.subTest(index=index):
    d=copy.deepcopy(self.date);d['regnal_year_mapping']['reference_index']=index;self.rejected(d)
 def test_invalid_reference_containers(self):
  for refs in [[],None,{},'not-a-list',[None],['not-a-reference']]:
   with self.subTest(refs=refs):d=copy.deepcopy(self.date);d['references']=refs;self.rejected(d)

 def test_invalid_reference_columns(self):
  for columns in [None,[],'not-columns',0,False]:
   with self.subTest(columns=columns):
    d=copy.deepcopy(self.date);d['references'][0]['columns']=columns;self.rejected(d)
  d=copy.deepcopy(self.date);d['references'][0].pop('columns');self.rejected(d)
