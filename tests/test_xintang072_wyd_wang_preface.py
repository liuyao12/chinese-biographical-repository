"""Normal catalog/API checks for one fixed 404-character source, never a full-corpus pass."""
import copy,json,tempfile,unittest,xml.etree.ElementTree as ET
from pathlib import Path
from scripts import fixed_repository_witness as witness
from scripts.fixed_xintang072_wang_preface import near_pair_valid,family_valid
from scripts.person_bundle import load_catalog,bundle,validate_courtesy_name,validate_full_name
from scripts.person_ids import family_path_errors
from scripts.biography_family_clause import valid as typed_family_valid
from scripts.render_corpus import render
from scripts.validation_context import scope
ROOT=Path(__file__).resolve().parents[1]
CID='c-xintangshu-072zhong-wyd1739-wang-preface';CH='corpus/xintangshu/072zhong-wyd1739-wang-preface.json';BASE='source-evidence/xintang072zhong-wyd1739-wang-preface'
class WangPrefaceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=json.loads((ROOT/CH).read_bytes());cls.roles=witness.validate_source(cls.chapter,ROOT)
  cls.catalog=load_catalog(ROOT);cls.people,cls.records=cls.catalog
  cls.chapters={r['id']:r for r in cls.records if r.get('record_type')=='marked_chapter'}
  cls.paragraphs={p['id']:(c['id'],p)for c in cls.chapters.values()for p in c['paragraphs']}
  cls.assertions=json.loads((ROOT/CH.replace('.json','-assertions.json')).read_bytes())['assertions']
  cls.names=json.loads((ROOT/CH.replace('.json','-names.json')).read_bytes())['records']
 def test_complete_source_and_normal_xml(self):
  self.assertEqual(len(self.roles),59);self.assertEqual(sum(len(p['text'])for p in self.chapter['paragraphs']),404)
  self.assertEqual(sum(len(p['mentions'])for p in self.chapter['paragraphs']),95)
  self.assertEqual(sum(p['text'].count('〓')for p in self.chapter['paragraphs']),1)
  self.assertEqual((ROOT/CH.replace('.json','.xml')).read_text(),render(self.chapter))
  xml=ET.fromstring(render(self.chapter));self.assertEqual([''.join(p.itertext())for p in xml],[p['text']for p in self.chapter['paragraphs']])
 def test_all_four_real_fathers_and_paths(self):
  self.assertEqual(len(self.assertions),4)
  for a in self.assertions:
   self.assertTrue(typed_family_valid(a,self.paragraphs,chapters=self.chapters,root=ROOT));self.assertTrue(near_pair_valid(a,self.chapter,ROOT))
   path=self.people[a['subject_person_id']]['family_path'];self.assertEqual(family_path_errors(a['subject_person_id'],path),[])
   self.assertEqual(path['parent_person_id'],a['object_person_id']);self.assertEqual(path['source_assertion_id'],a['id'])
 def test_nineteen_new_roots_do_not_acquire_deep_parentage(self):
  receipt=json.loads((ROOT/BASE/'ner-role-contract.json').read_bytes());paths=receipt['new_role_family_paths']
  self.assertEqual(len(paths),23);self.assertEqual(sum(p is not None for p in paths.values()),4)
  for key,p in paths.items():
   if p is None:self.assertNotIn('family_path',self.people[self.roles['$'+key]])
  for key in ('hongrang','hongzhi'):self.assertIsNone(paths[key]);self.assertEqual(len(self.roles['$'+key]),11)
 def test_all_names_use_normal_component_validation(self):
  self.assertEqual(len(self.names),23)
  for name in self.names:
   para=next(p for p in self.chapter['paragraphs']if p['id']==name['paragraph_id'])
   validate_full_name(name,para,chapter=self.chapter,root=ROOT);validate_courtesy_name(name)
  z=next(n for n in self.names if n.get('full_name')=='宗敬') if any('full_name'in n for n in self.names)else None
  self.assertIsNone(z['surname']);self.assertIsNone(z['ming'])
 def test_normal_api_all_source_roles_keep_original_identity(self):
  with scope(ROOT):
   for role,pid in self.roles.items():
    b=bundle(pid,root=ROOT,catalog=self.catalog)
    mids={m['id']for m in b['mentions']if m['chapter_id']==CID}
    expected={m['id']for p in self.chapter['paragraphs']for m in p['mentions']if m['person_id']==pid}
    self.assertEqual(mids,expected,role)
 def test_unknown_glyph_identity_does_not_claim_a_reading(self):
  m=next(m for p in self.chapter['paragraphs']for m in p['mentions']if m['surface']=='〓')
  self.assertTrue(witness.glyph_person_valid(self.chapter,m,ROOT));self.assertFalse(m['glyph_uncertainty']['source_glyph_filled']);self.assertFalse(m['glyph_uncertainty']['human_reviewed'])
  bad=copy.deepcopy(m);bad['surface']='穎';self.assertFalse(witness.glyph_person_valid(self.chapter,bad,ROOT))
 def test_foreign_endpoint_and_reversal_rejected_independently(self):
  for a in self.assertions:
   bad=copy.deepcopy(a);bad['subject_person_id'],bad['object_person_id']=bad['object_person_id'],bad['subject_person_id'];self.assertFalse(near_pair_valid(bad,self.chapter,ROOT));self.assertFalse(family_valid(bad,self.paragraphs,self.chapters,ROOT))
   bad=copy.deepcopy(a);bad['object_person_id']=self.roles['$hongrang'];self.assertFalse(near_pair_valid(bad,self.chapter,ROOT))
 def test_caller_missing_or_extra_reverse_alias_rejected(self):
  pid=self.roles['$hongrang']
  for extra in (False,True):
   people=self.people.copy();p=copy.deepcopy(people[pid]);people[pid]=p
   if extra:p['aliases'].append({'surface':'false','mention_ids':[CID+':fake']})
   else:p['evidence']=[e for e in p['evidence']if e.get('chapter_id')!=CID]
   with self.assertRaises(ValueError):witness.validate_source(self.chapter,ROOT,people,self.records)
 def test_caller_new_family_path_removed_or_fabricated_rejected(self):
  for key in ('qian_liang','hongrang'):
   people=self.people.copy();pid=self.roles['$'+key];people[pid]=copy.deepcopy(people[pid])
   if key=='qian_liang':people[pid].pop('family_path')
   else:people[pid]['family_path']={'connection':'father','parent_person_id':self.roles['$zi_sui']}
   with self.assertRaises(ValueError):witness.validate_source(self.chapter,ROOT,people,self.records)
 def test_caller_catalog_erasure_and_sidecar_mutation_rejected(self):
  records=[r for r in self.records if r.get('id')!=CID]
  with self.assertRaises(ValueError):witness.guard_bundle(ROOT,self.roles['$hongrang'],self.people,records)
  records=copy.deepcopy(self.records);r=next(r for r in records if r.get('record_type')=='person_assertion_set'and any(a.get('id','').startswith('a-xintang072-wyd-')for a in r.get('assertions',[])));r['assertions'].pop()
  with self.assertRaises(ValueError):witness.validate_source(self.chapter,ROOT,self.people,records)
 def test_malformed_family_record_fails_closed(self):
  for a in (None,True,[],{}, {'qualifiers':None},{'qualifiers':{'source_clause_binding':None}}):
   self.assertFalse(family_valid(a,self.paragraphs,self.chapters,ROOT))
 def test_empty_synthetic_root_does_not_impersonate_installed_source(self):
  with tempfile.TemporaryDirectory()as d:witness.guard_bundle(Path(d),'aaa_bbb_111',{'aaa_bbb_111':{'id':'aaa_bbb_111'}},[])
if __name__=='__main__':unittest.main()
