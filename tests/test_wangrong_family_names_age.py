"""Complete five-person surname/name reading and lifetime/death age boundaries."""
from pathlib import Path
import os,sys,json,copy,unittest,tempfile,shutil,hashlib
F=Path(os.environ.get('CBR_TEST_ROOT',Path(__file__).resolve().parents[1]));sys.path.insert(0,str(F))
from scripts import fixed_repository_family_names as g
from scripts.surname_from_father import validate as surname_valid
from scripts.person_bundle import validate_clan_style,validate_courtesy_name
from scripts.age_context import age_context_valid

def read(root,rel):return json.loads((root/rel).read_text())
def write(root,rel,obj):(root/rel).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def records(root):
 p=read(root,g.PROOF);r=read(root,'source-evidence/jin043-wyd1739-wangrong/ner-witness-contract.json');paths={u['path']for u in p['source_units']}|{p['witness_path'],p['assertions_path'],'corpus/jinshu/043-wangrong-life-events.json'}|set(p['name_files'])|set(r['sidecars']);return[read(root,x)for x in sorted(paths)]
def catalog(root):return{p['id']:p for p in read(root,'registry/persons.json')['persons']},records(root)
def required(root):
 p=read(root,g.PROOF);r=read(root,'source-evidence/jin043-wyd1739-wangrong/ner-witness-contract.json');paths={g.PROOF,'registry/persons.json',p['assertions_path'],'corpus/jinshu/043-wangrong-life-events.json','source-evidence/jin043-wyd1739-wangrong/ner-witness-contract.json',r['chapter_path'],r['seed_path'],r['raw_path']}|set(r['sidecars'])|set(r['fixed_files'])|set(p['name_files'])
 for u in p['source_units']:paths|={u['path'],u['raw_path']}
 return paths
class NamePhase(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.root=Path(self.t.name)
  for rel in required(F):
   p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(F/rel,p)
 def data(self):
  people,rr=catalog(self.root);ns=[n for r in rr if r.get('record_type')=='person_name_component_set'for n in r['records']];cs={r['id']:r for r in rr if r.get('record_type')=='marked_chapter'};aa=[a for r in rr if r.get('record_type')=='person_assertion_set'for a in r['assertions']];return people,rr,ns,cs,aa
 def phase(self):
  people,rr,ns,cs,aa=self.data();g.validate_installed(self.root,people,rr);return people,rr,ns,cs,aa
 def test_all_five_names_and_source_roles(self):
  people,rr,ns,cs,aa=self.phase();names=read(self.root,g.FILES[0])['records']+read(self.root,g.FILES[1])['records'];self.assertEqual({n['surname']+(n['ming']or'氏')for n in names},{'王戎','王雄','王渾','王綏','王興','王氏'})
  for n in names:
   if n.get('surname_basis'):surname_valid(n,ns,cs,aa,root=self.root)
   p=next(p for p in cs[n['chapter_id']]['paragraphs']if p['id']==n['paragraph_id']);validate_clan_style(n,p,aa,root=self.root);validate_courtesy_name(n)
  sui=next(n for n in names if n['ming']=='綏');self.assertNotIn('zi',sui);self.assertIn('王綏',sui['quote']);self.assertIn('瓚字國寶',sui['quote'])
 def test_no_new_relation_or_person_record(self):
  p,roles,cs,aa,files=g.state(self.root);grand=roles['$grandfather'];father=roles['$father'];self.assertFalse(any(a['predicate']=='father'and(a['subject_person_id'],a['object_person_id'])==(father,grand)for a in aa.values()));self.assertIsNone(files[g.FILES[0]]['records'][-1]['ming']);self.assertNotIn('full_name',files[g.FILES[0]]['records'][-1])
 def test_age_contexts_without_birth_inference(self):
  old=read(self.root,'corpus/jinshu/043-wangrong.json');ages=old['annotation']['age_assertions'];events={e['id']:e for e in read(self.root,'corpus/jinshu/043-wangrong-life-events.json')['events']};self.assertEqual([a['age_context']['kind']for a in ages],['during_life','at_death','at_death'])
  for a in ages:self.assertTrue(age_context_valid(a,events));self.assertIsNone(a['birth_year']);self.assertEqual(a['counting'],'unspecified_source_age')
  bad=copy.deepcopy(ages[0]);bad['age_context']={'kind':'at_death','life_event_id':'le-jin043-wangrong-rong'};self.assertFalse(age_context_valid(bad,events))
  bad=copy.deepcopy(ages[1]);bad['age_context']['life_event_id']='le-jin043-wangrong-hun';self.assertFalse(age_context_valid(bad,events))
 def test_wrong_head_source_endpoint_rejected(self):
  c=read(self.root,'corpus/jinshu/043-wangrong.json');c['paragraphs'][0]['mentions'][0]['person_id']=c['paragraphs'][0]['mentions'][2]['person_id'];write(self.root,'corpus/jinshu/043-wangrong.json',c)
  with self.assertRaises(ValueError):self.phase()
 def test_grandfather_cannot_be_maternal_or_father(self):
  for key,value in [('predicate','father'),('lineage','maternal')]:
   original=read(self.root,'corpus/jinshu/043-wangrong-assertions.json');bad=copy.deepcopy(original);a=next(a for a in bad['assertions']if a['id']=='a-jin043-wangrong-002')
   if key=='predicate':a[key]=value
   else:a['qualifiers'][key]=value
   write(self.root,'corpus/jinshu/043-wangrong-assertions.json',bad)
   with self.assertRaises(ValueError):self.phase()
   write(self.root,'corpus/jinshu/043-wangrong-assertions.json',original)
 def test_reversed_daughter_father_is_rejected(self):
  x=read(self.root,'corpus/jinshu/043-wangrong-assertions.json');a=next(a for a in x['assertions']if a['id']=='a-jin043-wangrong-009');a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];write(self.root,'corpus/jinshu/043-wangrong-assertions.json',x)
  with self.assertRaises(ValueError):self.phase()
 def test_partial_raw_source_rejected(self):
  p=read(self.root,g.PROOF);r=read(self.root,'source-evidence/jin043-wyd1739-wangrong/ner-witness-contract.json');q=self.root/r['raw_path'];q.write_bytes(q.read_bytes()[:-4])
  with self.assertRaises(ValueError):self.phase()
 def test_partial_chapter_rejected(self):
  c=read(self.root,'corpus/jinshu/043-wyd1739-wangrong.json');c['paragraphs']=c['paragraphs'][:1];write(self.root,'corpus/jinshu/043-wyd1739-wangrong.json',c)
  with self.assertRaises(ValueError):self.phase()
 def test_caller_cannot_omit_chapter_or_name_sidecar(self):
  people,rr,ns,cs,aa=self.data();pid=read(self.root,g.FILES[1])['records'][0]['person_id']
  for bad in [[r for r in rr if r.get('id')!=g.NEW],[r for r in rr if r!=read(self.root,g.FILES[1])],[r for r in rr if r.get('record_type')!='person_name_component_set']]:
   with self.assertRaises(ValueError):g.guard_bundle(self.root,pid,people,bad)
 def test_caller_person_reverse_omission_rejected(self):
  people,rr,ns,cs,aa=self.data();pid=read(self.root,g.FILES[1])['records'][0]['person_id'];people[pid]['evidence']=[]
  with self.assertRaises(ValueError):g.guard_bundle(self.root,pid,people,rr)
 def test_daughter_cannot_have_husband_surname_or_fake_ming(self):
  people,rr,ns,cs,aa=self.data();n=read(self.root,g.FILES[0])['records'][-1];p=next(p for p in cs[g.OLD]['paragraphs']if p['id']==n['paragraph_id'])
  for field,value in [('surname','裴'),('ming','王戎女'),('ming','國寶')]:
   bad=copy.deepcopy(n);bad[field]=value;self.assertFalse(g.clan_valid(bad,p,aa,root=self.root))
 def test_source_qualifications_not_promoted(self):
  c=read(self.root,'corpus/jinshu/043-wyd1739-wangrong.json');self.assertFalse(c['source']['image_verified']);self.assertEqual(c['source']['review_status'],'AI_image_transcription_draft');self.assertEqual(sum(p['text'].count('〓')for p in c['paragraphs']),3)
 def test_consistent_namespace_rekey_not_pid_whitelist(self):
  p,roles,*_=g.state(self.root);mapping={roles['$'+k]:'z8z_8z8_z8z'+tail for k,tail in [('grandfather',''),('father','_A'),('head','_AA'),('wan','_AAA'),('xing','_AAB'),('daughter','_AAC')]};self.assertFalse(set(mapping.values())&{x['id']for x in read(self.root,'registry/persons.json')['persons']})
  def replace(x):
   if isinstance(x,dict):return{k:replace(v)for k,v in x.items()}
   if isinstance(x,list):return[replace(v)for v in x]
   return mapping.get(x,x)if isinstance(x,str)else x
  for rel in required(self.root):
   if rel.endswith('.json'):
    # Contract templates have no PIDs; exact scalar replacement preserves MIDs/opaque IDs.
    value=read(self.root,rel);changed=replace(value)
    if changed!=value:write(self.root,rel,changed)
  self.phase()
 def test_single_endpoint_rekey_is_rejected(self):
  c=read(self.root,g.FILES[1]);c['records'][0]['person_id']='z8z_8z8_z8z_AAA';write(self.root,g.FILES[1],c)
  with self.assertRaises(ValueError):self.phase()
 def test_live_age_cannot_be_presented_as_death_age(self):
  c=read(self.root,'corpus/jinshu/043-wangrong.json');c['annotation']['age_assertions'][0]['age_context']={'kind':'at_death','life_event_id':'le-jin043-wangrong-rong'};write(self.root,'corpus/jinshu/043-wangrong.json',c)
  with self.assertRaises(ValueError):self.phase()
if __name__=='__main__':unittest.main()
