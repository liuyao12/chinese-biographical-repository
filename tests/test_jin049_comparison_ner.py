import unittest,json,copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from scripts.fixed_jin049_jikang_rendered_comparison import validate_source,source_errors,CH,CID,BASE,_phase
class Jin049NER(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/CH).read_bytes())
  if self.ch['annotation'].get('additional_typed_phase',{}).get('kind')=='jin049_received_basics_v1':self.ch['annotation']=copy.deepcopy(_phase(ROOT)['chapter_template']['annotation'])
 def test_complete(self):self.assertTrue(validate_source(self.ch,ROOT));self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),2636);self.assertEqual(len(self.ch['paragraphs']),17)
 def test_source_only_stays_strict(self):
  base=json.loads((ROOT/(BASE+'contract.json')).read_bytes());c=copy.deepcopy(self.ch);c['annotation']=base['required_annotation'];c['paragraphs']=base['paragraphs'];self.assertTrue(validate_source(c,ROOT));c['paragraphs'][0]['annotation_status']='in_progress';self.assertTrue(source_errors(c,ROOT))
 def test_marker_endpoint_or_role_drift(self):
  for k,v in [('person_id','wrong'),('surface','錯'),('start',1),('role_key','shantao'),('kind','unresolved')]:
   c=copy.deepcopy(self.ch);c['paragraphs'][0]['mentions'][0][k]=v;self.assertTrue(source_errors(c,ROOT),k)
 def test_capture_and_human_qualifications(self):
  for area,k,v in [('source','witness_role','preferred'),('source','revision_id',2199702),('source','image_verified',True),('annotation','human_reviewed',True),('annotation','model','invented')]:
   c=copy.deepcopy(self.ch);c[area][k]=v;self.assertTrue(source_errors(c,ROOT))
 def test_letter_poem_full_scope(self):
  for i in [3,8,10,13]:
   c=copy.deepcopy(self.ch);c['paragraphs'][i]['text']=c['paragraphs'][i]['text'][:-1];self.assertTrue(source_errors(c,ROOT))
 def test_two_xiangru_and_booknames(self):
  p=self.ch['paragraphs'][4];a={m['surface']:m['person_id']for m in p['mentions']};self.assertNotEqual(a['長卿'],a['相如']);q=self.ch['paragraphs'][5];m,=[m for m in q['mentions']if m['surface']=='尚子平、臺孝感傳'];self.assertEqual(m['kind'],'work');self.assertIsNone(m['person_id'])
 def test_no_mother_brother_death_or_false_names(self):
  c=_phase(ROOT);facts=c['sidecar_templates']['corpus/jinshu/049-jikang-rendered-comparison-assertions.json']['assertions'];self.assertEqual(len(facts),4);self.assertTrue(all(a['predicate']in ['father','brother']for a in facts));self.assertFalse(any(m['surface']=='髙子臧'for p in self.ch['paragraphs']for m in p['mentions']))
 def test_seed_metadata_or_owner_drift(self):
  from unittest.mock import patch
  seed=_phase(ROOT)['existing_seeds'][0];path=ROOT/seed['path'];original=Path.read_bytes
  for kind in ['metadata','owner']:
   d=json.loads(original(path))
   if kind=='metadata':d['source']['revision_id']='wrong'
   else:
    p,=[p for p in d['paragraphs']if p['id']==seed['paragraph_id']];m,=[m for m in p['mentions']if m['id']==seed['mention_id']];m['person_id']='wrong'
   raw=json.dumps(d,ensure_ascii=False).encode()
   with patch.object(Path,'read_bytes',lambda p:raw if p==path else original(p)):self.assertTrue(source_errors(self.ch,ROOT),kind)
 def test_legal_local_role_rekey_and_missing_reverse(self):
  from unittest.mock import patch
  phase=_phase(ROOT);key='xiangxiu';pid=next(m['person_id']for p in self.ch['paragraphs']for m in p['mentions']if m.get('role_key')==key);new='abc_xyz_012'
  def walk(x):
   if isinstance(x,str):return new if x==pid else x
   if isinstance(x,list):return[walk(a)for a in x]
   if isinstance(x,dict):return{k:walk(v)for k,v in x.items()}
   return x
  paths=[ROOT/'registry/persons.json']+[ROOT/k for k in phase['sidecar_templates']];original=Path.read_bytes;changed={p:json.dumps(walk(json.loads(original(p))),ensure_ascii=False).encode()for p in paths};ch=walk(self.ch)
  import hashlib
  from scripts import fixed_jin049_jikang_rendered_comparison as module
  np=ROOT/(BASE+'ner-phase-contract.json');tp=ROOT/(BASE+'typed-basics-contract.json');pp=copy.deepcopy(phase);pp['role_judgments']=walk(pp['role_judgments']);nb=(json.dumps(pp,ensure_ascii=False,indent=2)+'\n').encode();tt=json.loads(original(tp));tt['base_ner_phase_sha256']=hashlib.sha256(nb).hexdigest();tb=(json.dumps(tt,ensure_ascii=False,indent=2)+'\n').encode();changed[np]=nb;changed[tp]=tb
  with patch.object(Path,'read_bytes',lambda p:changed[p]if p in changed else original(p)),patch.object(module,'PHASE_SHA',hashlib.sha256(nb).hexdigest()),patch.object(module,'TYPED_SHA',hashlib.sha256(tb).hexdigest()):self.assertTrue(validate_source(ch,ROOT))
  d=json.loads(changed[ROOT/'registry/persons.json']);r,=[r for r in d['persons']if r['id']==new];r['evidence']=[];changed[ROOT/'registry/persons.json']=json.dumps(d,ensure_ascii=False).encode()
  with patch.object(Path,'read_bytes',lambda p:changed[p]if p in changed else original(p)),patch.object(module,'PHASE_SHA',hashlib.sha256(nb).hexdigest()),patch.object(module,'TYPED_SHA',hashlib.sha256(tb).hexdigest()):self.assertTrue(source_errors(ch,ROOT))
if __name__=='__main__':unittest.main()
