"""跨本辭句及分篇起訖須能直接回到當時核讀的原段。"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


class XunWitnesses(unittest.TestCase):
    def test_anchors_match_each_fixed_witness(self):
        record = load('source-evidence/jin075-xun-rui-and-song/song-and-guan.json')
        for name, witness in record['cross_witnesses'].items():
            with self.subTest(name=name):
                raw = (ROOT / witness['path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), witness['sha256'])
                line = raw.decode().splitlines()[witness['line'] - 1]
                self.assertEqual(line[witness['start']:witness['end']], witness['quote'])
        peers = record['cross_witnesses']
        self.assertIn('數十人', peers['灌救父']['quote'])
        self.assertIn('數千人', peers['灌傳']['quote'])
        self.assertIn('兵三千', peers['訪子']['quote'])

    def test_succession_and_boat_year_have_separate_sources(self):
        record = load('source-evidence/jin075-xun-rui-and-song/reading.json')
        death = next(x for x in record['chronology'] if x['event'] == '荀崧薨')
        boat = next(x for x in record['chronology'] if x['event'] == '奉成帝御溫嶠舟')
        self.assertEqual((death['ce_year'], boat['ce_year']), (328, 329))
        self.assertIn('子籍嗣位', record['relationships'][1]['quote'])
        self.assertIn('籍嗣位', record['extent']['fixed_text']['quote'])
        self.assertNotIn('子籍嗣位', record['extent']['fixed_text']['quote'])

    def test_daughter_and_heir_each_keep_their_source_roles(self):
        assertions = load('corpus/nanshi/019-xiehui-assertions.json')['assertions']
        links = {a['predicate']: a for a in assertions if a['id'].startswith('a-nanshi019-xiehui-daughter-')}
        self.assertEqual(links['father']['subject_person_id'], links['spouse']['subject_person_id'])
        self.assertNotEqual(links['father']['object_person_id'], links['spouse']['object_person_id'])
        report = load('source-evidence/jin079-shang-xuan/huan-lingyun.json')
        first, second = report['units']
        self.assertEqual(first['range'][1], second['range'][0])
        self.assertTrue(first['quote'].endswith('早卒。'))
        self.assertTrue(second['quote'].startswith('子靈運嗣。'))
        ref, = [r for r in second['mentions'] if r['surface'] == '世子']
        self.assertEqual(ref['person_id'], '0ab_f5d_337')
