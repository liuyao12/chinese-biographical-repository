# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.table_title_holdings import table_title_errors
from scripts.table_evidence import load_tables
from scripts.person_bundle import validate_name_component_alternatives
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
ORIGINAL_GRANTS = set({'th-table-shiji020-r052-founding-grant', 'th-table-shiji020-r045-founding-grant', 'th-table-shiji020-r062-founding-grant', 'th-table-shiji020-r053-founding-grant', 'th-table-shiji020-r056-founding-grant', 'th-table-shiji020-r054-founding-grant', 'th-table-shiji020-r055-founding-grant', 'th-table-shiji020-r046-founding-grant'})
def holdings():return [h for h in load('corpus/shiji/020-table-title-events.json')['holdings'] if h['id'] in ORIGINAL_GRANTS]
class NativeTableTitles(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.tables=load_tables(R);cls.people={p['id']for p in load('registry/persons.json')['persons']}
 def check_bad(self,h):self.assertTrue(table_title_errors(h,self.tables,self.people))
 def test_eight_grants_have_only_native_cell_evidence(self):
  hs=holdings();self.assertEqual(len(hs),8)
  for h in hs:
   self.assertEqual(table_title_errors(h,self.tables,self.people),[],h['id']);self.assertTrue(all(e['kind']=='table_cell'and 'paragraph_id'not in e for e in h['evidence']));self.assertEqual(h['effective_period']['end'],dict(status='unknown',date_expression=None,evidence=[]))
 def test_composed_date_keeps_original_column_and_cell_parts(self):
  for h in holdings():
   p=h['table_title_basis']['date_parts'];b=h['effective_period']['start'];self.assertEqual(b['date_expression_kind'],'table_columns_composed');self.assertEqual(b['date_expression'],p[0]['text']+p[1]['text']);self.assertNotIn(b['date_expression'],h['table_title_basis']['event']['quote'])
 def test_explicit_first_to_ninth_month_is_same_western_year(self):
  hs=holdings()
  for h in hs[:-1]:
   d=h['effective_period']['start']['normalized_date'];self.assertEqual(d['precision'],'year');self.assertEqual(d['year'],1-d['era_year']);self.assertEqual(d['era_year'],112 if h['person_id']in ['tz9_dhl_ifo_A','8xz_mlj_r3c_A']else 111)
 def test_unspecified_intercalary_month_stays_a_range(self):
  h=holdings()[-1];self.assertEqual(h['title'],'臨蔡侯');b=h['effective_period']['start'];self.assertEqual(b['date_expression'],'元封元年閏月癸卯');self.assertEqual((b['normalized_date_range']['earliest']['era_year'],b['normalized_date_range']['latest']['era_year']),(111,110));self.assertNotIn('normalized_date',b)
 def test_parent_death_cannot_grant_title_to_parent(self):
  h=copy.deepcopy(holdings()[0]);h['person_id']='tz9_dhl_ifo';self.check_bad(h)
 def test_mismatched_same_named_fief_row_is_rejected(self):
  h=copy.deepcopy(holdings()[5]);h['table_title_basis']['noble_name'].update(table_cell_id='shiji-020-t1-r037-c00',quote='湘成。');self.check_bad(h)
 def test_revision_and_name_anchor_are_checked(self):
  for kind in ['revision','anchor','source_kind']:
   h=copy.deepcopy(holdings()[0])
   if kind=='revision':h['evidence'][0]['source_revision']='0'
   elif kind=='anchor':h['table_title_basis']['event']['person_mention_id']='no-anchor'
   else:h['source_representation']='paragraph'
   self.check_bad(h)
 def test_era_column_and_same_year_from_another_era_are_rejected(self):
  h=copy.deepcopy(holdings()[0]);h['table_title_basis']['date_parts'][0]['table_column_id']='shiji-020-t1-column-4';self.check_bad(h)
  h=copy.deepcopy(holdings()[0]);h['table_title_basis']['year_mapping'].update(era_anchor_cell_id='shiji-022-t1-r073-c01',regnal_year_cell_id='shiji-022-t1-r077-c01',digital_year_cell_id='shiji-022-t1-r077-c00');self.check_bad(h)
 def test_date_wording_and_rank_parts_cannot_be_invented(self):
  h=copy.deepcopy(holdings()[0]);h['table_title_basis']['date_parts'][1]['text']='三年正月甲子';self.check_bad(h)
  h=copy.deepcopy(holdings()[0]);h['attestations'][0]['source_parts'][1]['surface']='廣德';self.check_bad(h)
 def test_known_month_cannot_be_widened_and_unknown_leap_cannot_be_exact(self):
  h=copy.deepcopy(holdings()[0]);b=h['effective_period']['start'];d=b.pop('normalized_date');b['normalized_date_range']=dict(d,earliest=dict(era='BCE',era_year=113,year=-112),latest=dict(era='BCE',era_year=112,year=-111));self.check_bad(h)
  h=copy.deepcopy(holdings()[-1]);b=h['effective_period']['start'];d=b.pop('normalized_date_range');b['normalized_date']=dict(d,era='BCE',era_year=110,year=-109,precision='year');self.check_bad(h)
 def test_earlier_holding_prevents_first_grant_claim(self):
  ts=copy.deepcopy(self.tables);h=holdings()[0];c=next(c for f in ts['shiji-020']['fragments']for r in f['rows']for c in r['cells']if c['id']=='shiji-020-t1-r045-c04');c['text']='synthetic prior holding';self.assertTrue(table_title_errors(h,ts,self.people))
 def test_native_story_opening_is_not_the_later_grant_date(self):
  hs=load('corpus/shiji/113-titles.json')['holdings']
  for hid in ['th-shiji113-026','th-shiji113-027']:
   h=next(h for h in hs if h['id']==hid);b=h['effective_period']['start'];self.assertIsNone(b['date_expression']);self.assertNotIn('normalized_date',b);self.assertIn('元鼎六年冬',h['evidence'][0]['quote'])
 def test_name_zi_alternative_keeps_both_sources_parseable(self):
  n=next(n for n in load('data/corpus/profile-names.json')['records']if n['person_id']=='u20_r6q_88g');validate_name_component_alternatives(n);self.assertEqual((n['surname'],n['ming'],n['zi']),('安國',None,'少季'));a=n['component_alternatives'][0];self.assertEqual(a['components'],dict(surname='安國',ming='少季',zi=None));self.assertIn('少季名也',a['reference']['quote']);self.assertIn('字少季',n['references'][0]['quote'])
 def test_name_alternative_rejects_unbound_components_and_forged_source(self):
  n=next(n for n in load('data/corpus/profile-names.json')['records']if n['person_id']=='u20_r6q_88g')
  for kind in ['component','url','raw','image']:
   x=copy.deepcopy(n);a=x['component_alternatives'][0]
   if kind=='component':a['components']['ming']='安國'
   elif kind=='url':a['reference']['url']='javascript:bad'
   elif kind=='raw':a['reference']['raw_quote']='synthetic unrelated text'
   else:a['reference']['image_verified']=True
   with self.assertRaises(ValueError):validate_name_component_alternatives(x)
 def test_api_cites_fief_event_and_year_without_fake_person_occurrences(self):
  for h in holdings():
   b=load('exports/persons/'+h['person_id']+'.json');self.assertTrue(any(x['id']==h['id']for x in b['title_holdings']));ids={c['table_cell_id']for c in b['table_passages']};basis=h['table_title_basis'];self.assertIn(basis['event']['table_cell_id'],ids);self.assertIn(basis['year_mapping']['digital_year_cell_id'],ids);self.assertFalse(any(x['table_id']=='shiji-022'and x['table_cell_id']==basis['year_mapping']['digital_year_cell_id']for x in b['table_occurrences']))
if __name__=='__main__':unittest.main()
