import copy,json,pathlib,unittest,tempfile
import received_sima_family_sources as owner
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ReceivedSimaFamilySources(unittest.TestCase):
 def fixture(self):
  raw=lambda p:(ROOT/p).read_bytes()
  people={p['id']:p for p in json.loads(raw('registry/persons.json'))['persons']}
  return raw,people
 def setUp(self):
  self.raw,self.people=self.fixture();self.c=json.loads(self.raw(owner.REF));self.chpath=self.c['chapter_path'];owner._proof(self.raw,self.people)
 def edit(self,path,change):
  v=json.loads(self.raw(path));change(v);b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode();return lambda p:b if p==path else self.raw(p)
 def rejected(self,raw=None,people=None,records=None):
  with self.assertRaises((AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration)):
   owner._proof(raw or self.raw,people or self.people,records)
 def test_current_sources_and_reverse(self):owner._proof(self.raw,self.people)
 def test_normal_courtesy_name_contract(self):
  from person_bundle import validate_courtesy_name
  for name in json.loads(self.raw(self.c['name_path']))['records']:validate_courtesy_name(name,root=ROOT)
 def test_unrelated_root_without_contract_is_noop(self):
  with tempfile.TemporaryDirectory()as d:self.assertEqual(owner.errors(d),[]);owner.guard_bundle(d,'unrelated',{},[])
 def test_installed_source_without_contract_rejected(self):
  with tempfile.TemporaryDirectory()as d:
   p=pathlib.Path(d)/self.chpath;p.parent.mkdir(parents=True);p.write_text('{}');self.assertTrue(owner.errors(d))
   with self.assertRaises(ValueError):owner.guard_bundle(d,'unrelated',{},[])
 def test_human_reviewed_false_is_not_integer_zero(self):
  self.rejected(self.edit(self.c['name_path'],lambda d:d['records'][0].update(human_reviewed=0)))
 def test_start_integer_zero_is_not_boolean_false(self):
  self.rejected(self.edit(self.chpath,lambda d:d['paragraphs'][0]['mentions'][0].update(start=False)))
 def test_single_endpoint(self):
  self.rejected(self.edit(self.chpath,lambda c:c['paragraphs'][0]['mentions'][0].update(person_id='zzz_zzz_zzz')))
 def test_unknown_metadata_not_masked(self):
  self.rejected(self.edit(self.chpath,lambda c:c['source'].update(unreviewed_extra='unexpected')))
 def test_acquisition_qualification_not_weakened(self):
  self.rejected(self.edit(self.chpath,lambda c:c['source'].update(image_verified=True)))
 def test_pronoun_not_name_alias(self):
  ch=json.loads(self.raw(self.chpath));m=next(m for p in ch['paragraphs']for m in p['mentions']if m['kind']=='pronoun');people=copy.deepcopy(self.people);people[m['person_id']]['aliases'].append({'surface':m['surface'],'mention_ids':[m['id']]});self.rejected(people=people)
 def test_missing_reverse(self):
  ch=json.loads(self.raw(self.chpath));m=ch['paragraphs'][0]['mentions'][0];people=copy.deepcopy(self.people);people[m['person_id']]['evidence']=[e for e in people[m['person_id']]['evidence']if e.get('mention_id')!=m['id']];self.rejected(people=people)
 def test_raised_by_not_birthmother(self):
  self.rejected(self.edit(self.c['assertion_path'],lambda d:d['assertions'][-1].update(predicate='mother')))
 def test_caller_side_names_not_hidden(self):
  records=[json.loads(self.raw(p))for p in self.c['expected_documents']];names=next(d for d in records if d.get('record_type')=='person_name_component_set');names['records'][0]['ming']='別名';self.rejected(records=records)
 def test_current_role_can_be_coherently_rekeyed(self):
  _,roles,_=owner._proof(self.raw,self.people);old=roles['yu'];new='zzz_zzz_zzz';people=copy.deepcopy(self.people);self.assertNotIn(new,people);person=people.pop(old);person['id']=new;people[new]=person
  paths=set(self.c['expected_documents'])|{self.c['role_seeds']['yu']['chapter_path']};overlay={}
  def move(v):
   if isinstance(v,dict):return{k:(new if k in ('person_id','subject_person_id','object_person_id','parent_person_id')and x==old else move(x))for k,x in v.items()}
   if isinstance(v,list):return[move(x)for x in v]
   return v
  for p in paths:overlay[p]=(json.dumps(move(json.loads(self.raw(p))),ensure_ascii=False,indent=2)+'\n').encode()
  raw=lambda p:overlay[p]if p in overlay else self.raw(p)
  _,changed,_=owner._proof(raw,people);self.assertEqual(changed['yu'],new)
  # Opaque source identifiers and received bytes survive the legitimate rekey.
  for p,b in overlay.items():
   a=json.loads(self.raw(p));z=json.loads(b)
   if a.get('record_type')=='marked_chapter':self.assertEqual([(q['id'],q['text'],[m['id']for m in q['mentions']])for q in a['paragraphs']],[(q['id'],q['text'],[m['id']for m in q['mentions']])for q in z['paragraphs']])


class ReceivedSimaGuardEntryTests(unittest.TestCase):
 # Caller consistency tests deliberately use the public guard entry. They require
 # its specific ValueError, so a later absent-registry/proof error cannot pass.
 def entry_inputs(self):
  import os
  root=pathlib.Path(os.environ.get('CBR_RECEIVED_SIMA_GUARD_TEST_ROOT',ROOT))
  people_root=pathlib.Path(os.environ.get('CBR_RECEIVED_SIMA_GUARD_PEOPLE_ROOT',ROOT))
  contract=json.loads((root/owner.REF).read_bytes())
  records=[json.loads((root/p).read_bytes())for p in contract['expected_documents']]
  people={p['id']:p for p in json.loads((people_root/'registry/persons.json').read_bytes())['persons']}
  chapter=next(d for d in records if d.get('record_type')=='marked_chapter')
  physical={m['person_id']for p in chapter['paragraphs']for m in p['mentions']if m.get('person_id')}
  wrong=next(pid for pid in people if pid not in physical)
  return root,people,records,chapter,wrong
 def mismatch(self,root,pid,people,records):
  with self.assertRaisesRegex(ValueError,'Received Sima caller/physical catalogue mismatch'):
   owner.guard_bundle(root,pid,people,records)
 def test_guard_caller_only_wrong_live_endpoint_rejected(self):
  root,people,records,ch,wrong=self.entry_inputs();ch['paragraphs'][0]['mentions'][0]['person_id']=wrong;self.mismatch(root,wrong,people,records)
 def test_guard_caller_only_name_owner_rejected(self):
  root,people,records,ch,wrong=self.entry_inputs();names=next(d for d in records if d.get('record_type')=='person_name_component_set');names['records'][0]['person_id']=wrong;self.mismatch(root,wrong,people,records)
 def test_guard_missing_name_sidecar_rejected(self):
  root,people,records,ch,wrong=self.entry_inputs();pid=ch['paragraphs'][0]['mentions'][0]['person_id'];self.mismatch(root,pid,people,[d for d in records if d.get('record_type')!='person_name_component_set'])
 def test_guard_missing_assertion_sidecar_rejected(self):
  root,people,records,ch,wrong=self.entry_inputs();pid=ch['paragraphs'][0]['mentions'][0]['person_id'];self.mismatch(root,pid,people,[d for d in records if d.get('record_type')!='person_assertion_set'])
 def test_guard_changed_chapter_header_cannot_hide_owned_mid(self):
  root,people,records,ch,wrong=self.entry_inputs();ch['id']='c-unrelated-forged';ch['paragraphs'][0]['mentions'][0]['person_id']=wrong;self.mismatch(root,wrong,people,records)
 def test_guard_duplicate_owned_chapter_rejected(self):
  root,people,records,ch,wrong=self.entry_inputs();pid=ch['paragraphs'][0]['mentions'][0]['person_id'];self.mismatch(root,pid,people,records+[copy.deepcopy(ch)])
 def test_guard_added_foreign_sidecar_owner_rejected(self):
  root,people,records,ch,wrong=self.entry_inputs();records.append({'record_type':'person_assertion_set','chapter_id':ch['id'],'assertions':[{'subject_person_id':wrong,'object_person_id':wrong}]});self.mismatch(root,wrong,people,records)
 def test_guard_unrelated_current_actor_unchanged_noop(self):
  root,people,records,ch,wrong=self.entry_inputs();owner.guard_bundle(root,wrong,people,records)

if __name__=='__main__':unittest.main()
