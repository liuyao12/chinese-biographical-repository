# coding: utf-8
import hashlib
import copy
import json
import re
import unittest
from pathlib import Path
from scripts.person_bundle import load_catalog, bundle
from scripts.family_assemblies import load_assemblies
ROOT = Path(__file__).resolve().parents[1]


class WangZhenzhiSourceFamily(unittest.TestCase):
    def test_full_three_original_paragraphs_keep_fixed_revision_and_literal_spans(self):
        c = json.loads((ROOT / 'corpus/songshu/092.json').read_text())
        self.assertEqual([p['source_position']['first_line'] for p in c['paragraphs']], [12, 14, 16])
        self.assertEqual(c['source']['revision_id'], 2195614)
        for p, e in zip(c['paragraphs'], c['source']['normalization']['excerpts']):
            self.assertFalse(p['source_position']['editorial_excerpt_boundary'])
            self.assertEqual(hashlib.sha256(e['raw_quote'].encode()).hexdigest(), e['raw_quote_sha256'])
            self.assertEqual(hashlib.sha256(p['text'].encode()).hexdigest(), e['selected_text_sha256'])
            for m in p['mentions']:
                self.assertEqual(p['text'][m['start']:m['end']], m['surface'])
        casualties = next(m for m in c['paragraphs'][1]['mentions'] if m['surface'] == '子弟五人')
        self.assertIsNone(casualties['person_id'])
        self.assertIn('群體', casualties['interpretation_note'])

    def test_named_ancestors_connect_existing_wangyi_without_invented_direct_assertions(self):
        catalog = load_catalog(ROOT)
        _, assembled = load_assemblies(ROOT, catalog)
        for pid in ['7r6_k52_qji_ABDAC', '7r6_k52_qji_ABDACA']:
            self.assertEqual(assembled[pid]['parent_connection']['type'], 'parent_between_consecutive_ancestors')
        self.assertEqual(assembled['7r6_k52_qji_ABDAC']['parent_person_id'], '7r6_k52_qji_ABDA')
        hong = assembled['7r6_k52_qji_ABDACAB']
        self.assertEqual(hong['parent_connection']['type'], 'shared_father_through_sibling')
        self.assertEqual(hong['parent_person_id'], '7r6_k52_qji_ABDACA')
        assertions = json.loads((ROOT / 'corpus/songshu/092-assertions.json').read_text())['assertions']
        self.assertFalse(any(a['predicate'] == 'father' and a['subject_person_id'] in
                             ['7r6_k52_qji_ABDAC', '7r6_k52_qji_ABDACA', hong['person_id']] for a in assertions))
        relation = next(a for a in assertions if a['predicate'] == 'brother')
        for endpoint in ['subject_person_id', 'object_person_id']:
            self.assertIn(relation, bundle(relation[endpoint], ROOT, catalog=catalog)['relations'])

    def test_hongzhi_complete_unit_keeps_maternal_ancestor_outside_paternal_tree(self):
        catalog = load_catalog(ROOT)
        c = json.loads((ROOT / 'corpus/songshu/093.json').read_text())
        lines = [60, 62, 64, 66, 68]
        self.assertEqual([p['source_position']['first_line'] for p in c['paragraphs']
                          if p['source_position']['first_line'] in lines], lines)
        data = bundle('7r6_k52_qji_ABDACAB', ROOT, catalog=catalog)
        maternal = next(a for a in data['relations'] if a['id'] == 'a-songshu093-hongzhi-maternal-grandfather')
        self.assertEqual(maternal['predicate'], 'grandfather')
        self.assertEqual(maternal['qualifiers']['lineage'], 'maternal')
        self.assertIsNone(maternal['qualifiers']['mother_person_id'])
        self.assertFalse(any(a['predicate'] == 'mother' for a in data['relations']))
        _, assembled = load_assemblies(ROOT, catalog)
        self.assertNotEqual(assembled['7r6_k52_qji_ABDACAB']['parent_person_id'], maternal['object_person_id'])
        self.assertEqual(assembled['7r6_k52_qji_ABDACABA']['parent_person_id'], '7r6_k52_qji_ABDACAB')
        letter = next(p for p in c['paragraphs'] if p['source_position']['first_line'] == 66)
        family_reference = next(m for m in letter['mentions'] if m['surface'] == '君家')
        self.assertIsNone(family_reference['person_id'])

    def test_parallel_histories_share_people_without_erasing_place_spelling(self):
        song = json.loads((ROOT / 'corpus/songshu/093.json').read_text())
        nan = json.loads((ROOT / 'corpus/nanshi/024.json').read_text())
        sp = next(p for p in song['paragraphs'] if p['source_position']['first_line'] == 62)
        np = next(p for p in nan['paragraphs'] if p['source_position']['first_line'] == 77)
        self.assertIn('烏程令', sp['text'])
        self.assertIn('烏傷令', np['text'])
        self.assertNotIn('烏傷令', sp['text'])
        for paragraph in [sp, np]:
            mentions = [m for m in paragraph['mentions'] if m['surface'] == '弘之']
            self.assertTrue(mentions)
            self.assertEqual({m['person_id'] for m in mentions}, {'7r6_k52_qji_ABDACAB'})
        unit_lines = [71, 73, 77, 79, 81]
        self.assertEqual([p['source_position']['first_line'] for p in nan['paragraphs']
                          if p['source_position']['first_line'] in unit_lines], unit_lines)

    def test_source_life_years_keep_abbreviated_and_explicit_eras_separate(self):
        catalog = load_catalog(ROOT)
        zhen = bundle('7r6_k52_qji_ABDACAA', ROOT, catalog=catalog)
        hong = bundle('7r6_k52_qji_ABDACAB', ROOT, catalog=catalog)
        self.assertTrue(any(e.get('normalized_date', {}).get('year') == 422 for e in zhen['life_events']))
        abbreviated = next(e for e in hong['life_events'] if e['id'] == 'le-songshu-093-66-wang-received')
        explicit = next(e for e in hong['life_events'] if e['id'] == 'le-nanshi-024-81-wang-received')
        self.assertEqual(abbreviated['date_expression'], '四年')
        self.assertNotIn('normalized_date', abbreviated)
        self.assertEqual(explicit['normalized_date']['year'], 427)
        self.assertEqual(explicit['date_expression'], '元嘉四年')
        for data, age in [(zhen, 66), (hong, 63)]:
            report = next(a for a in data['age_assertions'] if a['value'] == age)
            self.assertIsNone(report['birth_year'])
            self.assertFalse(any(e['event_type'] == 'birth' for e in data['life_events']))
        tansheng = bundle('7r6_k52_qji_ABDACABA', ROOT, catalog=catalog)
        self.assertFalse(tansheng.get('life_events', []))

    def test_native_place_is_not_birth_and_mothers_tomb_is_not_persons_burial(self):
        catalog = load_catalog(ROOT)
        zhen = bundle('7r6_k52_qji_ABDACAA', ROOT, catalog=catalog)
        hong = bundle('7r6_k52_qji_ABDACAB', ROOT, catalog=catalog)
        self.assertEqual({a['relation'] for a in zhen['address_assertions']}, {'biographical_origin'})
        self.assertEqual({a['place']['source_name'] for a in hong['address_assertions']},
                         {'琅邪臨沂', '會稽上虞', '始寧沃川'})
        for data in [zhen, hong]:
            self.assertFalse(any(a['relation'] in ['birthplace', 'burial'] for a in data['address_assertions']))
            self.assertTrue(all(a['place']['modern_identification'] is None for a in data['address_assertions']))

    def test_langye_king_resolution_is_scoped_to_hongzhi_dated_service(self):
        song92 = json.loads((ROOT / 'corpus/songshu/092.json').read_text())
        unresolved = next(m for p in song92['paragraphs'] for m in p['mentions']
                          if m['surface'] == '琅邪王')
        self.assertIsNone(unresolved['person_id'])
        decisions = json.loads((ROOT / 'corpus/songshu/093-identities.json').read_text())['decisions']
        decision = next(d for d in decisions if d['id'] == 'd-song093-langye-zhongjun')
        self.assertEqual(decision['chapter_ids'], ['c-songshu-093-recluses'])
        self.assertIn('隆安', decision['evidence'][0]['quote'])
        self.assertTrue(all(r['source_revision'] == 2567072 for r in decision['references']))
        catalog = load_catalog(ROOT)
        person = bundle(decision['person_id'], ROOT, catalog=catalog)
        self.assertTrue(any(p['label'] == '晉恭帝德文' for p in person['persons']))

    def test_letter_first_person_has_the_named_author_not_the_deceased_subject(self):
        c = json.loads((ROOT / 'corpus/songshu/093.json').read_text())
        p = next(p for p in c['paragraphs'] if p['source_position']['first_line'] == 66)
        author = next(m['person_id'] for m in p['mentions'] if m['surface'] == '顏延之')
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] == '僕'}, {author})
        self.assertNotEqual(author, '7r6_k52_qji_ABDACAB')

    def test_unsuccessful_decline_does_not_remove_held_military_office(self):
        holdings = json.loads((ROOT / 'corpus/songshu/092-titles.json').read_text())['holdings']
        office = next(h for h in holdings if h['title'] == '建威將軍'
                      and h['evidence'][0]['paragraph_id'].endswith('line014'))
        self.assertEqual(office['person_id'], '7r6_k52_qji_ABDACAA')
        self.assertEqual(office['mode'], 'grant')
        self.assertIn('固辭，不見聽', office['evidence'][0]['quote'])
        self.assertIn('白衣領職', office['evidence'][0]['quote'])
        self.assertTrue(all(h['effective_period']['end']['status'] == 'unknown'
                            for h in holdings if h['person_id'] == '7r6_k52_qji_ABDACAA'))
        self.assertTrue(any(h['title'] == '華容縣五等男' and h['kind'] == 'noble_rank'
                            for h in holdings))

    def test_memorial_former_office_is_only_an_attestation(self):
        holdings = json.loads((ROOT / 'corpus/songshu/093-titles.json').read_text())['holdings']
        office = next(h for h in holdings if h['person_id'] == '7r6_k52_qji_ABDACAB'
                      and h['title'] == '員外散騎常侍')
        self.assertEqual(office['mode'], 'attestation')
        self.assertEqual(office['effective_period']['start']['status'], 'unknown')
        self.assertIn('並不就', office['evidence'][0]['quote'])
        a = office['attestations'][0]
        chapter = json.loads((ROOT / 'corpus/songshu/093.json').read_text())
        p = next(p for p in chapter['paragraphs'] if p['id'] == a['paragraph_id'])
        self.assertEqual(p['text'][a['start'] - 1], '前')

    def test_hongzhi_invitations_and_summons_remain_unassumed(self):
        from scripts.unassumed_appointments import unassumed_appointment_valid
        chapter = json.loads((ROOT / 'corpus/songshu/093.json').read_text())
        proposals = [p for p in chapter['annotation']['title_proposals']
                     if p['person_id'] == '7r6_k52_qji_ABDACAB']
        self.assertCountEqual([p['title'] for p in proposals], ['南蠻長史', '右軍司馬',
                              '徐州治中從事史', '員外散騎常侍', '庶子', '通直散騎常侍'])
        self.assertEqual(sum(p['appointment_stage'] == 'invitation' for p in proposals), 2)
        for proposal in proposals:
            self.assertTrue(unassumed_appointment_valid(proposal, chapter))
            altered = copy.deepcopy(proposal)
            altered['appointment_stage'] = ('appointment' if proposal['appointment_stage'] == 'invitation'
                                            else 'invitation')
            self.assertFalse(unassumed_appointment_valid(altered, chapter))
        self.assertTrue(all(p['outcome'] == 'not_assumed' for p in proposals))

    def test_wangsui_father_and_inverse_nephew_statement_keep_two_lineages(self):
        from scripts.uncle_parentage import explicit_maternal_uncle_valid
        catalog = load_catalog(ROOT)
        labels = {p['label']: p['id'] for p in catalog[0].values()}
        _, assembled = load_assemblies(ROOT, catalog)
        self.assertEqual(assembled[labels['王綏']]['parent_person_id'], labels['王愉'])
        self.assertEqual(assembled[labels['王綏']]['root_person_id'], labels['王澤'])
        self.assertEqual(assembled[labels['王愉']]['parent_person_id'], labels['王坦之'])
        self.assertNotEqual(assembled[labels['王綏']]['root_person_id'], '7r6_k52_qji')
        self.assertNotEqual(labels['王愉'], '7r6_k52_qji')
        data = bundle(labels['王綏'], ROOT, catalog=catalog)
        uncle = next(a for a in data['relations'] if a['id'] == 'a-songshu092-wangsui-maternal-uncle')
        self.assertEqual(uncle['object_person_id'], labels['桓玄'])
        self.assertIsNone(uncle['qualifiers']['mother_person_id'])
        chapter = json.loads((ROOT / 'corpus/songshu/092.json').read_text())
        paragraphs = {p['id']: (chapter['id'], p) for p in chapter['paragraphs']}
        self.assertTrue(explicit_maternal_uncle_valid(uncle, paragraphs))
        changed = copy.deepcopy(uncle)
        changed['object_person_id'] = labels['王愉']
        self.assertFalse(explicit_maternal_uncle_valid(changed, paragraphs))
        changed = copy.deepcopy(uncle)
        changed['qualifiers']['source_term'] = '玄之甥'
        self.assertFalse(explicit_maternal_uncle_valid(changed, paragraphs))
        self.assertFalse(any(a['predicate'] == 'mother' for a in data['relations']))

    def test_full_written_name_includes_surname_and_keeps_existing_anchor_ids(self):
        c = json.loads((ROOT / 'corpus/songshu/093.json').read_text())
        found = 0
        for p in c['paragraphs']:
            for match in re.finditer('王弘之', p['text']):
                mention = next(m for m in p['mentions'] if m['start'] == match.start()
                               and m['end'] == match.end())
                self.assertEqual(mention['surface'], '王弘之')
                self.assertEqual(mention['person_id'], '7r6_k52_qji_ABDACAB')
                found += 1
        self.assertEqual(found, 4)
        anchors = {m['id']: m for p in c['paragraphs'] for m in p['mentions']}
        self.assertEqual(anchors['c-songshu-093-recluses:line062:m0273']['start'], 272)
        self.assertEqual(anchors['c-songshu-093-recluses:line064:m0169']['start'], 168)


if __name__ == '__main__':
    unittest.main()
