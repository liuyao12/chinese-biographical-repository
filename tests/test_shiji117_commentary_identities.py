"""Commentary resolves a name without making the literary scene an event."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = {'c-shiji-117-xiangru:m020-0038': ('孫叔', 'yay_w6f_lis_A'),
         'c-shiji-117-xiangru:m020-0043': ('衛公', '5dd_l1c_6g8'),
         'c-shiji-117-xiangru:m069-0008': ('平陵侯', 'ior_a2u_f1c')}

def read(path):
    return json.loads((ROOT / path).read_text())

class XiangruCommentaryIdentities(unittest.TestCase):
    def test_exact_three_existing_anchors_keep_their_received_names(self):
        chapter = read('corpus/shiji/117.json')
        mentions = {m['id']: (p, m) for p in chapter['paragraphs'] for m in p['mentions']}
        for mid, (surface, pid) in CASES.items():
            p, m = mentions[mid]
            self.assertEqual(m['surface'], surface)
            self.assertEqual(p['text'][m['start']:m['end']], surface)
            self.assertEqual(m['person_id'], pid)
            self.assertEqual(m['kind'], 'person')
            self.assertEqual(m['status'], 'contextual_provisional')

    def test_every_identification_keeps_commentary_and_parallel_evidence(self):
        decisions = read('corpus/shiji/117-identities.json')['decisions']
        self.assertEqual(len(decisions), 3)
        for d in decisions:
            self.assertEqual(set(d['chapter_ids']), {'c-shiji-117-xiangru', 'c-shiji-111-wei-huo'})
            mid, = d['identification_basis']['target_mention_ids']
            self.assertEqual(d['person_id'], CASES[mid][1])
            self.assertTrue(d['identification_basis']['historical_event_attendance_not_inferred'])
            self.assertFalse(d['human_reviewed'])
            self.assertEqual({e['chapter_id'] for e in d['evidence']}, set(d['chapter_ids']))
            ref, = d['references']
            self.assertEqual(ref['source_commit'], '73c4d2ba067d99a6de924ac952fd6921a958c7e7')
            self.assertIn(ref['source_commit'], ref['url'])
            self.assertEqual(len(ref['source_blob']), 40)
            self.assertEqual(len(ref['response_sha256']), 64)
            self.assertEqual(ref['scope'], 'ancient_commentary_identification')
            self.assertFalse(ref['image_verified'])

    def test_registry_indexes_received_forms_without_new_people(self):
        people = {p['id']: p for p in read('registry/persons.json')['persons']}
        for mid, (surface, pid) in CASES.items():
            self.assertTrue(any(a['surface'] == surface and mid in a['mention_ids']
                                for a in people[pid]['aliases']))
            self.assertTrue(any(e['mention_id'] == mid for e in people[pid]['evidence']))
        for pid, label in [('yay_w6f_lis_A', '公孫賀'), ('5dd_l1c_6g8', '衛青'), ('ior_a2u_f1c', '蘇建')]:
            self.assertEqual(people[pid]['label'], label)

    def test_other_literary_and_unnamed_roles_are_not_absorbed(self):
        chapter = read('corpus/shiji/117.json')
        mentions = {m['id']: m for p in chapter['paragraphs'] for m in p['mentions']}
        for mid in ['c-shiji-117-xiangru:m020-0009', 'c-shiji-117-xiangru:m059-0002',
                    'c-shiji-117-xiangru:m069-0014']:
            self.assertIsNone(mentions[mid]['person_id'])
        notes = '\n'.join(chapter['annotation']['limitations'])
        self.assertIn('賦中校獵不作確定共同事件', notes)
        self.assertNotIn('平陵侯及五公子由著作題名引出，未定身分', notes)

if __name__ == '__main__':
    unittest.main()
