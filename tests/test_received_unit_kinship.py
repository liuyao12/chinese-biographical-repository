"""Synthetic independent complete-unit role semantics, plus actual source contracts."""
import copy,hashlib,unittest
from unittest.mock import patch
from scripts import received_unit_kinship as H

def fixture():
 texts=['蔡顯，字文昭。父玄，祖珪。','有二子，明、昶。','昶字景弘。無子，以兄子寧嗣。']
 tokens=[[('蔡顯','alpha'),('文昭','alpha'),('玄','beta'),('珪','gamma')],[('明','delta'),('昶','epsilon')],[('昶','epsilon'),('景弘','epsilon'),('寧','zeta')]]
 ps={};bp={};recipes={};groups={}
 for i,(t,ts)in enumerate(zip(texts,tokens)):
  key='p'+str(i+1).zfill(3);pid='test-chapter:'+key;cursor=0;ms=[];template='';last=0;roles={}
  for j,(word,who)in enumerate(ts):
   st=t.index(word,cursor);r=key+'r'+str(j);mid=pid+':m'+str(j);m=dict(id=mid,kind='person',person_id=who,start=st,end=st+len(word),surface=word);ms.append(m);roles[r]=mid;template+=t[last:st]+'<'+r+'>';last=m['end'];cursor=last;groups.setdefault(who,[]).append(r)
  template+=t[last:];p=dict(id=pid,text=t,text_layer='received_chapter',source_position={'revision_id':7},mentions=ms);ps[pid]=('test-chapter',p);recipes[key]=template;bp[key]=dict(paragraph_id=pid,paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),roles=roles)
 slots={'father':dict(predicate='father',subject_role='p002r0',object_role='p001r0',source_term='有二子',subject_paragraph_key='p002',object_paragraph_key='p001',evidence_paragraph_keys=['p001','p002']), 'ritual':dict(predicate='ritual_successor_of',subject_role='p003r2',object_role='p003r0',source_term='以兄子寧嗣',subject_paragraph_key='p003',object_paragraph_key='p003'), 'uncle':dict(predicate='paternal_uncle',subject_role='p003r2',object_role='p003r0',source_term='兄子',subject_paragraph_key='p003',object_paragraph_key='p003')}
 recipe=dict(paragraphs=recipes,same_identity_roles=list(groups.values()),distinct_identity_roles=[['p001r0','p001r2'],['p002r0','p002r1']],slots=slots)
 b=dict(kind='biography_family_clause',rule=H.RULE,frame='synthetic',paragraphs=bp,human_reviewed=False,slot='father');ch=dict(id='test-chapter',work_id='work-test',book_id='book-test',source_id='source-test')
 return ps,recipe,b,ch
class ReceivedUnitFamilyTests(unittest.TestCase):
 def setUp(self):
  self.ps,self.recipe,self.b,self.ch=fixture();self.ctx=patch.dict(H.FRAMES,{'synthetic':self.recipe});self.ctx.start()
 def tearDown(self):self.ctx.stop()
 def assertion(self,slot='father'):
  b=copy.deepcopy(self.b);b['slot']=slot;_,ps,rs,_=H.unit(b,self.ps);s=self.recipe['slots'][slot];e=H.evidence(self.ch,ps,s,rs);a=dict(id='synthetic-'+slot,predicate=s['predicate'],subject_person_id=rs[s['subject_role']]['person_id'],object_person_id=rs[s['object_role']]['person_id'],status='source_attested',human_reviewed=False,qualifiers=H.qualifiers(s,rs,b),evidence=e)
  if len(e)>1:a['context']=dict(kind='received_biography_family_unit',paragraph_ids=[x['paragraph_id']for x in e])
  return a
 def test_named_two_sons_head_context(self):
  a=self.assertion();self.assertEqual((a['subject_person_id'],a['object_person_id']),('delta','alpha'));self.assertTrue(H.valid(a,self.ps))
 def test_reverse_both_evidence_and_endpoints_rejected(self):
  a=self.assertion();a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
  for e in a['evidence']:
   sm=e.pop('subject_person_mention_id',None);om=e.pop('object_person_mention_id',None)
   if sm:e['object_person_mention_id']=sm
   if om:e['subject_person_mention_id']=om
  self.assertFalse(H.valid(a,self.ps))
 def test_wrong_same_name_id_rejected(self):
  a=self.assertion('ritual');ps=copy.deepcopy(self.ps);ps['test-chapter:p003'][1]['mentions'][0]['person_id']='unrelated-epsilon';self.assertFalse(H.valid(a,ps))
 def test_wrong_role_position_rejected(self):
  a=self.assertion();a['qualifiers']['source_clause_binding']['paragraphs']['p002']['roles']['p002r0']='test-chapter:p002:m1';self.assertFalse(H.valid(a,self.ps))
 def test_truncated_quote_rejected(self):
  a=self.assertion();a['evidence'][0]['quote']='蔡顯';self.assertFalse(H.valid(a,self.ps))
 def test_missing_intervening_paragraph_rejected(self):
  a=self.assertion();a['qualifiers']['source_clause_binding']['paragraphs'].pop('p002');self.assertFalse(H.valid(a,self.ps))
 def test_negated_source_and_rehash_rejected(self):
  a=self.assertion();ps=copy.deepcopy(self.ps);p=ps['test-chapter:p002'][1];p['text']='未'+p['text'];a['qualifiers']['source_clause_binding']['paragraphs']['p002']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.assertFalse(H.valid(a,ps))
 def test_parent_cannot_be_mother_or_adoptive(self):
  for pred in('mother','adoptive_father','paternal_uncle'):
   a=self.assertion();a['predicate']=pred;self.assertFalse(H.valid(a,self.ps))
 def test_ritual_is_not_adoption(self):
  a=self.assertion('ritual');self.assertTrue(H.valid(a,self.ps));self.assertEqual(a['qualifiers']['legal_adoption_status'],'not_stated');a['predicate']='adoptive_father';self.assertFalse(H.valid(a,self.ps))
 def test_unknown_nephew_father_not_added(self):
  a=self.assertion('uncle');self.assertTrue(H.valid(a,self.ps));self.assertIsNone(a['qualifiers']['father_person_id']);a['qualifiers']['father_person_id']='delta';self.assertFalse(H.valid(a,self.ps))
 def test_unknown_parent_order_is_machine_readable_and_not_numbered(self):
  a=self.assertion('uncle');q=a['qualifiers']['parent_generation_relative_birth_order'];self.assertIsNone(q['older_person_id']);self.assertEqual(q['younger_person_id'],'epsilon');self.assertEqual(q['operator'],'lt');self.assertIsNone(q['older_ordinal']);self.assertTrue(H.valid(a,self.ps));q['operator']='gt';self.assertFalse(H.valid(a,self.ps))
 def test_wrong_chapter_evidence_rejected(self):
  a=self.assertion();a['evidence'][0]['chapter_id']='other';self.assertFalse(H.valid(a,self.ps))
 def test_cycle_and_alias_substitution_rejected(self):
  a=self.assertion();a['object_person_id']=a['subject_person_id'];self.assertFalse(H.valid(a,self.ps));a=self.assertion();a['qualifiers']['source_clause_binding']['paragraphs']['p001']['paragraph_id']='test-chapter:p002';self.assertFalse(H.valid(a,self.ps))
 def test_generic_identity_renaming_not_allowlist(self):
  a=self.assertion('ritual');ps=copy.deepcopy(self.ps)
  for _,p in ps.values():
   for m in p['mentions']:m['person_id']='new-'+m['person_id']
  a['subject_person_id']='new-'+a['subject_person_id'];a['object_person_id']='new-'+a['object_person_id'];self.assertTrue(H.valid(a,ps))
 def test_explicit_biological_or_ordinal_not_added(self):
  a=self.assertion();a['qualifiers']['birth_order']={'ordinal':1};self.assertFalse(H.valid(a,self.ps));a=self.assertion();a['qualifiers']['biological_parentage']=True;self.assertFalse(H.valid(a,self.ps))
if __name__=='__main__':unittest.main()
