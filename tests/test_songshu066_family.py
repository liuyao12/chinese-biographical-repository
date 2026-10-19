# coding: utf-8
import json
import unittest
from pathlib import Path
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog

ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())

class WangJinghongFamily(unittest.TestCase):
    def setUp(self):
        self.assertions=read('corpus/songshu/066-assertions.json')['assertions']
        self.a={a['id']:a for a in self.assertions}
        self.family=next(f for f in read('registry/family-assemblies.json')['assemblies']if f['id']=='family-langye-wang-dao')
        self.rows={m['person_id']:m for m in self.family['members']}
        self.jinghong=self.a['a-songshu066-family-huizhi-father']['object_person_id']
        self.hui=self.a['a-songshu066-family-huizhi-father']['subject_person_id']
        self.zan=self.a['a-songshu066-family-zanzhi-brother']['subject_person_id']
        self.sheng=self.a['a-songshu066-family-shengzhi-brother']['subject_person_id']
        self.yan=self.a['a-songshu066-family-yanzhi-father']['subject_person_id']

    def test_direct_fathers_and_sibling_derived_fathers_remain_distinct(self):
        for person in [self.hui,self.zan,self.sheng]:self.assertEqual(self.rows[person]['parent_person_id'],self.jinghong)
        self.assertEqual(self.rows[self.yan]['parent_person_id'],self.sheng)
        self.assertIsNone(self.rows[self.zan]['source_assertion_id'])
        self.assertIsNone(self.rows[self.sheng]['source_assertion_id'])
        self.assertEqual(self.rows[self.sheng]['parent_connection']['type'],'shared_father_through_sibling_chain')
        self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']in [self.zan,self.sheng]for a in self.assertions))

    def test_selected_family_navigation_reaches_same_wang_root(self):
        _,assembled=load_assemblies(ROOT,load_catalog(ROOT))
        for pid in [self.hui,self.zan,self.sheng,self.yan]:
            self.assertEqual(assembled[pid]['root_person_id'],self.family['root_person_id'])
        path=[];current=self.yan
        for _ in range(3):current=assembled[current]['parent_person_id'];path.append(current)
        self.assertEqual(path[:2],[self.sheng,self.jinghong])
        self.assertEqual(path[2],self.a['a-songshu066-wang-001']['object_person_id'])

    def test_brother_chain_records_relative_order_without_absolute_numbers(self):
        for key,older,younger in [('zanzhi-brother',self.hui,self.zan),('shengzhi-brother',self.zan,self.sheng)]:
            q=self.a['a-songshu066-family-'+key]['qualifiers']
            self.assertEqual(q['relative_birth_order']['older_person_id'],older)
            self.assertEqual(q['relative_birth_order']['younger_person_id'],younger)
            self.assertIsNone(q['relative_birth_order']['older_ordinal'])
            self.assertIsNone(q['relative_birth_order']['younger_ordinal'])
            self.assertNotIn('birth_order',q)

    def test_wife_daughter_and_their_spouses_are_not_conflated(self):
        wife=self.a['a-songshu066-family-wife'];daughter=self.a['a-songshu066-family-daughter-marriage']
        self.assertNotEqual(wife['subject_person_id'],daughter['subject_person_id'])
        self.assertEqual(wife['object_person_id'],self.jinghong)
        self.assertEqual(self.a['a-songshu066-family-daughter-father']['object_person_id'],self.jinghong)
        self.assertEqual(daughter['object_person_id'],self.a['a-songshu066-family-he-brothers']['object_person_id'])
        self.assertFalse(any(a['predicate']=='mother'and any(e['paragraph_id'].endswith(':line012')for e in a['evidence'])for a in self.assertions))

    def test_unpublished_initial_roots_are_fully_retired(self):
        people={p['id']for p in read('registry/persons.json')['persons']}
        for pid in ['srj_wtw_bth','lto_fe5_mjk','yvi_dta_v9t','w82_vop_qts','2c7_yrc_5f8']:
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/'exports/persons'/(pid+'.json')).exists())
            self.assertFalse((ROOT/'data/corpus/profiles'/(pid+'.json')).exists())

if __name__=='__main__':unittest.main()
