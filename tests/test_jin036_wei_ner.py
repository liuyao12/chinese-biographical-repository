"""Portable isolated finite-source tests; never mutate the live ROOT."""
import copy,json,hashlib,shutil,tempfile,unittest
from pathlib import Path
from scripts import fixed_jin036_wei_ner as owner
from scripts.source_person_reference_groups import validated_sets,for_people
from scripts.validation_context import scope
ROOT=Path(__file__).resolve().parents[1]
class WeiNER(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory(prefix='jin036-ner-');cls.root=Path(cls.temp.name);b=json.loads((ROOT/owner.EP).read_bytes());rels={owner.EP,owner.core.CH,'registry/persons.json','registry/works.json',b['names_path'],b['identities_path'],b['groups_path']}
  rels.update(owner.core.BASE+n for n in owner.core.PINS);rels.update(s['native_path']for s in b['external_roles']);cls.before={}
  if hasattr(owner,'CLOSE_KIN_EP')and(ROOT/owner.CLOSE_KIN_EP).is_file():
   phase=json.loads((ROOT/owner.CLOSE_KIN_EP).read_bytes());rels.add(owner.CLOSE_KIN_EP);rels.update(phase['expected_documents'])
  for rel in rels:
   src=ROOT/rel;dst=cls.root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);assert dst.stat().st_ino!=src.stat().st_ino;cls.before[rel]=hashlib.sha256(src.read_bytes()).hexdigest()
 @classmethod
 def tearDownClass(cls):
  try:
   for rel,h in cls.before.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
  finally:cls.temp.cleanup()
 def setUp(self):
  self.b,self.roles,self.people,self.ch=owner.accepted_state(self.root);self.doc=owner.read(self.root,self.b['groups_path'])
 def rejects(self,fn):
  with self.assertRaises((ValueError,KeyError,TypeError,IndexError,StopIteration)):fn()
 def test_complete_fixed_source_and_conservation(self):
  self.assertEqual(len(self.ch['paragraphs']),21);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),7129)
  ms=[m for p in self.ch['paragraphs']for m in p['mentions']];self.assertEqual(len(ms),489);self.assertEqual(sum(m['kind']=='person'for m in ms),447);self.assertEqual(sum(m['kind']=='unresolved'for m in ms),25);self.assertEqual(sum(m['kind']=='work'for m in ms),17)
  self.assertTrue(owner.validate_source(self.ch,self.root));self.assertEqual(self.ch['annotation']['modern_collation_reports'],owner.read(self.root,owner.core.BASE+'contract.json')['chapter_template']['annotation']['modern_collation_reports'])
 def test_source_annotation_downgrade_rejected(self):
  c=copy.deepcopy(self.ch);del c['annotation']['fixed_jin036_full_ner_ref'];self.rejects(lambda:owner.validate_source(c,self.root))
 def test_known_groups_members_are_not_person_mentions(self):
  docs=validated_sets([self.doc],self.people,self.root);self.assertEqual(len(docs[0]['groups']),9)
  mids={m['id']:m for p in self.ch['paragraphs']for m in p['mentions']}
  for g in self.doc['groups']:
   for mid in g['group_marker_ids']:self.assertEqual(mids[mid]['kind'],'unresolved');self.assertIsNone(mids[mid]['person_id'])
   for ref in g['members']:
    pid=ref['person_id'];m=ref['evidence'];self.assertEqual(mids[m['mention_id']]['person_id'],pid)
    self.assertFalse(any(mid in a.get('mention_ids',[])for a in self.people[pid]['aliases']for mid in g['group_marker_ids']))
 def test_unknown_owner_and_extra_set_rejected(self):
  d=copy.deepcopy(self.doc);d['owner']='invented';self.rejects(lambda:validated_sets([d],self.people,self.root));self.rejects(lambda:validated_sets([self.doc,copy.deepcopy(self.doc)],self.people,self.root))
 def test_extra_fake_group_rejected(self):
  d=copy.deepcopy(self.doc);d['groups'].append(copy.deepcopy(d['groups'][0]));self.rejects(lambda:validated_sets([d],self.people,self.root))
 def test_reported_count_bool_and_false_complete_rejected(self):
  for key,val in [('reported_count',True),('completeness','complete'),('unknown_members',False)]:
   d=copy.deepcopy(self.doc);g=next(g for g in d['groups']if g['id']=='g-jin036-group_six_sons');g[key]=val;self.rejects(lambda:validated_sets([d],self.people,self.root))
 def test_wrong_member_endpoint_or_source_rejected(self):
  for key,val in [('person_id',self.roles['jia_hou']),('evidence',dict(self.doc['groups'][0]['members'][0]['evidence'],source_id='s-fake'))]:
   d=copy.deepcopy(self.doc);d['groups'][0]['members'][0][key]=val;self.rejects(lambda:validated_sets([d],self.people,self.root))
 def test_candidate_not_alias_or_known_member(self):
  x=next(x for x in self.doc['unresolved_readings']if x['id']=='reading-jin036-wei_wen');self.assertEqual(len(x['candidate_person_ids']),2);self.assertIsNone(x['preferred_person_id']);self.assertNotIn('wei_wen',self.roles)
  d=copy.deepcopy(self.doc);next(x for x in d['unresolved_readings']if x['id']=='reading-jin036-wei_wen')['preferred_person_id']=x['candidate_person_ids'][0];self.rejects(lambda:validated_sets([d],self.people,self.root))
 def test_current_marker_retarget_and_cross_paragraph_rejected(self):
  for change in [('person_id',self.roles['jia_hou']),('start',1)]:
   c=copy.deepcopy(self.ch);m=c['paragraphs'][0]['mentions'][0];m[change[0]]=change[1];self.rejects(lambda:owner.validate_source(c,self.root))
 def test_missing_own_catalog_or_people_metadata_rejected(self):
  records=[self.ch,owner.read(self.root,self.b['names_path']),owner.read(self.root,self.b['identities_path']),self.doc];pid=self.roles['heng'];owner.guard_bundle(self.root,pid,self.people,records)
  self.rejects(lambda:owner.guard_bundle(self.root,pid,self.people,records[:-1]));people=copy.deepcopy(self.people);people[pid]['evidence']=[];self.rejects(lambda:owner.guard_bundle(self.root,pid,people,records))
 def test_unrelated_partial_catalog_keeps_old_behavior(self):
  owner.guard_bundle(self.root,'not-this-source',{'not-this-source':{'evidence':[]}},[]);self.assertEqual(validated_sets([],{},self.root),[])
 def test_names_literal_and_restored_are_separate(self):
  rows=owner.read(self.root,self.b['names_path'])['records'];self.assertEqual(len(rows),44)
  literal=next(n for n in rows if n['id']=='name-jin036-heng-literal');restored=next(n for n in rows if n['id']=='name-jin036-heng-context-restored');self.assertIsNone(literal['surname']);self.assertEqual(restored['surname'],'衛');self.assertEqual(restored['ming'],'恆')
  self.assertTrue(owner.name_record_valid(restored,self.root,rows));bad=copy.deepcopy(restored);bad['person_id']=self.roles['jia_hou'];self.assertFalse(owner.name_record_valid(bad,self.root,rows))
 def test_work_author_not_nearest_liudesheng(self):
  works=owner.expand(self.b['work_registry_fields'],self.roles);w=works['w-jin036-sitishushi'];e=w['source_author_attributions'][0];self.assertTrue(owner.work_author_valid(e,w,self.ch,self.root));bad=copy.deepcopy(e);bad['author_person_id']=self.roles['liudesheng'];self.assertFalse(owner.work_author_valid(bad,w,self.ch,self.root))
  lishi=works['w-jin036-lishi'];self.assertIsNone(lishi['author']);self.assertEqual(lishi['editorial_author_reading']['preferred_person_id'],self.roles['heng']);self.assertEqual(lishi['editorial_author_reading']['status'],'editorial_provisional')
 def test_all_wrong_work_reverse_and_source_seed_span_rejected(self):
  s=self.b['external_roles'][0];rel=s['native_path'];p=self.root/rel;raw=p.read_bytes();c=json.loads(raw);q=next(q for q in c['paragraphs']if q['id']==s['paragraph_id']);m=next(m for m in q['mentions']if m['id']==s['mention_id']);m['start']+=1;p.write_text(json.dumps(c,ensure_ascii=False))
  try:self.rejects(lambda:owner.accepted_state(self.root))
  finally:p.write_bytes(raw)
 def test_legendary_appellations_not_split_and_explicit_zi_scope(self):
  rows=owner.read(self.root,self.b['names_path'])['records']
  self.assertFalse(any(n['person_id']in {self.roles['jumeng'],self.roles['cangjie']}for n in rows))
  for role,pno,zi in [('heng',12,'\u5de8\u5c71'),('zhao',16,'\u4ef2\u5bf6')]:
   n,=[n for n in rows if n['id']=='name-jin036-'+role+'-zi-explicit'];self.assertEqual(n['zi'],zi);self.assertTrue(n['paragraph_id'].endswith(':p'+str(pno).zfill(3)));self.assertEqual(n['person_mention_id'],n['paragraph_id']+':m0000');self.assertIn('\u5b57'+zi,n['quote']);self.assertTrue(owner.name_record_valid(n,self.root,rows))
   bad=copy.deepcopy(n);bad['person_id']=self.roles['jia_hou'];self.assertFalse(owner.name_record_valid(bad,self.root,rows));bad=copy.deepcopy(n);bad['paragraph_id']=owner.core.CID+':p007';self.assertFalse(owner.name_record_valid(bad,self.root,rows))
 def test_explicit_zi_first_mentions_are_present(self):
  expected={'p001:m0004':('guan','伯玉'),'p012:m0002':('heng','巨山'),'p016:m0002':('zhao','仲寶'),'p021:m0005':('zhan','道舒')}
  ms={m['id']:m for p in self.ch['paragraphs']for m in p['mentions']}
  for suffix,(role,surface)in expected.items():
   m=ms[owner.core.CID+':'+suffix];self.assertEqual((m['surface'],m['person_id'],m['kind']),(surface,self.roles[role],'person'))
 def test_reference_collectives_and_partial_cui_do_not_forge_people(self):
  ms={m['id']:m for p in self.ch['paragraphs']for m in p['mentions']}
  expected={'m1519':'ji_ran','m1520':'sang_hongyang','m2228':'ji_ran','m2229':'sang_hongyang','m1995':'zhong_yao','m1996':'hu_zhao','m1537':'ban_public','m1538':'chui','m2235':'zai_yu','m2236':'duanmu_ci','m2519':'dudu'}
  for suffix,role in expected.items():self.assertEqual(ms[owner.core.CID+':p014:'+suffix]['person_id'],self.roles[role])
  self.assertEqual(ms[owner.core.CID+':p014:m2518']['kind'],'unresolved')
  partial=next(r for r in self.doc['unresolved_readings']if r.get('interpretation_kind')=='partial_collective_resolution');self.assertIsNone(partial['unresolved_component_refs'][0]['number_of_referents'])
 def test_dubo_is_a_qualified_non_person_exclusion(self):
  n,=self.ch['annotation']['non_person_exclusions'];self.assertEqual((n['start'],n['end'],n['surface']),(2782,2784,'杜伯'));self.assertEqual(n['classification'],'non_person');self.assertFalse(any(m['start']<=2782<m['end']for p in self.ch['paragraphs']if p['id']==n['paragraph_id']for m in p['mentions']))
 def test_external_preferred_names_do_not_fake_literal_components(self):
  rows=owner.read(self.root,self.b['names_path'])['records']
  for role,full in [('wen_shu','張昶'),('zuoziyi','左伯')]:
   r=next(r for r in self.doc['unresolved_readings']if r.get('subject_person_id')==self.roles[role]);self.assertEqual(r['preferred_name_components']['full_name'],full);self.assertIsNone(r['literal_source_components']['ming']);self.assertFalse(any(n['person_id']==self.roles[role]for n in rows))
   self.assertEqual(self.people[self.roles[role]]['label'],full)
 def test_collective_wrong_member_or_external_literal_upgrade_rejected(self):
  d=copy.deepcopy(self.doc);r=next(r for r in d['unresolved_readings']if r.get('interpretation_kind')=='collective_resolution');r['resolved_member_refs'][0]['person_id']=self.roles['jia_hou'];self.rejects(lambda:validated_sets([d],self.people,self.root))
  d=copy.deepcopy(self.doc);r=next(r for r in d['unresolved_readings']if r.get('interpretation_kind')=='external_name_reading');r['literal_source_components']['ming']=r['preferred_name_components']['ming'];self.rejects(lambda:validated_sets([d],self.people,self.root))
 def test_unrelated_100_calls_use_only_bounded_source_index(self):
  from unittest.mock import patch
  calls=[];original=owner.read
  def logged(root,rel):calls.append(rel);return original(root,rel)
  with scope(self.root),patch.object(owner,'read',side_effect=logged):
   for i in range(100):owner.guard_bundle(self.root,'unrelated-'+str(i),{},[])
  self.assertEqual(calls.count(owner.core.CH),1);self.assertNotIn('registry/persons.json',calls)
  self.assertLess(len(self.people),200)
 def test_outside_scope_rereads_reverse_change(self):
  p=self.root/'registry/persons.json';raw=p.read_bytes();v=json.loads(raw);person=next(p for p in v['persons']if p['id']==self.roles['heng']);person['evidence'][0]['work_id']='w-fake';p.write_text(json.dumps(v,ensure_ascii=False))
  try:self.rejects(lambda:owner.accepted_state(self.root))
  finally:p.write_bytes(raw)
if __name__=='__main__':unittest.main()
