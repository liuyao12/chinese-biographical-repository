from pathlib import Path
import unittest,json,hashlib,copy
from scripts.fixed_wuyingdian_song051_family_phase import source_errors
R=Path(__file__).resolve().parents[1]; B='source-evidence/song051-wyd1739-zongshi/'
class SixGlyphSource(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.ch=json.loads((R/'corpus/songshu/051-wyd1739.json').read_bytes());c.receipt=json.loads((R/(B+'six-glyph-image-correction.json')).read_bytes())
 def test_exact_six_codepoints_no_other_source_or_positions(self):
  old=(R/self.receipt['before_transcription_path']).read_bytes();zhi=json.loads((R/(B+'zhi-glyph-image-correction.json')).read_bytes());new=(R/zhi['before_transcription_path']).read_bytes();lines=old.decode().splitlines(keepends=True)
  self.assertEqual(len(self.receipt['changes']),6)
  for e in self.receipt['changes']:
   i=e['raw_line']-1;j=e['raw_character_0based'];self.assertEqual(lines[i][j],e['before']);lines[i]=lines[i][:j]+e['after']+lines[i][j+1:]
   p=next(p for p in self.ch['paragraphs']if p['id']==e['paragraph_id']);self.assertEqual(p['text'][e['start']:e['end']],e['after'])
  self.assertEqual(''.join(lines).encode(),new);self.assertEqual(source_errors(self.ch,R),[])
 def test_precise_wrong_glyph_or_metadata_rejected(self):
  for e in self.receipt['changes']:
   ch=copy.deepcopy(self.ch);p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);p['text']=p['text'][:e['start']]+e['before']+p['text'][e['end']:];self.assertTrue(source_errors(ch,R))
  for key,val in [('raw_sha256','0'*64),('image_verified',True)]:
   ch=copy.deepcopy(self.ch);ch['source'][key]=val;self.assertTrue(source_errors(ch,R))
 def test_printed_unusual_words_retained_no_invented_date(self):
  ps={p['id'].split(':')[-1]:p['text']for p in self.ch['paragraphs']};self.assertIn('昇平三年',ps['p019']);self.assertIn('豫章江二州',ps['p027']);self.assertIn('蕭氏舅也',ps['p027']);self.assertFalse(self.receipt['human_reviewed']);self.assertFalse(self.receipt['image_verified'])
 def test_historical_ledger_and_qualification_exact(self):
  q=json.loads((R/(B+'seven-glyph-historical-qualification.json')).read_bytes())
  for e in q['historical_files']:self.assertEqual(hashlib.sha256((R/e['path']).read_bytes()).hexdigest(),e['sha256'])
  p=json.loads((R/(B+'daogui-reading-ledger-six-glyph-current.json')).read_bytes())['snapshot_projection_qualification'];self.assertEqual(hashlib.sha256((R/p['original_snapshot_path']).read_bytes()).hexdigest(),p['original_snapshot_sha256'])
if __name__=='__main__':unittest.main()
