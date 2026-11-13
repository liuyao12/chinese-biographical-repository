import copy,json,unittest,tempfile,shutil
from pathlib import Path
try:
 from scripts.fixed_wuyingdian_song005_opening import source_errors,BASE
 from scripts.render_corpus import render
except ImportError:
 from fixed_wuyingdian_song005_opening import source_errors,BASE
 from render_corpus import render
ROOT=Path(__file__).resolve().parents[1]
class Song005(unittest.TestCase):
 def setUp(self):
  self.actual=json.loads((ROOT/'corpus/songshu/005-wyd1739-wendi-opening.json').read_text());self.c=self.actual;self.formal_count=None
  if self.actual.get('annotation',{}).get('formal_phase')=='song005_opening_emperor_identity_bridge_phase1':
   from scripts.fixed_wuyingdian_song051_family_phase import source_errors005 as formal_errors
   errors=formal_errors(self.actual,ROOT)
   if errors:raise AssertionError(errors)
   contract=json.loads((ROOT/'source-evidence/song051-wyd1739-zongshi/formal-role-contract.json').read_bytes())
   self.c=copy.deepcopy(contract['song005_opening_bridge']['source_before']);self.formal_count=len(contract['song005_opening_bridge']['markers'])
  self.assertEqual([(p['id'],p['text'],p['source_position'])for p in self.c['paragraphs']],[(p['id'],p['text'],p['source_position'])for p in self.actual['paragraphs']])
 def test_complete_pending_source_and_xml(self):
  self.assertEqual(source_errors(self.c,ROOT),[])
  self.assertEqual(render(self.actual),(ROOT/'corpus/songshu/005-wyd1739-wendi-opening.xml').read_text())
  self.assertEqual(len(self.c['paragraphs']),2)
  self.assertTrue(all(p['annotation_status']=='pending'and not p['mentions']for p in self.c['paragraphs']))
  if self.formal_count is not None:
   self.assertEqual(sum(len(p['mentions'])for p in self.actual['paragraphs']),self.formal_count)
   self.assertTrue(all(p['annotation_status']==('in_progress'if p['mentions']else'pending')for p in self.actual['paragraphs']))
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
    p=c['paragraphs'][0];p['text']=p['text'].replace('京城','京口')
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
  self.assertEqual(self.c['title'],'文帝')
  c=copy.deepcopy(self.c);c['title']='文帝（武英殿本）'
  self.assertTrue(source_errors(c,ROOT))
 def test_volume5_dimension_and_registry_union(self):
  c=copy.deepcopy(self.c);c['book_id']='b-songshu-006'
  self.assertTrue(source_errors(c,ROOT))
  works=json.loads((ROOT/'registry/works.json').read_bytes())
  w=next(w for w in works['works']if w['id']=='w-songshu')
  book,=[b for b in w['books']if b['id']=='b-songshu-005']
  self.assertEqual(book['number'],5)
  self.assertIn(self.c['id'],book['chapter_ids'])
  self.assertIn('c-songshu-005-wendi-annal',book['chapter_ids'])
 def test_bad_types_and_legacy_non_target(self):
  for c in (None,[],42,'bad'):self.assertTrue(source_errors(c,ROOT))
  self.assertEqual(source_errors({'id':'other','source_id':'other','annotation':{}},ROOT),[])
if __name__=='__main__':unittest.main()
