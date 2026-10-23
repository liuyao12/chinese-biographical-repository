import unittest,copy
from scripts.fixed_attached_biography_quotes import project
class QuotedBiographyProjection(unittest.TestCase):
 def setUp(self):self.raw='前文\n==甲==\n{{wikipedia|甲}}\n　　甲，字乙。\n{{quote|　　甲曰：[[目標|原字]]{{YL|某年}}。\n\n　　吾-{幹}-之。}}\n====子 丙====\n　　丙，字丁。\n==戊==\n不收入\n'
 def test_complete_quote_and_nested_section(self):
  a,z,p,e=project(self.raw,'甲傳');self.assertEqual([x['text']for x in p],['甲，字乙。','甲曰：原字某年。','吾幹之。','丙，字丁。']);self.assertTrue(p[1]['quoted_block']);self.assertTrue(p[2]['quoted_block']);self.assertFalse(p[3]['quoted_block']);self.assertEqual(p[3]['section'],'子 丙');v=[i for x in p for i in x['raw_character_offsets']];excluded=[i for x in e for i in range(x['start'],x['end'])];self.assertEqual(sorted(v+excluded),list(range(a,z)));self.assertEqual(len(set(v+excluded)),z-a)
 def test_quote_tail_not_dropped(self):
  p=project(self.raw.replace('}}\n====','}}尾文\n===='),'甲傳')[2];self.assertEqual(p[2]['text'],'吾幹之。尾文')
 def test_unclosed_quote_rejected(self):
  with self.assertRaises(AssertionError):project(self.raw.replace('之。}}','之。'),'甲傳')
 def test_unknown_template_rejected(self):
  with self.assertRaises(AssertionError):project(self.raw.replace('甲，字乙。','甲{{未知|不可略}}，字乙。'),'甲傳')
 def test_duplicate_opening_rejected(self):
  with self.assertRaises(AssertionError):project(self.raw+'==甲==\n甲\n','甲傳')
 def test_conversion_rule_not_silently_executed(self):
  with self.assertRaises(AssertionError):project(self.raw.replace('-{幹}-','-{zh-hant:幹|zh-hans:干}-'),'甲傳')
if __name__=='__main__':unittest.main()
