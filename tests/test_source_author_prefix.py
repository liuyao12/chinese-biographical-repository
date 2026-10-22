import copy,json,unittest
from pathlib import Path
from scripts.source_author_prefix import source_author_errors
R=Path(__file__).resolve().parents[1]
class SourceAuthorPrefixTests(unittest.TestCase):
 def setUp(self):
  self.works={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};self.chapters={}
  for rel in ['009-caozhen','009-caoxiu','010-osaka1670-ni-heng-interface']:
   d=json.loads((R/('corpus/sanguozhi/'+rel+'.json')).read_text());self.chapters[d['id']]=d
  for w in self.works.values():
   if 'source_author_attributions' in w:w['source_author_attributions']=[e for e in w['source_author_attributions']if e.get('chapter_id')in self.chapters]
 def all_evidence(self):return [e for w in self.works.values()for e in w.get('source_author_attributions',[])]
 def evidence(self,surface):return next(e for e in self.all_evidence()if e['author_surface']==surface)
 def test_nine_actual_authorships(self):
  self.assertGreaterEqual(len(self.all_evidence()),9);self.assertEqual(source_author_errors(self.works,self.chapters),[])
 def test_two_wenshi_authors_preserve_distinct_source_spelling(self):
  a=self.evidence('張衡');b=self.evidence('張隠');self.assertNotEqual(a['referenced_work_id'],b['referenced_work_id']);self.assertNotEqual(a['author_person_id'],b['author_person_id']);self.assertEqual(a['authorship_syntax']['kind'],'author_title_prefix');self.assertEqual(b['authorship_syntax']['kind'],'author_title_prefix')
 def test_consistent_wrong_same_paragraph_person_rejected(self):
  e=self.evidence('晏');p=next(p for p in self.chapters[e['chapter_id']]['paragraphs']if p['id']==e['paragraph_id']);wrong=next(m for m in p['mentions']if m['kind']=='person'and m['surface']=='公主');e.update(author_name='金鄉公主',author_surface=wrong['surface'],author_person_id=wrong['person_id'],author_mention_id=wrong['id']);e['authorship_syntax']['object_person_mention_ids']=[];self.assertTrue(source_author_errors(self.works,self.chapters))
 def test_wrong_same_paragraph_prior_person_all_fields_rejected(self):
  e=self.evidence('張隠');p=next(p for p in self.chapters[e['chapter_id']]['paragraphs']if p['id']==e['paragraph_id']);wrong=next(m for m in p['mentions']if m['kind']=='person'and m['surface']=='肇');e.update(author_name='曹肇',author_surface=wrong['surface'],author_person_id=wrong['person_id'],author_mention_id=wrong['id']);self.assertTrue(source_author_errors(self.works,self.chapters))
 def test_source_and_referenced_work_cannot_be_interchanged(self):
  e=self.evidence('張衡');e['work_id']=e['referenced_work_id'];self.assertTrue(source_author_errors(self.works,self.chapters))
 def test_source_book_required(self):
  self.evidence('張衡')['book_id']='b-sanguozhi-009';self.assertTrue(source_author_errors(self.works,self.chapters))
 def test_missing_syntax_rejected(self):
  self.evidence('張隠').pop('authorship_syntax');self.assertTrue(source_author_errors(self.works,self.chapters))
 def test_compilation_cannot_just_point_to_earlier_same_person(self):
  e=self.evidence('範');p=next(p for p in self.chapters[e['chapter_id']]['paragraphs']if p['id']==e['paragraph_id']);earlier=next(m for m in p['mentions']if m['id'].endswith('m0231'));e['author_mention_id']=earlier['id'];self.assertTrue(source_author_errors(self.works,self.chapters))
 def test_marriage_object_needs_literal_role(self):
  e=self.evidence('晏');e['authorship_syntax']['object_person_mention_ids']=[];self.assertTrue(source_author_errors(self.works,self.chapters))
 def test_generic_unrelated_name_and_title(self):
  d={'id':'chapter-a','work_id':'source-work','book_id':'source-book','source_id':'source-a','paragraphs':[{'id':'p-a','text':'甲乙所著丙丁','mentions':[{'id':'author-a','kind':'person','person_id':'person-a','surface':'甲乙','start':0,'end':2},{'id':'title-a','kind':'work','work_id':'referenced-a','surface':'丙丁','start':4,'end':6}]}]};e={'chapter_id':'chapter-a','paragraph_id':'p-a','work_id':'source-work','book_id':'source-book','source_id':'source-a','referenced_work_id':'referenced-a','author_name':'甲乙','author_surface':'甲乙','author_person_id':'person-a','author_mention_id':'author-a','work_mention_id':'title-a','quote':'甲乙所著丙丁','authorship_syntax':{'kind':'author_title_prefix'}};self.assertEqual(source_author_errors({'referenced-a':{'source_author_attributions':[e]}},{d['id']:d}),[])
