"""Seven bounded image readings; this is not a global character normalization."""
from pathlib import Path
import copy,json,hashlib,unittest
from scripts import wyd_song051_yixin as y
from scripts import fixed_wuyingdian_song051_family_phase as core
from scripts.person_bundle import validate_full_name
from scripts.name_childhood import validate_childhood_name
from scripts.validation_context import scope
ROOT=Path(__file__).resolve().parents[1];BASE='source-evidence/song051-wyd1739-zongshi/'
class SevenGlyphSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with scope(ROOT):cls.ch,cls.roles,cls.c,cls.docs=y.state(ROOT)
  cls.receipt=json.loads((ROOT/(BASE+'seven-glyph-image-correction.json')).read_bytes());cls.ps={p['id']:p for p in cls.ch['paragraphs']}
 def test_complete_source_seven_exact_positions_and_projection(self):
  current=(ROOT/(BASE+'transcription-columns.txt')).read_bytes();six=json.loads((ROOT/(BASE+'six-glyph-image-correction.json')).read_bytes());raw=(ROOT/six['before_transcription_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),self.receipt['after_transcription_sha256']);zhi=json.loads((ROOT/(BASE+'zhi-glyph-image-correction.json')).read_bytes());six_stage=(ROOT/zhi['before_transcription_path']).read_bytes();self.assertEqual(hashlib.sha256(six_stage).hexdigest(),six['after_transcription_sha256']);self.assertEqual(hashlib.sha256(current).hexdigest(),zhi['after_transcription_sha256']);self.assertEqual(len(self.receipt['changes']),7);self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),598);lines=raw.decode().splitlines()
  for c in self.receipt['changes']:
   p=self.ps[c['paragraph_id']];self.assertEqual(p['text'][c['start']:c['end']],c['after']);self.assertEqual(lines[c['raw_line_1based']-1][c['raw_char_0based']],c['after']);covered=[m for m in p['mentions']if m['start']<=c['start']<m['end']]
   for m in covered:
    row=next(r for r in self.c['markers']if r['role_key'].startswith('yq_')and r['marker']['id']==m['id']);self.assertEqual(m,y.materialize(row['marker'],self.roles))
  self.assertEqual(core.source_errors(self.ch,ROOT),[])
 def test_source_context_flags_or_unaccepted_glyph_change_rejected(self):
  for case in ['undo_glyph','raw','layer','human','model','status','marker','unknown_glyph_cover']:
   ch=copy.deepcopy(self.ch)
   if case=='undo_glyph':c=self.receipt['changes'][0];p=next(p for p in ch['paragraphs']if p['id']==c['paragraph_id']);p['text']=p['text'][:c['start']]+c['before']+p['text'][c['end']:]
   if case=='raw':ch['source']['raw_sha256']='0'*64
   if case=='layer':ch['paragraphs'][45]['text_layer']='received_chapter'
   if case=='human':ch['annotation']['human_reviewed']=True
   if case=='model':ch['annotation']['model']='unreviewed'
   if case=='status':ch['paragraphs'][0]['annotation_status']='complete'
   if case=='marker':ch['paragraphs'][0]['mentions'][0]['person_id']=self.roles['dl_gaozu']
   if case=='unknown_glyph_cover':
    p=next(p for p in ch['paragraphs']if p['id'].endswith(':p035'));p['mentions'].append({'id':p['id']+':synthetic-unknown','kind':'person','person_id':self.roles['yq_yiqing'],'start':178,'end':179,'surface':p['text'][178:179],'status':'contextual_provisional'});p['mentions'].sort(key=lambda m:m['start'])
   self.assertTrue(core.source_errors(ch,ROOT),case)
 def test_historical_snapshots_are_exact_files_not_directory_exemption(self):
  q=json.loads((ROOT/(BASE+'seven-glyph-historical-qualification.json')).read_bytes());self.assertTrue(q['no_directory_or_person_id_exemption']);self.assertTrue(q['historical_files'])
  for e in q['historical_files']:self.assertEqual(hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest(),e['sha256'])
 def test_real_full_name_and_childhood_apis_still_consume_current_raw(self):
  names=self.docs['corpus/songshu/051-wyd1739-daolian-name-components.json']['records']
  with scope(ROOT):
   for n in names:
    p=self.ps[n['paragraph_id']]
    if 'full_name'in n:validate_full_name(n,p,chapter=self.ch,root=ROOT)
    if 'xiaozhi'in n:validate_childhood_name(n,p,chapter=self.ch,root=ROOT)
  self.assertEqual(sum('full_name'in n for n in names),3);self.assertEqual(sum('xiaozhi'in n for n in names),1)
 def test_undecided_words_and_identity_population_not_editorially_filled(self):
  self.assertIn('神暮獨運',self.ps[y.CID+':p028']['text']);self.assertIn('陳豔',self.ps[y.CID+':p005']['text']);self.assertTrue(all(c['before']not in['暮','早','旱','豔']for c in self.receipt['changes']));self.assertFalse(self.receipt['human_reviewed']);self.assertFalse(self.receipt['image_verified']);self.assertIsNone(self.receipt['model'])
if __name__=='__main__':unittest.main()
