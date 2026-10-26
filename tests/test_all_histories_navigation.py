import json,unittest
from pathlib import Path
from scripts.reading_catalog import outputs
ROOT=Path(__file__).resolve().parents[1]
MINIMUM={'shiji','hanshu','houhanshu','sanguozhi','jinshu','songshu','nanqishu','liangshu','chenshu','weishu-weishou','beiqishu','zhoushu','suishu','nanshi','beishi','jiutangshu','xintangshu','jiuwudaishi','xinwudaishi','songshi','liaoshi','jinshi','yuanshi','mingshi','zizhitongjian'}
class NavigationCatalogTests(unittest.TestCase):
 def test_all_twenty_four_histories_and_tongjian_are_navigable(self):
  generated=outputs(ROOT);manifest=json.loads(generated[ROOT/'data/corpus/works.json']);rows={w['id']:w for w in manifest['works']}
  self.assertTrue({'w-'+s for s in MINIMUM}.issubset(rows))
  directory=json.loads((ROOT/'data/corpus/chapter-directory.json').read_text());byid={w['work_id']:w for w in directory['works']}
  for slug in MINIMUM-{'shiji'}:
   w=rows['w-'+slug];index=json.loads(generated[ROOT/w['catalog_path']]);self.assertEqual(index['work_id'],w['id']);self.assertTrue(byid[w['id']]['books'])
   self.assertTrue(all(c['available']in('marked_text','table')for c in index['chapters']))
   if not index['chapters']:self.assertIn('正文尚未收錄',index['policy'])
