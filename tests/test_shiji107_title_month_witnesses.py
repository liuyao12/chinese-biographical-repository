import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TitleMonthWitnesses(unittest.TestCase):
    def test_grant_witness_does_not_invent_specific_titles_in_hanshu(self):
        hs=json.loads((ROOT/'corpus/shiji/107-titles.json').read_text())['holdings']
        for suffix,pid in [('009','7mz_d13_9ka_A'),('010','7mz_d13_9ka_B')]:
            h=next(h for h in hs if h['id']=='th-shiji107-'+suffix)
            d=h['effective_period']['start']['normalized_date']
            ref=next(r for r in d['references']if r.get('scope')=='received_parallel_event')
            self.assertEqual(d['era_year'],141)
            self.assertIn('三月',ref['quote']);self.assertNotIn('武安侯',ref['quote']);self.assertNotIn('周陽侯',ref['quote'])
            c=json.loads((ROOT/'corpus/hanshu/006.json').read_text());p=next(p for p in c['paragraphs']if p['id']==ref['paragraph_id'])
            self.assertIn(ref['quote'],p['text']);self.assertEqual(next(m for m in p['mentions']if m['id']==ref['person_mention_id'])['person_id'],pid)
    def test_table_month_and_actor_are_same_appointment(self):
        hs=json.loads((ROOT/'corpus/shiji/107-titles.json').read_text())['holdings']
        h=next(h for h in hs if h['id']=='th-shiji107-017');d=h['effective_period']['start']['normalized_date']
        ref=next(r for r in d['references']if r.get('scope')=='received_parallel_event')
        t=json.loads((ROOT/'data/historical-tables/shiji-022.json').read_text());c=next(c for f in t['fragments']for r in f['rows']for c in r['cells']if c['id']==ref['table_cell_id'])
        self.assertEqual(ref['quote'],c['text']);self.assertIn('六月癸巳',c['text']);self.assertEqual(d['era_year'],135)
        self.assertEqual(next(m for m in c['person_mentions']if m['id']==ref['person_mention_id'])['person_id'],h['person_id'])
        self.assertEqual(h['effective_period']['end']['status'],'unknown')
    def test_same_row_dowager_and_officers_have_contextual_anchors(self):
        t=json.loads((ROOT/'data/historical-tables/shiji-022.json').read_text());r=next(r for f in t['fragments']for r in f['rows']if r['id']=='shiji-022-t1-r072')
        mentions={m['surface']:m for c in r['cells']for m in c['person_mentions']}
        self.assertEqual({s:m['person_id']for s,m in mentions.items()},{'閩越王':'xp5_39k_w5w','孝景太后':'ixk_6fg_v6f_A','昌':'jex_mvs_w6d','田蚡':'7mz_d13_9ka_A','青翟':'40p_hkv_oqy','安國':'6hy_i1z_hu2'})
        for m in mentions.values():self.assertTrue(m['identity_evidence'])
        self.assertTrue(all(not c['person_mentions']for c in r['cells']if c['column']==0))
