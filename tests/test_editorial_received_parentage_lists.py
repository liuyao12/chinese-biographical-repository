import unittest,tempfile,pathlib,json,hashlib,copy,sys,importlib.util
T=pathlib.Path(__file__).resolve().parents[1]
from scripts import biographical_kinship as module
H=lambda s:hashlib.sha256(s.encode()).hexdigest()
def put(root,rel,x):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False))
def fixture(root):
 texts=['甲字乙，晚年薨。','所著文集十卷，行於世。','薨後，長子丙嗣爵。次子丁居家。'];pids=['aaa_bbb_ccc','ddd_eee_fff','ggg_hhh_iii']; ps=[];rows=[]
 for i,(txt,line)in enumerate(zip(texts,[152,154,155])):
  ps.append({'id':f'c:p{i}','text':txt,'text_sha256':H(txt),'text_layer':'received_chapter','source_position':{'first_line':line,'last_line':line,'revision_id':7,'editorial_excerpt_boundary':True},'mentions':[]})
 for ix,surf,pid,mid in [(0,'甲',pids[0],'parent'),(2,'丙',pids[1],'child'),(2,'丁',pids[2],'second')]:
  txt=ps[ix]['text'];pos=txt.index(surf);m={'id':mid,'kind':'person','person_id':pid,'start':pos,'end':pos+1,'surface':surf};ps[ix]['mentions'].append(m)
  e={'work_id':'w','book_id':'b','chapter_id':'c','source_id':'s','paragraph_id':ps[ix]['id'],'mention_id':mid,'quote':surf}
  rows.append({'id':pid,'aliases':[{'surface':surf,'mention_ids':[mid]}],'evidence':[e]})
 source={'url':'https://example.org/received','revision_id':7,'edition':'未核印本','actual_print_edition':None,'image_verified':False,'fixed_body_obtained':False,'raw_capture_obtained':False,'normalization':{'verified_blank_line_gaps':[{'source_lines':[153,153],'raw_quote':'　','raw_quote_sha256':H('　'),'revision_id':7}]}}
 ch={'record_type':'marked_chapter','id':'c','work_id':'w','book_id':'b','source_id':'s','source':source,'paragraphs':ps};cap={'url':source['url'],'reported_revision':7,'actual_print_edition':None,'fixed_body_obtained':False,'raw_capture_obtained':False,'units':[{'text':p['text'],'map':list(range(len(p['text']))),'line':p['source_position']['first_line']}for p in ps]}
 put(root,'corpus/test/ch.json',ch);put(root,'source-evidence/test/received.json',cap);put(root,'registry/persons.json',{'persons':rows});put(root,'registry/works.json',{'works':[{'id':'w','books':[{'id':'b','chapter_ids':['c']}]}]});put(root,'registry/work-provenance.json',{'text_bases':{'s':{'source_id':'s','work_id':'w'}}})
 frames=[]
 for i,p in enumerate(ps):
  frames.append({'native_path':'corpus/test/ch.json','chapter_id':'c','paragraph_id':p['id'],'paragraph_sha256':H(p['text']),'source_metadata':copy.deepcopy(source),'capture_path':'source-evidence/test/received.json','capture_sha256':hashlib.sha256((root/'source-evidence/test/received.json').read_bytes()).hexdigest(),'capture_text_pointer':f'/units/{i}/text','capture_map_pointer':f'/units/{i}/map','character_positions':list(range(len(p['text']))),'capture_qualification':{'kind':'existing_received_observation','captured_leaves':{k:cap[k]for k in[]},'no_image_verification':True}})
  frames[-1]['capture_qualification']['captured_leaves']={'/url':cap['url'],'/reported_revision':7,'/actual_print_edition':None,'/fixed_body_obtained':False,'/raw_capture_obtained':False}
 child=ps[2]['mentions'][0];start=child['start']-2
 a={'id':'assertion-opaque','predicate':'father','subject_person_id':pids[1],'object_person_id':pids[0],'status':'source_attested','human_reviewed':False,'qualifiers':{'source_term':'長子','lineage':'paternal'},'context':{'kind':'biographical_child_continuation','paragraph_ids':[p['id']for p in ps],'parent_mention_id':'parent','child_mention_id':'child','status':'contextual_provisional','human_reviewed':False,'rationale':'離線編者由完整連續正文判父系主語，非schema自動同指。','source_continuity':{'kind':'editorial_received_subject_parentage','frames':frames,'parentage_clause':{'paragraph_id':'c:p2','start':start,'end':child['end'],'surface':'長子丙'},'source_positions':[{'paragraph_id':p['id'],'first_line_pointer':f'/units/{i}/line','last_line_pointer':f'/units/{i}/line'}for i,p in enumerate(ps)]}},'evidence':[{'work_id':'w','book_id':'b','chapter_id':'c','source_id':'s','paragraph_id':p['id'],'quote':p['text']}for p in ps]}
 return a,ch

def list_fixture(root):
 a,ch=fixture(root);p=ch['paragraphs'][-1];text='薨後，長子上將軍甲侯丙封甲郡王，次子乙侯丁封乙郡王，丙侯戊封丙郡王，己封丁郡王，庚封戊郡王，各二千戶。';p['text']=text;p['text_sha256']=H(text);p['mentions']=[]
 names=['甲侯丙','乙侯丁','丙侯戊','己','庚'];ids=['ddd_eee_fff','ggg_hhh_iii','jjj_kkk_lll','mmm_nnn_ooo','ppp_qqq_rrr'];members=[];people=json.loads((root/'registry/persons.json').read_text())['persons'][:1]
 for i,(name,pid)in enumerate(zip(names,ids)):
  start=text.index(name);mid='member'+str(i);m={'id':mid,'kind':'person','person_id':pid,'surface':name,'start':start,'end':start+len(name)};p['mentions'].append(m);e={'work_id':'w','book_id':'b','chapter_id':'c','source_id':'s','paragraph_id':p['id'],'mention_id':mid,'quote':name};people.append({'id':pid,'aliases':[{'surface':name,'mention_ids':[mid]}],'evidence':[e]})
  term={'paragraph_id':p['id'],'start':3 if i==0 else text.index('次子'),'end':5 if i==0 else text.index('次子')+2,'surface':'長子'if i==0 else'次子'}if i<2 else None
  gap={'paragraph_id':p['id'],'start':5,'end':start,'surface':text[5:start]}if i==0 else None
  members.append({'child_mention_id':mid,'kinship_term_anchor':term,'intervening_office_anchor':gap})
 put(root,'corpus/test/ch.json',ch);put(root,'registry/persons.json',{'persons':people});cap=json.loads((root/'source-evidence/test/received.json').read_text());cap['units'][2]['text']=text;cap['units'][2]['map']=list(range(len(text)));put(root,'source-evidence/test/received.json',cap)
 for i,f in enumerate(a['context']['source_continuity']['frames']):
  f['capture_sha256']=hashlib.sha256((root/'source-evidence/test/received.json').read_bytes()).hexdigest()
  if i==2:f['paragraph_sha256']=H(text);f['character_positions']=list(range(len(text)))
 a['evidence'][-1]['quote']=text;b=a['context']['source_continuity'];del b['parentage_clause'];b['parentage_list']={'kind':'editorial_source_named_children_list','scope_anchor':{'paragraph_id':p['id'],'start':0,'end':len(text),'surface':text},'members':members};a['context']['child_mention_id']='member0';a['qualifiers']['source_term']='長子'
 return a,ch
class ListTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name);self.a,self.c=list_fixture(self.root)
 def tearDown(self):self.tmp.cleanup()
 def check(self):return module.child_continuation_errors(self.a,self.c,self.root)
 def select(self,i):
  member=self.a['context']['source_continuity']['parentage_list']['members'][i];self.a['context']['child_mention_id']=member['child_mention_id'];self.a['subject_person_id']=self.c['paragraphs'][-1]['mentions'][i]['person_id'];term=member['kinship_term_anchor'];self.a['qualifiers']['source_term']=term['surface']if term else self.c['paragraphs'][-1]['text']
 def test_all_five_source_list_roles(self):
  for i in range(5):self.select(i);self.assertEqual(self.check(),[])
 def test_wrong_parent(self):self.a['object_person_id']='wrong';self.assertTrue(self.check())
 def test_wrong_child(self):self.a['subject_person_id']='wrong';self.assertTrue(self.check())
 def test_no_fake_child_term_for_implicit(self):self.select(3);self.a['qualifiers']['source_term']='子';self.assertTrue(self.check())
 def test_no_implicit_ordinal(self):self.select(3);self.a['qualifiers']['birth_order']={'ordinal':4};self.assertTrue(self.check())
 def test_office_gap_cannot_be_deleted(self):self.a['context']['source_continuity']['parentage_list']['members'][0]['intervening_office_anchor']=None;self.assertTrue(self.check())
 def test_child_marker_not_expanded_to_office(self):self.c['paragraphs'][-1]['mentions'][0]['start']=5;self.assertTrue(self.check())
 def test_unaccounted_person_in_list(self):
  self.a['context']['source_continuity']['parentage_list']['members'].pop();self.assertTrue(self.check())
 def test_changed_member_order(self):
  m=self.a['context']['source_continuity']['parentage_list']['members'];m[2],m[3]=m[3],m[2];self.assertTrue(self.check())
 def test_duplicate_child_rejected(self):
  m=self.a['context']['source_continuity']['parentage_list']['members'];m[2]['child_mention_id']=m[1]['child_mention_id'];self.assertTrue(self.check())
 def test_scope_changed(self):self.a['context']['source_continuity']['parentage_list']['scope_anchor']['end']-=1;self.assertTrue(self.check())
 def test_missing_intervening_paragraph(self):self.a['context']['paragraph_ids'].pop(1);self.a['evidence'].pop(1);self.assertTrue(self.check())
 def test_source_qualification_change(self):self.c['source']['image_verified']=True;self.assertTrue(self.check())
 def test_missing_current_reverse(self):
  r=json.loads((self.root/'registry/persons.json').read_text());r['persons'][4]['evidence']=[];put(self.root,'registry/persons.json',r);self.assertTrue(self.check())
if __name__=='__main__':unittest.main(verbosity=2)
