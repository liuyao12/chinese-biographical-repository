# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def chapter():return read('corpus/shiji/099.json')
def decisions():return [d for d in read('corpus/shiji/099-identities.json')['decisions'] if d['id'].startswith('d-shiji099-emperor-')]
def new_mentions():
 mids={mid for d in decisions() for e in d['evidence'] for mid in e['mention_ids']}
 return [m for p in chapter()['paragraphs'] for m in p['mentions'] if m['id'] in mids]
class LiushuEmperorContextTests(unittest.TestCase):
 def test_forty_eight_mentions_resolve_to_four_contextual_people(self):
  ms=new_mentions();self.assertEqual(len(ms),48)
  self.assertEqual({pid:sum(m['person_id']==pid for m in ms) for pid in {m['person_id'] for m in ms}},{'yqp_nlb_p1p_A':40,'ao3_0fy_d45_AAAA':1,'yqp_nlb_p1p_AA':5,'wjt_htu_081_A':2})
 def test_qin_inner_speech_and_hui_successor_do_not_inherit_gaozu(self):
  ms={m['id']:m for m in new_mentions()}
  self.assertEqual(ms['c-shiji-099-liushu:m008-0088']['person_id'],'ao3_0fy_d45_AAAA')
  for mid in ['m018-0042','m018-0130','m018-0157','m019-0033','m019-0046']:self.assertEqual(ms['c-shiji-099-liushu:'+mid]['person_id'],'yqp_nlb_p1p_AA')
  self.assertEqual(ms['c-shiji-099-liushu:m017-0017']['person_id'],'yqp_nlb_p1p_A')
 def test_direction_verbs_and_hypothetical_offices_are_not_person_marks(self):
  c=chapter()
  for num,start in [(2,141),(8,147),(14,167),(14,178),(18,78),(6,180),(6,231)]:
   p=next(p for p in c['paragraphs'] if p['id'].endswith(':p'+f'{num:03d}'))
   self.assertFalse(any(m['kind']=='person' and m['start']<=start<m['end'] for m in p['mentions']),(num,start))
 def test_every_new_anchor_has_matching_registry_and_source_evidence(self):
  people={p['id']:p for p in read('registry/persons.json')['persons']}
  for m in new_mentions():
   p=people[m['person_id']];self.assertTrue(any(m['id'] in a['mention_ids'] and a['surface']==m['surface'] for a in p['aliases']))
   self.assertTrue(any(e.get('mention_id')==m['id'] and e['quote']==m['surface'] for e in p['evidence']))
  ps={p['id']:p for p in chapter()['paragraphs']}
  for d in decisions():
   self.assertFalse(d['human_reviewed'])
   for e in d['evidence']:
    self.assertEqual(e['quote'],ps[e['paragraph_id']]['text']);self.assertTrue(e['mention_ids'])
 def test_generation_reading_and_unborn_descendants_stay_unresolved(self):
  c=chapter();m=next(m for p in c['paragraphs'] for m in p['mentions'] if m['id']=='c-shiji-099-liushu:m003-0021')
  self.assertIsNone(m['person_id']);self.assertEqual(m['kind'],'unresolved')
  p=next(p for p in c['paragraphs'] if p['id'].endswith(':p006'))
  self.assertTrue(all(m['person_id'] is None for m in p['mentions'] if m['surface']=='外孫'))
 def test_source_text_and_existing_anchor_count_remain_consistent(self):
  c=chapter();self.assertEqual(len(c['paragraphs']),21);self.assertEqual(sum(len(p['mentions']) for p in c['paragraphs']),220)
  for p in c['paragraphs']:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
