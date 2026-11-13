# coding: utf-8
import json
import copy
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

    def test_wangdongshan_person_mark_and_three_identity_decisions_are_source_bound(self):
        pid='7r6_k52_qji_ABDABAA'
        wang=self.paragraph(24)
        alias=next(m for m in wang['mentions']if m['id']==self.c['id']+':line024:m0045')
        self.assertEqual((alias['start'],alias['end'],alias['surface'],alias['person_id']),(45,48,'王東山',pid))
        xml=(ROOT/'corpus/songshu/066.xml').read_text()
        self.assertIn('<persName id="'+alias['id']+'" ref="'+pid+'">王東山</persName>',xml)

        expected={
            'd-songshu066-wangdongshan':(pid,'王東山',self.c['id']+':line024:m0045',24),
            'd-songshu066-lingbao-huanxuan':('u9s_w6j_8mc_AAF','靈寶',self.c['id']+':line012:m0071',12),
            'd-songshu066-shidi-liuyu':('3qs_nqa_ioa_AAA','先帝',self.c['id']+':line020:m0376',20),
        }
        for did,(person_id,surface,mid,line) in expected.items():
            d=self.decisions[did]
            self.assertEqual(d['person_id'],person_id)
            self.assertEqual(d['surfaces'],[surface])
            self.assertEqual(d['identification_basis']['target_mention_ids'],[mid])
            p=self.paragraph(line)
            target=next(m for m in p['mentions']if m['id']==mid)
            self.assertEqual((target['surface'],target['person_id']),(surface,person_id))
            self.assertTrue(any(e['paragraph_id']==p['id'] and e['quote']==p['text'] for e in d['evidence']))
            self.assertFalse(d['human_reviewed'])

    def test_new_identity_decision_mutations_break_the_fixed_source_binding(self):
        expected={
            'd-songshu066-wangdongshan':('7r6_k52_qji_ABDABAA','王東山',self.c['id']+':line024:m0045'),
            'd-songshu066-lingbao-huanxuan':('u9s_w6j_8mc_AAF','靈寶',self.c['id']+':line012:m0071'),
            'd-songshu066-shidi-liuyu':('3qs_nqa_ioa_AAA','先帝',self.c['id']+':line020:m0376'),
        }
        for did,(person_id,surface,mid) in expected.items():
            original=self.decisions[did]
            for field,value in [('person_id','3qs_nqa_ioa_AAAA'),('surface','誤名'),('mention_id',self.c['id']+':line001:m0000')]:
                bad=copy.deepcopy(original)
                if field=='person_id':bad['person_id']=value
                elif field=='surface':bad['surfaces']=[value]
                else:bad['identification_basis']['target_mention_ids']=[value]
                self.assertFalse(self._identity_binding_matches(bad,person_id,surface,mid),(did,field))

    def _identity_binding_matches(self,decision,person_id,surface,mid):
        if decision.get('person_id')!=person_id or decision.get('surfaces')!=[surface]:return False
        if decision.get('identification_basis',{}).get('target_mention_ids')!=[mid]:return False
        hit=next((p for p in self.c['paragraphs']if any(m['id']==mid for m in p.get('mentions',[]))),None)
        if not hit:return False
        target=next(m for m in hit['mentions']if m['id']==mid)
        return target.get('surface')==surface and target.get('person_id')==person_id

if __name__=='__main__':
    unittest.main()
