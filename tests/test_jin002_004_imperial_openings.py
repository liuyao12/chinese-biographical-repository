"""Bounded stage-one current-role source consistency; no registry allocation/rekey."""
import unittest,json,copy
from pathlib import Path
from scripts import jin002_004_imperial_openings as owner
from scripts.person_mentions import pronoun_errors
ROOT=Path(__file__).resolve().parents[1]
class ImperialOpenings(unittest.TestCase):
 def setUp(self):self.changes={}
 def raw(self,p):return self.changes[p]if p in self.changes else(ROOT/p).read_bytes()
 def test_current_source_names_fathers_and_ordinals(self):
  c,r,docs=owner._proof(self.raw);ns=[n for d in docs.values()for n in d.get('records',[])];aa=[a for d in docs.values()for a in d.get('assertions',[])];self.assertEqual([(n['ming'],n['zi'])for n in ns],[('師','子元'),('昭','子上'),('炎','安世'),('衷','正度')]);self.assertEqual([a['qualifiers']['birth_order']['ordinal']for a in aa if a['predicate']=='father'],[1,2]);self.assertFalse(any(a['id'].startswith('a-jinshu038')for a in aa))
 def test_source_first_person_not_aliases(self):
  c,r,docs=owner._proof(self.raw);people={p['id']:p for p in json.loads(self.raw('registry/persons.json'))['persons']}
  for ch in docs.values():
   if ch.get('record_type')!='marked_chapter':continue
   for p in ch['paragraphs']:
    for m in p['mentions']:
     if m['kind']=='pronoun':self.assertEqual(pronoun_errors(m,p['text'],set(people)),[]);self.assertFalse(any(m['id']in a['mention_ids']for a in people[m['person_id']]['aliases']))
 def test_missing_reverse_rejected(self):
  c,r,d=owner._proof(self.raw);people={p['id']:p for p in json.loads(self.raw('registry/persons.json'))['persons']};mid=c['role_current_mids']['yan'][0];people[r['$yan']]['evidence']=[e for e in people[r['$yan']]['evidence']if e.get('mention_id')!=mid]
  with self.assertRaises(AssertionError):owner._proof(self.raw,people)
 def test_wrong_father_or_adoptive_recipient_rejected(self):
  c,r,d=owner._proof(self.raw);path=next(p for p,x in d.items()if x.get('chapter_id')=='c-jinshu-003-wudi-opening'and x.get('record_type')=='person_assertion_set');x=copy.deepcopy(d[path]);x['assertions'][0]['object_person_id']=r['$shi'];self.changes[path]=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
  with self.assertRaises(AssertionError):owner._proof(self.raw)
 def test_raw_and_unknown_metadata_rejected(self):
  c,r,d=owner._proof(self.raw);path=c['chapter_paths'][0];x=copy.deepcopy(d[path]);x['source']['edition']='已核武英殿';self.changes[path]=json.dumps(x,ensure_ascii=False).encode()
  with self.assertRaises(AssertionError):owner._proof(self.raw)
 def test_all_reference_role_rekey_pure_projection(self):
  c,r,d=owner._proof(self.raw);old=r['$yan'];new='aaa_bbb_ccc_TEST';paths=set(c['expected_documents'])|{'registry/persons.json',c['ordinal_report_path']}|{s['path']for s in c['existing_role_seeds'].values()};opaque=[]
  def project(v,key=None):
   if isinstance(v,list):return[project(x,key)for x in v]
   if isinstance(v,dict):return{k:project(x,k)for k,x in v.items()}
   if isinstance(v,str):
    if key in ('mention_id','subject_person_mention_id','object_person_mention_id','id')and v!=old:opaque.append(v)
    return new if v==old else v
   return v
  for p in paths:self.changes[p]=(json.dumps(project(json.loads(self.raw(p))),ensure_ascii=False,indent=2)+'\n').encode()
  cc,rr,dd=owner._proof(self.raw);self.assertEqual(rr['$yan'],new);self.assertTrue(opaque);self.assertTrue(all(old not in x or x!=old for x in opaque))
class MissingContractInstallation(unittest.TestCase):
 def assert_orphan_rejected(self,rel):
  import tempfile
  with tempfile.TemporaryDirectory(prefix='cbr-imperial-missing-contract-')as d:
   root=Path(d);p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}')
   self.assertTrue(owner.errors(root))
   with self.assertRaises(ValueError):owner.guard_bundle(root,'unrelated_current_role',{},[])
   with self.assertRaises(ValueError):owner.ordinal_reports(root,set())
 def test_each_chapter_without_contract_rejected(self):
  for rel in owner.OWNED_PATHS:
   if rel.endswith('.json')and'openings.json'in rel or rel.endswith('-opening.json'):
    with self.subTest(path=rel):self.assert_orphan_rejected(rel)
 def test_source_capsule_without_contract_rejected(self):
  for rel in owner.OWNED_PATHS:
   if rel.startswith('source-evidence/'):
    with self.subTest(path=rel):self.assert_orphan_rejected(rel)
 def test_each_sidecar_or_XML_without_contract_rejected(self):
  for rel in owner.OWNED_PATHS:
   if rel.endswith(('-assertions.json','-name-components.json','.xml')):
    with self.subTest(path=rel):self.assert_orphan_rejected(rel)
 def test_unrelated_base_all_absent_noop(self):
  import tempfile
  with tempfile.TemporaryDirectory(prefix='cbr-imperial-absent-')as d:
   root=Path(d);self.assertEqual(owner.errors(root),[]);self.assertIsNone(owner.guard_bundle(root,'some_existing_person',{},[]));self.assertEqual(owner.ordinal_reports(root,set()),[])

if __name__=='__main__':unittest.main(verbosity=2)
