import json,hashlib,unittest,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P='source-evidence/sanguozhi019-full-title-resolution/'
def verify(j):
 for s in j['evidence']['sources.json']['sources']:
  b=(R/s['path']).read_bytes()
  if hashlib.sha256(b).hexdigest()!=s['sha256']:return False
 for a in j['evidence']['exact-anchors.json']['raw_anchors']:
  if (R/a['raw_path']).read_text()[a['raw_start']:a['raw_end']]!=a['quote']:return False
 return True
class FullTitleEvidence(unittest.TestCase):
 def setUp(self):self.j=json.loads((R/P/'review.json').read_text())
 def test_fixed_raw_hashes_and_spans(self):self.assertTrue(verify(self.j));self.assertEqual(len(self.j['evidence']['sources.json']['sources']),4)
 def test_wrong_offset_rejected(self):
  self.j['evidence']['exact-anchors.json']['raw_anchors'][0]['raw_start']+=1;self.assertFalse(verify(self.j))
 def test_wrong_raw_sha_rejected(self):
  self.j['evidence']['sources.json']['sources'][0]['sha256']='0'*64;self.assertFalse(verify(self.j))
 def test_annotations_current_and_sources_unchanged(self):
  c=json.loads((R/'corpus/sanguozhi/019-yangxiu.json').read_text());m=next(m for p in c['paragraphs']for m in p['mentions']if m['id'].endswith('p002:m1033'))
  self.assertEqual(m['work_id'],'w-lushichunqiu-sgz019-reference');self.assertEqual(m['surface'],'吕氏');self.assertNotIn('work_reference_resolution',m)
  r=next(x for x in c['annotation']['work_reference_reviews'][0]['source_authorship_not_typed']if x['surface'].startswith('對鶡'))
  self.assertIn('李善',r['reason']);self.assertNotIn('辭作而不獻不等於已作成',r['reason'])
