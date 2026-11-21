import copy
import json
import unittest
from pathlib import Path

from scripts.non_parental_family import non_parental_relation_valid

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


class XieCaiqingAndZaoTest(unittest.TestCase):
    def test_rearing_assertion_links_the_orphan_and_caregiver_in_both_texts(self):
        for source, chapter in [('nanshi', '019-xiezao'), ('liangshu', '050-xiezao')]:
            base = f'corpus/{source}/{chapter}'
            data = load(base + '.json')
            p = data['paragraphs'][0]
            paragraphs = {p['id']: (data['id'], p)}
            assertions = load(base + '-assertions.json')['assertions']
            care, = [row for row in assertions if row['predicate'] == 'raised_by']
            father, = [row for row in assertions if row['predicate'] == 'father']
            self.assertTrue(non_parental_relation_valid(care, paragraphs))
            self.assertEqual(care['subject_person_id'], father['subject_person_id'])
            self.assertNotEqual(care['object_person_id'], father['object_person_id'])
            # The father appears beside the orphan, but he is not the caregiver.
            wrong = copy.deepcopy(care)
            wrong['object_person_id'] = father['object_person_id']
            wrong['evidence'][0]['object_person_mention_id'] = father['evidence'][0]['object_person_mention_id']
            self.assertFalse(non_parental_relation_valid(wrong, paragraphs))

    def test_prison_death_is_only_assigned_where_the_verb_names_its_subject(self):
        earlier = 'corpus/nanqishu/036-wangyongxian-caiqing'
        later = 'corpus/nanshi/019-wangyongxian-caiqing'
        event, = load(earlier + '-life-events.json')['events']
        p = load(earlier + '.json')['paragraphs'][0]
        named = next(m for m in p['mentions'] if m['id'] == event['evidence'][0]['person_mention_id'])
        self.assertEqual(named['surface'], '永先')
        self.assertEqual(named['person_id'], event['person_id'])
        self.assertTrue(p['text'].endswith('永先於獄自盡。'))
        other = load(later + '.json')['paragraphs'][0]
        self.assertTrue(other['text'].endswith('永先於獄盡之。'))
        self.assertTrue(any(m['surface'] == '之' and m['kind'] == 'unresolved' for m in other['mentions']))
        self.assertFalse((ROOT / (later + '-life-events.json')).exists())
