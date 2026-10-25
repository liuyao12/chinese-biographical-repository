from pathlib import Path
import unittest,json,copy
R=Path(__file__).resolve().parents[1]
class PeiweiFactsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts.fixed_witness_fact_slots import records
  cls.ch=json.loads((R/'corpus/jinshu/035-peiwei.json').read_bytes());cls.rs=records(cls.ch,R);cls.v={r['fixed_source_fact_binding']['slot']:r for r in cls.rs};cls.paras={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.assertions=[r for r in cls.rs if 'predicate'in r]
 def reject(self,v):
  from scripts.fixed_witness_fact_slots import valid
  self.assertFalse(valid(v,self.ch,R))
 def test_complete_layers_and_source_slot_count(self):
  self.assertEqual(len(self.ch['paragraphs']),15);self.assertEqual(len(self.rs),70);self.assertEqual(self.v['biancai-unfinished']['person_id'],self.v['wei-father']['subject_person_id']);self.assertEqual(self.v['biancai-unfinished']['source_anchor']['paragraph_id'],self.ch['paragraphs'][13]['id']);self.assertEqual(self.v['biancai-unfinished']['evidence'][-1]['quote'],self.ch['paragraphs'][13]['text'])
  for p in self.ch['paragraphs'][8:13]:self.assertEqual(p['source_position']['source_layer'],'received_quoted_document')
 def test_mother_is_birth_mother_not_jia_empress(self):
  v=self.v['prince-birth-mother'];p=self.ch['paragraphs'][3];ms={m['surface']:m for m in p['mentions']if m['kind']=='person'};self.assertEqual((v['subject_person_id'],v['object_person_id']),(ms['太子']['person_id'],ms['謝淑妃']['person_id']));self.assertNotEqual(v['object_person_id'],ms['賈后']['person_id']);bad=copy.deepcopy(v);bad['object_person_id']=ms['賈后']['person_id'];self.reject(bad)
 def test_second_son_is_sons_scope_only_not_oldest_son_inference(self):
  v=self.v['gai-birth-order'];q=v['qualifiers']['birth_order'];self.assertEqual((q['ordinal'],q['scope']),(2,'sons_of_parent'));self.assertNotIn('birth_order',self.v['song-father']['qualifiers']);bad=copy.deepcopy(v);bad['qualifiers']['birth_order']['ordinal']=1;self.reject(bad)
 def test_wuchang_actual_grantee_not_proposed_wei_or_jing(self):
  h=self.v['gai-wuchang'];self.assertEqual(h['person_id'],self.v['gai-father']['subject_person_id']);self.assertEqual(h['title'],'武昌侯');self.assertFalse(self.v['jing-julu-request']['values']['grant_attested']);self.assertFalse(self.v['deposition-plan']['values']['xie_enthroned']);bad=copy.deepcopy(h);bad['person_id']=self.v['wei-father']['subject_person_id'];self.reject(bad)
 def test_only_direct_taikang_appointment_gets_281(self):
  dated=[]
  for slot,v in self.v.items():
   def walk(x):
    if isinstance(x,dict):
     for k,z in x.items():
      if k=='normalized_date':dated.append((slot,z['year']))
      else:walk(z)
    elif isinstance(x,list):
     for z in x:walk(z)
   walk(v)
  self.assertEqual(dated,[('wei-01',281),('wei-01',281)]);self.assertIsNone(self.v['wei-02']['effective_period']['start']['date_expression']);bad=copy.deepcopy(self.v['wei-02']);bad['effective_period']['start']['normalized_date']={'year':281};self.reject(bad)
 def test_age_and_deaths_unknown_years_and_no_derived_birth(self):
  age=self.v['wei-age-34'];self.assertEqual(age['value'],34);self.assertEqual(age['counting'],'unspecified_source_age');self.assertIsNone(age['birth_year'])
  for s in ['wei-death','song-death','gai-death','jiamo-death']:self.assertIsNone(self.v[s]['date_expression']);self.assertNotIn('normalized_date',self.v[s])
  bad=copy.deepcopy(age);bad['birth_year']=267;self.reject(bad)
 def test_relocation_is_two_sons_not_fathers_native_place(self):
  v=self.v['sons-relocated']['values'];self.assertEqual(v['place_source_name'],'帶方');self.assertFalse(v['native_place_inference']);self.assertIsNone(self.v['reburial']['values']['burial_place']);self.assertIsNone(self.v['restored-office']['values']['office_title'])
 def test_adoption_preserves_biological_father_and_independent_kai(self):
  from scripts.chuji_parentage import chuji_parentage_valid
  a=self.v['gai-adoptive-father'];f=self.v['gai-father'];self.assertTrue(chuji_parentage_valid(a,self.paras,self.assertions));self.assertEqual(a['subject_person_id'],f['subject_person_id']);self.assertNotEqual(a['object_person_id'],f['object_person_id']);self.assertIsNone(a['qualifiers']['common_ancestor_person_id']);self.assertEqual(a['qualifiers']['actual_upbringing'],'not_inferred')
 def test_adoption_wrong_person_direction_kind_father_and_distance_rejected(self):
  from scripts.chuji_parentage import chuji_parentage_valid as valid
  a=self.v['gai-adoptive-father']
  for key,value in [('subject_person_id',a['object_person_id']),('object_person_id',self.v['gai-father']['object_person_id'])]:
   bad=copy.deepcopy(a);bad[key]=value;self.assertFalse(valid(bad,self.paras,self.assertions))
  for key,value in [('adoption_basis','chuji_named_paternal_uncle'),('source_term','該後從伯凱'),('collateral_source_term','伯父'),('exact_distance',3),('modern_legal_status','legal_adoption')]:
   bad=copy.deepcopy(a);bad['qualifiers'][key]=value;self.assertFalse(valid(bad,self.paras,self.assertions))
  for role in ['child','adopter','biological_child','biological_father']:
   ps=copy.deepcopy(self.paras);p=ps[a['evidence'][0]['paragraph_id']][1];m=next(m for m in p['mentions']if m['id']==a['qualifiers']['source_clause_binding']['roles'][role]);m['kind']='unresolved';self.assertFalse(valid(a,ps,self.assertions))
  rows=copy.deepcopy(self.assertions);next(x for x in rows if x['id']==a['qualifiers']['biological_father_assertion_id'])['object_person_id']=a['object_person_id'];self.assertFalse(valid(a,self.paras,rows))
 def test_adoption_shared_span_and_text_mutation_rejected(self):
  from scripts.chuji_parentage import chuji_parentage_valid as valid
  a=self.v['gai-adoptive-father']
  for altered in ['該後從伯凱','該出後伯父凱','該非出後從伯凱']:
   bad=copy.deepcopy(a);ps=copy.deepcopy(self.paras);p=ps[a['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('該出後從伯凱',altered);bad['evidence'][0]['quote']=p['text'];bad['qualifiers']['source_clause_binding']['paragraph_sha256']=__import__('hashlib').sha256(p['text'].encode()).hexdigest();self.assertFalse(valid(bad,ps,self.assertions))
  bad=copy.deepcopy(a);ps=copy.deepcopy(self.paras);p=ps[a['evidence'][0]['paragraph_id']][1]
  for role in ['child','adopter']:
   m=next(m for m in p['mentions']if m['id']==bad['qualifiers']['source_clause_binding']['roles'][role]);m['start']+=1;m['end']+=1
  bad['qualifiers']['source_clause_binding']['clause_anchor']['start']+=1;bad['qualifiers']['source_clause_binding']['clause_anchor']['end']+=1;self.assertFalse(valid(bad,ps,self.assertions))
 def test_coherent_rekey_keeps_adoption_valid_without_pid_whitelist(self):
  from scripts.chuji_parentage import chuji_parentage_valid as valid
  a=copy.deepcopy(self.v['gai-adoptive-father']);ps=copy.deepcopy(self.paras);rows=copy.deepcopy(self.assertions);ids={v:'fresh_%d'%i for i,v in enumerate({a['subject_person_id'],a['object_person_id'],self.v['gai-father']['object_person_id']})}
  def repl(v):
   if isinstance(v,dict):return{k:repl(x)for k,x in v.items()}
   if isinstance(v,list):return[repl(x)for x in v]
   if isinstance(v,tuple):return tuple(repl(x)for x in v)
   return ids.get(v,v)if isinstance(v,str)else v
  self.assertTrue(valid(repl(a),repl(ps),repl(rows)))
if __name__=='__main__':unittest.main()
