import unittest,json,tempfile,shutil,copy
from pathlib import Path
from scripts.classic_quote_identification import validate,PREFIX
ROOT=Path(__file__).resolve().parents[1]
class ClassicQuoteEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.r=Path(self.temp.name)
  paths=['registry/works.json','registry/work-provenance.json','corpus/sanguozhi/022-chenqun-chentai.json']
  paths += [str(p.relative_to(ROOT))for p in (ROOT/PREFIX).glob('*')if p.is_file()]
  for path in paths:
   dest=self.r/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/path,dest)
 def mutate(self,rel,fn):
  p=self.r/rel;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d,ensure_ascii=False))
 def reject(self):
  with self.assertRaises((AssertionError,KeyError,StopIteration)):validate(self.r)
 def test_five_comparisons_six_units_three_titles(self):self.assertEqual(validate(self.r),{'comparisons':5,'witnesses':6,'identified_titles':3})
 def test_source_quote_coshift_rejected(self):
  def shift(d):d[0]['source']['start']+=1;d[0]['source']['end']+=1
  self.mutate(PREFIX+'/quote-comparisons.json',shift);self.reject()
 def test_target_span_shift_rejected(self):
  self.mutate(PREFIX+'/quote-comparisons.json',lambda d:d[0]['targets'][0].__setitem__('start',d[0]['targets'][0]['start']+1));self.reject()
 def test_fixed_raw_misrepresentation_rejected(self):
  self.mutate(PREFIX+'/witnesses.json',lambda d:d[0].__setitem__('fixed_revision_raw_downloaded',True));self.reject()
 def test_pei_commentary_layer_rejected(self):
  self.mutate(PREFIX+'/quote-comparisons.json',lambda d:d[-1]['source'].__setitem__('text_layer','received_body'));self.reject()
 def test_discontinuous_loci_cannot_be_one_exact_quote(self):
  self.mutate(PREFIX+'/quote-comparisons.json',lambda d:d[1].__setitem__('match_type','exact_after_punctuation_only'));self.reject()
 def test_unreported_character_fold_rejected(self):
  self.mutate(PREFIX+'/quote-comparisons.json',lambda d:d[0]['correspondences'][0].__setitem__('character_differences',[]));self.reject()
 def test_metadata_and_public_title_must_agree(self):
  self.mutate('registry/work-provenance.json',lambda d:d['works']['w-yi-sgz022-reference'].__setitem__('citation_title','尚書'));self.reject()
 def test_different_poem_cannot_replace_actual_quotation(self):
  self.mutate(PREFIX+'/quote-comparisons.json',lambda d:d[2].__setitem__('targets',copy.deepcopy(d[3]['targets'])));self.reject()
 def test_primary_reference_must_resolve(self):
  self.mutate('registry/work-provenance.json',lambda d:d['references'].pop('ref-sgz022-classic-shijing-yi'));self.reject()
if __name__=='__main__':unittest.main()
