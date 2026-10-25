from pathlib import Path
import json,copy,unittest
from scripts.fixed_witness_fact_slots import records,valid,errors
R=Path(__file__).resolve().parents[1];CID='c-jinshu-043-guoshu';KEY='jin043-guoshu-finite'
class GuoshuFacts(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.ch=json.loads((R/'corpus/jinshu/043-guoshu.json').read_text());c.v=records(c.ch,R);c.by={v['fixed_source_fact_binding']['slot']:v for v in c.v};c.ms={m['id']:m for p in c.ch['paragraphs']for m in p['mentions']}
 def test_complete_source_and_no_unresolved_role_fabrication(self):
  self.assertEqual(len(self.ch['paragraphs']),5);self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),116);self.assertEqual(sum(m['kind']=='unresolved'for m in self.ms.values()),3);self.assertTrue(all(valid(v,self.ch,R)for v in self.v));self.assertFalse(any('normalized_date'in v for v in self.v));self.assertFalse(any(v.get('event_type')=='birth'for v in self.v))
 def test_actual_career_and_family_semantic_boundaries(self):
  mother=self.by['guoshu-mother'];self.assertEqual(mother['predicate'],'maternal_role');self.assertIsNone(mother['qualifiers']['biological_mother']);fa=self.by['liufan-father'];self.assertEqual(fa['predicate'],'father');self.assertEqual(fa['subject_person_id'],self.ms[CID+':p001:m0141']['person_id']);self.assertEqual(fa['object_person_id'],self.ms[CID+':p001:m0139']['person_id'])
  titles=[v['title']for v in self.v if 'attestations'in v];self.assertNotIn('右丞',titles);self.assertNotIn('梁州刺史',titles);self.assertNotIn('廷尉',titles);self.assertEqual(self.by['career-07']['appointment_role'],'concurrent');self.assertEqual(self.by['career-07']['title'],'南郡');self.assertFalse(self.by['you-cheng-not-sent']['values']['holding_created']);self.assertFalse(self.by['liangzhou-memorial']['values']['appointment_reported']);self.assertFalse(self.by['unaccepted-duzeng']['values']['service_attested']);self.assertEqual(self.by['name-liufan']['surname'],'劉');self.assertEqual(self.by['name-liufan']['status'],'contextual_provisional');self.assertEqual(self.by['name-liufan']['fixed_biography_name_binding']['mode'],'ming_only')
 def test_coherent_wrong_recipient_and_biological_mother_are_rejected(self):
  v=copy.deepcopy(self.by['career-01']);other=self.ms[CID+':p001:m0065'];old=v['person_id']
  def swap(x):
   if isinstance(x,dict):
    for k,a in x.items():
     if k=='person_id'and a==old:x[k]=other['person_id']
     elif k=='person_mention_id':x[k]=other['id']
     else:swap(a)
   elif isinstance(x,list):
    for a in x:swap(a)
  swap(v);self.assertFalse(valid(v,self.ch,R));m=copy.deepcopy(self.by['guoshu-mother']);m['predicate']='mother';m['qualifiers']['biological_mother']=True;self.assertFalse(valid(m,self.ch,R));ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['text']=ch['paragraphs'][0]['text'].replace('弘子璠','弘從璠');self.assertFalse(valid(self.by['liufan-father'],ch,R))

 def test_inferred_surname_requires_actual_same_source_father_and_not_false_full_name(self):
  from scripts.fixed_biography_names import validate_surname,component_valid
  names=[v for v in self.v if 'fixed_biography_name_binding'in v];a=self.by['liufan-father'];n=self.by['name-liufan'];validate_surname(n,names,{CID:self.ch},[a],R)
  wrong=copy.deepcopy(a);wrong['object_person_id']=self.ms[CID+':p001:m0037']['person_id'];wrong['evidence'][0]['object_person_mention_id']=CID+':p001:m0037'
  with self.assertRaises(ValueError):validate_surname(n,names,{CID:self.ch},[wrong],R)
  fake=copy.deepcopy(n);fake['fixed_biography_name_binding']['mode']='full_name';self.assertFalse(component_valid(fake,self.ch,R,[a]))
