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
class Tests(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name);self.a,self.c=fixture(self.root)
 def tearDown(self):self.temp.cleanup()
 def check(self):return module.child_continuation_errors(self.a,self.c,self.root)
 def test_normal_entry_positive_full_three_paragraphs(self):self.assertEqual(self.check(),[])
 def test_second_son(self):
  m=self.c['paragraphs'][-1]['mentions'][1];self.a['subject_person_id']=m['person_id'];self.a['context']['child_mention_id']=m['id'];self.a['qualifiers']['source_term']='次子';self.a['context']['source_continuity']['parentage_clause']={'paragraph_id':'c:p2','start':m['start']-2,'end':m['end'],'surface':'次子丁'};self.assertEqual(self.check(),[])
 def test_wrong_parent(self):self.a['object_person_id']='ggg_hhh_iii';self.assertTrue(self.check())
 def test_wrong_child(self):self.a['subject_person_id']='ggg_hhh_iii';self.assertTrue(self.check())
 def test_missing_middle(self):self.a['context']['paragraph_ids'].pop(1);self.a['evidence'].pop(1);self.a['context']['source_continuity']['frames'].pop(1);self.a['context']['source_continuity']['source_positions'].pop(1);self.assertTrue(self.check())
 def test_quote_truncated(self):self.a['evidence'][0]['quote']='甲';self.assertTrue(self.check())
 def test_wrong_frame_capture_hash(self):self.a['context']['source_continuity']['frames'][0]['capture_sha256']='0'*64;self.assertTrue(self.check())
 def test_wrong_source_position(self):self.a['context']['source_continuity']['source_positions'][0]['first_line_pointer']='/units/1/line';self.assertTrue(self.check())
 def test_skip_unproved_nonblank_gap(self):
  self.c['source']['normalization']['verified_blank_line_gaps']=[];put(self.root,'corpus/test/ch.json',self.c)
  for f in self.a['context']['source_continuity']['frames']:f['source_metadata']=copy.deepcopy(self.c['source'])
  self.assertTrue(self.check())
 def test_missing_reverse(self):
  x=json.loads((self.root/'registry/persons.json').read_text());x['persons'][0]['evidence']=[];put(self.root,'registry/persons.json',x);self.assertTrue(self.check())
 def test_stolen_reverse(self):
  x=json.loads((self.root/'registry/persons.json').read_text());x['persons'][1]['evidence']+=x['persons'][0]['evidence'];put(self.root,'registry/persons.json',x);self.assertTrue(self.check())
 def test_maternal_not_paternal(self):self.a['qualifiers']['lineage']='maternal';self.assertTrue(self.check())
 def test_parent_and_child_collapse(self):self.a['subject_person_id']=self.a['object_person_id'];self.assertTrue(self.check())
 def test_wrong_term(self):self.a['qualifiers']['source_term']='子';self.assertTrue(self.check())
 def test_provisional_context_not_literal_certification(self):self.a['context']['status']='source_attested';self.assertTrue(self.check())
 def test_source_claim_cannot_invent_fixed_body(self):
  self.c['source']['fixed_body_obtained']=True;put(self.root,'corpus/test/ch.json',self.c)
  for f in self.a['context']['source_continuity']['frames']:f['source_metadata']=copy.deepcopy(self.c['source'])
  self.assertTrue(self.check())
 def test_unknown_metadata_preserved(self):
  self.c['source']['unknown_qualification']={'note':'keep'};put(self.root,'corpus/test/ch.json',self.c)
  for f in self.a['context']['source_continuity']['frames']:f['source_metadata']=copy.deepcopy(self.c['source'])
  before=copy.deepcopy(self.c);self.assertEqual(self.check(),[]);self.assertEqual(before,self.c)
 def test_actual_preexisting_fixture_old_model_unchanged(self):
  spec=importlib.util.spec_from_file_location('existing_biographical_fixture',T/'tests/test_biographical_kinship.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
  a,c=old.fixture();self.assertEqual(module.child_continuation_errors(a,c),old.child_continuation_errors(a,c));self.assertEqual(module.child_continuation_errors(a,c),[])
 def test_other_old_model_entry_unchanged(self):
  self.a['context']['source_continuity']['kind']='not-a-supported-kind';self.assertTrue(self.check())
if __name__=='__main__':unittest.main(verbosity=2)
