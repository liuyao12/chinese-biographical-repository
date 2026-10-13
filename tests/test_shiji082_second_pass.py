import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class TianDanSecondPassTests(unittest.TestCase):
    def test_group_soldiers_are_not_the_anonymous_teacher(self):
        c = json.loads((ROOT / 'corpus/shiji/082.json').read_text())
        p = c['paragraphs'][2]
        mentions = {m['id']:m for m in p['mentions']}
        for suffix in ('0009', '0165'):
            m = mentions['c-shiji-082-tiandan:m003-' + suffix]
            self.assertIsNone(m['person_id'])
            self.assertEqual(m['kind'], 'unresolved')
        self.assertEqual(mentions['c-shiji-082-tiandan:m003-0110']['person_id'], 'lwi_cje_46s')
        people = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        person = next(p for p in people if p['id'] == 'lwi_cje_46s')
        self.assertNotIn('c-shiji-082-tiandan:m003-0009', {e['mention_id'] for e in person['evidence']})

    def test_min_and_naochi_share_ids_without_harmonizing_story(self):
        c = json.loads((ROOT / 'corpus/shiji/082.json').read_text())
        p = c['paragraphs'][0]
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] in ('湣王', '齊湣王')}, {'lmu_nbm_rzo_AAAAAAABAAAAAAAA'})
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] == '淖齒'}, {'fvc_9z0_643'})
        self.assertIn('因堅守，距燕軍', p['text'])
        parallel = json.loads((ROOT / 'corpus/shiji/046.json').read_text())
        self.assertIn('與燕共分', next(p for p in parallel['paragraphs'] if p['id'].endswith(':p047'))['text'])
