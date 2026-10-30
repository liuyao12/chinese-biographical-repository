from pathlib import Path
import unittest,json,copy,sys,importlib.util,hashlib
ROOT=Path(__file__).resolve().parents[1]
if Path(__file__).parent.name=='tests':
 sys.path.insert(0,str(ROOT));from scripts.evaluated_biography_gift import valid
 FIX=ROOT/'tests/fixtures/evaluated-biography-gift.json'
else:
 spec=importlib.util.spec_from_file_location('test_evaluated_gift',Path(__file__).with_name('evaluated_biography_gift.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);valid=m.valid;FIX=Path(__file__).with_name('fixture.json')
class Cases(unittest.TestCase):
 def setUp(self):self.x=json.loads(FIX.read_bytes())
 def call(self,x=None):
  x=x or self.x;p=x['paragraph'];cid=x['chapter_id'];return valid(x['holding'],{p['id']:(cid,p)},{m['id']:(cid,p['id'],m)for m in p['mentions']},{x['death']['id']:x['death']})
 def test_same_topic_not_evaluator(self):self.assertTrue(self.call())
 def test_evaluator_cannot_receive(self):
  self.x['holding']['person_id']=next(m['person_id']for m in self.x['paragraph']['mentions']if m['surface']=='桓溫');self.assertFalse(self.call())
 def test_object_third_person_rejected(self):
  a=self.x['holding']['posthumous_basis']['object_anchor'];self.x['paragraph']['mentions'].append(dict(id='third-object',start=a['start'],end=a['end'],surface='之',kind='person',person_id='a1b_c2d_e3f'));self.assertFalse(self.call())
 def test_new_topic_in_career_rejected(self):
  a=self.x['holding']['posthumous_basis']['career_anchor'];self.x['paragraph']['mentions'].append(dict(id='third-topic',start=a['start']+1,end=a['start']+3,surface=self.x['paragraph']['text'][a['start']+1:a['start']+3],kind='person',person_id='a1b_c2d_e3f'));self.assertFalse(self.call())
 def test_cross_paragraph_and_discontinuous_rejected(self):
  self.x['holding']['posthumous_basis']['career_anchor']['paragraph_id']='other';self.assertFalse(self.call());self.setUp();self.x['holding']['posthumous_basis']['career_anchor']['start']+=1;self.assertFalse(self.call())
 def test_no_year_or_end_added(self):
  self.x['holding']['effective_period']['start']['normalized_date']={'year':377};self.assertFalse(self.call());self.setUp();self.x['holding']['effective_period']['end']['normalized_date']={'year':426};self.assertFalse(self.call())
 def test_wrong_death_and_title_rejected(self):
  self.x['death']['person_id']='a1b_c2d_e3f';self.assertFalse(self.call());self.setUp();self.x['holding']['title']='簡公';self.assertFalse(self.call())
 def test_malformed(self):
  for h in [None,[],True,{},'x']:self.assertFalse(valid(h,{}, {},{}))
 def test_consistent_rekey(self):
  old=self.x['holding']['person_id']
  def remap(v):
   if isinstance(v,dict):return{k:remap(x)for k,x in v.items()}
   if isinstance(v,list):return[remap(x)for x in v]
   return 'a1b_c2d_e3f'if v==old else v
  self.assertTrue(self.call(remap(self.x)))
 def test_single_end_rekey(self):self.x['holding']['person_id']='a1b_c2d_e3f';self.assertFalse(self.call())
if __name__=='__main__':unittest.main()
