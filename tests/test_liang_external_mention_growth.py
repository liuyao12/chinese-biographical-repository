import unittest,tempfile,pathlib,json,copy,importlib.util
from scripts import liang_xiao_close_family as mod
class Growth(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=pathlib.Path(self.tmp.name);self.pid='abc_def_123';self.other='abd_def_124';self.mid='c-extra:p001:m0';self.old={'id':self.pid,'label':'甲','family_path':{'retain':True},'unknown_metadata':{'exact':False},'aliases':[{'surface':'甲','mention_ids':['old:m'],'unknown':'preserve'}],'evidence':[{'mention_id':'old:m','chapter_id':'old','unknown':False}]};self.actor=copy.deepcopy(self.old);self.e={'work_id':'w-test','book_id':'b-test','source_id':'s-test','chapter_id':'c-extra','paragraph_id':'c-extra:p001','mention_id':self.mid,'quote':'甲'};self.actor['aliases'].append({'surface':'甲','mention_ids':[self.mid],'editorial_metadata':{'source_reading':False}});self.actor['evidence'].append(copy.deepcopy(self.e));self.physical={self.pid:self.actor,self.other:{'id':self.other,'aliases':[],'evidence':[]}};self.ch={'record_type':'marked_chapter','id':'c-extra','work_id':'w-test','book_id':'b-test','source_id':'s-test','paragraphs':[{'id':'c-extra:p001','text':'見甲。','mentions':[{'id':self.mid,'kind':'person','person_id':self.pid,'surface':'甲','start':1,'end':2}]}]};self.write('registry/works.json',{'works':[{'id':'w-test','books':[{'id':'b-test','chapter_ids':['c-extra']}]}]});self.write('registry/work-provenance.json',{'text_bases':{'s-test':{'source_id':'s-test','work_id':'w-test'}}});self.save()
 def write(self,path,x):
  p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False))
 def save(self):self.write('corpus/test/extra.json',self.ch)
 def check(self,caller=None,records=None):
  self.save();return mod._external_growth(self.root,self.physical,caller or self.physical,{self.pid:self.old},set(),{},records)
 def reject(self):
  with self.assertRaises((AssertionError,KeyError,ValueError)):self.check()
 def test01_valid_physical_addition_and_metadata(self):self.assertEqual(set(self.check()[self.pid]),{self.mid});self.assertEqual(self.actor['unknown_metadata'],self.old['unknown_metadata'])
 def test02_wrong_source(self):self.actor['evidence'][-1]['source_id']='other';self.reject()
 def test03_wrong_person(self):self.ch['paragraphs'][0]['mentions'][0]['person_id']=self.other;self.reject()
 def test04_wrong_mid(self):self.actor['evidence'][-1]['mention_id']='wrong';self.reject()
 def test05_no_reverse(self):self.actor['evidence'].pop();self.reject()
 def test06_no_alias(self):self.actor['aliases'].pop();self.reject()
 def test07_one_endpoint_caller(self):
  caller=copy.deepcopy(self.physical);caller[self.pid]['evidence'].pop()
  with self.assertRaises(AssertionError):self.check(caller)
 def test08_duplicate_other_person_reverse(self):self.physical[self.other]['evidence']=[copy.deepcopy(self.e)];self.reject()
 def test09_wrong_work_registration(self):self.write('registry/works.json',{'works':[{'id':'w-test','books':[{'id':'b-test','chapter_ids':[]}]}]});self.reject()
 def test10_bool_span(self):self.ch['paragraphs'][0]['mentions'][0]['start']=True;self.reject()
 def test11_old_alias_metadata_changed(self):self.actor['aliases'][0]['unknown']='lost';self.reject()
 def test12_old_evidence_metadata_bool_int(self):self.actor['evidence'][0]['unknown']=0;self.reject()
 def test13_caller_source_theft(self):
  caller=copy.deepcopy(self.ch);caller['paragraphs'][0]['text']='甲見。'
  with self.assertRaises(AssertionError):self.check(records=[caller])
 def test14_added_mid_can_append_existing_alias(self):
  self.actor['aliases'].pop();self.actor['aliases'][0]['mention_ids'].append(self.mid);self.assertTrue(self.check())
 def test15_extra_fake_reverse_without_physical_source(self):self.actor['evidence'].append(dict(self.e,mention_id='fake'));self.reject()
 def test16_added_pronoun_must_have_no_alias(self):
  self.ch['paragraphs'][0]['mentions'][0]['kind']='pronoun';self.actor['aliases'].pop();self.assertTrue(self.check());self.actor['aliases'].append({'surface':'甲','mention_ids':[self.mid]});self.reject()
 def test17_caller_new_cid_not_physical_rejected(self):
  fake=copy.deepcopy(self.ch);fake['id']='c-not-physical';fake['paragraphs'][0]['id']='c-not-physical:p001';fake['paragraphs'][0]['mentions'][0]['id']='c-not-physical:p001:m0'
  with self.assertRaises(AssertionError):self.check(records=[fake])
if __name__=='__main__':unittest.main(verbosity=2)
