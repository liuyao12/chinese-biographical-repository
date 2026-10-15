import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD={'jb9_8aa_47l','04s_md1_e2f','ccg_ycv_y85','ymz_578_wc0','q7p_z4x_qee'}
class CoreIdentities(unittest.TestCase):
    def test_retired_registry_ids_are_removed(self):
        r=json.loads((ROOT/'registry/persons.json').read_text())
        self.assertFalse(OLD & {p['id'] for p in r['persons']})
    def test_contextual_people_keep_specific_identities(self):
        c=json.loads((ROOT/'corpus/shiji/102.json').read_text())
        wanted={'絳侯周勃':'koy_6jg_gcc','薄太后':'9zj_vf7_86a_A','慎夫人':'evh_7zu_u3x','二世':'ao3_0fy_d45_AAAA','太子':'yqp_nlb_p1p_ACA'}
        for term,pid in wanted.items():
            found=[m for p in c['paragraphs'] for m in p['mentions'] if m['surface']==term]
            self.assertTrue(found)
            self.assertTrue(all(m.get('person_id')==pid for m in found))
        liang=[m for p in c['paragraphs'] for m in p['mentions'] if m['surface']=='梁王']
        self.assertTrue(liang)
        self.assertTrue(all(m.get('person_id')=='0c1_mro_k7x' for m in liang))
    def test_equivalences_have_cross_chapter_quotes_without_old_aliases(self):
        e=json.loads((ROOT/'corpus/shiji/102-equivalences.json').read_text())
        ds=[d for d in e['decisions'] if d['id'].startswith('eq-shiji102-core-')]
        self.assertEqual(len(ds),5)
        for d in ds:
            self.assertTrue(d['identity_materialized'])
            self.assertEqual(d['person_ids'],[d['canonical_person_id']])
            self.assertGreaterEqual(len({e['chapter_id'] for e in d['evidence']}),2)
            self.assertFalse(d['human_reviewed'])
            for ev in d['evidence']: self.assertTrue(ev['quote'])
