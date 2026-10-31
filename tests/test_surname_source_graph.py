"""Finite physical source fixtures, real ordinary assembly owner, no passed-state mock."""
import copy,hashlib,json,marshal,tempfile,unittest
from pathlib import Path
from scripts.surname_source_graph import prepare
from scripts.surname_from_father import validate

class SourceGraphSurname(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
  self.ids={'root':'abc_def_123','yuan':'abc_def_123_A','ping':'abc_def_123_B','an':'abc_def_123_BA'}
  self.text='謝祖子元。元弟平。平子安。';self.cid='c-test';self.par='c-test:p1';self.sid='s-test'
  specs=[('m0',0,2,'root'),('m1',3,4,'yuan'),('m2',5,6,'yuan'),('m3',7,8,'ping'),('m4',9,10,'ping'),('m5',11,12,'an')]
  self.ms=[dict(id=m,start=a,end=b,surface=self.text[a:b],kind='person',person_id=self.ids[role])for m,a,b,role in specs]
  src=dict(url='https://example.test/source',revision_id=None,image_verified=False,edition='實際印本未知',actual_print_edition=None,printed_base_edition=None,fixed_body_obtained=False,raw_capture_obtained=False)
  self.ch=dict(record_type='marked_chapter',id=self.cid,work_id='w-test',book_id='b-test',source_id=self.sid,source=src,paragraphs=[dict(id=self.par,text=self.text,text_layer='received_chapter',mentions=self.ms)])
  self.people={pid:dict(id=pid,aliases=[],evidence=[])for pid in self.ids.values()}
  for m in self.ms:
   r=self.people[m['person_id']];r['evidence'].append(self.reverse(m));aa=next((a for a in r['aliases']if a['surface']==m['surface']),None)
   if aa is None:aa=dict(surface=m['surface'],mention_ids=[]);r['aliases'].append(aa)
   aa['mention_ids'].append(m['id'])
  def assertion(aid,pred,sub,obj,sm,om,term):return dict(id=aid,predicate=pred,subject_person_id=self.ids[sub],object_person_id=self.ids[obj],status='source_attested',human_reviewed=False,qualifiers=dict(source_term=term,**({'lineage':'paternal'}if pred=='father'else{})),evidence=[dict(work_id='w-test',book_id='b-test',source_id=self.sid,chapter_id=self.cid,paragraph_id=self.par,quote=self.text,subject_person_mention_id=sm,object_person_mention_id=om)])
  self.aa=[assertion('a-yuan','father','yuan','root','m1','m0','子元'),assertion('a-brother','brother','ping','yuan','m3','m2','元弟平'),assertion('a-an','father','an','ping','m5','m4','平子安')]
  refs=[dict(assertion_id=a['id'],scope='同父為可撤回編者接合，非新literal父句',url=src['url'],**a['evidence'][0])for a in self.aa[:2]]
  cp=dict(type='shared_father_through_sibling',sibling_person_id=self.ids['yuan'],sibling_assertion_id='a-brother',sibling_father_assertion_id='a-yuan',status='contextual_provisional',human_reviewed=False,rationale='兄弟的同父屬有資格首選',references=refs)
  def member(role,parent,aid=None,conn=None):
   pid=self.ids[role];r=dict(person_id=pid,parent_person_id=self.ids[parent]if parent else None,source_person_ids=[pid],representative_source_person_id=pid,identity_equivalence_decision_ids=[],source_assertion_id=aid)
   if conn:r['parent_connection']=conn
   return r
  self.asm=dict(assemblies=[dict(id='family-test',root_person_id=self.ids['root'],status='contextual_provisional',human_reviewed=False,members=[member('root',None),member('yuan','root','a-yuan'),member('ping','root',conn=cp),member('an','ping','a-an')])])
  capture=dict(text=self.text,positions=list(range(len(self.text))),qualification=dict(url=src['url'],reported_revision_id=None,fixed_body_obtained=False,raw_capture_obtained=False,actual_print_edition=None))
  raw=(json.dumps(capture,ensure_ascii=False)+'\n').encode();self.write('source-evidence/test/received.json',raw)
  self.frame=dict(native_path='corpus/test/001.json',chapter_id=self.cid,paragraph_id=self.par,paragraph_sha256=hashlib.sha256(self.text.encode()).hexdigest(),source_metadata=src,capture_path='source-evidence/test/received.json',capture_sha256=hashlib.sha256(raw).hexdigest(),capture_text_pointer='/text',capture_map_pointer='/positions',character_positions=list(range(len(self.text))),capture_qualification=dict(kind='existing_received_observation',captured_leaves={'/qualification/'+k:v for k,v in capture['qualification'].items()},no_image_verification=True))
  self.name=dict(id='n-ping',person_id=self.ids['ping'],surname='謝',ming='平',chapter_id=self.cid,paragraph_id=self.par,person_mention_id='m3',source_anchor=dict(start=7,end=8,surface='平'),quote=self.text,status='contextual_provisional',human_reviewed=False)
  self.name['surname_basis']=dict(kind='contextual_surname_from_source_bound_kinship_graph',status='contextual_provisional',human_reviewed=False,rationale='離線讀稿選定原姓，父橋保編者資格',frames=[self.frame],seed=dict(kind='literal_surname_with_current_named_person_anchor',name_form='surname_given_name',paragraph_id=self.par,person_mention_id='m0',surname_anchor=dict(start=0,end=1,surface='謝')),target=dict(name_record_id='n-ping',paragraph_id=self.par,person_mention_id='m3',given_name_anchor=dict(start=7,end=8,surface='平')),steps=[dict(kind='validated_editorial_assembly_connection',assembly_id='family-test',member_person_id=self.ids['ping'],parent_connection_type='shared_father_through_sibling',supporting_assertion_ids=['a-yuan','a-brother'],from_person_id=self.ids['root'],to_person_id=self.ids['ping'],traversal='parent_to_child')],assertion_sources=[dict(assertion_id=aid,assertions_path='corpus/test/001-assertions.json')for aid in ['a-yuan','a-brother']])
  self.names=[self.name];self.records=[self.ch,dict(record_type='person_name_component_set',records=self.names),dict(record_type='person_assertion_set',chapter_id=self.cid,assertions=self.aa)];self.save();self.context=self.fresh()
 def reverse(self,m):return dict(work_id='w-test',book_id='b-test',source_id=self.sid,chapter_id=self.cid,paragraph_id=self.par,mention_id=m['id'],quote=m['surface'])
 def write(self,rel,raw):
  p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 def json(self,rel,value):self.write(rel,(json.dumps(value,ensure_ascii=False)+'\n').encode())
 def save(self):
  self.json('registry/persons.json',dict(persons=list(self.people.values())));self.json('registry/family-assemblies.json',self.asm);self.json('registry/works.json',dict(works=[dict(id='w-test',books=[dict(id='b-test',chapter_ids=[self.cid])])]))
  self.json('registry/work-provenance.json',dict(text_bases={self.sid:dict(source_id=self.sid,work_id='w-test')}));self.json('corpus/test/001.json',self.ch);self.json('corpus/test/001-assertions.json',self.records[-1])
 def fresh(self):return prepare(self.root,(self.people,self.records))
 def call(self,context=None):return validate(self.name,self.names,{self.cid:self.ch},self.aa,root=self.root,graph_context=self.context if context is None else context)
 def test_real_normal_assembly_and_source_frames(self):self.call()
 def test_no_state_or_fake_dict_is_not_authority(self):
  for fake in ({},True,'passed'):
   with self.assertRaises(ValueError):self.call(fake)
 def test_state_cannot_be_mutated_or_return_polluted(self):
  with self.assertRaises(AttributeError):self.context._assemblies=b'fake'
  marshal.loads(self.context._assemblies)[1].clear();self.call()
 def test_all_raw_assertions_required_not_filtered(self):
  with self.assertRaises(ValueError):validate(self.name,self.names,{self.cid:self.ch},self.aa[:2],root=self.root,graph_context=self.context)
 def test_missing_reverse_rejected(self):
  self.people[self.ids['root']]['evidence']=[];self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_duplicate_reverse_owner_rejected(self):
  self.people[self.ids['an']]['evidence'].append(copy.deepcopy(self.people[self.ids['root']]['evidence'][0]));self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_capture_change_rejected(self):
  self.write('source-evidence/test/received.json',b'{}')
  with self.assertRaises(ValueError):self.call()
 def test_claimed_edition_rejected_even_self_consistent_frame(self):
  self.ch['source']['edition']='武英殿本';self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_wrong_given_name_span_rejected(self):
  self.name['surname_basis']['target']['given_name_anchor']['surface']='安';self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_title_only_seed_declaration_rejected(self):
  self.name['surname_basis']['seed']['name_form']='title';self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_wrong_literal_surname_rejected(self):
  self.name['surname_basis']['seed']['surname_anchor']['surface']='蕭';self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_shared_father_false_fails_real_assembly_factory(self):
  self.aa[1]['qualifiers']['shared_father']=False;self.save()
  with self.assertRaises(ValueError):self.fresh()
 def test_assembly_source_assertion_not_null_rejected(self):
  self.asm['assemblies'][0]['members'][2]['source_assertion_id']='a-yuan';self.save()
  with self.assertRaises(ValueError):self.fresh()
 def test_unlisted_assembly_support_rejected(self):
  self.name['surname_basis']['steps'][0]['supporting_assertion_ids'].pop();self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_physical_assertion_differs_from_caller_rejected(self):
  physical=copy.deepcopy(self.records[-1]);physical['assertions'][0]['qualifiers']['lineage']='maternal';self.json('corpus/test/001-assertions.json',physical)
  with self.assertRaises(ValueError):self.call()
 def test_caller_mutation_rejected(self):
  self.aa[0]['human_reviewed']=0
  with self.assertRaises(ValueError):self.call()
 def test_source_physical_metadata_differs_from_caller(self):
  ch=copy.deepcopy(self.ch);ch['source']['unknown_metadata']='different';self.json('corpus/test/001.json',ch)
  with self.assertRaises(ValueError):self.call()
 def test_cycle_is_not_a_valid_surname_walk(self):
  step=self.name['surname_basis']['steps'][0];back=copy.deepcopy(step);back.update(from_person_id=self.ids['ping'],to_person_id=self.ids['root'],traversal='child_to_parent');self.name['surname_basis']['steps'].append(back);self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_private_catalog_membership_or_order_mutation_rejected(self):
  self.records.reverse()
  with self.assertRaises(ValueError):self.call()
 def test_multiple_source_and_assembly_steps(self):
  b=self.name['surname_basis'];self.name.update(id='n-an',person_id=self.ids['an'],ming='安',person_mention_id='m5',source_anchor=dict(start=11,end=12,surface='安'));b['target']=dict(name_record_id='n-an',paragraph_id=self.par,person_mention_id='m5',given_name_anchor=dict(start=11,end=12,surface='安'))
  b['steps'].append(dict(kind='validated_source_paternal_relation',assertion_id='a-an',from_person_id=self.ids['ping'],to_person_id=self.ids['an'],traversal='object_to_subject',from_person_mention_id='m4',to_person_mention_id='m5'));b['assertion_sources'].append(dict(assertion_id='a-an',assertions_path='corpus/test/001-assertions.json'));self.save();self.context=self.fresh();self.call()
 def test_maternal_source_qualification_cannot_transport_surname(self):
  self.test_multiple_source_and_assembly_steps();self.aa[2]['qualifiers']['lineage']='maternal';self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()

 def test_real_consecutive_ancestor_assembly_type(self):
  old=len(self.text);self.text+='安祖謝祖。';p=self.ch['paragraphs'][0];p['text']=self.text
  self.ms.extend([dict(id='m6',start=old,end=old+1,surface='安',kind='person',person_id=self.ids['an']),dict(id='m7',start=old+2,end=old+4,surface='謝祖',kind='person',person_id=self.ids['root'])])
  for r in self.people.values():r['aliases']=[];r['evidence']=[]
  for m in self.ms:
   r=self.people[m['person_id']];r['evidence'].append(self.reverse(m));a=next((a for a in r['aliases']if a['surface']==m['surface']),None)
   if a is None:a=dict(surface=m['surface'],mention_ids=[]);r['aliases'].append(a)
   a['mention_ids'].append(m['id'])
  for a in self.aa:a['evidence'][0]['quote']=self.text
  far=dict(id='a-grandfather',predicate='grandfather',subject_person_id=self.ids['an'],object_person_id=self.ids['root'],status='source_attested',human_reviewed=False,qualifiers=dict(lineage='paternal',source_term='安祖謝祖'),evidence=[dict(work_id='w-test',book_id='b-test',source_id=self.sid,chapter_id=self.cid,paragraph_id=self.par,quote=self.text,subject_person_mention_id='m6',object_person_mention_id='m7')]);self.aa.append(far)
  near=self.aa[2];cp=dict(type='parent_between_consecutive_ancestors',chain_subject_person_id=self.ids['an'],nearer_ancestor_assertion_id=near['id'],farther_ancestor_assertion_id=far['id'],status='contextual_provisional',human_reviewed=False,rationale='同一主體父與祖合讀；不造literal父句',references=[dict(assertion_id=a['id'],scope='同一主體明父祖的編者相鄰代橋',url=self.ch['source']['url'],**a['evidence'][0])for a in (near,far)])
  self.asm['assemblies'][0]['members'][2]['parent_connection']=cp;b=self.name['surname_basis'];step=b['steps'][0];step['parent_connection_type']=cp['type'];step['supporting_assertion_ids']=[near['id'],far['id']];b['assertion_sources']=[dict(assertion_id=a['id'],assertions_path='corpus/test/001-assertions.json')for a in (near,far)]
  cap=dict(text=self.text,positions=list(range(len(self.text))),qualification=dict(url=self.ch['source']['url'],reported_revision_id=None,fixed_body_obtained=False,raw_capture_obtained=False,actual_print_edition=None));raw=(json.dumps(cap,ensure_ascii=False)+'\n').encode();self.write(self.frame['capture_path'],raw);self.frame.update(paragraph_sha256=hashlib.sha256(self.text.encode()).hexdigest(),capture_sha256=hashlib.sha256(raw).hexdigest(),character_positions=list(range(len(self.text))));self.name['quote']=self.text;self.save();self.context=self.fresh();self.call()
 def test_unknown_extra_caller_metadata_not_erased(self):
  self.ch['unknown_source_field']=dict(value=0)
  with self.assertRaises(ValueError):self.call()
 def test_integer_false_review_not_accepted_after_fresh_state(self):
  self.aa[0]['human_reviewed']=0;self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_shared_source_conditions_reject_wrong_source(self):
  self.aa[0]['evidence'][0]['source_id']='foreign';self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()
 def test_genuine_raw_file_sha_alias(self):
  raw=self.text.encode();path='source-evidence/test/received.wikitext';self.write(path,raw);self.ch['source'].update(raw_path=path,raw_file_sha256=hashlib.sha256(raw).hexdigest(),revision_id='local-fixed-fixture',fixed_body_obtained=True,raw_capture_obtained=True)
  self.frame.update(capture_path=path,capture_sha256=hashlib.sha256(raw).hexdigest(),capture_text_pointer=None,capture_map_pointer=None,capture_qualification=dict(kind='existing_fixed_raw',revision_id='local-fixed-fixture',image_verified=False));self.save();self.context=self.fresh();self.call()
  self.ch['source']['raw_sha256']='inconsistent';self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()

 def test_existing_observed_named_brother_model_still_uses_same_shared_frames(self):
  text='謝元兄平。';ms=[dict(id='old-m0',start=0,end=2,surface='謝元',kind='person',person_id=self.ids['yuan']),dict(id='old-m1',start=3,end=4,surface='平',kind='person',person_id=self.ids['ping'])];self.ch['paragraphs'][0].update(text=text,mentions=ms)
  people={pid:dict(id=pid,aliases=[],evidence=[])for pid in [self.ids['yuan'],self.ids['ping']]}
  for m in ms:people[m['person_id']]['aliases']=[dict(surface=m['surface'],mention_ids=[m['id']])];people[m['person_id']]['evidence']=[self.reverse(m)]
  self.json('registry/persons.json',dict(persons=list(people.values())));self.json('corpus/test/001.json',self.ch)
  a=dict(id='old-brother',predicate='brother',subject_person_id=self.ids['ping'],object_person_id=self.ids['yuan'],status='source_attested',human_reviewed=False,qualifiers=dict(source_term='謝元兄平'),evidence=[dict(work_id='w-test',book_id='b-test',source_id=self.sid,chapter_id=self.cid,paragraph_id=self.par,quote=text,subject_person_mention_id='old-m1',object_person_mention_id='old-m0')]);self.json('corpus/test/001-assertions.json',dict(record_type='person_assertion_set',chapter_id=self.cid,assertions=[a]))
  cap=dict(text=text,positions=list(range(len(text))),qualification=dict(url=self.ch['source']['url'],reported_revision_id=None,fixed_body_obtained=False,raw_capture_obtained=False,actual_print_edition=None));raw=(json.dumps(cap,ensure_ascii=False)+'\n').encode();self.write(self.frame['capture_path'],raw);f=copy.deepcopy(self.frame);f.update(paragraph_sha256=hashlib.sha256(text.encode()).hexdigest(),capture_sha256=hashlib.sha256(raw).hexdigest(),character_positions=list(range(len(text))))
  name=dict(id='old-name',person_id=self.ids['ping'],surname='謝',ming='平',chapter_id=self.cid,paragraph_id=self.par,person_mention_id='old-m1',source_anchor=dict(paragraph_id=self.par,start=3,end=4,surface='平'),quote=text,status='contextual_provisional',human_reviewed=False)
  name['surname_basis']=dict(kind='contextual_surname_from_observed_named_near_kin',status='contextual_provisional',human_reviewed=False,rationale='舊同段兄弟模型保原契約',frames=[f],seed=dict(kind='literal_full_name',paragraph_id=self.par,person_mention_id='old-m0',surname='謝',ming='元'),edge=dict(assertion_id='old-brother',traversal='named_person_to_brother',clause_anchor=dict(paragraph_id=self.par,start=0,end=4,surface='謝元兄平'),rule='named_brother_clause',seed_role_mid='old-m0',target_role_mid='old-m1',assertions_path='corpus/test/001-assertions.json'))
  validate(name,[name],{self.cid:self.ch},[a],root=self.root)

 def test_standard_adjacent_parent_and_children_are_two_full_frames(self):
  p1=dict(id=self.par,text='謝祖，清慎。',text_layer='received_chapter',mentions=[dict(id='p1-head',start=0,end=2,surface='謝祖',kind='person',person_id=self.ids['root'])])
  p2=dict(id='c-test:p2',text='二子元、平。',text_layer='received_chapter',mentions=[dict(id='p2-yuan',start=2,end=3,surface='元',kind='person',person_id=self.ids['yuan']),dict(id='p2-ping',start=4,end=5,surface='平',kind='person',person_id=self.ids['ping'])]);self.ch['paragraphs']=[p1,p2]
  self.people={pid:dict(id=pid,aliases=[],evidence=[])for pid in [self.ids['root'],self.ids['yuan'],self.ids['ping']]}
  for p in (p1,p2):
   for m in p['mentions']:
    r=self.people[m['person_id']];r['aliases'].append(dict(surface=m['surface'],mention_ids=[m['id']]));e=self.reverse(m);e['paragraph_id']=p['id'];r['evidence'].append(e)
  def a(role,mid):return dict(id='adj-'+role,predicate='father',subject_person_id=self.ids[role],object_person_id=self.ids['root'],status='source_attested',human_reviewed=False,qualifiers=dict(lineage='paternal',source_term='二子元、平'),context=dict(kind='adjacent_paragraphs',paragraph_ids=[p1['id'],p2['id']]),evidence=[dict(work_id='w-test',book_id='b-test',source_id=self.sid,chapter_id=self.cid,paragraph_id=p1['id'],quote=p1['text'],object_person_mention_id='p1-head'),dict(work_id='w-test',book_id='b-test',source_id=self.sid,chapter_id=self.cid,paragraph_id=p2['id'],quote=p2['text'],subject_person_mention_id=mid)])
  self.aa=[a('yuan','p2-yuan'),a('ping','p2-ping')];members=self.asm['assemblies'][0]['members'];self.asm['assemblies'][0]['members']=members[:3];members[1]['source_assertion_id']='adj-yuan';members[2]['source_assertion_id']='adj-ping';members[2].pop('parent_connection')
  b=self.name['surname_basis'];self.name.update(paragraph_id=p2['id'],person_mention_id='p2-ping',source_anchor=dict(start=4,end=5,surface='平'),quote=p2['text']);b['seed'].update(paragraph_id=p1['id'],person_mention_id='p1-head');b['target'].update(paragraph_id=p2['id'],person_mention_id='p2-ping',given_name_anchor=dict(start=4,end=5,surface='平'))
  b['steps']=[dict(kind='validated_source_paternal_relation',assertion_id='adj-ping',from_person_id=self.ids['root'],to_person_id=self.ids['ping'],traversal='object_to_subject',from_person_mention_id='p1-head',to_person_mention_id='p2-ping')];b['assertion_sources']=[dict(assertion_id='adj-ping',assertions_path='corpus/test/001-assertions.json')]
  received=p1['text']+'\n'+p2['text'];positions=[list(range(len(p1['text']))),list(range(len(p1['text'])+1,len(received)))];cap=dict(text=received,maps=positions,qualification=dict(url=self.ch['source']['url'],reported_revision_id=None,fixed_body_obtained=False,raw_capture_obtained=False,actual_print_edition=None));raw=(json.dumps(cap,ensure_ascii=False)+'\n').encode();self.write(self.frame['capture_path'],raw);frames=[]
  for i,p in enumerate((p1,p2)):
   f=copy.deepcopy(self.frame);f.update(paragraph_id=p['id'],paragraph_sha256=hashlib.sha256(p['text'].encode()).hexdigest(),capture_sha256=hashlib.sha256(raw).hexdigest(),capture_map_pointer='/maps/'+str(i),character_positions=positions[i]);frames.append(f)
  b['frames']=frames;self.records=[self.ch,dict(record_type='person_name_component_set',records=self.names),dict(record_type='person_assertion_set',chapter_id=self.cid,assertions=self.aa)];self.save();self.context=self.fresh();self.call()
  self.aa[1]['context']['paragraph_ids'].reverse();self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()

 def test_current_physical_assertion_document_header_required(self):
  doc=copy.deepcopy(self.records[-1]);doc['record_type']='historical_snapshot';self.json('corpus/test/001-assertions.json',doc)
  with self.assertRaises(ValueError):self.call()

 def test_ordinary_editorial_preferred_assembly_keeps_provisional_parent(self):
  self.asm['assemblies'][0]['status']='editorial_preferred';self.save();self.context=self.fresh();self.call()
  row=marshal.loads(self.context._assemblies)[1][self.ids['ping']]
  self.assertEqual(row['status'],'editorial_preferred');self.assertEqual(row['parent_connection']['status'],'contextual_provisional');self.assertIsNone(row['source_assertion_id'])
  self.asm['assemblies'][0]['members'][2]['parent_connection']['status']='source_attested';self.save()
  with self.assertRaises(ValueError):self.fresh()
 def test_ordinary_adjacent_metadata_does_not_authorize_another_endpoint(self):
  self.test_standard_adjacent_parent_and_children_are_two_full_frames()
  self.aa[1]['context']['paragraph_ids'].reverse();self.aa[1]['context'].update(status='contextual_provisional',human_reviewed=False,rationale='前後完整原段，非插入父名',unknown_metadata=dict(value=0))
  self.save();self.context=self.fresh();self.call()
  self.name['surname_basis']['steps'][0]['to_person_id']=self.ids['yuan'];self.save();self.context=self.fresh()
  with self.assertRaises(ValueError):self.call()

if __name__=='__main__':unittest.main(verbosity=2)
