from pathlib import Path
import copy,json,tempfile,shutil,unittest,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import fixed_wuyingdian_jin040_jiachong as m
CID=m.CID
def current_source_fixture_paths(root,c=None):
 root=Path(root);c=m._c40_contract(root)if c is None else c
 paths={'registry/persons.json','corpus/jinshu/040-wyd1739-jiachong.json',*[f'corpus/jinshu/040-wyd1739-jiachong-{k}.json'for k in('names','assertions','addresses')]}
 for s in c['role_specs'].values():
  paths.update(z['path']for z in s.get('seeds',[]))
 for comparison in c.get('identity_comparisons',[]):paths.update(z['path']for z in comparison['supporting_seed']['seeds'])
 paths.update(str(p.relative_to(root))for p in(root/m.BASE).rglob('*')if p.is_file())
 # Copy actual named phase inputs, not a silent fallback to an older source owner.
 if (root/m.EW_SEED_CASE_PATH).is_file():
  ew=json.loads((root/m.EW_SEED_CASE_PATH).read_bytes())
  paths.update((m.EW_SEED_CASE_PATH,ew['source_path'],ew['identity_decisions_path']))
  for spec in ew['role_seeds'].values():paths.update(seed['path']for seed in spec['seeds'])
  paths.update(pin['path']for pin in ew['reference_payloads'])
 if (root/m.WQ_CASE_PATH).is_file():paths.add(m.WQ_RECORD_PATH)
 if m.death_stage_present(root):
  death=m._death_case(root)
  paths.update((m.DEATH_LIFE,m.DEATH_GROUP,'corpus/jinshu/039.json','corpus/jinshu/039-life-events.json',death['calendar_proof']['existing_capture_path']))
 return paths

class Cases(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();cls.r=Path(cls.tmp.name);cls.ch=json.loads((ROOT/'corpus/jinshu/040-wyd1739-jiachong.json').read_text());c=m._c40_contract(ROOT)
  paths=current_source_fixture_paths(ROOT,c)
  for rel in paths:
   out=cls.r/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,out)
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def bad(self,f):
  c=copy.deepcopy(self.ch);f(c)
  with self.assertRaises((ValueError,KeyError,StopIteration)):m.validate_source(c,self.r)
 def file_bad(self,rel,f):
  p=self.r/rel;b=p.read_bytes()
  try:
   x=json.loads(b);f(x);p.write_text(json.dumps(x,ensure_ascii=False))
   with self.assertRaises((ValueError,KeyError,StopIteration)):m.validate_source(copy.deepcopy(self.ch),self.r)
  finally:p.write_bytes(b)
 def test_01_actual(self):self.assertTrue(m.validate_source(self.ch,self.r))
 def test_02_body(self):self.bad(lambda c:c['paragraphs'][0].update(text='錯'+c['paragraphs'][0]['text'][1:]))
 def test_03_person_endpoint(self):self.bad(lambda c:c['paragraphs'][0]['mentions'][0].update(person_id='missing'))
 def test_04_offset(self):self.bad(lambda c:c['paragraphs'][0]['mentions'][0].update(start=1))
 def test_05_kind(self):self.bad(lambda c:c['paragraphs'][0]['mentions'][0].update(kind='unresolved',person_id=None))
 def test_06_human(self):self.bad(lambda c:c['annotation'].update(human_reviewed=True))
 def test_07_unknown_metadata(self):self.bad(lambda c:c['annotation'].update(unreviewed_extra='x'))
 def test_08_registry_alias(self):
  mid=self.ch['paragraphs'][0]['mentions'][0]['id'];pid=self.ch['paragraphs'][0]['mentions'][0]['person_id']
  self.file_bad('registry/persons.json',lambda r:next(p for p in r['persons']if p['id']==pid)['aliases'][0].update(mention_ids=[]))
 def test_09_registry_reverse_source(self):
  pid=self.ch['paragraphs'][0]['mentions'][0]['person_id']
  def f(r):next(e for p in r['persons']if p['id']==pid for e in p['evidence']if e.get('chapter_id')==CID)['source_id']='wrong'
  self.file_bad('registry/persons.json',f)
 def test_10_new_name_owner(self):self.file_bad('corpus/jinshu/040-wyd1739-jiachong-names.json',lambda d:d['records'][0].update(person_id='wrong'))
 def test_11_fact_direction(self):self.file_bad('corpus/jinshu/040-wyd1739-jiachong-assertions.json',lambda d:d['assertions'][0].update(object_person_id=d['assertions'][0]['subject_person_id']))
 def test_12_address_missing_nan(self):
  def f(d):next(a for a in d['assertions']if a['id']=='pa-jin040-wyd-hanshou')['qualifiers']['source_address_fragments']['fragments'].pop(0)
  self.file_bad('corpus/jinshu/040-wyd1739-jiachong-addresses.json',f)
 def test_13_address_wrong_owner(self):
  def f(d):next(a for a in d['assertions']if a['id']=='pa-jin040-wyd-hanshou')['person_id']='wrong'
  self.file_bad('corpus/jinshu/040-wyd1739-jiachong-addresses.json',f)
 def test_14_address_nonadjacent(self):
  def f(d):next(a for a in d['assertions']if a['id']=='pa-jin040-wyd-hanshou')['context']['paragraph_ids'][1]=self.ch['paragraphs'][17]['id']
  self.file_bad('corpus/jinshu/040-wyd1739-jiachong-addresses.json',f)
 def test_15_address_offset(self):
  def f(d):next(a for a in d['assertions']if a['id']=='pa-jin040-wyd-hanshou')['qualifiers']['source_address_fragments']['fragments'][1]['start']=1
  self.file_bad('corpus/jinshu/040-wyd1739-jiachong-addresses.json',f)
 def test_16_address_source(self):
  def f(d):next(a for a in d['assertions']if a['id']=='pa-jin040-wyd-hanshou')['evidence'][0]['source_id']='wrong'
  self.file_bad('corpus/jinshu/040-wyd1739-jiachong-addresses.json',f)
 def test_17_known_seed_metadata(self):
  c=m._c40_contract(self.r);s=next(s for s in c['role_specs'].values()if s['kind']=='known_source_roles')['seeds'][0]
  self.file_bad(s['path'],lambda d:d['source'].update(image_verified=True))
 def test_18_known_seed_mid(self):
  c=m._c40_contract(self.r);s=next(s for s in c['role_specs'].values()if s['kind']=='known_source_roles')['seeds'][0]
  def f(d):next(x for p in d['paragraphs']for x in p['mentions']if x['id']==s['person_mention_ids'][0])['id']='changed'
  self.file_bad(s['path'],f)
 def test_19_known_seed_full_quote(self):
  c=m._c40_contract(self.r);s=next(s for s in c['role_specs'].values()if s['kind']=='known_source_roles')['seeds'][0]
  self.file_bad(s['path'],lambda d:next(p for p in d['paragraphs']if p['id']==s['paragraph']['id']).update(text='錯'))
 def test_20_raw(self):
  p=self.r/(m.BASE+'transcription-columns.txt');b=p.read_bytes()
  try:
   p.write_bytes(b+'錯'.encode())
   with self.assertRaises(ValueError):m.validate_source(self.ch,self.r)
  finally:p.write_bytes(b)
 def test_21_contract_type(self):
  self.file_bad(m.BASE+m.C40_CONTRACT,lambda d:d.update(human_reviewed=0))
 def test_22_missing_chapter_api_guard(self):
  reg=json.loads((self.r/'registry/persons.json').read_text());people={p['id']:p for p in reg['persons']};pid=self.ch['paragraphs'][0]['mentions'][0]['person_id']
  with self.assertRaises(ValueError):m.guard_bundle(self.r,pid,people,[])
 def test_23_pending_api_guard(self):
  people={p['id']:p for p in json.loads((self.r/'registry/persons.json').read_text())['persons']};c=copy.deepcopy(self.ch);c['annotation'].pop('formal_phase');pid=self.ch['paragraphs'][0]['mentions'][0]['person_id']
  with self.assertRaises(ValueError):m.guard_bundle(self.r,pid,people,[c])
 def test_24_source_word_boundaries(self):
  c=m._c40_contract(self.r);t=''.join(p['text']for p in self.ch['paragraphs']);self.assertIn('大子斃於金酒',t);self.assertIn('小子困於枯木',t);self.assertIn('郭彰字叔武太原人賈后從舅也',t);self.assertNotIn('槐生黎民',t);self.assertEqual(len(t),5016)
 def test_25_wrong_root(self):
  with tempfile.TemporaryDirectory()as d:self.assertTrue(m.source_errors(self.ch,Path(d)))
 def test_26_comparison_full_quote(self):
  c=m._c40_contract(self.r);seed=c['identity_comparisons'][0]['supporting_seed']['seeds'][0]
  self.file_bad(seed['path'],lambda d:next(p for p in d['paragraphs']if p['id']==seed['paragraph']['id']).update(text='錯'))
 def test_27_jia_mi_full_name_boundary(self):
  p=next(p for p in self.ch['paragraphs']if p['id']==CID+':p020');mark=next(x for x in p['mentions']if x['surface']=='賈謐');self.assertEqual((mark['start'],mark['end']),(130,132));self.bad(lambda c:next(x for p in c['paragraphs']for x in p['mentions']if x['id']==mark['id']).update(start=131,surface='謐'))
 def test_28_returned_result_pollution(self):
  from scripts.validation_context import scope
  with scope(self.r):
   a=m.complete_unit_state(copy.deepcopy(self.ch),self.r);pid=next(iter(a['people']));before=a['people'][pid]['label'];a['people'][pid]['label']='污染'
   self.assertEqual(m.complete_unit_state(copy.deepcopy(self.ch),self.r)['people'][pid]['label'],before)
 def test_29_fragment_catalog_missing_chapter(self):
  people={p['id']:p for p in json.loads((self.r/'registry/persons.json').read_text())['persons']};ch,roles,docs=m._c40_local_docs(self.r)
  with self.assertRaises(ValueError):m.source_name_fragments(self.r,{roles['wangcui']},people,list(docs.values()))
 def test_30_unsupported_shapes(self):
  for value in [(),[],None,'bad',True]:self.assertFalse(m.same(value,{}))
  self.assertFalse(m.same((1,),(1,)));self.assertFalse(m.same({'x':True},{'x':1}));self.assertFalse(m.same(float('nan'),float('nan')));self.assertFalse(m.same({1:'x'},{1:'x'}))
 def test_31_annotation_type_preserves_pending_guard(self):
  for value in [None,[],'bad',True]:self.bad(lambda c,v=value:c.update(annotation=v))
 def test_32_unrelated_malformed_binding_is_not_claimed(self):
  for value in [None,[],'bad',True]:self.assertFalse(m.family_applies({'qualifiers':{'fixed_source_kinship':value}}))
if __name__=='__main__':unittest.main()
