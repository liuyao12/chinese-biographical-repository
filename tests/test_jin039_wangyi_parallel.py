"""Small pure unit tests over actual source payloads; no clone/native/export."""
import copy,json,unittest
from pathlib import Path
from scripts import jin039_wangyi_parallel as w
ROOT=Path(__file__).resolve().parents[1]
class WangYiRoleMerge(unittest.TestCase):
 def setUp(self):
  self.changed={};self.base={}
  for p in [w.REF,w.CH,w.CANON,w.DEC,w.LEDGER,w.RET,'registry/persons.json']:
   self.base[p]=(ROOT/p).read_bytes()
  self.c=json.loads(self.base[w.REF]);self.before_ledger=json.loads(self.base[w.LEDGER])
  self.old=self.c['retired_registry_record_before']['id']
  for pointer in self.c['ledger']['explicit_person_pointers']:w._slot(self.before_ledger,pointer)['person_id']=self.old
 def raw(self,p):
  if p in self.changed:return (json.dumps(self.changed[p],ensure_ascii=False,indent=2)+'\n').encode()
  return self.base[p]if p in self.base else(ROOT/p).read_bytes()
 def doc(self,p):
  if p not in self.changed:self.changed[p]=json.loads(self.raw(p))
  return self.changed[p]
 def fail(self):
  with self.assertRaises((AssertionError,KeyError,ValueError,TypeError)):w._proof(self.raw)
 def test_current_source_roles(self):
  c,pid,old,marks=w._proof(self.raw);self.assertNotEqual(pid,old);self.assertEqual(len(marks),2)
  self.assertEqual(w._project_current_ledger(self.before_ledger,w.LEDGER,self.raw),json.loads(self.raw(w.LEDGER)))
 def test_one_endpoint(self):
  c,pid,old,marks=w._proof(self.raw);ch=self.doc(w.CH)
  next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==marks[0]['id'])['person_id']=old;self.fail()
 def test_reverse_missing(self):
  c,pid,old,marks=w._proof(self.raw);actor=next(p for p in self.doc('registry/persons.json')['persons']if p['id']==pid)
  actor['evidence']=[e for e in actor['evidence']if e.get('mention_id')!=marks[0]['id']];self.fail()
 def test_wrong_owner_alias(self):
  c,pid,old,marks=w._proof(self.raw);actor=next(p for p in self.doc('registry/persons.json')['persons']if p['id']==pid)
  actor['aliases']=[a for a in actor['aliases']if a['surface']!=marks[0]['surface']];self.fail()
 def test_unknown_marker_metadata(self):
  c,pid,old,marks=w._proof(self.raw);next(m for p in self.doc(w.CH)['paragraphs']for m in p['mentions']if m['id']==marks[0]['id'])['unreviewed_extra']=True;self.fail()
 def test_wrong_canonical_mid(self):
  self.doc(w.CANON)['paragraphs'][0]['mentions'][0]['id']='foreign-mid';self.fail()
 def test_source_qualification(self):
  self.doc(w.CH)['source']['image_verified']=True;self.fail()
 def test_ledger_unapproved_leaf(self):
  self.doc(w.LEDGER)['extra_unknown']='tamper'
  with self.assertRaises(AssertionError):w._project_current_ledger(self.before_ledger,w.LEDGER,self.raw)
 def test_ledger_wrong_mid(self):
  pointer=self.c['ledger']['explicit_person_pointers'][0];w._slot(self.doc(w.LEDGER),pointer)['id']='foreign-mid';self.fail()
 def test_receipt_resurrection(self):
  self.doc('registry/persons.json')['persons'].append(self.c['retired_registry_record_before']);self.fail()
 def test_caller_duplicate_unknown_metadata(self):
  ch=json.loads(self.raw(w.CH));dec=json.loads(self.raw(w.DEC));bad=copy.deepcopy(ch);bad['unexpected']=True
  with self.assertRaises(AssertionError):w._proof(self.raw,records=[ch,bad,dec])
 def test_primary_observation_and_capture_immutable(self):
  for path in [self.c['primary_observation_path'],self.c['immutable_prior_captures'][0]['path']]:
   self.changed={};self.doc(path)['unexpected']=True;self.fail()
 def test_prior_reverse_preserved(self):
  c,pid,old,marks=w._proof(self.raw);actor=next(p for p in self.doc('registry/persons.json')['persons']if p['id']==pid);prior=c['canonical_prior_evidence'][-1];actor['evidence'].remove(prior);self.fail()
 def test_coherent_rekey_opaque_conserved(self):
  c,pid,old,marks=w._proof(self.raw);new='z9q_8xr_7pv'
  for path in [w.CH,w.CANON,w.DEC,w.LEDGER,'registry/persons.json']:
   v=self.doc(path)
   def visit(x):
    if isinstance(x,dict):
     if x.get('person_id')==pid:x['person_id']=new
     if x.get('id')==pid and x in v.get('persons',[]):x['id']=new
     for z in x.values():visit(z)
    elif isinstance(x,list):
     for z in x:visit(z)
   visit(v)
  self.assertEqual(w._proof(self.raw)[1],new)
  # Only typed endpoints/registry ID move; no substring changes to opaque IDs.
  def opaque(x,out):
   if isinstance(x,dict):
    if 'id'in x and x['id']not in(pid,new):out.append(x['id'])
    for z in x.values():opaque(z,out)
   elif isinstance(x,list):
    for z in x:opaque(z,out)
  for path in [w.CH,w.CANON,w.DEC,w.LEDGER]:
   a=[];b=[];opaque(json.loads(self.base[path]),a);opaque(self.changed[path],b);self.assertEqual(a,b)
if __name__=='__main__':unittest.main()
