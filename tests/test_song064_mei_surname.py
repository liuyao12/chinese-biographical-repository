import unittest,json,copy,tempfile,hashlib
from pathlib import Path
from scripts.surname_from_father import validate
from scripts.surname_received_grandfather import valid,CH,RAW,REF,KIND
from scripts.biographical_work_references import projection_valid
R=Path(__file__).resolve().parents[1]
class Song064MeiSurname(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.c=json.loads((R/CH).read_bytes());self.names=json.loads((R/'corpus/songshu/064-peisongzhi-name-components.json').read_bytes())['records'];self.a=json.loads((R/'corpus/songshu/064-peisongzhi-assertions.json').read_bytes())['assertions'];self.n=copy.deepcopy(next(n for n in self.names if n.get('id')=='name-song064-mei-contextual'))
  for rel in(CH,RAW,REF):p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((R/rel).read_bytes())
 def ok(self):return valid(self.n,self.names,{self.c['id']:self.c},self.a,self.root)
 def chapter(self):
  (self.root/CH).write_text(json.dumps(self.c,ensure_ascii=False))
 def test_dispatcher_preserves_non_dict_valueerror(self):
  for bad in (None,[],'bad'):
   with self.subTest(value=bad):
    with self.assertRaisesRegex(ValueError,'Name record must be a dictionary'):
     validate(bad,self.names,{self.c['id']:self.c},self.a,root=self.root)
 def test_real_gate_and_literal_retained(self):
  self.assertTrue(self.ok());validate(self.n,self.names,{self.c['id']:self.c},self.a,root=self.root)
  literal=next(n for n in self.names if n.get('id')=='name-song064-mei-literal');self.assertIsNone(literal['surname']);self.assertEqual(literal['ming'],'昧');self.assertEqual(self.n['surname'],'裴')
 def test_existing_4arg_source_validator_positive_and_foreign_layer_negative(self):
  b={'received_text_projection':{'path':REF,'sha256':hashlib.sha256((self.root/REF).read_bytes()).hexdigest(),'source_layer':'received_text','text_layer':'received_text'}}
  self.assertTrue(projection_valid(self.c,self.c['paragraphs'],b,self.root));self.c['paragraphs'][0]['text_layer']='commentary';self.chapter();self.assertFalse(projection_valid(self.c,self.c['paragraphs'],b,self.root));self.assertFalse(self.ok())
 def test_grandfather_not_father_or_shisun_or_collateral(self):
  for role,distance in [('father',1),('ancestor',8),('agnatic_cousin',2)]:
   n=copy.deepcopy(self.n);n['surname_basis']['source_role']=role;n['surname_basis']['generation_distance']=distance;self.assertFalse(valid(n,self.names,{self.c['id']:self.c},self.a,self.root))
 def test_maternal_adoptive_or_wrong_predicate(self):
  original=copy.deepcopy(self.a)
  for change in ['maternal','adoptive','father']:
   self.a=copy.deepcopy(original);a=next(a for a in self.a if a['id']=='a-song064-songzhi-grandfather')
   if change=='maternal':a['qualifiers']['lineage']='maternal'
   elif change=='adoptive':a['qualifiers']['adoptive']=True
   else:a['predicate']='father'
   self.assertFalse(self.ok())
 def test_wrong_seed_target_or_missing_literal(self):
  for key,value in [('source_name_record_id','name-song064-gui-contextual'),('literal_name_record_id','missing')]:
   n=copy.deepcopy(self.n);n['surname_basis'][key]=value;self.assertFalse(valid(n,self.names,{self.c['id']:self.c},self.a,self.root))
  self.n['person_mention_id']=self.c['id']+':p001:m0024';self.assertFalse(self.ok())
 def test_revision_int_not_coerced_and_bad_types_fail(self):
  self.n['surname_basis']['source_frame']['source_revision']='1748217';self.assertFalse(self.ok())
  for obj in(None,[],True):self.assertFalse(valid(obj,self.names,{self.c['id']:self.c},self.a,self.root))
 def test_source_url_raw_and_projection_changes_fail(self):
  for rel in(RAW,REF):
   old=(self.root/rel).read_bytes();(self.root/rel).write_bytes(old+b'X');self.assertFalse(self.ok());(self.root/rel).write_bytes(old)
  self.c['source']['permalink']='https://example.test';self.chapter();self.assertFalse(self.ok())
 def test_raw_and_reported_sha_coshift_fails(self):
  p=self.root/RAW;p.write_bytes(p.read_bytes()+b'X');sha=hashlib.sha256(p.read_bytes()).hexdigest();self.c['source']['raw_sha256']=self.c['source']['raw_file_sha256']=sha;self.n['surname_basis']['source_frame']['raw_sha256']=sha;self.chapter();self.assertFalse(self.ok())
 def test_full_unit_not_truncated_and_glyph_not_rewritten(self):
  original=copy.deepcopy(self.c);self.c['paragraphs'].pop();self.chapter();self.assertFalse(self.ok());self.c=original;self.c['paragraphs'][0]['text']=self.c['paragraphs'][0]['text'].replace('祖昧','外祖昧');self.chapter();self.assertFalse(self.ok())
 def test_conflicting_literal_surname_and_false_human_review(self):
  self.names.append(dict(person_id=self.n['person_id'],surname='某',ming='昧'));self.assertFalse(self.ok());self.names.pop();self.n['human_reviewed']=True;self.assertFalse(self.ok())
if __name__=='__main__':unittest.main()
