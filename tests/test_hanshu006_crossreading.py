import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())
class WudiCrossreading(unittest.TestCase):
 def chapter(self):return read('corpus/hanshu/006.json')
 def test_six_noncontiguous_paragraphs_not_whole_chapter(self):
  c=self.chapter();self.assertEqual([p['id'].rsplit(':',1)[1]for p in c['paragraphs']],['p001','p024','p025','p028','p039','p040']);self.assertEqual(sum(len(p['mentions'])for p in c['paragraphs']),14);self.assertEqual(c['source']['text_scope'],'partial_chapter');self.assertFalse(c['source']['image_verified']);b=next(b for b in read('corpus/progress.json')['books']if b['book_id']=='b-hanshu-006');self.assertFalse(b['complete']);self.assertEqual(b['text_status'],'partial_transcription')
 def test_seven_cross_book_identities_have_actual_source_anchors(self):
  ds=read('corpus/hanshu/006-identities.json')['decisions'];self.assertEqual(len(ds),7)
  for d in ds:self.assertFalse(d['human_reviewed']);self.assertEqual(d['scope'],'cross_chapter');self.assertIn('c-hanshu-006-wudi',d['chapter_ids']);self.assertTrue(all(e['mention_ids']for e in d['evidence']))
 def test_sibling_relationship_keeps_mother_and_father_distinct(self):
  a=read('corpus/hanshu/006-assertions.json')['assertions'];self.assertEqual([(x['predicate'],x['object_person_id'])for x in a[:2]],[('father','yqp_nlb_p1p_ACA'),('mother','6d6_eg1_o3a_A')])
  for x in a[2:]:self.assertTrue(x['qualifiers']['shared_mother']);self.assertIsNone(x['qualifiers']['shared_father']);self.assertEqual(x['qualifiers']['relative_birth_order']['older_person_id'],'6d6_eg1_o3a_A');self.assertIsNone(x['qualifiers']['relative_birth_order']['younger_ordinal'])
 def test_four_deaths_keep_own_subject_and_explicit_year_windows(self):
  c=self.chapter();ps={p['id']:p for p in c['paragraphs']};es=read('corpus/hanshu/006-life-events.json')['events'];self.assertEqual(len(es),4);self.assertEqual([e['normalized_date_range']['latest']['era_year']for e in es],[141,135,131,131])
  for e in es:
   ev=e['evidence'][0];p=ps[ev['paragraph_id']];self.assertEqual(next(m['person_id']for m in p['mentions']if m['id']==ev['person_mention_id']),e['person_id']);self.assertEqual(e['event_type'],'death');self.assertNotIn('normalized_date',e);w=e['normalized_date_range'];self.assertEqual(w['latest']['year']-w['earliest']['year'],1);self.assertIn(e['date_expression'],ev['quote'])
 def test_received_death_word_and_chronological_variant_preserved(self):
  c=self.chapter();p=next(p for p in c['paragraphs']if p['id'].endswith(':p039'));self.assertIn('棄巿',p['text']);self.assertNotIn('棄市',p['text']);self.assertIn('四年冬',p['text']);sj=read('corpus/shiji/107.json')['paragraphs'][23]['text'];self.assertIn('五年十月',sj);self.assertIn('十二月晦',sj)
 def test_title_words_not_mistaken_for_new_persons_or_birth_years(self):
  p=self.chapter()['paragraphs'][0]
  for term in ['膠東王','皇太子']:
   at=p['text'].index(term);self.assertFalse(any(m['start']<=at<m['end']for m in p['mentions']))
  self.assertFalse(any(e['event_type']=='birth'for e in read('corpus/hanshu/006-life-events.json')['events']))
