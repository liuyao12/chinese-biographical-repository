"""Literal biography-head uncle and named 從兄 preserve direction and unknown distance."""
import copy
import unittest
from scripts.song059_kinship import inverse_xiongzi_valid,named_congxiong_group_valid
from scripts.directed_uncle_roles import paternal_uncle_direction_valid
from scripts.historical_family_clauses import explicit_congdi_valid

def fixture():
    cid='synthetic-song059';pid=cid+':p001'
    text='張暢字少微呉郡呉人呉興太守邵兄子也暢少與從兄敷演鏡齊名'
    marks=[]
    for i,(surface,start,person)in enumerate([('張暢',0,'main'),('邵',13,'uncle'),('暢',17,'main'),('敷',22,'fu'),('演',23,'yan'),('鏡',24,'jing')]):
        assert text[start:start+len(surface)]==surface
        marks.append(dict(id='m'+str(i),kind='person',start=start,end=start+len(surface),surface=surface,person_id=person))
    paragraphs={pid:(cid,dict(id=pid,text=text,mentions=marks))}
    assertions=[]
    for i,target in enumerate(marks[1:2]+marks[3:]):
        uncle=i==0;s=marks[0]if uncle else marks[2];term='邵兄子也'if uncle else '暢少與從兄敷演鏡齊名';start=13 if uncle else 17
        binding=dict(kind='biography_head_named_uncle_xiongzi'if uncle else'named_subject_congxiong_group',start=start,end=start+len(term))
        q=dict(source_term=term,source_clause_binding=binding)
        if not uncle:
            binding['group_member_mention_ids']=[m['id']for m in marks[3:]]
            q['kinship_structure']=dict(lineage='paternal',generation_difference=0,collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age='younger')
        assertions.append(dict(id='a'+str(i),subject_person_id=s['person_id'],object_person_id=target['person_id'],predicate='paternal_uncle'if uncle else'agnatic_cousin',status='source_attested',human_reviewed=False,qualifiers=q,evidence=[dict(chapter_id=cid,paragraph_id=pid,quote=text,subject_person_mention_id=s['id'],object_person_mention_id=target['id'])]))
    return assertions,paragraphs

def verify_cases(case):
    assertions,paragraphs=fixture();count=0
    for a in assertions:
        direct=inverse_xiongzi_valid if a['predicate']=='paternal_uncle'else named_congxiong_group_valid
        hook=paternal_uncle_direction_valid if a['predicate']=='paternal_uncle'else explicit_congdi_valid
        case.assertTrue(direct(a,paragraphs));case.assertTrue(hook(a,paragraphs));count+=1
        for mutation in ['reverse','offset','quote','negative','wrong_endpoint','invented_father']:
            b=copy.deepcopy(a);ps=copy.deepcopy(paragraphs)
            if mutation=='reverse':b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id']
            if mutation=='offset':b['qualifiers']['source_clause_binding']['start']+=1
            if mutation=='quote':b['evidence'][0]['quote']=b['evidence'][0]['quote'][1:]
            if mutation=='negative':ps[b['evidence'][0]['paragraph_id']][1]['text']='非'+ps[b['evidence'][0]['paragraph_id']][1]['text']
            if mutation=='wrong_endpoint':b['evidence'][0]['object_person_mention_id']=b['evidence'][0]['subject_person_mention_id']
            if mutation=='invented_father':b['qualifiers']['father_person_id']='invented'
            case.assertFalse(direct(b,ps),(a['id'],mutation));case.assertFalse(hook(b,ps),(a['id'],mutation));count+=1
    return count

class Song059KinshipTests(unittest.TestCase):
    def test_literal_roles_and_guarded_rejections(self):self.assertEqual(verify_cases(self),28)
    def test_agnatic_distance_and_unknown_common_ancestor_stay_null(self):
        rows,_=fixture()
        for a in rows[1:]:
            self.assertIsNone(a['qualifiers']['kinship_structure']['distance']);self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id'])
            self.assertEqual(a['qualifiers']['kinship_structure']['subject_relative_age'],'younger')
        self.assertNotIn('father_person_id',rows[0]['qualifiers'])
    def test_input_source_and_assertions_unchanged(self):
        rows,ps=fixture();before=copy.deepcopy((rows,ps))
        for a in rows:
            direct=inverse_xiongzi_valid if a['predicate']=='paternal_uncle'else named_congxiong_group_valid
            hook=paternal_uncle_direction_valid if a['predicate']=='paternal_uncle'else explicit_congdi_valid
            self.assertTrue(direct(a,ps));self.assertTrue(hook(a,ps))
        self.assertEqual((rows,ps),before)
if __name__=='__main__':unittest.main()
