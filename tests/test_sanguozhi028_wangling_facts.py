# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def j(n):return json.loads((R/n).read_text())
class WanglingFacts(unittest.TestCase):
 def test_complete_217_reconciliation(self):
  a=j('source-evidence/sanguozhi028-wang41-consumption.json');self.assertEqual(len(a['ledger']),217);self.assertEqual({r['id']for r in a['proposal_records']},{r['proposal_id']for r in a['ledger']});self.assertEqual(len({r['proposal_id']for r in a['ledger']}),217)
  for row in a['ledger']:
   if row['state']=='typed':self.assertTrue(any(t['proposal_id']==row['proposal_id']for t in a['typed']))
 def test_ages_exact_and_open_not_birth_estimate(self):
  c=j('corpus/sanguozhi/028-wangling.json');a={r['person_id']:r for r in c['annotation']['age_assertions']if r['id'].startswith('age-wang41-')};self.assertEqual(a['f89_ad1_61d']['value'],80);g=a['f89_ad1_61d_A'];self.assertIsNone(g['value']);self.assertEqual(g['bounds'],{'lower':40,'lower_inclusive':False,'upper':None,'upper_inclusive':None})
  for v in a.values():self.assertIsNone(v['birth_year']);self.assertEqual(v['age_context']['kind'],'at_death')
 def test_only_recorded_removal_ends_specific_current_office(self):
  hs=j('corpus/sanguozhi/028-wangling-titles.json')['holdings'];ends=[h for h in hs if h['effective_period']['end']['status']!='unknown'];self.assertEqual([(h['person_id'],h['title'])for h in ends],[('43d_e5c_69f','和戎䕶軍')]);self.assertEqual(ends[0]['effective_period']['end']['event_type'],'explicit_end')
 def test_four_era_ranges_do_not_become_year_one(self):
  hs=j('corpus/sanguozhi/028-wangling-titles.json')['holdings'];xs=[h['effective_period']['start']['normalized_date_range']for h in hs if 'normalized_date_range'in h['effective_period']['start']];self.assertEqual(len(xs),4)
  for x in xs:self.assertEqual((x['earliest']['year'],x['latest']['year']),(240,249))
 def test_all_deaths_have_exact_full_quote_and_never_infer_birth(self):
  c=j('corpus/sanguozhi/028-wangling.json');ps={p['id']:p for p in c['paragraphs']};events=j('corpus/sanguozhi/028-wangling-life-events.json')['events'];self.assertEqual(len(events),11)
  for e in events:
   self.assertEqual(e['event_type'],'death');self.assertFalse(e['human_reviewed']);self.assertNotIn('birth_year',e)
   local={'le-wang41-118':'凌至項飲藥死','le-wang41-120':'太傅有疾夢凌逵為厲甚惡之遂薨'}
   for v in e['evidence']:
    self.assertEqual(v['quote'],local.get(e['id'],ps[v['paragraph_id']]['text']));self.assertIn(e['source_term'],v['quote'])
   if e['id']in local:
    d=e['normalized_date'];b=d['event_evidence_binding'];self.assertEqual(b['kind'],'local_death_in_fixed_narrative_year_chain');self.assertEqual((b['life_event_id'],b['person_id'],b['source_term']),(e['id'],e['person_id'],e['source_term']))
    self.assertEqual(d['year'],251);self.assertEqual(b['source_fingerprint'],{'source_id':'s-sanguozhi-028-wangling','source_commit':'214fcafa79894355909c9d8c2c1533089e7791c6','source_blob_sha':'d1d192e3e36be8919fa86563bd8e1fd82a3f4638','response_sha256':'0d69bbb981b5dd31bbeee865d503179979226e2d2ce7c42aeac0fe0fc6e868f7'})
    self.assertEqual(len(d['evidence']),7 if e['id'].endswith('118')else 8)
    for dv in d['evidence']:self.assertEqual(dv['quote'],ps[dv['paragraph_id']]['text'])
    self.assertEqual(b['event_evidence_index'],0);self.assertEqual(b['date_evidence_index'],len(d['evidence'])-1)
    q=b['event_quote_anchor'];t=b['event_term_anchor'];date=b['event_date_expression_anchor'];self.assertEqual((q['start'],q['end']),(157,163)if e['id'].endswith('118')else(444,458));self.assertEqual((t['start'],t['end']),(157,163)if e['id'].endswith('118')else(456,458))
    for a in [q,t,date]:self.assertEqual(ps[a['paragraph_id']]['text'][a['start']:a['end']],a['surface'])
    self.assertEqual(q['surface'],local[e['id']]);self.assertEqual(t['surface'],e['source_term']);self.assertEqual(date['surface'],e['date_expression'])
    m=next(m for m in ps[q['paragraph_id']]['mentions']if m['id']==b['event_person_mention_id']);self.assertEqual(m['person_id'],e['person_id']);self.assertTrue(q['start']<=m['start']<m['end']<=q['end'])

 def test_resolved_calendar_years_not_falsely_imported_by_helper_alone(self):
  audit=j('source-evidence/sanguozhi028-wang41-consumption.json');by={r['proposal_id'][-3:]:r for r in audit['ledger']}
  for no in ['118','120']:self.assertEqual(by[no]['state'],'native_partial');self.assertTrue(any(x['proposal_id'].endswith(no) for x in audit['typed']))
  events=j('corpus/sanguozhi/028-wangling-life-events.json')['events'];a=next(x for x in events if x['id']=='le-wang41-118');b=next(x for x in events if x['id']=='le-wang41-120');self.assertEqual(a['person_id'],'f89_ad1_61d');self.assertEqual(b['person_id'],'dkn_ge4_286_AAAA');self.assertEqual(a['date_expression'],'三年春');self.assertEqual(b['date_expression'],'其年八月')
 def test_no_false_career_or_kinship(self):
  hs=j('corpus/sanguozhi/028-wangling-titles.json')['holdings'];self.assertFalse(any(h['title']in ['青州刺史','揚州刺史','豫州刺史','别駕']for h in hs));a=j('corpus/sanguozhi/028-wangling-assertions.json')['assertions'];self.assertEqual(len(a),6);m=next(x for x in a if x['id'].endswith('-005'));self.assertEqual(m['predicate'],'maternal_role');self.assertIsNone(m['qualifiers']['biological_mother']);u=next(x for x in a if x['id'].endswith('-006'));self.assertEqual((u['subject_person_id'],u['object_person_id']),('43d_e5c_69f','f89_ad1_61d'));self.assertIsNone(u['qualifiers']['mother_person_id'])
if __name__=='__main__':unittest.main()
