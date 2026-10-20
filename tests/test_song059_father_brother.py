# coding: utf-8
import unittest,json,copy
from pathlib import Path
from scripts.song059_father_brother import explicit_father_elder_brother_valid as valid
class FatherBrotherTests(unittest.TestCase):
 def setUp(self):
  d=json.loads((Path(__file__).parent/'fixtures/song059_father_brother.json').read_text());self.rows=d['assertions'];self.a=self.rows[-1];c=d['chapter'];self.ps={p['id']:(c['id'],p)for p in c['paragraphs']}
 def test_source_positive(self):self.assertTrue(valid(self.a,self.ps,self.rows))
 def test_reverse(self):
  self.a['subject_person_id'],self.a['object_person_id']=self.a['object_person_id'],self.a['subject_person_id'];self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_wrong_age_direction(self):
  b=self.a['qualifiers']['relative_birth_order'];b['older_person_id'],b['younger_person_id']=b['younger_person_id'],b['older_person_id'];self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_invent_rank(self):
  self.a['qualifiers']['relative_birth_order']['older_ordinal']=1;self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_invent_grandfather(self):
  self.a['qualifiers']['grandfather_person_id']='invented';self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_wrong_father_anchor(self):
  e=self.a['evidence'][0];e['subject_person_mention_id']=e['object_person_mention_id'];self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_wrong_child_anchor(self):
  self.a['qualifiers']['source_clause_binding']['child_person_mention_id']=self.a['evidence'][0]['subject_person_mention_id'];self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_wrong_role_offset(self):
  self.a['qualifiers']['source_clause_binding']['father_role_start']+=1;self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_crop_quote(self):
  self.a['evidence'][0]['quote']=self.a['qualifiers']['source_term'];self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_missing_father_assertion(self):self.assertFalse(valid(self.a,self.ps,[self.a]))
 def test_wrong_father_assertion(self):
  self.rows[0]['object_person_id']='other';self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_duplicate_father_assertion(self):self.assertFalse(valid(self.a,self.ps,self.rows+[self.rows[0]]))
 def test_insert_negation(self):
  p=self.ps[self.a['evidence'][0]['paragraph_id']][1];p['text']='非'+p['text'];self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_nested_role(self):
  p=self.ps[self.a['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('兄子也父','從兄子父');self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_other_named_father(self):
  p=self.ps[self.a['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('父褘','父牧');self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_no_person_whitelist(self):
  def change(x):
   if isinstance(x,dict):return{k:change(v)for k,v in x.items()}
   if isinstance(x,(list,tuple)):return[change(v)for v in x]
   return 'new_'+x if isinstance(x,str)and x in {self.a['subject_person_id'],self.a['object_person_id'],self.rows[0]['subject_person_id']}else x
  rows=change(self.rows);ps=change(self.ps);self.assertTrue(valid(rows[-1],ps,rows))

 def test_wrong_contract_kind(self):
  self.a['qualifiers']['source_clause_binding']['kind']='unknown';self.assertFalse(valid(self.a,self.ps,self.rows))
 def test_invent_fixed_ordinal_scope(self):
  self.a['qualifiers']['relative_birth_order']['scope']='children';self.assertFalse(valid(self.a,self.ps,self.rows))
