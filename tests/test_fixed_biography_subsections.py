# -*- coding: utf-8 -*-
"""Synthetic complete-source contracts; no historical person ID whitelist."""
import unittest,tempfile,copy,json,hashlib
from pathlib import Path
try:from scripts.fixed_biography_subsections import project,errors,KIND
except ImportError:from fixed_biography_subsections import project,errors,KIND
class CompleteBiographyTest(unittest.TestCase):
 def fixture(self,root):
  raw='前文\n==甲==\n　　甲好《[[別題|原稱]]》，{{YL|某年}}卒。後語不可丟。\n\n===子乙===\n　　乙字仲。\n\n史臣曰：甲之善。\n\n==丙==\n丙文。\n';a,z,ps,ex=project(raw,'甲傳');rel='sources/fixed.txt';(root/'sources').mkdir();(root/rel).write_text(raw);sha=hashlib.sha256(raw.encode()).hexdigest()
  ch=dict(id='c-synthetic',title='甲傳',source=dict(revision_id=123,raw_file=rel,raw_path=rel,wikitext_sha256=sha,raw_file_sha256=sha),paragraphs=[])
  for n,p in enumerate(ps):ch['paragraphs'].append(dict(id=f'paragraph-{n}',text=p['text'],text_layer='received_chapter',source_position=dict(**{k:v for k,v in p.items()if k!='text'},revision_id=123,projection_sha256=hashlib.sha256((json.dumps(p['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),source_layer='received_commentary'if p['text'].startswith('史臣曰：')else'received_biography')))
  b=dict(record_type=KIND,chapter_id=ch['id'],source_revision=123,raw_file=rel,raw_sha256=sha,selection=dict(start=a,end=z,opening_heading='==甲==',following_heading='==丙==',raw=raw[a:z]),excluded=ex);return ch,b
 def probe(self,change=None):
  with tempfile.TemporaryDirectory()as d:
   r=Path(d);ch,b=self.fixture(r)
   if change:change(ch,b,r)
   return errors(ch,r,b)
 def test_complete_subsections_and_suffix(self):self.assertEqual(self.probe(),[])
 def test_display_not_link_target(self):
  a,z,p,e=project('==甲==\n[[乙|丙]]後文\n==丁==\n','甲傳');self.assertEqual(p[0]['text'],'丙後文')
 def test_template_suffix(self):
  self.assertEqual(project('==甲==\n{{YL|三年}}此後全存\n==乙==\n','甲傳')[2][0]['text'],'三年此後全存')
 def test_word_replacement_rejected(self):self.assertTrue(self.probe(lambda c,b,r:c['paragraphs'][0].update(text=c['paragraphs'][0]['text'].replace('後語','新語'))))
 def test_omitted_attached_biography(self):self.assertTrue(self.probe(lambda c,b,r:c['paragraphs'].pop(1)))
 def test_shifted_positions_and_rehash(self):
  def bad(c,b,r):
   l=c['paragraphs'][0]['source_position'];l['raw_character_offsets']=[i+1 for i in l['raw_character_offsets']];l['projection_sha256']=hashlib.sha256((json.dumps(l['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
  self.assertTrue(self.probe(bad))
 def test_wrong_boundary(self):self.assertTrue(self.probe(lambda c,b,r:b['selection'].update(end=b['selection']['end']-1)))
 def test_unknown_markup_rejected(self):
  for t in ('{{未知|甲}}','[[未分顯示]]','<ref>古注</ref>','====附題====','==錯配===','===錯配=='):
   with self.subTest(t=t),self.assertRaises((AssertionError,ValueError)):project('==甲==\n'+t+'\n==乙==\n','甲傳')
 def test_wrong_revision(self):self.assertTrue(self.probe(lambda c,b,r:c['source'].update(revision_id=124)))
 def test_wrong_layer(self):self.assertTrue(self.probe(lambda c,b,r:c['paragraphs'][-1]['source_position'].update(source_layer='received_biography')))
 def test_omit_markup_classification(self):self.assertTrue(self.probe(lambda c,b,r:b['excluded'].pop()))
 def test_raw_path_escape(self):self.assertTrue(self.probe(lambda c,b,r:b.update(raw_file='../fixed.txt')))
if __name__=='__main__':unittest.main()
