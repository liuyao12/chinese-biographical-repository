# coding: utf-8
"""Divine names retain witness spelling and never supply unsupported genealogies."""
import copy,json,unittest
from pathlib import Path
from scripts.referent_interpretations import interpretation_errors
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
CASES={'陵陽':'i4v_y28_wx0','玄冥':'dal_xne_xt3','含靁':'21k_m7f_sxc','潏湟':'oj8_zfy_dkl','勾芒':'hd8_aho_qei','豐隆':'hnj_ut6_7z4'}
class DivineNames(unittest.TestCase):
    def setUp(self):
        self.c=read('corpus/shiji/117.json');self.people={p['id']:p for p in read('registry/persons.json')['persons']};self.cases={c['id']:c for c in self.c['annotation']['referent_interpretations']}
    def test_six_names_have_stable_legendary_ids_and_exact_source_aliases(self):
        for surface,pid in CASES.items():
            m,= [m for p in self.c['paragraphs']for m in p['mentions']if m['surface']==surface]
            self.assertEqual(m['person_id'],pid);person=self.people[pid]
            self.assertEqual(person['historicity'],'legendary_tradition')
            self.assertEqual(person['aliases'],[{'surface':surface,'mention_ids':[m['id']]}])
            self.assertEqual(person['evidence'][0]['quote'],surface)
    def test_lingyang_is_not_inverted_into_yangling_or_forced_into_yangzi(self):
        self.assertEqual(self.people[CASES['陵陽']]['label'],'陵陽子明')
        case=self.cases['ri-shiji117-yangzi']
        self.assertIsNone(case['default_alternative_id'])
        self.assertTrue(any('陽陵' in a['interpretation'] for a in case['alternatives']))
        self.assertFalse(any(CASES['陵陽'] in a['candidate_person_ids'] for a in case['alternatives']))
        d=next(d for d in read('corpus/shiji/117-identities.json')['decisions']if d['person_id']==CASES['陵陽'])
        self.assertTrue(any('陵陽子明' in r['quote']for r in d['references']))
    def test_divine_names_do_not_gain_offices_life_events_or_kinship(self):
        for fn,key in [('117-life-events.json','events'),('117-titles.json','holdings'),('117-assertions.json','assertions')]:
            self.assertFalse(any(pid in json.dumps(row)for pid in CASES.values()for row in read('corpus/shiji/'+fn)[key]))
    def test_luli_readings_preserve_both_witness_spellings(self):
        case=self.cases['ri-shiji117-luli'];self.assertEqual(case['status'],'unresolved');self.assertIsNone(case['default_alternative_id']);self.assertEqual(len(case['alternatives']),3)
        self.assertEqual({a['referent_kind']for a in case['alternatives']},{'divinity','mythical_creature'})
        self.assertTrue(all(a['candidate_person_ids']==[]for a in case['alternatives']))
        self.assertEqual(case['witness_wording']['received_phrase'],'前陸離而後潏湟');self.assertEqual(case['witness_wording']['parallel_phrase'],'前長離而後矞皇');self.assertFalse(case['witness_wording']['adopted_as_text_correction'])
    def test_five_emperors_are_a_group_not_the_five_historical_persons(self):
        case=self.cases['ri-shiji117-five-celestial-emperors'];chosen=next(a for a in case['alternatives']if a['id']==case['default_alternative_id'])
        self.assertEqual(chosen['referent_kind'],'generic_group');self.assertEqual(chosen['candidate_person_ids'],[])
        m=next(m for p in self.c['paragraphs']for m in p['mentions']if m['id']==case['target_mention_ids'][0]);self.assertIsNone(m['person_id'])
    def test_mythical_creature_selection_requires_sources_and_cannot_assign_a_person(self):
        c=copy.deepcopy(self.c);case=next(c for c in c['annotation']['referent_interpretations']if c['id']=='ri-shiji117-luli');a=next(a for a in case['alternatives']if a['referent_kind']=='mythical_creature');case.update(status='editorial_provisional',default_alternative_id=a['id'],selection={'rationale':'Synthetic model-only selection test, not an editorial adoption.','source_reference_ids':a['source_reference_ids']})
        self.assertEqual(interpretation_errors(c,set(self.people)),[])
        a['candidate_person_ids']=[CASES['陵陽']];self.assertTrue(interpretation_errors(c,set(self.people)))
        a['candidate_person_ids']=[];case['selection']['source_reference_ids']=['missing'];self.assertTrue(interpretation_errors(c,set(self.people)))
if __name__=='__main__':unittest.main()
