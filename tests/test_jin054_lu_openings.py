"""Fixed three-unit source proof and normal callers; no whole-volume completion claim."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_jin054_lu_openings import proof,errors,guard_bundle,source_reference,name_valid,CH,CID,REF
from scripts.person_bundle import load_catalog,bundle,validate_full_name
from scripts.person_mentions import pronoun_errors
from scripts.source_person_reference_groups import validated_sets,for_people
ROOT=Path(__file__).resolve().parents[1]
class Lu054(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.ch,cls.c,cls.roles=proof(ROOT);cls.people,cls.records=load_catalog(ROOT)
 def overlay(self,changes):
  rb,rt=Path.read_bytes,Path.read_text
  def get(p):return json.dumps(changes[str(p.relative_to(ROOT))],ensure_ascii=False).encode()if p.is_relative_to(ROOT)and str(p.relative_to(ROOT))in changes else None
  from contextlib import ExitStack
  stack=ExitStack();stack.enter_context(patch.object(Path,'read_bytes',lambda p:get(p)if get(p)is not None else rb(p)));stack.enter_context(patch.object(Path,'read_text',lambda p,*a,**k:get(p).decode()if get(p)is not None else rt(p,*a,**k)));return stack
 def mark(self,ch,n,start):return next(m for m in ch['paragraphs'][n-1]['mentions']if m['start']==start)
 def test_01_three_complete_raw_units(self):
  self.assertEqual(len(self.ch['paragraphs']),3);self.assertEqual(self.c['selection'],[[173,340],[3195,3415],[7842,8170]])
  self.assertEqual({k:sum(m['kind']==k for p in self.ch['paragraphs']for m in p['mentions'])for k in['person','pronoun','unresolved']},{'person':60,'pronoun':10,'unresolved':9})
 def test_02_raw_glyphs_not_changed(self):
  self.assertIn('盧廷',self.ch['paragraphs'][1]['text']);self.assertNotIn('盧珽',self.ch['paragraphs'][1]['text']);self.assertIn('縗絰',self.ch['paragraphs'][2]['text']);self.assertIsNone(self.ch['source']['edition']);self.assertFalse(self.ch['source']['image_verified'])
 def test_03_ordinary_words_not_people(self):
  p=self.ch['paragraphs'][2]
  for term in['抗手','張爾弓','青雲','雲龍','白雉','山鹿野麋']:
   a=p['text'].index(term);self.assertFalse(any(m['kind']=='person'and a<=m['start']<a+len(term)for m in p['mentions']))
 def test_04_ten_pronouns_not_namealiases(self):
  for p in self.ch['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='pronoun':self.assertTrue(source_reference(m,p['text']));self.assertEqual(pronoun_errors(m,p['text'],self.people),[]);self.assertFalse(any(m['id']in a['mention_ids']for a in self.people[m['person_id']]['aliases']))
 def test_05_dialogue_recipient_switch(self):
  p=self.ch['paragraphs'][1];self.assertEqual(self.mark(self.ch,2,143)['person_id'],self.roles['$ji']);self.assertEqual(self.mark(self.ch,2,153)['person_id'],self.roles['$luzhi']);self.assertEqual(self.mark(self.ch,2,195)['person_id'],self.roles['$ji'])
 def test_06_wrong_dialogue_recipient_rejected(self):
  ch=copy.deepcopy(self.ch);self.mark(ch,2,153)['person_id']=self.roles['$ji']
  with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_07_unknown_pronoun_shape_rejected(self):
  m=copy.deepcopy(self.mark(self.ch,2,153));m['id']='unowned';self.assertFalse(source_reference(m))
 def test_08_pronoun_alias_rejected(self):
  ps=copy.deepcopy(self.people);m=self.mark(self.ch,2,195);ps[m['person_id']]['aliases'].append({'surface':m['surface'],'mention_ids':[m['id']]})
  with self.assertRaises(AssertionError):proof(ROOT,people=ps)
 def test_09_missing_reverse_rejected(self):
  ps=copy.deepcopy(self.people);pid=self.roles['$ji'];ps[pid]['evidence']=[e for e in ps[pid]['evidence']if e.get('chapter_id')!=CID]
  with self.assertRaises(AssertionError):proof(ROOT,people=ps)
 def test_10_missing_caller_sidecar_rejected(self):
  records=[r for r in self.records if not(r.get('record_type')=='person_assertion_set'and r.get('chapter_id')==CID)]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,self.roles['$ji'],self.people,records)
 def test_11_explicit_father_grandfather_brother_direction(self):
  rel=next(r for r in self.records if r.get('record_type')=='person_assertion_set'and r.get('chapter_id')==CID)['assertions'];self.assertEqual([(x['predicate'],x['subject_person_id'],x['object_person_id'])for x in rel],[('father',self.roles['$ji'],self.roles['$kang']),('grandfather',self.roles['$ji'],self.roles['$luxun']),('brother',self.roles['$ji'],self.roles['$yun'])]);self.assertIsNone(rel[2]['qualifiers']['relative_birth_order']['older_ordinal'])
 def test_12_brother_direction_cannot_be_coherently_flipped(self):
  rel='corpus/jinshu/054-lu-openings-ws2605147-assertions.json';d=json.loads((ROOT/rel).read_bytes());a=d['assertions'][2];a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];a['evidence'][0]['subject_person_mention_id'],a['evidence'][0]['object_person_mention_id']=a['evidence'][0]['object_person_mention_id'],a['evidence'][0]['subject_person_mention_id']
  with self.overlay({rel:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_13_ancestor_not_father(self):
  rel='corpus/jinshu/054-lu-openings-ws2605147-assertions.json';d=json.loads((ROOT/rel).read_bytes());d['assertions'][1]['predicate']='father'
  with self.overlay({rel:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_14_names_fullname_plus_zi_not_ming(self):
  ns=next(r for r in self.records if r.get('record_type')=='person_name_component_set'and r.get('chapter_id')==CID)['records'];self.assertEqual({n['ming']:n.get('zi')for n in ns},{'機':'士衡','雲':'士龍','遜':None,'鴻':None,'隱':'鳴鶴'})
  for n in ns:self.assertTrue(name_valid(n,ROOT));validate_full_name(n,root=ROOT)
 def test_15_wrong_ming_shilong_rejected(self):
  ns=next(r for r in self.records if r.get('record_type')=='person_name_component_set'and r.get('chapter_id')==CID)['records'];n=copy.deepcopy(ns[1]);n['ming']='士龍';self.assertFalse(name_valid(n,ROOT))
 def test_16_luting_raw_variant_is_contextual_luting_identity(self):
  self.assertEqual(self.mark(self.ch,2,158)['person_id'],self.roles['$luting']);d=next(r for r in self.records if r.get('record_type')=='person_identity_decision_set'and r.get('chapter_id')==CID);decision=next(x for x in d['decisions']if x['id']=='d-jin054-luting');self.assertIn('裴注',decision['rationale']);self.assertGreaterEqual(len(decision['evidence']),3)
 def test_17_yanzi_comparison_not_actor_alias(self):
  m=self.mark(self.ch,3,323);self.assertEqual(m['person_id'],self.roles['$yanhui']);self.assertNotEqual(m['person_id'],self.roles['$yun']);self.assertIn('比擬',m['interpretation_note'])
 def test_18_collectives_no_person_and_correct_members(self):
  ds=[r for r in validated_sets(self.records,self.people,ROOT)if r['chapter_id']==CID];self.assertEqual(len(ds),1);self.assertEqual(len(ds[0]['groups']),3);g=ds[0]['groups'][0];self.assertEqual({x['person_id']for x in g['members']},{self.roles['$ji'],self.roles['$yun']});self.assertTrue(all(self.mark(self.ch,2,214)['kind']=='unresolved'for _ in[0]))
 def test_19_current_endpoint_rekey_keeps_raw_and_mids(self):
  old=self.roles['$luxun'];new='zzz_zbc_825';self.assertNotIn(new,self.people)
  def move(x):
   if isinstance(x,str):return new if x==old else x
   if isinstance(x,list):return[move(v)for v in x]
   if isinstance(x,dict):return{k:move(v)for k,v in x.items()}
   return x
  paths=[CH,'registry/persons.json',*self.c['sidecar_templates']];ov={p:move(json.loads((ROOT/p).read_bytes()))for p in paths};capture=(ROOT/REF).read_bytes()
  with self.overlay(ov):ch,c,r=proof(ROOT);self.assertEqual(r['$luxun'],new);self.assertEqual([m['id']for p in ch['paragraphs']for m in p['mentions']],[m['id']for p in self.ch['paragraphs']for m in p['mentions']]);self.assertEqual((ROOT/REF).read_bytes(),capture)
 def test_20_wrong_active_xun_not_nearname_merge(self):
  ch=copy.deepcopy(self.ch);self.mark(ch,1,15)['person_id']='kbq_kjc_n2f_BCE';self.assertIn('kbq_kjc_n2f_BCE',self.people)
  with self.overlay({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_21_progress_and_book_exist_for_reader(self):
  rows=json.loads((ROOT/'corpus/progress.json').read_bytes())['books'];row=[x for x in rows if x['chapter_id']==CID];self.assertEqual(len(row),1);self.assertFalse(row[0]['complete']);self.assertEqual(row[0]['person_status'],'in_progress')
 def test_22_all_sixteen_normal_api(self):
  for role,pid in self.roles.items():
   with self.subTest(role=role):self.assertEqual(bundle(pid,ROOT,catalog=(self.people,self.records))['canonical_person_id'],pid)

 def test_23_inverted_zi_has_real_source_proof(self):
  from scripts.person_bundle import validate_courtesy_name
  n=next(r for r in self.records if r.get('record_type')=='person_name_component_set'and r.get('chapter_id')==CID)['records'][-1]
  self.assertIn('鳴鶴，隱字也',n['quote']);self.assertNotIn('字鳴鶴',n['quote']);validate_courtesy_name(n,root=ROOT)
  bad=copy.deepcopy(n);bad['zi']='士龍'
  with self.assertRaises(ValueError):validate_courtesy_name(bad,root=ROOT)
 def test_24_ancestor_collective_not_reported_count(self):
  doc=next(r for r in self.records if r.get('record_type')=='source_person_reference_group_set'and r.get('chapter_id')==CID);g=doc['groups'][2];self.assertEqual(g['completeness'],'known_subset');self.assertIsNone(g['reported_count']);self.assertTrue(g['unknown_members'])
if __name__=='__main__':unittest.main()
