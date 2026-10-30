import copy,json,unittest,tempfile,shutil,hashlib
from pathlib import Path
from contextlib import contextmanager
from scripts import fixed_jin031_jia_comparison as h
from scripts.fixed_wikisource_units import source_errors
from scripts.name_xiaoming import validate_xiaoming
from scripts.surname_from_father import validate as validate_surname
ROOT=Path(__file__).resolve().parents[1]
@contextmanager
def changed(rel,mutate):
 p=ROOT/rel;assert p.resolve().is_relative_to(ROOT.resolve());old=p.read_bytes()
 try:
  v=json.loads(old);mutate(v);p.write_text(json.dumps(v,ensure_ascii=False));yield v
 finally:p.write_bytes(old)
class Scope(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  global ROOT
  cls.source_root=ROOT
  proof=h.fixed(ROOT)
  dependencies={h.CH,h.EP,h.NS,h.AD,'registry/persons.json','data/corpus/chapter-directory.json',proof['raw_path'],proof['father_assertion']['native_path'],proof['father_name']['native_path']}
  dependencies.update(seed['native_path']for seed in proof['seeds'])
  from scripts import fixed_jin031_jia_full_ner as ner
  if ner.active(ROOT):
   fullproof=ner.fixed(ROOT);dependencies.update({ner.EP,ner.IP,ner.NSN});dependencies.update(seed['native_path']for seed in fullproof['external_roles'])
  if(ROOT/'source-evidence/jin031-jia-comparison/typed-phase-proof.json').is_file():
   from scripts.fixed_jin031_jia_typed import fixture_paths
   dependencies.update(fixture_paths(ROOT))
  cls.source_hashes={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()for rel in dependencies}
  cls.private_root=tempfile.TemporaryDirectory(prefix='cbr-jin031-negative-tests-')
  cls.addClassCleanup(cls.restore_source_root)
  for rel in dependencies:
   src=ROOT/rel;dst=Path(cls.private_root.name)/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
   if src.stat().st_ino==dst.stat().st_ino:raise AssertionError('Negative fixture must not share source inode')
  ROOT=Path(cls.private_root.name)
  cls.ch=h.read(ROOT,h.CH);cls.rs,_phaseproof=h.prepared(cls.ch,ROOT);cls.proof=h.fixed(ROOT);cls.ns=h.read(ROOT,h.NS);cls.names=cls.ns['records'];cls.p=cls.ch['paragraphs'][0]
 @classmethod
 def restore_source_root(cls):
  global ROOT
  ROOT=cls.source_root
  try:
   changed_sources=[rel for rel,digest in cls.source_hashes.items()if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest]
   if changed_sources:raise AssertionError('Negative tests changed authoritative source: '+str(changed_sources))
  finally:cls.private_root.cleanup()
 def test_normal_source_entry_full8(self):
  self.assertEqual(source_errors(self.ch,ROOT),[]);self.assertEqual(len(self.ch['paragraphs']),8);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),1628);self.assertEqual([p['annotation_status']for p in self.ch['paragraphs']],['in_progress']*8);self.assertEqual([p['annotation_status']for p in h.fixed(ROOT)['chapter_template']['paragraphs']],['in_progress']+['pending']*7)
 def test_two_distinct_modern_refs(self):
  a,b=self.ch['annotation']['modern_collation_reports'];self.assertEqual((a['report_kind'],b['report_kind']),('calendar_calculation','editorial_collation_report'));self.assertIn('为十七日',a['raw_text']);self.assertIn('宋本',b['raw_text']);self.assertFalse(any('十七日'in p['text']or'今從殿本'in p['text']for p in self.ch['paragraphs']))
 def test_ref_physical_bound_and_text_rejected(self):
  for field,value in [('raw_start',0),('raw_text','<ref>別注</ref>')]:
   with changed(h.CH,lambda c:c['annotation']['modern_collation_reports'][0].update({field:value}))as c:self.assertTrue(source_errors(c,ROOT))
 def test_unknown_template_raw_rejected(self):
  p=ROOT/self.proof['raw_path'];old=p.read_bytes();assert p.resolve().is_relative_to(ROOT.resolve())
  try:p.write_bytes(old.replace('{{YL|泰始八年}}'.encode(),'{{ZZ|泰始八年}}'.encode(),1));self.assertTrue(source_errors(self.ch,ROOT))
  finally:p.write_bytes(old)
 def test_unknown_link_target_rejected(self):
  p=ROOT/self.proof['raw_path'];old=p.read_bytes();assert p.resolve().is_relative_to(ROOT.resolve())
  try:p.write_bytes(old.replace('[[晉書/卷040#賈充|別有傳]]'.encode(),'[[晉書/卷041#賈充|別有傳]]'.encode(),1));self.assertTrue(source_errors(self.ch,ROOT))
  finally:p.write_bytes(old)
 def test_crossperson_time_rejected(self):
  p=copy.deepcopy(self.p);next(m for m in p['mentions']if m['id'].endswith(':m0015'))['person_id']=self.rs['father']
  with self.assertRaises(ValueError):validate_xiaoming(self.names[0],p)
 def test_wrong_ming_and_ordinary_time_rejected(self):
  for key,value in [('ming','午'),('xiaoming','時年')]:
   n=copy.deepcopy(self.names[0]);n[key]=value
   with self.assertRaises(ValueError):validate_xiaoming(n,self.p)
 def test_borrow_father_origin_rejected(self):
  with changed(h.AD,lambda a:a['assertions'][0]['place'].update(source_name='平陽襄陵')):self.assertTrue(source_errors(self.ch,ROOT))
 def test_no_invented_zi_or_birth(self):
  validate_xiaoming(self.names[0],self.p);self.assertNotIn('zi',self.names[0]);self.assertNotIn('birth_year',self.names[0]);self.assertEqual(h.read(ROOT,h.AD)['assertions'][0]['relation'],'biographical_origin');self.assertEqual(h.read(ROOT,h.AD)['assertions'][0]['place']['source_name'],'平陽')
 def test_xref_points_actual_father_unit(self):
  from scripts.cross_chapter_references import errors
  c=h.read(ROOT,'corpus/jinshu/040-wyd1739-jiachong.json');self.assertEqual(errors({self.ch['id']:self.ch,c['id']:c},ROOT),[]);r=self.ch['cross_chapter_references'][0];self.assertEqual(r['target']['paragraph_id'],c['paragraphs'][0]['id'])
 def test_complete_reverse_work_source_rejected(self):
  for field in ['work_id','source_id']:
   def mutate(r):
    person=next(p for p in r['persons']if p['id']==self.rs['queen']);e=next(e for e in person['evidence']if e['mention_id']==h.CID+':p001:m0005');e[field]='wrong-source'
   with changed('registry/persons.json',mutate):self.assertTrue(source_errors(self.ch,ROOT))
 def test_external_seed_span_rejected(self):
  seed=self.proof['seeds'][0]
  def mutate(c):
   p=next(p for p in c['paragraphs']if p['id']==seed['paragraph']['id']);m=next(m for m in p['mentions']if m['id']==seed['mention_id']);m['start']-=1;m['surface']=p['text'][m['start']:m['end']]
  with changed(seed['native_path'],mutate):self.assertTrue(source_errors(self.ch,ROOT))
 def test_unrelated_partial_catalog_unchanged(self):
  h.guard_bundle(ROOT,'unrelated_existing_person',{},[])
  people={p['id']:p for p in h.read(ROOT,'registry/persons.json')['persons']}
  with self.assertRaises(ValueError):h.guard_bundle(ROOT,self.rs['queen'],people,[])
 def test_scope_context_equal_and_bounded_copy(self):
  from scripts.validation_context import scope
  before=h.source_context(ROOT)
  with scope(ROOT):
   first=h.source_context(ROOT);second=h.source_context(ROOT);self.assertEqual(first,second);self.assertEqual(first,before);self.assertEqual(set(first[2]),set(first[1].values()));self.assertEqual(len(first[2]),2);second[2][self.rs['queen']]['label']='caller mutation';self.assertEqual(h.source_context(ROOT),first)
 def test_outside_scope_reverse_change_fresh_rejected(self):
  from scripts.validation_context import scope
  with scope(ROOT):h.source_context(ROOT)
  def mutate(r):
   person=next(p for p in r['persons']if p['id']==self.rs['queen']);e=next(e for e in person['evidence']if e['mention_id']==self.proof['seeds'][0]['mention_id']);e['work_id']='wrong-source'
  with changed('registry/persons.json',mutate):
   with self.assertRaises(ValueError):h.source_context(ROOT)
 def test_same_scope_missing_caller_records_still_rejected(self):
  from scripts.validation_context import scope
  people={p['id']:p for p in h.read(ROOT,'registry/persons.json')['persons']}
  with scope(ROOT):
   h.source_context(ROOT)
   with self.assertRaises(ValueError):h.guard_bundle(ROOT,self.rs['queen'],people,[])
 def test_roles_symbolic_uid(self):
  t=h.expand(self.proof['chapter_template'],{'queen':'replacement_uid_A','father':'replacement_uid_B'});self.assertEqual({m['person_id']for p in t['paragraphs']for m in p['mentions']},{'replacement_uid_A','replacement_uid_B'})
if __name__=='__main__':unittest.main(verbosity=2)
