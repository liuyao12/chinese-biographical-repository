"""Actual selected source inputs, copied to bounded private test roots; no synthetic witness."""
import unittest,tempfile,shutil,json,copy
from pathlib import Path
from scripts import fixed_wyd_sgz015_jia_opening as h
ROOT=Path(__file__).resolve().parents[1]
def enc(x):return(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
class WYDJiaOpening(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name);c=h.contract(ROOT)
  paths=['registry/persons.json',c['seed']['path'],h.CH]+[h.CH.removesuffix('.json')+'-'+k+'.json'for k in c['sidecar_templates']]
  paths += [p.relative_to(ROOT).as_posix()for p in (ROOT/h.BASE).rglob('*')if p.is_file()]
  if h._full_present(ROOT):paths += [p.relative_to(ROOT).as_posix()for p in (ROOT/h.FULL_BASE).rglob('*')if p.is_file()]
  if getattr(h,'_ner_present',lambda root:False)(ROOT):
   n=h._ner_case(ROOT);paths += [h.NER_CASE]+list(n['supporting_reference_files'])+list(n['sidecar_templates'])+[s['path']for s in n['known_seeds'].values()]
  if getattr(h,'_ner_present',lambda root:False)(ROOT):paths += h.caozhang_test_inputs(ROOT)
  for rel in paths:
   src=ROOT/rel;dst=cls.root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
  cls.ch=json.loads((cls.root/h.CH).read_bytes());cls.base=h.state(cls.root)
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def reject_ch(self,f):
  d=copy.deepcopy(self.ch);f(d)
  with self.assertRaises((ValueError,KeyError,StopIteration)):h.state(self.root,d)
 def modify(self,rel,fn,expect=True):
  q=self.root/rel;b=q.read_bytes()
  try:
   q.write_bytes(fn(b))
   if expect:
    with self.assertRaises((ValueError,KeyError,StopIteration)):h.state(self.root)
   else:return h.state(self.root)
  finally:q.write_bytes(b)
 def test_actual_78_and_two_layers(self):
  st=h.state(self.root);self.assertEqual([len(p['text'])for p in st['chapter']['paragraphs'][:2]],[40,38]);self.assertEqual([p['text_layer']for p in self.ch['paragraphs'][:2]],['received_chapter','witness_appended_pei_songzhi_note']);self.assertEqual(len(st['chapter']['paragraphs']),28 if h._full_present(self.root)else 2)
 def test_no_fictitious_father_or_office(self):
  st=h.state(self.root);a=h.sub(st['contract']['sidecar_templates']['assertions'],st['roles'])['assertions'];self.assertEqual(len(a),1);self.assertEqual(a[0]['predicate'],'grandfather');self.assertEqual(a[0]['qualifiers']['generation_distance'],2);self.assertIsNone(a[0]['qualifiers']['parent_person_id']);self.assertEqual(a[0]['qualifiers']['intermediate_person_ids'],[None])
 def test_note_pronouns_and_generic_words(self):
  p=self.ch['paragraphs'][1];self.assertEqual([m['surface']for m in p['mentions'] if m['kind']=='work'],['魏畧']);self.assertFalse(any(m['start']==23 for m in p['mentions']));self.assertFalse(any(m['surface']in('孤','通健','兵法','將率')for p in self.ch['paragraphs'][:2]for m in p['mentions']))
 def test_wrong_subject(self):self.reject_ch(lambda c:c['paragraphs'][0]['mentions'][0].update(person_id=self.base['roles']['xi']))
 def test_note_misclassified_as_body(self):self.reject_ch(lambda c:c['paragraphs'][1].update(text_layer='received_chapter'))
 def test_note_truncation(self):self.reject_ch(lambda c:c['paragraphs'][1].update(text=c['paragraphs'][1]['text'][:-1]))
 def test_wrong_witness(self):self.reject_ch(lambda c:c['source'].update(revision_id='unverified'))
 def test_false_human_review(self):self.reject_ch(lambda c:c['annotation'].update(human_reviewed=True))
 def test_missing_reverse(self):
  def f(b):
   d=json.loads(b);p=next(p for p in d['persons']if p['id']==self.base['roles']['xi']);p['evidence']=[];return enc(d)
  self.modify('registry/persons.json',f)
 def test_wrong_grandfather_direction(self):
  def f(b):
   d=json.loads(b);a=d['assertions'][0];a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];return enc(d)
  self.modify(h.CH.removesuffix('.json')+'-assertions.json',f)
 def test_no_fake_intermediate_father(self):
  def f(b):
   d=json.loads(b);d['assertions'][0]['qualifiers']['parent_person_id']=self.base['roles']['liufu'];return enc(d)
  self.modify(h.CH.removesuffix('.json')+'-assertions.json',f)
 def test_origin_not_inherited(self):
  def f(b):
   d=json.loads(b);d['assertions'][0]['person_id']=self.base['roles']['xi'];return enc(d)
  self.modify(h.CH.removesuffix('.json')+'-addresses.json',f)
 def test_qualified_surname_and_literal_null(self):
  st=self.base;rows=h.sub(st['contract']['sidecar_templates']['names']['records'],st['roles']);a=h.sub(st['contract']['sidecar_templates']['assertions']['assertions'],st['roles']);chapters={h.CID:self.ch};self.assertIsNone(rows[1]['surname']);h.validate_surname(rows[2],rows+[{'ming':'legacy idless'}],chapters,a,self.root)
  for label,ns,ass,cs in [('missing seed',rows[1:],a,chapters),('duplicate seed',rows+[rows[0]],a,chapters),('wrong source',rows,a,{}),('missing ancestor',rows,[],chapters)]:
   with self.subTest(label=label),self.assertRaises(ValueError):h.validate_surname(rows[2],ns,cs,ass,self.root)
 def test_literal_alias_not_fabricated_full_name(self):
  p=self.base['people'][self.base['roles']['xi']];self.assertEqual([a['surface']for a in p['aliases']],['習'])
 def test_complete_consistent_UID_relocation(self):
  old=self.base['roles']['xi'];new='tst_tst_xi0';by=self.base['people'];self.assertNotIn(new,by)
  def project(x):
   if isinstance(x,dict):return{k:project(v)for k,v in x.items()}
   if isinstance(x,list):return[project(v)for v in x]
   return new if x==old else x
  rels=['registry/persons.json',h.CH,h.CH.removesuffix('.json')+'-assertions.json',h.CH.removesuffix('.json')+'-names.json']
  if getattr(h,'_ner_present',lambda root:False)(self.root):
   n=h._ner_case(self.root);rels += list(n['sidecar_templates'])+[s['path']for s in n['known_seeds'].values()]
  rels=list(dict.fromkeys(rels));before={r:(self.root/r).read_bytes()for r in rels}
  try:
   for r,b in before.items():(self.root/r).write_bytes(enc(project(json.loads(b))))
   self.assertEqual(h.state(self.root)['roles']['xi'],new)
  finally:
   for r,b in before.items():(self.root/r).write_bytes(b)
  self.assertEqual(h.state(self.root)['roles']['xi'],old)
