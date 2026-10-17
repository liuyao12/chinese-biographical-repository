# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def paragraph(book,n):return next(p for p in load('corpus/shiji/'+book+'.json')['paragraphs']if p['id'].endswith(':p'+str(n).zfill(3)))
class HanCalendarIdentities(unittest.TestCase):
 def test_calendar_reference_keeps_exact_words_and_unverified_images(self):
  ds=[d for d in load('corpus/shiji/108-equivalences.json')['decisions']if d['id']in ['eq-shiji108-calendar-husui','eq-shiji108-calendar-qian']]
  self.assertEqual(len(ds),2)
  for d in ds:
   self.assertEqual(d['person_ids'],[d['canonical_person_id']]);self.assertTrue(d['identity_materialized']);r=d['references'][0];self.assertEqual(r['revision_id'],1373695);self.assertIn('大中大夫公孫卿、壺遂、太史令司馬遷',r['quote']);self.assertFalse(r['image_verified']);self.assertEqual(len(r['response_sha256']),64)
 def test_taishigong_father_and_son_do_not_collapse(self):
  p=paragraph('130',4);self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='太史公'),'pme_eis_xqi_*A*AAAA');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='遷'),'pme_eis_xqi_*A*AAAAA')
  p=paragraph('108',14);self.assertEqual({m['person_id']for m in p['mentions']if m['surface']in ['太史公','余']},{'pme_eis_xqi_*A*AAAAA'})
 def test_bangu_appendices_keep_text_layer(self):
  for book,n in [('006',111),('112',30)]:
   p=paragraph(book,n);self.assertEqual(p['text_layer'],'witness_appended_bangu_note');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='司馬遷'),'pme_eis_xqi_*A*AAAAA')
 def test_husui_dialogue_and_memorial_name_are_same_with_titles_preserved(self):
  for n in [9,10]:self.assertEqual(next(m['person_id']for m in paragraph('130',n)['mentions']if m['surface']=='壺遂'),'hmj_pm8_38e')
  self.assertTrue(paragraph('130',9)['text'].startswith('上大夫壺遂'));self.assertIn('壺遂官至詹事',paragraph('108',14)['text'])
 def test_self_references_stay_in_wanghui_speech(self):
  p=paragraph('108',10)
  for pos in [38,58,72]:
   m=next(m for m in p['mentions']if m['start']==pos);self.assertEqual(m['surface'],'臣');self.assertEqual(m['person_id'],'z2v_oh4_mhm');self.assertLess(p['text'].index('恢曰'),pos);self.assertLess(pos,p['text'].index('於是下恢廷尉'))
  p=paragraph('108',2);pos=p['text'].index('臣等六人');self.assertFalse(any(m['start']==pos for m in p['mentions']))
 def test_tianwang_is_the_recorded_official_not_new_person(self):
  p=paragraph('108',9);m=next(m for m in p['mentions']if m['surface']=='天王');self.assertEqual(m['person_id'],'2a2_j2z_xyc')
  h=next(h for h in load('corpus/shiji/108-titles.json')['holdings']if h['id']=='th-shiji108-033');self.assertEqual(h['person_id'],m['person_id']);self.assertEqual(h['attestations'][0]['person_mention_id'],m['id'])
 def test_four_retired_ids_removed_from_registry_and_public_json(self):
  ids={p['id']for p in load('registry/persons.json')['persons']}
  for pid in ['sxq_1wd_ih9','51v_myd_2cd','ddp_ol8_1w5','xch_o3n_p09']:
   self.assertNotIn(pid,ids)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(pid+'.json')).exists())
 def test_reference_is_readable_in_both_profiles(self):
  for pid in ['hmj_pm8_38e','pme_eis_xqi_*A*AAAAA']:
   p=load('data/corpus/profiles/'+pid+'.json');d=next(d for d in p['reading_decisions']if d['id'].startswith('eq-shiji108-calendar-'));self.assertIn('oldid=1373695',d['references'][0]['url']);self.assertFalse(d['human_reviewed'])
