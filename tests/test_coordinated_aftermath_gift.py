# coding: utf-8
"""共同侍從與亂事後死亡的受限追贈；所有反證僅deepcopy記憶體。"""
from pathlib import Path
import copy,json,hashlib,unittest
from scripts.posthumous_gifts import posthumous_gift_valid
from scripts.subject_continuation import coordinated_attendance_aftermath_subject_valid
ROOT=Path(__file__).resolve().parents[1]
CH=json.loads((ROOT/'corpus/jinshu/039.json').read_text());PARA=next(p for p in CH['paragraphs']if p['id']=='c-jinshu-039-wangxun-feng:xu-full:l110')
HOLD=next(h for h in json.loads((ROOT/'corpus/jinshu/039-titles.json').read_text())['holdings']if h['id']=='th-wang27-xunsui-jinzi')
EVENTS={e['id']:e for e in json.loads((ROOT/'corpus/jinshu/039-life-events.json').read_text())['events']}
def valid(h=None,p=None,events=None):
 h=copy.deepcopy(HOLD)if h is None else h;p=copy.deepcopy(PARA)if p is None else p
 return posthumous_gift_valid(h,{p['id']:(CH['id'],p)},{m['id']:(CH['id'],p['id'],m)for m in p['mentions']},EVENTS if events is None else events)
def refresh(h,p,events):
 text=p['text'];h['evidence'][0]['quote']=text;h['posthumous_basis']['source_term']=text;h['posthumous_basis']['paragraph_sha256']=hashlib.sha256(text.encode()).hexdigest();h['effective_period']['start']['evidence']=h['evidence'];h['posthumous_basis']['evidence']=h['evidence'];events[h['posthumous_basis']['death_event_id']]['evidence']=copy.deepcopy(h['evidence'])

class CoordinatedAftermathGift(unittest.TestCase):
 def test_actual_full_paragraph_and_posthumous_only(self):
  self.assertTrue(valid());self.assertEqual(len(HOLD['evidence'][0]['quote']),269);self.assertIn('王導、荀崧',HOLD['evidence'][0]['quote']);self.assertEqual(HOLD['mode'],'posthumous_grant');self.assertNotIn('追',HOLD['posthumous_basis']['grant_term'])
 def test_no_fake_year_or_death_ended_offices(self):
  self.assertIsNone(HOLD['effective_period']['start']['date_expression']);self.assertNotIn('normalized_date',HOLD['effective_period']['start']);self.assertEqual(HOLD['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]})
  self.assertEqual(EVENTS[HOLD['posthumous_basis']['death_event_id']]['source_term'],'峻平後卒')
 def test_nearest_temporal_actor_companion_authority_not_recipient(self):
  c=HOLD['posthumous_basis']['subject_context'];ms={m['id']:m for m in PARA['mentions']}
  for mid in [c['temporal_actor_mention_id'],*c['companion_mention_ids'],c['authority_mention_id']]:
   h=copy.deepcopy(HOLD);h['person_id']=ms[mid]['person_id'];self.assertFalse(valid(h))
 def test_wrong_lead_or_topic_cannot_override_first_named_subject(self):
  for field in ['lead_subject_mention_id','topic_mention_id']:
   h=copy.deepcopy(HOLD);c=h['posthumous_basis']['subject_context'];c[field]=c['companion_mention_ids'][0];self.assertFalse(valid(h))
 def test_companion_order_and_roles_are_not_a_free_bypass_list(self):
  h=copy.deepcopy(HOLD);h['posthumous_basis']['subject_context']['companion_mention_ids'].reverse();self.assertFalse(valid(h))
  h=copy.deepcopy(HOLD);c=h['posthumous_basis']['subject_context'];c['authority_mention_id']=c['companion_mention_ids'][0];self.assertFalse(valid(h))
 def test_temporal_short_form_requires_same_prior_disturbance_actor(self):
  h=copy.deepcopy(HOLD);c=h['posthumous_basis']['subject_context'];c['temporal_actor_mention_id']=c['lead_subject_mention_id'];self.assertFalse(valid(h))
  p=copy.deepcopy(PARA);actor=HOLD['posthumous_basis']['subject_context']['temporal_actor_mention_id'];next(m for m in p['mentions']if m['id']==actor)['person_id']='synthetic-other-actor';self.assertFalse(valid(p=p))
 def test_changed_authority_or_unresolved_role_rejected(self):
  p=copy.deepcopy(PARA);mid=HOLD['posthumous_basis']['subject_context']['authority_mention_id'];next(m for m in p['mentions']if m['id']==mid)['kind']='unresolved';self.assertFalse(valid(p=p))
 def test_added_competing_named_subject_inside_clause_rejected(self):
  p=copy.deepcopy(PARA);p['mentions'].append({'id':'test-only-foreign','kind':'person','person_id':'test-only-foreign','start':245,'end':247,'surface':'石頭'});self.assertFalse(valid(p=p))
 def test_missing_wrong_person_birth_or_wrong_death_term_rejected(self):
  self.assertFalse(valid(events={}))
  for field,value in [('person_id','test-other'),('event_type','birth'),('source_term','卒'),('date_expression','太興初')]:
   events=copy.deepcopy(EVENTS);events[HOLD['posthumous_basis']['death_event_id']][field]=value;self.assertFalse(valid(events=events))
 def test_living_grant_and_living_usage_rejected(self):
  h=copy.deepcopy(HOLD);h['mode']='grant';self.assertFalse(valid(h))
  h=copy.deepcopy(HOLD);h['effective_period']['start']['event_type']='grant';self.assertFalse(valid(h))
  h=copy.deepcopy(HOLD);h['attestations'][0]['usage']='narrative';self.assertFalse(valid(h))
 def test_bad_grant_or_attestation_position_rejected(self):
  h=copy.deepcopy(HOLD);h['posthumous_basis']['grant_term']='追贈金紫光祿大夫';self.assertFalse(valid(h))
  h=copy.deepcopy(HOLD);h['attestations'][0]['start']-=1;self.assertFalse(valid(h))
 def test_death_after_grant_or_wrong_death_anchor_rejected(self):
  h=copy.deepcopy(HOLD);a=h['posthumous_basis']['death_anchor'];a['start']+=1;a['surface']=a['surface'][1:];self.assertFalse(valid(h))
  h=copy.deepcopy(HOLD);h['posthumous_basis']['death_anchor'],h['posthumous_basis']['grant_anchor']=h['posthumous_basis']['grant_anchor'],h['posthumous_basis']['death_anchor'];self.assertFalse(valid(h))
 def test_full_paragraph_hash_revision_and_layer_are_guarded(self):
  for field,value in [('paragraph_sha256','bad'),('source_revision',1)]:
   h=copy.deepcopy(HOLD);h['posthumous_basis'][field]=value;self.assertFalse(valid(h))
  p=copy.deepcopy(PARA);p['text_layer']='commentary';self.assertFalse(valid(p=p))
 def test_no_cutting_others_out_of_quote_to_pass(self):
  h=copy.deepcopy(HOLD);h['evidence'][0]['quote']='峻平後卒，贈金紫光祿大夫';h['posthumous_basis']['source_term']=h['evidence'][0]['quote'];self.assertFalse(valid(h))
 def test_clause_boundaries_not_arbitrary_intervening_text(self):
  h=copy.deepcopy(HOLD);p=copy.deepcopy(PARA);events=copy.deepcopy(EVENTS);pos=h['posthumous_basis']['subject_context']['attendance_anchor']['end'];p['text']=p['text'][:pos]+'，'+p['text'][pos+1:];refresh(h,p,events);self.assertFalse(valid(h,p,events))
 def test_mentions_order_does_not_replace_source_positions(self):
  p=copy.deepcopy(PARA);p['mentions'].reverse();self.assertTrue(valid(p=p))
 def test_unlayered_speech_cannot_inherit_biography_topic(self):
  h=copy.deepcopy(HOLD);p=copy.deepcopy(PARA);events=copy.deepcopy(EVENTS);i=p['text'].index('解音樂');p['text']=p['text'][:i]+'曰'+p['text'][i+1:];refresh(h,p,events);self.assertFalse(valid(h,p,events))
 def test_same_linguistic_structure_uses_source_names_not_hardcoded_people(self):
  h=copy.deepcopy(HOLD);p=copy.deepcopy(PARA);events=copy.deepcopy(EVENTS);ctx=h['posthumous_basis']['subject_context'];roles={ctx['antecedent_actor_mention_id']:'趙玄',ctx['temporal_actor_mention_id']:'玄'}
  for m in p['mentions']:
   if m.get('person_id')==h['person_id']and m['surface']=='邃':roles[m['id']]='甲'
  for m in sorted(p['mentions'],key=lambda m:-m['start']):
   if m['id']in roles:
    word=roles[m['id']];self.assertEqual(len(word),m['end']-m['start']);p['text']=p['text'][:m['start']]+word+p['text'][m['end']:];m['surface']=word
  for field in ['disturbance_anchor','attendance_anchor','place_anchor','temporal_anchor']:
   a=ctx[field];a['surface']=p['text'][a['start']:a['end']]
  b=h['posthumous_basis'];a=b['death_anchor'];a['surface']=p['text'][a['start']:a['end']];b['death_term']=a['surface'];event=events[b['death_event_id']];event['source_term']=a['surface'];event['date_expression']=ctx['temporal_anchor']['surface'];refresh(h,p,events);self.assertTrue(valid(h,p,events))

if __name__=='__main__':unittest.main()
