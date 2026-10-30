"""Portable exact-witness/source-layer regressions; no private path or remote fetch."""
from tests.portable_fixture_copy import fixture_copy2
import unittest,json,hashlib,copy,tempfile,shutil
from pathlib import Path
from scripts.witness_projection import repository_positions
Q=Path(__file__).parent/'fixtures/houhan009_early'
class Houhan009EarlySource(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);shutil.copytree(Q,self.root,dirs_exist_ok=True, copy_function=fixture_copy2);self.c=json.loads((self.root/'chapter.json').read_text());self.raw=(self.root/'fixed-witness.txt').read_bytes();self.lines=self.raw.decode().splitlines();self.proj=json.loads((self.root/'source-evidence/houhan009-xiandi-projection.json').read_text())
 def project(self,p=None):return repository_positions(self.root,p or self.c['paragraphs'][0],self.lines)
 def write(self):(self.root/'source-evidence/houhan009-xiandi-projection.json').write_text(json.dumps(self.proj,ensure_ascii=False))
 def test_all_nineteen_exact_projections_and_mentions(self):
  self.assertEqual(len(self.c['paragraphs']),19);seen=set()
  for p in self.c['paragraphs']:
   pts,digest=self.project(p);self.assertEqual(digest,hashlib.sha256(self.raw).hexdigest());self.assertFalse(seen.intersection(pts));seen.update(pts)
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
  expected={(n,i)for n in range(13,67)if not self.lines[n-1].startswith('<pb:')for i,ch in enumerate(self.lines[n-1])if not ch.isspace()and ch not in '¶/()'};self.assertEqual(seen,expected)
 def test_body_tang_song_partition(self):
  from collections import Counter
  self.assertEqual(Counter(p['source_position']['source_layer']for p in self.c['paragraphs']),{'received_annal':2,'lixian_commentary':16,'liu_ban_collation':1})
 def test_no_book_title_person_false_positive(self):
  for p in self.c['paragraphs']:
   for term in ['獻帝起居注','帝王紀']:
    a=p['text'].find(term)
    if a>=0:self.assertFalse(any(m['start']<a+len(term)and m['end']>a for m in p['mentions']))
 def test_one_whitewave_identity_distinct_from_linzong(self):
  p=next(p for p in self.c['paragraphs']if '黄巾郭泰' in p['text']);m=next(m for m in p['mentions']if m['surface']=='郭泰');self.assertEqual(m['person_id'],'zni_5qt_ep7');self.assertNotEqual(m['person_id'],'89b_78c_9d5')
 def test_homonymous_emperors_are_not_nearest_emperor(self):
  p=next(p for p in self.c['paragraphs']if p['source_position']['unit_key']=='chuping01-note-08-1');a={m['surface']:m['person_id']for m in p['mentions']};self.assertEqual(a['安帝'],'7zd_hi5_fwe');self.assertNotEqual(a['安帝'],'s6y_280_81r');self.assertEqual(a['順帝'],a['敬宗'])
 def test_wrong_fixed_raw_sha_rejected(self):
  p=copy.deepcopy(self.c['paragraphs'][0]);p['source_position']['raw_file_sha256']='0'*64
  with self.assertRaises(ValueError):self.project(p)
 def test_changed_raw_character_rejected(self):
  r=self.proj['units'][0]['raw_runs'][0];n=r['raw_line']-1;a=r['raw_start'];self.lines[n]=self.lines[n][:a]+'錯'+self.lines[n][a+1:]
  with self.assertRaises(ValueError):self.project()
 def test_wrong_offset_rejected(self):
  self.proj['units'][0]['raw_runs'][0]['start']=1;self.write()
  with self.assertRaises(ValueError):self.project()
 def test_duplicate_unit_rejected(self):
  self.proj['units'].append(copy.deepcopy(self.proj['units'][0]));self.write()
  with self.assertRaises(ValueError):self.project()
 def test_forged_unit_text_rejected(self):
  self.proj['units'][0]['text']='錯';self.write()
  with self.assertRaises(ValueError):self.project()
if __name__=='__main__':unittest.main()
