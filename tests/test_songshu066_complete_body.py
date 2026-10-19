# coding: utf-8
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(f):
    return json.loads((ROOT/f).read_text())

class WangJinghongCompleteBody(unittest.TestCase):
    def setUp(self):
        self.c=read('corpus/songshu/066.json')
        self.paragraphs={p['id']:p for p in self.c['paragraphs']}
        self.decisions={d['id']:d for d in read('corpus/songshu/066-identities.json')['decisions']}
        self.jinghong=self.c['paragraphs'][0]['mentions'][0]['person_id']

    def paragraph(self,line):
        return self.paragraphs[self.c['id']+':line'+str(line).zfill(3)]

    def test_nine_complete_source_units_match_separate_apparatus(self):
        expected=[self.c['id']+':p001']+[self.c['id']+':line'+str(n).zfill(3)for n in range(12,27,2)]
        excerpts={e['proposed_paragraph_id']:e for e in self.c['source']['normalization']['excerpts']}
        for pid in expected:
            raw=excerpts[pid]['raw_quote']
            self.assertEqual(self.paragraphs[pid]['text'],re.sub(r'<ref>.*?</ref>','',raw).strip())
        death=self.paragraph(22)
        self.assertIn('時年八十八',death['text'])
        self.assertNotIn('據南史訂正',death['text'])
        self.assertTrue(any('八十' in note['text']for note in excerpts[death['id']]['removed_digital_editorial_notes']))

    def test_three_reigns_and_recalled_first_emperor_do_not_share_one_id(self):
        taizu=self.decisions['d-songshu066-full-taizu']['person_id']
        shundi=self.decisions['d-songshu066-full-shundi']['person_id']
        gaozu=next(m['person_id']for m in self.c['paragraphs'][0]['mentions']if m['surface']=='高祖')
        self.assertEqual(len({taizu,shundi,gaozu}),3)
        for m in self.paragraph(20)['mentions']:
            if m['surface']=='陛下':self.assertEqual(m['person_id'],taizu)
            if m['surface']=='先帝':self.assertEqual(m['person_id'],gaozu)
            if m['surface']in ['臣','微臣']:self.assertEqual(m['person_id'],self.jinghong)
        self.assertEqual(next(m['person_id']for m in self.paragraph(22)['mentions']if m['surface']=='順帝'),shundi)

    def test_shang_in_memorial_verbs_and_taizi_in_office_are_not_persons(self):
        p=self.paragraph(20)
        starts={m['start']for m in p['mentions']if m.get('person_id')}
        for match in re.finditer('上表',p['text']):self.assertNotIn(match.start(),starts)
        for match in re.finditer('太子少傅',p['text']):
            self.assertFalse(any(m.get('person_id')and m['start']<match.end()and m['end']>match.start()for m in p['mentions']))

    def test_collective_maids_remain_unresolved_and_speaker_is_jinghong(self):
        p=self.paragraph(24)
        for surface in ['二老婢','二婢','兒孫']:
            mentions=[m for m in p['mentions']if m['surface']==surface]
            self.assertTrue(mentions)
            self.assertTrue(all(m.get('person_id')is None for m in mentions))
        self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='吾'),self.jinghong)
        self.assertNotEqual(next(m['person_id']for m in p['mentions']if m['surface']=='汝'),self.jinghong)

if __name__=='__main__':
    unittest.main()
