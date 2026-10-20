from pathlib import Path
import hashlib,json,unittest
from scripts.person_bundle import bundle,load_catalog

ROOT=Path(__file__).resolve().parents[1]

class Song047SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'corpus/songshu/047-liuhuaisu.json').read_text())
        cls.raw=(ROOT/cls.c['source']['raw_path']).read_bytes()
        cls.relations=json.loads((ROOT/'corpus/songshu/047-liuhuaisu-assertions.json').read_text())['assertions']

    def test_full_selected_text_and_every_raw_character(self):
        c=self.c;lines=self.raw.decode().splitlines()
        self.assertEqual(1535,sum(len(p['text'])for p in c['paragraphs']))
        self.assertEqual(10,len(c['paragraphs']))
        self.assertEqual(c['source']['raw_file_sha256'],hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(165,sum(len(p['mentions'])for p in c['paragraphs']))
        for p in c['paragraphs']:
            positions=p['source_position']['raw_character_positions']
            self.assertEqual(p['text'],''.join(lines[s['line']-1][s['column']]for s in positions))
            for m in p['mentions']:self.assertEqual(m['surface'],p['text'][m['start']:m['end']])

    def test_shared_and_unresolved_identity_limits(self):
        c=self.c;marks=[m for p in c['paragraphs']for m in p['mentions']]
        self.assertTrue(any(m.get('person_id')=='kd4_921_4cr'for m in marks))
        u=next(m for m in marks if m['surface']=='張暢之')
        self.assertEqual('unresolved',u['kind']);self.assertIsNone(u['person_id'])
        self.assertEqual(['q7q_j3y_nhj'],u['candidate_person_ids'])
        liu=next(m for m in marks if m['surface']=='劉統')
        self.assertEqual('e7b_lo3_sxo',liu['person_id'])
        self.assertFalse(any(m['surface']=='劉統平'for m in marks))

    def test_dates_mothers_and_succession_do_not_invent_birth_or_adoption(self):
        c=self.c;age=next(a for a in c['annotation']['age_assertions']if a['id']=='age-song047-huaisu-death')
        self.assertEqual(41,age['value']);self.assertIsNone(age['birth_year'])
        events=json.loads((ROOT/'corpus/songshu/047-liuhuaisu-life-events.json').read_text())['events']
        death=next(e for e in events if e['id']=='le-song047-huaisu-death');self.assertEqual(407,death['normalized_date']['year'])
        self.assertFalse(any(a['predicate']=='adoptive_father'for a in self.relations))
        self.assertEqual(['myg_cco_ng6'],[a['object_person_id']for a in self.relations if a['subject_person_id']=='h1l_zwj_gdd'and a['predicate']=='father'])
        for a in self.relations:
            if a['predicate']=='maternal_role':
                self.assertIsNone(a['qualifiers']['biological_mother']);self.assertIsNone(a['qualifiers']['father_person_id'])
        self.assertEqual(3,next(a['qualifiers']['birth_order']['ordinal']for a in self.relations if a['subject_person_id']=='6ie_gjx_w1x'))
        self.assertEqual('children_of_parent',next(a['qualifiers']['birth_order']['scope']for a in self.relations if a['subject_person_id']=='6ie_gjx_w1x'))

    def test_actual_bundle_preserves_raw_but_suppresses_disputed_order(self):
        cat=load_catalog(ROOT)
        for pid in ('olf_c6j_hmg','cl5_su9_u9f'):
            b=bundle(pid,ROOT,True,cat)
            raw=next(a for a in b['relations']if a['id']=='a-song047-liuhuaisu-006')
            preferred=next(a for a in b['preferred_relations']if a['id']==raw['id'])
            self.assertIn('relative_birth_order',raw['qualifiers'])
            self.assertNotIn('relative_birth_order',preferred['qualifiers'])
            self.assertEqual('brother',preferred['predicate'])
            self.assertIsNone(b['relative_birth_order_decisions'][0]['preferred_claim_id'])
            self.assertFalse(any(a['assertion_id']==raw['id']for a in b['preferred_birth_order_constraints']))

if __name__=='__main__':unittest.main()
