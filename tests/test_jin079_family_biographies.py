import copy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.jin079_family_awards import succession_valid, valid

ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))


class XieYanHunReading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ch=load('corpus/jinshu/079.json')
        cls.paras={p['id']:(cls.ch['id'],p) for p in cls.ch['paragraphs']}
        cls.mentions={m['id']:(cls.ch['id'],p['id'],m) for p in cls.ch['paragraphs'] for m in p['mentions']}
        cls.deaths={e['id']:e for e in load('corpus/jinshu/079-life-events.json')['events']}
        cls.ts=[h for h in load('corpus/jinshu/079-titles.json')['holdings'] if h['id'].startswith('th-jin079-yan-hun-')]
        cls.review=load('source-evidence/jin079-xieyan-xiehun/reading.json')

    def test_all_primary_witnesses_and_offsets(self):
        for row in self.review['name_comparisons']:
            for citation in row['parallel_passages']:
                raw=(ROOT/citation['raw_path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(),citation['raw_sha256'])
                self.assertEqual(raw.decode()[citation['raw_start']:citation['raw_end']],citation['quote'])
        self.assertIn('宜城宣君',[r['source_surface'] for r in self.review['name_comparisons'] if r['person_id']])
        self.assertIsNone(next(r for r in self.review['name_comparisons'] if r['source_surface']=='武侯')['person_id'])

    def test_distinct_posthumous_awards(self):
        gifts=[h for h in self.ts if h['mode'].startswith('posthumous')]
        self.assertEqual(len(gifts),5)
        for h in gifts:
            self.assertTrue(valid(h,self.paras,self.mentions,self.deaths),h['id'])
            bad=copy.deepcopy(h);bad['person_id']='another-person'
            self.assertFalse(valid(bad,self.paras,self.mentions,self.deaths))
            bad=copy.deepcopy(h);bad['attestations'][0]['start']+=1
            self.assertFalse(valid(bad,self.paras,self.mentions,self.deaths))

    def test_distinct_noble_succession_and_abolition(self):
        events=[e for e in load('corpus/jinshu/079-events.json')['events'] if e['source_clause_binding']['kind']=='jin079_named_noble_successor']
        self.assertEqual(len(events),3)
        for event in events:
            self.assertTrue(succession_valid(event,self.paras),event['id'])
            bad=copy.deepcopy(event); bad['title']='別爵'
            self.assertFalse(succession_valid(bad,self.paras))

    def test_annual_death_headings_months_and_days(self):
        ch=load('corpus/jinshu/010-xieyan-xiehun.json')
        raw=(ROOT/ch['source']['raw_path']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),ch['source']['raw_file_sha256'])
        dates=load('corpus/jinshu/010-xieyan-xiehun-life-events.json')['events']
        for row,p in zip(self.review['parallel_annal_deaths'],ch['paragraphs']):
            snippets=[raw.decode()[s['raw_start']:s['raw_end']] for s in p['source_fragments']]
            self.assertEqual('\n'.join(snippets),p['text'])
            self.assertTrue(snippets[-1].startswith(row['sexagenary_day']+'，'))
            death=next(e for e in dates if e['id']==row['native_annal_death_id'])
            self.assertEqual(death['person_id'],row['person_id'])
            self.assertEqual(death['normalized_date']['year'],row['year'])
        self.assertEqual([(r['year'],r['lunar_month'],r['sexagenary_day']) for r in self.review['parallel_annal_deaths']],[(400,5,'己卯'),(412,9,'己卯')])
