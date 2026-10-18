import copy,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
class JiZhengCoreIdentitiesTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=read('corpus/shiji/120.json')
  cls.paragraphs={p['id']:p for p in cls.chapter['paragraphs']}
  cls.people={p['id']:p for p in read('registry/persons.json')['persons']}
 def test_emperor_accession_and_later_historical_recollection_stay_separate(self):
  first=self.paragraphs['c-shiji-120-jizheng:p001']
  self.assertEqual({m['person_id'] for m in first['mentions'] if m['surface'] in ['孝景','孝景帝']},{'yqp_nlb_p1p_ACA'})
  self.assertEqual({m['person_id'] for m in first['mentions'] if m['surface'] in ['太子','上']},{'yqp_nlb_p1p_ACAA'})
  ancestors=self.paragraphs['c-shiji-120-jizheng:p015']
  self.assertTrue(any(m['surface']=='高祖' and m['person_id']!='yqp_nlb_p1p_ACAA' for m in ancestors['mentions']))
  self.assertTrue(any(m['surface']=='孝文' and m['person_id']!='yqp_nlb_p1p_ACAA' for m in ancestors['mentions']))
 def test_sister_subject_is_the_queen_without_reversing_the_recorded_order(self):
  a=next(a for a in read('corpus/shiji/120-assertions.json')['assertions'] if a['id']=='a-shiji120-003')
  self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('l5c_h8i_d5q','sister','5dd_l1c_6g8'))
  order=a['qualifiers']['relative_birth_order']
  self.assertEqual((order['older_person_id'],order['younger_person_id']),('l5c_h8i_d5q','5dd_l1c_6g8'))
  self.assertIsNone(order['older_ordinal']);self.assertIsNone(order['younger_ordinal'])
  self.assertEqual(a['qualifiers']['source_term'],'姊')
  self.assertIn('姊為皇后',a['evidence'][0]['quote'])
 def test_queen_identification_has_explicit_enthronement_evidence(self):
  decisions=read('corpus/shiji/120-identities.json')['decisions']
  queen=next(d for d in decisions if d['person_id']=='l5c_h8i_d5q')
  self.assertTrue(any(e['paragraph_id']=='c-shiji-111-wei-huo:p001' and '姊衛子夫' in e['quote'] for e in queen['evidence']))
  self.assertTrue(any(e['paragraph_id']=='c-shiji-111-wei-huo:p005' and '立為皇后' in e['quote'] for e in queen['evidence']))
 def test_alternative_sibling_chronology_remains_a_source_claim(self):
  pair={'l5c_h8i_d5q','5dd_l1c_6g8'};claims=[]
  for n in ['111','120','126']:
   for a in read('corpus/shiji/'+n+'-assertions.json')['assertions']:
    if {a.get('subject_person_id'),a.get('object_person_id')}==pair:
     o=a.get('qualifiers',{}).get('relative_birth_order')
     if o:claims.append((n,o['older_person_id']))
  self.assertIn(('120','l5c_h8i_d5q'),claims)
  self.assertIn('5dd_l1c_6g8',{older for _,older in claims})
 def test_six_profiles_include_the_original_chapter_without_nlu(self):
  for pid in ['yqp_nlb_p1p_ACA','yqp_nlb_p1p_ACAA','7mz_d13_9ka_A','5dd_l1c_6g8','l5c_h8i_d5q','yqp_nlb_p1p_AFA']:
   p=read('data/corpus/profiles/'+pid+'.json')
   self.assertTrue(any(o['work_id']=='w-shiji' and o['chapter_id']=='c-shiji-120-jizheng' for o in p['occurrences']),pid)
 def test_retired_source_candidates_leave_no_registry_bundle_or_profile(self):
  for pid in ['kkh_kew_u6x','fu0_u16_g5t','6rp_jqd_p41','rm3_ef6_d55','2yf_ieu_fah','zt9_d8y_inq']:
   self.assertNotIn(pid,self.people)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
 def test_adjective_zhuang_and_office_taizi_xima_are_not_person_names(self):
  p=self.paragraphs['c-shiji-120-jizheng:p001']
  for text in ['以莊見憚','太子洗馬']:
   start=p['text'].index(text);end=start+len(text)
   self.assertFalse(any(m['kind']=='person' and max(start,m['start'])<min(end,m['end']) for m in p['mentions']))
 def test_appended_suoyin_narrative_layer_is_preserved(self):
  p=self.paragraphs['c-shiji-120-jizheng:p021']
  self.assertEqual(p['text_layer'],'witness_appended_suoyin_zan')
  self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='天子'),'yqp_nlb_p1p_ACAA')
 def test_queen_profile_uses_attested_title_house_and_zi_without_a_given_name(self):
  names=read('data/corpus/profile-names.json')['records']
  n=next(n for n in names if n['person_id']=='l5c_h8i_d5q')
  self.assertEqual((n['title'],n['surname'],n['ming'],n['zi']),('皇后','衛',None,'子夫'))
  self.assertIn('字子夫',n['quote']);self.assertIn('家號曰衛氏',n['quote'])
  from scripts.person_bundle import validate_courtesy_name
  validate_courtesy_name(n)
  bad=copy.deepcopy(n);bad['ming']=bad['zi']
  with self.assertRaises(ValueError):validate_courtesy_name(bad)
 def test_empress_spouse_claim_does_not_turn_installation_year_into_marriage_date(self):
  aid='a-shiji111-wei-empress-spouse'
  a=next(a for a in read('corpus/shiji/111-assertions.json')['assertions'] if a['id']==aid)
  self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('l5c_h8i_d5q','spouse','yqp_nlb_p1p_ACAA'))
  self.assertEqual(a['qualifiers'],{'source_term':'立為皇后'})
  self.assertIn('衛夫人有男，立為皇后。',a['evidence'][0]['quote'])
  for pid in [a['subject_person_id'],a['object_person_id']]:
   p=read('data/corpus/profiles/'+pid+'.json')
   self.assertTrue(any(r['id']==aid for r in p['relations']))
if __name__=='__main__':unittest.main()
