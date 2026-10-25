"""Real source-shaped surname gates. No label/family-ID identity whitelist."""
from pathlib import Path
import json,copy,tempfile,subprocess,sys,os,unittest
ROOT=Path(__file__).resolve().parents[1]
class SourceSurnames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.scope=json.loads((ROOT/'tests/fixtures/elided-surname-source-scope.json').read_text());rows=[json.loads((ROOT/p).read_text())for p in cls.scope['native_paths']]
  cls.names=[n for r in rows if r.get('record_type')=='person_name_component_set'for n in r['records']];cls.chapters={r['id']:r for r in rows if r.get('record_type')=='marked_chapter'};cls.assertions=[a for r in rows if r.get('record_type')=='person_assertion_set'for a in r['assertions']]
  cls.new=[n for rel in cls.scope['new_sidecars']for n in json.loads((ROOT/rel).read_text())['records']]
 def test_all33_real_name_gates(self):
  from scripts.surname_from_father import validate
  from scripts.fixed_kanripo_fact_slots import valid
  from scripts.fixed_biography_names import component_valid
  self.assertEqual(len(self.new),33);self.assertEqual(sum('surname_basis'in n for n in self.new),18)
  for n in self.new:
   with self.subTest(name=n['id']):
    validate(n,self.names,self.chapters,self.assertions,ROOT)
    if n.get('fixed_source_fact_binding',{}).get('kind')=='fixed_kanripo_person_fact_slots':self.assertTrue(valid(n,self.chapters[n['chapter_id']],ROOT))
    if 'fixed_biography_name_binding'in n:self.assertTrue(component_valid(n,self.chapters[n['chapter_id']],ROOT,self.assertions))
 def test_existing_contract_endpoint_and_surname_negatives(self):
  from scripts.surname_from_father import validate
  kinds=('contextual_surname_from_same_source_father_chain','contextual_surname_from_fixed_biography_family','contextual_surname_from_fixed_kanripo_slots')
  for n in self.new:
   if n.get('surname_basis',{}).get('kind')not in kinds:continue
   bad=copy.deepcopy(n)
   if bad['surname_basis']['kind']=='contextual_surname_from_fixed_kanripo_slots':bad['surname']='不相干姓'
   else:bad['surname_basis']['steps'][0]['to_person_id']='wrong-source-role-person'
   with self.subTest(name=n['id']),self.assertRaises(ValueError):validate(bad,self.names,self.chapters,self.assertions,ROOT)
 def test_literal_null_unchanged(self):
  by={n['id']:n for n in self.names}
  for rid,original in self.scope['original_literal_null_records_without_mutable_pid'].items():self.assertEqual({k:v for k,v in by[rid].items()if k!='person_id'},original)
 def test_badtypes_and_wrong_person(self):
  from scripts.bounded_source_surname import valid
  from scripts.surname_from_father import validate
  for bad in (None,[],'bad',{},dict(bounded_source_name_binding=None)):
   self.assertFalse(valid(bad,self.names,self.chapters,self.assertions,ROOT))
  for bad in (None,[],'bad'):
   with self.assertRaises(ValueError):validate(bad,self.names,self.chapters,self.assertions,ROOT)
  n=copy.deepcopy(next(n for n in self.new if 'bounded_source_name_binding'in n));n['person_id']='same-glyph-different-person';self.assertFalse(valid(n,self.names,self.chapters,self.assertions,ROOT))
 def test_no_mother_adoption_or_wrong_assertion(self):
  from scripts.bounded_source_surname import valid
  n=next(n for n in self.new if n.get('surname_basis',{}).get('kind')=='contextual_surname_from_bound_legacy_biography')
  aid=n['surname_basis']['steps'][0]['assertion_id']
  for pred in ('mother','adoptive_father','brother'):
   aa=copy.deepcopy(self.assertions);next(a for a in aa if a['id']==aid)['predicate']=pred;self.assertFalse(valid(n,self.names,self.chapters,aa,ROOT))
 def test_coherent_source_layer_work_span_raw_rejected(self):
  from scripts.bounded_source_surname import valid
  note=next(n for n in self.new if n.get('surname_basis',{}).get('kind')=='contextual_surname_from_bound_note_ancestor')
  legacy=next(n for n in self.new if n.get('surname_basis',{}).get('kind')=='contextual_surname_from_bound_legacy_biography')
  config=json.loads((ROOT/'scripts/bounded_source_surname.json').read_text())
  for record,change in [(note,'layer'),(note,'work'),(legacy,'span'),(legacy,'raw')]:
   proof=config['proofs'][record['bounded_source_name_binding']['key']];ch=copy.deepcopy(self.chapters[record['chapter_id']]);frame=proof['frame']
   with tempfile.TemporaryDirectory()as td:
    root=Path(td);f=root/frame['native_path'];f.parent.mkdir(parents=True);raw=root/frame['raw_file'];raw.parent.mkdir(parents=True,exist_ok=True);raw.write_bytes((ROOT/frame['raw_file']).read_bytes());q=root/'scripts/bounded_source_surname.json';q.parent.mkdir();q.write_text(json.dumps(config,ensure_ascii=False))
    if change=='layer':ch['paragraphs'][1]['text_layer']='received_chapter'
    elif change=='work':ch['paragraphs'][1]['mentions'][0]['work_id']='wrong-existing-work'
    elif change=='span':ch['paragraphs'][0]['mentions'][0]['start']+=1
    else:raw.write_bytes(raw.read_bytes()+b' ')
    f.write_text(json.dumps(ch,ensure_ascii=False));cs=dict(self.chapters);cs[ch['id']]=ch;self.assertFalse(valid(record,self.names,cs,self.assertions,root))
 def test_real_direct_script_dual_import(self):
  with tempfile.TemporaryDirectory()as td:
   p=Path(td);data=p/'data.json';data.write_text(json.dumps(dict(names=self.names,chapters=self.chapters,assertions=self.assertions,new=self.new),ensure_ascii=False));h=p/'harness.py'
   h.write_text("from pathlib import Path\nimport sys,json,importlib.util\nsys.path.insert(0,sys.argv[1]+'/scripts')\nassert importlib.util.find_spec('scripts') is None\nfrom surname_from_father import validate\nd=json.loads(Path(sys.argv[2]).read_text())\nfor n in d['new']:validate(n,d['names'],d['chapters'],d['assertions'],Path(sys.argv[1]))\nprint('direct script new33 passed')\n")
   result=subprocess.run([sys.executable,'-B',str(h),str(ROOT),str(data)],cwd=p,env=dict(os.environ,PYTHONPATH='',PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr);self.assertIn('new33 passed',result.stdout)
if __name__=='__main__':unittest.main()
