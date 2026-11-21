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

    def roles(self, paragraph):
        return [m for m in self.c['annotation']['person_reference_occurrences'] if m['paragraph_id']==paragraph['id']]

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
        gaozu=next(m['person_id']for m in self.roles(self.c['paragraphs'][0])if m['surface']=='高祖')
        self.assertEqual(len({taizu,shundi,gaozu}),3)
        roles=self.roles(self.paragraph(20))
        self.assertTrue({'先帝','陛下','臣','微臣'}.issubset({r['surface'] for r in roles}))
        for m in roles:
            if m['surface']=='陛下':self.assertEqual(m['person_id'],taizu)
            if m['surface']=='先帝':self.assertEqual(m['person_id'],gaozu)
            if m['surface']in ['臣','微臣']:self.assertEqual(m['person_id'],self.jinghong)
        self.assertEqual(next(m['person_id']for m in self.roles(self.paragraph(22))if m['surface']=='順帝'),shundi)

    def test_shang_in_memorial_verbs_and_taizi_in_office_are_not_persons(self):
        p=self.paragraph(20)
        resolved=p['mentions']+self.roles(p)
        starts={m['start']for m in resolved if m.get('person_id')}
        for match in re.finditer('上表',p['text']):self.assertNotIn(match.start(),starts)
        for match in re.finditer('太子少傅',p['text']):
            self.assertFalse(any(m.get('person_id')and m['start']<match.end()and m['end']>match.start()for m in resolved))

    def test_collective_maids_remain_unresolved_and_speaker_is_jinghong(self):
        p=self.paragraph(24)
        for surface in ['二老婢','二婢','兒孫']:
            mentions=[m for m in p['mentions']if m['surface']==surface]
            self.assertTrue(mentions)
            self.assertTrue(all(m.get('person_id')is None for m in mentions))
        roles={r['surface']:r for r in self.roles(p) if r['surface'] in ('吾','汝')}
        self.assertEqual((roles['吾']['id'],roles['吾']['referent_role'],roles['吾']['person_id']),
                         (p['id']+':m0225','speaker_self',self.jinghong))
        self.assertEqual((roles['汝']['id'],roles['汝']['referent_role'],roles['汝']['person_id']),
                         (p['id']+':m0228','addressee','7r6_k52_qji_ABDABAAA'))
        self.assertFalse(any(m['surface'] in roles for m in p['mentions']))

    def test_issued_decisions_and_reclassified_holding_remain_addressable(self):
        from copy import deepcopy
        from scripts.scoped_reference_decisions import scoped_reference_decision_valid
        other=read('corpus/songshu/044.json')
        chapters={c['id']:c for c in (self.c,other)}
        issued=set(self.c['annotation']['received_reference_decision_ids'])
        self.assertEqual(len(issued),5)
        self.assertEqual(set(self.decisions),issued|{'d-songshu066-full-daogui'})
        for did in issued:
            dec=self.decisions[did]
            self.assertTrue(scoped_reference_decision_valid(dec,chapters))
            wrong=deepcopy(dec)
            wrong['person_id']='unrelated'
            self.assertFalse(scoped_reference_decision_valid(wrong,chapters))
        cross=self.decisions['d-songshu-066-cross-001']['identification_basis']
        self.assertEqual(cross['target_mention_ids'],[other['paragraphs'][0]['id']+':m0037'])
        titles=read('corpus/songshu/066-titles.json')
        ident='th-wang-full-s-24-188'
        old,=[x for x in titles['superseded_holdings'] if x['id']==ident]
        new,=[p for p in self.c['annotation']['title_proposals'] if p.get('former_holding_id')==ident]
        self.assertFalse(any(h['id']==ident for h in titles['holdings']))
        self.assertEqual(old['replacement_id'],new['id'])
        self.assertEqual(old['original_record']['title'],new['title'])
        self.assertEqual(new['outcome'],'not_assumed')
        self.assertIn('太祖嘉而許之',new['source_frame'])


if __name__=='__main__':
    unittest.main()
