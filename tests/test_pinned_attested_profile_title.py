"""Pinned complete role source-use, distinct from a grant and from a bare label."""
import json,copy,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.profile_title_preferences import resolve,PreferenceCatalog,choice
from scripts.received_career_roles import holding_valid
from scripts import attached_biography_frames as frames
ROOT=Path(__file__).resolve().parents[1]
def fixture():
 c=json.loads((ROOT/'corpus/weishu-weishou/024-cuixuanbo.json').read_text());h=next(h for h in json.loads((ROOT/'corpus/weishu-weishou/024-cuixuanbo-titles.json').read_text())['holdings']if h['id']=='th-cui53-f036');pref=json.loads((ROOT/'corpus/weishu-weishou/024-cuiyue-profile-title.json').read_text());d,=pref['decisions'];people={m['person_id']:dict(id=m['person_id'])for p in c['paragraphs']for m in p['mentions']if m['kind']=='person'};return[c,dict(record_type='title_holding_assertion_set',holdings=[h]),pref],people,h,d,c
class PinnedSourceUse(unittest.TestCase):
 def test_source_use_not_a_grant_or_period(self):
  rows,people,h,d,c=fixture();self.assertTrue(holding_valid(h,c,root=ROOT));v=resolve(rows,people,ROOT)[h['person_id']];self.assertEqual(v['mode'],'attestation');self.assertEqual(v['title'],'關内侯');self.assertEqual(h['effective_period'],dict(start=dict(status='unknown',date_expression=None,evidence=[]),end=dict(status='unknown',date_expression=None,evidence=[])))
 def test_wrong_owner_and_nearest_other_role_rejected(self):
  for change in('holder_only','source_role','whole_role_swap'):
   rows,people,h,d,c=fixture();p=c['paragraphs'][0];owner=next(m for m in p['mentions']if m['id']==d['source_ref']['person_mention_id']);other=next(m for m in p['mentions']if m['start']==27)
   if change=='holder_only':h['person_id']=other['person_id'];d['person_id']=other['person_id']
   elif change=='source_role':h['source_career_role']['recipient_role']='r4'
   else:
    owner['person_id']=other['person_id'];h['person_id']=other['person_id'];d['person_id']=other['person_id']
   self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_forged_grant_date_and_missing_coverage(self):
  for change in('grant','date','missing_role','wrong_offset'):
   rows,people,h,d,c=fixture()
   if change=='grant':h['mode']='grant'
   elif change=='date':h['effective_period']['start']=dict(status='source_event',event_type='grant',date_expression='建興元年',evidence=h['evidence'])
   elif change=='missing_role':h['source_career_role']['roles'].pop('r4')
   else:h['source_career_role']['fields']['career_0']['start']+=1
   self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_bare_legacy_or_stripped_pin_cannot_be_selected(self):
  rows,people,h,d,c=fixture();h.pop('source_career_role');self.assertRaises(ValueError,resolve,rows,people,ROOT)
  rows,people,h,d,c=fixture();key=h['source_career_role']['frame'];r=copy.deepcopy(frames.RECIPES[key]);r.pop('source_pin')
  with patch.dict(frames.RECIPES,{key:r}):self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_raw_map_metadata_and_cropped_body_rejected(self):
  for change in('rawhash','revision','map','quote'):
   rows,people,h,d,c=fixture()
   if change=='rawhash':c['source']['raw_file_sha256']='0'*64
   elif change=='revision':c['source']['revision_id']='other-commit'
   elif change=='map':c['paragraphs'][0]['source_position']['raw_character_positions'][0]['column']+=1
   else:h['evidence'][0]['quote']=h['evidence'][0]['quote'][24:41]
   self.assertRaises(ValueError,resolve,rows,people,ROOT)
 def test_root_local_cache_watches_raw_path_and_copies_revalidate(self):
  rows,people,h,d,c=fixture();tx=PreferenceCatalog(rows,people,ROOT);pid=h['person_id'];self.assertEqual(tx.raw_dependencies[pid][0],ROOT/c['source']['raw_path']);self.assertEqual(choice(copy.deepcopy(tx),people,pid,ROOT),choice(tx,people,pid,ROOT))
  copied=copy.deepcopy(tx);copied[1]['holdings'][0]['mode']='grant';self.assertRaises(ValueError,choice,copied,people,pid,ROOT);self.assertRaises(ValueError,choice,tx,people,pid,ROOT.parent/'another-root')
  original=Path.read_bytes;target=(ROOT/c['source']['raw_path']).resolve()
  def changed(p):return b'changed original witness'if p.resolve()==target else original(p)
  with patch.object(Path,'read_bytes',changed):self.assertRaises(ValueError,choice,tx,people,pid,ROOT)
 def test_synthetic_canonical_ids_are_not_whitelisted(self):
  rows,people,h,d,c=fixture();mapping={pid:'synthetic-person-'+str(i)for i,pid in enumerate(people)}
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='person':m['person_id']=mapping[m['person_id']]
  h['person_id']=mapping[h['person_id']];d['person_id']=h['person_id'];synthetic={v:dict(id=v)for v in mapping.values()};self.assertEqual(resolve(rows,synthetic,ROOT)[h['person_id']]['mode'],'attestation')
if __name__=='__main__':unittest.main()
