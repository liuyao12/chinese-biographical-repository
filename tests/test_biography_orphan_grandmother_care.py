# coding: utf-8
import unittest,copy
from scripts.biography_orphan_grandmother_care import valid,KIND
from scripts.reported_grandmother import reported_grandmother_valid
from scripts.non_parental_family import non_parental_relation_valid

class OrphanGrandmotherCareTests(unittest.TestCase):
 def setUp(self):
  # Synthetic grammar fixture; these are not historical identifications.
  text='甲字乙，生而母丙氏亡，為祖母丁氏所養。後事略。'
  self.p=dict(id='synthetic:p001',text=text,source_position={},mentions=[])
  for i,(surface,pid)in enumerate([('甲','child'),('丙氏','mother'),('丁氏','grandmother')]):
   start=text.index(surface);self.p['mentions'].append(dict(id=f'm{i}',surface=surface,start=start,end=start+len(surface),person_id=pid,kind='person'))
  binding=dict(kind=KIND,mother_person_mention_id='m1',clause_anchor=dict(paragraph_id=self.p['id'],start=0,end=text.index('。')+1,surface=text[:text.index('。')+1]))
  self.a=dict(id='synthetic-a',subject_person_id='child',object_person_id='grandmother',predicate='grandmother',status='source_attested',human_reviewed=False,qualifiers=dict(source_term='祖母',lineage='unspecified',generation_difference=-2,parent_person_id=None,relationship_basis=KIND,source_clause_binding=binding),evidence=[dict(chapter_id='synthetic',paragraph_id=self.p['id'],quote=text,subject_person_mention_id='m0',object_person_mention_id='m2')])
 def ps(self):return{self.p['id']:('synthetic',self.p)}
 def care(self):
  a=copy.deepcopy(self.a);a['predicate']='raised_by';a['qualifiers']=dict(source_term='為祖母丁氏所養',care_basis=KIND,legal_adoption_status='not_stated',source_clause_binding=a['qualifiers']['source_clause_binding']);return a
 def test_both_dispatchers_and_generic_ids(self):
  self.assertTrue(valid(self.a,self.ps()));self.assertTrue(reported_grandmother_valid(self.a,self.ps()));self.assertTrue(non_parental_relation_valid(self.care(),self.ps()))
  self.a['id']='anything-else';self.assertTrue(valid(self.a,self.ps()))
 def test_lineage_parent_distance_not_inferred(self):
  for key,value in [('lineage','paternal'),('parent_person_id','father'),('generation_difference',-1)]:
   with self.subTest(key=key):
    old=self.a['qualifiers'][key];self.a['qualifiers'][key]=value;self.assertFalse(valid(self.a,self.ps()));self.a['qualifiers'][key]=old
 def test_mother_cannot_equal_child_or_grandmother(self):
  for pid in ['child','grandmother']:
   self.p['mentions'][1]['person_id']=pid;self.assertFalse(valid(self.a,self.ps()))
 def test_wrong_evidence_or_mention_anchor(self):
  self.a['evidence'][0]['object_person_mention_id']='m1';self.assertFalse(valid(self.a,self.ps()))
  self.a['evidence'][0]['object_person_mention_id']='m2';self.p['mentions'][2]['start']+=1;self.assertFalse(valid(self.a,self.ps()))
 def test_outer_quote_negation_and_maternal_qualification(self):
  original=copy.deepcopy(self.p)
  for text in ['「'+original['text']+'」',original['text'].replace('亡','未亡'),original['text'].replace('祖母','外祖母')]:
   self.p=copy.deepcopy(original);self.p['text']=text;self.a['evidence'][0]['quote']=text;self.a['qualifiers']['source_clause_binding']['clause_anchor']['surface']=text[:text.index('。')+1];self.a['qualifiers']['source_clause_binding']['clause_anchor']['end']=text.index('。')+1;self.assertFalse(valid(self.a,self.ps()))
 def test_care_does_not_imply_adoption_or_mother(self):
  for key,value in [('legal_adoption_status','adopted'),('source_term','丁氏養之')]:
   a=self.care();a['qualifiers'][key]=value;self.assertFalse(valid(a,self.ps()))
  a=self.care();a['predicate']='mother';self.assertFalse(valid(a,self.ps()))
 def test_annotation_layers(self):
  for obj in [self.p,self.p['source_position'],*self.p['mentions']]:
   for key,value in [('source_layer','commentary'),('text_layer','annotation'),('annotator','agent'),('attached_note_to_paragraph_id','other')]:
    obj[key]=value;self.assertFalse(valid(self.a,self.ps()));del obj[key]
 def test_no_review_status_bypass_or_fourth_actor(self):
  self.a['human_reviewed']=True;self.assertTrue(valid(self.a,self.ps()));self.a['human_reviewed']=False
  self.p['mentions'].append(dict(id='fourth',surface='字',start=1,end=2,kind='person',person_id='fourth'));self.assertFalse(valid(self.a,self.ps()))
 def test_older_literal_grandmother_model_unchanged(self):
  a=copy.deepcopy(self.a);a['qualifiers'].pop('source_clause_binding');a['qualifiers']['relationship_basis']='literal_grandmother_title_clause'
  p=dict(id='old:p001',text='甲尊祖母丁氏',mentions=[dict(id='child',surface='甲',start=0,end=1,person_id='child',kind='person'),dict(id='grandmother',surface='丁氏',start=4,end=6,person_id='grandmother',kind='person')])
  a['evidence']=[dict(chapter_id='old',paragraph_id=p['id'],quote=p['text'],subject_person_mention_id='child',object_person_mention_id='grandmother')]
  self.assertTrue(reported_grandmother_valid(a,{p['id']:('old',p)}))
