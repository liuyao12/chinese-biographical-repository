import copy
import json
import unittest
from pathlib import Path
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.validate_corpus import title_proposal_errors

ROOT=Path(__file__).resolve().parents[1]


class UnassumedAppointments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters=[json.loads((ROOT/('corpus/jinshu/'+n+'.json')).read_text()) for n in ['065','076']]
        cls.people={p['id']for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        cls.cases=[(c,q)for c in cls.chapters for q in c['annotation']['title_proposals']]

    def test_eight_appointments_keep_declining_distinct_from_nonattendance(self):
        self.assertEqual(len(self.cases),8)
        self.assertEqual(sum(q['non_assumption_kind']=='declined'for _,q in self.cases),4)
        for c,q in self.cases:
            self.assertTrue(unassumed_appointment_valid(q,c))
            self.assertEqual(title_proposal_errors(q,c,self.people),[])
            self.assertEqual(q['outcome'],'not_assumed')
            self.assertNotEqual(q['outcome'],'not_enacted')
            self.assertTrue(q['appointment_anchor']['surface'])
            self.assertIn(q['non_assumption_anchor']['surface'],q['evidence'][0]['quote'])

    def test_wrong_recipient_anchor_outcome_or_source_dimension_is_rejected(self):
        for c,q in self.cases:
            for mutate in [lambda x:x.update(outcome='not_enacted'),
                           lambda x:x.update(person_mention_id=x['role_mention_id']),
                           lambda x:x.update(non_assumption_kind='served'),
                           lambda x:x['evidence'][0].update(work_id='w-shiji'),
                           lambda x:x['non_assumption_anchor'].update(start=x['non_assumption_anchor']['start']+1)]:
                bad=copy.deepcopy(q);mutate(bad)
                self.assertFalse(unassumed_appointment_valid(bad,c))
                self.assertTrue(title_proposal_errors(bad,c,self.people))

    def test_refusal_text_cannot_be_removed_or_borrowed_from_another_paragraph(self):
        c,q=self.cases[-1]
        bad=copy.deepcopy(q);bad['evidence'][0]['quote']=q['title']
        self.assertFalse(unassumed_appointment_valid(bad,c))
        bad=copy.deepcopy(q);bad['non_assumption_anchor']['paragraph_id']=c['paragraphs'][0]['id']
        self.assertFalse(unassumed_appointment_valid(bad,c))
        bad=copy.deepcopy(q);bad['appointment_anchor']['surface']='欲立'
        self.assertFalse(unassumed_appointment_valid(bad,c))

    def test_ancestral_office_usage_keeps_unknown_tenure_beside_unassumed_appointment(self):
        c=next(c for c in self.chapters if c['book_id']=='b-jinshu-076')
        q=next(q for q in c['annotation']['title_proposals']if q['title']=='司州刺史')
        h=next(h for h in json.loads((ROOT/'corpus/songshu/066-titles.json').read_text())['holdings']if h['person_id']==q['person_id'])
        self.assertEqual(h['mode'],'attestation')
        self.assertEqual(h['effective_period']['start']['status'],'unknown')
        self.assertEqual(h['effective_period']['end']['status'],'unknown')
        self.assertEqual(q['non_assumption_anchor']['surface'],'以疾固辭，未行而卒')


if __name__=='__main__':unittest.main()
