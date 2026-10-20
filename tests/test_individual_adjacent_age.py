"""Synthetic child-age bindings: a parent's death must not inherit the child's age."""
import unittest,copy
from scripts.individual_adjacent_age import individual_adjacent_age_errors
class IndividualAdjacentAgeTests(unittest.TestCase):
 def example(self):
  p={'id':'synthetic:p1','text':'甲死有一男年五六嵗','mentions':[{'id':'synthetic:parent','kind':'person','person_id':'parent','surface':'甲','start':0,'end':1},{'id':'synthetic:child','kind':'person','person_id':'child','surface':'男','start':4,'end':5}]}
  a={'person_id':'child','source_number':'五六','source_term':'年五六嵗','value':None,'birth_year':None,'unit':'source_age_years','counting':'unspecified_source_age','status':'source_attested','reporting_status':'approximate_report','human_reviewed':False,'reviewer':'synthetic test','approximation':{'kind':'adjacent_age_numbers','numbers':[5,6]},'subject_scope':{'kind':'immediate_child_age','paragraph_id':p['id'],'start':2,'end':9,'source_term':'有一男年五六嵗'},'approximation_interpretation':{'status':'editorial_provisional','human_reviewed':False,'reviewer':'synthetic test','rationale':'adjacent numerals are approximate'},'evidence':[{'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':'synthetic:child'}]};return a,p
 def test_source_bound_child_and_random_ids(self):
  a,p=self.example();self.assertEqual([],individual_adjacent_age_errors(a,p));a['person_id']='another-child';p['mentions'][1]['person_id']='another-child';self.assertEqual([],individual_adjacent_age_errors(a,p))
 def test_parent_anchor_or_identity_is_rejected(self):
  for key,value in [('person_id','parent'),('person_mention_id','synthetic:parent')]:
   a,p=self.example()
   if key=='person_id':a[key]=value
   else:a['evidence'][0][key]=value
   self.assertTrue(individual_adjacent_age_errors(a,p))
 def test_exact_age_bounds_or_birth_year_rejected(self):
  for key,value in [('value',5),('birth_year',244),('bounds',{'lower':5,'upper':6}),('normalized_date',{'year':249})]:
   a,p=self.example();a[key]=value;self.assertTrue(individual_adjacent_age_errors(a,p))
 def test_wrong_or_boolean_numerals_rejected(self):
  for numbers in [[5,7],[6,5],[True,6],[5]]:
   a,p=self.example();a['approximation']['numbers']=numbers;self.assertTrue(individual_adjacent_age_errors(a,p))
 def test_wrong_quote_or_clause_bounds_rejected(self):
  for field,value in [('quote','有一男年五六嵗'),('start',1),('end',8)]:
   a,p=self.example()
   if field=='quote':a['evidence'][0][field]=value
   else:a['subject_scope'][field]=value
   self.assertTrue(individual_adjacent_age_errors(a,p))
 def test_incompatible_group_or_review_status_rejected(self):
  for key,value in [('group_reference',{}),('reporting_status','direct_report'),('human_reviewed',True),('counting','nominal_age')]:
   a,p=self.example();a[key]=value;self.assertTrue(individual_adjacent_age_errors(a,p))
 def test_negated_child_phrase_is_not_asserted(self):
  a,p=self.example();p['text']='甲死無一男年五六嵗';a['evidence'][0]['quote']=p['text'];a['subject_scope']['source_term']='無一男年五六嵗';self.assertTrue(individual_adjacent_age_errors(a,p))
