import copy,json,unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import received_sima_family_sources as owner53
import jin064_wudi_family_sources as owner64
ROOT=Path(__file__).resolve().parents[1]
class SimaReverseEntryChecksum(unittest.TestCase):
 def fixture(self):
  raw=lambda p:(ROOT/p).read_bytes();return ROOT,raw,{p['id']:p for p in json.loads(raw('registry/persons.json'))['persons']}
 def setup(self):
  root,raw,people=self.fixture();c53,r53,d53=owner53._proof(raw,people);c64,r64,d64=owner64._proof(raw,people);docs={**d53,**d64};owners=set(r53.values())|set(r64.values());wrong=next(p for p in people if p not in owners);return root,raw,people,c53,c64,r53,r64,docs,wrong
 def claim(self,owner,mode='both'):
  root,raw,people,c53,c64,r53,r64,docs,wrong=self.setup();c=c53 if owner is owner53 else c64;cid=next(d['id']for p,d in docs.items()if p==c['chapter_path']);mid=next(iter(c['role_current_mids'].values()))[0];p=copy.deepcopy(people);e={'chapter_id':cid,'mention_id':mid,'quote':'本源current reverse claim'}
  if mode=='MID':e['chapter_id']='c-unrelated-current-source'
  if mode=='CID':e['mention_id']='m-not-owned-but-chapter-claim-is-owned'
  p[wrong]['evidence'].append(e);return root,raw,p,wrong
 def rejected_entry(self,owner,mode='both'):
  root,raw,p,wrong=self.claim(owner,mode)
  with patch.object(owner53,'_raw',lambda r,path:raw(path)),patch.object(owner64,'_raw',lambda r,path:raw(path)):
   with self.assertRaisesRegex(ValueError,'caller/physical'):owner.guard_bundle(root,wrong,p,[])
 def test_01_both_current_owners_prove_sources_and_caller(self):
  root,raw,p,c53,c64,r53,r64,docs,wrong=self.setup()
  with patch.object(owner53,'_raw',lambda r,path:raw(path)),patch.object(owner64,'_raw',lambda r,path:raw(path)):
   owner53.guard_bundle(root,r53['yu'],p,list(docs.values()));owner53.guard_bundle(root,r64['qin'],p,list(docs.values()))
 def test_02_053_reverse_only_new_live_owner_with_no_records_rejected(self):self.rejected_entry(owner53)
 def test_03_064_reverse_only_new_live_owner_with_no_records_rejected(self):self.rejected_entry(owner64)
 def test_04_064_reverse_claim_through_normal_053_dispatch_rejected(self):
  root,raw,p,wrong=self.claim(owner64)
  with patch.object(owner53,'_raw',lambda r,path:raw(path)),patch.object(owner64,'_raw',lambda r,path:raw(path)):
   with self.assertRaisesRegex(ValueError,'Jin064 caller/physical'):owner53.guard_bundle(root,wrong,p,[])
 def test_05_exact_owned_mid_cannot_hide_in_wrong_cid(self):
  for owner in(owner53,owner64):self.rejected_entry(owner,'MID')
 def test_06_exact_owned_cid_cannot_hide_with_wrong_mid(self):
  for owner in(owner53,owner64):self.rejected_entry(owner,'CID')
 def test_07_unrelated_historical_embedded_string_does_not_claim_owner(self):
  root,raw,p,c53,c64,r53,r64,docs,wrong=self.setup();p=copy.deepcopy(p)
  for c in(c53,c64):
   mid=next(iter(c['role_current_mids'].values()))[0];p[wrong]['evidence'].append({'chapter_id':'c-unrelated','mention_id':'opaque-prefix-'+mid,'historical_note':mid})
  with patch.object(owner53,'_raw',lambda r,path:raw(path)),patch.object(owner64,'_raw',lambda r,path:raw(path)):owner53.guard_bundle(root,wrong,p,[])
 def test_08_missing_contract_with_current_reverse_claim_rejected(self):
  for owner in(owner53,owner64):
   _,raw,p,wrong=self.claim(owner)
   with tempfile.TemporaryDirectory(prefix='sima-guard-empty-')as d:
    with self.assertRaisesRegex(ValueError,'without contract'):owner.guard_bundle(Path(d),wrong,p,[])
 def checksum_before_docs(self,owner):
  root,raw,p,c53,c64,r53,r64,docs,wrong=self.setup();c=c53 if owner is owner53 else c64;calls=[]
  def read(r,path):
   calls.append(path)
   return b'{'if path==owner.REF else raw(path)
  with patch.object(owner53,'_raw',read),patch.object(owner64,'_raw',read):
   with self.assertRaisesRegex(ValueError,'contract checksum mismatch'):owner.guard_bundle(root,wrong,p,[])
  self.assertFalse(set(c['expected_documents'])&set(calls))
 def test_09_053_checksum_checked_before_json_or_expected_documents(self):self.checksum_before_docs(owner53)
 def test_10_064_checksum_checked_before_json_or_expected_documents(self):self.checksum_before_docs(owner64)
 def test_11_valid_unrelated_caller_remains_noop(self):
  root,raw,p,_,_,_,_,_,wrong=self.setup()
  with patch.object(owner53,'_raw',lambda r,path:raw(path)),patch.object(owner64,'_raw',lambda r,path:raw(path)):owner53.guard_bundle(root,wrong,p,[])
if __name__=='__main__':unittest.main()
