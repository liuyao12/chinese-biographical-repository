import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class LuBuweiSecondPassTests(unittest.TestCase):
    def test_summer_mother_is_distinct_from_adoptive_mother(self):
        c=json.loads((ROOT/'corpus/shiji/085.json').read_text())
        p=c['paragraphs'][6]
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] in ('夏姬','夏太后')},{'pz6_lqa_ina'})
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] in ('華陽后','華陽太后')},{'jb2_tak_5p8'})
        a=json.loads((ROOT/'corpus/shiji/085-assertions.json').read_text())['assertions']
        self.assertFalse(any(x['predicate']=='mother' and x['object_person_id']=='jb2_tak_5p8' for x in a))
        adopted=next(x for x in a if x['predicate']=='adoptive_mother')
        self.assertEqual((adopted['subject_person_id'],adopted['object_person_id']),('ao3_0fy_d45_AA','jb2_tak_5p8'))
        self.assertIn('所母',adopted['qualifiers']['source_term'])

    def test_mother_identity_does_not_resolve_biological_father_or_other_taihou(self):
        c=json.loads((ROOT/'corpus/shiji/085.json').read_text())
        self.assertIn('姬自匿有身',c['paragraphs'][4]['text'])
        self.assertEqual({m['person_id'] for m in c['paragraphs'][4]['mentions'] if m['surface']=='邯鄲諸姬絕好善舞者'},{'lap_qc0_yqm'})
        parallel=json.loads((ROOT/'corpus/shiji/006.json').read_text())
        self.assertIn('秦莊襄王子也',parallel['paragraphs'][0]['text'])
        self.assertTrue(all(m['person_id'] is None for m in parallel['paragraphs'][9]['mentions'] if m['surface']=='太后'))
        assertions=json.loads((ROOT/'corpus/shiji/085-assertions.json').read_text())['assertions']
        self.assertFalse(any(x['predicate']=='father' and x['subject_person_id']=='ao3_0fy_d45_AAA' and x['object_person_id']=='puu_6hs_m4f' for x in assertions))

    def test_zhao_death_successor_and_unidentified_prince_stay_separate(self):
        c=json.loads((ROOT/'corpus/shiji/085.json').read_text())
        self.assertEqual({m['person_id'] for m in c['paragraphs'][5]['mentions'] if m['surface']=='秦昭王'},{'ao3_0fy_d45'})
        self.assertEqual({m['person_id'] for m in c['paragraphs'][1]['mentions'] if m['surface']=='太子'},{'lje_891_3sg'})
