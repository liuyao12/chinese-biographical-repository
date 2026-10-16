import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def para(n):return read('corpus/shiji/097.json')['paragraphs'][n-1]
def ids(n,s):return {m['person_id'] for m in para(n)['mentions'] if m['surface']==s and m['kind']=='person'}
class LiLuSecondPassTests(unittest.TestCase):
    def test_court_people_follow_particular_events(self):
        for n,s,pid in [(5,'項羽','ob7_g6i_7pp'),(8,'黥布','zxd_afr_2xg'),(14,'絳侯','koy_6jg_gcc'),(18,'呂太后','i30_mjq_6q8_A'),(18,'孝惠帝','yqp_nlb_p1p_AA'),(20,'淮南厲王','yqp_nlb_p1p_AF')]:
            self.assertEqual(ids(n,s),{pid})
        self.assertEqual(ids(14,'陳平'),{'i3f_9l9_g53'})
        self.assertNotIn('rwg_skp_gbq',ids(14,'陳平'))

    def test_hongru_corrected_identity_preserves_received_spelling(self):
        self.assertEqual(ids(18,'閎籍孺'),{'nxn_szf_9gi'})
        self.assertEqual(para(18)['text'].count('閎籍孺'),2)
        b=read('exports/persons/nxn_szf_9gi.json')
        corrections=[d['preferred_reading'] for d in b['identity_decisions'] if d.get('preferred_reading')]
        self.assertEqual({d['person_mention_id'] for d in corrections},{'c-shiji-097-luli:m018-0093','c-shiji-097-luli:m018-0196'})
        self.assertTrue(all(d['source_spelling_is_not_alias'] and d['preferred_surface']=='閎孺' for d in corrections))
        self.assertNotIn('wbf_66x_6s2',b['person_ids'])
        profile=read('data/corpus/profiles/nxn_szf_9gi.json')
        self.assertNotIn('閎籍孺',profile['names'])

    def test_jian_son_link_is_commentary_based_not_all_children_merged(self):
        self.assertEqual(ids(20,'其子'),{'tkc_9z3_91l_A'})
        self.assertEqual(ids(24,'子'),{'tkc_9z3_91l_A'})
        self.assertTrue(any(m['surface']=='諸子' and m['person_id'] is None for m in para(20)['mentions']))
        b=read('exports/persons/tkc_9z3_91l_A.json')
        eq=next(x for x in b['equivalence_decisions'] if x['id']=='eq-shiji097-zhujian-son-commentary')
        self.assertIn('與太史公善',eq['references'][0]['quote'])
        self.assertEqual(eq['references'][0]['revision_id'],2514767)
        self.assertFalse(eq['references'][0]['image_verified'])
        fathers=[x for x in b['relations'] if x['subject_person_id']=='tkc_9z3_91l_A' and x['predicate']=='father']
        self.assertTrue(fathers)
        self.assertEqual({x['object_person_id'] for x in fathers},{'tkc_9z3_91l'})

    def test_unknown_narrator_stays_unresolved_after_unrelated_merges(self):
        c=read('corpus/shiji/096.json')
        case=next(x for x in c['annotation']['unresolved_identity_cases'] if x['id']=='ic-shiji096-final-narrator')
        self.assertTrue(case['unknown_identity_possible'])
        self.assertEqual(case['status'],'unresolved')
        self.assertFalse(any(x['id']==case['id'] for x in c['annotation'].get('resolved_identity_cases',[])))

    def test_eight_retired_candidates_have_no_registry_or_public_files(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        for old in ['50g_j9s_2le','m68_ewg_gly','rg1_213_xlb','otq_r9b_d3z','noy_49h_qor','k4e_4tr_lg0','9hr_p35_zdj','tkc_9z3_91l_B']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())
