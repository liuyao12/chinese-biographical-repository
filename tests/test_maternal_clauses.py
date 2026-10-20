"""Synthetic clauses test grammar binding; these are not historical assertions."""
import copy
import unittest
from scripts.maternal_clauses import maternal_clause_valid


def fixture(kind):
    cases = {
        'opening_grandchild_mother': ('甲乙孫也母丙氏', '甲', '丙氏', '母丙氏'),
        'named_child_yisui_mother': ('丁亦隨母在家', '丁', '母', '丁亦隨母'),
        'named_child_xianwei_qimu': ('戊賢謂其母己氏', '戊', '己氏', '其母己氏'),
        'named_child_selfinjury_qimu_calls': ('庚於是竊入寢室以刀斷鼻䝉被而卧其母呼與語不應', '庚', '母', '其母呼與語'),
    }
    text, child, mother, term = cases[kind]
    mentions = []
    for mid, surface, pid in [('child', child, 'synthetic-child'), ('mother', mother, 'synthetic-mother')]:
        pos = text.index(surface)
        mentions.append(dict(id=mid, surface=surface, person_id=pid, kind='person', start=pos, end=pos+len(surface)))
    if kind == 'opening_grandchild_mother':
        mentions.append(dict(id='ancestor',surface='乙',person_id='synthetic-ancestor',kind='person',start=1,end=2))
    p = dict(id='synthetic:p',text=text,mentions=mentions)
    start=text.index(term)
    a=dict(predicate='maternal_role',status='source_attested',human_reviewed=False,
           subject_person_id='synthetic-child',object_person_id='synthetic-mother',
           qualifiers=dict(source_term=term,role='mother_unspecified',biological_mother=None,
                           father_person_id=None,maternal_clause=dict(kind=kind,start=start,end=start+len(term))),
           evidence=[dict(chapter_id='synthetic-chapter',paragraph_id='synthetic:p',quote=text,
                          subject_person_mention_id='child',object_person_mention_id='mother')])
    return a, {'synthetic:p':('synthetic-chapter',p)}


class MaternalClauseGrammar(unittest.TestCase):
    kinds = ('opening_grandchild_mother','named_child_yisui_mother',
             'named_child_xianwei_qimu','named_child_selfinjury_qimu_calls')

    def test_four_narrow_clauses(self):
        for kind in self.kinds:
            with self.subTest(kind=kind):self.assertTrue(maternal_clause_valid(*fixture(kind)))

    def test_no_birth_father_or_marriage_inference(self):
        for kind in self.kinds:
            for key, value in [('biological_mother',True),('father_person_id','synthetic-father'),('spouse_person_id','synthetic-spouse')]:
                a,p=fixture(kind);a['qualifiers'][key]=value
                with self.subTest(kind=kind,key=key):self.assertFalse(maternal_clause_valid(a,p))

    def test_swapped_endpoints_and_wrong_word_position(self):
        for kind in self.kinds:
            a,p=fixture(kind);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
            self.assertFalse(maternal_clause_valid(a,p))
            a,p=fixture(kind);a['qualifiers']['maternal_clause']['start']+=1
            self.assertFalse(maternal_clause_valid(a,p))

    def test_truncated_quote_or_corrupt_anchor(self):
        for kind in self.kinds:
            a,p=fixture(kind);a['evidence'][0]['quote']=a['evidence'][0]['quote'][:-1]
            self.assertFalse(maternal_clause_valid(a,p))
            a,p=fixture(kind);p['synthetic:p'][1]['mentions'][0]['surface']='synthetic-not-the-text'
            self.assertFalse(maternal_clause_valid(a,p))

    def test_ancestor_cannot_replace_opening_child(self):
        a,p=fixture(self.kinds[0]);a['subject_person_id']='synthetic-ancestor';a['evidence'][0]['subject_person_mention_id']='ancestor'
        self.assertFalse(maternal_clause_valid(a,p))

    def test_negation_is_not_a_mother_assertion(self):
        for kind in self.kinds:
            a,ps=fixture(kind);p=ps['synthetic:p'][1];at=p['mentions'][0]['end'];p['text']=p['text'][:at]+'非'+p['text'][at:]
            for m in p['mentions']:
                if m['start']>=at:m['start']+=1;m['end']+=1
            b=a['qualifiers']['maternal_clause'];b['start']+=int(b['start']>=at);b['end']+=int(b['end']>=at)
            a['qualifiers']['source_term']=p['text'][b['start']:b['end']];a['evidence'][0]['quote']=p['text']
            self.assertFalse(maternal_clause_valid(a,ps))
