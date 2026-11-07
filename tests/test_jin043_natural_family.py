import unittest,json,copy,sys,os,tempfile,shutil,hashlib
from pathlib import Path
F=Path(os.environ.get('CBR_TEST_ROOT',Path(__file__).resolve().parents[1]));sys.path.insert(0,str(F))
from scripts.biographical_kinship import natural_parentage_errors
from scripts.biography_family_clause import valid
from scripts.surname_family_chain import validate_cross_chapter
class Guards(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.ch=json.loads((F/'corpus/jinshu/043-wangyan.json').read_text());c.aa=json.loads((F/'corpus/jinshu/043-wangyan-family-assertions.json').read_text())['assertions']
 def test_two_source_roles(self):
  for a in self.aa:self.assertEqual(natural_parentage_errors(a,self.ch,F),[])
  self.assertTrue(valid(self.aa[0],{},self.aa,{self.ch['id']:self.ch},F))
 def test_wrong_endpoint(self):
  for a in self.aa:
   n=copy.deepcopy(a);n['subject_person_id'],n['object_person_id']=n['object_person_id'],n['subject_person_id'];self.assertTrue(natural_parentage_errors(n,self.ch,F))
 def test_other_topic(self):
  c=copy.deepcopy(self.ch);c['paragraphs'][8]['mentions'][0]['person_id']='other'
  self.assertTrue(natural_parentage_errors(self.aa[1],c,F))
 def test_raw_shift_not_reinterpreted(self):
  c=copy.deepcopy(self.ch);c['paragraphs'][9]['text']='曰'+c['paragraphs'][9]['text']
  for m in c['paragraphs'][9]['mentions']:m['start']+=1;m['end']+=1
  self.assertTrue(natural_parentage_errors(self.aa[1],c,F))
 def test_wrong_kind_and_context(self):
  for val in [None,[],{},'x']:
   self.assertTrue(natural_parentage_errors(val,self.ch,F))
  n=copy.deepcopy(self.aa[1]);n['qualifiers']['lineage']='maternal';self.assertTrue(natural_parentage_errors(n,self.ch,F))
 def test_fullname_seed_path(self):
  names=json.loads((F/'data/corpus/profile-names.json').read_text())['records'];names+=json.loads((F/'corpus/jinshu/043-wangyan-family-names.json').read_text())['records'];cs={self.ch['id']:self.ch};sc=json.loads((F/'corpus/jinshu/090-caoshu.json').read_text());cs[sc['id']]=sc
  for n in names:
   if n.get('surname_basis',{}).get('kind')=='contextual_surname_from_cross_chapter_same_canonical_family_path':
    validate_cross_chapter(n,names,cs,self.aa,F)
    bad=copy.deepcopy(n);bad['surname']='張'
    with self.assertRaises(ValueError):validate_cross_chapter(bad,names,cs,self.aa,F)
 def test_consistent_rekey_and_single_endpoint_reject(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);contract=json.loads((F/'source-evidence/jin043-wangyan-family/fixed-natural-units.json').read_text())
   for rel in ['source-evidence/jin043-wangyan-family/fixed-natural-units.json',contract['raw_file'],'registry/persons.json']:
    dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(F/rel,dest)
   c=copy.deepcopy(self.ch);aa=copy.deepcopy(self.aa);reg=json.loads((root/'registry/persons.json').read_text())
   old=aa[0]['subject_person_id'];new='abc_def_123'
   def replace(x):
    if isinstance(x,dict):return {k:replace(v)for k,v in x.items()}
    if isinstance(x,list):return [replace(v)for v in x]
    return new if x==old else x
   c=replace(c);aa=replace(aa);reg=replace(reg);(root/'registry/persons.json').write_text(json.dumps(reg))
   for a in aa:self.assertEqual(natural_parentage_errors(a,c,root),[])
   aa[0]['subject_person_id']=old;self.assertTrue(natural_parentage_errors(aa[0],c,root))
 def test_co_shifted_raw_and_contract_still_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);a=copy.deepcopy(self.aa[1]);c=copy.deepcopy(self.ch);ref=a['context']['source_continuity']['fixed_witness_reference'];spec=json.loads((F/ref['path']).read_text())
   raw=(F/spec['raw_file']).read_bytes().replace('子玄，字眉子'.encode(),'子玄，字眉子甲'.encode());spec['raw_sha256']=hashlib.sha256(raw).hexdigest();c['source']['wikitext_sha256']=spec['raw_sha256']
   dest=root/spec['raw_file'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
   b=json.dumps(spec,ensure_ascii=False).encode();dest=root/ref['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);ref['sha256']=hashlib.sha256(b).hexdigest()
   self.assertTrue(natural_parentage_errors(a,c,root))
if __name__=='__main__':unittest.main()
