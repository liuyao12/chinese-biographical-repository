"""Actual current-source C40 maternal uncle; no fixed person-ID exemptions."""
from pathlib import Path
import copy
import json
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

class WangqianMaternalUncleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts import fixed_wuyingdian_jin040_jiachong as m
        from scripts.person_bundle import load_catalog
        cls.m=m
        cls.people,cls.records=load_catalog(ROOT)
        cls.ch=m._c40_chapter(ROOT)
        cls.state=m.complete_unit_state(cls.ch,ROOT,cls.people,cls.records)
        cls.case=json.loads((ROOT/m.WQ_CASE_PATH).read_bytes())
        cls.record=m._c40_read(ROOT,m.WQ_RECORD_PATH)
        cls.assertion=cls.record['assertions'][0]
        cls.paragraphs={p['id']:(m.CID,p)for p in cls.ch['paragraphs']}

    def test_actual_root_complete_owner_and_direction(self):
        m=self.m;a=self.assertion;roles=self.state['roles']
        self.assertTrue(m.validate_source(self.ch,ROOT))
        self.assertTrue(m.wangqian_maternal_uncle_valid(a,self.record,self.paragraphs,ROOT))
        self.assertEqual((a['subject_person_id'],a['object_person_id']),(roles['simayan'],roles['wangqian']))
        self.assertEqual(a['predicate'],'maternal_uncle')
        self.assertEqual(a['qualifiers']['generation_difference'],-1)
        self.assertEqual(a['qualifiers']['lineage'],'maternal')
        self.assertIsNone(a['qualifiers']['mother_person_id'])
        e=a['evidence'][0];p=self.paragraphs[e['paragraph_id']][1]
        sm=next(v for v in p['mentions']if v['id']==e['subject_person_mention_id'])
        om=next(v for v in p['mentions']if v['id']==e['object_person_mention_id'])
        self.assertEqual(p['text'][sm['end']:om['start']],'舅羽林監')
        self.assertEqual(self.case['anchors']['office']['lexical_role'],'office_title_not_place')
        self.assertEqual(p['text'][om['end']:om['end']+2],'前妻')

    def rejected(self,mutate):
        a=copy.deepcopy(self.assertion);r=copy.deepcopy(self.record);p=copy.deepcopy(self.paragraphs)
        mutate(a,r,p)
        self.assertFalse(self.m.wangqian_maternal_uncle_valid(a,r,p,ROOT))

    def test_wrong_actor_and_one_end_rekey_rejected(self):
        # Use a real different role endpoint, not a permanently reserved PID.
        other=self.state['roles']['chong']
        self.rejected(lambda a,r,p:a.update(subject_person_id=other))
        self.rejected(lambda a,r,p:a.update(object_person_id=other))
        self.rejected(lambda a,r,p:a.update(subject_person_id=a['object_person_id'],object_person_id=a['subject_person_id']))

    def test_source_context_and_quote_rejected(self):
        self.rejected(lambda a,r,p:a['evidence'][0].update(source_id='wrong-source'))
        self.rejected(lambda a,r,p:a['evidence'][0].update(subject_person_mention_id=self.m.CID+':p014:m0090'))
        self.rejected(lambda a,r,p:a['evidence'][0].update(quote='帝舅羽林監王虔'))
        self.rejected(lambda a,r,p:p[self.m.CID+':p015'][1].update(text='錯'))

    def test_unstated_mother_and_office_are_not_inferred(self):
        self.rejected(lambda a,r,p:a['qualifiers'].update(mother_person_id=self.state['roles']['wangqianwife']))
        self.rejected(lambda a,r,p:a['qualifiers'].update(intervening_place_name='羽林監'))

    def test_second_row_rejected_by_complete_owner(self):
        m=self.m;original=m._c40_read
        bad=copy.deepcopy(self.record);bad['assertions'].append(copy.deepcopy(self.assertion))
        def read(root,rel):return bad if rel==m.WQ_RECORD_PATH else original(root,rel)
        with patch.object(m,'_c40_read',read):
            with self.assertRaises(ValueError):m.complete_unit_state(self.ch,ROOT)

    def test_missing_or_mutated_catalog_sidecar_rejected(self):
        records=[r for r in self.records if not self.m.same(r,self.record)]
        with self.assertRaises(ValueError):self.m.complete_unit_state(self.ch,ROOT,self.people,records)
        bad=copy.deepcopy(self.record);bad['assertions'][0]['object_person_id']=self.state['roles']['chong']
        with self.assertRaises(ValueError):self.m.complete_unit_state(self.ch,ROOT,self.people,records+[bad])

    def test_full_case_metadata_and_hash_remain_bound(self):
        b=(ROOT/self.m.WQ_CASE_PATH).read_bytes()
        with self.assertRaises(ValueError):
            self.m.validate_wangqian_candidate_bytes(self.assertion,self.record,self.paragraphs,ROOT,b+b' ')
        case=copy.deepcopy(self.case);case['context_paragraphs'][0]['text']='錯'
        with self.assertRaises(ValueError):
            self.m._wangqian_case_with_state(self.assertion,self.record,self.paragraphs,self.state,case)

    def test_consistent_in_memory_rekey_is_not_pid_whitelisted(self):
        old=self.state['roles']['simayan'];new='private-consistent-role-substitution'
        def sub(v):
            if type(v)is dict:return{k:sub(x)for k,x in v.items()}
            if type(v)is list:return[sub(x)for x in v]
            return new if v==old else v
        state=sub(self.state);record=sub(self.record)
        paragraphs={p['id']:(self.m.CID,p)for p in state['chapter']['paragraphs']}
        self.assertTrue(self.m._wangqian_case_with_state(record['assertions'][0],record,paragraphs,state,self.case))
        bad=copy.deepcopy(record['assertions'][0]);bad['object_person_id']=new
        with self.assertRaises(ValueError):self.m._wangqian_case_with_state(bad,record,paragraphs,state,self.case)

if __name__=='__main__':unittest.main()
