import copy,json,unittest
from pathlib import Path
from scripts.source_author_prefix import source_author_errors
R=Path(__file__).resolve().parents[1];C=json.loads((R/'corpus/sanguozhi/019-yangxiu.json').read_text());WORKS={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};W={wid:dict(w,source_author_attributions=[e for e in w.get('source_author_attributions',[])if e['chapter_id']==C['id']])for wid,w in WORKS.items()};CH={C['id']:C}
class Sgz019WorkReferences(unittest.TestCase):
 def test_all_twelve_exact_and_work_only(self):
  ms=[m for p in C['paragraphs']for m in p['mentions']if m['kind']=='work'];self.assertEqual(len(ms),12)
  for p in C['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='work':self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertIsNone(m['person_id']);self.assertIn(m['work_id'],W)
 def test_two_actual_source_authors(self):
  es=[e for w in W.values()for e in w.get('source_author_attributions',[])];self.assertEqual({e['author_surface']for e in es},{'摯虞','荀綽'});self.assertEqual(source_author_errors(W,CH),[])
 def mutate(self,fn):
  w=copy.deepcopy(W);es=[e for x in w.values()for e in x.get('source_author_attributions',[])];fn(es[0]);return source_author_errors(w,CH)
 def test_source_and_referenced_work_cannot_swap(self):self.assertTrue(self.mutate(lambda e:e.update(work_id=e['referenced_work_id'])))
 def test_wrong_author_rejected(self):self.assertTrue(self.mutate(lambda e:e.update(author_person_id='wrong')))
 def test_truncated_quote_rejected(self):self.assertTrue(self.mutate(lambda e:e.update(quote=e['quote'][:-1])))
 def test_wrong_title_offset_rejected(self):
  ch=copy.deepcopy(CH);pid=next(e for w in W.values()for e in w.get('source_author_attributions',[]))['work_mention_id'];m=next(m for p in ch[C['id']]['paragraphs']for m in p['mentions']if m['id']==pid);m['start']+=1;self.assertTrue(source_author_errors(W,ch))
 def test_no_fake_fuchang_book_and_no_silent_wing_correction(self):
  self.assertFalse(any(w['citation_title']=='傅暢'for w in W.values()if 'citation_title'in w));self.assertEqual(W['w-yizhouji-sgz019-reference']['citation_title'],'翼州記')
 def test_short_titles_resolved_from_external_commentary(self):
  self.assertNotIn('w-lushi-sgz019-reference',W)
  self.assertEqual(W['w-huainan-sgz019-reference']['citation_title'],'淮南子')
  self.assertEqual(W['w-lushichunqiu-sgz019-reference']['citation_title'],'吕氏春秋')
  m=next(m for p in C['paragraphs']for m in p['mentions']if m['id']=='c-sanguozhi-019-yangxiu:p002:m1033')
  self.assertEqual(m['surface'],'吕氏');self.assertEqual(m['work_id'],'w-lushichunqiu-sgz019-reference');self.assertNotIn('work_reference_resolution',m)
