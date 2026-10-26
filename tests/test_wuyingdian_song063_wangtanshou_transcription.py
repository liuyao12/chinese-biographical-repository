import copy,json,unittest,tempfile,shutil,hashlib
from pathlib import Path
try:
 from scripts.fixed_wuyingdian_song063_wangtanshou import source_errors,BASE
 from scripts.render_corpus import render
except ImportError:
 from fixed_wuyingdian_song063_wangtanshou import source_errors,BASE
 from render_corpus import render
ROOT=Path(__file__).resolve().parents[1]
class Song063(unittest.TestCase):
 def setUp(self):self.c=json.loads((ROOT/'corpus/songshu/063-wyd1739-wangtanshou.json').read_bytes())
 def test_complete_source_xml_and_scopes(self):
  self.assertEqual(source_errors(self.c,ROOT),[])
  self.assertEqual(render(self.c),(ROOT/'corpus/songshu/063-wyd1739-wangtanshou.xml').read_text())
  self.assertEqual(self.c['title'],'王華 王曇首 殷景仁 沈演之')
  self.assertEqual(len(self.c['paragraphs']),7)
  body=''.join(p['text']for p in self.c['paragraphs']if p['text_layer']=='received_chapter')
  self.assertEqual(len(body),994)
  self.assertTrue(body.startswith('王曇首琅邪臨沂人'))
  self.assertTrue(body.endswith('子僧綽嗣別有傳少子僧虔昇明末為尚書令'))
  self.assertEqual(self.c['paragraphs'][-1]['text_layer'],'witness_appended_wuyingdian_collation')
  self.assertEqual(len(self.c['paragraphs'][-1]['text']),42)
 def test_pending_flags_cannot_be_promoted(self):
  for k,v in [('human_reviewed',True),('model','fake'),('status','reviewed')]:
   c=copy.deepcopy(self.c);c['annotation'][k]=v;self.assertTrue(source_errors(c,ROOT))
  for k,v in [('annotation_status','reviewed'),('mentions',[{'kind':'person','person_id':'invented'}])]:
   c=copy.deepcopy(self.c);c['paragraphs'][0][k]=v;self.assertTrue(source_errors(c,ROOT))
 def test_layers_dimensions_and_title(self):
  for k,v in [('book_id','b-songshu-062'),('work_id','w-jinshu'),('title','王曇首及附敘')]:
   c=copy.deepcopy(self.c);c[k]=v;self.assertTrue(source_errors(c,ROOT))
  c=copy.deepcopy(self.c);c['paragraphs'][-1]['text_layer']='received_chapter';self.assertTrue(source_errors(c,ROOT))
 def test_source_and_missing_binding(self):
  for mutate in ('binding','edition','human','pdf'):
   c=copy.deepcopy(self.c)
   if mutate=='binding':del c['annotation']['fixed_transcription_contract']
   if mutate=='edition':c['source']['edition']='四庫本'
   if mutate=='human':c['source']['image_verified']=True
   if mutate=='pdf':c['source']['received_transcription_witness']['original_pdf_locally_obtained']=True
   self.assertTrue(source_errors(c,ROOT))
 def test_truncation_duplicate_and_glyph(self):
  for mutate in ('drop','duplicate','glyph'):
   c=copy.deepcopy(self.c)
   if mutate=='drop':c['paragraphs'].pop(-2)
   if mutate=='duplicate':c['paragraphs'][1]=copy.deepcopy(c['paragraphs'][0])
   if mutate=='glyph':c['paragraphs'][2]['text']=c['paragraphs'][2]['text'].replace('虛五緯','虛危五緯')
   self.assertTrue(source_errors(c,ROOT))
 def test_coherent_raw_rehash_not_trusted(self):
  with tempfile.TemporaryDirectory()as t:
   r=Path(t);shutil.copytree(ROOT/BASE,r/BASE)
   p=r/BASE/'transcription-columns.txt';p.write_bytes(b'\n'+p.read_bytes());c=copy.deepcopy(self.c)
   c['source']['raw_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();self.assertTrue(source_errors(c,r))
 def test_image_encoded_variants_not_global_normalized(self):
  for before,after in [('慍','愠'),('怏怏','快快')]:
   c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if before in p['text']);p['text']=p['text'].replace(before,after)
   self.assertTrue(source_errors(c,ROOT))
 def test_badtypes_and_legacy_non_target(self):
  for c in (None,[],42,'bad'):self.assertTrue(source_errors(c,ROOT))
  self.assertEqual(source_errors({'id':'other','source_id':'other','annotation':{}},ROOT),[])
if __name__=='__main__':unittest.main()
