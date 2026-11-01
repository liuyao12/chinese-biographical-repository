"""Normal validator tests on tiny synthetic received prose, not XunLang identity proof."""
import unittest,tempfile,json,hashlib,copy
from pathlib import Path
from scripts.validate_corpus import validate
from scripts.render_corpus import render
class JointResistanceGift(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.cid='c-synthetic-joint';self.sid='s-synthetic-joint';self.par=self.cid+':p001';self.persons=['abc_def_123','abd_def_124','abe_def_125','abf_def_126','abg_def_127'];self.make()
 def write(self,path,value):
  p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 def make(self,prefix='先有戊事。',age=True):
  text=prefix+'因厚撫慰甲，令與乙等共拒敵丙。丙平，遷使持節、安北將軍、合州刺史。天嘉六年卒'+('，時年四十八'if age else'')+'。贈南豫州刺史，諡曰壯。子丁嗣。';self.text=text
  def marker(key,s,pid,start=None):
   i=text.index(s)if start is None else start;return{'id':self.par+':'+key,'start':i,'end':i+len(s),'surface':s,'person_id':pid,'kind':'person','status':'resolved'}
  rec=marker('rec','甲',self.persons[0]);ally=marker('ally','乙',self.persons[1]);opp=marker('opp','敵丙',self.persons[2]);resume=marker('resume','丙',self.persons[2],text.index('丙平'));outside=marker('outside','戊',self.persons[3]);son=marker('son','丁',self.persons[4]);self.ms=[outside,rec,ally,opp,resume,son]
  self.chapter={'format_version':'0.2','record_type':'marked_chapter','id':self.cid,'work_id':'w-synthetic','book_id':'b-synthetic','source_id':self.sid,'title':'語法測試','source':{'url':'https://example.test/source','permalink':'https://example.test/fixed','license_url':'https://creativecommons.org/publicdomain/zero/1.0/','image_verified':False},'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'paragraphs':[{'id':self.par,'text':text,'text_layer':'received_chapter','annotation_status':'in_progress','mentions':self.ms}],'annotation':{'status':'in_progress','human_reviewed':False}}
  e={'work_id':'w-synthetic','book_id':'b-synthetic','source_id':self.sid,'chapter_id':self.cid,'paragraph_id':self.par,'person_mention_id':rec['id'],'quote':text};self.e=e
  def a(s):
   i=text.index(s);return{'paragraph_id':self.par,'start':i,'end':i+len(s),'surface':s}
  rc=a('因厚撫慰甲');gift=a('贈南豫州刺史');scope={'paragraph_id':self.par,'start':rc['start'],'end':gift['end'],'surface':text[rc['start']:gift['end']]}
  b={'kind':'explicit_recipient_joint_resistance_gift','source_term':text,'paragraph_sha256':hashlib.sha256(text.encode()).hexdigest(),'recipient_person_mention_id':rec['id'],'ally_person_mention_id':ally['id'],'opponent_person_mention_ids':[opp['id'],resume['id']],'scope_anchor':scope,'recipient_clause_anchor':rc,'command_anchor':a('令與乙等共拒敵丙'),'opponent_resolution_anchor':a('丙平'),'career_anchor':a('遷使持節、安北將軍、合州刺史'),'death_event_id':'d-synthetic','death_anchor':a('天嘉六年卒'),'age_anchor':a('時年四十八')if age else None,'gift_anchor':gift,'evidence':[copy.deepcopy(e)]}
  self.h={'id':'h-synthetic','person_id':self.persons[0],'title':'南豫州刺史','kind':'office','mode':'posthumous_grant','status':'source_attested','evidence':[copy.deepcopy(e)],'posthumous_basis':b,'attestations':[{'id':'a-synthetic','paragraph_id':self.par,'person_mention_id':rec['id'],'surface':'南豫州刺史','start':gift['start']+1,'end':gift['end'],'usage':'posthumous_usage'}],'effective_period':{'start':{'status':'source_event','event_type':'posthumous_grant','date_expression':None,'evidence':[copy.deepcopy(e)]},'end':{'status':'unknown','date_expression':None,'evidence':[]}}}
  self.event={'id':'d-synthetic','event_type':'death','person_id':self.persons[0],'status':'source_attested','source_term':'卒','date_expression':'天嘉六年','evidence':[copy.deepcopy(e)],'interpretation_note':'合成測試資料，不是史實。','reviewer':'unit test','human_reviewed':False}
  people=[]
  for pid in self.persons:
   mm=[m for m in self.ms if m['person_id']==pid];people.append({'id':pid,'record_type':'historical_person','label':mm[0]['surface'],'aliases':[{'surface':m['surface'],'mention_ids':[m['id']]}for m in mm],'evidence':[{'work_id':'w-synthetic','book_id':'b-synthetic','source_id':self.sid,'chapter_id':self.cid,'paragraph_id':self.par,'mention_id':m['id'],'quote':m['surface']}for m in mm]})
  self.registry={'next_number':1,'persons':people};self.write('registry/persons.json',self.registry);self.write('registry/works.json',{'works':[{'id':'w-synthetic','title':'測試','books':[{'id':'b-synthetic','work_id':'w-synthetic','title':'卷一','chapter_ids':[self.cid]}]}]});self.write('corpus/progress.json',{'active_work_id':'w-synthetic','books':[{'book_id':'b-synthetic','chapter_id':self.cid,'person_status':'in_progress','complete':False}]});self.save()
 def save(self):
  self.write('corpus/synthetic/source.json',self.chapter);(self.root/'corpus/synthetic/source.xml').write_text(render(self.chapter));self.write('corpus/synthetic/source-titles.json',{'record_type':'title_holding_assertion_set','chapter_id':self.cid,'holdings':[self.h]});self.write('corpus/synthetic/source-life-events.json',{'record_type':'person_life_event_assertion_set','chapter_id':self.cid,'events':[self.event]})
 def errors(self):self.save();return validate(self.root)
 def rejected(self):self.assertIn('追尊授號缺少相符原詞與起點證據',self.errors())
 def test_01_normal_full_quote_with_people_before_after_scope(self):self.assertEqual(self.errors(),[]);self.assertLess(self.ms[0]['start'],self.h['posthumous_basis']['scope_anchor']['start']);self.assertGreater(self.ms[-1]['start'],self.h['posthumous_basis']['scope_anchor']['end'])
 def test_02_optional_age_absent(self):self.make(age=False);self.assertEqual(self.errors(),[])
 def test_03_wrong_recipient_opponent(self):self.h['person_id']=self.persons[2];self.rejected()
 def test_04_wrong_recipient_ally(self):self.h['person_id']=self.persons[1];self.rejected()
 def test_05_second_opponent_same_surface_different_person(self):self.ms[4]['person_id']=self.persons[1];self.rejected()
 def test_06_foreign_mid(self):self.h['posthumous_basis']['recipient_person_mention_id']='foreign:p:m';self.rejected()
 def test_07_uncovered_extra_other_person_in_scope(self):
  m=copy.deepcopy(self.ms[0]);i=self.text.index('安北');m.update(id=self.par+':extra',start=i,end=i+2,surface='安北');self.ms.append(m);self.ms.sort(key=lambda x:x['start']);self.rejected()
 def test_08_scope_cannot_start_after_recipient_clause(self):self.h['posthumous_basis']['scope_anchor']=copy.deepcopy(self.h['posthumous_basis']['command_anchor']);self.rejected()
 def test_09_full_quote_not_scope_only(self):self.h['posthumous_basis']['source_term']=self.h['posthumous_basis']['scope_anchor']['surface'];self.rejected()
 def test_10_unclosed_quote_before_scope(self):self.make(prefix='「先有戊事。');self.rejected()
 def test_11_closed_earlier_quote_allowed(self):self.make(prefix='「先有戊事。」先是。');self.assertEqual(self.errors(),[])
 def test_12_wrong_death_person(self):self.event['person_id']=self.persons[2];self.rejected()
 def test_13_wrong_death_event_type(self):self.event['event_type']='birth';self.rejected()
 def test_14_death_evidence_not_same_recipient_mid(self):self.event['evidence'][0]['person_mention_id']=self.ms[3]['id'];self.rejected()
 def test_15_wrong_order(self):self.h['posthumous_basis']['death_anchor']=copy.deepcopy(self.h['posthumous_basis']['gift_anchor']);self.rejected()
 def test_16_wrong_gift_title(self):self.h['title']='安北將軍';self.rejected()
 def test_17_grant_mode_cannot_replace_posthumous(self):self.h['mode']='grant';self.h['effective_period']['start']['event_type']='grant';self.rejected()
 def test_18_attestation_cannot_replace_posthumous(self):self.h['mode']='attestation';self.h['effective_period']['start']={'status':'unknown','date_expression':None,'evidence':[]};self.rejected()
 def test_19_wrong_source(self):self.h['posthumous_basis']['evidence'][0]['source_id']='foreign-source';self.rejected()
 def test_20_source_layer_declaration_not_enough(self):self.h['posthumous_basis']['command_anchor']['surface']='令與乙同往';self.rejected()
 def test_21_received_layer_required(self):self.chapter['paragraphs'][0].pop('text_layer');self.rejected()
 def test_22_normal_metadata_and_alias_order_additions(self):
  self.registry['persons'][2]['aliases'].reverse();self.registry['persons'][0]['extra_review_metadata']={'human_reviewed':False};self.write('registry/persons.json',self.registry);self.chapter['paragraphs'][0]['extra_metadata']={'keep':1};self.h['extra_metadata']=['independent'];self.event['extra_metadata']='independent';self.assertEqual(self.errors(),[])
 def test_23_boolean_offset_not_integer(self):self.h['posthumous_basis']['scope_anchor']['start']=True;self.rejected()
 def test_24_unknown_kind_does_not_fall_through_as_valid(self):self.h['posthumous_basis']['kind']='unknown_joint_story';self.rejected()
if __name__=='__main__':unittest.main(verbosity=2)
