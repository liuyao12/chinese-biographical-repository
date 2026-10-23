# coding: utf-8
import copy, unittest
from scripts.work_reference_resolution import chapter_errors
class WorkReferenceTests(unittest.TestCase):
    def fixture(self):
        a={'id':'c:p1:w0','kind':'work','person_id':None,'work_id':'w-fictional','status':'source_explicit','surface':'甲乙傳','start':0,'end':3}
        s={'id':'c:p3:w0','kind':'work','person_id':None,'work_id':'w-fictional','status':'contextual_provisional','surface':'乙傳','start':0,'end':2,'work_reference_resolution':{'kind':'shortened_title','antecedent_mention_id':a['id'],'scope_paragraph_ids':['c:p1','c:p2','c:p3'],'reason':'合成測試：明示首題之後連續同一引文與編者回指。'}}
        return {'paragraphs':[{'id':'c:p1','text':'甲乙傳曰','mentions':[a]},{'id':'c:p2','text':'合成引文','mentions':[]},{'id':'c:p3','text':'乙傳云','mentions':[s]}]}
    def test_source_local_continuation(self): self.assertEqual(chapter_errors(self.fixture()), [])
    def test_no_resolution_legacy_unchanged(self): self.assertEqual(chapter_errors({'paragraphs':[{'id':'p','mentions':[]}]}), [])
    def test_wrong_work(self):
        d=self.fixture(); d['paragraphs'][2]['mentions'][0]['work_id']='w-other'; self.assertTrue(chapter_errors(d))
    def test_forward_antecedent(self):
        d=self.fixture(); d['paragraphs'].reverse(); self.assertTrue(chapter_errors(d))
    def test_nonexistent_scope(self):
        d=self.fixture(); d['paragraphs'][2]['mentions'][0]['work_reference_resolution']['scope_paragraph_ids'].append('another:chapter'); self.assertTrue(chapter_errors(d))
    def test_scope_must_not_skip_intervening_paragraph(self):
        d=self.fixture(); d['paragraphs'][2]['mentions'][0]['work_reference_resolution']['scope_paragraph_ids']=['c:p1','c:p3']; self.assertTrue(chapter_errors(d))
    def test_person_cannot_be_book_antecedent(self):
        d=self.fixture(); d['paragraphs'][0]['mentions'][0].update(kind='person',person_id='person'); self.assertTrue(chapter_errors(d))
    def test_short_form_is_not_identical_full_title(self):
        d=self.fixture(); d['paragraphs'][2]['mentions'][0]['surface']='甲乙傳'; self.assertTrue(chapter_errors(d))
    def test_reason_not_omitted(self):
        d=self.fixture(); d['paragraphs'][2]['mentions'][0]['work_reference_resolution']['reason']=' '; self.assertTrue(chapter_errors(d))
    def test_not_auto_choose_first_in_whole_chapter(self):
        d=self.fixture(); d['paragraphs'].insert(0,{'id':'c:outside','mentions':[dict(d['paragraphs'][0]['mentions'][0],id='c:outside:w0')]}); self.assertEqual(chapter_errors(d),[])
    def test_declared_first_must_be_first_inside_scope(self):
        d=self.fixture(); d['paragraphs'][1]['mentions']=[dict(d['paragraphs'][0]['mentions'][0],id='c:p2:w0')]; d['paragraphs'][2]['mentions'][0]['work_reference_resolution']['antecedent_mention_id']='c:p2:w0'; self.assertTrue(chapter_errors(d))
    def test_malformed_scope_fails_without_exception(self):
        d=self.fixture(); d['paragraphs'][2]['mentions'][0]['work_reference_resolution']['scope_paragraph_ids']=[{}]; self.assertTrue(chapter_errors(d))
if __name__=='__main__': unittest.main()
