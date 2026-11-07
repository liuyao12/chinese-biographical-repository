import unittest,json,copy,os
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_jin035_peixiu_peiwei_registration import errors,guard_bundle
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(os.environ.get('CBR_ALLUSION_TEST_ROOT',Path(__file__).resolve().parents[1]))
CH='corpus/jinshu/035-peixiu-peiwei.json'
class ClassicalAllusionSuccessor(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/CH).read_text());cls.people,cls.records=load_catalog(ROOT)
 def altered(self,changes):
  original=Path.read_text
  def read(path,*args,**kwargs):
   try:rel=str(path.relative_to(ROOT))
   except ValueError:return original(path,*args,**kwargs)
   return json.dumps(changes[rel],ensure_ascii=False)if rel in changes else original(path,*args,**kwargs)
  return patch.object(Path,'read_text',read)
 def test_all_source_and_finite_types(self):
  self.assertEqual(errors(self.ch,ROOT),[]);self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),252 if (ROOT/'source-evidence/jin035-peixiu-peiwei/contemporary-ner-contract.json').exists() else 133)
  self.assertEqual(sum(m['kind']=='unresolved'for p in self.ch['paragraphs']for m in p['mentions']),23 if (ROOT/'source-evidence/jin035-peixiu-peiwei/contemporary-ner-contract.json').exists() else 22)
 def test_literal_source_truncation_rejected(self):
  ch=copy.deepcopy(self.ch);ch['paragraphs'][1]['text']=ch['paragraphs'][1]['text'][:-1]
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_work_promoted_to_person_rejected(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='禹貢');m.update(kind='person',person_id='x2u_81x_m6e',status='contextual_provisional')
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_wrong_allusion_endpoint_rejected(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='樊仲');m['person_id']='gxd_15x_9d0'
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_missing_reverse_and_alias_rejected(self):
  reg=json.loads((ROOT/'registry/persons.json').read_text());p=next(p for p in reg['persons']if p['id']=='x2u_81x_m6e');p['aliases']=[];p['evidence']=[]
  with self.altered({'registry/persons.json':reg}):self.assertTrue(errors(self.ch,ROOT))
 def test_original_family_direction_still_rejected(self):
  rel='corpus/jinshu/035-peixiu-peiwei-assertions.json';doc=json.loads((ROOT/rel).read_text());a=doc['assertions'][0];a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
  with self.altered({rel:doc}):self.assertTrue(errors(self.ch,ROOT))
 def test_partial_caller_catalog_rejected(self):
  records=[r for r in self.records if r.get('chapter_id')!='c-jinshu-035-peixiu-peiwei'or r.get('record_type')!='identity_decision_set']
  with self.assertRaises(AssertionError):guard_bundle(ROOT,'x2u_81x_m6e',self.people,records)
 def test_caller_person_reverse_omission_rejected(self):
  people=copy.deepcopy(self.people);people['x2u_81x_m6e']['evidence']=[]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,'x2u_81x_m6e',people,self.records)
 def test_normal_consumer_keeps_sources_and_does_not_promote_work(self):
  for pid in ['x2u_81x_m6e','kzy_ysk_775','kbq_kjc_n2f_AA','kbq_kjc_n2f_AAB']:
   out=bundle(pid,root=ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertEqual(out['canonical_person_id'],pid)
  out=bundle('x2u_81x_m6e',root=ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertTrue(any(x.get('chapter_id')=='c-jinshu-035-peixiu-peiwei'for x in next(p for p in out['persons']if p['id']=='x2u_81x_m6e')['evidence']))
 def test_coherent_namespace_rekey_keeps_name_source_valid(self):
  original=Path.read_text
  def rewrite(v):
   if isinstance(v,dict):return{k:rewrite(x)for k,x in v.items()}
   if isinstance(v,list):return[rewrite(x)for x in v]
   return 'zzz_abc_def'if v=='x2u_81x_m6e'else v
  def read(path,*args,**kwargs):
   text=original(path,*args,**kwargs)
   try:rel=str(path.relative_to(ROOT))
   except ValueError:return text
   if path.suffix=='.json'and(rel.startswith('corpus/')or rel=='registry/persons.json'):
    return json.dumps(rewrite(json.loads(text)),ensure_ascii=False)
   return text
  with patch.object(Path,'read_text',read):self.assertEqual(errors(rewrite(self.ch),ROOT),[])
if __name__=='__main__':unittest.main()
