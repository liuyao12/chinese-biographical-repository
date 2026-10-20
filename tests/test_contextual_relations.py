"""Synthetic grammar fixtures, not historical source assertions."""
import copy
import unittest
from scripts.contextual_relations import teaching_clause_valid, weiqin_pair_valid

def teacher_fixture():
    text='甲字乙君初拜博士祭酒賜爵武城子常授君經書';start=text.index('常授');end=len(text)
    mentions=[dict(id='instructor',kind='person',person_id='synthetic-instructor',surface='甲',start=0,end=1),dict(id='transition',kind='person',person_id='synthetic-learner',surface='君',start=3,end=4),dict(id='learner',kind='person',person_id='synthetic-learner',surface='君',start=start+2,end=start+3)]
    p=dict(text=text,mentions=mentions)
    a=dict(predicate='teacher',subject_person_id='synthetic-learner',object_person_id='synthetic-instructor',status='source_attested',human_reviewed=False,
           qualifiers=dict(source_term='常授君經書',relationship_basis='teaching',teaching_clause_binding=dict(kind='biographical_subject_teaches_after_accession_office',start=start,end=end,transition_mention_id='transition')),
           evidence=[dict(chapter_id='synthetic-c',paragraph_id='synthetic-p',quote=text,subject_person_mention_id='learner',object_person_mention_id='instructor')])
    return a,{'synthetic-p':('synthetic-c',p)}

def kinship_fixture():
    text='三人别祖而甲乙為親';p=dict(text=text,mentions=[dict(id='first',kind='person',person_id='synthetic-first',surface='甲',start=5,end=6),dict(id='second',kind='person',person_id='synthetic-second',surface='乙',start=6,end=7)])
    a=dict(predicate='kinship_unspecified',subject_person_id='synthetic-first',object_person_id='synthetic-second',status='source_attested',human_reviewed=False,
           qualifiers=dict(source_term='甲乙為親',kinship_basis='explicit_weiqin_pair',generation_difference=None,exact_distance=None,lineage=None,common_ancestor_person_id=None,connecting_person_ids=None,kinship_clause_binding=dict(kind='biezu_weiqin_pair',start=5,end=9)),
           evidence=[dict(chapter_id='synthetic-c',paragraph_id='synthetic-p',quote=text,subject_person_mention_id='first',object_person_mention_id='second')])
    return a,{'synthetic-p':('synthetic-c',p)}

class ContextualRelations(unittest.TestCase):
    def test_both_positive(self):
        self.assertTrue(teaching_clause_valid(*teacher_fixture()));self.assertTrue(weiqin_pair_valid(*kinship_fixture()))
    def test_teacher_contract_student_to_instructor(self):
        a,p=teacher_fixture();a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];e=a['evidence'][0];e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id'];self.assertFalse(teaching_clause_valid(a,p))
    def test_office_grant_is_not_teaching(self):
        a,p=teacher_fixture();t=p['synthetic-p'][1]['text'];start=t.index('拜博士祭酒');a['qualifiers']['source_term']='拜博士祭酒';a['qualifiers']['teaching_clause_binding'].update(start=start,end=start+5);self.assertFalse(teaching_clause_valid(a,p))
    def test_kinship_cannot_add_generation_lineage_or_common_ancestor(self):
        for key,value in [('generation_difference',0),('exact_distance',2),('lineage','paternal'),('common_ancestor_person_id','synthetic'),('connecting_person_ids',['synthetic'])]:
            a,p=kinship_fixture();a['qualifiers'][key]=value;self.assertFalse(weiqin_pair_valid(a,p))
    def test_trimmed_quote_wrong_offset_or_wrong_endpoint_rejected(self):
        for maker,fn in [(teacher_fixture,teaching_clause_valid),(kinship_fixture,weiqin_pair_valid)]:
            a,p=maker();a['evidence'][0]['quote']=a['evidence'][0]['quote'][:-1];self.assertFalse(fn(a,p))
            a,p=maker();b=a['qualifiers'].get('teaching_clause_binding',a['qualifiers'].get('kinship_clause_binding'));b['start']+=1;self.assertFalse(fn(a,p))
            a,p=maker();a['object_person_id']='synthetic-wrong';self.assertFalse(fn(a,p))
    def test_teacher_negation_and_kinship_feiqin_rejected(self):
        for maker,fn in [(teacher_fixture,teaching_clause_valid),(kinship_fixture,weiqin_pair_valid)]:
            a,ps=maker();p=ps['synthetic-p'][1];b=a['qualifiers'].get('teaching_clause_binding',a['qualifiers'].get('kinship_clause_binding'));at=b['start']+1;p['text']=p['text'][:at]+'非'+p['text'][at:]
            for m in p['mentions']:
                if m['start']>=at:m['start']+=1;m['end']+=1
            b['end']+=1;a['qualifiers']['source_term']=p['text'][b['start']:b['end']];a['evidence'][0]['quote']=p['text'];self.assertFalse(fn(a,ps))

    def test_literal_feiqin_and_granting_an_office_are_rejected(self):
        for maker,fn,old,new in [(teacher_fixture,teaching_clause_valid,'經書','官職'),(kinship_fixture,weiqin_pair_valid,'為親','非親')]:
            a,p=maker();text=p['synthetic-p'][1]['text'].replace(old,new);p['synthetic-p'][1]['text']=text;a['evidence'][0]['quote']=text;a['qualifiers']['source_term']=a['qualifiers']['source_term'].replace(old,new);self.assertFalse(fn(a,p))
