import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts.family_assemblies import load_assemblies
from scripts.ancestry_chain import consecutive_ancestor_parent_valid
BASIS='punctuated_biography_explicit_paternal_zu_fu_pair'
class PaternalPairTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.ids=['abc_def_123_AB','abc_def_123_A','abc_def_123'];t='荀朗字深明，潁川潁陰人也。祖延祖，梁潁川太守，父伯道，衛尉卿。'
  ms=[]
  for mid,s,pid in zip(['h','g','f'],['荀朗','延祖','伯道'],[self.ids[0],self.ids[2],self.ids[1]]):
   start=t.index(s);ms.append(dict(id=mid,kind='person',person_id=pid,start=start,end=start+len(s),surface=s,status='resolved'))
  self.chapter=dict(id='c-test',record_type='marked_chapter',work_id='w-test',book_id='b-test',source_id='s-test',source=dict(url='https://example.org/current',revision_id='reported-123',observation_kind='current_rendered_observation',fixed_body_obtained=False,raw_capture_obtained=False,image_verified=False,human_reviewed=False),paragraphs=[dict(id='p1',text=t,text_layer='received_chapter',mentions=ms)])
  self.aa={}
  for aid,pred,mid,term,pid in [('af','father','f','父伯道',self.ids[1]),('ag','grandfather','g','祖延祖',self.ids[2])]:
   self.aa[aid]=dict(id=aid,predicate=pred,subject_person_id=self.ids[0],object_person_id=pid,status='source_attested',human_reviewed=False,qualifiers=dict(lineage='paternal',source_term=term),evidence=[dict(chapter_id='c-test',paragraph_id='p1',work_id='w-test',book_id='b-test',source_id='s-test',quote=t,subject_person_mention_id='h',object_person_mention_id=mid)])
  self.people={}
  for m in ms:self.people[m['person_id']]=dict(id=m['person_id'],aliases=[dict(surface=m['surface'],mention_ids=[m['id']])],evidence=[dict(mention_id=m['id'],chapter_id='c-test',paragraph_id='p1',quote=m['surface'])])
  self.rows={pid:dict(person_id=pid,source_person_ids=[pid],representative_source_person_id=pid,identity_equivalence_decision_ids=[],parent_person_id=None,source_assertion_id=None)for pid in self.ids}
  self.rows[self.ids[0]].update(parent_person_id=self.ids[1],source_assertion_id='af')
  self.member=self.rows[self.ids[1]];self.member['parent_person_id']=self.ids[2]
  self.conn=dict(type='parent_between_consecutive_ancestors',interpretation_basis=BASIS,status='contextual_provisional',human_reviewed=False,rationale='同段明祖與明父，僅編輯推得父之父。',chain_subject_person_id=self.ids[0],nearer_ancestor_assertion_id='af',farther_ancestor_assertion_id='ag',references=[dict(assertion_id=a,chapter_id='c-test',paragraph_id='p1',work_id='w-test',book_id='b-test',source_id='s-test',quote=t,scope='完整父祖句',url='https://example.org/current')for a in ('af','ag')])
  self.member['parent_connection']=self.conn
  self.obs=dict(kind='current_rendered_observation',fixed_body_obtained=False,raw_capture_obtained=False,image_checked=False,human_reviewed=False,work_id='w-test',book_id='b-test',source_id='s-test',reported_revision='reported-123',url='https://example.org/current',paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),observed_text=t,character_map=list(range(len(t))))
  self.frame=dict(chapter_path='corpus/test/chapter.json',assertions_path='corpus/test/assertions.json',observation_path='source-evidence/test/observation.json',observation_sha256='',chapter_id='c-test',paragraph_id='p1',head_mention_id='h',grandfather_mention_id='g',father_mention_id='f');self.conn['paternal_pair_frame']=self.frame
  self.write()
 def save(self,p,x):
  p=self.root/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False))
 def write(self):
  self.save(self.frame['observation_path'],self.obs);self.frame['observation_sha256']=hashlib.sha256((self.root/self.frame['observation_path']).read_bytes()).hexdigest()
  self.save(self.frame['chapter_path'],self.chapter);self.save(self.frame['assertions_path'],dict(record_type='person_assertion_set',assertions=list(self.aa.values())));self.save('registry/persons.json',dict(persons=list(self.people.values())))
  self.save('registry/family-assemblies.json',dict(assemblies=[dict(id='family-test',root_person_id=self.ids[2],status='contextual_provisional',human_reviewed=False,members=list(self.rows.values()))]))
 def valid(self):return consecutive_ancestor_parent_valid(self.member,self.rows,self.aa,{'c-test':self.chapter},self.root,people=self.people)
 def test_normal_load_assemblies_retains_inference_fields(self):
  sources,rows=load_assemblies(self.root,(self.people,[self.chapter,dict(record_type='person_assertion_set',assertions=list(self.aa.values()))]));self.assertEqual(len(rows),3);self.assertEqual(sources[self.ids[1]]['parent_person_id'],self.ids[2]);self.assertEqual(rows[self.ids[1]]['parent_connection']['status'],'contextual_provisional');self.assertIsNone(rows[self.ids[1]]['source_assertion_id'])
 def test_positive(self):self.assertTrue(self.valid())
 def test_metadata_addition(self):
  self.people[self.ids[1]]['future_unknown']={'evidence':['later']};self.people[self.ids[1]]['evidence'].append(dict(mention_id='later'));self.write();self.assertTrue(self.valid())
 def test_coherent_typed_rekey(self):
  old=self.ids[1];new='abc_def_123_C';self.people[new]=self.people.pop(old);self.people[new]['id']=new;self.member['person_id']=new;self.member['source_person_ids']=[new];self.member['representative_source_person_id']=new;self.rows[new]=self.rows.pop(old);self.rows[self.ids[0]]['parent_person_id']=new;self.aa['af']['object_person_id']=new;self.chapter['paragraphs'][0]['mentions'][2]['person_id']=new;self.ids[1]=new;self.write();self.assertTrue(self.valid())
 def test_conflicting_grandfather(self):
  self.aa['other']=dict(id='other',predicate='grandfather',subject_person_id=self.ids[0],object_person_id=self.ids[1]);self.write();self.assertFalse(self.valid())
 def test_missing_physical_reverse_with_intact_caller(self):
  saved=copy.deepcopy(self.people);self.people[self.ids[1]]['evidence']=[];self.write();self.people=saved;self.assertFalse(self.valid())
 def test_missing_caller_reverse_with_intact_physical(self):
  self.people[self.ids[1]]['evidence']=[];self.assertFalse(self.valid())
 def test_physical_claim_omitted_by_caller(self):
  self.aa['extra']=dict(id='extra',predicate='father',subject_person_id=self.ids[1],object_person_id=self.ids[0]);self.write();self.aa.pop('extra');self.assertFalse(self.valid())
 def test_extra_uncovered_person(self):
  self.chapter['paragraphs'][0]['mentions'].append(dict(id='other',kind='person',person_id=self.ids[0],start=2,end=3,surface='字'));self.write();self.assertFalse(self.valid())
 def test_other_child(self):
  self.aa['ag']['subject_person_id']=self.ids[1];self.write();self.assertFalse(self.valid())
 def test_mother_as_head_is_not_subject(self):
  self.rewrite_text(self.chapter['paragraphs'][0]['text'].replace('荀朗字深明','荀朗母'));self.assertFalse(self.valid())
 def test_source_image_qualification_mismatch(self):
  self.chapter['source']['image_verified']=True;self.write();self.assertFalse(self.valid())
 def test_source_human_qualification_mismatch(self):
  self.chapter['source']['human_reviewed']=True;self.write();self.assertFalse(self.valid())
 def test_literal_evidence_work_book_mismatch(self):
  for a in self.aa.values():a['evidence'][0].update(work_id='other-work',book_id='other-book')
  self.write();self.assertFalse(self.valid())
 def test_reference_work_mismatch(self):
  self.conn['references'][0]['work_id']='other';self.write();self.assertFalse(self.valid())
 def test_courtesy_with_zi_character(self):
  self.rewrite_text(self.chapter['paragraphs'][0]['text'].replace('字深明','字子深'));self.assertTrue(self.valid())
 def test_missing_courtesy_valid(self):
  self.rewrite_text(self.chapter['paragraphs'][0]['text'].replace('字深明',''));self.assertTrue(self.valid())
 def test_dialogue_head_refused(self):
  self.rewrite_text(self.chapter['paragraphs'][0]['text'].replace('字深明','曰深明'));self.assertFalse(self.valid())
 def test_maternal_head_refused(self):
  self.rewrite_text(self.chapter['paragraphs'][0]['text'].replace('字深明','母字深明'));self.assertFalse(self.valid())
 def test_source_bool_integer_not_equal(self):
  self.chapter['source']['fixed_body_obtained']=0;self.assertFalse(self.valid())
 def test_assertion_bool_integer_not_equal(self):
  self.aa['af']['human_reviewed']=0;self.assertFalse(self.valid())
 def test_revision_bool_integer_not_equal(self):
  self.chapter['source']['revision_id']=1;self.obs['reported_revision']=True;self.write();self.assertFalse(self.valid())
 def test_fragmented_callout_cannot_be_joined(self):
  t=self.chapter['paragraphs'][0]['text'];self.obs['observed_text']='['+t[:2]+'1'+t[2:]+']';self.obs['character_map']=[i+1 if i<2 else i+2 for i in range(len(t))];self.write();self.assertFalse(self.valid())
 def test_separate_complete_callouts_and_indent(self):
  t=self.chapter['paragraphs'][0]['text'];self.obs['observed_text']='  [1]'+t[:2]+'[23]'+t[2:]+'[4]  ';self.obs['character_map']=[i+5 if i<2 else i+9 for i in range(len(t))];self.write();self.assertTrue(self.valid())
 def test_split_callout_with_whitespace_runs_refused(self):
  t=self.chapter['paragraphs'][0]['text'];self.obs['observed_text']='  ['+t[:2]+'12] '+t[2:];self.obs['character_map']=[i+3 if i<2 else i+7 for i in range(len(t))];self.write();self.assertFalse(self.valid())
 def test_missing_reverse(self):self.people[self.ids[1]]['evidence']=[];self.write();self.assertFalse(self.valid())
 def test_missing_alias(self):self.people[self.ids[1]]['aliases']=[];self.write();self.assertFalse(self.valid())
 def test_single_endpoint_theft(self):self.aa['af']['object_person_id']=self.ids[2];self.write();self.assertFalse(self.valid())
 def test_wrong_current_marker(self):self.chapter['paragraphs'][0]['mentions'][2]['person_id']=self.ids[2];self.write();self.assertFalse(self.valid())
 def test_maternal(self):self.aa['ag']['qualifiers']['lineage']='maternal';self.write();self.assertFalse(self.valid())
 def test_adoption(self):self.aa['af']['qualifiers']['adopted']=True;self.write();self.assertFalse(self.valid())
 def test_unresolved(self):self.chapter['paragraphs'][0]['mentions'][1]['status']='unresolved';self.write();self.assertFalse(self.valid())
 def test_conflicting_father(self):self.aa['other']=dict(id='other',predicate='father',subject_person_id=self.ids[1],object_person_id=self.ids[0]);self.write();self.assertFalse(self.valid())
 def test_fixed_capture_claim_refused(self):self.obs['fixed_body_obtained']=True;self.write();self.assertFalse(self.valid())
 def test_new_relative_field(self):self.aa['ag']['qualifiers']['adoptive_lineage']='unknown';self.write();self.assertFalse(self.valid())
 def test_caller_chapter_changed(self):self.chapter['source']['url']='https://other.example';self.assertFalse(self.valid())
 def rewrite_text(self,t):
  self.chapter['paragraphs'][0]['text']=t
  for m in self.chapter['paragraphs'][0]['mentions']:
   m['start']=t.index(m['surface']);m['end']=m['start']+len(m['surface'])
  for a in self.aa.values():a['evidence'][0]['quote']=t
  for r in self.conn['references']:r['quote']=t
  self.obs.update(observed_text=t,character_map=list(range(len(t))),paragraph_sha256=hashlib.sha256(t.encode()).hexdigest());self.write()
 def test_dialogue_negative_and_maternal_words(self):
  for replacement in ('外祖','非祖','或祖','曰祖'):
   with self.subTest(replacement=replacement):
    self.rewrite_text(self.chapter['paragraphs'][0]['text'].replace('。祖','。'+replacement,1));self.assertFalse(self.valid())
    self.setUp()
 def test_deleted_chinese_cannot_be_callout(self):
  self.obs['observed_text']='外'+self.obs['observed_text'];self.obs['character_map']=[i+1 for i in self.obs['character_map']];self.write();self.assertFalse(self.valid())
 def test_numeric_callout_projection(self):
  self.obs['observed_text']='[1]'+self.obs['observed_text'];self.obs['character_map']=[i+3 for i in self.obs['character_map']];self.write();self.assertTrue(self.valid())
if __name__=='__main__':unittest.main()
