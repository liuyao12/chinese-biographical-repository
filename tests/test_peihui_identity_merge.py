# coding: utf-8
"""Source-bound identity/retirement checks; fixed MIDs resolve current IDs."""
from pathlib import Path
import json,copy,hashlib,unittest
ROOT=Path(__file__).resolve().parents[1]
OLD='047_850_e7d';DID='d-sanguozhi010-peihui-xuncan-peikai';BASE='source-evidence/peihui-identity-merge'
PATHS=['corpus/sanguozhi/010.json','corpus/jinshu/035-pei-family.json','corpus/jinshu/035-peixiu.json']
MID='c-sanguozhi-010-xunyu-xunyou-jiaxu:full:u029:m0324'
RAW_SHA256='d6f42012810a7643dbf554325f4f653b5ae8758322d9afaa0caf1b385b51d4f3';RAW_GIT_BLOB='78b3841be4cb93f1c70f4304753ac4b15b900562'
J=lambda p:json.loads(p.read_bytes())
H=lambda b:hashlib.sha256(b).hexdigest()
def get(v,p):
 for k in p.split('/')[1:]:v=v[int(k)]if isinstance(v,list)else v[k.replace('~1','/').replace('~0','~')]
 return v
def anchor(c,mid):
 for p in c['paragraphs']:
  for m in p['mentions']:
   if m['id']==mid:return p,m
 raise AssertionError('missing source MID')
def state(root):
 cs=[J(root/x)for x in PATHS];review=J(root/BASE/'current-reading.json');d=next(d for d in J(root/'corpus/sanguozhi/010-peihui-identities.json')['decisions']if d['id']==DID)
 primary=review['parallel_primary'];raw=(root/primary['raw_path']).read_bytes();people=J(root/'registry/persons.json')['persons'];keeper=d['person_id']
 links=[]
 for b in review['current_projection_bindings']:
  wrapper=J(root/b['current_path']);links.append(dict(binding=b,value=get(wrapper,b['current_pointer']),history_hash=H((root/b['historical_file']).read_bytes()),history_value=get(J(root/b['historical_file']),b['historical_pointer'])))
 return dict(chapters=cs,decision=d,review=review,raw=raw,links=links,people=[p for p in people if p['id']in (OLD,keeper)],registry_count=len(people),registry_unique=len({p['id']for p in people}))
def valid(s):
 a,b,c=s['chapters'];pa,ma=anchor(a,MID);pb,mb=anchor(b,'c-jinshu-035-peikai-family:p001:m0006');pc,mc=anchor(c,'c-jinshu-035-peixiu:p001:m0047');keeper=mb['person_id'];d=s['decision'];r=s['review'];q=r['parallel_primary'];raw=s['raw']
 assert ma['person_id']==mc['person_id']==d['person_id']==r['canonical_person_id']==keeper
 assert (ma['start'],ma['end'],ma['surface'])==(324,326,'裴徽')and pa['text'][324:326]=='裴徽'
 assert pb['text'].startswith('楷字叔則。父徽，魏冀州刺史。')and pc['text'].startswith('裴秀，字季彥，河東聞喜人也。祖茂，漢尚書令。父潛，魏尚書令。')and '叔父徽有盛名' in pc['text']
 assert '與傅嘏談' in pa['text']and '裴徽通彼我之懐為二家騎驛' in pa['text']and pa['text_layer']=='witness_appended_pei_songzhi_note'
 assert d['id']==DID and d['scope']=='cross_chapter'and d['human_reviewed']is False and set(d['chapter_ids'])=={a['id'],b['id'],c['id']}
 for ch,p in [(a,pa),(b,pb),(c,pc)]:assert any(e['chapter_id']==ch['id']and e['paragraph_id']==p['id']and e['quote']==p['text']for e in d['evidence'])
 assert H(raw)==q['raw_sha256']==RAW_SHA256 and q['git_blob_sha1']==RAW_GIT_BLOB and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==q['git_blob_sha1']
 assert q['revision']=='214fcafa79894355909c9d8c2c1533089e7791c6'and q['native_chapter_id']is None and q['image_verified']is False
 for f in q['bridge_fragments']:assert raw.decode()[f['raw_start']:f['raw_end']]==f['raw']and H(f['raw'].encode())==f['sha256']
 joined=''.join(f['raw']for f in q['bridge_fragments']);assert '潛少弟徽字文季冀州刺史' in joined and '事見荀粲傅嘏王弼管輅諸傳' in joined and '次楷字叔則' in joined
 assert len(s['people'])==1 and s['people'][0]['id']==keeper and s['people'][0]['label']=='裴徽'and s['registry_count']==s['registry_unique']
 assert {e['mention_id']for e in s['people'][0]['evidence']}.issuperset({MID,mb['id'],mc['id']})
 assert len(s['links'])==2
 for link in s['links']:
  z=link['binding'];assert z['source_path']==PATHS[0]and z['source_mention_id']==MID and z['source_surface']=='裴徽'and z['current_person_id']==link['value']==keeper and z['historical_sha256']==link['history_hash']and link['history_value']==OLD
 assert not any(x['id']=='ic-jin035-hui-sgz'for x in b['annotation']['unresolved_identity_cases'])
 resolved=next(x for x in b['annotation']['source_reading_cases']if x['id']=='ic-jin035-hui-sgz');assert resolved['person_id']==keeper and resolved['identity_decision_id']==DID and 'candidate_person_ids'not in resolved
 return True
class PeiHuiIdentity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.s=state(ROOT)
 def bad(self,fn):
  x=copy.deepcopy(self.s);fn(x)
  with self.assertRaises((AssertionError,KeyError,StopIteration)):valid(x)
 def test_complete_source_roles_and_two_current_bindings(self):self.assertTrue(valid(self.s))
 def test_wrong_active_identity_rejected(self):self.bad(lambda s:s['decision'].update(person_id='a28_f5c_105'))
 def test_wrong_current_projection_even_if_active_rejected(self):self.bad(lambda s:s['links'][0].update(value='a28_f5c_105'))
 def test_source_participant_change_rejected(self):self.bad(lambda s:anchor(s['chapters'][0],MID)[0].update(text=anchor(s['chapters'][0],MID)[0]['text'].replace('與傅嘏談','與別人談')))
 def test_wrong_office_and_child_context_rejected(self):self.bad(lambda s:anchor(s['chapters'][1],'c-jinshu-035-peikai-family:p001:m0006')[0].update(text='另一父徽、另一官職'))
 def test_primary_raw_or_offset_drift_rejected(self):
  self.bad(lambda s:s.update(raw=s['raw']+b' '));self.bad(lambda s:s['review']['parallel_primary']['bridge_fragments'][0].update(raw_start=0))
 def test_false_image_or_native_chapter_claim_rejected(self):
  self.bad(lambda s:s['review']['parallel_primary'].update(image_verified=True));self.bad(lambda s:s['review']['parallel_primary'].update(native_chapter_id='c-fake-023'))
 def test_historical_base_hash_and_value_rejected_if_changed(self):
  self.bad(lambda s:s['links'][0].update(history_hash='0'*64));self.bad(lambda s:s['links'][0].update(history_value=s['decision']['person_id']))
 def test_retirement_query_and_allocator(self):
  from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
  from scripts.person_bundle import bundle,load_catalog
  retired=retired_person_ids(ROOT);self.assertIn(OLD,retired);self.assertTrue(allocation_conflicts(OLD+'_A',retired))
  with self.assertRaises((ValueError,KeyError)):bundle(OLD,root=ROOT,catalog=load_catalog(ROOT))
  for directory in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/directory/(OLD+'.json')).exists())
 def test_exact_prior_case_and_historical_pointer_values(self):
  q=J(ROOT/BASE/'historical-qualification.json');self.assertEqual(H((ROOT/BASE/'prior-case.json').read_bytes()),q['prior_case_sha256']);cache={}
  for row in q['qualified_pointers']:
   cache.setdefault(row['path'],(ROOT/row['path']).read_bytes());self.assertEqual(H(cache[row['path']]),row['file_sha256']);self.assertEqual(get(json.loads(cache[row['path']]),row['pointer']),OLD)
if __name__=='__main__':unittest.main()
