import json,unittest
from pathlib import Path
from scripts.person_bundle import bundle
from scripts.table_evidence import load_tables,table_regnal_range_errors
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class ChaoxianParallelReadings(unittest.TestCase):
 def test_biwang_name_is_explicit_commentary_and_not_the_other_chang(self):
  n=next(n for n in read('data/corpus/profile-names.json')['records']if n['person_id']=='fa5_rxi_3t4');self.assertEqual((n['title'],n['surname'],n['ming']),('裨王',None,'長'));self.assertIn('者裨王名也',n['references'][0]['quote']);self.assertNotEqual(n['person_id'],'f41_ulg_3u1_*AA');self.assertIn('683113d4baf6febecaf2ccb7913df87c4d68d454',n['references'][0]['url'])
 def test_named_title_usage_and_appointment_have_calendar_windows(self):
  tables=load_tables(R)
  for h in read('corpus/shiji/115-titles.json')['holdings'][3:5]:
   a=h['attestations'][0];d=a['normalized_date_range'];self.assertEqual([d[k]['era_year']for k in ['earliest','latest']],[110,109]);self.assertEqual(table_regnal_range_errors(d,a['date_expression'],tables),[]);self.assertEqual(h['effective_period']['end']['status'],'unknown')
   if h['mode']=='grant':self.assertNotIn('normalized_date',h['effective_period']['start']);self.assertEqual(h['effective_period']['start']['normalized_date_range']['latest']['era_year'],109)
 def test_parallel_readings_keep_actions_names_and_titles_distinct(self):
  vs=read('corpus/shiji/115.json')['annotation']['reported_variants'];self.assertEqual([(v['received_reading'],v['reported_reading'])for v in vs],[('誅遂','許遂'),('韓陰','韓陶'),('成巳','成已'),('溫陽侯','涅陽侯')])
  for v in vs:self.assertFalse(v['adopted']);self.assertFalse(v['image_verified']);self.assertEqual(v['status'],'reported_not_collated');self.assertIn(v['reported_reading'],v['quote']);self.assertIn('683113d4baf6febecaf2ccb7913df87c4d68d454',v['url'])
 def test_variants_export_to_correct_person_without_changing_source_death(self):
  p=bundle('b80_lq9_z00',R);self.assertTrue(any(v['reported_reading']=='許遂'for v in p['reported_variants']));self.assertTrue(any(e['event_type']=='death'for e in p['life_events']));self.assertTrue(any('天子誅遂' in e['quote']for x in p['life_events']for e in x['evidence']))
 def test_received_text_and_name_anchors_are_preserved(self):
  c=read('corpus/shiji/115.json');self.assertEqual(c['text_sha256'],'2bf00055869f83634772f322c716d26724cb0fd8dad907280da2395195d60b53');p=next(p for p in c['paragraphs']if p['id'].endswith('p008'));self.assertIn('相韓陰',p['text']);self.assertIn('成巳',p['text']);self.assertIn('為溫陽侯',p['text'])
if __name__=='__main__':unittest.main()
