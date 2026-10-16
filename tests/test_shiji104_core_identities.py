import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD={'jya_fko_ski','mih_vxs_rhx','431_23t_wkr','nnw_99z_4e5','es5_b3z_9kk','ax6_77g_gsd'}
class CoreIdentities(unittest.TestCase):
    def test_retired_ids_and_mother_context(self):
        r=json.loads((ROOT/'registry/persons.json').read_text())
        self.assertFalse(OLD & {p['id'] for p in r['persons']})
        c=json.loads((ROOT/'corpus/shiji/104.json').read_text())
        p=next(p for p in c['paragraphs'] if p['id'].endswith('p004'))
        self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='太后'),'ixk_6fg_v6f_A')
        self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='梁孝王'),'yqp_nlb_p1p_ACG')
    def test_chenxi_conflicting_years_and_context_are_retained(self):
        d=json.loads((ROOT/'corpus/shiji/104-equivalences.json').read_text())
        rows=[r for r in d['decisions'] if r['id'].startswith('eq-shiji104-core-')]
        self.assertEqual(len(rows),6)
        chen=next(r for r in rows if r['canonical_person_id']=='1xx_s1v_svn')
        self.assertIn('漢七年',chen['evidence'][0]['quote'])
        self.assertTrue(any(e['quote'].startswith('十年十月') for e in chen['references']))
        self.assertTrue(any(e['paragraph_id'].endswith('p072') for e in chen['references']))
        self.assertIn('不統一事件年',chen['rationale'])
        for r in rows:
            self.assertTrue(r['identity_materialized'])
            self.assertEqual(r['person_ids'],[r['canonical_person_id']])
    def test_shi_chancellor_is_qing_in_chu_supplement(self):
        c=json.loads((ROOT/'corpus/shiji/104.json').read_text())
        p=next(p for p in c['paragraphs'] if p['id'].endswith('p014'))
        self.assertEqual(p['text_layer'],'witness_appended_chu_note')
        self.assertEqual(next(m['person_id'] for m in p['mentions'] if m['surface']=='石丞相'),'esh_e0a_jrw_AD')
        self.assertIn('河東太守石丞相子孫也',p['text'])
