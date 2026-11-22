"""王素兩源所報卒時、族親及相鄰具名世次分別核證。"""
import copy
import json
from pathlib import Path
import unittest

from scripts import nanshi024_wangsu as study
from scripts.relative_regnal_year import relative_regnal_year_valid
from scripts.validate_corpus import source_age_number

ROOT = Path(__file__).resolve().parents[1]

def read(filename):
    return json.loads((ROOT / filename).read_text())

class WangSuWitnesses(unittest.TestCase):
    def test_date_and_mother(self):
        song = read('corpus/songshu/093-wangsu.json')
        events = read('corpus/songshu/093-wangsu-life-events.json')['events']
        death, mother = events
        date = death['normalized_date']
        chapters = {song['id']: song}
        self.assertEqual((death['date_expression'],date['year']),('七年',471))
        self.assertTrue(relative_regnal_year_valid(date,source_age_number,chapters))
        bad = copy.deepcopy(date)
        bad['narrative_era_scope']['era_ruler_person_id'] = 'hx8_st4_jdd'
        self.assertFalse(relative_regnal_year_valid(bad,source_age_number,chapters))
        bad = dict(death,person_id=mother['person_id'])
        self.assertFalse(study.death_valid(bad,bad['evidence'][0],song,ROOT))
        nan_death, = read('corpus/nanshi/024-wangsu-life-events.json')['events']
        self.assertIsNone(nan_death['date_expression'])
        self.assertNotIn('normalized_date',nan_death)

    def test_ancestry_is_attached_to_the_reported_head(self):
        chapter = read('corpus/nanshi/024-wangsu.json')
        chapters = {chapter['id']:chapter}
        assertions = {a['id']:a for a in read('corpus/nanshi/024-wangsu-assertions.json')['assertions']}
        assembly = next(a for a in read('registry/family-assemblies.json')['assemblies']
                        if a['id']=='family-nanshi024-wangsu-s')
        items = {m['person_id']:m for m in assembly['members']}
        child = assembly['members'][1]
        self.assertTrue(study.four_ancestor_pair(child,items,assertions,chapters,ROOT))
        bad = copy.deepcopy(child)
        bad['parent_connection']['farther_ancestor_assertion_id'] = 'a-nanshi024-wangsu-reported-bin'
        self.assertFalse(study.four_ancestor_pair(bad,items,assertions,chapters,ROOT))
        far = assertions['a-nanshi024-wangsu-reported-bin']
        self.assertEqual(far['qualifiers']['reported_generation_number'],5)
        self.assertIsNone(far['qualifiers']['generation_distance'])
        self.assertFalse(far['qualifiers']['adopted_for_family_tree'])
        for q in read('corpus/songshu/093-wangsu.json')['annotation']['title_proposals']:
            self.assertIn(q['title'],('倉曹屬','太子中舍人'))
            self.assertNotIn(q['title'], {h['title'] for h in read('corpus/songshu/093-wangsu-titles.json')['holdings']})
