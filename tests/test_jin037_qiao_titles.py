"""Finite received titles and external265 bridge; no inferred birthdays/office ends."""
import ast,copy,json,unittest
from pathlib import Path
from scripts import jin037_qiao_title_reports as owner
from scripts.noble_transfers import noble_transfer_errors
ROOT=Path(__file__).resolve().parents[1]
class QiaoTitles(unittest.TestCase):
 def setUp(self):self.changes={}
 def raw(self,p):return (json.dumps(self.changes[p],ensure_ascii=False,indent=2)+'\n').encode()if p in self.changes else(ROOT/p).read_bytes()
 def doc(self,p):
  if p not in self.changes:self.changes[p]=json.loads(self.raw(p))
  return self.changes[p]
 def state(self):return owner._proof(self.raw)
 def bad(self):
  with self.assertRaises((AssertionError,ValueError,KeyError,TypeError)):self.state()
 def test_fifteen_source_holdings_and_four_raw_accessions(self):
  ch,c,r,d=self.state();self.assertEqual(len(d['holdings']),15)
  inherited=[h for h in d['holdings']if'inheritance'in h];self.assertEqual(len(inherited),4)
  for h in inherited:self.assertEqual(h['title'],'立');self.assertEqual(h['inheritance']['resolved_title'],'譙王');self.assertEqual(h['mode'],'accession')
  self.assertFalse(any(h['mode']=='posthumous_naming'for h in d['holdings']))
 def test_two_transfers_use_actual_generic_checker(self):
  ch,c,r,d=self.state();hs={h['id']:h for h in d['holdings']};ps={p['id']:(ch['id'],p)for p in ch['paragraphs']};ms={m['id']:(ch['id'],p['id'],m)for p in ch['paragraphs']for m in p['mentions']}
  moves=[h for h in d['holdings']if h['mode']=='transfer'];self.assertEqual(len(moves),2)
  for h in moves:self.assertEqual(noble_transfer_errors(h,hs,ps,ms,{ch['id']:ch}),[])
  bad=copy.deepcopy(moves[0]);bad['transfer_basis']['previous_holding_id']=bad['id'];self.assertTrue(noble_transfer_errors(bad,hs,ps,ms,{ch['id']:ch}))
 def test_265_standard_metadata_and_direct_reference(self):
  ch,c,r,d=self.state();h=next(h for h in d['holdings']if'normalized_date'in h['effective_period']['start']);date=h['effective_period']['start']['normalized_date']
  self.assertEqual(date['year'],265);self.assertEqual(date['calendar'],'chinese_civil');self.assertFalse(any(k in date for k in('month','day')));self.assertTrue(owner._date_valid(self.raw,date,h,'start',{ch['id']:ch}))
  self.assertEqual(h['reported_households']['value'],4400);self.assertEqual(h['reported_households']['source_anchor']['surface'],'邑四千四百戶')
 def test_266_and_other_holding_date_rejected(self):
  ch,c,r,d=self.state();h=next(h for h in d['holdings']if'normalized_date'in h['effective_period']['start']);date=copy.deepcopy(h['effective_period']['start']['normalized_date']);date['year']=date['era_year']=266
  self.assertFalse(owner._date_valid(self.raw,date,h,'start',{ch['id']:ch}));other=d['holdings'][0];self.assertFalse(owner._date_valid(self.raw,h['effective_period']['start']['normalized_date'],other,'start',{ch['id']:ch}))
 def test_date_metadata_precision_review_and_wrong_endpoint(self):
  ch,c,r,d=self.state();h=next(h for h in d['holdings']if'normalized_date'in h['effective_period']['start']);date=h['effective_period']['start']['normalized_date']
  for key,value in [('month',12),('day',1),('human_reviewed',True)]:
   bad=copy.deepcopy(date);bad[key]=value;self.assertFalse(owner._date_valid(self.raw,bad,h,'start',{ch['id']:ch}))
  self.assertFalse(owner._date_valid(self.raw,date,h,'life_event',{ch['id']:ch}))
 def test_foreign_title_claim_dispatches_to_base_proof(self):
  # Dispatch-only spy: real source consistency is independently exercised above.
  ch,c,r,d=self.state();calls=[];foreign='z9q_8xr_7pv';raw=self.raw
  class SourcePath:
   def __truediv__(self,p):self.p=p;return self
   def is_file(self):return True
   def exists(self):return True
   def read_bytes(self):return raw(self.p)
  def reject(*a):calls.append(True);raise ValueError('base proof invoked')
  source=(ROOT/'scripts/fixed_jin037_qiao_cheng_wuji.py').read_bytes().decode();tree=ast.parse(source);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='guard_bundle')
  ns=dict(Path=lambda root:SourcePath(),CH=owner.CH,REF='source-evidence/jin037-qiao-cheng-wuji/source-contract.json',CID=ch['id'],json=json,proof=reject);exec(compile(ast.Module(body=[node],type_ignores=[]),'<actual guard_bundle dispatch>','exec'),ns)
  changed=copy.deepcopy(d);changed['holdings'][0]['person_id']=foreign
  with self.assertRaises(ValueError):ns['guard_bundle'](None,foreign,{},[ch,changed])
  self.assertEqual(calls,[True])
 def test_no_offices_or_death_endpoints(self):
  _,_,_,d=self.state();self.assertTrue(all(h['kind']in('noble_rank','honorific')for h in d['holdings']))
  for h in d['holdings']:
   self.assertIsNone(h['effective_period']['end'].get('normalized_date'));self.assertNotIn('death',str(h['effective_period']['end']))
 def test_missing_title_sidecar_or_unknown_metadata_rejected(self):
  _,c,_,_=self.state();self.doc(c['title_path'])['unreviewed_metadata']=True;self.bad()
 def test_wrong_successor_parent_or_fief_rejected(self):
  _,c,_,_=self.state();h=next(h for h in self.doc(c['title_path'])['holdings']if'inheritance'in h);h['inheritance']['predecessor_person_id']=h['person_id'];self.bad()
 def test_wrong_grant_recipient_rejected(self):
  _,c,r,_=self.state();h=next(h for h in self.doc(c['title_path'])['holdings']if h['title']=='廣晉伯');h['person_id']=r['$wuji'];self.bad()
 def test_honorific_is_not_fabricated_naming_event(self):
  _,c,_,_=self.state();h=next(h for h in self.doc(c['title_path'])['holdings']if h['kind']=='honorific');h['mode']='posthumous_naming';self.bad()
 def test_unknown_source_qualification_rejected(self):
  self.doc(owner.CH)['source']['image_verified']=True;self.bad()
 def test_reference_qualification_and_calendar_source_rejected(self):
  _,c,_,_=self.state();bridge=json.loads(self.raw(c['bridge_path']));self.doc(bridge['observation_path'])['qualification']['fixed_body_obtained']=True;self.bad()
 def test_wrong_calendar_bytes_rejected(self):
  _,c,_,_=self.state();bridge=json.loads(self.raw(c['bridge_path']));cal=bridge['calendar']['path'];raw=self.raw
  with self.assertRaises(AssertionError):owner._proof(lambda p:raw(p)+b' 'if p==cal else raw(p))
 def test_single_endpoint_rejected(self):
  _,c,_,_=self.state();seed=c['role_seeds']['xun'];m=next(m for p in self.doc(owner.CH)['paragraphs']for m in p['mentions']if m['id']==seed['marker']['id']);m['person_id']='z9q_8xr_7pv';self.bad()
 def test_coherent_role_endpoint_rekey_retains_opaque_ids(self):
  ch,c,r,d=self.state();old=r['$xun'];new='z9q_8xr_7pv';paths=[owner.CH,c['title_path'],c['father_assertion_path'],'registry/persons.json']
  def opaque(v,out):
   if isinstance(v,dict):
    if'id'in v and v['id']not in(old,new):out.append(v['id'])
    for x in v.values():opaque(x,out)
   elif isinstance(v,list):
    for x in v:opaque(x,out)
  for path in paths:
   original=json.loads(self.raw(path));v=self.doc(path)
   def change(x):
    if isinstance(x,dict):
     for k,z in list(x.items()):
      if k in('person_id','subject_person_id','object_person_id','predecessor_person_id','parent_person_id')and z==old:x[k]=new
      elif k=='id'and z==old and path=='registry/persons.json':x[k]=new
      else:change(z)
    elif isinstance(x,list):
     for z in x:change(z)
   change(v);a=[];b=[];opaque(original,a);opaque(v,b);self.assertEqual(a,b)
  self.assertEqual(self.state()[2]['$xun'],new)
if __name__=='__main__':unittest.main()
