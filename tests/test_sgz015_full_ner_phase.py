"""Actual full-phase inputs; mutations stay in one bounded private source fixture."""
from pathlib import Path
import json,copy,tempfile,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class FullNER(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts import fixed_wyd_sgz015_jia_opening as h
  cls.h=h;cls.current=h.state(ROOT);cls.c=cls.current['ner_contract'];cls.temp=tempfile.TemporaryDirectory(prefix='cbr-sgz015-ner-');cls.root=Path(cls.temp.name)
  paths={'registry/persons.json',h.CH,h.NER_CASE};paths.update(cls.c['parent_sidecars']);paths.update(cls.c['sidecar_templates']);paths.update(cls.c['supporting_reference_files']);paths.update(s['path']for s in cls.c['known_seeds'].values())
  paths.update(p.relative_to(ROOT).as_posix()for base in(h.BASE,h.FULL_BASE)for p in(ROOT/base).rglob('*')if p.is_file())
  paths.update(h.caozhang_test_inputs(ROOT))
  for rel in paths:f=cls.root/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((ROOT/rel).read_bytes())
  cls.st=h.state(cls.root);cls.ch=cls.st['chapter'];cls.people=cls.st['people'];cls.records=[cls.ch]+[h.read(cls.root,p)for p in cls.c['parent_sidecars']]+[h.read(cls.root,p)for p in cls.c['sidecar_templates']]+[h.read(cls.root,p)for p in sorted(set(s['path']for s in cls.c['known_seeds'].values()))]
  cls.records += h.caozhang_catalog_support(cls.root)
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_actual_root_full_catalog(self):
  from scripts.person_bundle import load_catalog
  people,records=load_catalog(ROOT);self.assertEqual(self.h.source_errors(self.current['chapter'],ROOT),[]);self.h.guard_bundle(ROOT,self.current['roles']['kui'],people,records)
 def test_original_markers_wife_only_promotion(self):
  parent=self.h.sub(self.c['parent_two_paragraphs'],self.st['ner_roles'])
  for a,b in zip(parent,self.ch['paragraphs'][:2]):
   self.assertEqual({k:v for k,v in a.items()if k!='mentions'},{k:v for k,v in b.items()if k!='mentions'})
   for old,new in zip(a['mentions'],b['mentions']):
    if old['surface']=='妻':self.assertEqual([old[k]for k in('id','start','end','surface')],[new[k]for k in('id','start','end','surface')]);self.assertEqual((old['kind'],new['kind']),('unresolved','person'))
    else:self.assertEqual(old,new)
 def test_individuals_not_institutions_or_groups(self):
  self.assertEqual(len(self.st['ner_roles']),45);self.assertNotIn('situ_official',self.st['ner_roles']);self.assertNotIn('household_agent',self.st['ner_roles']);markers=[m for p in self.ch['paragraphs']for m in p['mentions']]
  self.assertEqual(next(m for m in markers if m['surface']=='司徒')['kind'],'unresolved');self.assertEqual(next(m for m in markers if m['surface']=='重者一人')['person_id'],self.st['ner_roles']['heavy_prisoner'])
 def test_literal_names_and_reported_changes(self):
  from scripts.person_bundle import validate_courtesy_name
  docs=[self.h.read(self.root,p)for p in self.c['sidecar_templates']];names=next(x['records']for x in docs if x['record_type']=='person_name_component_set');self.assertEqual(len(names),10)
  for n in names:validate_courtesy_name(n)
  decisions=next(x['decisions']for x in docs if x['record_type']=='person_identity_decision_set');changes=[d['reported_name_change']for d in decisions if 'reported_name_change'in d];self.assertEqual({(x['component'],x['before'],x['after'])for x in changes},{('ming','衢','逵'),('surname','馮','李')});self.assertTrue(all(x['date']is None and not x['birth_name_asserted']for x in changes))
 def test_wrong_keeper_span_and_missing_marker(self):
  for kind in('keeper','span','missing'):
   ch=copy.deepcopy(self.ch)
   if kind=='keeper':next(m for p in ch['paragraphs']for m in p['mentions']if m['person_id']==self.st['ner_roles']['guo_yuan'])['person_id']=self.st['ner_roles']['caopi']
   elif kind=='span':ch['paragraphs'][0]['mentions'][0]['start']=1
   else:ch['paragraphs'][2]['mentions'].pop()
   with self.assertRaises(ValueError):self.h.state(self.root,ch)
 def test_reverse_and_caller_registry_drift(self):
  actual=self.h.read
  def changed(root,rel):
   v=actual(root,rel)
   if rel=='registry/persons.json':
    v=copy.deepcopy(v);p=next(p for p in v['persons']if p['id']==self.st['ner_roles']['lifu']);next(e for e in p['evidence']if e.get('chapter_id')==self.h.CID)['source_id']='wrong'
   return v
  with patch.object(self.h,'read',changed):
   with self.assertRaises(ValueError):self.h.state(self.root)
  wrong=copy.deepcopy(self.people);wrong[self.st['roles']['kui']]['label']='wrong'
  with self.assertRaises(ValueError):self.h.state(self.root,self.ch,wrong,self.records)
 def test_catalog_and_case_boundary(self):
  self.h.guard_bundle(self.root,self.st['roles']['kui'],self.people,self.records)
  bads=[self.records[1:],self.records[:-1],self.records+[{'record_type':'person_assertion_set','chapter_id':self.h.CID,'assertions':[]}]]
  for rows in bads:
   with self.assertRaises(ValueError):self.h.guard_bundle(self.root,self.st['roles']['kui'],self.people,rows)
  ch=copy.deepcopy(self.ch);ch['paragraphs'][2]['annotation_status']='pending'
  with self.assertRaises(ValueError):self.h.state(self.root,ch)
 def test_pronoun_scope_is_not_global_word_exclusion(self):
  self.assertFalse(any(m['surface']=='孤'for p in self.ch['paragraphs'][:2]for m in p['mentions']))
  p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p011'));self.assertTrue(any(m['surface']=='孤'and m.get('person_id')==self.st['ner_roles']['cao_cao']for m in p['mentions']))
 def test_known_source_qualification_not_promoted(self):
  seed=self.c['known_seeds']['cao_cao'];actual=self.h.read
  for field,value in [('human_reviewed',True),('edition','invented-WYD'),('source_id','wrong')]:
   def changed(root,rel):
    v=actual(root,rel)
    if rel==seed['path']:
     v=copy.deepcopy(v)
     if field=='human_reviewed':v.setdefault('annotation',{})[field]=value
     elif field=='edition':v['source'][field]=value
     else:v[field]=value
    return v
   with self.subTest(field=field),patch.object(self.h,'read',changed),self.assertRaises(ValueError):self.h.state(self.root)
 def test_literal_name_anchor_must_be_actual_source_not_only_contract(self):
  rows=next(self.h.read(self.root,path)['records']for path in self.c['sidecar_templates']if self.h.read(self.root,path)['record_type']=='person_name_component_set')
  if 'editorial_surname_continuation'in self.st:
   binding=self.st['editorial_surname_continuation'];self.assertEqual(next(n for n in rows if n['id']=='name-sgz015-full-caozhang')['surname'],'曹');rows=[binding['literal_name']if n['id']=='name-sgz015-full-caozhang'else n for n in rows]
  self.h._ner_literal_names_valid(self.ch,rows)
  row=next(r for r in rows if r['id']=='name-sgz015-full-caozhang');self.assertTrue(row['paragraph_id'].endswith(':p015'));self.assertEqual(row['source_anchor'],{'start':4,'end':5,'surface':'彰'})
  wrong=copy.deepcopy(rows);bad=next(r for r in wrong if r['id']==row['id']);p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p014'));m=next(m for m in p['mentions']if m['surface']=='鄢陵侯');bad.update(paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'],source_anchor={'start':10,'end':11,'surface':'彰'})
  with self.assertRaises(ValueError):self.h._ner_literal_names_valid(self.ch,wrong)
 def test_identity_scope_and_complete_cross_source_evidence(self):
  rows=next(self.h.read(self.root,path)['decisions']for path in self.c['sidecar_templates']if self.h.read(self.root,path)['record_type']=='person_identity_decision_set');self.h._ner_identity_rows_valid(self.ch,self.c,rows,self.st['ner_roles']);self.assertEqual(sum(d['scope']=='same_chapter'for d in rows),18);self.assertEqual(sum(d['scope']=='cross_chapter'for d in rows),27)
  for kind in('scope','missing-foreign','source'):
   wrong=copy.deepcopy(rows)
   if kind=='scope':next(d for d in wrong if d['scope']=='same_chapter')['scope']='within_chapter'
   elif kind=='missing-foreign':next(d for d in wrong if d['scope']=='cross_chapter')['evidence'].pop()
   else:wrong[0]['evidence'][0]['source_id']='wrong'
   with self.subTest(kind=kind),self.assertRaises(ValueError):self.h._ner_identity_rows_valid(self.ch,self.c,wrong,self.st['ner_roles'])
 def test_consistent_role_rekey_no_pid_allowlist(self):
  mapping={pid:'private-rekey-'+role for role,pid in self.st['ner_roles'].items()};actual=getattr(self.h,'_cao_original_read',self.h.read)
  def sub(v):
   if type(v)is dict:return{mapping.get(k,k):sub(x)for k,x in v.items()}
   if type(v)is list:return[sub(x)for x in v]
   return mapping.get(v,v)if type(v)is str else v
  with patch.object(self.h,'_cao_original_read'if hasattr(self.h,'_cao_original_read')else'read',lambda root,rel:sub(actual(root,rel))):self.h.guard_bundle(self.root,mapping[self.st['roles']['kui']],sub(self.people),sub(self.records))
if __name__=='__main__':unittest.main()
