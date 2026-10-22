import unittest,json,copy,hashlib
from pathlib import Path
from scripts.surname_from_father import validate
R=Path(__file__).resolve().parents[1]
class YangchunNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/weishu-weishou/058-yangchun.json').read_text());cls.ch={cls.c['id']:cls.c};cls.a=json.loads((R/'corpus/weishu-weishou/058-yangchun-assertions.json').read_text())['assertions'];cls.ns=json.loads((R/'corpus/weishu-weishou/058-yangchun-name-components.json').read_text())['records'];cls.inferred=[n for n in cls.ns if n.get('surname_basis')];cls.ying=next(n for n in cls.ns if n['ming']=='穎');cls.last=next(n for n in cls.ns if n['ming']=='稚卿')
 def bad(self,n=None,ns=None,a=None,ch=None):
  with self.assertRaises(ValueError):validate(n or self.ying,ns or self.ns,ch or self.ch,a or self.a)
 def test_all_eleven_complete_and_bounded(self):
  self.assertEqual(len(self.ns),11);self.assertEqual(len(self.inferred),9);self.assertTrue(all(n['surname']=='楊'for n in self.ns));self.assertEqual(max(len(n['surname_basis']['steps'])for n in self.inferred),5)
  for n in self.inferred:validate(n,self.ns,self.ch,self.a)
 def test_courtesy_and_original_former_zi(self):
  by={n['ming']:n for n in self.ns};self.assertEqual({x:by[x]['zi']for x in ['椿','昱','穎','順','辯']},{'椿':'延壽','昱':'元晷','穎':'惠哲','順':'延和','辯':'僧達'});self.assertEqual(by['椿']['additional_names'],['本字仲考']);self.assertNotIn('former_ming',by['椿'])
 def test_mother_spouse_uncle_and_unknown_parent_never_used(self):
  aid=self.ying['surname_basis']['steps'][0]['assertion_id']
  for pred in ['mother','spouse','paternal_uncle','kinship_unspecified']:
   a=copy.deepcopy(self.a);next(x for x in a if x['id']==aid)['predicate']=pred;self.bad(a=a)
  n=copy.deepcopy(self.ying);n['surname_basis']['steps'][0]['traversal']='unknown_shared_father';self.bad(n=n)
 def test_adoptive_sworn_maternal_siblings_rejected(self):
  aid=self.ying['surname_basis']['steps'][0]['assertion_id']
  for k,v in [('adoptive',True),('sworn',True),('same_mother_only',True),('shared_father',False),('lineage','maternal')]:
   a=copy.deepcopy(self.a);next(x for x in a if x['id']==aid)['qualifiers'][k]=v;self.bad(a=a)
 def test_brother_cannot_be_fabricated_source_father(self):
  a=copy.deepcopy(self.a);n=copy.deepcopy(self.ying);s=n['surname_basis']['steps'][0];x=next(x for x in a if x['id']==s['assertion_id']);x['predicate']='father';s['traversal']='father_to_child';s['generation_after']=1;self.bad(n=n,a=a)
 def test_generations_and_same_generation_role_checked(self):
  n=copy.deepcopy(self.ying);n['surname_basis']['steps'][0]['generation_after']=1;self.bad(n=n)
  n=copy.deepcopy(self.last);step=next(s for s in n['surname_basis']['steps']if s['traversal']=='father_to_child');step['generation_after']=step['generation_before'];self.bad(n=n)
 def test_cycle_duplicate_assertion_and_sixth_step_rejected(self):
  n=copy.deepcopy(self.ying);s=n['surname_basis']['steps'][0];s['to_person_id']=s['from_person_id'];self.bad(n=n)
  n=copy.deepcopy(self.ying);n['surname_basis']['steps']*=2;self.bad(n=n)
  n=copy.deepcopy(self.last);n['surname_basis']['steps'].append(copy.deepcopy(n['surname_basis']['steps'][-1]));self.bad(n=n)
 def test_wrong_source_and_malformed_scope_rejected(self):
  n=copy.deepcopy(self.ying);n['surname_basis']['steps'][0]['source_frames'][0]['raw_sha256']='0'*64;self.bad(n=n)
  n=copy.deepcopy(self.ying);n['surname_basis']['seed_frame']['source_revision']='wrong';self.bad(n=n)
  a=copy.deepcopy(self.a);aid=self.ying['surname_basis']['steps'][0]['assertion_id'];x=next(x for x in a if x['id']==aid);x['evidence'][0]['source_id']='other-source';n=copy.deepcopy(self.ying);n['surname_basis']['steps'][0]['evidence']=copy.deepcopy(x['evidence']);self.bad(n=n,a=a)
 def test_synthetic_people_not_structural_id_or_label(self):
  ids={m['person_id']for p in self.c['paragraphs']for m in p['mentions']if m['kind']=='person'};mp={x:'fixture-person-'+str(n)for n,x in enumerate(sorted(ids))}
  def change(v):
   if isinstance(v,str):return mp.get(v,v)
   if isinstance(v,list):return[change(x)for x in v]
   if isinstance(v,dict):return{mp.get(k,k):change(x)for k,x in v.items()}
   return v
  for n in self.inferred:validate(change(n),change(self.ns),change(self.ch),change(self.a))
 def test_inferred_seed_and_duplicate_seed_rejected(self):
  ns=copy.deepcopy(self.ns);ns[0]['surname_basis']={'kind':'inferred'};self.bad(ns=ns);self.bad(ns=self.ns+[copy.deepcopy(self.ns[0])])
 def test_target_name_is_source_ming_not_pasted_full_name(self):
  for original in self.inferred:
   n=copy.deepcopy(original);n['ming']='楊'+n['ming'];self.bad(n=n)
 def test_misassigned_adjacent_child_context_rejected(self):
  n=next(n for n in self.ns if n['ming']=='辯');a=copy.deepcopy(self.a);aid=n['surname_basis']['steps'][-1]['assertion_id'];x=next(x for x in a if x['id']==aid);x['context']['paragraph_ids'].reverse();self.bad(n=n,a=a)
 def test_named_brother_role_cannot_turn_into_older_brother_by_word_change(self):
  a=copy.deepcopy(self.a);ch=copy.deepcopy(self.ch);n=copy.deepcopy(self.ying);aid=n['surname_basis']['steps'][0]['assertion_id'];x=next(x for x in a if x['id']==aid);p=next(p for p in ch[self.c['id']]['paragraphs']if p['id']==x['evidence'][0]['paragraph_id']);p['text']=p['text'].replace('椿弟穎','椿兄穎');h=hashlib.sha256(p['text'].encode()).hexdigest();x['evidence'][0]['quote']=p['text'];x['qualifiers']['source_term']='椿兄穎';x['qualifiers']['source_clause_binding']['source_anchor']['surface']='椿兄穎';n['quote']=p['text'];n['surname_basis']['steps'][0]['evidence']=copy.deepcopy(x['evidence']);n['surname_basis']['steps'][0]['source_frames'][0]['paragraph_sha256']=h;self.bad(n=n,a=a,ch=ch)
 def test_consistent_wrong_adjacent_parent_not_merely_same_paragraph(self):
  n=copy.deepcopy(next(n for n in self.ns if n['ming']=='孝邕'));chun=next(n for n in self.ns if n['ming']=='椿');a=copy.deepcopy(self.a);step=n['surname_basis']['steps'][0];x=next(x for x in a if x['id']==step['assertion_id']);p=next(p for p in self.c['paragraphs']if p['id']==x['evidence'][0]['paragraph_id']);wrong=next(m for m in p['mentions']if m.get('kind')=='person'and m['person_id']==chun['person_id']);x['object_person_id']=chun['person_id'];x['evidence'][0]['object_person_mention_id']=wrong['id'];step['from_person_id']=chun['person_id'];step['evidence']=copy.deepcopy(x['evidence']);n['surname_basis'].update(source_name_record_id=chun['id'],source_full_quote=chun['quote']);sp=next(p for p in self.c['paragraphs']if p['id']==chun['paragraph_id']);n['surname_basis']['seed_frame']=dict(paragraph_id=sp['id'],paragraph_sha256=hashlib.sha256(sp['text'].encode()).hexdigest(),source_revision=self.c['source']['revision_id'],raw_sha256=self.c['source']['raw_file_sha256']);self.bad(n=n,a=a)
