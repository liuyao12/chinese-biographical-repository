import unittest,json,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class ZuFamilyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=next(x for x in json.loads((R/'registry/family-assemblies.json').read_text())['assemblies']if x['id']=='family-zu-chang-shuozhi-chongzhi');cls.rows={x['person_id']:x for x in cls.f['members']};cls.m=cls.f['members'][1];cls.c=json.loads((R/'corpus/nanqishu/052-zuchongzhi.json').read_text());cls.a={x['id']:x for x in json.loads((R/'corpus/nanqishu/052-zuchongzhi-assertions.json').read_text())['assertions']};cls.ch={cls.c['id']:cls.c}
 def test_valid_source_roles_and_no_new_father(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  self.assertTrue(valid(self.m,self.rows,self.a,self.ch));self.assertEqual(len(self.a),2);self.assertEqual({x['predicate']for x in self.a.values()},{'father','grandfather'});self.assertIsNone(self.m['source_assertion_id']);self.assertEqual(self.f['root_person_id'],'vcm_d77_tsz')
 def test_surname_at_head_not_grandfather_role(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  a=copy.deepcopy(self.a);m=copy.deepcopy(self.m)
  for x in a.values():x['qualifiers']['source_clause_binding']['roles']['grandfather']=x['qualifiers']['source_clause_binding']['roles']['head']
  m['parent_connection']['source_frame']['source_clause_binding']=copy.deepcopy(next(iter(a.values()))['qualifiers']['source_clause_binding']);self.assertFalse(valid(m,self.rows,a,self.ch))
 def test_wrong_generation_and_contrary_father(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  a=copy.deepcopy(self.a);a['a-nanqi052-zu-grandfather']['predicate']='great_grandfather';self.assertFalse(valid(self.m,self.rows,a,self.ch));a=copy.deepcopy(self.a);a['other']={'predicate':'father','subject_person_id':self.m['person_id'],'object_person_id':'other'};self.assertFalse(valid(self.m,self.rows,a,self.ch))
 def test_maternal_or_missing_role_consistent_source_rejected(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  for old,new in [('也祖昌','也母昌'),('父朔之','母朔之')]:
   a=copy.deepcopy(self.a);m=copy.deepcopy(self.m);ch=copy.deepcopy(self.ch);p=ch[self.c['id']]['paragraphs'][0];p['text']=p['text'].replace(old,new);h=hashlib.sha256(p['text'].encode()).hexdigest();m['parent_connection']['source_frame']['paragraph_sha256']=h;m['parent_connection']['source_frame']['source_clause_binding']['paragraph_sha256']=h
   for x in a.values():x['evidence'][0]['quote']=p['text'];x['qualifiers']['source_clause_binding']['paragraph_sha256']=h
   for e in m['parent_connection']['references']:e['quote']=p['text']
   self.assertFalse(valid(m,self.rows,a,ch))
 def test_full_source_revision_hash_and_span_required(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  for field,value in [('raw_sha256','0'*64),('source_revision','wrong'),('paragraph_sha256','0'*64)]:
   m=copy.deepcopy(self.m);m['parent_connection']['source_frame'][field]=value;self.assertFalse(valid(m,self.rows,self.a,self.ch))
 def test_recipient_not_just_same_paragraph(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  a=copy.deepcopy(self.a);a['a-nanqi052-zu-father']['evidence'][0]['object_person_mention_id']=a['a-nanqi052-zu-father']['evidence'][0]['subject_person_mention_id'];self.assertFalse(valid(self.m,self.rows,a,self.ch))
 def test_generic_ids_and_retirement(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  mapping={x:'synthetic-'+str(n)for n,x in enumerate(self.rows)}
  def remap(v):
   if isinstance(v,str):return mapping.get(v,v)
   if isinstance(v,list):return[remap(x)for x in v]
   if isinstance(v,dict):return{mapping.get(k,k):remap(x)for k,x in v.items()}
   return v
  self.assertTrue(valid(remap(self.m),remap(self.rows),remap(self.a),remap(self.ch)))
  from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
  ret=retired_person_ids(R)
  for x in ['ild_419_r6p','b7o_jjx_4h3']:self.assertIn(x,ret);self.assertTrue(allocation_conflicts(x+'_A',ret))
 def test_death_age_address_and_names_preserved(self):
  c=self.c;age=c['annotation']['age_assertions'][0];self.assertEqual(age['value'],72);self.assertIsNone(age['birth_year']);events=json.loads((R/'corpus/nanqishu/052-zuchongzhi-life-events.json').read_text())['events'];self.assertEqual(events[0]['normalized_date']['year'],500);names=json.loads((R/'corpus/nanqishu/052-zuchongzhi-name-components.json').read_text())['records'];self.assertEqual((names[0]['surname'],names[0]['ming'],names[0]['zi']),('祖','沖之','文逺'))

 def test_consistent_empty_raw_metadata_rejected(self):
  from scripts.unpunctuated_zu_fu_assembly import valid
  m=copy.deepcopy(self.m);ch=copy.deepcopy(self.ch);m['parent_connection']['source_frame']['raw_sha256']='';ch[self.c['id']]['source']['raw_sha256']='';self.assertFalse(valid(m,self.rows,self.a,ch))
