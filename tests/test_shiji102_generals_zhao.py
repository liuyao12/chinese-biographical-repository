import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD={'mb1_jy6_k0x','mag_s6n_b0c','nml_3oq_o49','ur3_6rb_cp2'}
class GeneralsZhao(unittest.TestCase):
    def test_retired_ids_are_gone(self):
        r=json.loads((ROOT/'registry/persons.json').read_text())
        self.assertFalse(OLD & {p['id'] for p in r['persons']})
        c=json.loads((ROOT/'corpus/shiji/102.json').read_text())
        self.assertFalse(OLD & {m.get('person_id') for p in c['paragraphs'] for m in p['mentions']})
    def test_mother_keeps_both_source_assertions(self):
        for num,aid in [('043','a-shiji043-064'),('102','a-shiji102-007')]:
            d=json.loads((ROOT/f'corpus/shiji/{num}-assertions.json').read_text())
            a=next(a for a in d['assertions'] if a['id']==aid)
            self.assertEqual(a['subject_person_id'],'q6w_qm5_w2b_AA')
            self.assertEqual(a['object_person_id'],'xdq_h9k_zzl')
            self.assertEqual(a['predicate'],'mother')
            self.assertIn('其母倡也',a['evidence'][0]['quote'])
    def test_mother_and_child_have_separate_evidence_anchors(self):
        d=json.loads((ROOT/'corpus/shiji/102-equivalences.json').read_text())
        rows=[x for x in d['decisions'] if x['id'].startswith('eq-shiji102-generals-')]
        self.assertEqual(len(rows),4)
        for row in rows:
            self.assertTrue(row['identity_materialized'])
            self.assertEqual(row['person_ids'],[row['canonical_person_id']])
            self.assertGreaterEqual(len(row['chapter_ids']),2)
        mother=next(x for x in rows if x['canonical_person_id']=='xdq_h9k_zzl')
        ids={mid for e in mother['evidence'] for mid in e['mention_ids']}
        self.assertIn('c-shiji-102-zhangfeng:m012-0230',ids)
        self.assertIn('c-shiji-043-zhao:m121-0017',ids)
