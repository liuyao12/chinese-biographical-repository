import copy
import json
import unittest
from pathlib import Path
from scripts.biographical_kinship import child_continuation_errors
from scripts.person_bundle import validate_clan_style
from scripts.subject_continuation import prior_subject_valid, title_attestation_subject_valid

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class SongshuXunFamilyTests(unittest.TestCase):
    def test_chisong_parent_keeps_all_three_original_paragraphs(self):
        c = read('corpus/songshu/060.json')
        a = next(a for a in read('corpus/songshu/060-assertions.json')['assertions']
                 if a.get('context', {}).get('kind') == 'biographical_child_continuation')
        self.assertEqual(child_continuation_errors(a, c), [])
        self.assertEqual([p['source_position']['first_line'] for p in c['paragraphs'][4:7]], [99, 101, 103])
        self.assertNotIn('伯子', c['paragraphs'][6]['text'])
        self.assertEqual(len(a['evidence']), 3)
        self.assertEqual(a['subject_person_id'], 'yoo_ox0_545_BABAAABAAA')
        self.assertEqual(a['object_person_id'], 'yoo_ox0_545_BABAAABAA')

    def test_death_age_has_source_and_does_not_invent_birth(self):
        c = read('corpus/songshu/060.json')
        a = c['annotation']['age_assertions'][0]
        self.assertEqual(a['value'], 61)
        self.assertIsNone(a['birth_year'])
        self.assertEqual(a['normalized_date']['year'], 438)
        self.assertEqual(a['normalized_date']['source_expression'], '元嘉十五年')
        self.assertEqual(a['normalized_date']['calendar'], 'chinese_civil')
        self.assertTrue(prior_subject_valid(a['evidence'][0]['context'], a['evidence'][0], a['person_id'], c))
        for h in read('corpus/songshu/060-titles.json')['holdings']:
            for att in h['attestations']:
                if 'context' in att: self.assertTrue(title_attestation_subject_valid(att, h, c))
            if h['title'] == '東陽太守':
                self.assertEqual(h['effective_period']['end']['normalized_date']['year'], 438)
                self.assertEqual(h['end_basis']['source_term'], '東陽太守。元嘉十五年，卒官')
            else:
                self.assertNotIn('normalized_date', h['effective_period']['end'])

    def test_mourning_number_does_not_become_ancestry_distance(self):
        a = next(a for a in read('corpus/songshu/060-assertions.json')['assertions'] if a['predicate'] == 'agnatic_cousin')
        self.assertEqual(a['qualifiers']['mourning_separation']['value'], 5)
        self.assertIsNone(a['qualifiers']['mourning_separation']['common_ancestor_distance'])
        self.assertIsNone(a['qualifiers']['kinship_structure']['distance'])
        families = read('registry/family-assemblies.json')['assemblies']
        branch = next(a for a in families if a['id'] == 'family-xun-chang-song')
        main = next(a for a in families if a['id'] == 'family-xun-shu-early-medieval')
        self.assertNotIn(branch['root_person_id'], {m['person_id'] for m in main['members']})

    def test_wife_clan_keeps_unknown_ming_and_no_mother_claim(self):
        names = read('data/corpus/profile-names.json')['records']
        name = next(n for n in names if n.get('clan_style', {}).get('kind') == 'wife_sibling_clan_appellation')
        c = read('corpus/songshu/060.json')
        p = next(p for p in c['paragraphs'] if p['id'] == name['paragraph_id'])
        relations = read('corpus/songshu/060-assertions.json')['assertions']
        validate_clan_style(name, p, relations)
        self.assertIsNone(name['ming'])
        self.assertFalse(any(a['predicate'] == 'mother' and a['object_person_id'] == name['person_id'] for a in relations))
        for field, value in [('ming', '宣明'), ('surname', '王')]:
            bad = copy.deepcopy(name); bad[field] = value
            with self.assertRaises(ValueError): validate_clan_style(bad, p, relations)
        bad = copy.deepcopy(relations)
        next(a for a in bad if a['id'] == name['clan_style']['assertion_ids'][0])['predicate'] = 'spouse'
        with self.assertRaises(ValueError): validate_clan_style(name, p, bad)

    def test_proposals_and_simile_do_not_become_titles_of_bozi(self):
        pid = 'yoo_ox0_545_BABAAABAA'
        titles = read('corpus/songshu/060-titles.json')['holdings']
        self.assertFalse(any(h['person_id'] == pid and h['title'] in ('平陽侯', '世子', '陳留王', '零陵王') for h in titles))
        end = next(h['effective_period']['end'] for h in titles if h['title'] == '晉陵太守')
        self.assertEqual(end['event_type'], 'explicit_end')
        self.assertIsNone(end['date_expression'])
        self.assertIn('下獄免', end['evidence'][0]['quote'])
        self.assertFalse(any(a['predicate'] == 'spouse' and a['object_person_id'] == pid and a['subject_person_id'] !=
            next(n['person_id'] for n in read('data/corpus/profile-names.json')['records']
                 if n.get('clan_style', {}).get('kind') == 'wife_sibling_clan_appellation')
            for a in read('corpus/songshu/060-assertions.json')['assertions']))

    def test_wei_posthumous_emperor_uses_existing_identity(self):
        d = next(d for d in read('corpus/songshu/060-identities.json')['decisions'] if d['person_id'] == 'bis_ydq_yeg')
        self.assertIn('太祖文皇帝', d['surfaces'])
        self.assertIn('文王', d['surfaces'])
        self.assertIn('追尊號曰文皇帝', d['references'][0]['quote'])
        new_chapter = read('corpus/songshu/060.json')
        self.assertEqual(next(m['person_id'] for p in new_chapter['paragraphs'] for m in p['mentions']
                              if m['surface'] == '太祖文皇帝'), 'bis_ydq_yeg')

    def test_received_text_and_digital_apparatus_remain_separate(self):
        c = read('corpus/songshu/060.json')
        self.assertTrue(all('<ref' not in p['text'] for p in c['paragraphs']))
        notes = [n for e in c['source']['normalization']['excerpts'] for n in e['digital_editorial_notes']]
        self.assertEqual(len(notes), 3)
        self.assertTrue(all(n['text_layer'] == 'digital_editorial_note' and n['printed_editions_directly_checked'] is False for n in notes))
        review = read('docs/source-reviews/songshu060-digital-witness-comparison.json')
        self.assertEqual(len(review['comparisons']), 6)
        self.assertFalse(review['kanripo_source']['image_verified'])
