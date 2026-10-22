"""Source-bound surname inheritance, independent synthetic people and witnesses."""
import copy
import unittest
from scripts.surname_from_father import validate

class SurnameFamilyChainTest(unittest.TestCase):
 def setUp(self):
  cid='c-fixture-family';sid='s-fixture';wid='w-fixture';bid='b-fixture'
  def paragraph(key,text,spec):
   mentions=[]
   for mid,surface,pid in spec:
    start=text.index(surface);mentions.append(dict(id=mid,kind='person',person_id=pid,surface=surface,start=start,end=start+len(surface)))
   return dict(id=key,text=text,mentions=mentions)
  p1=paragraph('p-head','沈澄，字明遠。父嵩。',[('m-head','沈澄','person-child'),('m-parent','嵩','person-parent')])
  p2=paragraph('p-son','澄之子岑。',[('m-father','澄','person-child'),('m-son','岑','person-son')])
  p3=paragraph('p-grandson','岑子岳。',[('m-sonfather','岑','person-son'),('m-grandson','岳','person-grandson')])
  self.chapter=dict(id=cid,source_id=sid,work_id=wid,book_id=bid,paragraphs=[p1,p2,p3])
  def assertion(key,child,father,p,sm,om,term):
   return dict(id=key,predicate='father',status='source_attested',subject_person_id=child,object_person_id=father,qualifiers=dict(source_term=term),evidence=[dict(chapter_id=cid,source_id=sid,work_id=wid,book_id=bid,paragraph_id=p['id'],quote=p['text'],subject_person_mention_id=sm,object_person_mention_id=om)])
  self.assertions=[assertion('a-parent','person-child','person-parent',p1,'m-head','m-parent','父嵩'),assertion('a-son','person-son','person-child',p2,'m-son','m-father','子岑'),assertion('a-grandson','person-grandson','person-son',p3,'m-grandson','m-sonfather','子岳')]
  self.seed=dict(id='n-full',person_id='person-child',surname='沈',ming='澄',chapter_id=cid,paragraph_id=p1['id'],person_mention_id='m-head',quote=p1['text'])
  def name(pid,ming,p,mid,steps):
   return dict(person_id=pid,surname='沈',ming=ming,chapter_id=cid,paragraph_id=p['id'],person_mention_id=mid,quote=p['text'],status='contextual_provisional',human_reviewed=False,surname_basis=dict(kind='contextual_surname_from_same_source_father_chain',status='contextual_provisional',human_reviewed=False,rationale='同源明文父子鏈；僅編輯承接姓。',source_name_record_id='n-full',source_full_quote=p1['text'],steps=steps))
  def step(a,direction):
   child=a['subject_person_id'];father=a['object_person_id'];x,y=(child,father) if direction=='child_to_father' else (father,child)
   return dict(assertion_id=a['id'],from_person_id=x,to_person_id=y,traversal=direction,source_term=a['qualifiers']['source_term'],evidence=copy.deepcopy(a['evidence'][0]))
  self.reverse=name('person-parent','嵩',p1,'m-parent',[step(self.assertions[0],'child_to_father')])
  self.forward=name('person-grandson','岳',p3,'m-grandson',[step(self.assertions[1],'father_to_child'),step(self.assertions[2],'father_to_child')])
 def check(self,n):validate(n,[self.seed],{self.chapter['id']:self.chapter},self.assertions)
 def test_reverse_explicit_father(self):self.check(self.reverse)
 def test_two_forward_generations(self):self.check(self.forward)
 def test_non_father_relations_rejected(self):
  for predicate in ('mother','adoptive_father','paternal_uncle','agnatic_cousin'):
   with self.subTest(predicate=predicate):
    original=self.assertions[1]['predicate'];self.assertions[1]['predicate']=predicate
    with self.assertRaises(ValueError):self.check(self.forward)
    self.assertions[1]['predicate']=original
 def test_changed_source_rejected_even_when_assertion_snapshot_matches(self):
  self.forward['surname_basis']['steps'][0]['evidence']['source_id']='s-other'
  self.assertions[1]['evidence'][0]['source_id']='s-other'
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_wrong_endpoint_rejected(self):
  self.forward['surname_basis']['steps'][0]['evidence']['object_person_mention_id']='m-son'
  self.assertions[1]['evidence'][0]['object_person_mention_id']='m-son'
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_cycle_rejected(self):
  self.forward['surname_basis']['steps'][1]['to_person_id']='person-child'
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_missing_first_edge_rejected(self):
  self.forward['surname_basis']['steps'].pop(0)
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_wrong_chapter_rejected(self):
  self.forward['surname_basis']['steps'][0]['evidence']['chapter_id']='c-other'
  self.assertions[1]['evidence'][0]['chapter_id']='c-other'
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_missing_full_name_rejected(self):
  self.seed['surname']=None
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_explicit_status_is_not_allowed(self):
  self.forward['status']='source_attested'
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_inferred_father_is_not_allowed(self):
  self.assertions[1]['status']='contextual_provisional'
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_complete_quote_required(self):
  self.forward['surname_basis']['steps'][0]['evidence']['quote']='子岑'
  self.assertions[1]['evidence'][0]['quote']='子岑'
  with self.assertRaises(ValueError):self.check(self.forward)
 def test_legacy_absent_basis_is_noop(self):validate({'surname':None},[],{},[])
 def test_legacy_unknown_basis_still_rejected(self):
  with self.assertRaises(ValueError):validate({'surname_basis':{'kind':'unrecognized'}},[],{},[])

if __name__=='__main__':unittest.main()
