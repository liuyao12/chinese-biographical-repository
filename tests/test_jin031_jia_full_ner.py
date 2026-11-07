import copy,json,hashlib,tempfile,shutil,unittest
from pathlib import Path
from contextlib import contextmanager
from scripts import fixed_jin031_jia_comparison as core
from scripts import fixed_jin031_jia_full_ner as h
from scripts.fixed_wikisource_units import source_errors
SOURCE=Path(__file__).resolve().parents[1]

class FullNer(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  b=h.fixed(SOURCE);parent=core.fixed(SOURCE)
  rels={core.CH,core.EP,core.NS,core.AD,h.EP,h.IP,h.NSN,'registry/persons.json','data/corpus/chapter-directory.json',b['raw_path'],parent['father_assertion']['native_path'],parent['father_name']['native_path']}
  rels.update(s['native_path']for s in parent['seeds']+b['external_roles'])
  if(SOURCE/'source-evidence/jin031-jia-comparison/typed-phase-proof.json').is_file():
   from scripts.fixed_jin031_jia_typed import fixture_paths
   rels.update(fixture_paths(SOURCE))
  cls.before={rel:hashlib.sha256((SOURCE/rel).read_bytes()).hexdigest()for rel in rels}
  cls.temp=tempfile.TemporaryDirectory(prefix='jin031-full-ner-negative-');cls.addClassCleanup(cls.cleanup);cls.root=Path(cls.temp.name)
  for rel in rels:
   src=SOURCE/rel;dst=cls.root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);assert src.stat().st_ino!=dst.stat().st_ino
  cls.ch=core.read(cls.root,core.CH);cls.roles,cls.proof=h.prepared(cls.ch,cls.root)
 @classmethod
 def cleanup(cls):
  try:
   assert all(hashlib.sha256((SOURCE/rel).read_bytes()).hexdigest()==v for rel,v in cls.before.items()),'negative tests wrote source fixture'
  finally:cls.temp.cleanup()
 @contextmanager
 def changed(self,rel,fn):
  p=self.root/rel;assert p.resolve().is_relative_to(self.root.resolve());before=p.read_bytes()
  try:
   value=json.loads(before);fn(value);p.write_text(json.dumps(value,ensure_ascii=False));yield value
  finally:p.write_bytes(before)
 def test_full_source_entry_and_independent_counts(self):
  self.assertEqual(source_errors(self.ch,self.root),[])
  self.assertEqual([len(p['mentions'])for p in self.ch['paragraphs']],[31,25,20,28 if self.ch['annotation'].get('fixed_jin031_remaining_titles_ref')else 27,22,43,41,13])
  self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),1628)
  self.assertEqual(sum(m['kind'] in ('person','pronoun')for p in self.ch['paragraphs']for m in p['mentions']),205 if self.ch['annotation'].get('fixed_jin031_remaining_titles_ref')else 204)
  self.assertEqual(sum(m['kind']=='unresolved'for p in self.ch['paragraphs']for m in p['mentions']),18)
 def test_old_five_and_two_modern_refs_preserved(self):
  parent=core.expand(core.fixed(self.root)['chapter_template'],self.roles)
  for old,p in zip(parent['paragraphs'],self.ch['paragraphs']):
   self.assertEqual((old['text'],old['source_position'],old['text_layer']),(p['text'],p['source_position'],p['text_layer']))
   for m in old['mentions']:self.assertIn(m,p['mentions'])
  self.assertEqual(parent['annotation']['modern_collation_reports'],self.ch['annotation']['modern_collation_reports'])
 def test_early_and_late_princes_not_same(self):
  self.assertEqual(self.roles['early_prince'],self.roles['huidi']);self.assertNotEqual(self.roles['early_prince'],self.roles['late_prince'])
  for paragraph in [self.ch['paragraphs'][0],self.ch['paragraphs'][1]]:
   self.assertTrue(all(m['person_id']==self.roles['early_prince']for m in paragraph['mentions']if m['surface']=='太子'))
  p=self.ch['paragraphs'][5];self.assertTrue(all(m['person_id']==self.roles['late_prince']for m in p['mentions']if m['surface']=='太子'))
  self.assertIn('侍東宮',p['text']);self.assertFalse(any(m['surface']=='東宮'for m in p['mentions']))
 def test_wrong_prince_and_yao_you_rejected(self):
  for paragraph,surface,wrong in [('p002','太子','late_prince'),('p004','東安公繇','simawei')]:
   def mutate(c):
    p=next(p for p in c['paragraphs']if p['id'].endswith(':'+paragraph));next(m for m in p['mentions']if m['surface']==surface)['person_id']=self.roles[wrong]
   with self.changed(core.CH,mutate)as ch:self.assertTrue(source_errors(ch,self.root))
 def test_clear_linhai_qinghe_same_current_role(self):
  p=self.ch['paragraphs'][7];self.assertEqual({m['person_id']for m in p['mentions']if m['surface']in ['臨海公主','主','之']},{self.roles['daughter_linhai']})
  self.assertNotEqual(self.roles['daughter_hedong'],self.roles['daughter_linhai']);self.assertIn('先封清河',p['text']);self.assertFalse(any(m['surface']=='清河'for m in p['mentions']))
 def test_collective_does_not_allocate_people(self):
  for word in ['三兄','師巫','宮婢','賈郭親黨','外人','答者','作草主']:
   m,=[m for p in self.ch['paragraphs']for m in p['mentions']if m['surface']==word];self.assertEqual((m['kind'],m['person_id']),('unresolved',None))
  def mutate(c):
   next(m for p in c['paragraphs']for m in p['mentions']if m['surface']=='三兄').update(kind='person',person_id=self.roles['dongmeng'])
  with self.changed(core.CH,mutate)as ch:self.assertTrue(source_errors(ch,self.root))
 def test_office_words_and_relation_compounds_not_wrong_person(self):
  for suffix,start,end in [('p001',170,173),('p002',155,159),('p003',114,116),('p008',6,8)]:
   p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':'+suffix));self.assertFalse(any(max(start,m['start'])<min(end,m['end'])for m in p['mentions']))
  p=self.ch['paragraphs'][0];by={m['start']:m for m in p['mentions']};self.assertEqual((by[33]['surface'],by[33]['person_id']),('衛瓘',self.roles['weiguan']));self.assertEqual((by[35]['surface'],by[35]['person_id']),('女',self.roles['weiguan_daughter']));self.assertEqual((by[63]['surface'],by[63]['person_id']),('賈公',self.roles['father']));self.assertEqual((by[65]['kind'],by[65]['person_id']),('unresolved',None))
  for suffix,queen,mother in [('p004',47,49),('p006',80,82)]:
   p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':'+suffix));by={m['start']:m for m in p['mentions']};self.assertEqual(by[queen]['person_id'],self.roles['queen']);self.assertEqual(by[mother]['person_id'],self.roles['guohuai'])
  p=self.ch['paragraphs'][6];by={m['start']:m for m in p['mentions']};self.assertEqual(by[77]['person_id'],self.roles['simajiong']);self.assertEqual(by[78]['person_id'],self.roles['jiong_mother'])
 def test_relation_object_cannot_absorb_named_relative(self):
  def mutate(c):
   p=c['paragraphs'][0];next(m for m in p['mentions']if m['start']==33)['person_id']=self.roles['weiguan_daughter']
  with self.changed(core.CH,mutate)as ch:self.assertTrue(source_errors(ch,self.root))
  def mutate(c):
   p=c['paragraphs'][6];next(m for m in p['mentions']if m['start']==78)['person_id']=self.roles['simajiong']
  with self.changed(core.CH,mutate)as ch:self.assertTrue(source_errors(ch,self.root))
 def test_complete_false_parent_merge_still_rejected(self):
  old=self.roles['jiong_mother'];target=self.roles['simajiong']
  def registry(r):
   by={p['id']:p for p in r['persons']};from_person=by[old];to_person=by[target]
   for e in from_person['evidence']:to_person['evidence'].append(copy.deepcopy(e))
   for a in from_person['aliases']:
    found=next((x for x in to_person['aliases']if x['surface']==a['surface']),None)
    if found is None:to_person['aliases'].append(copy.deepcopy(a))
    else:found['mention_ids'].extend(mid for mid in a['mention_ids']if mid not in found['mention_ids'])
   r['persons']=[p for p in r['persons']if p['id']!=old]
  def chapter(c):
   for p in c['paragraphs']:
    for m in p['mentions']:
     if m.get('person_id')==old:m['person_id']=target
  def identities(d):
   for x in d['decisions']:
    if x['person_id']==old:x['person_id']=target
  with self.changed('registry/persons.json',registry),self.changed(core.CH,chapter),self.changed(h.IP,identities):
   with self.assertRaisesRegex(ValueError,'明親屬'):h.source_context(self.root)
 def test_draft_author_not_an_asserted_single_person(self):
  self.assertNotIn('draft_writer',self.roles)
  for word in ['外人','答者','作草主']:
   m,=[m for m in self.ch['paragraphs'][1]['mentions']if m['surface']==word];self.assertEqual((m['kind'],m['person_id']),('unresolved',None))
 def test_uncertain_chong_daughter_not_forced_to_queen(self):
  case,=self.ch['annotation']['unresolved_identity_cases'];self.assertEqual(set(case['candidate_person_ids']),{self.roles['queen'],self.roles['jiawu']});self.assertTrue(case['unknown_identity_possible']);self.assertFalse(case['candidate_list_exhaustive'])
 def test_foreign_seed_reverse_wrong_dimension_rejected(self):
  seed=self.proof['external_roles'][0]
  for field in ['work_id','source_id']:
   def mutate(r):
    next(e for p in r['persons']for e in p['evidence']if e['mention_id']==seed['mention_id'])[field]='wrong-dimension'
   with self.changed('registry/persons.json',mutate):
    with self.assertRaises(ValueError):h.source_context(self.root)
 def test_wrong_foreign_seed_span_rejected(self):
  seed=self.proof['external_roles'][0]
  def mutate(c):
   p=next(p for p in c['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==seed['mention_id']);m['start']+=1;m['surface']=p['text'][m['start']:m['end']]
  with self.changed(seed['native_path'],mutate):
   with self.assertRaises(ValueError):h.source_context(self.root)
 def test_one_end_source_local_rekey_rejected(self):
  role=self.proof['local_roles'][0]
  def mutate(c):
   p=next(p for p in c['paragraphs']if p['id']==role['paragraph_id']);next(m for m in p['mentions']if m['id']==role['mention_id'])['person_id']=self.roles['father']
  with self.changed(core.CH,mutate)as ch:self.assertTrue(source_errors(ch,self.root))
 def test_ref_and_plain_time_pollution_rejected(self):
  def mutate(c):c['annotation']['modern_collation_reports'][0]['raw_start']+=1
  with self.changed(core.CH,mutate)as ch:self.assertTrue(source_errors(ch,self.root))
  def mutate(c):
   p=c['paragraphs'][4];i=p['text'].index('時他人');p['mentions'].append({'id':p['id']+':fake','start':i,'end':i+1,'surface':'時','kind':'person','person_id':self.roles['queen'],'status':'source_attested'})
  with self.changed(core.CH,mutate)as ch:self.assertTrue(source_errors(ch,self.root))
 def test_caller_catalog_missing_source_or_sidecar_rejected(self):
  people={p['id']:p for p in core.read(self.root,'registry/persons.json')['persons']};records=[core.read(self.root,rel)for rel in [core.CH,core.NS,h.NSN,core.AD,h.IP]]
  if(self.root/'source-evidence/jin031-jia-comparison/typed-phase-proof.json').is_file():
   from scripts.fixed_jin031_jia_typed import proof as typed_proof
   records.extend(core.read(self.root,rel)for rel in typed_proof(self.root)['expected_documents'])
  h.guard_bundle(self.root,self.roles['zhaocan'],people,records)
  for i in range(len(records)):
   with self.assertRaises(ValueError):h.guard_bundle(self.root,self.roles['zhaocan'],people,records[:i]+records[i+1:])
  h.guard_bundle(self.root,'unrelated-existing-person',{},[])
 def test_scope_bounded_and_caller_independent(self):
  from scripts.validation_context import scope
  before=h.source_context(self.root)
  with scope(self.root):
   self.assertEqual(h.source_context(self.root),before);self.assertEqual(set(h.source_context(self.root)[2]),set(self.roles.values()))
   with self.assertRaises(ValueError):h.guard_bundle(self.root,self.roles['queen'],{},[])
 def test_hundred_unrelated_queries_use_only_light_index(self):
  from unittest.mock import patch
  from scripts.validation_context import scope
  people={p['id']:p for p in core.read(self.root,'registry/persons.json')['persons']};others=[pid for pid in people if pid not in set(self.roles.values())][:100];self.assertEqual(len(others),100)
  with scope(self.root),patch.object(h,'read',wraps=h.read)as reads,patch.object(h,'source_context',wraps=h.source_context)as full:
   for pid in others:core.guard_bundle(self.root,pid,{pid:people[pid]},[])
   self.assertEqual(full.call_count,0);self.assertEqual(sum(call.args[1]=='registry/persons.json'for call in reads.call_args_list),1);self.assertEqual(sum(call.args[1]==core.CH for call in reads.call_args_list),1)
   index=h.source_index(self.root);self.assertEqual(set(index['person_ids']),set(self.roles.values()));index['person_ids'].clear();self.assertTrue(h.source_index(self.root)['person_ids'])
   bad=dict(people[others[0]],evidence=[{'chapter_id':core.CID}])
   with self.assertRaises(ValueError):core.guard_bundle(self.root,others[0],{others[0]:bad},[])
 def test_plain_partial_root_unrelated_old_behavior(self):
  with tempfile.TemporaryDirectory(prefix='jin031-no-source-')as name:
   tiny=Path(name);core.guard_bundle(tiny,'unrelated-existing-person',{},[])
   with self.assertRaises(ValueError):core.guard_bundle(tiny,'claimed-source-person',{'claimed-source-person':{'evidence':[{'chapter_id':core.CID}]}},[])
  with tempfile.TemporaryDirectory(prefix='jin031-unrelated-partial-')as name:
   tiny=Path(name);p=tiny/core.CH;p.parent.mkdir(parents=True);p.write_text(json.dumps(self.ch,ensure_ascii=False));core.guard_bundle(tiny,'unrelated-existing-person',{},[])
   with self.assertRaises((OSError,ValueError,KeyError)):core.guard_bundle(tiny,self.roles['queen'],{},[])
 def test_literal_names_and_titles_are_source_bound(self):
  ns=core.read(self.root,h.NSN);self.assertEqual(len(ns['records']),11)
  for n in ns['records']:self.assertTrue(h.name_record_valid(n,self.root))
  all_names=core.read(self.root,core.NS)['records']+ns['records'];self.assertTrue(h.name_record_valid(ns['records'][0],self.root,all_names));self.assertFalse(h.name_record_valid(ns['records'][0],self.root,all_names+[copy.deepcopy(ns['records'][0])]))
  for role in ['daughter_hedong','daughter_linhai','daughter_shiping','daughter_aixian']:
   n,=[n for n in ns['records']if n['person_id']==self.roles[role]];self.assertIsNone(n['surname']);self.assertIsNone(n['ming']);self.assertTrue(n['title'])
  bad=copy.deepcopy(ns['records'][0]);bad['ming']='南風';self.assertFalse(h.name_record_valid(bad,self.root));bad=copy.deepcopy(ns['records'][0]);bad['person_id']=self.roles['father'];self.assertFalse(h.name_record_valid(bad,self.root))
  bad=copy.deepcopy(ns['records'][-1]);bad['ming']=bad['title'];self.assertFalse(h.name_record_valid(bad,self.root))
  with self.changed(h.NSN,lambda d:d['records'][0].update(ming='南風')):self.assertTrue(source_errors(self.ch,self.root))
 def test_unknown_added_markup_not_allowed(self):
  p=self.root/self.proof['raw_path'];before=p.read_bytes()
  try:
   p.write_bytes(before.replace('{{YL|泰始八年}}'.encode(),'{{UNRECOGNIZED|泰始八年}}'.encode(),1));self.assertTrue(source_errors(self.ch,self.root))
  finally:p.write_bytes(before)
if __name__=='__main__':unittest.main(verbosity=2)
