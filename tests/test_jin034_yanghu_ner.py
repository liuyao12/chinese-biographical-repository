# coding: utf-8
"""Finite complete Yang Hu source tests. All mutation targets are unique physical temp files."""
from pathlib import Path
import copy,hashlib,json,shutil,tempfile,unittest
from unittest.mock import patch
from tests.portable_fixture_copy import fixture_copy2
from scripts import fixed_jin034_yanghu_ner as m
from scripts.validation_context import scope
from tests.jin034_phase_fixture import synchronized_minimal_parent_pins
ROOT=Path(__file__).resolve().parents[1]
class YangHuNER(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.addClassCleanup(cls.temp.cleanup);cls.T=Path(cls.temp.name);b=m.fixed(ROOT);rels={'registry/persons.json','registry/works.json',m.CH,m.EP,b['source_parent_path'],b['names_path'],b['identities_path'],b['groups_path'],m.BASE+'projection.json',m.BASE+'rendered-extract.txt'}|{s['native_path']for s in b['external_roles']};cls.source_hash={};cls.original={}
  # New finite family phase is a real source dependency, not an exemption.
  family_path=m.BASE+'close-kin-phase.json'
  if (ROOT/family_path).is_file():
   fb=m.read(ROOT,family_path);rels.add(family_path);rels.update(fb['expected_documents']);rels.update(fb['reference_pins'])
  minimal_path=m.BASE+'minimal-life-phase.json'
  if (ROOT/minimal_path).is_file():
   mb=m.read(ROOT,minimal_path);rels.add(minimal_path);rels.update(mb['expected_documents'])
  for rel in rels:
   src=ROOT/rel;dst=cls.T/rel;dst.parent.mkdir(parents=True,exist_ok=True);fixture_copy2(src,dst);assert src.stat().st_ino!=dst.stat().st_ino and dst.resolve().is_relative_to(cls.T.resolve());cls.source_hash[rel]=hashlib.sha256(src.read_bytes()).hexdigest();cls.original[rel]=dst.read_bytes()
 @classmethod
 def tearDownClass(cls):
  assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==h for k,h in cls.source_hash.items());cls.temp.cleanup()
 def setUp(self):
  self.b,self.r,self.people,self.ch=m.accepted_state(self.T)
 def tearDown(self):
  for rel,raw in self.original.items():
   p=self.T/rel
   if p.read_bytes()!=raw:
    p.unlink();fixture_copy2(ROOT/rel,p);assert p.read_bytes()==raw and p.stat().st_ino!=(ROOT/rel).stat().st_ino
 def change(self,rel,fn):
  p=self.T/rel;v=json.loads(p.read_bytes());fn(v);p.write_text(json.dumps(v,ensure_ascii=False,separators=(',',':'))+'\n')
 def records(self):
  records=[self.ch]+[m.read(self.T,self.b[k])for k in('names_path','identities_path','groups_path')]
  minimal_path=m.BASE+'minimal-life-phase.json'
  if (self.T/minimal_path).is_file():records += [m.read(self.T,p)for p in m.read(self.T,minimal_path)['expected_documents']]
  return records
 def test_full_source_shape(self):
  self.assertEqual((len(self.ch['paragraphs']),sum(len(p['text'])for p in self.ch['paragraphs'])),(41,6567));self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),387);self.assertEqual(len(self.r),114)
 def test_all_source_anchors_exact(self):
  for p in self.ch['paragraphs']:
   end=0
   for x in p['mentions']:self.assertTrue(type(x['start'])is int and end<=x['start']<x['end']);self.assertEqual(p['text'][x['start']:x['end']],x['surface']);end=x['end']
 def test_comparison_not_wyd(self):
  s=self.ch['source'];self.assertIsNone(s['edition']);self.assertFalse(s['preferred_text_base']);self.assertFalse(s['image_verified']);self.assertFalse(s['human_reviewed']);self.assertEqual(s['revision_id'],2567662)
 def test_body_drift(self):
  self.change(m.CH,lambda x:x['paragraphs'][0].update(text=x['paragraphs'][0]['text'].replace('上党','上黨')))
  self.assertTrue(m.source_errors(m.read(self.T,m.CH),self.T,source_path=self.T/m.CH))
 def test_unknown_source_layer(self):
  self.change(m.CH,lambda x:x['paragraphs'][30].update(text_layer='received_compiler_appraisal'))
  self.assertTrue(m.source_errors(m.read(self.T,m.CH),self.T,source_path=self.T/m.CH))
 def test_missing_owner_annotation(self):
  self.change(m.CH,lambda x:x['annotation'].pop('fixed_jin034_full_ner_ref'))
  self.assertTrue(m.source_errors(m.read(self.T,m.CH),self.T,source_path=self.T/m.CH))
 def test_wrong_person_single_endpoint(self):
  def f(x):x['paragraphs'][0]['mentions'][0]['person_id']=self.r['yang_dao']
  self.change(m.CH,f)
  with self.assertRaises(ValueError):m.accepted_state(self.T)
 def test_wrong_span_same_source(self):
  def f(x):x['paragraphs'][0]['mentions'][0]['end']+=1
  self.change(m.CH,f)
  with self.assertRaises(ValueError):m.accepted_state(self.T)
 def test_missing_seven_field_reverse(self):
  pid=self.r['yang_dao'];mid=next(s['mention_id']for s in self.b['local_roles']if s['role']=='yang_dao')
  def f(x):
   p=next(p for p in x['persons']if p['id']==pid);next(e for e in p['evidence']if e.get('mention_id')==mid)['work_id']='w-shiji'
  self.change('registry/persons.json',f)
  with self.assertRaises(ValueError):m.accepted_state(self.T)
 def test_missing_alias_reverse(self):
  pid=self.r['yang_dao'];mid=next(s['mention_id']for s in self.b['local_roles']if s['role']=='yang_dao')
  def f(x):
   p=next(p for p in x['persons']if p['id']==pid)
   for a in p['aliases']:a['mention_ids']=[m for m in a['mention_ids']if m!=mid]
  self.change('registry/persons.json',f)
  with self.assertRaises(ValueError):m.accepted_state(self.T)
 def test_literal_and_restored_sheep_name(self):
  ns=m.read(self.T,self.b['names_path'])['records'];pid=self.r['yang_dao'];own=[n for n in ns if n['person_id']==pid];self.assertEqual({(n['surname'],n['ming'])for n in own},{(None,'道'),('羊','道')});self.assertTrue(all(m.name_record_valid(n,self.T,ns)for n in own))
 def test_wrong_surname_rejected(self):
  def f(x):next(n for n in x['records']if n.get('surname_basis'))['surname']='王'
  self.change(self.b['names_path'],f)
  with self.assertRaises(ValueError):m.accepted_state(self.T)
 def test_explicit_zi_not_alias_guess(self):
  ns=m.read(self.T,self.b['names_path'])['records'];self.assertTrue(any(n['person_id']==self.r['yang_hu']and n.get('zi')=='叔子'for n in ns));self.assertTrue(any(n['person_id']==self.r['yang_liang']and n.get('zi')=='長玄'for n in ns))
 def test_mother_not_biological(self):
  d=m.read(self.T,self.b['groups_path']);row=next(x for x in d['unresolved_readings']if x.get('subject_person_id')==self.r['hu_mother']);self.assertEqual(row['qualifiers']['biological_mother_status'],'not_stated');self.assertNotEqual(self.r['hu_mother'],self.r['qianmu_kong'])
 def test_biological_mother_injection_rejected(self):
  def f(x):next(x for x in x['unresolved_readings']if x.get('subject_person_id')==self.r['hu_mother'])['qualifiers']['biological_mother_status']='source_attested'
  self.change(self.b['groups_path'],f)
  with self.assertRaises(ValueError):m.accepted_state(self.T)
 def test_unknown_group_owner_is_not_ignored(self):
  from scripts.source_person_reference_groups import validated_sets
  d=m.read(self.T,self.b['groups_path']);d['owner']='unknown_source'
  with self.assertRaises(ValueError):validated_sets([d],self.people,self.T)
 def test_extra_group_rejected(self):
  d=m.read(self.T,self.b['groups_path']);g=copy.deepcopy(d['groups'][0]);g['id']='fake-extra';d['groups'].append(g)
  with self.assertRaises(ValueError):m.group_set_valid(d,self.people,self.T)
 def test_group_does_not_create_people(self):
  d=m.read(self.T,self.b['groups_path']);g=next(g for g in d['groups']if g['id'].endswith('two-wangs-group'));self.assertEqual(g['reported_count'],2);self.assertEqual({r['person_id']for r in g['members']},{self.r['wang_rong'],self.r['wang_yan']});self.assertTrue(all(next(m for p in self.ch['paragraphs']for m in p['mentions']if m['id']==mid)['person_id']is None for mid in g['group_marker_ids']))
 def test_rebirth_not_identity_equality(self):
  d=m.read(self.T,self.b['groups_path']);g=next(g for g in d['unresolved_readings']if g.get('subject_person_id')==self.r['deceased_li_child']);self.assertIs(g['qualifiers']['identity_equality_asserted'],False);self.assertNotEqual(self.r['deceased_li_child'],self.r['yang_hu'])
 def test_work_author_not_namer(self):
  w={x['id']:x for x in m.read(self.T,'registry/works.json')['works']};self.assertEqual(w['w-jin034-yanghu-laozizhuan']['source_author_attributions'][0]['author_person_id'],self.r['yang_hu']);self.assertIsNone(w['w-jin034-duoleibei']['author']);self.assertNotIn('source_author_attributions',w['w-jin034-duoleibei'])
 def test_wrong_author_rejected(self):
  def f(x):next(w for w in x['works']if w['id']=='w-jin034-yanghu-laozizhuan')['source_author_attributions'][0]['author_person_id']=self.r['du_yu']
  self.change('registry/works.json',f)
  with self.assertRaises(ValueError):m.accepted_state(self.T)
 def test_missing_catalog_owner_sidecar(self):
  records=self.records();m.guard_bundle(self.T,self.r['yang_hu'],self.people,records)
  for kind in('marked_chapter','person_name_component_set','person_identity_decision_set','source_person_reference_group_set'):
   with self.assertRaises(ValueError):m.guard_bundle(self.T,self.r['yang_hu'],self.people,[r for r in records if r['record_type']!=kind])
 def test_scope_equivalence_and_caller_fresh(self):
  a=m.accepted_state(self.T)
  with scope(self.T):
   b=m.accepted_state(self.T);self.assertEqual(a,b);bad=copy.deepcopy(self.people);bad[self.r['yang_hu']]['label']='wrong'
   with self.assertRaises(ValueError):m.guard_bundle(self.T,self.r['yang_hu'],bad,self.records())
 def test_irrelevant_100_pid_bounded_reads(self):
  calls=[];original=m.read
  def counted(root,rel):calls.append(rel);return original(root,rel)
  with patch.object(m,'read',counted),scope(self.T):
   for i in range(100):m.guard_bundle(self.T,f'unrelated-{i}',{},[])
  self.assertNotIn('registry/persons.json',calls);self.assertNotIn(m.EP,calls);self.assertLessEqual(calls.count(m.CH),1)
 def test_generic_identity_and_name_files_visible(self):
  from scripts.person_bundle import load_catalog
  with scope(ROOT):people,records=load_catalog(ROOT)
  self.assertEqual(len([r for r in records if r.get('record_type')=='person_identity_decision_set'and r.get('chapter_id')==m.CID]),1);self.assertEqual(len([r for r in records if r.get('record_type')=='person_name_component_set'and r.get('chapter_id')==m.CID]),1)
 def test_consistent_local_leaf_rekey_and_single_end_rejection(self):
  before_registry=m.read(self.T,'registry/persons.json');old=self.r['yang_pian'];new='z9z_z9z_z9z';self.assertNotIn(new,{p['id']for p in m.read(self.T,'registry/persons.json')['persons']})
  def rewrite(v):
   if isinstance(v,str):return new if v==old else v
   if isinstance(v,list):return [rewrite(x)for x in v]
   if isinstance(v,dict):return {k:rewrite(x)for k,x in v.items()}
   return v
  rekey_paths=['registry/persons.json',m.CH,self.b['names_path'],self.b['identities_path'],self.b['groups_path']]
  if (self.T/(m.BASE+'close-kin-phase.json')).is_file():rekey_paths+=list(m.read(self.T,m.BASE+'close-kin-phase.json')['expected_documents'])
  for rel in rekey_paths:
   (self.T/rel).write_text(json.dumps(rewrite(m.read(self.T,rel)),ensure_ascii=False,separators=(',',':'))+'\n')
  b,r,people,ch=m.accepted_state(self.T);self.assertEqual(r['yang_pian'],new);self.assertNotIn(old,people)
  after_registry=m.read(self.T,'registry/persons.json');self.assertEqual(after_registry,rewrite(before_registry));self.assertEqual(len(after_registry['persons']),len(before_registry['persons']))
  def wrong(x):
   mark=next(m for p in x['paragraphs']for m in p['mentions']if m.get('person_id')==new);mark['person_id']=old
  self.change(m.CH,wrong)
  with self.assertRaises((ValueError,KeyError)):m.accepted_state(self.T)
 def test_same_chapter_scope_is_real_schema_value(self):
  ids=m.read(self.T,self.b['identities_path'])['decisions'];self.assertEqual(sum(d['scope']=='same_chapter'for d in ids),51);self.assertTrue(all(d['scope']in('same_chapter','cross_chapter')for d in ids));self.assertTrue(all((len(d['chapter_ids'])==1 if d['scope']=='same_chapter'else len(d['chapter_ids'])>=2)for d in ids))
if __name__=='__main__':unittest.main()

class YangZhaoLiteral(YangHuNER):
 def test_yang_zhao_full_literal_not_family_prefix(self):
  rows=[n for n in m.read(self.T,self.b['names_path'])['records']if n['person_id']==self.r['yang_zhao']]
  self.assertEqual(len(rows),1);self.assertEqual((rows[0]['surname'],rows[0]['ming']),('楊','肇'));self.assertNotIn('surname_basis',rows[0])
 def test_record_and_template_changed_together_still_rejected(self):
  def wrong(x):
   for n in x['records']:
    if n['person_id']==self.r['yang_zhao']:n['surname']='羊'
  self.change(self.b['names_path'],wrong)
  b=copy.deepcopy(m.read(self.T,m.EP))
  for n in b['names_template']['records']:
   if n['person_id']=='$role:yang_zhao':n['surname']='羊'
  pp=self.T/m.EP;pp.write_text(json.dumps(b,ensure_ascii=False)+'\n');newpin=hashlib.sha256(pp.read_bytes()).hexdigest()
  from contextlib import ExitStack
  with ExitStack() as stack:
   stack.enter_context(patch.object(m,'PROOF_SHA',newpin))
   family_path=m.BASE+'close-kin-phase.json'
   if (self.T/family_path).is_file():
    from scripts import fixed_jin034_core_kinship as family
    fb=m.read(self.T,family_path);fb['parent_ner_sha256']=newpin;fp=self.T/family_path;fp.write_text(json.dumps(fb,ensure_ascii=False)+'\n');stack.enter_context(patch.object(family,'PROOF_SHA',hashlib.sha256(fp.read_bytes()).hexdigest()))
   stack.enter_context(synchronized_minimal_parent_pins(self.T))
   with self.assertRaisesRegex(ValueError,'楊肇原文明姓'):m.accepted_state(self.T)
