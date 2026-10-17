import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
MAPPING={'y8l_c2q_j7r':'m61_2wu_0ru','f95_kwr_nbs':'466_pwj_snr','qq5_jcs_gh0':'tvb_urc_goi','7g6_yj7_yit':'z9d_qn5_wg8_A'}
def read(p):return json.loads((R/p).read_text())
class ChaoxianNamesAndTable(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.names={n['person_id']:n for n in read('data/corpus/profile-names.json')['records']};cls.t=read('data/historical-tables/shiji-020.json');cls.cells={c['id']:c for f in cls.t['fragments']for row in f['rows']for c in row['cells']}
 def test_man_has_explicit_commentary_surname_not_mechanical_split(self):
  n=self.names['f41_ulg_3u1'];self.assertEqual((n['surname'],n['ming'],n['title']),('衛','滿','朝鮮王'));self.assertTrue(any('姓衛'in r['quote']and '85cc2d3b'in r['url']for r in n['references']))
 def test_luren_is_full_given_name_and_no_invented_surname(self):
  n=self.names['z9d_qn5_wg8'];self.assertIsNone(n['surname']);self.assertEqual(n['ming'],'路人');self.assertTrue(any('路人名也'in r['quote']for r in n['references']))
 def test_chang_preserves_reported_variant_and_received_editorial_form(self):
  n=self.names['f41_ulg_3u1_*AA'];self.assertEqual(n['ming'],'長');self.assertIsNone(n['surname']);self.assertIn('長路',n['additional_names']);self.assertTrue(any('之子名長'in r['quote']for r in n['references']));self.assertIn('長［降］',n['quote'])
 def test_zui_is_not_named_zizui_and_title_variants_remain_sourced(self):
  n=self.names['z9d_qn5_wg8_A'];self.assertEqual(n['ming'],'最');self.assertIsNone(n['surname']);self.assertEqual(n['title'],'溫陽侯');self.assertIn('涅陽侯',n['additional_names']);self.assertTrue(any('也名最'in r['quote']for r in n['references']));self.assertIn('子最',self.cells['shiji-020-t1-r073-c06']['text'])
 def test_four_table_candidates_retired_and_no_old_person_files(self):
  ids={p['id']for p in read('data/historical-tables/person-candidates.json')['persons']}
  for old in MAPPING:self.assertNotIn(old,ids);self.assertFalse((R/'data/corpus/profiles'/f'{old}.json').exists());self.assertFalse((R/'exports/persons'/f'{old}.json').exists())
 def test_five_existing_person_anchors_link_to_chapter_people(self):
  count=0
  for row,pid in [('r066','m61_2wu_0ru'),('r067','466_pwj_snr'),('r068','tvb_urc_goi'),('r073','z9d_qn5_wg8_A')]:
   for m in self.cells['shiji-020-t1-'+row+'-c06']['person_mentions']:self.assertEqual(m['person_id'],pid);self.assertEqual(m['identity_evidence'][0]['person_id'],pid);count+=1
  self.assertEqual(count,5)
 def test_six_merit_person_references_are_precise_not_whole_cells(self):
  count=0
  for row in ['r066','r067','r068','r073']:
   c=self.cells['shiji-020-t1-'+row+'-c01']
   for m in c['person_mentions']:self.assertEqual(c['text'][m['start']:m['end']],m['surface']);self.assertLess(len(m['surface']),len(c['text']));self.assertEqual(m['identity_evidence'][0]['source_revision'],439220);count+=1
  self.assertEqual(count,6)
 def test_luren_and_son_are_separate_in_same_merit_cell(self):
  ms=self.cells['shiji-020-t1-r073-c01']['person_mentions'];self.assertEqual([(m['surface'],m['person_id'])for m in ms],[('路人','z9d_qn5_wg8'),('其子','z9d_qn5_wg8_A')])
 def test_chang_prince_is_separate_from_already_killed_deputy_king(self):
  ps={p['id']for p in read('registry/persons.json')['persons']};self.assertIn('fa5_rxi_3t4',ps);self.assertIn('f41_ulg_3u1_*AA',ps);self.assertNotEqual('fa5_rxi_3t4','f41_ulg_3u1_*AA')
 def test_received_surname_not_propagated_to_rightqu(self):self.assertNotIn('f41_ulg_3u1_*A',self.names)
if __name__=='__main__':unittest.main()
