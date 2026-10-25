"""Current projection endpoints cannot resurrect any family/identity's retired IDs."""
from pathlib import Path
import json,hashlib,copy,unittest
from scripts.retired_person_ids import retired_person_ids
R=Path(__file__).resolve().parents[1]
J=lambda p:json.loads(p.read_text())
H=lambda b:hashlib.sha256(b).hexdigest()
def get(v,p):
 for k in p.split('/')[1:]:v=v[int(k)]if isinstance(v,list)else v[k.replace('~1','/').replace('~0','~')]
 return v
def scan(root,replacements=None):
 root=Path(root);replacements=replacements or{};retired=retired_person_ids(root);rows=J(root/'source-evidence/wangxiong-family-assembly/capture-qualification.json')['historical_files'];fail=[];loaded={}
 indexed={x['current_projection']for x in rows if x.get('current_projection')};actual={str(p.relative_to(root))for p in(root/'source-evidence/wangxiong-family-assembly/current-projections').rglob('*.json')};assert indexed==actual and indexed
 for row in rows:
  rel=row.get('current_projection')
  if not rel:continue
  d=copy.deepcopy(replacements[rel])if rel in replacements else J(root/rel);loaded[rel]=d
  assert d['record_type']=='current_identity_endpoint_projection'and d['current_family_id']=='family-langye-wang-xiong-core'
  assert d['historical_file']==row['path']and d['historical_sha256']==row['sha256']==H((root/row['path']).read_bytes())
  assert d['person_aliases_created']is False
  protected={x['projection_pointer']:x for x in d['protected_historical_capture_values']}
  expected={'/records'+p for p in row.get('protected_capture_pointers',[])};assert set(protected)==expected
  for ptr,q in protected.items():
   assert q['original_pointer']==ptr[len('/records'):];assert get(d,ptr)==get(J(root/row['path']),q['original_pointer'])
   assert H(json.dumps(get(d,ptr),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==q['json_value_sha256']
   original=next(x for x in row['protected_values']if x['pointer']==q['original_pointer']);assert original['json_value_sha256']==q['json_value_sha256']
  def walk(v,p=''):
   if p in protected:return
   if isinstance(v,dict):
    for k,x in v.items():
     pp=p+'/'+k.replace('~','~0').replace('/','~1')
     if k in retired:fail.append((rel,pp,k))
     walk(x,pp)
   elif isinstance(v,list):
    for i,x in enumerate(v):walk(x,p+'/'+str(i))
   elif isinstance(v,str)and v in retired:fail.append((rel,p,v))
  walk(d)
 # Public, source-bound qualification supplements EU's own M8 receipt.
 qref='source-evidence/wangxiong-family-assembly/prior-retirement-endpoint-qualification.json';public=J(root/qref)
 assert public['record_type']=='prior_retirement_current_endpoint_qualification'and public['family_id']=='family-langye-wang-xiong-core'and public['person_aliases_created']is False
 people={p['id']for p in J(root/'registry/persons.json')['persons']};sources={};history={};receipts={};seen=set()
 for entry in public['entries']:
  rel=entry['current_projection_path'];assert rel in loaded and rel not in seen;seen.add(rel);d=loaded[rel];assert d['prior_retirement_qualification_ref']==qref
  assert entry['historical_file']==d['historical_file']and entry['historical_sha256']==d['historical_sha256']==H((root/entry['historical_file']).read_bytes())
  history.setdefault(entry['historical_file'],J(root/entry['historical_file']))
  protected={x['projection_pointer']for x in d['protected_historical_capture_values']}
  for b in entry['bindings']:
   ptr=b['current_pointer'];assert ptr=='/records'+b['historical_pointer']and not any(ptr==p or ptr.startswith(p+'/')for p in protected)
   old=get(history[entry['historical_file']],b['historical_pointer']);assert old in retired and old not in people
   receipts.setdefault(b['retirement_receipt'],J(root/b['retirement_receipt']));receipt=receipts[b['retirement_receipt']]
   assert H((root/b['retirement_receipt']).read_bytes())==b['retirement_receipt_sha256']and receipt['person_aliases_created']is False and old in receipt.get('retired_person_ids',receipt.get('historical_rekey_mapping',{}))
   sources.setdefault(b['source_path'],J(root/b['source_path']));source=sources[b['source_path']];assert source['id']==b['source_chapter_id']
   m=next(m for p in source['paragraphs']for m in p['mentions']if m['id']==b['source_mention_id']);assert m['surface']==b['source_surface']and m['person_id']==b['current_person_id']and m['person_id']in people and m['person_id']not in retired
   if 'historical_rekey_mapping'in receipt:assert receipt['historical_rekey_mapping'][old]==m['person_id']
   value=get(d,ptr)
   if value!=m['person_id']:fail.append((rel,ptr,value))
 return fail
class CurrentProjectionRetirementGuard(unittest.TestCase):
 def test_all_current_projections_reject_retired_ids(self):self.assertEqual(scan(R),[])
 def test_cross_family_current_endpoint_rollback_rejected(self):
  # Two different shapes: candidate-ledger list and current identity person scalar.
  checks=[('source-evidence/wangxiong-family-assembly/current-projections/jin008077/facts-reading-ledger.json','/records/records/45/mentioned_person_ids/0','326_faf_cd3'),('source-evidence/wangxiong-family-assembly/current-projections/shan-family-assembly/current-source-projections/jin035-pei-source-reading/identity-review.json','/records/77/person_id','537_48d_739')]
  for rel,p,old in checks:
   d=J(R/rel);ks=p.split('/')[1:];v=d
   for k in ks[:-1]:v=v[int(k)]if isinstance(v,list)else v[k]
   k=ks[-1];v[int(k)if isinstance(v,list)else k]=old
   self.assertIn((rel,p,old),scan(R,{rel:d}))
 def test_protected_capture_hash_is_not_a_blanket_exemption(self):
  rows=J(R/'source-evidence/wangxiong-family-assembly/capture-qualification.json')['historical_files'];row=next(x for x in rows if x.get('current_projection')and x.get('protected_capture_pointers'));rel=row['current_projection'];d=J(R/rel);q=d['protected_historical_capture_values'][0];v=get(d,q['projection_pointer'])
  if isinstance(v,list):v.append({'not_original_capture':True})
  else:v['not_original_capture']=True
  with self.assertRaises(AssertionError):scan(R,{rel:d})

 def test_wrong_active_current_endpoint_is_rejected_by_public_source_binding(self):
  q=J(R/'source-evidence/wangxiong-family-assembly/prior-retirement-endpoint-qualification.json');entry=q['entries'][0];b=entry['bindings'][0];rel=entry['current_projection_path'];d=J(R/rel)
  people={p['id']for p in J(R/'registry/persons.json')['persons']};wrong=next(pid for pid in sorted(people)if pid!=b['current_person_id']);self.assertNotIn(wrong,retired_person_ids(R));ks=b['current_pointer'].split('/')[1:];v=d
  for k in ks[:-1]:v=v[int(k)]if isinstance(v,list)else v[k]
  k=ks[-1];v[int(k)if isinstance(v,list)else k]=wrong
  self.assertIn((rel,b['current_pointer'],wrong),scan(R,{rel:d}))
