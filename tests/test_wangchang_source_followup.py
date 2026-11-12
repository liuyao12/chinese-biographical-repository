from pathlib import Path
import unittest,json,copy,hashlib
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1];CID='c-sanguozhi-027-wangchang';PREFIX=CID+':'
class WangSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());cls.by={m['id']:(p,m)for p in cls.c['paragraphs']for m in p['mentions']};cls.review=json.loads((R/'source-evidence/sanguozhi027-wangchang-identity-followup/identity-followup.json').read_text());cls.ids=cls.review['new_source_person_ids'];cls.catalog=load_catalog(R)
 def test_named_anchors_have_reverse_evidence(self):
  self.assertEqual(len(self.review['decisions']),15)
  for row in self.review['decisions']:
   p,m=self.by[row['mention_id']];self.assertEqual(p['text'][row['start']:row['end']],row['surface']);self.assertEqual(m['kind'],'person');self.assertEqual(m['person_id'],row['selected_person_id']);reg=self.catalog[0][m['person_id']];self.assertTrue(any(e.get('mention_id')==m['id']for e in reg['evidence']));self.assertTrue(any(m['id']in a['mention_ids']and a['surface']==m['surface']for a in reg['aliases']))
 def test_no_new_family_title_life_or_name_component_claims(self):
  for pid in self.ids.values():
   p=self.catalog[0][pid];self.assertNotIn('family_path',p);b=bundle(pid,root=R,catalog=self.catalog);self.assertTrue(all(r['id']in ['a-sanguozhi027-wangchang-011','a-sanguozhi027-wangchang-012','a-sanguozhi027-wangchang-013']for r in b['relations']));self.assertEqual(b['title_holdings'],[]);self.assertEqual(b['date_normalizations'],[])
 def test_source_local_shen_reuses_four_positions_but_not_foreign_homonyms(self):
  pids=[self.by[PREFIX+x][1]['person_id']for x in ['unit005:m0039','unit005:m0041','unit018:m0054','unit018:m0059']];self.assertEqual(set(pids),{self.ids['shen']});self.assertNotIn('7r6_k52_qji_ABAAAABA',pids);self.assertNotIn('b2a_88b_095',pids)
 def test_candidates_remain_unresolved_not_identity_equivalence(self):
  cases=self.c['annotation']['unresolved_identity_cases'];self.assertEqual(len([x for x in cases if x['id'].startswith('case-sgz027-')and x['id'].endswith('-source-local')]),3)
  for key in ['mo','shen','guoyi']:
   case=next(x for x in cases if x['id']=='case-sgz027-'+key+'-source-local');self.assertEqual(case['status'],'unresolved');self.assertEqual(len(case['candidate_person_ids']),2);self.assertIn(self.ids[key],case['candidate_person_ids']);self.assertFalse(case['candidate_list_exhaustive']);self.assertFalse(case['human_reviewed'])
 def test_quote_speaker_is_not_zigong(self):
  kong=self.by[PREFIX+'unit007:m0113'][1]['person_id'];zi=self.by[PREFIX+'unit007:m0134'][1]['person_id'];self.assertNotEqual(kong,zi)
  for x in ['unit007:m0116','unit007:m0143']:self.assertEqual(self.by[PREFIX+x][1]['person_id'],kong)
  self.assertEqual(self.by[PREFIX+'unit007:m0138'][1]['person_id'],zi)
 def test_complete_received_words_projections_work_marks_unchanged(self):
  capture=json.loads((R/'source-evidence/sanguozhi027-wangchang-identity-followup/complete-source-reading.json').read_text());self.assertEqual([(p['id'],p['text'],p['text_layer'],p['source_position'])for p in self.c['paragraphs']],[(p['id'],p['text'],p['text_layer'],p['source_position'])for p in capture['paragraphs']]);self.assertEqual(len(self.c['paragraphs']),20);self.assertEqual(sum(m['kind']=='work'for p in self.c['paragraphs']for m in p['mentions']),8)
 def test_new_wei_xumiao_not_eastern_jin_and_guo_groups_distinct(self):
  self.assertNotEqual(self.ids['xumiao'],'1b7_36b_29b');self.assertNotEqual(self.ids['guoyi'],'64e_ce8_aba');ref=json.loads((R/'source-evidence/sanguozhi027-wangchang-identity-followup/parallel-reading.json').read_text());ss=next(x for x in ref['references']if x['path'].endswith('KR3l0002_002-c6c870d.txt'));reading=''.join(x['reading']for x in ss['layout_reconstruction']);self.assertIn('泰業太原陽曲人',reading);self.assertIn('剌史',reading);self.assertNotIn('大業',reading)
 def test_pronominal_refs_are_not_names_or_aliases(self):
  expected='''
  unit002:m0093 unit003:m0015
  unit005:m0005 unit005:m0020 unit005:m0033
  unit007:m0116 unit007:m0143 unit008:m0102 unit010:m0032
  unit011:m0035 unit011:m0067 unit011:m0096 unit011:m0122 unit011:m0127 unit011:m0129
  unit013:m0021 unit013:m0032 unit013:m0040 unit013:m0042 unit013:m0044 unit013:m0049 unit013:m0080 unit013:m0082 unit013:m0084 unit013:m0090
  unit015:m0029 unit015:m0031 unit015:m0033 unit015:m0038
  unit016:m0086 unit016:m0260 unit016:m0311 unit016:m0332 unit016:m0375 unit016:m0414 unit016:m0426 unit016:m0466
  unit017:m0083
  '''.split()
  ids={PREFIX+x for x in expected};self.assertEqual(len(ids),38)
  for mid in ids:
   m=self.by[mid][1];self.assertEqual(m['kind'],'pronoun',mid);self.assertIsInstance(m.get('person_id'),str,mid)
  aliases={mid for person in self.catalog[0].values() for alias in person['aliases'] for mid in alias['mention_ids']}
  self.assertFalse(ids & aliases)
 def test_wangchang_parent_assertions_anchor_the_actual_son_clause(self):
  a={x['id']:x for x in json.loads((R/'corpus/sanguozhi/027-wangchang-assertions.json').read_text())['assertions']}
  for aid,quote in [('a-sanguozhi027-wangchang-003','其子渾字玄冲'),('a-sanguozhi027-wangchang-011','其子渾字玄冲深字道冲')]:
   e=a[aid]['evidence'][0];self.assertEqual(e['object_person_mention_id'],PREFIX+'unit005:m0033');self.assertEqual(e['quote'],quote)
   self.assertEqual(self.by[e['object_person_mention_id']][1]['kind'],'pronoun')
  for aid in ['a-sanguozhi027-wangchang-010','a-sanguozhi027-wangchang-013']:
   e=a[aid]['evidence'][0];self.assertEqual(e['object_person_mention_id'],PREFIX+'unit005:m0005')
   self.assertIn('故兄子黙',e['quote'])
if __name__=='__main__':unittest.main()
