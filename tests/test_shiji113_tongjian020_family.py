# coding: utf-8
import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];W='w-zizhitongjian';B='b-zizhitongjian-020';C='c-zizhitongjian-020-han12';HU='bvb_d1z_fd0_*A';Y=HU+'A';X=Y+'A';CI=Y+'B';J=Y+'C'
def load(f):return json.loads((R/f).read_text())
def chapter():return load('corpus/zizhitongjian/020.json')
def relations():return load('corpus/zizhitongjian/020-assertions.json')['assertions']
class NanyueTongjianFamily(unittest.TestCase):
 def test_partial_primary_source_has_native_work_book_chapter(self):
  c=chapter();self.assertEqual((c['work_id'],c['book_id'],c['id']),(W,B,C));self.assertEqual(c['source']['text_scope'],'partial_chapter');self.assertEqual(len(c['paragraphs']),1);self.assertEqual(len(c['paragraphs'][0]['mentions']),9);self.assertIn('南越文王遣其子嬰齊',c['paragraphs'][0]['text']);self.assertEqual(c['text_sha256'],hashlib.sha256(c['paragraphs'][0]['text'].encode()).hexdigest())
 def test_fixed_revision_scope_and_edition_uncertainty_are_preserved(self):
  s=chapter()['source'];self.assertEqual(s['revision_id'],'80174f61e491db29f9921d0d3e54a59649419aa9');self.assertEqual(s['source_blob_sha'],'71c9f2f93a06f0869cbe807edf3f42524a9ea2a3');self.assertEqual(s['response_extent'],dict(first_line=201,last_line=350,partial_file=True));self.assertEqual(len(s['response_sha256']),64);self.assertIsNone(s['edition']);self.assertIn('SBCK',s['edition_metadata_note']);self.assertIn('WYG',s['edition_metadata_note']);self.assertFalse(s['image_verified'])
 def test_raw_commentary_is_not_inserted_into_received_text(self):
  p=chapter()['paragraphs'][0];self.assertIn('南越王胡薨謚文王',p['source_position']['raw_quote']);self.assertNotIn('南越王胡薨',p['text']);self.assertIn('蔵其先武帝璽',p['text']);self.assertNotIn('藏其先武帝璽',p['text']);self.assertEqual(p['source_position']['first_line'],305)
 def test_direct_child_phrase_supports_new_father_edge(self):
  a=next(a for a in relations()if a['id'].endswith('001'));self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),(Y,'father',HU));self.assertEqual(a['qualifiers']['source_term'],'南越文王遣其子嬰齊');self.assertEqual(a['evidence'][0]['work_id'],W)
 def test_same_person_identity_has_received_evidence_from_both_works(self):
  ds=load('corpus/zizhitongjian/020-identities.json')['decisions']
  for d in ds:self.assertEqual({e['chapter_id']for e in d['evidence']},{C,'c-shiji-113-nanyue'});self.assertFalse(d['human_reviewed'])
  d=next(d for d in ds if d['person_id']==HU);self.assertTrue(any('胡薨，謚為文王'in e['quote']for e in d['evidence']));self.assertTrue(any('南越王胡薨謚文王'in r['quote']for r in d['references']))
 def test_seal_wudi_still_identifies_zhaotuo(self):
  m=next(m for m in chapter()['paragraphs'][0]['mentions']if m['surface']=='武帝');self.assertEqual(m['person_id'],'bvb_d1z_fd0');self.assertNotEqual(m['person_id'],'yqp_nlb_p1p_ACAA')
 def test_mother_only_applies_to_explicit_child_xing(self):
  ms=[a for a in relations()if a['predicate']=='mother'];self.assertEqual([(a['subject_person_id'],a['object_person_id'])for a in ms],[(X,'3q4_zsp_jwy')]);self.assertTrue(any(a['predicate']=='spouse'and a['object_person_id']==Y for a in relations()));self.assertFalse(any(a['predicate']=='mother'and a['subject_person_id']in [CI,J]for a in relations()))
 def test_family_paths_join_four_existing_people_and_keep_missing_generation(self):
  ps={p['id']:p for p in load('registry/persons.json')['persons']};self.assertEqual(ps[Y]['family_path']['parent_person_id'],HU);self.assertEqual(ps[HU]['family_path']['ancestor_person_id'],'bvb_d1z_fd0');self.assertEqual(ps[HU]['family_path']['generation_distance'],2)
  for child in [X,CI,J]:self.assertEqual(ps[child]['family_path']['parent_person_id'],Y)
  self.assertFalse(any(p['id']=='bvb_d1z_fd0_A'for p in ps.values()))
 def test_retrospective_initial_does_not_set_all_events_to_yuanding4(self):
  c=chapter();self.assertTrue(c['paragraphs'][0]['text'].startswith('初'));self.assertFalse((R/'corpus/zizhitongjian/020-life-events.json').exists())
  for a in relations():self.assertNotIn('normalized_date',a);self.assertNotIn('date_expression',a)
 def test_retired_family_ids_are_absent_from_active_data_and_files(self):
  olds=['f4l_jyl_oqv','f4l_jyl_oqv_A','f4l_jyl_oqv_B','f4l_jyl_oqv_C'];paths=list((R/'registry').glob('*.json'))+list((R/'corpus').glob('*/*.json'))+list((R/'data/historical-tables').glob('*.json'))+[R/'data/corpus/profile-names.json']
  for p in paths:
   text=p.read_text()
   for old in olds:self.assertNotIn(old,text,str(p))
  for old in olds:
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((R/folder/(old+'.json')).exists())
 def test_api_cites_new_source_and_original_grandparent_without_stored_chain(self):
  b=load('exports/persons/'+Y+'.json');self.assertTrue(any(s['work_id']==W for s in b['sources']));self.assertTrue(any(a['predicate']=='father'and a['object_person_id']==HU for a in b['relations']));self.assertFalse('ancestors'in b);hu=load('exports/persons/'+HU+'.json');self.assertTrue(any(a['predicate']=='grandfather'and a['object_person_id']=='bvb_d1z_fd0'for a in hu['relations']))
 def test_reader_catalogue_retains_work_specific_chapter20(self):
  works=load('data/corpus/works.json')['works'];w=next(w for w in works if w['id']==W);c=load(w['catalog_path'])['chapters'][0];self.assertEqual(c['chapter_id'],C);self.assertEqual(c['number'],20);self.assertNotEqual(c['chapter_id'],'table-chapter-shiji-020');self.assertEqual(load('data/corpus/zizhitongjian/020.json')['id'],C)
if __name__=='__main__':unittest.main()
