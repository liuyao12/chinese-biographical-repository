import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import wyd_song045_roles as m
from scripts.fixed_wuyingdian_song045_liucui import validate_source
ROOT=Path(__file__).resolve().parents[1]
class WydSong045Roles(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/m.PATH).read_bytes());cls.c=m.load_contract(ROOT);cls.roles=m.resolve_roles(cls.ch,ROOT);cls.ps={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.chs={cls.ch['id']:cls.ch};cls.a=m.relation_records(cls.ch,ROOT);cls.ns=m.name_records(cls.ch,ROOT)
  cls.all_a=cls.a+json.loads((ROOT/'corpus/songshu/044-wyd1739-direct-brothers-assertions.json').read_bytes())['assertions']
 def test_full_source_old_gate_still_passes(self):
  self.assertTrue(validate_source(self.ch,ROOT));self.assertEqual(len(self.ch['paragraphs']),15);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),2953)
 def test_all_277_mentions_have_exact_source_roles_or_unresolved(self):
  self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),277)
  for p in self.ch['paragraphs']:
   for mark in p['mentions']:self.assertEqual(p['text'][mark['start']:mark['end']],mark['surface'])
 def test_ten_exact_relations_and_directions(self):
  self.assertEqual(len(self.a),10)
  for a in self.a:self.assertTrue(m.relation_valid(a,self.ps,self.chs,ROOT),a['id'])
  for a in self.a:
   bad=copy.deepcopy(a);bad['subject_person_id'],bad['object_person_id']=bad['object_person_id'],bad['subject_person_id'];self.assertFalse(m.relation_valid(bad,self.ps,self.chs,ROOT))
 def test_no_synthetic_parent_global_ordinal_or_common_ancestor(self):
  huai=next(a for a in self.a if a['id'].endswith('huai-father'));self.assertIsNone(huai['qualifiers']['source_birth_position']['absolute_ordinal'])
  for a in self.a:
   if a['predicate']=='agnatic_cousin':self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id']);self.assertIsNone(a['qualifiers']['kinship_structure']['distance'])
  self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==self.roles['liudaoji']for a in self.a))
 def test_impersonation_and_named_lists_are_separate(self):
  self.assertNotEqual(self.roles['real_feilong'],self.roles['chengdaoyang']);self.assertNotEqual(self.roles['simafeiyan'],self.roles['real_feilong']);self.assertNotEqual(self.roles['bashinu'],self.roles['liangxian']);self.assertNotEqual(self.roles['renlangzhi'],self.roles['renhuizhi'])
  p=next(p for p in self.ch['paragraphs']if p['id'].endswith('p008'));marks=[x for x in p['mentions']if x['surface']=='飛龍'];self.assertEqual([x['person_id']for x in marks],[self.roles['real_feilong'],self.roles['real_feilong'],self.roles['chengdaoyang']])
 def test_new_source_roles_cannot_merge_via_same_label(self):
  bad=copy.deepcopy(self.ch);marks=[x for p in bad['paragraphs']for x in p['mentions']if x.get('person_id')==self.roles['liangxian']];marks[0]['person_id']=self.roles['bashinu']
  with self.assertRaises(ValueError):m.source_only_projection(bad,ROOT)
 def test_shifted_text_and_source_role_kind_rejected(self):
  bad=copy.deepcopy(self.ch);p=bad['paragraphs'][0];p['text']='甲'+p['text']
  for x in p['mentions']:x['start']+=1;x['end']+=1
  with self.assertRaises(ValueError):m.source_only_projection(bad,ROOT)
  bad=copy.deepcopy(self.ch);bad['paragraphs'][0]['mentions'][0]['kind']='unresolved';bad['paragraphs'][0]['mentions'][0]['person_id']=None
  with self.assertRaises(ValueError):m.source_only_projection(bad,ROOT)
 def test_two_full_names_and_all_nine_contextual_surnames(self):
  self.assertEqual(len(self.ns),11)
  for n in self.ns:self.assertTrue(m.name_valid(n,self.ns,self.chs,self.all_a,ROOT),n['id'])
  self.assertEqual({n['surname']for n in self.ns},{'劉','程'})
 def test_wrong_surname_missing_seed_or_parent_chain_rejected(self):
  n=copy.deepcopy(self.ns[1]);n['surname']='王';self.assertFalse(m.name_valid(n,self.ns,self.chs,self.all_a,ROOT))
  self.assertFalse(m.name_valid(self.ns[1],self.ns[1:],self.chs,self.all_a,ROOT))
  self.assertFalse(m.name_valid(self.ns[1],self.ns,self.chs,[],ROOT))
 def test_legal_consistent_rekey_and_single_end_drift(self):
  old=self.roles['liudaoji'];new='z8x_9yz_0pq';original=Path.read_bytes
  def remap(x):
   if isinstance(x,dict):return {k:remap(v)for k,v in x.items()}
   if isinstance(x,list):return [remap(v)for v in x]
   if isinstance(x,str):return x.replace(old,new)
   return x
  def read(p):
   b=original(p)
   if p.suffix=='.json'and (p.is_relative_to(ROOT/'corpus')or p==ROOT/'registry/persons.json'):return json.dumps(remap(json.loads(b)),ensure_ascii=False).encode()
   return b
  with patch.object(Path,'read_bytes',read):
   ch=remap(self.ch);self.assertEqual(m.resolve_roles(ch,ROOT)['liudaoji'],new);self.assertIsInstance(m.source_only_projection(ch,ROOT),dict)
  bad=copy.deepcopy(self.ch)
  for p in bad['paragraphs']:
   for x in p['mentions']:
    if x.get('person_id')==old:x['person_id']=new
  with self.assertRaises(ValueError):m.source_only_projection(bad,ROOT)
 def test_malformed_relations_fail_closed(self):
  for value in (None,[],1,'x',{}):self.assertFalse(m.relation_valid(value,self.ps,self.chs,ROOT))
 def test_old_unresolved_and_version_marker_are_not_person(self):
  p=next(p for p in self.ch['paragraphs']if p['id'].endswith('p003'));self.assertTrue(any(x['surface']=='頓謀'and x['kind']=='unresolved'for x in p['mentions']))
  self.assertFalse(any(x.get('person_id')for p in self.ch['paragraphs']for x in p['mentions']if '〓'in x['surface']))
 def test_boolean_ai_flags_are_not_numbers_or_strings(self):
  for v in [0,1,'false',None]:
   ch=copy.deepcopy(self.ch);ch['annotation'][m.KEY]['human_reviewed']=v
   with self.assertRaises(ValueError):m.source_only_projection(ch,ROOT)
   a=copy.deepcopy(self.a[0]);a['human_reviewed']=v;self.assertFalse(m.relation_valid(a,self.ps,self.chs,ROOT))
   n=copy.deepcopy(self.ns[1]);n['surname_basis']['human_reviewed']=v;self.assertFalse(m.name_valid(n,self.ns,self.chs,self.all_a,ROOT))
 def test_impersonation_notes_reach_existing_consumer_field(self):
  notes=[x for p in self.ch['paragraphs']for x in p['mentions']if x.get('resolution_note')and x['kind']=='person']
  self.assertTrue(notes)
  for x in notes:self.assertEqual(x['interpretation_note'],x['resolution_note'])
 def test_shu_eldest_reported_one_is_not_accepted_global_order(self):
  a=next(a for a in self.a if a['id']=='a-song045-wyd-huai-father');b=a['qualifiers']['source_birth_position'];self.assertEqual(b['reported_ordinal'],1);self.assertIs(type(b['reported_ordinal']),int);self.assertEqual(b['source_qualifier'],'庶');self.assertIsNone(b['accepted_birth_order']);self.assertIsNone(b['scope_interpretation'])
  for key,value in [('reported_ordinal',True),('reported_ordinal','1'),('reported_ordinal',0),('reported_ordinal',2),('accepted_birth_order',1),('scope_interpretation','all_children'),('scope_interpretation','shu_children_only'),('source_qualifier','嫡')]:
   bad=copy.deepcopy(a);bad['qualifiers']['source_birth_position'][key]=value;self.assertFalse(m.relation_valid(bad,self.ps,self.chs,ROOT),(key,value))
if __name__=='__main__':unittest.main()
