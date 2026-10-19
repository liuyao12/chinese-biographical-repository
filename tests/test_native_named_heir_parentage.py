import unittest,json,copy,importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from scripts.chuji_parentage import chuji_parentage_valid

def read(p):return json.loads(p.read_text())
class NamedHeirTests(unittest.TestCase):
 def setUp(self):
  self.c=read(ROOT/'corpus/jinshu/065.json');self.ps={p['id']:(self.c['id'],p) for p in self.c['paragraphs']};all_rel=read(ROOT/'corpus/jinshu/065-assertions.json')['assertions'];self.aa=[a for a in all_rel if a.get('qualifiers',{}).get('adoption_basis')=='named_younger_brother_son_as_heir'];bio_ids={a['qualifiers']['biological_father_assertion_id'] for a in self.aa};self.bs=[a for a in all_rel if a['id'] in bio_ids]
 def check(self,a=None,ps=None,bs=None):return chuji_parentage_valid(a or self.aa[0],ps or self.ps,self.bs if bs is None else bs)
 def test_both_real_units_and_biological_fathers_retained(self):
  for a in self.aa:
   self.assertTrue(self.check(a));bf=next(b for b in self.bs if b['id']==a['qualifiers']['biological_father_assertion_id']);self.assertNotEqual(bf['object_person_id'],a['object_person_id']);self.assertNotEqual(bf['subject_person_id'],bf['object_person_id'])
 def test_missing_biological_father_rejected(self):self.assertFalse(self.check(bs=[]))
 def test_adoptive_father_cannot_replace_biological_father(self):
  b=copy.deepcopy(self.bs);b[0]['object_person_id']=self.aa[0]['object_person_id'];self.assertFalse(self.check(bs=b))
 def test_wrong_child_and_owner_rejected(self):
  a=copy.deepcopy(self.aa[0]);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(self.check(a))
 def test_title_succession_is_not_adoption(self):
  a=copy.deepcopy(self.aa[0]);a['qualifiers']['source_term']='襲導爵';self.assertFalse(self.check(a))
 def test_ritual_service_is_not_adoption(self):
  a=copy.deepcopy(self.aa[0]);a['qualifiers']['source_term']='命他族奉祀';self.assertFalse(self.check(a))
 def test_other_brother_distance_not_silently_accepted(self):
  a=copy.deepcopy(self.aa[0]);a['qualifiers']['source_term']='以從弟恬子琨爲嗣';self.assertFalse(self.check(a))
 def test_uncited_or_partial_quote_rejected(self):
  a=copy.deepcopy(self.aa[0]);a['evidence'][0]['quote']=a['qualifiers']['source_term'];self.assertFalse(self.check(a))
 def test_unresolved_anchor_rejected(self):
  ps=copy.deepcopy(self.ps);a=self.aa[0];p=ps[a['evidence'][0]['paragraph_id']][1];m=next(m for m in p['mentions'] if m['id']==a['evidence'][0]['object_person_mention_id']);m['kind']='unresolved';m['person_id']=None;self.assertFalse(self.check(ps=ps))
 def test_missing_childlessness_not_adopted_as_same_formula(self):
  a=copy.deepcopy(self.aa[0]);ps=copy.deepcopy(self.ps);p=ps[a['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('無子','有子',1);a['evidence'][0]['quote']=p['text'];bs=copy.deepcopy(self.bs);bs[0]['evidence'][0]['quote']=p['text'];self.assertFalse(self.check(a,ps,bs))
 def test_wrong_biological_father_anchor_rejected(self):
  bs=copy.deepcopy(self.bs);bs[0]['evidence'][0]['object_person_mention_id']=self.aa[0]['evidence'][0]['object_person_mention_id'];self.assertFalse(self.check(bs=bs))
 def test_modern_legal_effect_not_inferred(self):
  a=copy.deepcopy(self.aa[0]);a['qualifiers']['modern_legal_status']='confirmed';self.assertFalse(self.check(a))
 def test_full_source_title_succession_near_match_rejected(self):
  a=copy.deepcopy(self.aa[0]);ps=copy.deepcopy(self.ps);bs=copy.deepcopy(self.bs);p=ps[a['evidence'][0]['paragraph_id']][1];old=a['qualifiers']['source_term'];term=old.replace('爲嗣','襲爵');p['text']=p['text'].replace(old,term);a['qualifiers']['source_term']=term;a['evidence'][0]['quote']=p['text'];bs[0]['evidence'][0]['quote']=p['text'];self.assertFalse(self.check(a,ps,bs))
 def test_full_source_ritual_service_near_match_rejected(self):
  a=copy.deepcopy(self.aa[0]);ps=copy.deepcopy(self.ps);bs=copy.deepcopy(self.bs);p=ps[a['evidence'][0]['paragraph_id']][1];old=a['qualifiers']['source_term'];term=old.replace('爲嗣','奉祀');p['text']=p['text'].replace(old,term);a['qualifiers']['source_term']=term;a['evidence'][0]['quote']=p['text'];bs[0]['evidence'][0]['quote']=p['text'];self.assertFalse(self.check(a,ps,bs))
 def test_digital_heading_cannot_supply_adoption(self):
  ps=copy.deepcopy(self.ps);p=ps[self.aa[0]['evidence'][0]['paragraph_id']][1];p['text_layer']='digital_editorial_heading';self.assertFalse(self.check(ps=ps))
if __name__=='__main__':unittest.main(verbosity=2)
