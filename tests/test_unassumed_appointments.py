import copy
import json
import unittest
from pathlib import Path
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.validate_corpus import title_proposal_errors

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL_IDS={'tp-jinshu076-huzhi-73', 'tp-jinshu065-wangqia-zhongshuling', 'tp-jinshu065-wangdao-87', 'tp-jinshu076-huzhi-83', 'tp-jinshu065-wangdao-93', 'tp-jinshu076-huzhi-78', 'tp-jinshu065-wangdao-102', 'tp-jinshu065-wangdao-97'}
NEW_IDS={'tp-wangdao4-110-6', 'tp-wangdao4-80-4'}


class UnassumedAppointments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters=[json.loads((ROOT/('corpus/jinshu/'+n+'.json')).read_text()) for n in ['065','076']]
        cls.people={p['id']for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        cls.cases=[(c,q)for c in cls.chapters for q in c['annotation']['title_proposals']]

    def test_eight_appointments_keep_declining_distinct_from_nonattendance(self):
        original=[(c,q)for c,q in self.cases if q['id'] in ORIGINAL_IDS]
        self.assertEqual({q['id']for _,q in original},ORIGINAL_IDS)
        self.assertEqual(len(original),8)
        self.assertEqual(sum(q['non_assumption_kind']=='declined'for _,q in original),4)
        for c,q in self.cases:
            self.assertTrue(unassumed_appointment_valid(q,c))
            self.assertEqual(title_proposal_errors(q,c,self.people),[])
            self.assertEqual(q['outcome'],'not_assumed')
            self.assertNotEqual(q['outcome'],'not_enacted')
            self.assertTrue(q['appointment_anchor']['surface'])
            self.assertIn(q['non_assumption_anchor']['surface'],q['evidence'][0]['quote'])

    def test_two_additional_appointments_keep_real_role_anchors_and_do_not_become_holdings(self):
        additional=[(c,q)for c,q in self.cases if q['id'] not in ORIGINAL_IDS]
        self.assertEqual({q['id']for _,q in additional},NEW_IDS)
        expected={
            'tp-wangdao4-80-4':('7r6_k52_qji_ABAAAA','散騎常侍','除','不拜',56,60),
            'tp-wangdao4-110-6':('7r6_k52_qji_ABAAF','中領軍','征補','不拜',70,73),
        }
        for c,q in additional:
            pid,title,verb,negative,start,end=expected[q['id']]
            self.assertEqual((q['person_id'],q['title'],q['appointment_anchor']['surface'],q['non_assumption_anchor']['surface']),(pid,title,verb,negative))
            self.assertEqual(q['non_assumption_kind'],'did_not_take_up')
            self.assertNotIn('role_mention_id',q)
            paragraph=next(p for p in c['paragraphs']if p['id']==q['role_anchor']['paragraph_id'])
            self.assertEqual(q['role_anchor'],dict(paragraph_id=paragraph['id'],start=start,end=end,surface=title))
            self.assertEqual(paragraph['text'][start:end],title)
            self.assertTrue(any(m['id']==q['person_mention_id'] and m.get('person_id')==pid for m in paragraph['mentions']))
            self.assertTrue(unassumed_appointment_valid(q,c))
            self.assertEqual(title_proposal_errors(q,c,self.people),[])
            holdings=json.loads((ROOT/'corpus/jinshu/065-titles.json').read_text())['holdings']
            self.assertFalse(any(h['person_id']==pid and h['title']==title and any(e.get('paragraph_id')==paragraph['id'] for e in h['evidence'])for h in holdings))
            # Role-coordinate/word corruption and a real wrong-recipient anchor must all fail.
            for mutate in [lambda x:x['role_anchor'].update(start=start+1),
                           lambda x:x['role_anchor'].update(surface='中書令'),
                           lambda x:x.update(person_id=next(m['person_id']for m in paragraph['mentions']if m.get('kind')=='person' and m.get('person_id')!=pid))]:
                bad=copy.deepcopy(q);mutate(bad)
                self.assertFalse(unassumed_appointment_valid(bad,c))
                self.assertTrue(title_proposal_errors(bad,c,self.people))

    def test_wrong_recipient_anchor_outcome_or_source_dimension_is_rejected(self):
        for c,q in self.cases:
            paragraph=next(p for p in c['paragraphs']if p['id']==q['evidence'][0]['paragraph_id'])
            if q.get('role_mention_id'):
                wrong_recipient=q['role_mention_id'] # actual unresolved-role mention, never a person
            else:
                # Actual other person in this same paragraph: 謝安 / 桓沖, not a fabricated ID.
                wrong_recipient=next(m['id']for m in paragraph['mentions']if m.get('kind')=='person' and m.get('person_id')!=q['person_id'])
            for mutate in [lambda x:x.update(outcome='not_enacted'),
                           lambda x:x.update(person_mention_id=wrong_recipient),
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
