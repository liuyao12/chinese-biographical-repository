from pathlib import Path
import copy,json,hashlib,unittest
R=Path(__file__).resolve().parents[1];Q='source-evidence/wangcheng-eight-wang-identity/protected-capture-successor.json';MID='c-jinshu-035-peikai-family:p019:m0041'
def get(v,p):
 for k in p.split('/')[1:]:v=v[int(k)]if isinstance(v,list)else v[k.replace('~1','/').replace('~0','~')]
 return v
def h(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def check(root,overrides=None):
 overrides=overrides or{}
 def read(rel):return copy.deepcopy(overrides[rel])if rel in overrides else json.loads((root/rel).read_text())
 q=read(Q);rows=q['restored_historical_snapshots'];assert len(rows)==8 and len({(x['path'],x['pointer'])for x in rows})==8
 for x in rows:
  d=read(x['path']);pin=next(p for p in d['protected_historical_capture_values']if p['projection_pointer']==x['pointer']);v=get(d,x['pointer']);assert h(v)==x['historical_json_value_sha256']==pin['json_value_sha256']
  snap=get(d,x['snapshot_mention_pointer']);assert snap['id']==MID and snap['surface']=='王澄'and snap['person_id']=='8sa_o0b_y2i'
  assert x['source_path']=='corpus/jinshu/035-pei-family.json'and x['source_chapter_id']=='c-jinshu-035-peikai-family'and x['source_mention_id']==MID and x['source_surface']=='王澄'
  c=read(x['source_path']);m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']==MID);assert m['person_id']==x['current_person_id']==q['canonical_person_id']and m['surface']=='王澄'
 return True
class ProtectedSnapshots(unittest.TestCase):
 def test_all_eight_historical_values_and_live_source_mid_bindings(self):
  self.assertTrue(check(R));q=json.loads((R/Q).read_text());bad=copy.deepcopy(q);bad['restored_historical_snapshots'][0]['current_person_id']='a8f_ec8_e74_ABC'
  with self.assertRaises(AssertionError):check(R,{Q:bad})
  x=q['restored_historical_snapshots'][0];d=json.loads((R/x['path']).read_text());get(d,x['snapshot_mention_pointer'])['person_id']=q['canonical_person_id']
  with self.assertRaises(AssertionError):check(R,{x['path']:d})
if __name__=='__main__':unittest.main()
