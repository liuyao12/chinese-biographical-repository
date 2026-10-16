import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD={'t90_dfp_2t1','a54_d6h_wd1','blw_xsu_w9q','0r9_eg1_k8e'}
class FurtherIdentities(unittest.TestCase):
    def test_retired_ids_removed(self):
        r=json.loads((ROOT/'registry/persons.json').read_text())
        self.assertFalse(OLD & {p['id'] for p in r['persons']})
    def test_full_named_mentions_use_cross_chapter_identities(self):
        c=json.loads((ROOT/'corpus/shiji/103.json').read_text())
        wanted={'項籍':'ob7_g6i_7pp','王温舒':'6ym_eva_k4a','兒寬':'x8r_9sk_d7a','桑弘羊':'fi2_2cl_w22'}
        for term,pid in wanted.items():
            ms=[m for p in c['paragraphs'] for m in p['mentions'] if m['surface']==term]
            self.assertTrue(ms)
            self.assertTrue(all(m['person_id']==pid for m in ms))
    def test_bangu_attribution_is_retained_in_evidence(self):
        d=json.loads((ROOT/'corpus/shiji/103-equivalences.json').read_text())
        rows=[r for r in d['decisions'] if r['id'].startswith('eq-shiji103-further-')]
        self.assertEqual(len(rows),4)
        for row in rows:
            self.assertTrue(row['identity_materialized'])
            self.assertEqual(row['person_ids'],[row['canonical_person_id']])
            self.assertFalse(row['human_reviewed'])
        sang=next(r for r in rows if r['canonical_person_id']=='fi2_2cl_w22')
        e=next(e for e in sang['evidence'] if e['paragraph_id']=='c-shiji-112-pingjin:p030')
        self.assertTrue(e['quote'].startswith('班固稱曰'))
        self.assertIn('運籌則桑弘羊',e['quote'])
        self.assertIn('班固',sang['rationale'])
