# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def paragraph(book,n):return next(p for p in load('corpus/shiji/'+book+'.json')['paragraphs']if p['id'].endswith(':p'+str(n).zfill(3)))
def cell(cid):return next(c for f in load('data/historical-tables/shiji-018.json')['fragments']for row in f['rows']for c in row['cells']if c['id']==cid)
class YingyinIdentities(unittest.TestCase):
 def test_unnamed_grandson_is_qiang_not_xian(self):
  p=paragraph('109',6);self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='潁陰侯'),'sj9_pfu_fwh');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='孫'),'sj9_pfu_fwh_AA');self.assertFalse(any(m['start']<=p['text'].index('屏')<m['end']for m in p['mentions']))
 def test_commentary_is_separate_and_not_image_verified(self):
  ds=[d for d in load('corpus/shiji/109-equivalences.json')['decisions']if d['id'].startswith('eq-shiji109-commentary-')];self.assertEqual(len(ds),2)
  for d in ds:
   self.assertFalse(d['human_reviewed']);r=d['references'][0];self.assertEqual(r['revision_id'],2514779);self.assertEqual(r['quote'],'灌嬰之孫，名強。');self.assertFalse(r['image_verified']);self.assertEqual(len(r['response_sha256']),64)
 def test_source_grandfather_and_two_step_father_chain_survive(self):
  a=next(a for a in load('corpus/shiji/109-assertions.json')['assertions']if a['id']=='a-shiji109-003');self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('sj9_pfu_fwh_AA','grandfather','sj9_pfu_fwh'))
  ds=load('corpus/shiji/095-assertions.json')['assertions']
  self.assertTrue(any(a['subject_person_id']=='sj9_pfu_fwh_AA'and a['predicate']=='father'and a['object_person_id']=='sj9_pfu_fwh_A'for a in ds));self.assertTrue(any(a['subject_person_id']=='sj9_pfu_fwh_A'and a['predicate']=='father'and a['object_person_id']=='sj9_pfu_fwh'for a in ds));self.assertFalse(any(a['subject_person_id']=='sj9_pfu_fwh_*A'and a['predicate']=='father'for a in ds))
 def test_two_table_people_link_to_distinct_grandsons(self):
  for cid,pid in [('shiji-018-t1-r019-c06','sj9_pfu_fwh_AA'),('shiji-018-t1-r019-c07','sj9_pfu_fwh_*A')]:
   ms=cell(cid)['person_mentions'];self.assertEqual(ms[0]['person_id'],pid);self.assertEqual(ms[0]['identity_evidence'][0]['person_id'],pid)
 def test_investiture_year_difference_is_preserved(self):
  self.assertIn('元光二年',cell('shiji-018-t1-r019-c07')['text']);self.assertIn('元光三年',paragraph('095',33)['text'])
 def test_a_and_he_are_not_silently_corrected_or_merged(self):
  self.assertIn('平侯阿',paragraph('095',33)['text']);c=cell('shiji-018-t1-r019-c05');self.assertIn('平侯何',c['text']);self.assertEqual(next(m['person_id']for m in c['person_mentions']if m['surface']=='何'),'hrg_h4f_j9x')
 def test_qiang_and_xian_share_root_but_xian_keeps_missing_father(self):
  aa=load('registry/family-assemblies.json')['assemblies'];self.assertNotIn('family-yingyin-shiji109',{a['id']for a in aa});a=next(a for a in aa if a['id']=='family-guanying-shiji095');self.assertEqual(a['root_person_id'],'sj9_pfu_fwh');m=next(m for m in a['members']if m['person_id']=='sj9_pfu_fwh_*A');self.assertIsNone(m['parent_person_id']);self.assertEqual(m['intermediate_person_ids'],[None])
 def test_retired_ids_have_no_public_entry(self):
  registry={p['id']for p in load('registry/persons.json')['persons']};tables={p['id']for p in load('data/historical-tables/person-candidates.json')['persons']}
  for pid in ['gqv_vyi_jao','gqv_vyi_jao_*A','8s8_d4z_23z','3zw_jw0_h1i']:
   self.assertNotIn(pid,registry|tables)
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
