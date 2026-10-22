# coding: utf-8
import unittest,json,copy,hashlib
from pathlib import Path
from scripts.biography_close_family import valid
ROOT=Path(__file__).resolve().parents[1]
class ZuSource(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/nanqishu/052-zuchongzhi.json').read_text());self.rows=json.loads((ROOT/'corpus/nanqishu/052-zuchongzhi-assertions.json').read_text())['assertions'];self.pars={p['id']:(self.ch['id'],p)for p in self.ch['paragraphs']}
 def test_two_roles(self):
  self.assertTrue(all(valid(a,self.pars)for a in self.rows));self.assertEqual([a['predicate']for a in self.rows],['father','grandfather'])
 def test_parent_generation_not_interchangeable(self):
  for a in self.rows:
   b=copy.deepcopy(a);b['predicate']='grandfather'if a['predicate']=='father'else'father';self.assertFalse(valid(b,self.pars))
 def test_reversed_and_hidden_parent_fields(self):
  for a in self.rows:
   b=copy.deepcopy(a);b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id'];b['evidence'][0]['subject_person_mention_id'],b['evidence'][0]['object_person_mention_id']=b['evidence'][0]['object_person_mention_id'],b['evidence'][0]['subject_person_mention_id'];self.assertFalse(valid(b,self.pars))
   for key,value in [('birth_order',1),('biological_mother',True),('parent_person_id','fake')]:
    b=copy.deepcopy(a);b['qualifiers'][key]=value;self.assertFalse(valid(b,self.pars))
 def test_anchor_hash_truncation(self):
  for field,value in [('clause_start',1),('clause_end',20),('paragraph_sha256','0'*64),('revision_id','wrong')]:
   b=copy.deepcopy(self.rows[0]);b['qualifiers']['source_clause_binding'][field]=value;self.assertFalse(valid(b,self.pars))
 def test_consistent_inserted_negation(self):
  a=copy.deepcopy(self.rows[0]);ps=copy.deepcopy(self.pars);_,p=ps[a['evidence'][0]['paragraph_id']];at=p['text'].index('父朔之');p['text']=p['text'][:at]+'非'+p['text'][at:]
  for m in p['mentions']:
   if m['start']>=at:m['start']+=1;m['end']+=1
  a['evidence'][0]['quote']=p['text'];b=a['qualifiers']['source_clause_binding'];b['clause_end']+=1;b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.assertFalse(valid(a,ps))
 def test_style_is_same_person(self):
  a=copy.deepcopy(self.rows[0]);ps=copy.deepcopy(self.pars);p=ps[a['evidence'][0]['paragraph_id']][1];z=next(m for m in p['mentions']if m['surface']=='文逺');z['person_id']='synthetic-other';self.assertFalse(valid(a,ps))
 def test_source_full_math_and_different_dynasties(self):
  t=''.join(p['text']for p in self.ch['paragraphs']);self.assertEqual(len(t),1255);self.assertIn('三百九十一年有一百四十四閏',t);self.assertIn('伐之初即秦厯',t);self.assertIn('綴述',t)
  p=self.pars[self.ch['id']+':p004'][1];s={m['surface']:m.get('person_id')for m in p['mentions']};self.assertNotEqual(s['宋武'],s['太祖']);self.assertNotEqual(s['帝'],s['太祖'])
 def test_ordinary_qian_not_person(self):
  p=self.pars[self.ch['id']+':p003'][1];ms=[m for m in p['mentions']if m['surface']=='遷'];self.assertEqual(len(ms),1);self.assertEqual(p['text'][ms[0]['start']-1:ms[0]['end']],'談遷')
 def test_no_descendants_or_inferred_birth(self):
  self.assertEqual(len(self.rows),2);self.assertNotIn('暅之',''.join(p['text']for p in self.ch['paragraphs']));age=self.ch['annotation']['age_assertions'][0];self.assertEqual(age['value'],72);self.assertIsNone(age['birth_year'])
 def test_source_local_work_qualifications(self):
  works=json.loads((ROOT/'registry/works.json').read_text())['works'];mine=[w for w in works if w['id'].endswith('-nanqi052-reference')];self.assertEqual(len(mine),4);self.assertTrue(all(w['citation_title']and w['citation_qualification']for w in mine))
