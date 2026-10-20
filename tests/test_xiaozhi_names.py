import unittest,copy,json
from pathlib import Path
from scripts.name_childhood import validate_childhood_name
class XiaozhiNames(unittest.TestCase):
 def fixture(self):
  p={'id':'p','text':'甲者乙小字也','mentions':[{'id':'v','start':0,'end':1,'surface':'甲','person_id':'person'},{'id':'s','start':2,'end':3,'surface':'乙','person_id':'person'}]}
  def a(s,e,m=None):
   x={'paragraph_id':'p','start':s,'end':e,'surface':p['text'][s:e]}
   if m:x['person_mention_id']=m
   return x
  n={'person_id':'person','paragraph_id':'p','quote':p['text'],'xiaozhi':'甲','xiaozhi_basis':{'kind':'explicit_xiaozhi_statement','source_term':p['text'],'value_anchor':a(0,1,'v'),'subject_anchor':a(2,3,'s'),'marker_anchor':a(3,5),'status':'source_attested','human_reviewed':False,'rationale':'Synthetic source.'}};return n,p
 def test_explicit_same_person_statement(self):self.assertIsNone(validate_childhood_name(*self.fixture()))
 def test_source_only_courtesy_marker_not_childhood(self):
  n,p=self.fixture();p['text']='甲者乙字也';n['quote']=p['text'];self.assertRaises(ValueError,validate_childhood_name,n,p)
 def test_other_person_or_shifted_value_rejected(self):
  for change in ['person','position']:
   n,p=self.fixture()
   if change=='person':p['mentions'][0]['person_id']='other'
   else:n['xiaozhi_basis']['value_anchor']['start']=1
   self.assertRaises(ValueError,validate_childhood_name,n,p)
 def test_untyped_generic_alias_never_becomes_xiaozhi(self):
  self.assertIsNone(validate_childhood_name({'additional_names':['公','中軍大將軍']},None));self.assertRaises(ValueError,validate_childhood_name,{'xiaozhi':'公'},None)
 def test_no_marker_or_unverified_basis_rejected(self):
  for key,val in [('human_reviewed',True),('source_term','甲字乙'),('kind','guessed_from_alias')]:
   n,p=self.fixture();n['xiaozhi_basis'][key]=val;self.assertRaises(ValueError,validate_childhood_name,n,p)
 def test_actual_cao_shuang_childhood_is_separate_from_courtesy(self):
  root=Path(__file__).resolve().parents[1];rs=json.loads((root/'data/corpus/profile-names.json').read_text())['records'];r=next(r for r in rs if r.get('source_proposal_id')=='proposal-sgz009-names-shuang-xiaozhi');c=json.loads((root/'corpus/sanguozhi/009-caozhen.json').read_text());p=next(p for p in c['paragraphs']if p['id']==r['paragraph_id']);self.assertIsNone(validate_childhood_name(r,p));self.assertEqual(r['xiaozhi'],'黙');self.assertNotIn('zi',r);zi=next(r for r in rs if r.get('source_proposal_id')=='proposal-sgz009-names-shuang');self.assertEqual(zi['zi'],'昭伯')
if __name__=='__main__':unittest.main()
