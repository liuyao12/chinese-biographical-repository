# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class MengtianEvidenceTests(unittest.TestCase):
    def read(self, name):
        return json.loads((ROOT / 'corpus/shiji' / name).read_text())
    def test_condemnation_custody_and_capture_do_not_become_deaths(self):
        events = self.read('088-life-events.json')['events']
        ids = {e['person_id'] for e in events}
        self.assertFalse(ids.intersection({'0xx_ozc_454', 'ylb_ttg_8dr', 'wfm_qvc_ykk', 'k2p_5ol_dwh_A'}))
        tian = [e for e in events if e['person_id'] == 'k2p_5ol_dwh_AA']
        self.assertEqual(len(tian), 1)
        self.assertEqual(tian[0]['source_term'], '乃吞藥自殺')
        self.assertTrue(tian[0]['evidence'][0]['paragraph_id'].endswith(':p010'))
        self.assertNotIn('normalized_date', tian[0])
    def test_ancestral_origin_and_death_places_keep_source_scope(self):
        rows = self.read('088-addresses.json')['assertions']
        origin = next(x for x in rows if x['relation'] == 'ancestral_origin')
        self.assertEqual(origin['qualifiers']['subject_scope'], 'ancestors_unspecified')
        self.assertIsNone(origin['qualifiers']['ancestor_person_id'])
        self.assertFalse(any(x['relation'] in ('birth_place','biographical_origin') for x in rows))
        deaths = {x['person_id']: x for x in rows if x['relation'] == 'death_place'}
        for pid, place, actual in [('k2p_5ol_dwh_AB','代','遂殺之'), ('k2p_5ol_dwh_AA','陽周','乃吞藥自殺')]:
            self.assertEqual(deaths[pid]['place']['source_name'], place)
            self.assertIsNone(deaths[pid]['place']['modern_identification'])
            self.assertIn(actual, deaths[pid]['evidence'][0]['quote'])
    def test_xiangyan_default_retains_other_year_and_mechanism(self):
        decision = self.read('088-date-decisions.json')['decisions'][0]
        old = next(e for e in self.read('006-life-events.json')['events'] if e['id'] == 'le-shiji006-018')
        new = next(e for e in self.read('088-life-events.json')['events'] if e['id'] == decision['preferred_event_id'])
        self.assertEqual((old['normalized_date']['era_year'],new['normalized_date']['era_year']), (223,224))
        self.assertIn('自殺', old['source_term'])
        self.assertEqual(new['source_term'], '殺項燕')
        self.assertEqual(old['normalized_date']['references'][0]['scope'], 'received_regnal_year_attestation')
        self.assertFalse(decision['human_reviewed'])
        self.assertEqual(decision['evidence'], old['evidence'] + new['evidence'])
    def test_younger_brother_is_relative_order_without_absolute_numbers(self):
        a = next(a for a in self.read('088-assertions.json')['assertions'] if a['id'] == 'a-shiji088-003')
        order = a['qualifiers']['relative_birth_order']
        self.assertEqual((order['older_person_id'],order['younger_person_id']), ('k2p_5ol_dwh_AA','k2p_5ol_dwh_AB'))
        self.assertEqual(order['operator'],'lt')
        self.assertIsNone(order['older_ordinal']);self.assertIsNone(order['younger_ordinal'])
        self.assertEqual(a['qualifiers']['source_term'],'蒙恬弟毅')
    def test_quoted_posthumous_name_retains_original_glyph_and_unknown_date(self):
        h = next(h for h in self.read('088-titles.json')['holdings'] if h['id'] == 'th-shiji088-017')
        self.assertEqual((h['title'],h['mode']),('繆','posthumous_naming'))
        self.assertNotIn('normalized_date',h['effective_period']['start'])
        self.assertLess(h['naming_basis']['source_term'].index('死'),h['naming_basis']['source_term'].index('立號'))
        p = next(p for p in self.read('088.json')['paragraphs'] if p['id'].endswith(':p009'))
        m = next(m for m in p['mentions'] if m['surface']=='繆')
        self.assertEqual(m['person_id'],'y97_huh_vuz_AAAAA')
        self.assertEqual(p['text'][m['start']:m['end']],'繆')
