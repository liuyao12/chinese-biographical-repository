"""Actual source closure only; portable copies, no generated corpus or network."""
from pathlib import Path
import unittest,tempfile,json,copy
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class CaoZhangSurname(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts import fixed_wyd_sgz015_jia_opening as h
  cls.h=h;cls.c=h._cao_case(ROOT);cls.current=h.state(ROOT);n=cls.current['ner_contract'];cls.tmp=tempfile.TemporaryDirectory(prefix='sgz015-cao-');cls.root=Path(cls.tmp.name)
  paths={'registry/persons.json',h.CH,h.NER_CASE};paths.update(n['parent_sidecars']);paths.update(n['sidecar_templates']);paths.update(n['supporting_reference_files']);paths.update(s['path']for s in n['known_seeds'].values());paths.update(h.caozhang_test_inputs(ROOT));paths.update(p.relative_to(ROOT).as_posix()for base in(h.BASE,h.FULL_BASE)for p in(ROOT/base).rglob('*')if p.is_file())
  for rel in paths:p=cls.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/rel).read_bytes())
  cls.st=h.state(cls.root);cls.ch=cls.st['chapter'];cls.roles=cls.st['editorial_surname_continuation']['roles']
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def changed(self,rel,fn,*,missing=False):
  p=self.root/rel;b=p.read_bytes()
  try:
   if missing:p.unlink()
   else:p.write_text(json.dumps(fn(json.loads(b)),ensure_ascii=False,indent=2)+'\n')
   with self.assertRaises((ValueError,KeyError,StopIteration,OSError)):self.h.state(self.root)
  finally:p.write_bytes(b)
 def test_actual_root_normal_both_policies(self):
  from scripts.person_bundle import load_catalog,bundle
  people,records=load_catalog(ROOT)
  for policy in(False,True):
   b=bundle(self.current['editorial_surname_continuation']['roles']['child'],root=ROOT,include_provisional=policy,catalog=(people,records));row=next(n for n in b['name_components']if n['id']=='name-sgz015-full-caozhang');self.assertEqual((row['surname'],row['ming'],row['title']),('曹','彰','鄢陵侯'));self.assertEqual(row['surname_basis']['literal_source_components'],{'surname':None,'ming':'彰'})
 def test_reference_three_units_and_unknown_edition(self):
  r=self.h._cao_original_read(self.root,self.c['reference_path']);self.h._cao_reference_valid(r)
  for field,value in(('edition','武英殿'),('human_reviewed',True),('raw_bytes_acquired',True)):
   bad=copy.deepcopy(r);bad[field]=value
   with self.subTest(field=field),self.assertRaises(ValueError):self.h._cao_reference_valid(bad)
  bad=copy.deepcopy(r);bad['units'].pop()
  with self.assertRaises(ValueError):self.h._cao_reference_valid(bad)
 def test_literal_anchor_and_no_restored_raw_alias(self):
  d=self.st['editorial_surname_continuation'];a=d['literal_name'];b=d['current_name'];self.assertEqual(a['surname'],None);self.assertEqual(b['surname'],'曹')
  for k in('id','ming','title','source_anchor','person_mention_id','paragraph_id','quote'):self.assertEqual(a[k],b[k])
  self.assertEqual(b['source_anchor'],{'start':4,'end':5,'surface':'彰'});self.assertFalse(any(a['surface']=='曹彰'for a in self.st['people'][self.roles['child']]['aliases']))
 def test_wrong_name_boundary_only_title_paragraph(self):
  def f(d):
   n=next(n for n in d['records']if n['id']=='name-sgz015-full-caozhang');p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p014'));n.update(paragraph_id=p['id'],quote=p['text'],person_mention_id=p['id']+':m0008',source_anchor={'start':10,'end':11,'surface':'彰'});return d
  self.changed(self.c['names_path'],f)
 def test_parent_name_missing_or_other_person(self):
  def missing(d):d['records']=[n for n in d['records']if n['id']!='name-song051-daogui-literal-caocao'];return d
  self.changed(self.c['parent_name_seed']['path'],missing)
  def wrong(d):next(n for n in d['records']if n['id']=='name-song051-daogui-literal-caocao')['ming']='洪';return d
  self.changed(self.c['parent_name_seed']['path'],wrong)
 def test_parent_reverse_and_source_dimensions(self):
  mid=self.c['parent_name_seed']['marker']['id']
  def reverse(d):p=next(p for p in d['persons']if p['id']==self.roles['father']);p['evidence']=[e for e in p['evidence']if e.get('mention_id')!=mid];return d
  self.changed('registry/persons.json',reverse)
  def source(d):d['source_id']='not-zongshi';return d
  self.changed(self.c['parent_name_seed']['chapter_path'],source)
 def test_required_reference_and_continuation(self):
  self.changed(self.c['reference_path'],lambda x:x,missing=True);self.changed(self.h._CAO_CASE,lambda x:x,missing=True)
 def test_one_end_child_rekey_rejected(self):
  def f(d):next(n for n in d['records']if n['id']=='name-sgz015-full-caozhang')['person_id']=self.roles['father'];return d
  self.changed(self.c['names_path'],f)
 def test_caller_seed_catalog_and_extra_source_record(self):
  from scripts.person_bundle import load_catalog
  people,records=load_catalog(ROOT);seedid=self.c['parent_name_seed']['record']['id'];rows=[r for r in records if not any(n.get('id')==seedid for n in r.get('records',[]))]
  with self.assertRaises(ValueError):self.h.state(ROOT,None,people,rows)
  with self.assertRaises(ValueError):self.h.state(ROOT,None,people,records+[{'record_type':'person_assertion_set','chapter_id':self.h.CID,'assertions':[]}])
 def test_exception_releases_parent_view(self):
  bad=copy.deepcopy(self.ch);bad['paragraphs'][0]['mentions'][0]['start']=1
  with self.assertRaises(ValueError):self.h.state(self.root,bad)
  self.assertIsNone(self.h._cao_view.get());self.assertEqual(self.h.state(self.root)['people'][self.roles['child']]['label'],'曹彰');self.assertEqual(next(n for n in self.h.read(self.root,self.c['names_path'])['records']if n['id']=='name-sgz015-full-caozhang')['surname'],'曹')
 def test_consistent_source_scope_rekey_dynamic_roles(self):
  old=self.roles['child'];new='tst_cao_zha';original=self.h._cao_original_read
  def sub(v):
   if type(v)is dict:return{k:sub(x)for k,x in v.items()}
   if type(v)is list:return[sub(x)for x in v]
   return new if type(v)is str and v==old else v
  with patch.object(self.h,'_cao_original_read',lambda root,rel:sub(original(root,rel))):self.assertEqual(self.h.state(self.root)['editorial_surname_continuation']['roles']['child'],new)
if __name__=='__main__':unittest.main()
