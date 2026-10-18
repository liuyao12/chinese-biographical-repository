# coding: utf-8
import json,unittest
from pathlib import Path
from scripts.person_bundle import bundle
ROOT=Path(__file__).resolve().parents[1]
class ZhangFamilyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
 def test_known_father_and_son_form_three_generations_without_fake_missing_nodes(self):
  self.assertEqual(self.people['1ex_se1_yef_A']['family_path']['parent_person_id'],'1ex_se1_yef')
  self.assertEqual(self.people['1ex_se1_yef_AA']['family_path']['parent_person_id'],'1ex_se1_yef_A')
  self.assertNotIn('family_path',self.people['1ex_se1_yef']);self.assertIn('未名',self.people['1ex_se1_yef']['label'])
 def test_zhang_anshi_is_not_the_liu_prince_with_the_same_given_name(self):
  z=bundle('1ex_se1_yef_AA');self.assertEqual(z['person_ids'],['1ex_se1_yef_AA'])
  self.assertIn('yqp_nlb_p1p_ACAGCA',self.people);self.assertNotEqual(self.people['yqp_nlb_p1p_ACAGCA']['family_path']['parent_person_id'],'1ex_se1_yef_A')
  chapter_ids={p['chapter_id'] for p in z['passages']};self.assertIn('c-shiji-112-pingjin',chapter_ids);self.assertIn('c-hanshu-059-zhangtang',chapter_ids)
 def test_courtesy_name_and_title_have_explicit_source_and_separate_components(self):
  b=bundle('1ex_se1_yef_AA');n=next(n for n in b['name_components'] if n['person_id']=='1ex_se1_yef_AA');self.assertEqual((n['title'],n['surname'],n['ming'],n['zi']),('富平侯','張','安世','子孺'));self.assertIn('安世字子孺',n['quote']);self.assertIn('其封安世為富平侯',n['quote'])
 def test_mother_is_preserved_without_inventing_a_marriage(self):
  b=bundle('1ex_se1_yef_A');relations=b['preferred_relations'];self.assertTrue(any(x['subject_person_id']=='1ex_se1_yef_A' and x['predicate']=='mother' and x['object_person_id']=='5ha_kdu_ux1' for x in relations));self.assertFalse(any(x['predicate']=='spouse' and {x['subject_person_id'],x['object_person_id']}=={'1ex_se1_yef','5ha_kdu_ux1'} for x in relations))
 def test_retired_ids_are_absent_from_every_live_reference_and_public_json(self):
  old=['04o_yps_sg0','04o_yps_sg0_A','3e6_5sg_v5w']
  for folder in ['corpus','registry','data/corpus','exports']:
   for p in (ROOT/folder).rglob('*'):
    if p.is_file() and p.suffix in ['.json','.xml','.md']:
     text=p.read_text();self.assertFalse(any(i in text for i in old),str(p))
  for pid in old:
   self.assertNotIn(pid,self.people);self.assertFalse((ROOT/'exports/persons'/f'{pid}.json').exists());self.assertFalse((ROOT/'data/corpus/profiles'/f'{pid}.json').exists())
