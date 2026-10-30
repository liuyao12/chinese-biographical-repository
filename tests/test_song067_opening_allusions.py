"""Finite full-unit source regressions; stable source MID roles, no PID whitelist."""
from pathlib import Path
import unittest,json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];CID='c-songshu-067-xielingyun';SLOTS={'chisong':['m00082','m00228'],'yao':['m00058','m00187'],'wenzhong':['m00094','m00242']}
class Song067OpeningAllusions(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/067-xielingyun.json').read_text());cls.p=next(p for p in cls.c['paragraphs']if p['id']==CID+':p006');cls.ref=json.loads((R/'source-evidence/song067-opening-allusions-reading.json').read_text());cls.roles={}
  for role,s in cls.ref['seed_roles'].items():
   ch=json.loads((R/s['path']).read_text());cls.roles[role]=next(m['person_id']for q in ch['paragraphs']for m in q['mentions']if m['id']==s['mention_id'])
  cls.people={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']}
 def test_six_actual_source_anchors_and_reverses(self):
  for role,slots in SLOTS.items():
   for suffix in slots:
    m=next(m for m in self.p['mentions']if m['id']==self.p['id']+':'+suffix);self.assertEqual((m['kind'],m['person_id']),('person',self.roles[role]));self.assertEqual(self.p['text'][m['start']:m['end']],m['surface']);self.assertTrue(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in self.people[self.roles[role]]['aliases']));self.assertTrue(any(e['mention_id']==m['id']and e['chapter_id']==CID and e['paragraph_id']==self.p['id']and e['quote']==m['surface']for e in self.people[self.roles[role]]['evidence']))
 def test_same_self_commentary_specific_bridges(self):
  t=self.p['text'][:291];self.assertIn('文成張良却粒',t);self.assertIn('赤松子遊陶朱范蠡',t);self.assertIn('語文種',t);self.assertIn('二賢既權榮素',t);self.assertTrue(self.p['text'][291:].startswith('若夫巢穴'))
 def test_preserved_already_correct_roles_and_unresolved_boundaries(self):
  for suffix in ('m00075','m00216','m00218','m00087','m00232','m00234','m00263','m00270'):
   m=next(m for m in self.p['mentions']if m['id']==self.p['id']+':'+suffix);self.assertEqual(m['kind'],'person')
  for suffix in ('m00051','m00185','m00249'):self.assertEqual(next(m['kind']for m in self.p['mentions']if m['id']==self.p['id']+':'+suffix),'unresolved')
 def test_retirement_source_qualification_and_no_live_alias(self):
  old='eea_4d1_915';self.assertNotIn(old,self.people);r=json.loads((R/'source-evidence/song067-opening-allusions/retirement-wenzhong-source-person.json').read_text());self.assertEqual(set(r),{'record_type','identity_decision_id','retired_person_ids','retirement_policy','person_aliases_created'});self.assertEqual(r['retired_person_ids'],[old]);self.assertFalse(r['person_aliases_created']);d=json.loads((R/'corpus/songshu/067-opening-allusion-identities.json').read_text());a=next(x for x in d['decisions']if x['id']==r['identity_decision_id']);self.assertEqual(a['person_id'],self.roles['wenzhong']);self.assertTrue(a['prior_source_qualifications'])
 def test_legendary_and_inherited_source_qualifications_unchanged(self):
  self.assertEqual(self.people[self.roles['chisong']]['historicity'],'legendary_tradition');self.assertEqual(self.people[self.roles['yao']]['historicity'],'legendary_tradition');self.assertEqual(self.c['source']['base_edition'],'WYG');self.assertFalse(self.c['source']['image_verified']);self.assertFalse(self.ref['human_reviewed'])
 def test_xml_exact_text_no_new_source_words(self):
  x=ET.parse(R/'corpus/songshu/067-xielingyun.xml').getroot();self.assertEqual([''.join(p.itertext())for p in x.findall('p')],[p['text']for p in self.c['paragraphs']])
if __name__=='__main__':unittest.main()
