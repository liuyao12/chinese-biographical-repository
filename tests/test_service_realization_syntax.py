"""Synthetic source syntax; no historical identity claim or full corpus fixture."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts import validate_corpus as native
from scripts.render_corpus import render
class ServiceRealizationSyntax(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.pid='abc_def_123';self.other='abd_def_124';self.cid='c-synthetic-service';self.sid='s-synthetic-service';self.par=self.cid+':p001';self.mid=self.par+':m0000';self.othermid=self.par+':m-other';self.text='甲授太守，未行而荊州陷。乙在郡。'
  self.make_source('未行')
 def write(self,p,x):
  f=self.root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 def make_source(self,term):
  self.text='甲授太守，'+term+'而荊州陷。乙在郡。';mentions=[{'id':self.mid,'start':0,'end':1,'surface':'甲','kind':'person','person_id':self.pid,'status':'resolved'},{'id':self.othermid,'start':self.text.index('乙'),'end':self.text.index('乙')+1,'surface':'乙','kind':'person','person_id':self.other,'status':'resolved'}];self.chapter={'format_version':'0.2','record_type':'marked_chapter','id':self.cid,'work_id':'w-synthetic','book_id':'b-synthetic','source_id':self.sid,'title':'語法測試','source':{'url':'https://example.test/source','permalink':'https://example.test/fixed','license_url':'https://creativecommons.org/publicdomain/zero/1.0/','image_verified':False},'text_sha256':hashlib.sha256(self.text.encode()).hexdigest(),'paragraphs':[{'id':self.par,'text':self.text,'annotation_status':'in_progress','mentions':mentions}],'annotation':{'status':'in_progress','human_reviewed':False}}
  self.e={'work_id':'w-synthetic','book_id':'b-synthetic','source_id':self.sid,'chapter_id':self.cid,'paragraph_id':self.par,'quote':self.text,'person_mention_id':self.mid};empty={'status':'unknown','date_expression':None,'evidence':[]};self.holding={'id':'h-synthetic','person_id':self.pid,'title':'太守','kind':'office','mode':'grant','status':'source_attested','effective_period':{'start':{'status':'source_event','event_type':'grant','date_expression':None,'evidence':[copy.deepcopy(self.e)]},'end':copy.deepcopy(empty)},'evidence':[copy.deepcopy(self.e)],'attestations':[{'id':'t-synthetic','paragraph_id':self.par,'person_mention_id':self.mid,'surface':'太守','start':2,'end':4,'usage':'narrative'}],'service_realization':{'status':'not_taken_up','source_term':term+'而荊州陷','evidence':[copy.deepcopy(self.e)]}}
  people=[]
  for pid,surface,mid in [(self.pid,'甲',self.mid),(self.other,'乙',self.othermid)]:people.append({'id':pid,'label':surface,'record_type':'historical_person','aliases':[{'surface':surface,'mention_ids':[mid]}],'evidence':[{'work_id':'w-synthetic','book_id':'b-synthetic','source_id':self.sid,'chapter_id':self.cid,'paragraph_id':self.par,'mention_id':mid,'quote':surface}]})
  self.write('registry/persons.json',{'next_number':1,'persons':people});self.write('registry/works.json',{'works':[{'id':'w-synthetic','title':'語法測試','books':[{'id':'b-synthetic','work_id':'w-synthetic','title':'卷一','chapter_ids':[self.cid]}]}]});self.write('corpus/progress.json',{'active_work_id':'w-synthetic','books':[{'book_id':'b-synthetic','chapter_id':self.cid,'text_status':'transcribed','person_status':'in_progress','complete':False}]});self.write('corpus/synthetic/source.json',self.chapter);f=self.root/'corpus/synthetic/source.xml';f.write_text(render(self.chapter));self.save_holding()
 def save_holding(self):self.write('corpus/synthetic/source-titles.json',{'format_version':'0.2','record_type':'title_holding_assertion_set','chapter_id':self.cid,'holdings':[self.holding]})
 def errors(self):self.save_holding();return native.validate(self.root)
 def test_granted_but_not_departed_weixing(self):self.assertEqual(self.errors(),[]);self.assertEqual(self.holding['mode'],'grant');self.assertNotIn('declination',self.holding)
 def test_original_buwang_regression(self):self.make_source('不往');self.assertEqual(self.errors(),[])
 def test_attestation_mode_cannot_claim_unassumed_grant(self):
  self.holding['mode']='attestation';self.assertTrue(any('授予未赴任' in e for e in self.errors()))
 def test_unrelated_wei_word_not_enough(self):
  self.holding['service_realization']['source_term']='未定';self.assertTrue(any('授予未赴任' in e for e in self.errors()))
 def test_other_person_cannot_be_service_subject(self):
  self.holding['service_realization']['evidence'][0]['person_mention_id']=self.othermid;self.assertIn('未赴任人物、來源原詞或證據不符',self.errors())
 def test_source_term_must_occur_in_quote(self):
  self.holding['service_realization']['source_term']='不往';self.assertIn('未赴任人物、來源原詞或證據不符',self.errors())
 def test_quote_must_be_actual_source(self):
  self.holding['service_realization']['evidence'][0]['quote']='甲未行而京城陷';self.assertIn('未赴任人物、來源原詞或證據不符',self.errors())
 def test_wrong_source_still_rejected(self):
  self.holding['service_realization']['evidence'][0]['source_id']='s-foreign';self.assertIn('未赴任人物、來源原詞或證據不符',self.errors())
 def test_actual_service_status_cannot_replace_not_taken_up(self):
  self.holding['service_realization']['status']='assumed';self.assertTrue(any('授予未赴任' in e for e in self.errors()))
 def test_other_generic_title_checks_still_run(self):
  self.holding['attestations'][0]['surface']='刺史';self.assertIn('稱號用稱文字或種類不符',self.errors())
if __name__=='__main__':unittest.main(verbosity=2)
