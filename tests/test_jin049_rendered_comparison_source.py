import unittest,json,copy
from pathlib import Path
from scripts.fixed_jin049_jikang_rendered_comparison import validate_source,source_errors,CID,CH
ROOT=Path(__file__).resolve().parents[1]
class Jin049RenderedSource(unittest.TestCase):
 def setUp(self):self.c=json.loads((ROOT/CH).read_bytes())
 def test_complete_capture(self):self.assertTrue(validate_source(self.c,ROOT));self.assertEqual(len(self.c['paragraphs']),17);self.assertEqual(sum(len(p['text'])for p in self.c['paragraphs']),2636)
 def test_capture_not_original_raw(self):
  s=self.c['source'];self.assertIsNone(s['revision_id']);self.assertEqual(s['revision_id_observed_in_navigation'],2199702);self.assertFalse(s['fixed_revision_independently_obtained']);self.assertFalse(s['original_wikitext_obtained']);self.assertEqual(s['witness_role'],'comparison_only')
 def test_source_qualification_drift(self):
  for k,v in [('revision_id',2199702),('edition','武英殿本'),('image_verified',True),('witness_role','preferred'),('capture_sha256','0'*64)]:
   c=copy.deepcopy(self.c);c['source'][k]=v;self.assertTrue(source_errors(c,ROOT),k)
 def test_annotation_and_pending_drift(self):
  for k,v in [('human_reviewed',True),('model','invented'),('status','complete')]:
   c=copy.deepcopy(self.c);c['annotation'][k]=v;self.assertTrue(source_errors(c,ROOT),k)
  c=copy.deepcopy(self.c);base=json.loads((ROOT/'source-evidence/jin049-jikang-rendered-comparison/contract.json').read_bytes());c['annotation']=base['required_annotation'];c['paragraphs']=base['paragraphs'];c['paragraphs'][0]['annotation_status']='in_progress';self.assertTrue(source_errors(c,ROOT))
 def test_mentions_cannot_pretend_ner_done(self):
  c=copy.deepcopy(self.c);c['paragraphs'][0]['mentions']=[{'kind':'person','person_id':'wrong'}];self.assertTrue(source_errors(c,ROOT))
 def test_full_letter_poem_may_not_be_truncated(self):
  for i in [0,3,8,10,13,16]:
   c=copy.deepcopy(self.c);c['paragraphs'][i]['text']=c['paragraphs'][i]['text'][:-1];self.assertTrue(source_errors(c,ROOT))
 def test_wrong_layer_or_position(self):
  for k,v in [('text_layer','witness_appended_pei_songzhi_note'),('id','wrong')]:
   c=copy.deepcopy(self.c);c['paragraphs'][0][k]=v;self.assertTrue(source_errors(c,ROOT))
  c=copy.deepcopy(self.c);c['paragraphs'][0]['captured_source_position']['unit_key']='p002';self.assertTrue(source_errors(c,ROOT))
 def test_wrong_book_and_coshift_owned_path(self):
  c=copy.deepcopy(self.c);c['book_id']='b-jinshu-080';self.assertTrue(source_errors(c,ROOT))
  c=copy.deepcopy(self.c);c['id']='other';c['source_id']='other';c['annotation']['fixed_rendered_capture_contract']='other';self.assertTrue(source_errors(c,ROOT,source_path=ROOT/CH))
 def test_bad_input_rejected(self):
  for c in [None,[],1,'x']:self.assertTrue(source_errors(c,ROOT))
 def test_other_sources_untouched(self):self.assertEqual(source_errors({'id':'other','source_id':'other','annotation':{}},ROOT),[])
if __name__=='__main__':unittest.main()
