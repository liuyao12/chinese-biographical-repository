from tests.portable_fixture_copy import fixture_copy2
import unittest,json,copy,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
sys.path.insert(0,str(ROOT/'scripts'))
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies
from scripts.wyd_song044_nephew import nephew_valid,ancestor_valid
from scripts.wyd_song044_formal_roles import source_errors
class FormalRoleTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_bytes());cls.facts=json.loads((ROOT/'corpus/songshu/044-wyd1739-assertions.json').read_bytes());cls.catalog=load_catalog(ROOT);cls.people,cls.records=cls.catalog;cls.chapters={r['id']:r for r in cls.records if r.get('record_type')=='marked_chapter'};cls.paragraphs={p['id']:(r['id'],p)for r in cls.chapters.values()for p in r['paragraphs']};cls.assertions={a['id']:a for r in cls.records if r.get('record_type')=='person_assertion_set'for a in r['assertions']};cls.families=json.loads((ROOT/'registry/family-assemblies.json').read_bytes());cls.family=next(a for a in cls.families['assemblies']if a['id']=='family-chenjun-xie-lang');cls.rows={r['person_id']:r for r in cls.family['members']};cls.nephews=[r for r in cls.rows.values()if r.get('ancestor_connection',{}).get('type')=='wyd_song044_paternal_nephew_to_uncle_father']
 def test_source_438_and_original_qualifications(self):
  old=json.loads((ROOT/'source-evidence/song044-wyd1739-xiehui/transcription-witness-contract.json').read_bytes());self.assertEqual(self.ch['source'],old['source']);self.assertEqual([(p['text'],p['source_position'],p['text_layer'])for p in self.ch['paragraphs']],[(p['text'],p['source_position'],p['text_layer'])for p in old['paragraphs']]);self.assertEqual(source_errors(self.ch,ROOT),[]);self.assertEqual(sum(m['kind']=='person'for p in self.ch['paragraphs']for m in p['mentions']),438)
 def test_actual_assembly_and_no_unknown_fathers(self):
  _,assembled=load_assemblies(ROOT,self.catalog);self.assertEqual(len(self.nephews),2)
  for row in self.nephews:
   self.assertIn(row['person_id'],assembled);self.assertIsNone(row['parent_person_id']);self.assertEqual(row['intermediate_person_ids'],[None]);self.assertIsNone(row['source_assertion_id']);self.assertTrue(ancestor_valid(row,self.rows,self.assertions,self.chapters,ROOT))
 def test_true_nephew_direction_and_generic_rejection(self):
  a=next(a for a in self.facts['assertions']if a['id'].endswith('shao-uncle'));self.assertTrue(nephew_valid(a,self.paragraphs,ROOT));b=copy.deepcopy(a);b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id'];self.assertFalse(nephew_valid(b,self.paragraphs,ROOT))
  for term in ['從子','從弟','姊子','養子']:
   b=copy.deepcopy(a);b['qualifiers']['source_term']=term;self.assertFalse(nephew_valid(b,self.paragraphs,ROOT))
 def test_wrong_ancestor_or_father_or_human(self):
  for row in self.nephews:
   for field,value in [('ancestor_person_id',row['person_id']),('parent_person_id',row['ancestor_person_id']),('intermediate_person_ids',['invented'])]:
    b=copy.deepcopy(row);b[field]=value;self.assertFalse(ancestor_valid(b,self.rows,self.assertions,self.chapters,ROOT))
   b=copy.deepcopy(row);b['ancestor_connection']['human_reviewed']=True;self.assertFalse(ancestor_valid(b,self.rows,self.assertions,self.chapters,ROOT))
 def test_maternal_adoptive_or_conflicting_father_reject(self):
  for row in self.nephews:
   conn=row['ancestor_connection'];aid=conn['uncle_father_assertion_id']
   for q in [{'lineage':'maternal'},{'adopted_for_family_tree':False}]:
    a=copy.deepcopy(self.assertions);a[aid]['qualifiers'].update(q);self.assertFalse(ancestor_valid(row,self.rows,a,self.chapters,ROOT))
   for pred in ['father','adoptive_father']:
    a=copy.deepcopy(self.assertions);a['fake']={'id':'fake','subject_person_id':row['person_id'],'predicate':pred,'object_person_id':conn['uncle_person_id']};self.assertFalse(ancestor_valid(row,self.rows,a,self.chapters,ROOT))
 def test_invalid_shapes_fail_closed(self):
  for a in [None,[],3,{}, {'qualifiers':None},{'qualifiers':{'source_clause_binding':None}}]:self.assertFalse(nephew_valid(a,self.paragraphs,ROOT))
 def test_invalid_ancestor_connection_keeps_legacy_valueerror(self):
  # Read-only source links; only this private temporary registry JSON is mutated.
  import tempfile,shutil
  with tempfile.TemporaryDirectory(prefix='song044-family-negative-')as folder:
   view=Path(folder)
   for entry in ROOT.iterdir():
    if entry.name not in ('registry','source-evidence'):(view/entry.name).symlink_to(entry,target_is_directory=entry.is_dir())
   (view/'source-evidence').mkdir()
   for entry in(ROOT/'source-evidence').iterdir():
    if entry.name=='song044-wyd1739-xiehui':shutil.copytree(entry,view/'source-evidence'/entry.name, copy_function=fixture_copy2)
    else:(view/'source-evidence'/entry.name).symlink_to(entry,target_is_directory=entry.is_dir())
   (view/'registry').mkdir()
   for entry in(ROOT/'registry').iterdir():
    if entry.name!='family-assemblies.json':(view/'registry'/entry.name).symlink_to(entry,target_is_directory=entry.is_dir())
   path=view/'registry/family-assemblies.json';fs=copy.deepcopy(self.families);fs['assemblies']=[copy.deepcopy(self.family)];path.write_text(json.dumps(fs,ensure_ascii=False));load_assemblies(view,self.catalog)
   for invalid in [[],['bad'],'bad',4]:
    bad=copy.deepcopy(fs);row=next(r for r in bad['assemblies'][0]['members']if r['person_id']==self.nephews[0]['person_id']);row['ancestor_connection']=invalid;path.write_text(json.dumps(bad,ensure_ascii=False))
    with self.assertRaises(ValueError):load_assemblies(view,self.catalog)
 def test_source_guard_rejects_unreviewed_markup_or_annotation(self):
  self.assertEqual(source_errors(self.ch,ROOT),[])
  for field in ['mentions','annotation']:
   bad=copy.deepcopy(self.ch)
   if field=='mentions':bad['paragraphs'][0]['mentions'].append({'id':'future-marker','kind':'unresolved','start':0,'end':1,'surface':bad['paragraphs'][0]['text'][0],'person_id':None})
   else:bad['annotation']['other_editor_note']='未經覆核的新增欄位'
   self.assertTrue(source_errors(bad,ROOT))
 def test_cao_spouse_not_birth_mother(self):
  spouse=next(a for a in self.facts['assertions']if a['predicate']=='spouse');self.assertIn('妻曹',spouse['qualifiers']['source_term']);self.assertFalse(any(a['predicate']in ['mother','maternal_role']for a in self.facts['assertions']))
 def test_source_mid_or_role_corruption_reject(self):
  for field,value in [('id','wrong-mid'),('source_role_key','wrong-role'),('person_id','wrong_person_id')]:
   bad=copy.deepcopy(self.ch);m=next(m for p in bad['paragraphs']for m in p['mentions']if m['kind']=='person');m[field]=value;self.assertTrue(source_errors(bad,ROOT))
if __name__=='__main__':unittest.main()
