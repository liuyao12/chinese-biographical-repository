"""Next complete source unit; data-driven extension retains the old119 frame."""
from pathlib import Path
import unittest,json,copy
from scripts import wyd_song051_yixin as y
from scripts import fixed_wuyingdian_song051_family_phase as core
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.received_family_names import source_component_valid
from scripts.validation_context import scope
ROOT=Path(__file__).resolve().parents[1]
class Yirong(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch,cls.roles,cls.c,all_docs=y.state(ROOT);cls.docs={k:v for k,v in all_docs.items()if k.startswith('corpus/songshu/051-wyd1739-yirong-')};cls.catalog=load_catalog(ROOT);cls.sm,_=load_assemblies(ROOT,cls.catalog)
 def test_complete300_and_pending_scope(self):
  u=next(u for u in self.c['additional_complete_units']if u['key']=='yirong');self.assertEqual(u['length'],300);self.assertEqual(sum(len(s['text'])for s in u['scope']),300);self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),598);self.assertEqual(sum(p['annotation_status']=='pending'for p in self.ch['paragraphs']),8);self.assertEqual(self.ch['paragraphs'][11]['text'][193],'顗');self.assertEqual(self.ch['paragraphs'][8]['text'][150],'蕭');self.assertEqual(self.ch['paragraphs'][9]['text'][103],'祗')
 def test_three_birth_fathers_five_relative_siblings(self):
  aa=[a for d in self.docs.values()for a in d.get('assertions',[])];self.assertEqual(len(aa),8);self.assertEqual(sum(a['predicate']=='father'for a in aa),3);self.assertEqual(sum(a['predicate']=='brother'for a in aa),5)
  r=next(a for a in aa if a['id']=='a-song051-yixin-yirong-min-brother')['qualifiers']['relative_birth_order'];self.assertEqual((r['older_person_id'],r['younger_person_id']),(self.roles['yr_huang'],self.roles['yr_min']));self.assertIsNone(r['older_ordinal']);self.assertIsNone(r['younger_ordinal'])
  chapters={r['id']:r for r in self.catalog[1]if r.get('record_type')=='marked_chapter'};paragraphs={p['id']:(r['id'],p)for r in chapters.values()for p in r['paragraphs']};self.assertTrue(all(core.family_valid(a,paragraphs,chapters,ROOT)for a in aa))
 def test_qualified_family_and_birth_not_succession_parent(self):
  self.assertEqual(self.sm[self.roles['yr_huang']]['parent_person_id'],self.roles['yr_xi']);self.assertEqual(self.sm[self.roles['yr_min']]['parent_person_id'],self.roles['yr_xi']);self.assertEqual(self.sm[self.roles['yr_di']]['parent_person_id'],self.roles['old_yirong'])
  for role in('yr_xi','yr_biao','yr_ding','yr_yi'):
   row=self.sm[self.roles[role]];self.assertIsNone(row['source_assertion_id']);self.assertEqual(row['parent_person_id'],self.roles['old_yirong']);self.assertEqual(row['parent_connection']['status'],'contextual_provisional')
  d=next(x for doc in self.docs.values()for x in doc.get('decisions',[])if x['id']=='d-song051-yirong-yr_huang');s=d['reported_title_succession'];self.assertEqual(s['predecessor_person_id'],self.roles['yr_di']);self.assertEqual(s['birth_father_person_id'],self.roles['yr_xi']);self.assertFalse(s['parent_override']);self.assertEqual(s['adoption_assertion_scope'],'本條未作收養斷言；不是確未收養的負面史實。');self.assertIsNone(s['event_year'])
 def test_literal_and_restored_components_from_source(self):
  ns=[n for d in self.docs.values()for n in d.get('records',[])];self.assertEqual(len(ns),17);self.assertTrue(all(source_component_valid(n,self.ch,ROOT)for n in ns))
  for role in('yr_di','yr_xi','yr_huang','yr_min','yr_biao','yr_ding','yr_yi'):self.assertEqual({n['surname']for n in ns if n['person_id']==self.roles[role]},{None,'劉'})
  xi=next(n for n in ns if n['id']=='name-song051-yirong-literal-yr_xi');self.assertEqual((xi['ming'],xi['zi']),('襲','茂德'));self.assertNotEqual(self.roles['yr_xi'],'8dd_b21_728')
 def test_actual_bundle_for_all10_and_retained_homonym(self):
  with scope(ROOT):
   for role in [r for r in self.c['new_names']if r.startswith('yr_')]:
    b=bundle(self.roles[role],root=ROOT,include_provisional=True,catalog=self.catalog);self.assertEqual(b['canonical_person_id'],self.roles[role]);self.assertTrue(b['mentions']);self.assertTrue(b['name_components'])
  self.assertIn('8dd_b21_728',self.catalog[0])
 def test_old_new_frame_and_unknown_changes_fail(self):
  for case in('old_marker','new_marker','text','metadata'):
   ch=copy.deepcopy(self.ch)
   if case=='old_marker':ch['paragraphs'][7]['mentions'][0]['person_id']=self.roles['yr_di']
   if case=='new_marker':next(m for m in ch['paragraphs'][12]['mentions']if m['surface']=='旻')['person_id']=self.roles['yr_huang']
   if case=='text':ch['paragraphs'][12]['text']=ch['paragraphs'][12]['text'].replace('王武連','王武蓮')
   if case=='metadata':ch['annotation']['additional_annotation_phase']['unexpected']=True
   self.assertTrue(core.source_errors(ch,ROOT),case)
if __name__=='__main__':unittest.main()
