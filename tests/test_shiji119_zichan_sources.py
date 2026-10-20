import copy,json,unittest
from pathlib import Path
from scripts.source_excerpts import excerpt_errors
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
class CommentaryExcerptTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.chapters=[read(f'corpus/zuozhuan-zhushu/030-xiang{y:03}.json')for y in [5,8,9]]
 def mutated(self,index=0):return copy.deepcopy(self.chapters[index])
 def test_three_actual_quotes_have_exact_unicode_source_positions(self):
  self.assertEqual([c['paragraphs'][0]['text']for c in self.chapters],['發子産父','子産子國子','公子發注子國'])
  for c in self.chapters:
   self.assertEqual(excerpt_errors(c),[]);p=c['paragraphs'][0];e=p['source_excerpt'];self.assertEqual(e['raw_line'][e['start']:e['end']],p['text']);self.assertEqual(c['source']['source_commit'],'685a6ddca22d98535cac38038afdff7308273d23')
 def test_rewritten_quote_is_rejected(self):
  c=self.mutated();c['paragraphs'][0]['text']='發子産兄';self.assertTrue(excerpt_errors(c))
 def test_wrong_unicode_offset_is_rejected(self):
  c=self.mutated();c['paragraphs'][0]['source_excerpt']['start']-=1;self.assertTrue(excerpt_errors(c))
 def test_commentary_cannot_be_presented_as_received_chapter(self):
  c=self.mutated();c['paragraphs'][0]['text_layer']='received_chapter';self.assertTrue(excerpt_errors(c))
 def test_year_heading_cannot_be_assigned_another_number(self):
  c=self.mutated();c['paragraphs'][0]['source_excerpt']['year_section_heading']['year_number']=9;self.assertTrue(excerpt_errors(c))
 def test_fixed_revision_cannot_be_replaced_by_head(self):
  c=self.mutated();c['source']['revision_id']='HEAD';self.assertTrue(excerpt_errors(c))
 def test_excerpt_cannot_move_to_another_book(self):
  c=self.mutated();c['book_id']='b-zuozhuan-zhushu-031';self.assertTrue(excerpt_errors(c))
 def test_attribution_marker_is_required_even_when_quote_is_exact(self):
  c=self.mutated(1);e=c['paragraphs'][0]['source_excerpt'];e['attribution_context_lines'][0]['raw_line']=e['attribution_context_lines'][0]['raw_line'].replace('注','按');self.assertTrue(excerpt_errors(c))
 def test_missing_excerpt_metadata_is_rejected(self):
  c=self.mutated();del c['paragraphs'][0]['source_excerpt'];self.assertTrue(excerpt_errors(c))
 def test_review_image_and_extent_are_not_overclaimed(self):
  for key,value in [('image_verified',True),('text_scope','chapter')]:
   c=self.mutated();c['source'][key]=value;self.assertTrue(excerpt_errors(c))
  c=self.mutated();c['annotation']['human_reviewed']=True;self.assertTrue(excerpt_errors(c))
class ZichanPreferredParentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.decision=next(d for d in read('corpus/shiji/family-tree-decisions.json')['decisions']if d['id']=='ft-shiji-zichan-parent');cls.child=cls.decision['subject_person_id'];cls.father=cls.decision['preferred_parent_person_id'];cls.people={p['id']:p for p in read('registry/persons.json')['persons']}
 def test_source_claim_is_retained_but_default_follows_explicit_du_note(self):
  d=self.decision;a=next(a for a in read('corpus/shiji/042-assertions.json')['assertions']if a['id']=='a-shiji042-041');self.assertEqual(a['subject_person_id'],self.child);self.assertEqual(a['object_person_id'],'gts_42q_flu');self.assertIn('鄭成公少子',a['evidence'][0]['quote']);self.assertIn(a['id'],d['excluded_assertion_ids'])
  preferred=read('corpus/zuozhuan-zhushu/030-xiang008-assertions.json')['assertions'][0];self.assertEqual(preferred['id'],d['preferred_assertion_id']);self.assertEqual((preferred['subject_person_id'],preferred['object_person_id']),(self.child,self.father));self.assertEqual(preferred['evidence'][0]['quote'],'子産子國子');self.assertEqual(self.people[self.child]['family_path']['parent_person_id'],self.father)
 def test_new_family_id_and_source_names_do_not_invent_earlier_ancestry_or_surname(self):
  self.assertEqual(self.child,self.father+'_A');self.assertNotIn('family_path',self.people[self.father]);self.assertEqual({a['surface']for a in self.people[self.father]['aliases']},{'公子發','發','子國'})
  names=next(n for n in read('data/corpus/profile-names.json')['records']if n['person_id']==self.father);self.assertIsNone(names['surname']);self.assertEqual(names['ming'],'發');self.assertEqual(names['additional_names'],['子國'])
 def test_retired_child_id_has_no_registry_export_or_profile(self):
  old='gts_42q_flu_B';self.assertNotIn(old,self.people)
  for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(old+'.json')).exists())
if __name__=='__main__':unittest.main()
