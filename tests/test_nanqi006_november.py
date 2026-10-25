"""Finite complete-month source and six royal-son paths; no global surname/order inference."""
import copy,json,unittest,hashlib,subprocess,sys,textwrap
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_nanqi006_november import source_errors,kinship_valid,CID
from scripts.person_ids import family_path_errors
from scripts.witness_projection import repository_positions
ROOT=Path(__file__).resolve().parents[1]
BASE='source-evidence/nanqi006-jianwu1-nov/'
class Nanqi006November(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/nanqishu/006-jianwu1-nov.json').read_bytes());cls.aset=json.loads((ROOT/'corpus/nanqishu/006-jianwu1-nov-assertions.json').read_bytes());cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_bytes())['persons']}
 def valid(self,a=None,ch=None):
  ch=self.ch if ch is None else ch;a=self.aset['assertions'][0]if a is None else a;p=ch['paragraphs'][0]
  return kinship_valid(a,{p['id']:(CID,p)},{CID:ch},ROOT)
 def test_complete_month_and_all_six(self):
  self.assertEqual([],source_errors(self.ch,ROOT));self.assertEqual(421,len(self.ch['paragraphs'][0]['text']));self.assertEqual(6,len(self.aset['assertions']));self.assertTrue(all(self.valid(a)for a in self.aset['assertions']))
 def test_all_person_marks_and_non_person_shang(self):
  ms=self.ch['paragraphs'][0]['mentions'];self.assertEqual(18,len(ms));self.assertEqual([404],[m['start']for m in ms if m['surface']=='上']);self.assertEqual(2,len([m for m in ms if m['surface']=='寳𤣥']))
 def test_all_six_paths_with_real_assertions(self):
  for a in self.aset['assertions']:
   p=self.people[a['subject_person_id']]['family_path'];self.assertEqual([],family_path_errors(a['subject_person_id'],p));self.assertEqual(a['object_person_id'],p['parent_person_id']);self.assertEqual(a['id'],p['source_assertion_id']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_wrong_known_person_cannot_comove(self):
  ch=copy.deepcopy(self.ch);a=copy.deepcopy(self.aset['assertions'][0]);m=next(m for m in ch['paragraphs'][0]['mentions']if m['id']==a['evidence'][0]['subject_person_mention_id']);m['person_id']=a['object_person_id'];a['subject_person_id']=m['person_id'];self.assertFalse(self.valid(a,ch))
 def test_wrong_role_kind_and_directions(self):
  for kind in ('work','unresolved',None):
   ch=copy.deepcopy(self.ch);m=next(m for m in ch['paragraphs'][0]['mentions']if m['start']==88);m['kind']=kind;self.assertFalse(self.valid(ch=ch))
  a=copy.deepcopy(self.aset['assertions'][0]);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(self.valid(a))
 def test_not_mother_or_ordinal(self):
  a=copy.deepcopy(self.aset['assertions'][0]);a['predicate']='mother';self.assertFalse(self.valid(a));a=copy.deepcopy(self.aset['assertions'][0]);a['qualifiers']['birth_order']={'ordinal':1};self.assertFalse(self.valid(a))
 def test_missing_royal_son_word_and_shift(self):
  ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['text']=ch['paragraphs'][0]['text'].replace('立皇子','立太子');self.assertFalse(self.valid(ch=ch))
  ch=copy.deepcopy(self.ch);m=next(m for m in ch['paragraphs'][0]['mentions']if m['start']==88);m['start']+=1;m['end']+=1;self.assertFalse(self.valid(ch=ch))
 def test_raw_projection_coshift_fails_pin(self):
  path=ROOT/BASE/'projection.json';v=json.loads(path.read_bytes());v['raw_positions']=[i+1 for i in v['raw_positions']];bad=json.dumps(v).encode();original=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda p:bad if p==path else original(p)):self.assertTrue(source_errors(self.ch,ROOT))
 def test_production_codepoint_projection(self):
  p=self.ch['paragraphs'][0];raw=(ROOT/BASE/'KR2a0017_006.txt').read_text();points,digest=repository_positions(ROOT,p,raw.splitlines());self.assertEqual(421,len(points));self.assertEqual(self.ch['source']['response_sha256'],digest)
 def test_work_book_source_and_line_bounds(self):
  for key,value in [('work_id','w-songshu'),('book_id','b-nanqishu-047'),('source_id','wrong-source'),('text_sha256','0'*64)]:
   ch=copy.deepcopy(self.ch);ch[key]=value;self.assertTrue(source_errors(ch,ROOT))
  for key,value in [('first_line',64),('last_line',88),('unit_key','other')]:
   ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['source_position'][key]=value;self.assertTrue(source_errors(ch,ROOT))
 def test_no_shenyuan_age_or_new_maternal_edge(self):
  self.assertNotIn('age_assertions',self.ch['annotation']);self.assertEqual({'father'},{a['predicate']for a in self.aset['assertions']})
 def test_malformed_inputs_fail_closed(self):
  for v in (None,[],1,'father',{}):self.assertFalse(kinship_valid(v,{}, {},ROOT))
  for v in (None,[],1):self.assertTrue(source_errors(v,ROOT))
 def test_no_owner_hint_required(self):
  path=ROOT/'registry/persons.json';v=json.loads(path.read_bytes())
  for row in v['persons']:row.pop('source_identity_key',None)
  raw=json.dumps(v,ensure_ascii=False).encode();original=Path.read_bytes
  with patch.object(Path,'read_bytes',lambda p:raw if p==path else original(p)):self.assertEqual([],source_errors(self.ch,ROOT))
 def test_direct_script_import(self):
  code="import sys,json;from pathlib import Path;r=Path(sys.argv[1]);sys.path.insert(0,str(r/'scripts'));from fixed_nanqi006_november import source_errors;c=json.loads((r/'corpus/nanqishu/006-jianwu1-nov.json').read_bytes());assert not source_errors(c,r)"
  result=subprocess.run([sys.executable,'-c',code,str(ROOT)],text=True,capture_output=True);self.assertEqual(0,result.returncode,result.stderr)
 def test_actual_main_dispatch(self):
  main=(ROOT/'scripts/validate_corpus.py').read_text();start=main.index('            try:from scripts.fixed_nanqi006_november import source_errors');end=main.index('            errors.extend(nanqi006_source_errors(d, root))',start)+len('            errors.extend(nanqi006_source_errors(d, root))');scope={'d':self.ch,'root':ROOT,'errors':[]};exec(textwrap.dedent(main[start:end]),scope);self.assertEqual([],scope['errors'])
  start=main.index("                if a.get('id','').startswith('a-nanqi006-jianwu1-nov-father-')");end=main.index("                if qualifiers.get('source_clause_binding', {}).get('kind') == 'biography_family_clause':",start);code=textwrap.dedent(main[start:end]);p=self.ch['paragraphs'][0]
  for bad in (False,True):
   a=copy.deepcopy(self.aset['assertions'][0]);results=[]
   if bad:a['qualifiers']['source_clause_binding']['kind']='wrong'
   scope={'a':a,'qualifiers':a['qualifiers'],'paragraphs':{p['id']:(CID,p)},'chapters':{CID:self.ch},'root':ROOT,'check':lambda value,message:results.append(value)};exec(code,scope);self.assertEqual([not bad],results)
 def test_old_id_not_current_or_alias(self):
  self.assertNotIn('bni_9ky_npc',self.people);self.assertFalse(any('bni_9ky_npc'in p.get('id_aliases',[])for p in self.people.values()))
if __name__=='__main__':unittest.main()
