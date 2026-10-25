from pathlib import Path
import copy,hashlib,json,unittest
R=Path(__file__).resolve().parents[1]
PINS={
 'source-evidence/shan-family-assembly/current-source-projections/jin035-pei-source-reading/native-source-fidelity.json':('/marks/317','242bc2aaa9961b431ecce415d94f140ab4b700762dcbd6b01868f811ee9cdca1'),
 'source-evidence/xunchuo-family-rekey/current-review.json':('/records/8/projection/6','cffff87b7ab8ec2895c8e0169a36529fbe075b1212908f8a35fc80e9e1dbfdca')}
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def value_at(doc,pointer):
 for p in pointer.split('/')[1:]:doc=doc[int(p)]if isinstance(doc,list)else doc[p.replace('~1','/').replace('~0','~')]
 return doc
def qualified(q,docs):
 try:
  if q['historical_revision']!='8898e83ca559f7a14533fff9e144539b648d9bb2' or len(q['items'])!=2 or {i['path']for i in q['items']}!=set(PINS):return False
  for item in q['items']:
   pointer,sha=PINS[item['path']]
   if len(item['old_m0061'])!=1 or len(item['current_m0061'])!=1:return False
   for k in ('old_m0061','current_m0061'):
    s=item[k][0]
    if s['pointer']!=pointer or s['value_sha256']!=sha or digest(s['value'])!=sha or s['value'].get('mention_id')!='c-jinshu-035-peikai-family:p019:m0061':return False
   if item['quoted_sha256']!=item['fixed_commit_sha256'] or item['quoted_sha256']==item['current_sha256']:return False
   if digest(value_at(docs[item['path']],pointer))!=sha:return False
  return True
 except(KeyError,TypeError,ValueError,IndexError):return False
class HistoricalSnapshots(unittest.TestCase):
 def test_fixed_snapshot_pins_and_reject_empty_wrong_pointer_or_changed_value(self):
  q=json.loads((R/'source-evidence/wangxuan-eight-wang-identity/historical-snapshot-qualification.json').read_text());docs={p:json.loads((R/p).read_text())for p in PINS};self.assertTrue(qualified(q,docs))
  bad=copy.deepcopy(q);bad['items']=[];self.assertFalse(qualified(bad,docs))
  for key in ('old_m0061','current_m0061'):
   bad=copy.deepcopy(q);bad['items'][0][key]=[];self.assertFalse(qualified(bad,docs))
  bad=copy.deepcopy(q);bad['items'][0]['current_m0061'][0]['pointer']='/marks/5';self.assertFalse(qualified(bad,docs))
  for path,(pointer,sha)in PINS.items():
   for key,value in [('person_id','35b_mo3_adg'),('end',63),('surface','王玄')]:
    changed=copy.deepcopy(docs);value_at(changed[path],pointer)[key]=value;self.assertFalse(qualified(q,changed))
  # Co-shifted metadata and snapshot hashes still cannot replace the independent pins.
  bad=copy.deepcopy(q);changed=copy.deepcopy(docs);path=bad['items'][0]['path'];pointer=PINS[path][0];value_at(changed[path],pointer)['person_id']='35b_mo3_adg'
  for key in ('old_m0061','current_m0061'):
   bad['items'][0][key][0]['value']=copy.deepcopy(value_at(changed[path],pointer));bad['items'][0][key][0]['value_sha256']=digest(value_at(changed[path],pointer))
  self.assertFalse(qualified(bad,changed))
if __name__=='__main__':unittest.main()
