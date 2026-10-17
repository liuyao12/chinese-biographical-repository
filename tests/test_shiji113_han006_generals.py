# coding: utf-8
import json, unittest, hashlib
from scripts.date_ranges import parallel_event_date
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
class Han006NanyueGenerals(unittest.TestCase):
 def test_existing_six_source_paragraphs_and_fixed_revision_preserved(self):
  new=load('corpus/hanshu/006.json');old_six=json.dumps(new['paragraphs'][:-1],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();self.assertEqual(hashlib.sha256(old_six).hexdigest(),'d8a36f35159b34bbd7441d96203fba983feef60d8543c8515fe42de421c6c12f');self.assertEqual(new['source']['revision_id'],2631854);self.assertEqual(len(new['paragraphs']),7)
 def test_five_precise_name_spans_reuse_existing_ids(self):
  p=load('corpus/hanshu/006.json')['paragraphs'][-1];self.assertTrue(p['id'].endswith('p133'));self.assertEqual([(m['surface'],m['person_id'])for m in p['mentions']],[('路博德','vib_10x_51n'),('楊僕','jk8_8gt_vmi'),('嚴','4zn_n9v_k0v'),('甲','iw9_udd_jr2'),('遺','dzl_mvt_l93')]);self.assertTrue(all(p['text'][m['start']:m['end']]==m['surface']for m in p['mentions']))
 def test_single_names_have_no_invented_surname(self):
  names={x['person_id']:x for x in load('data/corpus/profile-names.json')['records']}
  for pid,name in [('4zn_n9v_k0v','嚴'),('iw9_udd_jr2','甲'),('dzl_mvt_l93','遺')]:self.assertEqual(names[pid]['ming'],name);self.assertIsNone(names[pid]['surname']);self.assertFalse(names[pid]['human_reviewed'])
 def test_cross_work_decisions_keep_both_sources_and_variant(self):
  ds=[d for d in load('corpus/shiji/113-identities.json')['decisions']if d['id'].startswith('d-shiji113-han006-')];self.assertEqual(len(ds),3)
  for d in ds:self.assertEqual({e['work_id']for e in d['evidence']},{'w-shiji','w-hanshu'});self.assertFalse(d['references'][0]['image_verified']);self.assertIn('683113d4baf6febecaf2ccb7913df87c4d68d454',d['references'][0]['url'])
  n=next(x for x in load('data/corpus/profile-names.json')['records']if x['person_id']=='iw9_udd_jr2');self.assertIn('下厲將軍',n['additional_names']);self.assertEqual(n['title'],'下瀨將軍')
 def test_grants_are_distinct_from_attestations_and_not_falsely_dated(self):
  hs=load('corpus/hanshu/006-titles.json')['holdings'];self.assertEqual(len(hs),6);self.assertEqual([h['title']for h in hs if h['mode']=='grant'],['戈船將軍','下瀨將軍'])
  for h in hs:
   self.assertIsNone(h['effective_period']['start']['date_expression']);self.assertTrue('normalized_date'not in h['effective_period']['start']or parallel_event_date(h['effective_period']['start']['normalized_date']));self.assertEqual(h['effective_period']['end']['status'],'unknown');self.assertTrue(all(e['chapter_id']=='c-hanshu-006-wudi'for e in h['evidence']))
 def test_posthumous_names_require_explicit_death_and_naming(self):
  hs=[h for h in load('corpus/shiji/113-titles.json')['holdings']if h['id']in ['th-shiji113-032','th-shiji113-033']];self.assertEqual(len(hs),2)
  for h in hs:self.assertEqual(h['mode'],'posthumous_naming');self.assertIn(h['naming_basis']['source_term'],h['evidence'][0]['quote']);self.assertEqual(h['effective_period']['start']['event_type'],'posthumous_naming');self.assertEqual(h['effective_period']['end']['status'],'unknown')
 def test_locality_does_not_become_birthplace_or_modern_coordinate(self):
  ds=[a for a in load('corpus/shiji/113-addresses.json')['assertions']if a['id']in ['pa-shiji113-002','pa-shiji113-003','pa-shiji113-004']];self.assertEqual([a['place']['source_name']for a in ds],['霸陵','邯鄲','郟'])
  for a in ds:self.assertIsNone(a['place']['modern_identification']);self.assertNotEqual(a['relation'],'birth_place');self.assertIn(a['source_term'],a['evidence'][0]['quote'])
  self.assertEqual(ds[-1]['relation'],'source_locality_designation');self.assertIsNone(ds[-1]['qualifiers']['origin_or_residence'])
if __name__=='__main__':unittest.main()
