import copy,hashlib,json,sys,tempfile,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.fixed_wuyingdian_song044 import validate_source,source_errors,BASE
class WuyingdianSong044Tests(unittest.TestCase):
 def setUp(self):self.chapter=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_text())
 def test_complete_projection_and_future_person_markup(self):
  self.assertTrue(validate_source(self.chapter,ROOT));self.assertEqual(source_errors(self.chapter,ROOT),[])
  self.chapter['paragraphs'][0]['mentions']=[{'id':'future-mid','start':0,'end':2,'surface':'謝晦','kind':'person','person_id':'new_mutable_identity'}]
  self.assertTrue(validate_source(self.chapter,ROOT)) # source-only; ordinary mention validator remains responsible
 def test_bad_input_and_source_dimensions(self):
  for value in [None,[], 'bad']:
   with self.subTest(value=value):self.assertTrue(source_errors(value,ROOT))
  for key in ['id','work_id','book_id','source_id']:
   c=copy.deepcopy(self.chapter);c[key]='wrong';self.assertTrue(source_errors(c,ROOT))
 def test_source_qualifiers_cannot_claim_original_pdf_or_siku(self):
  for key,value in [('edition','四庫本'),('revision_id',None),('image_verified',True)]:
   c=copy.deepcopy(self.chapter);c['source'][key]=value;self.assertTrue(source_errors(c,ROOT))
  c=copy.deepcopy(self.chapter);c['source']['received_transcription_witness']['original_pdf_locally_obtained']=True;self.assertTrue(source_errors(c,ROOT))
  c=copy.deepcopy(self.chapter);c['source']['received_transcription_witness']['reported_pdf_sha1']='bad';self.assertTrue(source_errors(c,ROOT))
 def test_accepted_glyph_and_printed_notice_cannot_merge(self):
  for key,value in [('accepted_reading','邈'),('placeholder_is_source_glyph',True),('start',0)]:
   c=copy.deepcopy(self.chapter);c['source']['normalization']['editorial_readings'][0][key]=value;self.assertTrue(source_errors(c,ROOT))
  for key,value in [('estimated_missing_characters',6),('notice_in_main_text',True)]:
   c=copy.deepcopy(self.chapter);c['source']['normalization']['missing_text_markers'][0][key]=value;self.assertTrue(source_errors(c,ROOT))
 def test_paragraph_order_text_layer_and_character_position(self):
  for mutate in [lambda c:c['paragraphs'].reverse(),lambda c:c['paragraphs'][0].update(text='改'+c['paragraphs'][0]['text'][1:]),lambda c:c['paragraphs'][-1].update(text_layer='witness_appended_qing_siku_collation'),lambda c:c['paragraphs'][0]['source_position'].update(first_line=2)]:
   c=copy.deepcopy(self.chapter);mutate(c);self.assertTrue(source_errors(c,ROOT))
 def _mutated_file(self,name,mutate):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);target=root/BASE;target.mkdir(parents=True)
   for path in (ROOT/BASE).iterdir():
    if path.is_file():(target/path.name).write_bytes(path.read_bytes())
   f=target/name;j=json.loads(f.read_text());mutate(j);f.write_text(json.dumps(j,ensure_ascii=False))
   self.assertTrue(source_errors(self.chapter,root))
 def test_page_side_physical_column_and_letter_tampering_rejected(self):
  for key,value in [('pdf_page',99),('side','right'),('physical_column_from_right_1based',1),('main_character_range',[2,22])]:
   self._mutated_file('image-column-locations.json',lambda j,k=key,v=value:j['column_coordinates'][0].update({k:v}))
 def test_raw_runs_reordered_or_changed_rejected(self):
  self._mutated_file('transcription-projection.json',lambda j:j['units'][0]['raw_runs'].reverse())
  self._mutated_file('transcription-projection.json',lambda j:j['units'][0]['raw_runs'][0].update(raw_start=1))
 def test_direct_flat_import_and_module_import(self):
  script="import json,sys;from pathlib import Path;from fixed_wuyingdian_song044 import validate_source;r=Path(sys.argv[1]);assert validate_source(json.loads((r/'corpus/songshu/044-wyd1739.json').read_text()),r)"
  result=subprocess.run([sys.executable,'-c',script,str(ROOT)],cwd=ROOT/'scripts',capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)
  result=subprocess.run([sys.executable,'-c',"from scripts.fixed_wuyingdian_song044 import validate_source;assert callable(validate_source)"],cwd=ROOT,capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)
if __name__=='__main__':unittest.main()
