# -*- coding: utf-8 -*-
import json
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = json.loads((ROOT / 'corpus/songshu/075-wangsengda.json').read_text())
PID = '7r6_k52_qji_ABAAAAAB'
CHAPTER_ID = 'c-songshu-075-wangsengda'
TITLES = json.loads((ROOT / 'corpus/songshu/075-wangsengda-titles.json').read_text())['holdings']
ADDRESSES = json.loads((ROOT / 'corpus/songshu/075-wangsengda-addresses.json').read_text())['assertions']
EVENTS = json.loads((ROOT / 'corpus/songshu/075-wangsengda-life-events.json').read_text())['events']
PARAGRAPHS = {p['id']: p for p in CHAPTER['paragraphs']}
sys.path.insert(0, str(ROOT / 'scripts'))
from song075_contextual_death_year import valid as contextual_death_year_valid


class Song075WangsengdaTitlesAddresses(unittest.TestCase):
    def test_address_is_exactly_biographical_origin(self):
        a = next(x for x in ADDRESSES if x['relation'] == 'biographical_origin')
        p = PARAGRAPHS[a['source_anchor']['paragraph_id']]
        self.assertEqual((a['source_anchor']['start'], a['source_anchor']['end']), (4, 9))
        self.assertEqual(p['text'][4:9], '琅邪臨沂人')
        self.assertEqual(a['place']['source_name'], '琅邪臨沂')
        self.assertEqual(a['relation'], 'biographical_origin')
        self.assertIsNone(a['place']['modern_identification'])

    def test_death_place_is_machine_readable_but_unlocated(self):
        a = next(x for x in ADDRESSES if x['relation'] == 'death_place')
        p = PARAGRAPHS[a['source_anchor']['paragraph_id']]
        self.assertEqual(a['place']['source_name'], '獄')
        self.assertEqual((a['source_anchor']['start'], a['source_anchor']['end']), (478, 479))
        self.assertEqual(p['text'][478:479], '獄')
        self.assertEqual(a['source_term'], '於獄賜死')
        self.assertIsNone(a['place']['place_id'])
        self.assertIsNone(a['place']['modern_identification'])
        self.assertIn('不視為具名監獄', a['interpretation_note'])

    def test_all_holding_anchors_match_the_received_words(self):
        for h in TITLES:
            self.assertEqual(h['person_id'], PID)
            for a in h['attestations']:
                p = PARAGRAPHS[a['paragraph_id']]
                self.assertEqual(p['text'][a['start']:a['end']], a['surface'])
            for e in h['evidence']:
                self.assertEqual(e['source_id'], CHAPTER['source_id'])
                self.assertEqual(e['chapter_id'], CHAPTER_ID)
                self.assertIn(e['quote'], PARAGRAPHS[e['paragraph_id']]['text'])

    def test_explicit_transfers_and_enfeoffment_are_separate(self):
        by_title_line = {(h['title'], h['attestations'][0]['paragraph_id']): h for h in TITLES}
        for title, line, verb in [('太子舍人', 'line012', '遷'), ('太子洗馬', 'line012', '遷'),
                                  ('太宰長史', 'line042', '徙'), ('左衛將軍', 'line042', '遷'),
                                  ('中書令', 'line042', '遷')]:
            h = by_title_line[(title, f'{CHAPTER_ID}:{line}')]
            self.assertEqual(h['mode'], 'transfer')
            self.assertEqual(h['office_transfer_basis']['source_term'], verb + title)
        marquis = next(h for h in TITLES if h['title'] == '寧陵縣五等侯')
        self.assertEqual(marquis['kind'], 'noble_rank')
        self.assertEqual(marquis['appointment_role'], 'enfeoffment')

    def test_washima_memorial_is_same_holding_not_a_new_appointment(self):
        h = next(h for h in TITLES if h['title'] == '太子洗馬')
        occurrence, = h['related_source_occurrences']
        p = PARAGRAPHS[occurrence['paragraph_id']]
        self.assertEqual((occurrence['start'], occurrence['end']), (118, 120))
        self.assertEqual(p['text'][118:120], '洗馬')
        self.assertIn('又擢為洗馬', occurrence['context_surface'])
        self.assertIn('非第二次任命', occurrence['note'])
        self.assertEqual(h['effective_period']['end']['event_type'], 'explicit_end')

    def test_unassumed_nanman_appointment_and_holding_limits(self):
        by_title = {h['title']: h for h in TITLES if h['attestations'][0]['paragraph_id'].endswith('line016')}
        for title in ('使持節', '南蠻校尉'):
            self.assertEqual(by_title[title]['service_realization']['status'], 'not_taken_up')
            self.assertEqual(by_title[title]['service_realization']['source_term'], '不成行')
        p = json.loads((ROOT / 'corpus/songshu/075-wangsengda.json').read_text())
        proposals = [x for x in p['annotation']['title_proposals'] if x['id'] == 'tp-song075-wangsengda-nanman']
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]['non_assumption_anchor']['surface'], '不成行')
        # No office term is terminated by death; only mourning ends 太子洗馬 explicitly.
        for h in TITLES:
            if h['title'] != '太子洗馬':
                self.assertEqual(h['effective_period']['end']['status'], 'unknown')

    def test_converted_years_keep_source_precision_and_context(self):
        expected = {'長史': 453, '尚書右僕射': 453, '太常': 456, '左衛將軍': 457,
                    '太子中庶子': 457, '寧陵縣五等侯': 457, '中書令': 458}
        for title, year in expected.items():
            h = next(h for h in TITLES if h['title'] == title)
            normalized = h['effective_period']['start']['normalized_date']
            self.assertEqual(normalized['year'], year)
            self.assertEqual(normalized['precision'], 'year')
            self.assertEqual(normalized['status'], 'editorial_provisional')
        death, = EVENTS
        self.assertEqual(death['event_type'], 'death')
        self.assertEqual(death['reported_age']['value'], 36)
        self.assertIsNone(death['date_expression'])
        self.assertEqual(death['normalized_date']['year'], 458)
        self.assertIn('不把八月一日當死日', death['interpretation_note'])
        self.assertEqual(death['source_anchor']['surface'], '於獄賜死')
        self.assertNotIn('birth_year', death)

    def test_contextual_death_year_binding_rejects_wrong_person_year_chapter_or_day(self):
        event = copy.deepcopy(EVENTS[0])
        date = event['normalized_date']
        self.assertTrue(contextual_death_year_valid(event, date, CHAPTER))
        bad = copy.deepcopy(event); bad['normalized_date']['year'] = 457
        self.assertFalse(contextual_death_year_valid(bad, bad['normalized_date'], CHAPTER))
        bad = copy.deepcopy(event); bad['person_id'] = 'not-wangsengda'
        self.assertFalse(contextual_death_year_valid(bad, bad['normalized_date'], CHAPTER))
        wrong_chapter = copy.deepcopy(CHAPTER); wrong_chapter['id'] = 'c-songshu-076-other'
        self.assertFalse(contextual_death_year_valid(event, date, wrong_chapter))
        bad = copy.deepcopy(event); bad['date_expression'] = '二年'
        self.assertFalse(contextual_death_year_valid(bad, bad['normalized_date'], CHAPTER))
        bad = copy.deepcopy(event); bad['date_expression'] = '大明二年'
        self.assertFalse(contextual_death_year_valid(bad, bad['normalized_date'], CHAPTER))
        bad = copy.deepcopy(event); del bad['normalized_date']['contextual_death_year_binding']
        self.assertFalse(contextual_death_year_valid(bad, bad['normalized_date'], CHAPTER))
        bad = copy.deepcopy(event); bad['interpretation_note'] = '把八月一日當作死亡日'
        self.assertFalse(contextual_death_year_valid(bad, bad['normalized_date'], CHAPTER))

    def test_fixed_revision_is_unaltered_and_not_image_verified(self):
        self.assertEqual(CHAPTER['source']['revision_id'], 1997722)
        self.assertFalse(CHAPTER['source']['image_verified'])
        self.assertTrue(all(e.get('image_verified') is False for h in TITLES
                            for d in h['effective_period'].values()
                            for e in d.get('normalized_date', {}).get('references', [])))


if __name__ == '__main__':
    unittest.main()
