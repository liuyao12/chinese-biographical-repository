import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD={'6qw_s6t_pib','c68_rcg_qsu','gy7_87j_x9e','dip_c4z_kc6'}
class CoreIdentities(unittest.TestCase):
    def test_retired_ids_removed_and_empress_mothers_distinct(self):
        r=json.loads((ROOT/'registry/persons.json').read_text())
        ids={p['id'] for p in r['persons']}
        self.assertFalse(OLD & ids)
        self.assertTrue({'6d6_eg1_o3a_A','9zj_vf7_86a_A','ixk_6fg_v6f_A'} <= ids)
        c=json.loads((ROOT/'corpus/shiji/103.json').read_text())
        p=next(p for p in c['paragraphs'] if p['id'].endswith('p004'))
        self.assertEqual(next(m for m in p['mentions'] if m['surface']=='皇太后')['person_id'],'6d6_eg1_o3a_A')
    def test_chronology_disagreement_does_not_prevent_sourced_identity(self):
        d=json.loads((ROOT/'corpus/shiji/103-equivalences.json').read_text())
        rows=[x for x in d['decisions'] if x['id'].startswith('eq-shiji103-core-')]
        self.assertEqual(len(rows),4)
        for row in rows:
            self.assertTrue(row['identity_materialized'])
            self.assertEqual(row['person_ids'],[row['canonical_person_id']])
        han=next(x for x in rows if x['canonical_person_id']=='6hy_i1z_hu2')
        self.assertIn('元朔四年',han['rationale'])
        self.assertIn('元朔二年',han['rationale'])
        self.assertTrue(any('元朔二年中卒' in e['quote'] for e in han['evidence']))
        self.assertTrue(any('元朔四年，韓安國免' in e['quote'] for e in han['evidence']))
    def test_shi_sons_are_not_renamed_by_identity_merge(self):
        c=json.loads((ROOT/'corpus/shiji/103.json').read_text())
        p=next(p for p in c['paragraphs'] if p['id'].endswith('p002'))
        self.assertEqual(next(m for m in p['mentions'] if m['surface']=='甲')['person_id'],'esh_e0a_jrw_AB')
        self.assertEqual(next(m for m in p['mentions'] if m['surface']=='乙')['person_id'],'esh_e0a_jrw_AC')
