# coding: utf-8
import json
from pathlib import Path
import unittest
from scripts.person_bundle import bundle
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
class MarriageContext(unittest.TestCase):
    def test_marriage_zhuo_is_wenjun_but_other_clan_mentions_are_not(self):
        c=read('corpus/shiji/117.json');ms={m['id']:m for p in c['paragraphs']for m in p['mentions']}
        m=ms['c-shiji-117-xiangru:m045-0016'];self.assertEqual((m['surface'],m['person_id']),('卓氏','2ph_uqm_vm3'))
        for mid,m in ms.items():
            if m['surface']=='卓氏' and mid!='c-shiji-117-xiangru:m045-0016':self.assertNotEqual(m['person_id'],'2ph_uqm_vm3')
    def test_end_of_life_wife_remains_nonexhaustive_candidate(self):
        c=read('corpus/shiji/117.json');m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']=='c-shiji-117-xiangru:m056-0057')
        self.assertIsNone(m['person_id']);self.assertEqual(m['kind'],'unresolved')
        case=next(c for c in c['annotation']['unresolved_identity_cases']if c['id']=='u-shiji117-last-wife')
        self.assertEqual(case['candidate_person_ids'],['2ph_uqm_vm3']);self.assertFalse(case['candidate_list_exhaustive']);self.assertTrue(case['unknown_identity_possible'])
    def test_named_and_unnamed_comparative_evidence_are_separate(self):
        d=next(d for d in read('corpus/shiji/117-identities.json')['decisions']if d['id']=='d-shiji117-zhuo-marriage')
        self.assertEqual(d['confidence_level'],'moderate');self.assertFalse(d['human_reviewed'])
        self.assertEqual({e['paragraph_id'].split(':')[1]for e in d['evidence']},{'p002','p045'})
        ref,=d['references'];self.assertTrue(ref['paragraph_id'].endswith('p035'));self.assertIn('自以得使女尚司馬長卿晚',ref['quote'])
        p=next(p for p in read('corpus/shiji/117.json')['paragraphs']if p['id']==ref['paragraph_id']);self.assertEqual(ref['quote'],p['text'])
    def test_name_components_are_provisional_and_keep_both_source_forms(self):
        n=next(n for n in read('data/corpus/profile-names.json')['records']if n['person_id']=='2ph_uqm_vm3')
        self.assertEqual((n['surname'],n['ming']),('卓','文君'));self.assertEqual(n['status'],'editorial_provisional');self.assertFalse(n['human_reviewed'])
        self.assertIn('卓王孫有女文君',n['quote']);self.assertEqual(n['references'][0]['quote'],'與卓氏婚，饒於財。')
    def test_profile_bundle_does_not_count_the_unknown_wife_as_accepted(self):
        b=bundle('2ph_uqm_vm3',include_provisional=True)
        self.assertTrue(any(m['id']=='c-shiji-117-xiangru:m045-0016'for m in b['mentions']))
        self.assertFalse(any(m['id']=='c-shiji-117-xiangru:m056-0057'for m in b['mentions']))
        self.assertTrue(any(c['id']=='u-shiji117-last-wife'for c in b['unresolved_identity_cases']))
if __name__=='__main__':unittest.main()
