"""Actual received-source regressions; negative mutations live solely in memory."""
import unittest,json,copy,hashlib
from pathlib import Path
from scripts.received_genealogy_kinship import valid
from scripts.biography_family_clause import valid as dispatch
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'corpus/xintangshu/071xia-chen-preface.json').read_text());P=C['paragraphs'][0];A=json.loads((R/'corpus/xintangshu/071xia-chen-preface-assertions.json').read_text())['assertions'];D=json.loads((R/'corpus/xintangshu/family-tree-decisions.json').read_text())['decisions']
class ReceivedGenealogy(unittest.TestCase):
 def check_bad(self,a,p=None):
  self.assertFalse(valid(a,{P['id']:(C['id'],p or P)}));self.assertFalse(dispatch(a,{P['id']:(C['id'],p or P)}))
 def test_actual_eleven_position_bound_claims(self):
  self.assertEqual(len(A),11)
  for a in A:self.assertTrue(valid(a,{P['id']:(C['id'],P)}),a['id']);self.assertTrue(dispatch(a,{P['id']:(C['id'],P)}),a['id'])
 def test_archived_raw_and_response_hashes(self):
  e=R/'source-evidence/xintang071xia-chen-preface';m=json.loads((e/'xintang071xia-metadata.json').read_text());self.assertEqual(m['raw_sha256'],hashlib.sha256((e/'xintang071xia.wikitext').read_bytes()).hexdigest());self.assertEqual(m['response_sha256'],hashlib.sha256((e/'xintang071xia-response.json').read_bytes()).hexdigest());self.assertEqual(m['revision_id'],2405769);self.assertIs(m['image_verified'],False)
 def test_whole_received_projection_all_names(self):
  raw=(R/'source-evidence/xintang071xia-chen-preface/xintang071xia.wikitext').read_text();self.assertEqual(P['text'],raw[27860:28269]);self.assertEqual(len(P['text']),409);self.assertEqual(len(P['mentions']),89);self.assertEqual(len({m['person_id']for m in P['mentions']}),55)
  for m in P['mentions']:self.assertEqual(m['surface'],P['text'][m['start']:m['end']])
 def test_each_tang_father_has_explicit_source_choice_no_order_or_mother(self):
  source_ids={a['id']for a in A};selected={d['preferred_assertion_id']for d in D if d['preferred_assertion_id']in source_ids};excluded={i for d in D for i in d['excluded_assertion_ids']};self.assertEqual(source_ids,selected|excluded);self.assertFalse(selected&excluded);self.assertEqual(len(selected),4)
  for a in A:self.assertEqual(set(a['qualifiers']),{'source_term','lineage','source_clause_binding'});self.assertNotIn('adopted_for_family_tree',a)
  self.assertEqual(sum(d['preferred_assertion_id']is not None for d in D),7)
 def test_consistent_wrong_recipient_with_real_other_person(self):
  for a0 in A:
   a=copy.deepcopy(a0);other=next(m for m in P['mentions']if m['person_id']not in[a['subject_person_id'],a['object_person_id']]);a['subject_person_id']=other['person_id'];a['evidence'][0]['subject_person_mention_id']=other['id'];a['qualifiers']['source_clause_binding']['roles']['child']=other['id'];self.check_bad(a)
 def test_consistent_wrong_parent_with_real_other_person(self):
  for a0 in A:
   a=copy.deepcopy(a0);other=next(m for m in P['mentions']if m['person_id']not in[a['subject_person_id'],a['object_person_id']]);a['object_person_id']=other['person_id'];a['evidence'][0]['object_person_mention_id']=other['id'];a['qualifiers']['source_clause_binding']['roles']['parent']=other['id'];self.check_bad(a)
 def test_no_omission_from_complete_sons_list(self):
  a=copy.deepcopy(A[0]);a['qualifiers']['source_clause_binding']['children_mention_ids']=a['qualifiers']['source_clause_binding']['children_mention_ids'][:1];a['qualifiers']['source_clause_binding']['source_count']=1;self.check_bad(a)
 def test_wrong_revision_hash_quote_span(self):
  for field,value in [('revision_id',2405770),('paragraph_sha256','0'*64),('clause_start',204),('clause_end',239),('rule','genealogical_preface_unknown')]:
   a=copy.deepcopy(A[0]);a['qualifiers']['source_clause_binding'][field]=value;self.check_bad(a)
  a=copy.deepcopy(A[0]);a['evidence'][0]['quote']=a['evidence'][0]['quote'][:-1];self.check_bad(a)
  a=copy.deepcopy(A[0]);a['evidence'][0]['relationship_anchor']['start']+=1;self.check_bad(a)
  for rule in [None,1,[]]:
   a=copy.deepcopy(A[0]);a['qualifiers']['source_clause_binding']['rule']=rule;self.check_bad(a)
 def test_no_unstated_order_or_maternity(self):
  for field,value in [('ordinal',1),('same_mother',True),('adopted_for_family_tree',False)]:
   a=copy.deepcopy(A[0]);a['qualifiers'][field]=value;self.check_bad(a)
 def test_not_self_parent_and_no_role_swap(self):
  a=copy.deepcopy(A[0]);a['subject_person_id']=a['object_person_id'];a['evidence'][0]['subject_person_mention_id']=a['evidence'][0]['object_person_mention_id'];a['qualifiers']['source_clause_binding']['roles']['child']=a['evidence'][0]['subject_person_mention_id'];self.check_bad(a)
 def test_received_glyphs_and_unknown_cases(self):
  self.assertIn('厲公他',P['text']);self.assertIn('恒生願',P['text']);self.assertIn('準字道基',P['text']);self.assertNotIn('wikitable',P['text']);self.assertNotIn('cell',P)
  cases=C['annotation']['unresolved_identity_cases'];self.assertEqual(len(cases),3)
  for case in cases:self.assertFalse(case['candidate_list_exhaustive']);self.assertEqual(case['status'],'unresolved');self.assertGreater(len(case['candidate_person_ids']),1)
 def test_synthetic_names_and_ids_no_allowlist(self):
  text='甲字子元。生尚書乙。';ms=[{'id':'parent','start':0,'end':1,'surface':'甲','kind':'person','person_id':'synthetic-parent'},{'id':'zi','start':2,'end':4,'surface':'子元','kind':'person','person_id':'synthetic-parent'},{'id':'child','start':8,'end':9,'surface':'乙','kind':'person','person_id':'synthetic-child'}];p={'id':'synthetic-paragraph','text':text,'text_layer':'received_chapter','source_position':{'revision_id':1},'mentions':ms}
  a=copy.deepcopy(A[6]);a['subject_person_id']='synthetic-child';a['object_person_id']='synthetic-parent';a['evidence'][0].update(chapter_id='synthetic-chapter',paragraph_id=p['id'],quote=text,subject_person_mention_id='child',object_person_mention_id='parent');q=a['qualifiers'];q['source_term']=text;b=q['source_clause_binding'];b.update(rule='genealogical_preface_named_birth_clause',roles={'parent':'parent','child':'child'},clause_start=0,clause_end=len(text),paragraph_sha256=hashlib.sha256(text.encode()).hexdigest(),revision_id=1,children_mention_ids=['child'],source_count=None);a['evidence'][0]['relationship_anchor']={'paragraph_id':p['id'],'start':0,'end':len(text),'surface':text}
  self.assertTrue(valid(a,{p['id']:('synthetic-chapter',p)}));self.assertTrue(dispatch(a,{p['id']:('synthetic-chapter',p)}))
 def test_not_earliest_catalog_or_digital_date(self):
  m=json.loads((R/'registry/work-provenance.json').read_text());w=m['works']['w-xintangshu'];self.assertEqual(w['earliest_extant_edition'],{'status':'unknown','assertions':[]});s=m['text_bases'][C['source_id']];self.assertIsNone(s['edition_id']);self.assertIsNone(s['earliest_extant_basis_edition_id'])
if __name__=='__main__':unittest.main()
