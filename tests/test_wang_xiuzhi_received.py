# coding: utf-8
import hashlib
import copy
import json
import re
import unittest
from pathlib import Path

from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog, bundle

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def plain(raw):
    text = re.sub(r'<ref>.*?</ref>', '', raw)
    text = re.sub(r'-\{([^{}]*)\}-', r'\1', text)
    text = re.sub(r'\{\{YL\|([^}|]+)\}\}', r'\1', text)
    return re.sub(r'\[\[([^]|]+)(?:\|([^]]+))?\]\]', lambda m: m[2] or m[1], text).strip()


class WangXiuzhiReceived(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.people, _ = cls.catalog
        cls.ids = {p['label']: p['id'] for p in cls.people.values()}

    def test_three_complete_biography_units_preserve_all_original_paragraphs(self):
        for path, lines in [('corpus/nanqishu/046.json', [11, 13, 15, 17, 19, 21, 23]),
                            ('corpus/songshu/093.json', [78, 80, 82, 84]),
                            ('corpus/nanqishu/032-ruantao.json', [92, 94])]:
            c = read(path)
            self.assertEqual([p['source_position']['first_line'] for p in c['paragraphs']], lines)
            excerpts = {e['proposed_paragraph_id']: e for e in c['source']['normalization']['excerpts']}
            for p in c['paragraphs']:
                e = excerpts[p['id']]
                self.assertEqual(p['text'], plain(e['raw_quote']))
                self.assertEqual(e['raw_quote_sha256'], hashlib.sha256(e['raw_quote'].encode()).hexdigest())
                self.assertFalse(p['source_position']['editorial_excerpt_boundary'])
                notes = e.get('removed_digital_editorial_notes', [])
                self.assertEqual([n['text'] for n in notes], re.findall(r'<ref>(.*?)</ref>', e['raw_quote']))
                self.assertTrue(all(n['text_layer'] == 'modern_digital_apparatus' for n in notes))
                for m in p['mentions']:
                    self.assertEqual(p['text'][m['start']:m['end']], m['surface'])

    def test_two_letters_in_one_paragraph_have_different_addressees(self):
        p = next(p for p in read('corpus/nanqishu/046.json')['paragraphs']
                 if p['source_position']['first_line'] == 19)
        boundary = p['text'].index('平又與儉書')
        earlier = [m for m in p['mentions'] if m['surface'] == '足下' and m['start'] < boundary]
        later = [m for m in p['mentions'] if m['surface'] == '足下' and m['start'] > boundary]
        self.assertTrue(earlier)
        self.assertEqual(len(later), 1)
        self.assertEqual({m['person_id'] for m in earlier}, {self.ids['王秀之']})
        self.assertEqual(later[0]['person_id'], self.ids['王儉'])
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] in ['僕', '我']},
                         {self.ids['苟平']})
        # The proper name 平原 is not a shortened reference to 苟平.
        self.assertTrue(all(m['person_id'] != self.ids['苟平'] for m in p['mentions'] if m['surface'] == '平原'))

    def test_ming_with_same_character_as_emperor_and_other_xie_story_remain_distinct(self):
        c = read('corpus/nanqishu/032-ruantao.json')
        p = c['paragraphs'][1]
        wang = next(m['person_id'] for m in p['mentions'] if m['surface'] == '王彧')
        xie = next(m['person_id'] for m in p['mentions'] if m['surface'] == '謝莊')
        self.assertNotEqual(wang, self.ids['宋明帝彧'])
        self.assertNotEqual(xie, '5o2_8lk_osv')

    def test_kong_family_keeps_inferred_links_distinct_from_direct_sources(self):
        _, assembled = load_assemblies(ROOT, self.catalog)
        can, mo = self.ids['孔粲（淳之父）'], self.ids['孔默之']
        self.assertEqual(assembled[can]['parent_connection']['type'], 'parent_between_consecutive_ancestors')
        self.assertEqual(assembled[mo]['parent_connection']['type'], 'shared_father_through_sibling')
        assertions = read('corpus/songshu/093-assertions.json')['assertions']
        self.assertFalse(any(a['predicate'] == 'father' and a['subject_person_id'] in [can, mo]
                             for a in assertions))
        self.assertEqual(assembled[self.ids['孔尚']]['parent_person_id'], self.ids['孔淳之'])
        self.assertEqual(assembled[self.ids['孔熙先']]['parent_person_id'], mo)

    def test_marriage_and_daughter_links_are_available_from_both_endpoints(self):
        daughter = self.ids['王敬弘女（孔尚妻）']
        data = bundle(daughter, ROOT, catalog=self.catalog)
        father = next(a for a in data['relations'] if a['id'] == 'a-songshu093-wang-daughter-father')
        marriage = next(a for a in data['relations'] if a['id'] == 'a-songshu093-kongshang-marriage')
        self.assertIn(father, bundle(father['object_person_id'], ROOT, catalog=self.catalog)['relations'])
        self.assertIn(marriage, bundle(marriage['object_person_id'], ROOT, catalog=self.catalog)['relations'])
        self.assertEqual(marriage['evidence'][0]['chapter_id'], 'c-songshu-093-recluses')
        self.assertIn('適', marriage['qualifiers']['source_term'])
        self.assertFalse(any(a['predicate'] == 'mother' for a in data['relations']))

    def test_two_daughter_contexts_are_an_explicit_unresolved_identity_case(self):
        cases = read('corpus/nanshi/024.json')['annotation']['unresolved_identity_cases']
        case = next(c for c in cases if c['id'] == 'u-wangjinghong-two-daughter-contexts')
        self.assertEqual(case['status'], 'unresolved')
        self.assertEqual(set(case['candidate_person_ids']),
                         {self.ids['王敬弘女（何述之妻，未名）'], self.ids['王敬弘女（孔尚妻）']})

    def test_parallel_guoqin_names_merge_without_absorbing_learning_story(self):
        canonical = 'ccx_50c_ssi'
        self.assertNotIn('28u_l10_cos', self.people)
        for path, surface in [('corpus/shiji/006.json', '寧越'),
                              ('corpus/shiji/048.json', '甯越')]:
            mentions = [m for p in read(path)['paragraphs'] for m in p['mentions']
                        if m['surface'] == surface]
            self.assertTrue(mentions)
            self.assertEqual({m['person_id'] for m in mentions}, {canonical})
        cases = read('corpus/nanshi/024.json')['annotation']['unresolved_identity_cases']
        case = next(c for c in cases if c['id'] == 'u-ningyue-learning-and-guoqin')
        self.assertEqual(case['status'], 'unresolved')
        self.assertEqual(set(case['candidate_person_ids']), {canonical, 'hhx_c6e_0lx'})
        self.assertIn('不必甯越也', case['references'][0]['quote'])
        for pid in case['candidate_person_ids']:
            self.assertIn(pid, self.people)

    def test_context_parallels_are_not_claimed_as_direct_person_attestations(self):
        decisions = read('corpus/nanshi/024-identities.json')['decisions']
        for ident, context in [
                ('d-nanshi024-zhongzu-wangmeng', 'c-nanqishu-046-wangxiuzhi:line021'),
                ('d-nanshi024-luling-marriage-shao', 'c-nanshi-024-wang-family:line017')]:
            decision = next(d for d in decisions if d['id'] == ident)
            self.assertFalse(any(e['paragraph_id'] == context for e in decision['evidence']))
            reference = next(r for r in decision['references'] if r.get('paragraph_id') == context)
            self.assertEqual(reference['scope'], 'narrative_context_only_not_direct_person_attestation')

    def test_received_death_years_and_reported_ages_do_not_create_birth_years(self):
        for path, year, age in [('corpus/nanqishu/046', 494, 53),
                                ('corpus/nanqishu/032-ruantao', 484, None),
                                ('corpus/songshu/093', 430, 59)]:
            event = read(path + '-life-events.json')['events'][0]
            self.assertEqual(event['event_type'], 'death')
            self.assertEqual(event['normalized_date']['year'], year)
            self.assertEqual(event['normalized_date']['calendar'], 'chinese_civil')
            self.assertIn(event['date_expression'], event['evidence'][0]['quote'])
            data = bundle(event['person_id'], ROOT, catalog=self.catalog)
            self.assertIn(event, data['life_events'])
            reports = read(path + '.json')['annotation'].get('age_assertions', [])
            if age is None:
                self.assertFalse(reports)
            else:
                report = next(a for a in reports if a['person_id'] == event['person_id'])
                self.assertEqual(report['value'], age)
                self.assertIsNone(report['birth_year'])
                self.assertEqual(report['normalized_date']['year'], year)

    def test_biographical_origins_preserve_historical_place_names(self):
        for path, place in [('corpus/nanqishu/046-addresses.json', '琅邪臨沂'),
                            ('corpus/nanqishu/032-ruantao-addresses.json', '陳留'),
                            ('corpus/songshu/093-addresses.json', '魯郡魯')]:
            assertion = read(path)['assertions'][0]
            self.assertEqual(assertion['relation'], 'biographical_origin')
            self.assertEqual(assertion['place']['source_name'], place)
            self.assertIsNone(assertion['place']['modern_identification'])
            self.assertIn(place + '人', assertion['evidence'][0]['quote'])

    def test_unassumed_offices_keep_refusal_and_person_anchors(self):
        from scripts.unassumed_appointments import unassumed_appointment_valid
        for path, titles in [('corpus/songshu/093.json', ['著作佐郎', '太尉參軍', '祕書監']),
                             ('corpus/nanqishu/046.json', ['侍中', '游擊將軍', '黃門郎'])]:
            chapter = read(path)
            proposals = chapter['annotation']['title_proposals']
            self.assertCountEqual([p['title'] for p in proposals], titles)
            for proposal in proposals:
                self.assertTrue(unassumed_appointment_valid(proposal, chapter))
                corrupted = copy.deepcopy(proposal)
                corrupted['non_assumption_anchor']['start'] += 1
                self.assertFalse(unassumed_appointment_valid(corrupted, chapter))
                corrupted = copy.deepcopy(proposal)
                corrupted['person_id'] = self.ids['王儉']
                self.assertFalse(unassumed_appointment_valid(corrupted, chapter))

    def test_received_titles_have_exact_spans_and_keep_ancestors_distinct(self):
        for stem in ['corpus/nanqishu/046', 'corpus/nanqishu/032-ruantao', 'corpus/songshu/093']:
            chapter = read(stem + '.json')
            paragraphs = {p['id']: p for p in chapter['paragraphs']}
            for holding in read(stem + '-titles.json')['holdings']:
                for attestation in holding['attestations']:
                    p = paragraphs[attestation['paragraph_id']]
                    self.assertEqual(p['text'][attestation['start']:attestation['end']], holding['title'])
                    person = next(m for m in p['mentions'] if m['id'] == attestation['person_mention_id'])
                    self.assertEqual(person['person_id'], holding['person_id'])
                self.assertEqual(holding['effective_period']['end']['status'], 'unknown')
        qi = read('corpus/nanqishu/046-titles.json')['holdings']
        posthumous = next(h for h in qi if h['title'] == '簡子')
        self.assertEqual(posthumous['person_id'], self.ids['王秀之'])
        self.assertEqual(posthumous['mode'], 'posthumous_naming')
        self.assertIsNone(posthumous['effective_period']['start']['date_expression'])
        ruan = read('corpus/nanqishu/032-ruantao-titles.json')['holdings']
        ancestor = next(h for h in ruan if h['evidence'][0]['paragraph_id'].endswith('line092')
                        and h['title'] == '金紫光祿大夫')
        self.assertEqual(ancestor['person_id'], self.ids['阮裕（韜玄祖）'])

    def test_later_huangmen_service_does_not_erase_earlier_non_assumption(self):
        chapter = read('corpus/nanqishu/046.json')
        refusal = next(p for p in chapter['annotation']['title_proposals'] if p['title'] == '黃門郎')
        holding = next(h for h in read('corpus/nanqishu/046-titles.json')['holdings']
                       if h['title'] == '黃門郎' and h['person_id'] == self.ids['王秀之'])
        attestation = holding['attestations'][0]
        self.assertEqual(refusal['role_anchor']['paragraph_id'], attestation['paragraph_id'])
        self.assertLess(refusal['non_assumption_anchor']['end'], attestation['start'])
        text = next(p['text'] for p in chapter['paragraphs'] if p['id'] == attestation['paragraph_id'])
        self.assertEqual(text[attestation['start'] - 2:attestation['start']], '復爲')

    def test_jun_honorific_is_distinct_from_unassumed_office(self):
        from scripts.unassumed_appointments import unassumed_appointment_valid
        chapter = read('corpus/nanshi/024.json')
        proposal = next(p for p in chapter['annotation']['title_proposals']
                        if p['id'] == 'tp-nanshi024-jun-jinzi-unassumed')
        self.assertTrue(unassumed_appointment_valid(proposal, chapter))
        honorific = next(h for h in read('corpus/nanshi/024-titles.json')['holdings']
                         if h['id'] == 'th-nanshi024-jun-huizi')
        self.assertEqual(proposal['person_id'], honorific['person_id'])
        self.assertEqual(honorific['title'], '惠子')
        self.assertEqual(honorific['mode'], 'posthumous_naming')
        self.assertIsNone(honorific['effective_period']['start']['date_expression'])

    def test_biographical_name_components_are_parseable_in_person_bundles(self):
        for pid, surname, ming, zi in [('7r6_k52_qji_ABDABAABA', '王', '秀之', '伯奮'),
                                       ('03n_n2r_8rt_***A', '阮', '韜', '長明'),
                                       ('vhw_07a_wzm_AA', '孔', '淳之', '彦深')]:
            names = bundle(pid, ROOT, catalog=self.catalog)['name_components']
            name = next(n for n in names if surname + ming + '字' + zi in n['quote'])
            self.assertEqual((name['surname'], name['ming'], name['zi']), (surname, ming, zi))
            self.assertIn('字' + zi, name['additional_names'])
            self.assertFalse(name['human_reviewed'])

    def test_ruan_four_generation_claim_is_available_at_both_endpoints(self):
        assertion = read('corpus/nanqishu/032-ruantao-assertions.json')['assertions'][0]
        self.assertEqual(assertion['predicate'], 'ancestor')
        self.assertEqual(assertion['qualifiers']['generation_distance'], 4)
        self.assertEqual(assertion['qualifiers']['source_term'], '裕玄孫')
        self.assertEqual(assertion['subject_person_id'], self.ids['阮韜'])
        self.assertEqual(assertion['object_person_id'], self.ids['阮裕（韜玄祖）'])
        for key in ['subject_person_id', 'object_person_id']:
            self.assertIn(assertion, bundle(assertion[key], ROOT, catalog=self.catalog)['relations'])

    def test_postposed_summons_requires_adjacent_role_and_correct_recipient(self):
        from scripts.unassumed_appointments import unassumed_appointment_valid
        chapter = read('corpus/songshu/093.json')
        proposal = next(p for p in chapter['annotation']['title_proposals']
                        if p['id'] == 'tp-songshu093-can-mishu-unassumed')
        self.assertEqual(proposal['person_id'], self.ids['孔粲（淳之父）'])
        self.assertEqual(proposal['role_anchor']['end'], proposal['appointment_anchor']['start'])
        self.assertTrue(unassumed_appointment_valid(proposal, chapter))
        changed = copy.deepcopy(proposal)
        changed['person_id'] = self.ids['孔淳之']
        self.assertFalse(unassumed_appointment_valid(changed, chapter))


if __name__ == '__main__':
    unittest.main()
