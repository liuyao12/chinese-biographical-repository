import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SuoZhongCommentary(unittest.TestCase):
    def test_three_contexts_retain_every_occurrence(self):
        expected={'012':2,'103':1,'117':3}
        for num,count in expected.items():
            c=json.loads((ROOT/f'corpus/shiji/{num}.json').read_text())
            ms=[m for p in c['paragraphs'] for m in p['mentions'] if m.get('person_id')=='gns_w0b_kfj']
            self.assertEqual(len(ms),count)
        reg=json.loads((ROOT/'registry/persons.json').read_text())
        self.assertFalse({'lpm_cci_4wd','k0u_vj7_93t'} & {p['id'] for p in reg['persons']})
    def test_three_way_decision_keeps_inference_limit(self):
        d=json.loads((ROOT/'corpus/shiji/103-equivalences.json').read_text())
        e=next(e for e in d['decisions'] if e['id']=='eq-shiji103-suozhong')
        self.assertEqual(e['person_ids'],['gns_w0b_kfj'])
        self.assertEqual(len(e['chapter_ids']),3)
        self.assertTrue(e['identity_materialized'])
        self.assertFalse(e['human_reviewed'])
        self.assertIn('未直接互指',e['rationale'])
    def test_placeholder_commentary_is_fixed_witness_not_renaming(self):
        d=json.loads((ROOT/'corpus/shiji/103-identities.json').read_text())
        reg=json.loads((ROOT/'registry/persons.json').read_text())
        for did,pid in [('d-shiji103-032','esh_e0a_jrw_AB'),('d-shiji103-033','esh_e0a_jrw_AC')]:
            e=next(e for e in d['decisions'] if e['id']==did)
            r=next(r for r in e['references'] if r.get('revision_id')==2514773)
            self.assertFalse(r['image_verified'])
            self.assertIn('非其名也',r['quote'])
            p=next(p for p in reg['persons'] if p['id']==pid)
            self.assertEqual(p['designation_type'],'placeholder_for_unrecorded_name')
            self.assertFalse(any(a['surface']=='仁' for a in p['aliases']))
