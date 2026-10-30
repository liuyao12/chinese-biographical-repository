import unittest,json,copy,os
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_jin035_peixiu_peiwei_registration import errors,guard_bundle
from scripts.fixed_jin035_contemporary import FIRST_PERSON,source_first_person
from scripts.person_mentions import is_person_reference,pronoun_errors
from scripts.person_bundle import load_catalog,bundle
from scripts.render_corpus import render
ROOT=Path(os.environ.get('CBR_CONTEMPORARY_TEST_ROOT',Path(__file__).resolve().parents[1]));CH='corpus/jinshu/035-peixiu-peiwei.json'
class ContemporarySuccessor(unittest.TestCase):
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
 def first(self):return next((p,m)for p in self.ch['paragraphs']for m in p['mentions']if m['kind']=='pronoun')
 def test_normal_source_and_finite_counts(self):
  self.assertEqual(errors(self.ch,ROOT),[]);ms=[m for p in self.ch['paragraphs']for m in p['mentions']];self.assertEqual(len(ms),252);self.assertEqual(sum(m['kind']=='pronoun'for m in ms),6);self.assertEqual(sum(m['kind']=='unresolved'for m in ms),23)
 def test_first_person_not_alias_or_xml_person_name(self):
  xml=render(self.ch)
  for p in self.ch['paragraphs']:
   for m in p['mentions']:
    if m['kind']!='pronoun':continue
    self.assertTrue(source_first_person(m,p['text']));self.assertTrue(is_person_reference(m));self.assertEqual(pronoun_errors(m,p['text']),[]);self.assertIn('<seg id="'+m['id']+'" type="pronoun"',xml);self.assertNotIn('<persName id="'+m['id']+'"',xml);self.assertFalse(any(m['id']in a['mention_ids']for v in self.people.values()for a in v['aliases']))
 def test_other_first_person_not_globally_permitted(self):
  p,m=self.first();m=copy.deepcopy(m);m['id']='unowned:mid';self.assertFalse(is_person_reference(m));self.assertTrue(pronoun_errors(m,p['text']));p,m=self.first();self.assertTrue(pronoun_errors(m,p['text']+'改'))
 def test_first_person_promoted_to_name_rejected(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['kind']=='pronoun');m['kind']='person'
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_first_person_wrong_speaker_rejected(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['kind']=='pronoun');m['person_id']='kbq_kjc_n2f_AAB'
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_alias_injection_rejected(self):
  p,m=self.first();reg=json.loads((ROOT/'registry/persons.json').read_text());person=next(p for p in reg['persons']if p['id']==m['person_id']);person['aliases'].append({'surface':m['surface'],'mention_ids':[m['id']]})
  with self.altered({'registry/persons.json':reg}):self.assertTrue(errors(self.ch,ROOT))
 def test_orphan_retains_two_candidates_and_no_selected_identity(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='遺孤');self.assertIsNone(m['person_id']);self.assertEqual(len(m['candidate_person_ids']),2);m.update(person_id=m['candidate_person_ids'][0],kind='person',status='contextual_provisional')
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_original_parent_family_guard_remains(self):
  rel='corpus/jinshu/035-peixiu-peiwei-assertions.json';d=json.loads((ROOT/rel).read_text());a=d['assertions'][0];a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
  with self.altered({rel:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_original_source_truncation_rejected(self):
  ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['text']=ch['paragraphs'][0]['text'][:-1]
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_caller_catalog_and_reverse_omission_rejected(self):
  records=[r for r in self.records if not(r.get('record_type')=='identity_decision_set'and any(d.get('id','').startswith('d-jin035-contemporary')for d in r.get('decisions',[])))]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,'kbq_kjc_n2f_AA',self.people,records)
  people=copy.deepcopy(self.people);p,m=self.first();people[m['person_id']]['evidence']=[e for e in people[m['person_id']]['evidence']if e['mention_id']!=m['id']]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,m['person_id'],people,self.records)
 def test_normal_API_keeps_six_first_person_passage_references(self):
  for pid in ['hgm_jvn_hle','kbq_kjc_n2f_AA','kbq_kjc_n2f_AAB','op5_nwa_729']:
   out=bundle(pid,root=ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertEqual(out['canonical_person_id'],pid)
   for p in self.ch['paragraphs']:
    for m in p['mentions']:
     if m['kind']=='pronoun'and m['person_id']==pid:self.assertTrue(any(m['id']==mm['id']and mm['kind']=='pronoun'for passage in out['passages']for pp in passage.get('paragraphs',[])for mm in pp['mentions'])or any(m['id']==mm['id']and mm['kind']=='pronoun'for passage in out['passages']for mm in passage.get('mentions',[])))
 def test_coherent_namespace_rekey(self):
  original=Path.read_text
  def rewrite(v):
   if isinstance(v,dict):return{k:rewrite(x)for k,x in v.items()}
   if isinstance(v,list):return[rewrite(x)for x in v]
   return 'zzz_abc_def'if v=='op5_nwa_729'else v
  def read(path,*args,**kwargs):
   s=original(path,*args,**kwargs)
   try:rel=str(path.relative_to(ROOT))
   except ValueError:return s
   if path.suffix=='.json'and(rel.startswith('corpus/')or rel=='registry/persons.json'):return json.dumps(rewrite(json.loads(s)),ensure_ascii=False)
   return s
  with patch.object(Path,'read_text',read):self.assertEqual(errors(rewrite(self.ch),ROOT),[])
if __name__=='__main__':unittest.main()
