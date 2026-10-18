import copy
import json
import unittest
from pathlib import Path
from scripts.non_parental_family import non_parental_relation_valid
from scripts.regnal_relationships import accession_death_interval_valid

ROOT=Path(__file__).resolve().parents[1]

class NonParentalFamily(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paragraphs={}
        cls.relations=[]
        for number in ['032','064','075']:
            c=json.loads((ROOT/('corpus/jinshu/'+number+'.json')).read_text())
            cls.paragraphs.update({p['id']:(c['id'],p) for p in c['paragraphs']})
            cls.relations.extend(json.loads((ROOT/('corpus/jinshu/'+number+'-assertions.json')).read_text())['assertions'])
        cls.cases=[a for a in cls.relations if a['predicate'] in ('raised_by','ritual_successor_of')]

    def test_four_care_and_two_succession_claims_preserve_nonparental_meaning(self):
        self.assertEqual(len(self.cases),6)
        self.assertEqual(sum(a['predicate']=='raised_by' for a in self.cases),4)
        for a in self.cases:
            with self.subTest(id=a['id']):
                self.assertTrue(non_parental_relation_valid(a,self.paragraphs))
                self.assertEqual(a['qualifiers']['legal_adoption_status'],'not_stated')

    def test_wrong_endpoint_direction_and_legal_adoption_are_rejected(self):
        for a in self.cases:
            for change in ['reverse','adoption','parent','hidden-parent','quote']:
                bad=copy.deepcopy(a)
                if change=='reverse':bad['subject_person_id'],bad['object_person_id']=bad['object_person_id'],bad['subject_person_id']
                elif change=='adoption':bad['qualifiers']['legal_adoption_status']='adopted'
                elif change=='parent':bad['predicate']='father'
                elif change=='hidden-parent':bad['qualifiers']['father_person_id']=bad['object_person_id']
                else:bad['evidence'][0]['quote']=bad['qualifiers']['source_term']
                with self.subTest(id=a['id'],change=change):
                    self.assertFalse(non_parental_relation_valid(bad,self.paragraphs))

    def test_rearing_speech_requires_identity_of_actual_speaker(self):
        a=next(a for a in self.cases if a['qualifiers'].get('care_basis')=='speaker_recalls_rearing')
        p=self.paragraphs[a['evidence'][0]['paragraph_id']][1]
        bad=copy.deepcopy(a)
        bad['qualifiers']['speaker_identity_mention_id']=next(m['id'] for m in p['mentions'] if m['surface']=='元帝')
        self.assertFalse(non_parental_relation_valid(bad,self.paragraphs))

    def test_actual_birth_mother_survives_care_and_ritual_records(self):
        care=next(a for a in self.cases if a['qualifiers'].get('care_basis')=='explicit_yang')
        mothers=[a for a in self.relations if a['subject_person_id']==care['subject_person_id'] and a['predicate']=='mother']
        self.assertTrue(mothers)
        self.assertTrue(all(a['object_person_id']=='12b_2lg_vs3' for a in mothers))
        self.assertNotEqual(care['object_person_id'],mothers[0]['object_person_id'])
        self.assertFalse(any(a['subject_person_id']==care['subject_person_id'] and a['predicate']=='adoptive_mother' for a in self.relations))

    def test_care_does_not_replace_the_two_orphans_father(self):
        for a in self.cases:
            if a['qualifiers'].get('care_basis')!='welcomed_like_children':continue
            fathers=[x for x in self.relations if x['subject_person_id']==a['subject_person_id'] and x['predicate']=='father']
            self.assertEqual(len(fathers),1)
            self.assertEqual(fathers[0]['object_person_id'],'1ay_9qe_u4h')
            self.assertNotEqual(fathers[0]['object_person_id'],a['object_person_id'])

    def test_anguo_interval_is_after_accession_and_not_age_or_exact_date(self):
        records=json.loads((ROOT/'corpus/jinshu/064-life-events.json').read_text())['events']
        e=next(e for e in records if e['id']=='le-jinshu064-anguo-death')
        mentions={m['id']:(cid,pid,m) for pid,(cid,p) in self.paragraphs.items() for m in p['mentions']}
        self.assertTrue(accession_death_interval_valid(e,self.paragraphs,mentions))
        self.assertEqual(e['reported_reign_interval']['upper_years'],1)
        self.assertIsNone(e['date_expression'])
        ages=json.loads((ROOT/'corpus/jinshu/064.json').read_text())['annotation'].get('age_assertions',[])
        self.assertFalse(any(a['person_id']==e['person_id'] for a in ages))
        for change in ['age','borrowed-year','different-person','bound']:
            bad=copy.deepcopy(e)
            if change=='age':bad['reported_reign_interval']['reference_event']='birth'
            elif change=='borrowed-year':bad['date_expression']='建武元年'
            elif change=='different-person':bad['person_id']='dkn_ge4_286_AAAAAAAB'
            else:bad['reported_reign_interval']['upper_years']=18
            with self.subTest(change=change):
                self.assertFalse(accession_death_interval_valid(bad,self.paragraphs,mentions))

if __name__=='__main__':unittest.main()
