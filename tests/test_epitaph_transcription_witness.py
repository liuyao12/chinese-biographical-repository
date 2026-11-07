import unittest,json,copy,tempfile,shutil
from pathlib import Path
from scripts.epitaph_transcription_witness import errors
ROOT=Path(__file__).resolve().parents[1]
class ModernEpitaphWitness(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'corpus/epitaph-wangminzhi/full.json').read_text());cat=json.loads((ROOT/'registry/works.json').read_text());self.works={w['id']:w for w in cat['works']};self.books={b['id']:b for w in cat['works']for b in w['books']}
  self.temp=tempfile.TemporaryDirectory(prefix='cbr-epitaph-witness-test-');self.r=Path(self.temp.name);p=self.r/'source-evidence/wangminzhi-epitaph-ntu2009';p.parent.mkdir();shutil.copytree(ROOT/'source-evidence/wangminzhi-epitaph-ntu2009',p)
 def tearDown(self):self.temp.cleanup()
 def check(self):return errors(self.c,self.r,self.works,self.books)
 def mutate_file(self,key,fn):
  p=self.r/self.c['source']['transcription_witness'][key];d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d,ensure_ascii=False))
 def test_actual_complete_source_valid(self):self.assertEqual(self.check(),[])
 def test_old_chapters_not_reinterpreted(self):self.assertEqual(errors({'source':{},'paragraphs':[{'text':'某'}]},self.r,{},{}),[])
 def test_fabricated_web_revision_rejected(self):self.c['source']['revision_id']=12345;self.assertTrue(self.check())
 def test_original_image_overclaim_rejected(self):self.c['source']['image_verified']=True;self.assertTrue(self.check())
 def test_rubbing_access_overclaim_rejected(self):self.c['source']['transcription_witness']['underlying_rubbing_personally_accessed']=True;self.assertTrue(self.check())
 def test_fake_original_volume_one_rejected(self):self.books[self.c['book_id']]['number']=1;self.assertTrue(self.check())
 def test_not_an_epitaph_work_rejected(self):self.works[self.c['work_id']]['work_type']='dynastic_history';self.assertTrue(self.check())
 def test_silent_variant_emendation_rejected(self):self.c['paragraphs'][0]['text']=self.c['paragraphs'][0]['text'].replace('冶民','冾民');self.assertTrue(self.check())
 def test_modern_footnote_in_body_rejected(self):self.c['paragraphs'][0]['text']+='（註二）';self.assertTrue(self.check())
 def test_missing_character_anchor_rejected(self):self.mutate_file('span_path',lambda d:d['character_anchors'].pop());self.assertTrue(self.check())
 def test_wrong_character_offset_rejected(self):self.mutate_file('span_path',lambda d:d['character_anchors'][0].update(offset_in_span=99));self.assertTrue(self.check())
 def test_unconsumed_visible_glyph_rejected(self):self.mutate_file('span_path',lambda d:d['upper_transcription_only'].append({'text':'某','x':0,'y':0}));self.assertTrue(self.check())
 def test_exterior_evidence_path_rejected(self):self.c['source']['transcription_witness']['transcription_path']='source-evidence/../../outside.json';self.assertTrue(self.check())
 def test_another_root_does_not_read_global_evidence(self):self.assertTrue(errors(self.c,self.r/'empty',self.works,self.books))
 def test_wrong_page_rejected(self):self.c['source']['transcription_witness']['printed_page']=40;self.assertTrue(self.check())
 def test_pdf_hash_disagreement_rejected(self):self.c['source']['transcription_witness']['pdf_sha256']='0'*64;self.assertTrue(self.check())
 def test_received_history_layer_rejected(self):self.c['paragraphs'][0]['text_layer']='received_chapter';self.assertTrue(self.check())
 def test_modern_article_scope_rejected(self):self.c['source']['text_scope']='complete_modern_article';self.assertTrue(self.check())
 def test_claimed_pdf_payload_rejected(self):self.mutate_file('metadata_path',lambda d:d.update(copied_pdf=True));self.assertTrue(self.check())
 def test_epitaph_cannot_drop_witness_contract(self):
  self.c['source'].pop('transcription_witness');self.c['paragraphs'][0]['text_layer']='received_chapter';self.assertTrue(self.check())
 def test_mismatched_publisher_entry_rejected(self):self.c['source']['url']='https://example.org/other';self.assertTrue(self.check())
 def test_actual_mixed_numbered_and_epitaph_profile_occurrences(self):
  from scripts.person_bundle import load_catalog,bundle
  from scripts.profile_occurrence_counts import profile_occurrences
  catalog=load_catalog(ROOT);chapters={}
  for c in catalog[1]:
   if c.get('record_type')=='marked_chapter':
    book=self.books[c['book_id']];chapters[c['id']]={'number':book['number'],'title':c['title']}
  binid=next(m['person_id']for m in self.c['paragraphs'][0]['mentions']if m['surface']=='彬')
  b=bundle(binid,ROOT,True,catalog=catalog)
  occurrences=profile_occurrences(b,chapters,{k:w['title']for k,w in self.works.items()})
  one=[r for r in occurrences if r['chapter_id']==self.c['id']]
  self.assertEqual(len(one),1);self.assertIsNone(one[0]['number']);self.assertEqual(one[0]['mention_ids'],[m['id']for m in self.c['paragraphs'][0]['mentions']if m.get('person_id')==binid])
  self.assertTrue(any(r['number']==76 for r in occurrences))
if __name__=='__main__':unittest.main()
