import copy
import hashlib
import json
import unittest
from pathlib import Path
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.validate_corpus import title_proposal_errors
from scripts.lexical_annotations import non_person_errors
from scripts.noble_transfers import noble_transfer_errors

ROOT=Path(__file__).resolve().parents[1]

class XunUnassumedAppointments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=json.loads((ROOT/'corpus/jinshu/075.json').read_text())
        cls.people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        cls.cases=[p for p in cls.chapter['annotation']['title_proposals'] if p['id'].startswith('tp-jinshu075-unassumed-')]

    def test_six_refusals_do_not_become_service(self):
        self.assertEqual(len(self.cases),6)
        self.assertEqual(sum('context' in q['evidence'][0] for q in self.cases),2)
        for q in self.cases:
            with self.subTest(title=q['title'],id=q['id']):
                self.assertTrue(unassumed_appointment_valid(q,self.chapter))
                self.assertEqual(title_proposal_errors(q,self.chapter,self.people),[])
                self.assertEqual(q['outcome'],'not_assumed')
        self.assertEqual({q['non_assumption_anchor']['surface'] for q in self.cases},{'不拜','皆不就','讓不拜'})
        holdings=json.loads((ROOT/'corpus/jinshu/075-titles.json').read_text())['holdings']
        for q in self.cases:
            self.assertFalse(any(h['person_id']==q['person_id'] and h['title']==q['title']
                                 and any(e['paragraph_id']==q['evidence'][0]['paragraph_id'] for e in h['evidence'])
                                 for h in holdings))

    def test_carried_subject_requires_fixed_blank_gap(self):
        q=next(q for q in self.cases if 'context' in q['evidence'][0])
        for mutate in ['missing','prose','revision','hash','range']:
            with self.subTest(mutate=mutate):
                c=copy.deepcopy(self.chapter)
                gaps=c['source']['normalization']['verified_blank_line_gaps']
                gap=next(g for g in gaps if g['source_lines']==[155,155])
                if mutate=='missing':gaps.remove(gap)
                elif mutate=='prose':gap['raw_quote']='奏';gap['raw_quote_sha256']=hashlib.sha256('奏'.encode()).hexdigest()
                elif mutate=='revision':gap['revision_id']+=1
                elif mutate=='hash':gap['raw_quote_sha256']='0'*64
                else:gap['source_lines']=[154,155]
                self.assertFalse(unassumed_appointment_valid(q,c))
                self.assertTrue(title_proposal_errors(q,c,self.people))

    def test_carried_subject_cannot_change_to_ruler_or_skip_source_context(self):
        q=next(q for q in self.cases if 'context' in q['evidence'][0])
        for mutation in ['recipient','context-person','quote','missing-context','wrong-paragraph']:
            bad=copy.deepcopy(q)
            if mutation=='recipient':bad['person_id']='84i_4jp_gmc'
            elif mutation=='context-person':bad['evidence'][0]['context']['person_mention_id']='not-a-mention'
            elif mutation=='quote':bad['evidence'][0]['context']['quote']='無妄言'
            elif mutation=='missing-context':bad['evidence'][0].pop('context')
            else:bad['evidence'][0]['context']['paragraph_id']=q['evidence'][0]['paragraph_id']
            with self.subTest(mutation=mutation):
                self.assertFalse(unassumed_appointment_valid(bad,self.chapter))
                self.assertTrue(title_proposal_errors(bad,self.chapter,self.people))

    def test_a_different_named_recipient_in_assignment_is_not_bypassed(self):
        q=self.cases[0];c=copy.deepcopy(self.chapter)
        p=next(p for p in c['paragraphs'] if p['id']==q['evidence'][0]['paragraph_id'])
        role=next(m for m in p['mentions'] if m['id']==q['role_mention_id'])
        p['mentions'].append(dict(id='synthetic-conflicting-recipient',kind='person',person_id='84i_4jp_gmc',start=role['start'],end=role['start']+1,surface=role['surface'][0]))
        self.assertFalse(unassumed_appointment_valid(q,c))

    def test_explicit_declining_cannot_be_reclassified_as_unexplained_nonattendance(self):
        q=copy.deepcopy(next(q for q in self.cases if q['non_assumption_anchor']['surface']=='讓不拜'))
        q['non_assumption_kind']='did_not_take_up'
        q['non_assumption_anchor']['start']+=1
        q['non_assumption_anchor']['surface']='不拜'
        self.assertFalse(unassumed_appointment_valid(q,self.chapter))

    def test_refusal_and_complete_quote_are_required(self):
        for q in self.cases:
            bad=copy.deepcopy(q);bad['evidence'][0]['quote']=q['title']
            self.assertFalse(unassumed_appointment_valid(bad,self.chapter))
            bad=copy.deepcopy(q);bad['non_assumption_anchor']['surface']='拜'
            self.assertFalse(unassumed_appointment_valid(bad,self.chapter))

    def test_office_component_does_not_manufacture_a_crown_prince_mention(self):
        p=next(p for p in self.chapter['paragraphs'] if p['source_position']['first_line']==144)
        m=next(m for m in p['mentions'] if m['surface']=='太子')
        self.assertEqual(m['kind'],'non_person')
        self.assertIsNone(m['person_id'])
        self.assertEqual(non_person_errors(m,p['text']),[])
        for change in [{'basis_quote':'太子'}, {'person_id':'dkn_ge4_286_AAAAAAAAA'}, {'basis_quote':'太子太保'}]:
            bad=copy.deepcopy(m);bad.update(change)
            self.assertTrue(non_person_errors(bad,p['text']))

    def test_pingle_transfer_ends_quling_without_inventing_a_year(self):
        records=json.loads((ROOT/'corpus/jinshu/075-titles.json').read_text())['holdings']
        titles={h['id']:h for h in records}
        h=next(h for h in records if h['title']=='平樂伯')
        paras={p['id']:(self.chapter['id'],p) for p in self.chapter['paragraphs']}
        mentions={m['id']:(self.chapter['id'],p['id'],m) for p in self.chapter['paragraphs'] for m in p['mentions']}
        chapters={self.chapter['id']:self.chapter}
        self.assertEqual(noble_transfer_errors(h,titles,paras,mentions,chapters),[])
        previous=titles[h['transfer_basis']['previous_holding_id']]
        self.assertEqual(previous['title'],'曲陵公')
        self.assertEqual(previous['effective_period']['end']['evidence'],h['effective_period']['start']['evidence'])
        self.assertIsNone(h['effective_period']['start']['date_expression'])
        self.assertNotIn('normalized_date',h['effective_period']['start'])
        bad=copy.deepcopy(h);bad['transfer_basis']['source_term']='改封平樂伯'
        self.assertTrue(noble_transfer_errors(bad,titles,paras,mentions,chapters))
        badchapters=copy.deepcopy(chapters)
        badchapters[self.chapter['id']]['source']['normalization']['verified_blank_line_gaps']=[]
        self.assertTrue(noble_transfer_errors(h,titles,paras,mentions,badchapters))
        badtitles=copy.deepcopy(titles)
        badtitles[previous['id']]['effective_period']['end']['date_expression']='咸和三年'
        self.assertTrue(noble_transfer_errors(h,badtitles,paras,mentions,chapters))

if __name__=='__main__':unittest.main()
