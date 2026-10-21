import unittest,json,copy
from pathlib import Path
from scripts.preferred_name_components import reading_errors
ROOT=Path(__file__).resolve().parents[1]
class PreferredNameReviewStateTests(unittest.TestCase):
 def setUp(self):
  self.names=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records'];self.chapters={r['id']:r for p in(ROOT/'corpus').glob('*/*.json')for r in[json.loads(p.read_text())]if r.get('record_type')=='marked_chapter'};self.reading=json.loads((ROOT/'corpus/jinshu/098-huanwen-preferred-name-components.json').read_text())['readings'][0]
 def test_true_and_false_keep_same_source_semantics(self):
  for value in [True,False]:
   r=copy.deepcopy(self.reading);r['human_reviewed']=value;self.assertEqual(reading_errors(r,self.names,self.chapters),[])
 def test_review_state_must_be_boolean(self):
  for value in ['true',1,None,[],{}]:
   r=copy.deepcopy(self.reading);r['human_reviewed']=value;self.assertTrue(reading_errors(r,self.names,self.chapters))
 def test_reviewed_true_does_not_excuse_wrong_anchor(self):
  r=copy.deepcopy(self.reading);r['human_reviewed']=True;r['records'][0]['anchor']['start']+=1;self.assertTrue(reading_errors(r,self.names,self.chapters))
 def test_validation_never_changes_review_state(self):
  for value in [True,False]:
   r=copy.deepcopy(self.reading);r['human_reviewed']=value;before=copy.deepcopy(r);reading_errors(r,self.names,self.chapters);self.assertEqual(r,before)
