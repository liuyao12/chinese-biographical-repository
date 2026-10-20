# coding: utf-8
from pathlib import Path
import json,hashlib,unittest
R=Path(__file__).resolve().parents[1]
class Song041ParentsSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/041-parents.json').read_text());cls.c1=json.loads((R/'corpus/songshu/001-parents-reference.json').read_text());cls.ps={p['id']:p for c in(cls.c,cls.c1)for p in c['paragraphs']};cls.reg={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']}
 def test_complete_two_units_keep_source_name_and_all_positions(self):
  self.assertEqual(sum(len(p['mentions'])for p in self.c1['paragraphs']),8);self.assertEqual(sum(len(p['mentions'])for p in self.c['paragraphs']),72)
  self.assertEqual([len(p['text'])for p in self.c['paragraphs']],[321,425]);self.assertTrue(self.c['paragraphs'][0]['text'].startswith('孝穆趙皇后諱安下邳僮人也'))
  self.assertNotIn('安宗',self.c['paragraphs'][0]['text']);self.assertEqual(self.c['source']['revision_id'],'e80c057667e3c8684f11d5088251e10244d5a264')
  for c in(self.c,self.c1):
   self.assertEqual(hashlib.sha256((R/c['source']['raw_path']).read_bytes()).hexdigest(),c['source']['raw_file_sha256'])
   lines=(R/c['source']['raw_path']).read_text().splitlines()
   for p in c['paragraphs']:
    self.assertEqual(len(p['text']),len(p['source_position']['raw_character_positions']))
    for ch,pos in zip(p['text'],p['source_position']['raw_character_positions']):self.assertEqual(lines[pos['line']-1][pos['column']],ch)
    end=0
    for m in p['mentions']:
     self.assertGreaterEqual(m['start'],end);end=m['end'];self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
 def test_adopted_parent_identity_names_and_independent_birth_role(self):
  f=self.reg['fd4_ult_nsi'];m=self.reg['ntw_hsm_9iv'];self.assertEqual(f['label'],'翹〔孝皇帝；高祖之父〕');self.assertEqual(m['label'],'趙安〔孝穆皇后；本見證，高祖之母〕')
  mother=json.loads((R/'corpus/songshu/041-parents-assertions.json').read_text())['assertions'][0];self.assertEqual(mother['predicate'],'mother');self.assertEqual(mother['object_person_id'],m['id']);self.assertEqual(mother['qualifiers']['source_term'],'生高祖其日后以産疾殂')
  father=json.loads((R/'corpus/songshu/001-parents-reference-assertions.json').read_text())['assertions'][0];self.assertEqual(father['predicate'],'father');self.assertEqual(father['qualifiers']['source_term'],'翹是為皇考')
  names=json.loads((R/'corpus/songshu/001-parents-reference-name-components.json').read_text())['records'];self.assertIsNone(names[0]['surname']);self.assertEqual(names[0]['ming'],'翹')
  self.assertFalse(any(a['surface']in('劉翹','趙安宗','安宗')for p in(f,m)for a in p['aliases']))
 def test_birth_dates_are_two_typed_proposals_not_month_day_reconciliation(self):
  case=json.loads((R/'source-evidence/song041-parents/birth-date-disagreement.json').read_text());self.assertEqual(case['common_chinese_civil_year'],363);self.assertIsNone(case['preferred_claim_id']);self.assertEqual(len(case['claims']),2)
  self.assertEqual({c['year']for c in case['claims']},{363});self.assertTrue(any('三月壬寅'in c['date_expression']for c in case['claims']));self.assertTrue(any('四月二日'in c['date_expression']for c in case['claims']))
  self.assertTrue(all(c['status']=='typed_proposal_not_native'for c in case['claims']))
 def test_all_other_proposals_have_exact_source_and_are_not_consumed(self):
  proposals=json.loads((R/'source-evidence/song041-parents/typed-proposals.json').read_text());self.assertEqual(proposals['native_status'],'NOT_CONSUMED');self.assertGreaterEqual(len(proposals['records']),125)
  for r in proposals['records']:
   e,=r['evidence'];p=self.ps[e['paragraph_id']];a=r['source_anchor'];self.assertEqual(e['quote'],p['text']);self.assertEqual(p['text'][a['start']:a['end']],r['source_term']);self.assertEqual(a['surface'],r['source_term'])
   self.assertNotIn(r['status'],('source_attested','editorial_preferred'))
 def test_lingwen_candidates_not_merged_and_fanzhong_primary_reference(self):
  u=self.c['annotation']['unresolved_identity_cases'][0];self.assertEqual(u['candidate_person_ids'],['9zj_vf7_86a','fdi_2l0_u1g']);self.assertIn('9zj_vf7_86a',self.reg);self.assertIn('fdi_2l0_u1g',self.reg)
  receipt=json.loads((R/'source-evidence/song041-parents/shouzhang-primary-reading.json').read_text());self.assertEqual(hashlib.sha256((R/receipt['path']).read_bytes()).hexdigest(),receipt['sha256']);self.assertIn('十五年定封宏夀張侯',receipt['complete_read_narrative']);self.assertIn('祠重墓追爵諡為夀張敬侯',receipt['complete_read_narrative']);self.assertEqual(receipt['role'],'identity_reference_only_not_imported_houhan_chapter')
if __name__=='__main__':unittest.main()
