import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables,table_family_path_errors,table_evidence_errors
from scripts.person_bundle import bundle,load_catalog
from scripts.person_ids import family_path_errors

ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text())
class HanNativeIntegration(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(ROOT);cls.table=cls.tables['hanshu-016'];cls.claims=load('corpus/hanshu/016-assertions.json')['assertions'];cls.people={p['id']:p for p in load('registry/persons.json')['persons']};cls.catalog=load_catalog(ROOT)
 def test_partial_original_row_retains_all_headers_and_no_invented_year(self):
  t=self.table;self.assertEqual(t['source']['text_scope'],'partial_table');self.assertFalse(t['source']['image_verified']);self.assertEqual(t['fragments'][0]['source_header'],['號謚姓名','矦狀戶數','始封','位次','子','孫','曾孫','玄孫']);row=t['fragments'][0]['rows'][0];self.assertIsNone(row['year']);self.assertEqual(len(row['cells']),8);self.assertEqual({c['source_row']for c in row['cells']},{69});self.assertEqual(row['cells'][6]['text'],'曾孫');self.assertEqual(row['cells'][6]['person_mentions'],[])
 def test_explicit_generation_claims_never_make_jie_the_grandsons_father(self):
  pairs={(a['subject_person_id'],a['predicate'],a['object_person_id'])for a in self.claims};self.assertIn(('d7u_bgr_wdi_A','father','d7u_bgr_wdi'),pairs);self.assertIn(('d7u_bgr_wdi_*A','grandfather','d7u_bgr_wdi'),pairs);self.assertFalse(any(a['subject_person_id']=='d7u_bgr_wdi_*A'and a['predicate']=='father'for a in self.claims));self.assertEqual(next(a for a in self.claims if a['predicate']=='ancestor')['qualifiers']['generation_distance'],4)
 def test_every_native_family_path_is_bound_to_the_same_assertion_and_original_cells(self):
  for pid in ['d7u_bgr_wdi_A','d7u_bgr_wdi_*A','d7u_bgr_wdi_***A']:
   path=self.people[pid]['family_path'];self.assertEqual(family_path_errors(pid,path),[]);self.assertEqual(table_family_path_errors(pid,path,self.tables,self.claims),[])
  path=copy.deepcopy(self.people['d7u_bgr_wdi_*A']['family_path']);path['intermediate_person_ids']=['d7u_bgr_wdi_A'];self.assertTrue(table_family_path_errors('d7u_bgr_wdi_*A',path,self.tables,self.claims))
 def test_family_path_cannot_borrow_a_different_generation_or_assertion(self):
  pid='d7u_bgr_wdi_***A';path=copy.deepcopy(self.people[pid]['family_path']);path['generation_distance']=2;self.assertTrue(table_family_path_errors(pid,path,self.tables,self.claims));path=copy.deepcopy(self.people[pid]['family_path']);path['source_assertion_id']=self.claims[0]['id'];self.assertTrue(table_family_path_errors(pid,path,self.tables,self.claims))
 def test_bundle_exposes_both_native_sources_and_received_spelling_variants(self):
  b=bundle('d7u_bgr_wdi_*A',catalog=self.catalog);self.assertEqual({o['table_id']for o in b['table_occurrences']},{'shiji-018','hanshu-016'});self.assertTrue(any(o['surface']=='皇柔'for o in b['table_occurrences']));self.assertTrue(any(o['surface']=='皋柔'for o in b['table_occurrences']));self.assertEqual(b['name_components'][0]['surname'],None);self.assertEqual(b['name_components'][0]['ming'],'皇柔')
 def test_shared_emperor_and_general_profiles_keep_explicit_han_source_scope(self):
  for pid in ['yqp_nlb_p1p_AC','yqp_nlb_p1p_ACA','acg_se3_w5x','ob7_g6i_7pp']:
   p=load('data/corpus/profiles/'+pid+'.json');rows=[x for x in p['table_occurrences']if x['table_id']=='hanshu-016'];self.assertTrue(rows);self.assertTrue(all(x['work_id']=='w-hanshu'and x['book_id']=='b-hanshu-016'and x['chapter_id']=='table-chapter-hanshu-016'for x in rows))
 def test_han_catalog_embeds_the_table_without_a_synthetic_paragraph_file(self):
  entry=next(x for x in load('data/corpus/hanshu/index.json')['chapters']if x['book_id']=='b-hanshu-016');self.assertEqual(entry['available'],'table');self.assertEqual(entry['table_id'],'hanshu-016');self.assertEqual(entry['text_scope'],'partial_table');self.assertNotIn('path',entry);self.assertFalse((ROOT/'corpus/hanshu/016.json').exists())
if __name__=='__main__':unittest.main()
