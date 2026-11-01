"""Finite received unit regression tests, no generated exports."""
import copy,json,os,shutil,tempfile,unittest
from pathlib import Path
from scripts.fixed_jin044_lu_rendered import CH,REF,proof,errors
ROOT=Path(os.environ.get('CBR_NATIVE_TEST_ROOT',Path(__file__).resolve().parents[1]))
class Jin044LuTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  b=json.loads((ROOT/REF).read_text());paths={REF,CH,'registry/persons.json','registry/family-assemblies.json',b['capture_ref'],*b['expected_sidecars']}
  paths|={s['path']for s in b['role_seeds'].values()if s['kind']=='existing_mid'}
  paths|={s['path']for s in b.get('identity_exclusion_seeds',{}).values()}
  for rel in paths:
   out=self.root/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,out)
 def read(self,p):return json.loads((self.root/p).read_text())
 def write(self,p,o):(self.root/p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 def test_positive_complete_unit(self):
  c,r=proof(self.root);self.assertEqual(len(c['paragraphs']),12);self.assertEqual(len(r),52)
 def test_missing_last_paragraph_rejected(self):
  c=self.read(CH);c['paragraphs'].pop();self.write(CH,c);self.assertTrue(errors(c,self.root))
 def test_edition_image_promotion_rejected(self):
  c=self.read(CH);c['source']['edition']='武英殿';c['source']['image_verified']=True;self.write(CH,c);self.assertTrue(errors(c,self.root))
 def test_false_liaoxi_person_rejected(self):
  c=self.read(CH);p=c['paragraphs'][10];self.assertEqual([m['surface']for m in p['mentions']if m['surface']=='遼'],['遼']);c['paragraphs'][10]['mentions'][0]['start']+=1;self.write(CH,c);self.assertTrue(errors(c,self.root))
 def test_reverse_evidence_must_exist(self):
  c=self.read(CH);m=c['paragraphs'][0]['mentions'][0];p=self.read('registry/persons.json');a=next(a for a in p['persons']if a['id']==m['person_id']);a['evidence']=[e for e in a['evidence']if e.get('mention_id')!=m['id']];self.write('registry/persons.json',p);self.assertTrue(errors(c,self.root))
 def test_missing_sidecar_rejected(self):
  c=self.read(CH);b=self.read(REF);(self.root/next(iter(b['expected_sidecars']))).unlink();self.assertTrue(errors(c,self.root))
 def test_refused_offer_must_not_become_actual(self):
  c=self.read(CH);rel='source-evidence/jin044-lu-rendered/non_service-and-posthumous-reports.json';o=self.read(rel);o['reports'][0]['reported_state']='actual_service';self.write(rel,o);self.assertTrue(errors(c,self.root))
 def test_fan_parent_not_invented(self):
  c,r=proof(self.root);a=self.read('corpus/jinshu/044-luqin-family-rendered-assertions.json')['assertions'];self.assertFalse(any('藩'in e['quote']for x in a for e in x['evidence']))
 def test_pronouns_not_person_names(self):
  c,r=proof(self.root);self.assertFalse(any(m['surface']in ['之','其','我','吾']for p in c['paragraphs']for m in p['mentions']))
 def test_order_not_absolute_for_ting(self):
  o=self.read('corpus/jinshu/044-luqin-family-rendered-assertions.json');a=next(a for a in o['assertions']if a['predicate']=='brother');q=a['qualifiers']['relative_birth_order'];self.assertIsNone(q.get('older_ordinal'));self.assertIsNone(q.get('younger_ordinal'))
if __name__=='__main__':unittest.main()

class Jin044DynamicRolesTests(unittest.TestCase):
 setUp=Jin044LuTests.setUp
 read=Jin044LuTests.read
 write=Jin044LuTests.write
 def test_current_source_local_rekey_not_permanent_pid_whitelist(self):
  c,r=proof(self.root);before=r['$zhaoxiang'];after='abc_def_xyz'
  for f in self.root.rglob('*.json'):
   o=json.loads(f.read_text())
   def rekey(x):
    if isinstance(x,str):return after if x==before else x
    if isinstance(x,list):return[rekey(v)for v in x]
    if isinstance(x,dict):return{k:rekey(v)for k,v in x.items()}
    return x
   f.write_text(json.dumps(rekey(o),ensure_ascii=False,indent=2)+'\n')
  self.assertEqual(proof(self.root)[1]['$zhaoxiang'],after)
 def test_unknown_owner_rejected(self):
  c=self.read(CH);c['id']='c-foreign-owner';self.write(CH,c);self.assertTrue(errors(c,self.root))
