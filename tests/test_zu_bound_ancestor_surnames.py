import unittest,json,copy
from pathlib import Path
from scripts.surname_from_father import validate
R=Path(__file__).resolve().parents[1]
class ZuSurnameTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/nanqishu/052-zuchongzhi.json').read_text());cls.ch={cls.c['id']:cls.c};cls.a=json.loads((R/'corpus/nanqishu/052-zuchongzhi-assertions.json').read_text())['assertions'];cls.ns=json.loads((R/'corpus/nanqishu/052-zuchongzhi-name-components.json').read_text())['records'];cls.new=[x for x in cls.ns if x.get('surname_basis')];cls.seed=next(x for x in cls.ns if not x.get('surname_basis'))
 def bad(self,n=None,ns=None,a=None,ch=None):
  with self.assertRaises(ValueError):validate(n or self.new[0],ns or self.ns,ch or self.ch,a or self.a)
 def test_both_source_roles_valid(self):
  self.assertEqual(len(self.new),2)
  for n in self.new:validate(n,self.ns,self.ch,self.a);self.assertEqual(n['quote'],self.c['paragraphs'][0]['text']);self.assertEqual(n['surname'],'祖');m=next(m for m in self.c['paragraphs'][0]['mentions']if m['id']==n['person_mention_id']);self.assertEqual(m['surface'],n['ming']);self.assertNotEqual(m['surface'],n['surname']+n['ming'])
 def test_maternal_adoptive_uncle_unknown_generation_rejected(self):
  for field,value in [('lineage','maternal'),('adoptive',True)]:
   a=copy.deepcopy(self.a);a[0]['qualifiers'][field]=value;self.bad(a=a)
  for pred in ['paternal_uncle','ancestor','adoptive_father']:
   a=copy.deepcopy(self.a);a[0]['predicate']=pred;n=copy.deepcopy(self.new[0]);n['surname_basis']['source_role']=pred;self.bad(n=n,a=a)
  n=copy.deepcopy(self.new[0]);n['surname_basis']['generation_distance']=2;self.bad(n=n)
 def test_editorial_assembly_is_not_source_father(self):
  n=copy.deepcopy(self.new[1]);a=copy.deepcopy(self.a);x=copy.deepcopy(a[1]);x['id']='synthetic-editorial';x['status']='contextual_provisional';x['predicate']='father';a.append(x);n['surname_basis'].update(assertion_id=x['id'],source_role='father',generation_distance=1);self.bad(n=n,a=a)
  x['status']='source_attested';self.bad(n=n,a=a)
 def test_wrong_recipient_same_paragraph_and_surname_head(self):
  a=copy.deepcopy(self.a);a[0]['evidence'][0]['object_person_mention_id']=a[0]['evidence'][0]['subject_person_mention_id'];n=copy.deepcopy(self.new[0]);n['surname_basis']['evidence']=copy.deepcopy(a[0]['evidence'][0]);self.bad(n=n,a=a)
  n=copy.deepcopy(self.new[1]);n['person_mention_id']=self.seed['person_mention_id'];self.bad(n=n)
 def test_bad_source_metadata_or_missing_full_quote(self):
  for k,v in [('raw_sha256',''),('source_revision','wrong'),('paragraph_sha256','0'*64)]:
   n=copy.deepcopy(self.new[0]);n['surname_basis']['source_frame'][k]=v;self.bad(n=n)
  n=copy.deepcopy(self.new[0]);n['quote']='父朔之';self.bad(n=n)
 def test_inferred_or_other_chapter_seed_not_allowed(self):
  ns=copy.deepcopy(self.ns);ns[0]['surname_basis']={'kind':'inferred'};self.bad(ns=ns)
  ns=copy.deepcopy(self.ns);ns[0]['chapter_id']='other-chapter';self.bad(ns=ns)
 def test_duplicate_seed_and_nonexact_ming_rejected(self):
  self.bad(ns=self.ns+[copy.deepcopy(self.seed)]);n=copy.deepcopy(self.new[0]);n['ming']='祖'+n['ming'];self.bad(n=n)
 def test_generic_person_ids_not_family_prefix_inference(self):
  ids={m['person_id']for p in self.c['paragraphs']for m in p['mentions']if m['kind']=='person'};mapping={x:'synthetic-person-'+str(n)for n,x in enumerate(sorted(ids))}
  def remap(v):
   if isinstance(v,str):return mapping.get(v,v)
   if isinstance(v,list):return[remap(x)for x in v]
   if isinstance(v,dict):return{mapping.get(k,k):remap(x)for k,x in v.items()}
   return v
  for n in self.new:validate(remap(n),remap(self.ns),remap(self.ch),remap(self.a))
 def test_actual_bundle_has_readable_names_not_label_patch(self):
  from scripts.person_bundle import bundle,load_catalog
  cat=load_catalog(R)
  for n in self.new:
   b=bundle(n['person_id'],root=R,catalog=cat);self.assertEqual([(x['surname'],x['ming'])for x in b['name_components']],[(n['surname'],n['ming'])]);self.assertEqual(b['name_components'][0]['surname_basis']['generation_distance'],n['surname_basis']['generation_distance'])
 def test_old_father_chain_contract_still_father_only(self):
  from scripts.surname_family_chain import validate as old_validate
  n=copy.deepcopy(self.new[1]);n['surname_basis']['kind']='contextual_surname_from_same_source_father_chain'
  with self.assertRaises(ValueError):old_validate(n,self.ns,self.ch,self.a)
