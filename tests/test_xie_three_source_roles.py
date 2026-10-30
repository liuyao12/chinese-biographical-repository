"""Bounded physical-source unit tests, not a substitute for normal full-native validation."""
import copy,json,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import xie_three_source_roles as owner
ROOT=Path(__file__).resolve().parents[1]

def write(root,path,obj):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def read(root,path):return json.loads((root/path).read_text(encoding='utf-8'))

class XieThreeBoundedSourceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  proof=owner.fixed(ROOT)
  files=list(proof['chapters'])+list(owner.IDENTITIES)+['corpus/songshu/056-xiezhan-assertions.json','source-evidence/nanshi020-xiehongwei-reading/review.json',owner.BASE+'proof.json']
  for rel in files:
   p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p);self.assertNotEqual(p.stat().st_ino,(ROOT/rel).stat().st_ino)
  # Explicitly bounded unit fixture: retain the exact five complete endpoint records, not a fake full-native pass.
  roles,_,people,_=owner.prepared(ROOT);self.roles=roles
  write(self.root,'registry/persons.json',{'persons':list(people.values())})
 def prepared(self):return owner.prepared(self.root)
 def chapter_mutation(self,path,mid,key,value):
  ch=read(self.root,path);owner.marker(ch,mid)[1][key]=value;write(self.root,path,ch)
 def rejection(self):
  with self.assertRaises((ValueError,KeyError,TypeError,StopIteration)):self.prepared()
 def records(self):
  _,chs,_,_=self.prepared();return list(chs.values())+[read(self.root,p)for p in owner.IDENTITIES]+[read(self.root,'corpus/songshu/056-xiezhan-assertions.json')]
 def test_actual_source_roles_and_five_not_parents(self):
  roles,chs,people,t=self.prepared();self.assertEqual(len(set(roles.values())),5);self.assertEqual(t['care']['predicate'],'raised_by');self.assertEqual(t['care']['qualifiers']['legal_adoption_status'],'not_stated');self.assertEqual(len(people[roles['friend']]['evidence']),3);self.assertEqual(len(people[roles['guest']]['evidence']),1)
 def test_care_direction_rejected(self):
  p='corpus/songshu/056-xiezhan-assertions.json';d=read(self.root,p);a=next(a for a in d['assertions']if owner.family_applies(a));a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];write(self.root,p,d);self.rejection()
 def test_mother_not_raised_by(self):
  p='corpus/songshu/056-xiezhan-assertions.json';d=read(self.root,p);next(a for a in d['assertions']if owner.family_applies(a))['predicate']='mother';write(self.root,p,d);self.rejection()
 def test_legal_adoption_not_inferred(self):
  p='corpus/songshu/056-xiezhan-assertions.json';d=read(self.root,p);next(a for a in d['assertions']if owner.family_applies(a))['qualifiers']['legal_adoption_status']='adopted';write(self.root,p,d);self.rejection()
 def test_copy_nurture_to_brother_is_rejected(self):
  p='corpus/songshu/056-xiezhan-assertions.json';d=read(self.root,p);a=copy.deepcopy(next(a for a in d['assertions']if owner.family_applies(a)));a['id']+='-brother';a['subject_person_id']='invalid-brother';d['assertions'].append(a);write(self.root,p,d);self.rejection()
 def test_care_raw_clause_change_rejected(self):
  ch=read(self.root,owner.SS);p,_=owner.marker(ch,'c-songshu-056-xiezhan:p001:m0059');p['text']=p['text'].replace('撫養有恩','撫養無恩');write(self.root,owner.SS,ch);self.rejection()
 def test_wrong_care_seed_span_rejected(self):
  self.chapter_mutation(owner.SS,'c-songshu-056-xiezhan:p001:m0064','start',65);self.rejection()
 def test_friend_three_mids_same_individual(self):
  self.chapter_mutation(owner.NS,owner.FRIEND[1],'person_id',self.roles['guest']);self.rejection()
 def test_guest_cannot_be_chess_friend(self):
  self.chapter_mutation(owner.NS,owner.GUEST,'person_id',self.roles['friend']);self.rejection()
 def test_guest_cannot_be_known_huilin_or_keer(self):
  self.chapter_mutation(owner.NS,owner.GUEST,'person_id',self.roles['child']);self.rejection()
 def test_guest_no_claimed_sex(self):
  d=read(self.root,'registry/persons.json');next(p for p in d['persons']if p['id']==self.roles['guest'])['sex']='male';write(self.root,'registry/persons.json',d);self.rejection()
 def test_anonymous_reverse_source_dimension_required(self):
  d=read(self.root,'registry/persons.json');next(p for p in d['persons']if p['id']==self.roles['friend'])['evidence'][0]['source_id']='wrong';write(self.root,'registry/persons.json',d);self.rejection()
 def test_anonymous_alias_surface_required(self):
  d=read(self.root,'registry/persons.json');next(p for p in d['persons']if p['id']==self.roles['friend'])['aliases'][0]['surface']='慧琳';write(self.root,'registry/persons.json',d);self.rejection()
 def test_shuduan_wrong_target(self):
  self.chapter_mutation(owner.WY,owner.SHUDUAN,'person_id',self.roles['child']);self.rejection()
 def test_shuduan_042_clause_rejected(self):
  ch=read(self.root,owner.ZH);p,_=owner.marker(ch,owner.SEED);p['text']=p['text'].replace('後生少子叔段','後生少子叔叔');write(self.root,owner.ZH,ch);self.rejection()
 def test_shuduan_identity_scope_cannot_shrink(self):
  p='corpus/songshu/044-wyd1739-identities.json';d=read(self.root,p);a=next(a for a in d['decisions']if a['id']=='d-song044-wyd-shuduan-allusion');a.update(scope='same_chapter',chapter_ids=[d['chapter_id']]);write(self.root,p,d);self.rejection()
 def test_record_template_pin_cannot_assert_contemporary_shuduan(self):
  path='corpus/songshu/044-wyd1739-identities.json';d=read(self.root,path);a=next(a for a in d['decisions']if a['id']=='d-song044-wyd-shuduan-allusion');a['source_context']['contemporary_participation']='asserted';write(self.root,path,d)
  proof=read(self.root,owner.BASE+'proof.json');proof['records'][path]['decisions'][0]['source_context']['contemporary_participation']='asserted';write(self.root,owner.BASE+'proof.json',proof)
  import hashlib
  digest=hashlib.sha256((self.root/(owner.BASE+'proof.json')).read_bytes()).hexdigest()
  with patch.object(owner,'PROOF_SHA',digest):self.rejection()
 def test_generic_filename_and_evidence_each_chapter(self):
  for p,ids in owner.IDENTITIES.items():
   self.assertTrue(Path(p).match('*/*-identities.json'));d=read(self.root,p)
   for a in d['decisions']:
    if a['id']not in ids:continue
    ps={p['id']:(c['id'],p)for c in self.prepared()[1].values()for p in c['paragraphs']};seen=set()
    for e in a['evidence']:
     cid,p=ps[e['paragraph_id']];self.assertEqual(e['quote'],p['text']);self.assertTrue(any(m.get('person_id')==a['person_id']for m in p['mentions']));seen.add(cid)
    self.assertEqual(set(a['chapter_ids']),seen)
 def test_shuduan_cannot_be_song_death(self):
  roles,chs,_,_=self.prepared();p,_=owner.marker(chs[owner.WY],owner.SHUDUAN);e={'person_id':roles['shuduan'],'event_type':'death','evidence':[{'paragraph_id':p['id'],'person_mention_id':owner.SHUDUAN,'quote':p['text']}]};self.assertTrue(owner.event_applies(e));self.assertFalse(owner.event_valid(e,self.root))
 def test_scope_no_scope_same_and_unrelated_catalog_unchanged(self):
  from scripts.validation_context import scope
  before=self.prepared()
  with scope(self.root):self.assertEqual(before,self.prepared());owner.guard_bundle(self.root,'unrelated',{},[])
  self.assertEqual(before,self.prepared())
 def test_outside_scope_modified_reverse_is_fresh(self):
  self.prepared();d=read(self.root,'registry/persons.json');next(p for p in d['persons']if p['id']==self.roles['caregiver'])['evidence']=[];write(self.root,'registry/persons.json',d);self.rejection()
 def test_supplied_catalog_must_not_omit_source(self):
  _,chs,people,_=self.prepared();records=[r for r in self.records()if r.get('id')!=chs[owner.WY]['id']]
  with self.assertRaises(ValueError):owner.guard_bundle(self.root,self.roles['shuduan'],people,records)
 def test_supplied_catalog_missing_care_fails(self):
  _,_,people,_=self.prepared();records=[r for r in self.records()if r.get('record_type')!='person_assertion_set']
  with self.assertRaises(ValueError):owner.guard_bundle(self.root,self.roles['child'],people,records)
 def test_100_unrelated_calls_do_not_prepare_or_read_registry(self):
  from scripts.validation_context import scope
  original=owner.read;calls=[]
  def counted(root,path):calls.append(path);return original(root,path)
  with scope(self.root),patch.object(owner,'read',side_effect=counted),patch.object(owner,'prepared',side_effect=AssertionError('unrelated full proof')):
   for i in range(100):owner.guard_bundle(self.root,'unrelated-'+str(i),{},[])
  self.assertEqual(len(calls),5);self.assertNotIn('registry/persons.json',calls)
 def test_legal_consistent_five_endpoint_rekey(self):
  old=copy.deepcopy(self.roles);mapping={pid:('tst_'+str(i).zfill(3)+'_aaa')for i,pid in enumerate(old.values())}
  def replace(v):
   if isinstance(v,str):return mapping.get(v,v)
   if isinstance(v,list):return [replace(x)for x in v]
   if isinstance(v,dict):return {k:replace(x)for k,x in v.items()}
   return v
  for p in self.root.rglob('*.json'):
   if p.relative_to(self.root).as_posix()==owner.BASE+'proof.json':continue
   write(self.root,p.relative_to(self.root),replace(json.loads(p.read_text())))
  roles,_,_,_=self.prepared();self.assertEqual(roles,{k:mapping[v]for k,v in old.items()})
 def test_same_record_template_pin_forgery_still_cannot_make_mother(self):
  proof=read(self.root,owner.BASE+'proof.json');proof['records']['care']['predicate']='mother';write(self.root,owner.BASE+'proof.json',proof)
  p='corpus/songshu/056-xiezhan-assertions.json';d=read(self.root,p);next(a for a in d['assertions']if owner.family_applies(a))['predicate']='mother';write(self.root,p,d)
  import hashlib
  digest=hashlib.sha256((self.root/(owner.BASE+'proof.json')).read_bytes()).hexdigest()
  with patch.object(owner,'PROOF_SHA',digest):self.rejection()
 def test_old_partial_catalog_without_new_source_stage_keeps_old_path(self):
  with tempfile.TemporaryDirectory()as t:owner.guard_bundle(Path(t),'unrelated',{},[])
 def test_missing_owner_proof_with_active_data_is_rejected(self):
  records=self.records();(self.root/(owner.BASE+'proof.json')).unlink()
  with self.assertRaises(ValueError):owner.guard_bundle(self.root,self.roles['friend'],{},records)
 def test_current_reading_must_not_remain_unresolved(self):
  path='source-evidence/nanshi020-xiehongwei-reading/review.json';d=read(self.root,path);d['unresolved'].append({'mention':{'id':owner.GUEST}});write(self.root,path,d);self.rejection()
 def test_unknown_profile_metadata_not_whitelisted(self):
  roles,chs,people,_=self.prepared();bad=copy.deepcopy(people);bad[roles['guest']]['identity_note']='實為慧琳'
  with self.assertRaises(ValueError):owner.guard_bundle(self.root,roles['guest'],bad,self.records())

if __name__=='__main__':unittest.main()
