from pathlib import Path
import unittest,json,copy
from scripts.received_career_roles import holding_valid,detail_valid,unassumed_valid,event_valid
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1]
class LuCareer(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((R/'corpus/sanguozhi/022-luyu.json').read_text());cls.hs=json.loads((R/'corpus/sanguozhi/022-luyu-titles.json').read_text())['holdings'];cls.ds=json.loads((R/'corpus/sanguozhi/022-luyu-source-details.json').read_text())['records'];cls.qs=cls.ch['annotation']['title_proposals'];cls.by={h['id']:h for h in cls.hs}
 def choose(self,rule,slot,recipient='subject'):return next(h for h in self.hs if h['source_career_role']['rule']==rule and h['source_career_role']['slot']==slot and h['source_career_role']['recipient_role']==recipient)
 def test_all_source_roles(self):
  self.assertEqual(len(self.hs),48);self.assertTrue(all(holding_valid(h,self.ch)for h in self.hs));self.assertEqual(len(self.ds),12);self.assertTrue(all(detail_valid(d,self.ch,self.by)for d in self.ds));self.assertTrue(all(unassumed_valid(q,self.ch)for q in self.qs if'source_career_role'in q))
 def test_each_wrong_recipient_consistent_all_public_fields(self):
  # Match person/evidence/attestation consistently to a real other role; grammatical recipient must still reject.
  for h in self.hs:
   z=copy.deepcopy(h);p=next(p for p in self.ch['paragraphs']if p['id']==z['source_career_role']['paragraph_id']);other=next((m for m in p['mentions']if m.get('kind')=='person'and m['person_id']!=h['person_id']),None)
   if other is None:continue
   z['person_id']=other['person_id'];z['evidence'][0]['person_mention_id']=other['id'];z['attestations'][0]['person_mention_id']=other['id'];self.assertFalse(holding_valid(z,self.ch),h['id'])
 def test_shared_suffix_and_no_birthplace(self):
  hs=[h for h in self.hs if'shared_title_suffix'in h];self.assertEqual({h['title']for h in hs},{'梁太守','譙太守','安平太守','廣平太守'})
  for h in hs:
   z=copy.deepcopy(h);z['title']='涿郡太守';self.assertFalse(holding_valid(z,self.ch));self.assertNotIn('native_place',h)
 def test_no_copied_death_end_or_duration_arithmetic(self):
  for h in self.hs:
   self.assertEqual(h['effective_period']['end'],dict(status='unknown',date_expression=None,evidence=[]));z=copy.deepcopy(h);z['effective_period']['end']=dict(status='source_event',date_expression='甘露二年',evidence=h['evidence']);self.assertFalse(holding_valid(z,self.ch))
  d=next(d for d in self.ds if d['kind']=='office_duration');self.assertEqual(d['values']['duration_years'],3);self.assertIsNone(d['values']['tenure_end_year']);z=copy.deepcopy(d);z['values']['tenure_end_year']=237;self.assertFalse(detail_valid(z,self.ch,self.by))
 def test_anonymous_son_no_named_recipient_and_count(self):
  d=next(d for d in self.ds if d['kind']=='unnamed_family_title_grants');self.assertEqual(d['values']['recipient_person_ids'],[]);self.assertFalse(d['values']['biological_children_only']);z=copy.deepcopy(d);z['values']['biological_children_only']=True;self.assertFalse(detail_valid(z,self.ch,self.by));z=copy.deepcopy(d);z['values']['recipient_person_ids']=[self.choose('late_advancement_and_children','sonoffice1','son1')['person_id']];self.assertFalse(detail_valid(z,self.ch,self.by));z=copy.deepcopy(d);z['values']['grants'][0]['recipient_count']=2;self.assertFalse(detail_valid(z,self.ch,self.by))
 def test_fief_count_not_revenue(self):
  d=next(d for d in self.ds if d['kind']=='fief_household_count');self.assertEqual(d['values']['total'],2300);self.assertIsNone(d['values']['actual_revenue']);z=copy.deepcopy(d);z['values']['total']=23000;self.assertFalse(detail_valid(z,self.ch,self.by))
 def test_no_three_nominated_candidates_offices_for_yu(self):
  h=self.choose('late_advancement_and_children','office2');self.assertEqual(h['title'],'司空')
  for title in ['驃騎將軍','光祿大夫','司隸校尉']:
   z=copy.deepcopy(h);z['title']=title;self.assertFalse(holding_valid(z,self.ch))
 def test_qin_posthumous_and_unassumed_chen(self):
  self.assertEqual(self.choose('noted_son_career','postoffice')['mode'],'posthumous_grant');self.assertEqual(self.choose('noted_son_career','privilege')['mode'],'posthumous_grant')
  qs=[q for q in self.qs if'source_career_role'in q];self.assertEqual({q['title']for q in qs},{'散騎','中書侍郎'})
  for q in qs:
   z=copy.deepcopy(q);z['effective_service_attested']=True;self.assertFalse(unassumed_valid(z,self.ch));z=copy.deepcopy(q);z['title']='散騎常侍';self.assertFalse(unassumed_valid(z,self.ch))
 def test_field_positions_and_source_fingerprint(self):
  for h in self.hs:
   z=copy.deepcopy(h);z['source_career_role']['scope_anchor']['start']+=1;self.assertFalse(holding_valid(z,self.ch));z=copy.deepcopy(h);z['source_career_role']['paragraph_sha256']='0'*64;self.assertFalse(holding_valid(z,self.ch))
 def test_no_later_same_title_for_duration_or_duty(self):
  d=next(d for d in self.ds if d['kind']=='office_duration');z=copy.deepcopy(d);z['values']['linked_holding_id']=self.choose('late_advancement_and_children','office1')['id'];self.assertFalse(detail_valid(z,self.ch,self.by))
  d=next(d for d in self.ds if d['kind']=='official_duty'and d['values'].get('continued_after_transfer'));z=copy.deepcopy(d);z['values']['linked_holding_id']=self.choose('power_and_restoration_series','office1')['id'];self.assertFalse(detail_valid(z,self.ch,self.by))
 def test_exact_dated_office_not_other_stage(self):
  court=self.choose('dated_court_service','office');space=self.choose('late_advancement_and_children','office2');self.assertEqual(court['effective_period']['start']['normalized_date']['year'],234);self.assertEqual(space['effective_period']['start']['normalized_date']['year'],256)
  z=copy.deepcopy(space);z['effective_period']['start']['normalized_date']=copy.deepcopy(court['effective_period']['start']['normalized_date']);z['effective_period']['start']['normalized_date']['evidence']=z['evidence'];z['effective_period']['start']['normalized_date']['original_quote']=z['evidence'][0]['quote'];self.assertFalse(holding_valid(z,self.ch))
 def test_grandson_succession_not_title_or_father(self):
  e=json.loads((R/'corpus/sanguozhi/022-luyu-career-events.json').read_text())['events'][0];self.assertTrue(event_valid(e,self.ch));self.assertIsNone(e['title']);self.assertIsNone(e['holding_id']);z=copy.deepcopy(e);z['title']='容城侯';self.assertFalse(event_valid(z,self.ch));z=copy.deepcopy(e);z['person_id']=self.choose('late_advancement_and_children','sonoffice1','son1')['person_id'];self.assertFalse(event_valid(z,self.ch))
 def test_real_central_validator_rejects_consistent_wrong_recipient_in_memory(self):
  from unittest.mock import patch
  from scripts.validate_corpus import validate
  target=R/'corpus/sanguozhi/022-luyu-titles.json';data=json.loads(target.read_text());h=next(h for h in data['holdings']if h['id']==self.choose('late_advancement_and_children','office2')['id']);p=self.ch['paragraphs'][6];other=next(m for m in p['mentions']if m['id']==h['source_career_role']['roles']['candidate1']);h['person_id']=other['person_id'];h['attestations'][0]['person_mention_id']=other['id'];h['evidence'][0]['person_mention_id']=other['id'];raw=Path.read_text
  def reading(path,*args,**kwargs):return json.dumps(data,ensure_ascii=False)if path.resolve()==target.resolve()else raw(path,*args,**kwargs)
  with patch.object(Path,'read_text',reading):errors=validate(R)
  self.assertTrue(any('來源職歷須逐原句角色'in e for e in errors))
 def test_repeated_offices_remain_distinct(self):
  yu=self.choose('early_recruitment','office1')['person_id'];hs=[h for h in self.hs if h['person_id']==yu];self.assertEqual(len([h for h in hs if h['title']=='僕射']),2);self.assertEqual(len([h for h in hs if h['title']=='吏部尚書']),2);self.assertEqual(len([h for h in hs if h['title']=='侍中']),2)
if __name__=='__main__':unittest.main()
