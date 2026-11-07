import unittest,json,copy,hashlib
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_jin049_jikang_rendered_comparison as mod
ROOT=Path(__file__).resolve().parents[1]
class CurrentRoleJudgments(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/mod.CH).read_bytes());self.phase=mod._phase(ROOT);self.people={r['id']:r for r in json.loads((ROOT/'registry/persons.json').read_bytes())['persons']};self.roles=mod.resolve_roles(self.ch,ROOT,self.phase)
 def test_actual_all_roles(self):self.assertTrue(mod.current_role_judgments_valid(self.phase,self.roles,self.people));self.assertTrue(mod.validate_source(self.ch,ROOT))
 def test_wrong_preferred_existing_member(self):
  p=copy.deepcopy(self.phase);keys=list(self.roles);p['role_judgments'][keys[0]]['preferred_person_id']=next(pid for pid in self.roles.values()if pid!=self.roles[keys[0]])
  with self.assertRaises(ValueError):mod.current_role_judgments_valid(p,self.roles,self.people)
 def test_current_candidate_membership_and_role(self):
  key=next(iter(self.roles))
  for kind in ['missing','role','label']:
   p=copy.deepcopy(self.phase);x=next(x for x in p['role_judgments'][key]['registry_candidates']if x.get('candidate_type')=='current_preferred_role')
   if kind=='missing':x['person_id']='missing'
   if kind=='role':x['current_role_key']='wrong'
   if kind=='label':x['label']='wrong'
   with self.assertRaises(ValueError):mod.current_role_judgments_valid(p,self.roles,self.people)
 def test_unresolved_and_recall_not_preferred(self):
  key=next(k for k in self.phase['role_judgments']if k not in self.roles);p=copy.deepcopy(self.phase);p['role_judgments'][key]['preferred_person_id']=next(iter(self.roles.values()))
  with self.assertRaises(ValueError):mod.current_role_judgments_valid(p,self.roles,self.people)
 def test_missing_seed_reverse(self):
  original=Path.read_bytes;reg=ROOT/'registry/persons.json';d=json.loads(original(reg));seed=self.phase['existing_seeds'][0];pid=self.roles[seed['role_key']];r,=[r for r in d['persons']if r['id']==pid];r['evidence']=[e for e in r['evidence']if e.get('mention_id')!=seed['mention_id']];raw=json.dumps(d,ensure_ascii=False).encode()
  with patch.object(Path,'read_bytes',lambda p:raw if p==reg else original(p)):self.assertTrue(mod.source_errors(self.ch,ROOT))
 def test_coherent_canonical_rekey_requires_current_judgments_and_pins(self):
  # Any verified seed role is eligible, no Shan/person whitelist in production guard.
  key='shantao';old=self.roles[key];new='abc_xyz_017';self.assertNotIn(new,self.people)
  def walk(x):
   if isinstance(x,str):return new if x==old else x
   if isinstance(x,list):return[walk(a)for a in x]
   if isinstance(x,dict):return{k:walk(v)for k,v in x.items()}
   return x
  paths={ROOT/mod.CH,ROOT/'registry/persons.json'}|{ROOT/s['path']for s in self.phase['existing_seeds']}|{ROOT/k for k in self.phase['sidecar_templates']}
  read=Path.read_bytes;changed={p:json.dumps(walk(json.loads(read(p))),ensure_ascii=False).encode()for p in paths};ch=walk(self.ch);np=ROOT/(mod.BASE+'ner-phase-contract.json');tp=ROOT/(mod.BASE+'typed-basics-contract.json');phase=walk(self.phase);nb=(json.dumps(phase,ensure_ascii=False,indent=2)+'\n').encode();typed=json.loads(read(tp));typed['base_ner_phase_sha256']=hashlib.sha256(nb).hexdigest();tb=(json.dumps(typed,ensure_ascii=False,indent=2)+'\n').encode();changed[np]=nb;changed[tp]=tb
  with patch.object(Path,'read_bytes',lambda p:changed[p]if p in changed else read(p)),patch.object(mod,'PHASE_SHA',hashlib.sha256(nb).hexdigest()),patch.object(mod,'TYPED_SHA',hashlib.sha256(tb).hexdigest()):self.assertTrue(mod.validate_source(ch,ROOT))
  # All source endpoints moved, but old metadata/pins cannot masquerade as current.
  changed.pop(np);changed.pop(tp)
  with patch.object(Path,'read_bytes',lambda p:changed[p]if p in changed else read(p)):self.assertTrue(mod.source_errors(ch,ROOT))
if __name__=='__main__':unittest.main()
