from pathlib import Path
import json,copy,unittest,hashlib,xml.etree.ElementTree as ET
from scripts.reading_layout import partition,validate_chapter
from scripts.render_corpus import render
ROOT=Path(__file__).resolve().parents[1];D=json.loads((ROOT/'corpus/sanguozhi/010.json').read_text());ARCH='c-sanguozhi-010-xunyu-xunyou-jiaxu:descendants:p001'
class ReadingLayout(unittest.TestCase):
 def bad(self,fn):
  d=copy.deepcopy(D);fn(d)
  with self.assertRaises((ValueError,KeyError,TypeError)):validate_chapter(d,ROOT)
 def test_complete_partition_and_fixedraw_ranges(self):
  validate_chapter(D,ROOT);rows=partition(D);self.assertEqual({p['id']for p,_,_ in rows},{p['id']for p in D['paragraphs']});self.assertEqual(len(rows),len(D['paragraphs']));self.assertEqual(rows[-1][0]['id'],ARCH);self.assertEqual(rows[-1][1],'archival-excerpt');self.assertNotEqual(rows[1][0]['id'],ARCH)
 def test_unknown_id(self):self.bad(lambda d:d['reading_layout']['primary_paragraph_ids'].append('missing'))
 def test_missing_id(self):self.bad(lambda d:d['reading_layout']['primary_paragraph_ids'].pop())
 def test_duplicate_id(self):self.bad(lambda d:d['reading_layout']['primary_paragraph_ids'].append(d['reading_layout']['primary_paragraph_ids'][0]))
 def test_cross_role(self):self.bad(lambda d:d['reading_layout']['primary_paragraph_ids'].append(ARCH))
 def test_wrong_order(self):self.bad(lambda d:d['reading_layout']['primary_paragraph_ids'].reverse())
 def test_partial_coverage(self):self.bad(lambda d:d['reading_layout']['archival_excerpts'][0]['canonical_segments'].pop())
 def test_wrong_text(self):self.bad(lambda d:d['reading_layout']['archival_excerpts'][0]['canonical_segments'][0].update(quote='偽文'))
 def test_wrong_range(self):self.bad(lambda d:d['reading_layout']['archival_excerpts'][0]['canonical_segments'][0].update(canonical_start=1))
 def test_revision(self):self.bad(lambda d:d['reading_layout']['source'].update(revision_id='0'*40))
 def test_cross_source(self):self.bad(lambda d:d['reading_layout']['source'].update(source_id='foreign'))
 def test_wrong_raw_sha(self):self.bad(lambda d:d['reading_layout']['source'].update(raw_file_sha256='0'*64))
 def test_traversal(self):self.bad(lambda d:d['reading_layout']['source'].update(raw_path='sources/witnesses/../../../private.txt'))
 def test_cannot_autoarchive_similar_text(self):
  self.bad(lambda d:d['reading_layout']['archival_excerpts'][0].update(reason='similar_quote'))
 def test_xml_order_preserves_all_original_text_and_mentions(self):
  xml=ET.fromstring(render(D));ps=xml.findall('p');self.assertEqual([p.get('id')for p in ps],[p['id']for p,_,_ in partition(D)]);by={p['id']:p for p in D['paragraphs']}
  for p in ps:self.assertEqual(''.join(p.itertext()),by[p.get('id')]['text']);self.assertEqual([m.get('id')for m in p],[m['id']for m in by[p.get('id')]['mentions']])
  self.assertEqual(D['text_sha256'],hashlib.sha256('\n\n'.join(p['text']for p in D['paragraphs']).encode()).hexdigest())
 def test_without_layout_exact_legacy_xml(self):
  c={'id':'c','work_id':'w','book_id':'b','source_id':'s','paragraphs':[{'id':'p','text':'甲乙','mentions':[]}]};self.assertEqual(render(c),'<?xml version="1.0" encoding="UTF-8"?>\n<text format-version="0.2" work-id="w" book-id="b" chapter-id="c" source-id="s">\n  <p id="p">甲乙</p>\n</text>\n');self.assertEqual(partition(c),[(c['paragraphs'][0],None,None)])
if __name__=='__main__':unittest.main()
