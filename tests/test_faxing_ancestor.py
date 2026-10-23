import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
from scripts.collateral_descendant_ancestor import valid
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies
class Contract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(__file__).resolve().parents[1];cls.cat=load_catalog(cls.root);_,rs=load_assemblies(cls.root,cls.cat);cls.rows=rs;cls.member=next(x for x in rs.values()if x.get('ancestor_connection',{}).get('type')=='ancestor_above_unnamed_sibling_descendant');cls.claims={a['id']:a for r in cls.cat[1]for a in r.get('assertions',[])};cls.chapters={r['id']:r for r in cls.cat[1]if r.get('record_type')=='marked_chapter'}
 def setUp(self):self.m=copy.deepcopy(self.member);self.a=copy.deepcopy(self.claims);self.c=copy.deepcopy(self.chapters)
 def check(self):return valid(self.m,self.rows,self.a,self.c,self.root)
 def kin(self):return self.a[self.m['ancestor_connection']['collateral_descendant_assertion_id']]
 def test_actual_positive(self):self.assertTrue(self.check())
 def test_generation(self):self.m['generation_distance']=7;self.assertFalse(self.check())
 def test_step(self):self.kin()['qualifiers']['source_generation_steps'][0]['generation_distance']=3;self.assertFalse(self.check())
 def test_maternal(self):self.kin()['qualifiers']['lineage']='maternal';self.assertFalse(self.check())
 def test_named_brother(self):self.kin()['qualifiers']['unnamed_ancestor_role']['person_id']='dqd_5q9_pkz_BA';self.assertFalse(self.check())
 def test_reversal(self):k=self.kin();k['subject_person_id'],k['object_person_id']=k['object_person_id'],k['subject_person_id'];self.assertFalse(self.check())
 def test_cousin(self):self.kin()['qualifiers']['unnamed_ancestor_role']['relation_to_reference']='agnatic_cousin';self.assertFalse(self.check())
 def test_parent_fabrication(self):self.m['parent_person_id']='dqd_5q9_pkz_BA';self.assertFalse(self.check())
 def test_known_father(self):self.a['contradictory']=dict(predicate='father',subject_person_id=self.m['person_id'],object_person_id='dqd_5q9_pkz_BA');self.assertFalse(self.check())
 def test_wrong_ancestor(self):self.m['ancestor_person_id']='dqd_5q9_pkz';self.assertFalse(self.check())
 def test_wrong_source_role(self):self.kin()['evidence'][0]['subject_person_mention_id']=self.kin()['evidence'][0]['object_person_mention_id'];self.assertFalse(self.check())
 def test_source_text_change(self):e=self.kin()['evidence'][0];p=next(p for p in self.c[e['chapter_id']]['paragraphs']if p['id']==e['paragraph_id']);p['text']=p['text'].replace('兄玄孫','弟玄孫');self.assertFalse(self.check())
 def test_source_layer(self):e=self.kin()['evidence'][0];p=next(p for p in self.c[e['chapter_id']]['paragraphs']if p['id']==e['paragraph_id']);p['text_layer']='commentary';self.assertFalse(self.check())
 def test_scope(self):self.kin()['fixed_source_fact_binding']['key']='wrong-recipe';self.assertFalse(self.check())
