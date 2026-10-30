import unittest,json,copy,shutil,tempfile,hashlib
from pathlib import Path
from scripts import fixed_jin098_wangdun_comparison as source
ROOT=Path(__file__).resolve().parents[1];CH='corpus/jinshu/098-wangdun-comparison.json';EP=source.EP
class Jin098Roles(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/CH).read_bytes());self.facts=json.loads((ROOT/'corpus/jinshu/098-wangdun-comparison-assertions.json').read_bytes())['assertions']
 def reject(self,ch):self.assertTrue(source.source_errors(ch,ROOT))
 def mini(self):
  t=tempfile.TemporaryDirectory();r=Path(t.name);spec=json.loads((ROOT/EP/'ner-roles.json').read_bytes());files={CH,source.RAW,'registry/persons.json','corpus/jinshu/098-wangdun-comparison-assertions.json','corpus/jinshu/098-wangdun-comparison-names.json','corpus/jinshu/098-wangdun-comparison-identities.json'}|{EP+n for n in source.PINS}|{s['native_path']for s in spec['existing_seeds'].values()}|{x['seed']['native_path']for x in spec.get('support_seeds',[])}|{s['native_path']for s in spec.get('comparison_seeds',{}).values()}|{x['seed']['native_path']for x in spec.get('negative_identity_seeds',[])}
  ref=json.loads((ROOT/EP/'ner-legal-precedent.json').read_bytes())['parallel'];files.add(ref['raw_path']);files.add(ref['native_path'])
  if json.loads((ROOT/CH).read_bytes()).get('annotation',{}).get('life_stage')=='fixed_jin098_three_basics_and_same_death':
   from scripts import fixed_jin098_wangdun_life as life
   files.update(set(life.PINS)|{life.LIFE,life.ADDR,life.GROUP,life.OLDLIFE})
  if json.loads((ROOT/CH).read_bytes()).get('annotation',{}).get('career_stage')=='fixed_jin098_career_p001_p019':
   from scripts import fixed_jin098_wangdun_career as career
   files.update(set(career.PINS)|{career.TITLES,career.DETAILS})
   files.add(career.fixed(ROOT,'calendar-row-proof.json')['existing_capture_path'])
  for rel in files:q=r/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((ROOT/rel).read_bytes())
  return t,r
 def test_whole_source_and_role_sets(self):
  self.assertEqual(source.source_errors(self.ch,ROOT),[]);self.assertEqual(len(self.ch['paragraphs']),41);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),7827);self.assertEqual(len(self.facts),16);self.assertEqual(len(json.loads((ROOT/'corpus/jinshu/098-wangdun-comparison-names.json').read_bytes())['records']),79)
  self.assertEqual(self.ch['paragraphs'][40]['text_layer'],'received_compiler_appraisal');self.assertTrue(all(p['text_layer']=='received_chapter'for p in self.ch['paragraphs'][:40]))
  spec=json.loads((ROOT/EP/'ner-roles.json').read_bytes());actual={m['id']for p in self.ch['paragraphs']for m in p['mentions']if m['kind']=='person'};self.assertEqual(actual,set(spec['role_by_mid']));self.assertEqual(len(spec['existing_seeds']),80);self.assertEqual(len(spec['new_role_first_mids']),48)
 def test_all_finite_relations_and_actual_tokens(self):
  ps={p['id']:(self.ch['id'],p)for p in self.ch['paragraphs']}
  for a in self.facts:self.assertTrue(source.family_valid(a,ps,ROOT),a['id'])
  father=next(a for a in self.facts if a['id']=='a-jin098-dun-father-ji');self.assertIn('父基，治書侍御史',father['evidence'][0]['quote'])
 def test_wrong_direction_wrong_person_and_wrong_relation(self):
  for a in self.facts:
   for mutate in ['swap','predicate','term']:
    x=copy.deepcopy(a)
    if mutate=='swap':x['subject_person_id'],x['object_person_id']=x['object_person_id'],x['subject_person_id']
    elif mutate=='predicate':x['predicate']='mother'
    else:x['qualifiers']['source_term']='兄弟世將處季'
    self.assertFalse(source.family_valid(x,root=ROOT),(a['id'],mutate))
 def test_adoptive_is_not_biological_or_office_succession(self):
  a=next(a for a in self.facts if a['id']=='a-jin098-ying-adoptive-father-dun');self.assertEqual(a['predicate'],'adoptive_father');self.assertEqual(a['qualifiers']['legal_adoption_status'],'not_stated');self.assertNotIn('succession',a['qualifiers'])
  x=copy.deepcopy(a);x['predicate']='raised_by';self.assertFalse(source.family_valid(x,root=ROOT))
  father=next(a for a in self.facts if a['id']=='a-jin098-ying-father-han');self.assertNotEqual(father['object_person_id'],a['object_person_id'])
 def test_no_inferred_father_for_han_or_chuji(self):
  roles=source.resolve(ROOT,self.ch);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']in(roles['wanghan'],roles['chuji'])for a in self.facts));self.assertNotEqual(roles['chuji'],roles['wangbin'])
 def test_false_death_edict_and_quotation_speakers(self):
  scope=json.loads((ROOT/EP/'ner-speech-reading.json').read_bytes());self.assertTrue(scope['false_death_claim']['do_not_create_false_report_life_event']);self.assertEqual(len(scope['quotes']),33)
  embedded=next(x for x in scope['quotes']if x['paragraph_id'].endswith(':p008'));self.assertEqual(embedded['speaker_role'],'yuandi');self.assertTrue(any(x.get('quoted_author_role')=='caocao'and x['speaker_role']=='dun'for x in scope['quotes']))
 def test_titles_books_and_imperial_transition(self):
  ps=self.ch['paragraphs'];self.assertFalse(any(m['start']==49 and m['surface']=='太子'for m in ps[0]['mentions']));self.assertFalse(any(m['start']==27 and m['surface']=='明帝'for m in ps[18]['mentions']));roles=source.resolve(ROOT,self.ch);m=next(m for m in ps[18]['mentions']if m['start']==1);self.assertEqual(m['person_id'],roles['yuandi']);m=next(m for m in ps[18]['mentions']if m['start']==74);self.assertEqual(m['person_id'],roles['mingdi'])
 def test_wrong_layer_source_and_co_shift(self):
  for i in[4,12,22,23,24]:x=copy.deepcopy(self.ch);x['paragraphs'][i]['text_layer']='received_compiler_appraisal';self.reject(x)
  x=copy.deepcopy(self.ch);p=x['paragraphs'][0];p['text']='某'+p['text'];p['text_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
  for m in p['mentions']:m['start']+=1;m['end']+=1
  self.reject(x)
 def test_malformed_and_boolean_qualification(self):
  for x in[None,[],1,'bad']:self.assertTrue(source.source_errors(x,ROOT))
  x=copy.deepcopy(self.ch);x['source']['image_verified']=0;self.reject(x)
  x=copy.deepcopy(self.ch);x['annotation']['human_reviewed']=True;self.reject(x)
 def test_sidecar_drift_fails_actual_context(self):
  t,r=self.mini()
  try:
   self.assertEqual(source.source_errors(self.ch,r),[]);p=r/'corpus/jinshu/098-wangdun-comparison-assertions.json';x=json.loads(p.read_bytes());x['assertions'][0]['subject_person_id']=x['assertions'][0]['object_person_id'];p.write_text(json.dumps(x,ensure_ascii=False));self.assertTrue(source.source_errors(self.ch,r))
  finally:t.cleanup()
 def test_root_argument_really_controls_raw_and_pin(self):
  t,r=self.mini()
  try:
   p=r/source.RAW;p.write_bytes(p.read_bytes()+b'\n');self.assertTrue(source.source_errors(self.ch,r));self.assertEqual(source.source_errors(self.ch,ROOT),[])
  finally:t.cleanup()
 def test_new_source_role_consistent_rekey_and_one_end_reject(self):
  t,r=self.mini()
  try:
   roles=source.resolve(r,self.ch);old=roles['jiangtong'];new='7jq_f9v_4nk';reg=json.loads((r/'registry/persons.json').read_bytes());self.assertNotIn(new,{p['id']for p in reg['persons']})
   def replace(x):
    if isinstance(x,dict):return{k:replace(v)for k,v in x.items()}
    if isinstance(x,list):return[replace(v)for v in x]
    return new if x==old else x
   for rel in['registry/persons.json',CH,'corpus/jinshu/098-wangdun-comparison-assertions.json','corpus/jinshu/098-wangdun-comparison-names.json','corpus/jinshu/098-wangdun-comparison-identities.json']:
    p=r/rel;p.write_text(json.dumps(replace(json.loads(p.read_bytes())),ensure_ascii=False))
   after=json.loads((r/CH).read_bytes());self.assertEqual(source.source_errors(after,r),[])
   m=next(m for p in after['paragraphs']for m in p['mentions']if m.get('person_id')==new);m['person_id']=old;self.assertTrue(source.source_errors(after,r))
  finally:t.cleanup()
 def test_parent_source_only_contract_still_accepted(self):
  before=json.loads((ROOT/EP/'source-template.json').read_bytes());self.assertEqual(source.source_errors(before,ROOT),[]);self.assertTrue(all(not p['mentions']for p in before['paragraphs']))
if __name__=='__main__':unittest.main()
