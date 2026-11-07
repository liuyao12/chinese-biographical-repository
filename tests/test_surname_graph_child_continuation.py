import pathlib,json,hashlib,copy,tempfile,unittest
from tests import test_editorial_received_parentage_lists as f
from scripts.surname_source_graph import prepare,validate
class ChildGraphTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=pathlib.Path(self.tmp.name);a,self.ch=f.list_fixture(self.root);p=self.ch['paragraphs'][0];p['text']='蕭'+p['text'];p['mentions'][0].update(surface='蕭甲',end=2);p['text_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.aa=[];self.names=[]
  cap=json.loads((self.root/'source-evidence/test/received.json').read_text());cap['units'][0]['text']=p['text'];cap['units'][0]['map']=list(range(len(p['text'])));f.put(self.root,'source-evidence/test/received.json',cap)
  for frame in a['context']['source_continuity']['frames']:
   frame['capture_sha256']=hashlib.sha256((self.root/frame['capture_path']).read_bytes()).hexdigest()
   if frame['paragraph_id']==p['id']:frame['paragraph_sha256']=p['text_sha256'];frame['character_positions']=list(range(len(p['text'])))
  a['evidence'][0]['quote']=p['text'];self.people={r['id']:r for r in json.loads((self.root/'registry/persons.json').read_text())['persons']};parent=self.people[a['object_person_id']];parent['aliases'][0]['surface']='蕭甲';parent['evidence'][0]['quote']='蕭甲'
  for i,m in enumerate(self.ch['paragraphs'][-1]['mentions']):
   row=copy.deepcopy(a);row['id']='claim-'+str(i);row['subject_person_id']=m['person_id'];row['context']['child_mention_id']=m['id'];member=row['context']['source_continuity']['parentage_list']['members'][i];term=member['kinship_term_anchor'];row['qualifiers']['source_term']=term['surface']if term else self.ch['paragraphs'][-1]['text'];self.aa.append(row)
   n={'id':'name-'+str(i),'person_id':m['person_id'],'surname':'蕭','ming':m['surface'][-1],'chapter_id':'c','paragraph_id':'c:p2','person_mention_id':m['id'],'quote':self.ch['paragraphs'][-1]['text'],'status':'contextual_provisional','human_reviewed':False}
   n['surname_basis']={'kind':'contextual_surname_from_source_bound_kinship_graph','status':'contextual_provisional','human_reviewed':False,'rationale':'Synthetic editorial source graph','frames':copy.deepcopy(row['context']['source_continuity']['frames']),'seed':{'kind':'literal_surname_with_current_named_person_anchor','name_form':'surname_given_name','paragraph_id':'c:p0','person_mention_id':'parent','surname_anchor':{'start':0,'end':1,'surface':'蕭'}},'target':{'name_record_id':n['id'],'paragraph_id':'c:p2','person_mention_id':m['id'],'given_name_anchor':{'start':m['end']-1,'end':m['end'],'surface':n['ming']}},'steps':[{'kind':'validated_source_paternal_relation','assertion_id':row['id'],'from_person_id':a['object_person_id'],'to_person_id':m['person_id'],'traversal':'object_to_subject','from_person_mention_id':'parent','to_person_mention_id':m['id']}],'assertion_sources':[{'assertion_id':row['id'],'assertions_path':'corpus/test/ch-assertions.json'}]};self.names.append(n)
  self.save()
 def save(self):
  f.put(self.root,'registry/persons.json',{'persons':list(self.people.values())});f.put(self.root,'corpus/test/ch.json',self.ch);self.doc={'record_type':'person_assertion_set','chapter_id':'c','assertions':self.aa};f.put(self.root,'corpus/test/ch-assertions.json',self.doc);self.records=[self.ch,self.doc,{'record_type':'person_name_component_set','records':self.names}];self.ctx=prepare(self.root,(self.people,self.records))
 def call(self,i=3):return validate(self.names[i],self.names,{'c':self.ch},self.aa,self.root,self.ctx)
 def test_all_five_real_ordinary_context_factory(self):
  for i in range(5):self.call(i)
 def test_wrong_context_parent(self):self.aa[3]['context']['parent_mention_id']='member0';self.save();self.assertRaises(ValueError,self.call)
 def test_skip_middle(self):
  a=self.aa[3];a['context']['paragraph_ids'].pop(1);a['evidence'].pop(1);a['context']['source_continuity']['frames'].pop(1);a['context']['source_continuity']['source_positions'].pop(1);self.save();self.assertRaises(ValueError,self.call)
 def test_wrong_context_child(self):self.aa[3]['context']['child_mention_id']='member4';self.save();self.assertRaises(ValueError,self.call)
 def test_unvalidated_context_does_not_authorize_any_mid(self):self.names[3]['surname_basis']['steps'][0]['from_person_mention_id']='member0';self.save();self.assertRaises(ValueError,self.call)
 def test_missing_reverse(self):self.people[self.aa[0]['object_person_id']]['evidence']=[];self.save();self.assertRaises(ValueError,self.call)
 def test_foreign_reverse_owner(self):self.people[self.aa[0]['subject_person_id']]['evidence']+=self.people[self.aa[0]['object_person_id']]['evidence'];self.save();self.assertRaises(ValueError,self.call)
 def test_caller_physical_assertion_mismatch(self):
  self.aa[3]['editorial_extra']='caller only';self.records[1]['assertions']=self.aa;self.ctx=prepare(self.root,(self.people,self.records));self.assertRaises(ValueError,self.call)
 def test_child_context_cannot_be_used_for_grandfather(self):self.aa[3]['predicate']='grandfather';self.save();self.assertRaises(ValueError,self.call)
class RegisteredRawFrameTests(unittest.TestCase):
 def setUp(self):
  from tests.test_surname_source_graph import SourceGraphSurname
  self.b=SourceGraphSurname(methodName='test_real_normal_assembly_and_source_frames');self.b.setUp();self.addCleanup(self.b.doCleanups)
  b=self.b;raw=b.text.encode();self.path='sources/test/registered.wikitext';b.write(self.path,raw)
  b.ch['source'].update(raw_path=self.path,raw_file_sha256=hashlib.sha256(raw).hexdigest(),revision_id=7,fixed_body_obtained=True,raw_capture_obtained=True)
  b.frame.update(capture_path=self.path,capture_sha256=hashlib.sha256(raw).hexdigest(),capture_text_pointer=None,capture_map_pointer=None,character_positions=list(range(len(b.text))),source_metadata=copy.deepcopy(b.ch['source']),capture_qualification={'kind':'existing_fixed_raw','revision_id':7,'image_verified':False})
  b.save();b.context=b.fresh()
 def test_exact_registered_raw_allowed(self):self.b.call()
 def test_same_bytes_wrong_path_rejected(self):
  self.b.write('sources/test/unregistered.wikitext',self.b.text.encode());self.b.frame['capture_path']='sources/test/unregistered.wikitext';self.b.save();self.b.context=self.b.fresh();self.assertRaises(ValueError,self.b.call)
 def test_registered_raw_hash_still_required(self):
  self.b.ch['source']['raw_file_sha256']='0'*64;self.b.frame['source_metadata']=copy.deepcopy(self.b.ch['source']);self.b.save();self.b.context=self.b.fresh();self.assertRaises(ValueError,self.b.call)
 def test_observed_qualification_cannot_masquerade_as_raw(self):
  self.b.frame['capture_qualification']['kind']='existing_received_observation';self.b.save();self.b.context=self.b.fresh();self.assertRaises(ValueError,self.b.call)
 def test_sources_json_pointer_not_newly_allowed(self):
  self.b.frame['capture_text_pointer']='/text';self.b.save();self.b.context=self.b.fresh();self.assertRaises(ValueError,self.b.call)
 def test_unobtained_raw_not_newly_allowed(self):
  self.b.ch['source']['raw_capture_obtained']=False;self.b.frame['source_metadata']=copy.deepcopy(self.b.ch['source']);self.b.save();self.b.context=self.b.fresh();self.assertRaises(ValueError,self.b.call)
 def test_same_hash_changed_raw_bytes_rejected(self):
  self.b.write(self.path,self.b.text.encode()+b'x');self.assertRaises(ValueError,self.b.call)
if __name__=='__main__':unittest.main(verbosity=2)
