import copy
import json
import unittest
from pathlib import Path
from scripts.validate_corpus import normalized_date_errors, title_proposal_errors
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class WangBridges065(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = read('corpus/jinshu/065.json')
        cls.people = {p['label']: p['id'] for p in read('registry/persons.json')['persons']}
        cls.rels = read('corpus/jinshu/065-assertions.json')['assertions']
        cls.holdings = read('corpus/jinshu/065-titles.json')['holdings']

    def test_direct_jin_fathers_replace_inference_without_erasing_song(self):
        _, members = load_assemblies(ROOT, load_catalog(ROOT))
        for child, parent in [('王洽', '王導'), ('王珣', '王洽'), ('王弘', '王珣')]:
            m = members[self.people[child]]
            a = next(a for a in self.rels if a['id'] == m['source_assertion_id'])
            self.assertEqual((a['subject_person_id'], a['object_person_id']),
                             (self.people[child], self.people[parent]))
            self.assertNotIn('parent_connection', m)
        song = read('corpus/songshu/042-assertions.json')['assertions']
        self.assertEqual({a['predicate'] for a in song}, {'father', 'grandfather', 'great_grandfather'})

    def test_body_six_sons_does_not_repeat_digital_header_error(self):
        sons = {a['subject_person_id'] for a in self.rels if a['predicate'] == 'father'
                and a['object_person_id'] == self.people['王導']}
        self.assertEqual(sons, {self.people[n] for n in ['王悅', '王恬', '王洽', '王協', '王邵', '王薈']})
        self.assertNotIn(self.people['王珣'], sons)
        self.assertTrue(all('notes=' not in p['text'] for p in self.c['paragraphs']))
        self.assertTrue(all('birth_order' not in a['qualifiers'] for a in self.rels
                            if a['predicate'] == 'father' and a['object_person_id'] == self.people['王導']))

    def test_cousin_age_is_preserved_without_fabricated_distance(self):
        cousins = [a for a in self.rels if a['predicate'] == 'agnatic_cousin']
        self.assertEqual(len(cousins), 2)
        for a in cousins:
            k = a['qualifiers']['kinship_structure']
            self.assertIsNone(k['distance'])
            self.assertIsNone(k['common_ancestor_person_id'])
            self.assertEqual(k['generation_difference'], 0)
        older = next(a for a in cousins if a['subject_person_id'] == self.people['王敦'])
        self.assertEqual(older['qualifiers']['relative_birth_order']['younger_person_id'], self.people['王導'])
        younger = next(a for a in cousins if a['subject_person_id'] == self.people['王獻之'])
        self.assertEqual(younger['qualifiers']['relative_birth_order']['older_person_id'], self.people['王珣'])

    def test_refused_offices_are_not_held_or_life_endpoints(self):
        proposals = self.c['annotation']['title_proposals']
        original_ids=['tp-jinshu065-wangqia-zhongshuling', 'tp-jinshu065-wangdao-87', 'tp-jinshu065-wangdao-93', 'tp-jinshu065-wangdao-97', 'tp-jinshu065-wangdao-102']
        self.assertEqual(len([p for p in proposals if p['id'] in original_ids]),5)
        self.assertEqual({p['id']for p in proposals},set(original_ids)|{'tp-wangdao4-80-4','tp-wangdao4-110-6'})
        for p in proposals:
            self.assertEqual(title_proposal_errors(p, self.c, set(self.people.values())), [])
            if p['id'] in original_ids:
                self.assertFalse(any(h['person_id']==p['person_id'] and h['title']==p['title'] for h in self.holdings))
            else:
                self.assertFalse(any(h['person_id']==p['person_id'] and h['title']==p['title'] and any(a['paragraph_id']==p['role_anchor']['paragraph_id'] and a['start']==p['role_anchor']['start'] and a['end']==p['role_anchor']['end'] for a in h['attestations'])for h in self.holdings))
        # Later grant is a distinct event; refusal cannot erase it.
        later=next(h for h in self.holdings if h['id']=='th-wangdao4-84-213-098')
        self.assertEqual((later['person_id'],later['title'],later['mode']),('7r6_k52_qji_ABAAAA','散騎常侍','grant'))
        self.assertEqual(later['attestations'][0]['paragraph_id'],'c-jinshu-065-wangdao-family:line084')
        original_holding_ids=['th-jinshu065-wang-001', 'th-jinshu065-wang-002', 'th-jinshu065-wang-003', 'th-jinshu065-wang-004', 'th-jinshu065-wang-005', 'th-jinshu065-wang-006', 'th-jinshu065-wang-007', 'th-jinshu065-wang-008', 'th-jinshu065-wang-009', 'th-jinshu065-wang-010', 'th-jinshu065-wang-011']
        self.assertEqual(len([h for h in self.holdings if h['id'] in original_holding_ids]),11)
        self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in self.holdings if h['id'] in original_holding_ids))
        expected_ends={'th-wangdao4-20-225-015': '後坐事除節', 'th-wangdao4-20-184-009': '解揚州', 'th-wangdao4-36-237-032': '解大司馬', 'th-wangdao4-50-16-035': '解大司馬', 'th-wangdao4-36-76-028': '罷司徒官以並之', 'th-wangdao4-84-188-095': '上所假節'}
        ended={h['id']:h for h in self.holdings if h['effective_period']['end']['status']!='unknown'}
        self.assertEqual(set(ended),set(expected_ends))
        for hid,term in expected_ends.items():
            end=ended[hid]['effective_period']['end']
            self.assertEqual(end['status'],'source_event')
            self.assertTrue(any(term in e['quote']for e in end['evidence']))
            self.assertNotIn(end['event_type'],['death','life_end'])
        self.assertTrue(any(h['person_id'] == self.people['王洽'] and h['title'] == '中書郎' for h in self.holdings))

    def test_death_keeps_original_spelling_and_age_without_birth_estimate(self):
        age = self.c['annotation']['age_assertions'][0]
        death = read('corpus/jinshu/065-life-events.json')['events'][0]
        self.assertEqual(age['value'], 36)
        self.assertIsNone(age['birth_year'])
        self.assertEqual(death['normalized_date']['year'], 358)
        self.assertEqual(death['date_expression'], '昇平二年')
        self.assertEqual(death['normalized_date']['references'][0]['quote'], '升平')
        self.assertEqual(normalized_date_errors(death['normalized_date']), [])
        for year in [357, 359]:
            bad = copy.deepcopy(death['normalized_date'])
            bad.update(year=year, era_year=year)
            self.assertTrue(normalized_date_errors(bad))

    def test_era_spelling_exception_does_not_accept_arbitrary_names_or_changed_table(self):
        date = read('corpus/jinshu/065-life-events.json')['events'][0]['normalized_date']
        bad = copy.deepcopy(date)
        bad['regnal_year_mapping']['source_era_name'] = '太平'
        bad['source_expression'] = '太平二年'
        bad['original_quote'] = '太平二年卒於官'
        self.assertTrue(normalized_date_errors(bad))
        bad = copy.deepcopy(date)
        bad['references'][0]['columns']['first_year'] = '358'
        self.assertTrue(normalized_date_errors(bad))

    def test_fahu_is_childhood_name_and_not_given_name(self):
        p = next(n for n in read('data/corpus/profile-names.json')['records']
                 if n['person_id'] == self.people['王珣'])
        self.assertEqual(p['ming'], '珣')
        self.assertIn('法護', p['additional_names'])
        self.assertTrue(any('法護，珣小字也' in ref['quote'] for ref in p['references']))
        d = next(d for d in read('corpus/jinshu/065-identities.json')['decisions'] if d['id'] == 'd-jinshu065-xun-fahu')
        self.assertEqual(d['person_id'], self.people['王珣'])

    def test_source_characters_and_excerpt_hashes_remain_stable(self):
        import hashlib
        for p, x in zip(self.c['paragraphs'], self.c['source']['normalization']['excerpts']):
            self.assertEqual(hashlib.sha256(p['text'].encode()).hexdigest(), x['selected_text_sha256'])
        paragraphs_by_source_line = {p['source_position']['first_line']: p for p in self.c['paragraphs']}
        self.assertEqual(len(self.c['paragraphs']), 45)
        self.assertTrue({12, 60, 74, 88}.issubset(paragraphs_by_source_line))
        self.assertEqual(self.c['source']['text_scope'], 'full_chapter')
        self.assertIn('邵', paragraphs_by_source_line[60]['text'])
        self.assertIn('昇平二年', paragraphs_by_source_line[74]['text'])
        self.assertEqual(self.c['source']['revision_id'], 1756144)


if __name__ == '__main__':
    unittest.main()
