import ast,copy,hashlib,json,unittest
from pathlib import Path
from scripts.collateral_kinship import agnatic_senior_kin_valid
ROOT=Path(__file__).resolve().parents[1]

class BiographicalSeniorCollateralTests(unittest.TestCase):
 def setUp(self):
  self.examples=json.loads((ROOT/'tests/fixtures/biographical-senior-collateral/received-examples.json').read_text())
 def pair(self,n=0):
  x=copy.deepcopy(self.examples[n]);c=x['chapter'];return x['assertion'],{p['id']:(c['id'],p)for p in c['paragraphs']}
 def p(self,a,ps):return ps[a['evidence'][0]['paragraph_id']][1]
 def seal(self,a,ps):
  p=self.p(a,ps);a['evidence'][0]['quote']=p['text'];a['qualifiers']['source_clause_binding']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
 def test_both_complete_received_paragraphs(self):
  for n in (0,1):
   a,ps=self.pair(n);self.assertTrue(agnatic_senior_kin_valid(a,ps))
 def test_reverse_direction_rejected(self):
  a,ps=self.pair();a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_wrong_endpoint_with_same_surface_rejected(self):
  a,ps=self.pair();a['subject_person_id']='another';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_foreign_mid_rejected(self):
  a,ps=self.pair();a['evidence'][0]['subject_person_mention_id']='other-chapter:m1';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_wrong_chapter_rejected(self):
  a,ps=self.pair();a['evidence'][0]['chapter_id']='other';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_whole_paragraph_quote_required(self):
  a,ps=self.pair();a['evidence'][0]['quote']=a['evidence'][0]['quote'].split('。')[0]+'。';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_full_text_hash_required(self):
  a,ps=self.pair();self.p(a,ps)['text']+='。';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_received_layer_required(self):
  a,ps=self.pair();self.p(a,ps)['text_layer']='modern_note';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_only_two_explicit_terms_supported(self):
  a,ps=self.pair();a['qualifiers']['source_term']='族父';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_term_span_cannot_borrow_another_position(self):
  a,ps=self.pair();a['qualifiers']['source_clause_binding']['relationship_span']['start']-=1;self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_senior_must_be_biographical_head(self):
  a,ps=self.pair(1);b=a['qualifiers']['source_clause_binding'];b['head_person_mention_id']=b['courtesy_name_mention_id'];self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_courtesy_must_be_same_person(self):
  a,ps=self.pair(1);b=a['qualifiers']['source_clause_binding'];m=next(m for m in self.p(a,ps)['mentions']if m['id']==b['courtesy_name_mention_id']);m['person_id']='wrong';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_parentage_roles_cannot_swap(self):
  a,ps=self.pair(1);b=a['qualifiers']['source_clause_binding']['parentage_clause'];b['older_person_mention_id'],b['father_person_mention_id']=b['father_person_mention_id'],b['older_person_mention_id'];self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_undeclared_person_in_opening_rejected(self):
  a,ps=self.pair();p=self.p(a,ps);p['mentions'].append(dict(id='extra',start=10,end=11,surface=p['text'][10:11],kind='person',person_id='other'));self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_unresolved_opening_role_is_not_ignored(self):
  a,ps=self.pair();p=self.p(a,ps);p['mentions'].append(dict(id='extra',start=10,end=11,surface=p['text'][10:11],kind='unresolved',person_id=None));self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_later_paragraph_people_allowed(self):
  a,ps=self.pair(1);self.assertGreater(len(self.p(a,ps)['mentions']),10);self.assertTrue(agnatic_senior_kin_valid(a,ps))
 def test_unknown_distance_ancestor_and_age_cannot_be_invented(self):
  for k,v in [('lineage','maternal'),('generation_difference',0),('generation_difference',True),('collateral',1),('distance',2),('common_ancestor_person_id','someone'),('subject_relative_age','younger')]:
   a,ps=self.pair();a['qualifiers']['kinship_structure'][k]=v;self.assertFalse(agnatic_senior_kin_valid(a,ps),(k,v))
 def test_reviewed_and_integer_reviewed_rejected(self):
  for v in (True,0):
   a,ps=self.pair();a['human_reviewed']=v;self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_bool_position_rejected(self):
  a,ps=self.pair();self.p(a,ps)['mentions'][0]['start']=False;self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_duplicate_mid_rejected(self):
  a,ps=self.pair();p=self.p(a,ps);p['mentions'].append(copy.deepcopy(p['mentions'][0]));self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_coherent_rekey_retains_all_opaque_ids_and_raw(self):
  a,ps=self.pair(1);p=self.p(a,ps);before=(a['id'],p['text'],[m['id']for m in p['mentions']]);mapping={a['subject_person_id']:'junior_current',a['object_person_id']:'senior_current'}
  for k in ('subject_person_id','object_person_id'):a[k]=mapping[a[k]]
  for m in p['mentions']:m['person_id']=mapping.get(m.get('person_id'),m.get('person_id'))
  self.assertTrue(agnatic_senior_kin_valid(a,ps));self.assertEqual(before,(a['id'],p['text'],[m['id']for m in p['mentions']]))
 def test_non_target_malformed_model_does_not_fall_into_new_rule(self):
  a,ps=self.pair();a['qualifiers']['source_clause_binding']['kind']='unsupported';self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_source_edition_and_global_reverse_are_upstream_boundary(self):
  # These values cannot be certified by the paragraph-only helper. The normal
  # validator must still check chapter acquisition and registry reciprocity.
  a,ps=self.pair();a['evidence'][0]['source_id']='not-visible-in-paragraphs';self.assertTrue(agnatic_senior_kin_valid(a,ps))

 def test_wrong_parentage_word_rejected_after_fresh_hash(self):
  a,ps=self.pair(1);p=self.p(a,ps);p['text']=p['text'].replace('朗弟允','朗兄允',1);self.seal(a,ps);self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_unclosed_quotation_not_accepted_as_biographical_head(self):
  a,ps=self.pair(1);p=self.p(a,ps);p['text']='「'+p['text']
  for m in p['mentions']:m['start']+=1;m['end']+=1
  head=p['mentions'][0];head['start']=0;head['surface']='「'+head['surface']
  r=a['qualifiers']['source_clause_binding']['relationship_span'];r['start']+=1;r['end']+=1
  self.seal(a,ps);self.assertFalse(agnatic_senior_kin_valid(a,ps))
 def test_negated_relation_rejected_after_fresh_spans_and_hash(self):
  a,ps=self.pair();p=self.p(a,ps);b=a['qualifiers']['source_clause_binding'];i=b['relationship_span']['start'];p['text']=p['text'][:i]+'非'+p['text'][i:]
  for m in p['mentions']:
   if m['start']>=i:m['start']+=1;m['end']+=1
  b['relationship_span']['start']+=1;b['relationship_span']['end']+=1
  self.seal(a,ps);self.assertFalse(agnatic_senior_kin_valid(a,ps))

if __name__=='__main__':unittest.main(verbosity=2)
