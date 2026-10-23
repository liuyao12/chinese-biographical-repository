# coding: utf-8
from pathlib import Path
import copy,json,hashlib,tempfile,unittest
from scripts.fixed_wikisource_units import source_errors
from scripts.fixed_linked_heading_biography import project
R=Path(__file__).resolve().parents[1];CP='corpus/jinshu/034-yanghu.json'
class YanghuCompleteSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.c=json.loads((R/CP).read_text());cls.ref=cls.c['annotation']['fixed_wikisource_unit_ref'];cls.b=json.loads((R/cls.ref).read_text());cls.raw=(R/cls.b['raw_file']).read_text()
 def bad(self,fn):c=copy.deepcopy(self.c);fn(c);self.assertTrue(source_errors(c,R))
 def test_complete_source(self):
  self.assertEqual(source_errors(self.c,R),[]);self.assertEqual(len(self.c['paragraphs']),41);self.assertEqual(sum(len(p['text'])for p in self.c['paragraphs']),6567)
  self.assertTrue(self.c['paragraphs'][-1]['text'].endswith('亮弟陶，為徐州刺史。'))
 def test_missing_family_tail_rejected(self):self.bad(lambda c:c['paragraphs'].pop())
 def test_missing_quoted_line_rejected(self):self.bad(lambda c:c['paragraphs'].pop(7))
 def test_swapped_document_lines_rejected(self):
  def change(c):c['paragraphs'][6],c['paragraphs'][7]=c['paragraphs'][7],c['paragraphs'][6]
  self.bad(change)
 def test_changed_received_glyph_rejected(self):self.bad(lambda c:c['paragraphs'][0].update(text=c['paragraphs'][0]['text'].replace('父道','父衜')))
 def test_projection_offset_rejected(self):self.bad(lambda c:c['paragraphs'][0]['source_position']['raw_character_offsets'].__setitem__(0,0))
 def test_document_is_not_ancient_note(self):
  q=[p for p in self.c['paragraphs']if p['source_position']['quotation_block_markup']];self.assertEqual(len(q),8);self.assertTrue(all(p['source_position']['source_layer']=='received_biography'for p in q))
 def test_received_anomalies_preserved(self):
  s=''.join(p['text']for p in self.c['paragraphs']);self.assertIn('初，祐以',s);self.assertIn('孫皓孫恣情任意',s);self.assertIn('其仁千所感',s);self.assertIn('因表留浚監',s)
 def test_prior_mother_and_mother_separate(self):
  p=self.c['paragraphs'][39];ms=p['mentions'];first=next(m for m in ms if m['surface']=='前母');mother=next(m for m in ms if m['surface']=='祜母');self.assertNotEqual(first['person_id'],mother['person_id']);self.assertIn('前母，孔融女，生兄發',p['text']);self.assertIn('發與祜同母兄承',p['text'])
 def test_cao_huan_not_eastern_jin_king_by_same_title(self):
  p=self.c['paragraphs'][2];m=next(m for m in p['mentions']if m['surface']=='陳留王');self.assertNotEqual(m['person_id'],'a80_779_2d5');self.assertEqual(next(x for x in p['mentions']if x['surface']=='少帝')['person_id'],m['person_id'])
 def test_source_book_not_person(self):
  p=self.c['paragraphs'][30];m=next(m for m in p['mentions']if m['surface']=='老子傳');self.assertEqual(m['kind'],'work');self.assertIsNone(m['person_id']);self.assertEqual(m['work_id'],'w-yanghu-laozizhuan-jin034-reference')
 def test_wei_jin_emperors_scoped(self):
  p=self.c['paragraphs'][2];self.assertEqual(next(m for m in p['mentions']if m['surface']=='文帝')['person_id'],'dkn_ge4_286_AAAAI');self.assertEqual(next(m for m in self.c['paragraphs'][38]['mentions']if m['surface']=='孝武')['person_id'],'uke_dff_yrf')
 def test_refusal_and_successor_words_all_preserved(self):
  s=self.c['paragraphs'][37]['text'];self.assertIn('暨以父沒不得為人後',s);self.assertIn('又不奉詔',s);self.assertIn('以伊弟篇為钜平侯，奉祜嗣',s)
 def test_children_and_no_heir_claims_coexist(self):
  self.assertIn('退告諸子',self.c['paragraphs'][22]['text']);self.assertIn('家無胤嗣',self.c['paragraphs'][33]['text']);self.assertIn('位至公而無子',self.c['paragraphs'][36]['text'])
 def test_no_heading_person_occurrence(self):
  a=self.b['selection']['start'];first=self.c['paragraphs'][0]['source_position']['raw_start'];self.assertLess(a,first);self.assertTrue(all(m['start']>=0 for p in self.c['paragraphs']for m in p['mentions']))
 def test_unknown_markup_fails_closed(self):
  s=self.raw.replace('羊祜，字叔子','{{unknown|羊祜}}，字叔子',1)
  with self.assertRaises(AssertionError):project(s,'羊祜傳')
 def test_consistent_raw_reshash_shift_rejected_by_witness_pin(self):
  with tempfile.TemporaryDirectory()as td:
   t=Path(td);c=copy.deepcopy(self.c);b=copy.deepcopy(self.b);rb=('\n'+self.raw).encode();sha=hashlib.sha256(rb).hexdigest();b['raw_sha256']=sha;c['source'].update(raw_file_sha256=sha,wikitext_sha256=sha)
   for rel,data in [(b['raw_file'],rb),(self.ref,(json.dumps(b,ensure_ascii=False)+'\n').encode()),('scripts/fixed_linked_heading_witnesses.json',(R/'scripts/fixed_linked_heading_witnesses.json').read_bytes())]:p=t/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
   self.assertTrue(source_errors(c,t))
 def test_raw_symlink_escape_rejected(self):
  with tempfile.TemporaryDirectory()as td:
   t=Path(td)
   for rel in[self.ref,'scripts/fixed_linked_heading_witnesses.json']:p=t/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((R/rel).read_bytes())
   q=t/self.b['raw_file'];q.parent.mkdir(parents=True,exist_ok=True);q.symlink_to(R/self.b['raw_file']);self.assertTrue(source_errors(self.c,t))
if __name__=='__main__':unittest.main()
