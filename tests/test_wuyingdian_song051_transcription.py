import copy,json,unittest,tempfile,shutil
from pathlib import Path
try:
 from scripts.fixed_wuyingdian_song051 import source_errors,BASE
 from scripts.render_corpus import render
except ImportError:
 from fixed_wuyingdian_song051 import source_errors,BASE
 from render_corpus import render
ROOT=Path(__file__).resolve().parents[1]
class Song051(unittest.TestCase):
 def setUp(self):self.c=json.loads((ROOT/'corpus/songshu/051-wyd1739.json').read_text())
 def test_complete_pending_source_and_xml(self):
  self.assertEqual(source_errors(self.c,ROOT),[])
  self.assertEqual(render(self.c),(ROOT/'corpus/songshu/051-wyd1739.xml').read_text())
  self.assertEqual(len(self.c['paragraphs']),48)
  self.assertTrue(all(p['annotation_status']=='pending'and not p['mentions']for p in self.c['paragraphs']))
 def test_wrong_layer_and_missing_binding(self):
  for field in ('layer','binding'):
   c=copy.deepcopy(self.c)
   if field=='layer':c['paragraphs'][-1]['text_layer']='witness_appended_pei_songzhi_note'
   else:del c['annotation']['fixed_transcription_contract']
   self.assertTrue(source_errors(c,ROOT))
 def test_wrong_source_flags_and_glyph(self):
  for field in ('edition','image','pdf','glyph'):
   c=copy.deepcopy(self.c)
   if field=='edition':c['source']['edition']='四庫'
   if field=='image':c['source']['image_verified']=True
   if field=='pdf':c['source']['received_transcription_witness']['original_pdf_locally_obtained']=True
   if field=='glyph':
    p=next(p for p in c['paragraphs']if'〓'in p['text']);p['text']=p['text'].replace('〓','祗')
   self.assertTrue(source_errors(c,ROOT))
 def test_raw_cochange_cannot_repin_itself(self):
  with tempfile.TemporaryDirectory()as t:
   r=Path(t);shutil.copytree(ROOT/BASE,r/BASE)
   p=r/BASE/'transcription-columns.txt';p.write_bytes(b'\n'+p.read_bytes())
   c=copy.deepcopy(self.c)
   import hashlib
   c['source']['raw_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
   self.assertTrue(source_errors(c,r))
 def test_pending_ai_stage_cannot_be_promoted(self):
  for key,value in [('human_reviewed',True),('model','unverified-model'),('status','reviewed')]:
   c=copy.deepcopy(self.c);c['annotation'][key]=value
   self.assertTrue(source_errors(c,ROOT))
  for mutation in ('status','mentions','missing_mentions','missing_status'):
   c=copy.deepcopy(self.c);p=c['paragraphs'][0]
   if mutation=='status':p['annotation_status']='in_progress'
   if mutation=='mentions':p['mentions']=[{'kind':'unresolved','person_id':None}]
   if mutation=='missing_mentions':del p['mentions']
   if mutation=='missing_status':del p['annotation_status']
   self.assertTrue(source_errors(c,ROOT))
 def test_formal_title_only(self):
  self.assertEqual(self.c['title'],'宗室')
  c=copy.deepcopy(self.c);c['title']='宗室（武英殿本卷五十一）'
  self.assertTrue(source_errors(c,ROOT))
 def test_bad_types_and_legacy_non_target(self):
  for c in (None,[],42,'bad'):self.assertTrue(source_errors(c,ROOT))
  self.assertEqual(source_errors({'id':'other','source_id':'other','annotation':{}},ROOT),[])
if __name__=='__main__':unittest.main()
