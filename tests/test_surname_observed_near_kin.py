"""Normal surname-dispatch regression on a bounded physical source fixture.

Only registered source files requested by the opt-in rows are copied; no tree
clone/export. Test-only root overrides let the sealed after rows be reviewed
against an unchanged source carrier before adoption.
"""
import unittest,tempfile,json,pathlib,copy,os,hashlib
from scripts.surname_from_father import validate
KIND='contextual_surname_from_observed_named_near_kin'
BASE=pathlib.Path(os.environ.get('CBR_SURNAME_TEST_INPUT_ROOT',pathlib.Path(__file__).resolve().parents[1]))
ROWS=pathlib.Path(os.environ.get('CBR_SURNAME_TEST_ROWS_ROOT',BASE))
class ObservedSurname(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();cls.root=pathlib.Path(cls.tmp.name);cls.original={};cls.names=[];cls.assertions=[];cls.chapters={}
  for p in sorted((ROWS/'corpus').glob('*/*.json')):
   doc=json.loads(p.read_text())
   cls.names.extend(n for n in doc.get('records',[])if isinstance(n,dict)and n.get('surname_basis',{}).get('kind')==KIND)
  if not cls.names:raise AssertionError('Real opted-in source rows required; no permanent skip')
  aids={n['surname_basis']['edge']['assertion_id']for n in cls.names}|{n['surname_basis']['seed']['father_assertion_id']for n in cls.names if n['surname_basis']['seed']['kind']=='declared_clan_near_member'}
  for p in sorted((BASE/'corpus').glob('*/*.json')):
   doc=json.loads(p.read_text());cls.assertions.extend(a for a in doc.get('assertions',[])if a.get('id')in aids)
  paths={'registry/persons.json','registry/works.json','registry/work-provenance.json'}
  for n in cls.names:
   for f in n['surname_basis']['frames']:paths.update((f['native_path'],f['capture_path']))
   paths.add(n['surname_basis']['edge']['assertions_path'])
   if n['surname_basis']['seed'].get('father_assertions_path'):paths.add(n['surname_basis']['seed']['father_assertions_path'])
  for rel in paths:
   value=(BASE/rel).read_bytes();p=cls.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value);cls.original[rel]=value
   if rel.startswith('corpus/'):
    ch=json.loads(value)
    if ch.get('record_type')=='marked_chapter':cls.chapters[ch['id']]=ch
  cls.roles={n['surname_basis']['edge']['rule']:n for n in cls.names};cls.seeds={n['surname_basis']['seed']['kind']:n for n in cls.names}
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def setUp(self):self.names=copy.deepcopy(type(self).names);self.aa=copy.deepcopy(type(self).assertions);self.cs=copy.deepcopy(type(self).chapters);self.changed=[]
 def tearDown(self):
  for rel in self.changed:(self.root/rel).write_bytes(self.original[rel])
 def wrong_current(self,exclude):return next(p['id']for p in json.loads(self.original['registry/persons.json'])['persons']if p['id']!=exclude)
 def selected(self,rule='head_named_paternal_grandfather'):return next(n for n in self.names if n['surname_basis']['edge']['rule']==rule)
 def check(self,n):return validate(n,self.names,self.cs,self.aa,root=self.root)
 def reject(self,n):
  with self.assertRaises(ValueError):self.check(n)
 def write(self,rel,doc):self.changed.append(rel);(self.root/rel).write_text(json.dumps(doc,ensure_ascii=False))
 def test01_all_actual_opted_rows_normal_dispatch(self):
  for n in self.names:self.check(n)
 def test02_wrong_person(self):n=self.selected();n['person_id']=self.wrong_current(n['person_id']);self.reject(n)
 def test03_foreign_seed_mid(self):n=self.selected();n['surname_basis']['seed']['person_mention_id']='foreign:p:m';self.reject(n)
 def test04_wrong_assertion_endpoint(self):
  n=self.selected();a=next(a for a in self.aa if a['id']==n['surname_basis']['edge']['assertion_id']);a['object_person_id']=self.wrong_current(a['object_person_id']);self.reject(n)
 def test05_wrong_clause_literal(self):n=self.selected();n['surname_basis']['edge']['clause_anchor']['surface']+='假';self.reject(n)
 def qualification_attack(self,key,value):
  n=self.selected();f=n['surname_basis']['frames'][0];ch=self.cs[f['chapter_id']];ch['source'][key]=value;f['source_metadata'][key]=value;self.write(f['native_path'],ch);self.reject(n)
 def test06_no_fake_fixed_body(self):self.qualification_attack('fixed_body_obtained',True)
 def test07_no_fake_image(self):self.qualification_attack('image_verified',True)
 def test08_no_fake_reported_revision(self):self.qualification_attack('revision_id',9999999)
 def test09_map_must_match_actual_capture(self):n=self.selected();n['surname_basis']['frames'][0]['character_positions'][0]=False;self.reject(n)
 def test10_missing_physical_reverse(self):
  n=self.selected();mid=n['surname_basis']['seed']['person_mention_id'];doc=json.loads(self.original['registry/persons.json']);
  for p in doc['persons']:p['evidence']=[e for e in p.get('evidence',[])if e.get('mention_id')!=mid]
  self.write('registry/persons.json',doc);self.reject(n)
 def test11_missing_alias(self):
  n=self.selected();mid=n['surname_basis']['seed']['person_mention_id'];doc=json.loads(self.original['registry/persons.json'])
  for p in doc['persons']:
   for a in p.get('aliases',[]):a['mention_ids']=[x for x in a['mention_ids']if x!=mid]
  self.write('registry/persons.json',doc);self.reject(n)
 def test12_single_physical_endpoint_change(self):
  n=self.selected();f=n['surname_basis']['frames'][0];ch=self.cs[f['chapter_id']];mid=n['surname_basis']['seed']['person_mention_id']
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m['id']==mid:m['person_id']=self.wrong_current(m['person_id'])
  self.write(f['native_path'],ch);self.reject(n)
 def test13_coherent_rekey_keeps_raw_mid_assertion_ids(self):
  n=self.selected();f=n['surname_basis']['frames'][0];old=next(m['person_id']for p in self.cs[f['chapter_id']]['paragraphs']for m in p['mentions']if m['id']==n['surname_basis']['seed']['person_mention_id']);new='zzz_zzz_zzz'
  mids=[m['id']for c in self.cs.values()for p in c['paragraphs']for m in p['mentions']];aids=[a['id']for a in self.aa]
  def project(x):
   if type(x)is str:return new if x==old else x
   if type(x)is list:return[project(v)for v in x]
   if type(x)is dict:return{k:project(v)for k,v in x.items()}
   return x
  for rel,value in self.original.items():
   if rel.startswith('corpus/')or rel=='registry/persons.json':self.write(rel,project(json.loads(value)))
  self.cs=project(self.cs);self.aa=project(self.aa);self.names=project(self.names);n=self.selected();self.check(n)
  self.assertEqual(mids,[m['id']for c in self.cs.values()for p in c['paragraphs']for m in p['mentions']]);self.assertEqual(aids,[a['id']for a in self.aa]);self.assertTrue(all((self.root/rel).read_bytes()==b for rel,b in self.original.items()if rel.startswith('source-evidence/')))
 def test14_brother_unknown_parent_not_generated(self):
  n=self.selected('named_brother_clause');before=copy.deepcopy(self.aa);self.check(n);self.assertEqual(before,self.aa)
 def test15_maternal_only_not_allowed(self):
  n=self.selected('named_brother_clause');a=next(a for a in self.aa if a['id']==n['surname_basis']['edge']['assertion_id']);a['qualifiers']['same_mother_only']=True;self.reject(n)
 def test16_clan_seed_not_arbitrary_far_ancestor(self):
  n=next(n for n in self.names if n['surname_basis']['seed']['kind']=='declared_clan_near_member');f=n['surname_basis']['frames'][0];p=self.cs[f['chapter_id']]['paragraphs'][0];other=next(m for m in p['mentions']if m['start']<20);n['surname_basis']['seed']['person_mention_id']=other['id'];self.reject(n)
 def test17_extra_editorial_metadata_preserved(self):
  n=self.selected();n['unknown_editorial_metadata']={'human_reviewed':False};before=copy.deepcopy(n);self.check(n);self.assertEqual(n,before)
 def test18_whole_evidence_quote_required(self):
  n=self.selected();a=next(a for a in self.aa if a['id']==n['surname_basis']['edge']['assertion_id']);a['evidence'][0]['quote']=a['qualifiers']['source_term'];self.reject(n)
 def test19_unknown_kind_not_accepted(self):n=self.selected();n['surname_basis']['kind']='unreviewed_kind';self.reject(n)
 def test20_no_unobserved_print_edition(self):self.qualification_attack('edition','武英殿本')
 def test21_clan_not_a_literal_fullname(self):
  n=next(n for n in self.names if n['surname_basis']['seed']['kind']=='declared_clan_near_member');n['surname_basis']['seed']['not_full_name_literal']=False;self.reject(n)
 def test22_ordinary_bundle_name_api_on_bounded_source_root(self):
  from scripts.person_bundle import bundle
  n=self.selected();people={p['id']:p for p in json.loads(self.original['registry/persons.json'])['persons']};records=[*self.cs.values(),{'record_type':'person_name_component_set','records':self.names},{'record_type':'person_assertion_set','assertions':self.aa}]
  result=bundle(n['person_id'],root=self.root,include_provisional=True,catalog=(people,records));self.assertEqual(result['canonical_person_id'],n['person_id']);self.assertTrue(any(p.get('id')==n['person_id']for p in result['persons']))
 def test23_caller_cannot_invent_existing_assertion_id(self):
  n=self.selected();a=next(a for a in self.aa if a['id']==n['surname_basis']['edge']['assertion_id']);a['id']='not-a-physical-assertion';n['surname_basis']['edge']['assertion_id']=a['id'];self.reject(n)
 def test24_caller_assertion_metadata_type_strict(self):
  n=self.selected();a=next(a for a in self.aa if a['id']==n['surname_basis']['edge']['assertion_id']);a['human_reviewed']=0;self.reject(n)
if __name__=='__main__':unittest.main(verbosity=2)
