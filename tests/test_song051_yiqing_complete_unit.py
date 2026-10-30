from pathlib import Path
import json,copy,unittest
from scripts import wyd_song051_yixin as y
from scripts.validation_context import scope
from scripts.source_author_prefix import source_author_errors
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1]
class Yiqing(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sc=scope(ROOT);cls.sc.__enter__();cls.ch,cls.roles,cls.c,cls.docs=y.state(ROOT);cls.catalog=load_catalog(ROOT);cls.works={w['id']:w for w in json.loads((ROOT/'registry/works.json').read_bytes())['works']};cls.newworks={b['work_id']:cls.works[b['work_id']]for b in cls.c['source_work_author_bindings']}
 @classmethod
 def tearDownClass(cls):cls.sc.__exit__(None,None,None)
 def test_complete2206_and_old_stage_preserved(self):
  u=next(x for x in self.c['additional_complete_units']if x['key']=='yiqing');self.assertEqual(sum(len(x['text'])for x in u['scope']),2206);self.assertEqual(u['new_marker_count'],84)
  self.assertEqual(sum(m['kind'] in ('person','pronoun')for p in self.ch['paragraphs']for m in p['mentions']),589);self.assertEqual(sum(m['kind']=='work'for p in self.ch['paragraphs']for m in p['mentions']),5);self.assertTrue(any(p['annotation_status']=='pending'for p in self.ch['paragraphs']))
 def test_all_sixteen_source_people_have_real_bundles(self):
  for r in ['huangchu','zhao','victim','grandchild','zheng','yushi','gongqi','shijue','baozhao','ye','chuo','gun','yan','jing','ying','qian']:
   for provisional in [False,True]:
    b=bundle(self.roles['yq_'+r],ROOT,include_provisional=provisional,catalog=self.catalog);self.assertEqual(b['canonical_person_id'],self.roles['yq_'+r]);self.assertTrue(b['mentions']);self.assertTrue(b['name_components'])
 def test_literal_names_and_reference_restored_full_name(self):
  ns=self.docs['corpus/songshu/051-wyd1739-yiqing-name-components.json']['records'];a=next(n for n in ns if n['id']=='name-song051-yiqing-appellation-yq_zheng');b=next(n for n in ns if n['id']=='name-song051-yiqing-zheng-restored');self.assertIsNone(a['ming']);self.assertEqual((b['surname'],b['ming'],b['zi']),('鄭','鮮之','道子'));self.assertEqual(a['person_id'],b['person_id']);self.assertIn('未經書影',b['references'][0]['access_scope_display'])
 def test_two_original_ming_values_and_explicit_display_choice(self):
  ns=self.docs['corpus/songshu/051-wyd1739-yiqing-name-components.json']['records'];self.assertEqual({n['ming']for n in ns if n['person_id']==self.roles['yq_ye']},{'曄','燁'});r=self.docs['corpus/songshu/051-wyd1739-yiqing-preferred-name-readings.json']['readings'][0];self.assertEqual(r['preferred_value'],'曄');self.assertEqual(r['coverage'],'listed_records_only')
 def test_raw_fathers_brothers_and_no_spouse_birth_mother(self):
  aa=self.docs['corpus/songshu/051-wyd1739-yiqing-assertions.json']['assertions'];self.assertEqual(len(aa),8);self.assertEqual(sum(a['predicate']=='father'for a in aa),2);self.assertEqual(sum(a['predicate']=='brother'for a in aa),5);self.assertFalse(next(a for a in aa if a['predicate']=='spouse')['qualifiers']['birth_mother_asserted']);self.assertTrue(all(a['qualifiers']['relative_birth_order']['older_ordinal']is None for a in aa if a['predicate']=='brother'))
 def test_work_titles_only_reference_and_four_bound_authors(self):
  self.assertEqual(len(self.c['referenced_work_markers']),5);self.assertEqual(len(self.newworks),4);self.assertEqual(source_author_errors(self.newworks,{self.ch['id']:self.ch},ROOT),[])
  self.assertTrue(all(w['status']=='referenced_only'and w['books']==[]for w in self.newworks.values()))
  z=self.works['w-zhouli-song051-reference'];self.assertFalse(z.get('source_author_attributions'))
 def author_changed(self,fn):
  ws=copy.deepcopy(self.newworks);w=ws['w-xuzhou-xianxian-song051-reference'];fn(w['source_author_attributions'][0]);return source_author_errors(ws,{self.ch['id']:self.ch},ROOT)
 def test_wanghong_in_aside_is_not_author(self):
  p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p033'));m=next(m for m in p['mentions']if m.get('person_id')==self.roles['yq_wang_hong']);self.assertTrue(self.author_changed(lambda e:e.update(author_person_id=m['person_id'],author_mention_id=m['id'],author_surface=m['surface'])))
 def test_author_borrowed_other_paragraph_rejected(self):self.assertTrue(self.author_changed(lambda e:e.update(paragraph_id=self.ch['paragraphs'][34]['id'],quote=self.ch['paragraphs'][34]['text'])))
 def test_missing_or_changed_whole_chapter_rejected(self):
  self.assertFalse(y.work_author_valid(next(iter(self.newworks.values()))['source_author_attributions'][0],next(iter(self.newworks.values())),None,ROOT));bad=copy.deepcopy(self.ch);bad['paragraphs'][32]['text']=bad['paragraphs'][32]['text'].replace('撰徐州','為徐州');self.assertTrue(source_author_errors(self.newworks,{bad['id']:bad},ROOT))
 def test_courtesy_fragments_have_actual_adjacent_tail_head(self):
  b=y.materialize(self.c['courtesy_fragment_groups'][0],self.roles);self.assertEqual([f['surface']for f in b['fragments']],['子','流']);self.assertEqual(b['value'],'子流')
 def altered_group_rejects(self,fn):
  c=copy.deepcopy(self.c);fn(c['courtesy_fragment_groups'][0]);self.assertRaises((ValueError,KeyError,StopIteration),y.validated_yiqing_context,ROOT,self.ch,self.roles,c,self.docs)
 def test_courtesy_wrong_owner_reverse_gap_shift_rejected(self):
  self.altered_group_rejects(lambda b:b.update(role='yq_ye'))
  self.altered_group_rejects(lambda b:b['fragments'].reverse())
  self.altered_group_rejects(lambda b:b['fragments'][1].update(paragraph_id=self.ch['paragraphs'][40]['id']))
  self.altered_group_rejects(lambda b:b['fragments'][0].update(start=208))
 def test_external_full_name_anchor_cannot_point_at_editorial_heading(self):
  c=copy.deepcopy(self.c);c['reference_supported_name_components'][0]['reference_head_anchor'].update(start=3,end=6);self.assertRaises(ValueError,y.validated_yiqing_context,ROOT,self.ch,self.roles,c,self.docs)
 def test_external_name_wrong_role_rejected(self):
  c=copy.deepcopy(self.c);c['reference_supported_name_components'][0]['role']='yq_wang_hong';self.assertRaises(ValueError,y.validated_yiqing_context,ROOT,self.ch,self.roles,c,self.docs)
if __name__=='__main__':unittest.main()
