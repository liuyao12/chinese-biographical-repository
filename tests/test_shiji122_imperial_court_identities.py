# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ImperialCourtIdentityTests(unittest.TestCase):
 def test_all_60_source_spans_preserve_original_text(self):
  f=json.loads((ROOT/'tests/fixtures/shiji122-imperial-court-identities.json').read_text());c=json.loads((ROOT/'corpus/shiji/122.json').read_text());ps={p['id']:p for p in c['paragraphs']};self.assertEqual(len(f['mentions']),60)
  for row in f['mentions']:
   p=ps[row['paragraph_id']];m=next(m for m in p['mentions'] if m['id']==row['marker']['id']);self.assertEqual(p['text'],row['text']);self.assertEqual(m,row['marker']);self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
 def test_earlier_six_decisions_survive_the_three_new_decisions(self):
  d=json.loads((ROOT/'corpus/shiji/122-identities.json').read_text());self.assertEqual(len(d['decisions']),9);self.assertEqual(len({x['id'] for x in d['decisions']}),9)
 def test_retired_imperial_candidates_have_no_live_source_references(self):
  f=json.loads((ROOT/'tests/fixtures/shiji122-imperial-court-identities.json').read_text())
  for folder in ['corpus','registry','data/corpus','exports']:
   for p in (ROOT/folder).rglob('*'):
    if p.is_file() and p.suffix in ['.json','.xml','.md']:self.assertFalse(any(x in p.read_text() for x in f['mapping']),str(p))
 def test_zhou_yafu_title_and_name_are_sourced_and_calendar_pilot_survives(self):
  names=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records'];n=next(x for x in names if x['person_id']=='koy_6jg_gcc_C');self.assertEqual((n['title'],n['surname'],n['ming'],n['additional_names']),('條侯','周','亞夫',[]));c=json.loads((ROOT/'corpus/shiji/011.json').read_text());p=next(p for p in c['paragraphs'] if p['id']==n['paragraph_id']);self.assertEqual(n['quote'],p['text']);self.assertIn('條侯周亞夫',p['text'])
  events=json.loads((ROOT/'corpus/shiji/106-life-events.json').read_text())['events'];e=next(e for e in events if e['id']=='le-shiji106-008');self.assertEqual(e['chinese_civil_year']['era_year'],154);self.assertEqual(e['normalized_date_range']['earliest']['year'],-154)
