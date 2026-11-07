"""Source-verified title continuation is neither a name nor witness duplication."""
import copy,json,unittest
from pathlib import Path
from scripts.person_bundle import load_catalog,bundle
from scripts.validation_context import scope
from scripts.occurrence_concordance import appellation_continuations,index_counts
from scripts.profile_occurrence_counts import profile_occurrences
ROOT=Path(__file__).resolve().parents[1]
class AppellationFragmentConsumers(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,cls.records=load_catalog(ROOT);ch=next(r for r in cls.records if r.get('id')=='c-songshu-051-wyd1739-zongshi');p=next(p for p in ch['paragraphs']if p['id'].endswith(':p001'));cls.pid=next(m['person_id']for m in p['mentions']if m['id'].endswith(':m0000'));ns=json.loads((ROOT/'corpus/songshu/051-wyd1739-yiqing-name-components.json').read_text());cls.chuo=next(n['person_id']for n in ns['records']if n.get('zi')=='子流')
  with scope(ROOT):cls.b=bundle(cls.pid,ROOT,include_provisional=True,catalog=(cls.people,cls.records));cls.oldname=bundle(cls.chuo,ROOT,include_provisional=True,catalog=(cls.people,cls.records))
  catalog=json.loads((ROOT/'data/corpus/index.json').read_text());cls.chapters={r.get('chapter_id'):r for r in catalog['chapters']}
  for work in json.loads((ROOT/'data/corpus/works.json').read_text())['works']:
   if work['reader_kind']!='shiji':cls.chapters.update({r['chapter_id']:r for r in json.loads((ROOT/work['catalog_path']).read_text())['chapters']})
  cls.titles={w['id']:w['title']for w in json.loads((ROOT/'registry/works.json').read_text())['works']}
 def test_two_raw_anchors_one_title_no_witness_duplicate(self):
  b=self.b;g=b['source_appellation_fragments'][0];self.assertEqual(g['complete_appellation'],{'kind':'title','value':'長沙景王'});self.assertEqual([f['surface']for f in g['fragments']],['長','沙景王']);self.assertEqual(len(g['mention_ids']),2);self.assertTrue(set(g['mention_ids'])<={m['id']for m in b['mentions']});r=next(r for r in b['source_mention_summary']if r['source_id']==g['source_id']);self.assertEqual(r['continuation_fragment_count'],1);self.assertEqual(r['raw_mention_count'],r['mention_count']+r['duplicate_mention_count']+1);self.assertIn('不是重出',r['count_explanation']);self.assertFalse(any(h['id']==g['id']for h in b['title_holdings']))
 def test_direct_positive_group_and_JSON_shape(self):
  g=self.b['source_appellation_fragments'];aliases,details=appellation_continuations(ROOT,self.records,self.b['mentions'],g);self.assertEqual(aliases,{g[0]['mention_ids'][1]:g[0]['mention_ids'][0]});self.assertEqual(details[g[0]['mention_ids'][0]]['fragment_kind'],'appellation')
  n=self.oldname['source_name_fragments'];aliases,details=appellation_continuations(ROOT,self.records,self.oldname['mentions'],[],n);self.assertEqual(aliases,{n[0]['mention_ids'][1]:n[0]['mention_ids'][0]});self.assertEqual(details[n[0]['mention_ids'][0]]['fragment_kind'],'name')
  for value in [(),{},'bad',True]:
   with self.subTest(value=repr(value)),self.assertRaises(ValueError):appellation_continuations(ROOT,self.records,self.b['mentions'],value)
 def test_source_group_changes_fail_closed(self):
  original=self.b['source_appellation_fragments']
  for mode in ['person','source','chapter','MID','order','surface','complete','quote','human','canonical']:
   groups=copy.deepcopy(original);g=groups[0]
   if mode=='person':g['person_id']=self.chuo
   elif mode=='source':g['source_id']='wrong'
   elif mode=='chapter':g['chapter_id']='wrong'
   elif mode=='MID':g['mention_ids'][1]='unknown'
   elif mode=='order':g['fragments'].reverse()
   elif mode=='surface':g['fragments'][0]['surface']='別'
   elif mode=='complete':g['complete_appellation']['kind']='ming'
   elif mode=='quote':g['source_quotes'][0]['quote']+='別'
   elif mode=='human':g['human_reviewed']=True
   elif mode=='canonical':g['canonical_mention_id']=g['mention_ids'][1]
   with self.subTest(mode=mode),self.assertRaises(ValueError):appellation_continuations(ROOT,self.records,self.b['mentions'],groups)
 def test_profile_requires_complete_continuation_proof(self):
  for mode in ['missing','count','boolean','canonical','kind','duplicate_group']:
   b=copy.deepcopy(self.b);g=next(g for r in b['source_mention_summary']for g in r['occurrence_groups']if g.get('continuation_fragment_count'))
   if mode=='missing':b.pop('source_appellation_fragments')
   elif mode=='count':g['continuation_fragment_count']=2
   elif mode=='boolean':g['continuation_fragment_count']=True
   elif mode=='canonical':g['canonical_mention_id']=g['mention_ids'][1]
   elif mode=='kind':g['counting_basis']='same_position_duplicate'
   elif mode=='duplicate_group':b['source_appellation_fragments']*=2
   with self.subTest(mode=mode),self.assertRaises(ValueError):profile_occurrences(b,self.chapters,self.titles)
 def test_profile_and_index_separate_continuations_from_duplicates(self):
  rows=profile_occurrences(self.b,self.chapters,self.titles);r=next(r for r in rows if r.get('continuation_fragment_count'));self.assertEqual(r['continuation_fragment_count'],1);self.assertEqual(r['raw_count'],r['count']+r['duplicate_count']+1);c=index_counts(self.b);self.assertEqual(c['continuation_fragment_count'],1);self.assertEqual(c['raw_mention_count'],c['mention_count']+c['duplicate_mention_count']+1)
 def test_original_child_zi_fragment_interface_unchanged(self):
  b=self.oldname;self.assertNotIn('source_appellation_fragments',b);g=b['source_name_fragments'][0];self.assertEqual(g['kind'],'source_bound_name_fragment_group');self.assertEqual(g['complete_component']['field'],'zi');self.assertEqual(g['complete_component']['value'],'子流');self.assertEqual(index_counts(b)['continuation_fragment_count'],1);self.assertEqual(next(r for r in b['source_mention_summary']if r['source_id']==g['source_id'])['mention_count'],3)
if __name__=='__main__':unittest.main()
