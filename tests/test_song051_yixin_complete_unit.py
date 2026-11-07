"""Complete Yixin unit, preserving prior formal49 and mutable person endpoints."""
from pathlib import Path
import copy,json,unittest,tempfile
from scripts import wyd_song051_yixin as y
from scripts import fixed_wuyingdian_song051_family_phase as core
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.received_family_names import source_component_valid
from scripts.validation_context import scope
ROOT=Path(__file__).resolve().parents[1]
class CompleteYixin(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.actual,cls.roles,cls.c,all_docs=y.state(ROOT);cls.docs={k:v for k,v in all_docs.items()if k.startswith("corpus/songshu/051-wyd1739-yixin-")};cls.prior=core.context(ROOT)[0];cls.catalog=load_catalog(ROOT);cls.sm,_=load_assemblies(ROOT,cls.catalog)
 def test_complete908_and_strict_current_not_stale49(self):
  self.assertEqual(sum(len(u['text'])for u in self.c['complete_unit_scope']),908);self.assertEqual(core.source_errors(self.actual,ROOT),[]);self.assertTrue(core.source_errors(self.prior,ROOT));self.assertEqual(sum(len(p['mentions'])for p in self.actual['paragraphs']),598);self.assertEqual(sum(len(p['mentions'])for p in self.prior['paragraphs']),49);self.assertEqual(sum(p['annotation_status']=='pending'for p in self.actual['paragraphs']),8)
  old={m['id']:m for p in self.prior['paragraphs']for m in p['mentions']};new={m['id']:m for p in self.actual['paragraphs']for m in p['mentions']};self.assertTrue(all(new[k]==v for k,v in old.items()))
 def test_corrected_source_and_resolved_AI_printed_glyph(self):
  p=self.actual['paragraphs'][9];self.assertEqual(p['text'][53],'三');self.assertEqual(p['text'][115],'宰');self.assertEqual(p['text'][103],'祗');self.assertEqual(self.actual['source']['normalization']['editorial_readings'][0]['accepted_reading'],'祗');self.assertFalse(any(m['surface']=='〓'for m in p['mentions']));self.assertEqual(next(m for m in p['mentions']if m['surface']=='太宰')['person_id'],self.roles['yigong'])
 def test_fifteen_explicit_relations_not_inferred_father_assertions(self):
  assertions=[a for d in self.docs.values()for a in d.get('assertions',[])];self.assertEqual(len(assertions),15);self.assertEqual({a['subject_person_id']for a in assertions if a['predicate']=='father'},{self.roles[x]for x in('jin','can','jie')});self.assertEqual(sum(a['predicate']=='brother'for a in assertions),11);a=next(a for a in assertions if a['predicate']=='agnatic_cousin');self.assertEqual((a['subject_person_id'],a['object_person_id']),(self.roles['bing'],self.roles['shu']));self.assertIsNone(a['qualifiers']['kinship_structure']['distance']);self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id'])
  chapters={r['id']:r for r in self.catalog[1]if r.get('record_type')=='marked_chapter'};paragraphs={p['id']:(r['id'],p)for r in chapters.values()for p in r['paragraphs']}
  self.assertTrue(all(core.family_valid(a,paragraphs,chapters,ROOT)for a in assertions))
 def test_actual_family_chains_and_qualified_same_father(self):
  for role in('zhi','kai','zhan','yun','bi','jian','xie','hao','shu'):self.assertEqual(self.sm[self.roles[role]]['parent_person_id'],self.roles['yixin']);self.assertIn(self.sm[self.roles[role]]['parent_connection']['type'],('shared_father_through_sibling','shared_father_through_sibling_chain'))
  self.assertEqual(self.sm[self.roles['can']]['parent_person_id'],self.roles['jin']);self.assertEqual(self.sm[self.roles['zuan']]['parent_person_id'],self.roles['jin']);self.assertEqual(self.sm[self.roles['bing']]['parent_person_id'],self.roles['old_yizong']);self.assertNotIn(self.roles['yinsu'],self.sm)
 def test_literal_and_source_restored_names_actual_components(self):
  ns=[n for d in self.docs.values()for n in d.get('records',[])];self.assertEqual(len(ns),29);self.assertTrue(all(source_component_valid(n,self.actual,ROOT)for n in ns))
  for role in {n['component_source_binding']['role']for n in ns}:
   rows=[n for n in ns if n['person_id']==self.roles[role]]
   if role=='yinsu':self.assertEqual([(n['surname'],n['ming'])for n in rows],[('殷','蕭')])
   else:self.assertEqual({n['surname']for n in rows},{None,'劉'})
  for bad in(None,[], 'bad',{'component_source_binding':None}):self.assertFalse(core.component_valid(bad,self.actual,ROOT))
 def test_actual_bundles_for_every_new_source_individual(self):
  with scope(ROOT):
   for role in self.c['new_names']:
    b=bundle(self.roles[role],root=ROOT,include_provisional=True,catalog=self.catalog);self.assertEqual(b['canonical_person_id'],self.roles[role]);self.assertTrue(b['mentions']);self.assertTrue(b['name_components'])
 def test_old_or_new_in_memory_marker_metadata_or_text_change_rejected(self):
  for case in('old','new','metadata','body','tuple','human'):
   ch=copy.deepcopy(self.actual)
   if case=='old':ch['paragraphs'][7]['mentions'][0]['person_id']=self.roles['jin']
   if case=='new':next(m for p in ch['paragraphs']for m in p['mentions']if m.get('source_role_key')=='yixin-unit:jin')['person_id']=self.roles['can']
   if case=='metadata':ch['annotation']['additional_annotation_phase']['unlisted_key']=True
   if case=='body':ch['paragraphs'][9]['text']=ch['paragraphs'][9]['text'].replace('三十年','二十年',1)
   if case=='tuple':ch['paragraphs'][9]['mentions']=tuple(ch['paragraphs'][9]['mentions'])
   if case=='human':ch['annotation']['additional_annotation_phase']['human_reviewed']=0
   self.assertTrue(core.source_errors(ch,ROOT),case)
 def test_unrelated_or_unknown_bundle_without_song051_retains_old_behavior(self):
  pid='abc_def_123';person={'id':pid,'label':'合成測試人物','aliases':[],'evidence':[],'historicity':'historical_tradition'}
  with tempfile.TemporaryDirectory()as t:
   b=bundle(pid,root=Path(t),include_provisional=True,catalog=({pid:person},[]));self.assertEqual(b['canonical_person_id'],pid)
   with self.assertRaises(ValueError):bundle('zzz_zzz_zzz',root=Path(t),catalog=({},[]))
 def test_missing_chapter_cannot_be_filled_from_root(self):
  ns=[n for d in self.docs.values()for n in d.get('records',[])];n=next(n for n in ns if n.get('surname_basis'))
  self.assertFalse(core.component_valid(n,None,ROOT));self.assertFalse(source_component_valid(n,None,ROOT))
  with self.assertRaises(ValueError):y.project_previous_phase(ROOT,None)
  with self.assertRaises(ValueError):y.validate_surname(n,ns,{},[],ROOT)
 def test_supplied_current_paragraph_must_match_full_current_chapter(self):
  people,records=self.catalog;chapters={r['id']:r for r in records if r.get('record_type')=='marked_chapter'};paragraphs={p['id']:(r['id'],p)for r in chapters.values()for p in r['paragraphs']};a=json.loads((ROOT/core.FACTS).read_bytes())['assertions'][0];pid=a['evidence'][0]['paragraph_id'];wrong=copy.deepcopy(paragraphs);wrong[pid]=(y.CID,dict(wrong[pid][1],text='bad'));self.assertFalse(core.family_valid(a,wrong,chapters,ROOT));badchapters=dict(chapters);badchapters[y.CID]=self.prior;self.assertFalse(core.family_valid(a,paragraphs,badchapters,ROOT))
if __name__=='__main__':unittest.main()
