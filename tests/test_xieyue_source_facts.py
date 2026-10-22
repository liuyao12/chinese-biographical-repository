# coding:utf-8
import unittest,json,copy,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if not(ROOT/'corpus').exists():ROOT=Path(__file__).resolve().parent/'fixture'
sys.path.insert(0,str(ROOT))
from scripts.biography_family_clause import valid
from scripts.maternal_roles import maternal_role_valid
from scripts.resumed_biography_lifecycle import gift_valid,mourning_end_valid,declined_valid
class XieyueFactsTests(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'corpus/nanqishu/043-xieyue.json').read_text());self.ps={p['id']:(self.c['id'],p)for p in self.c['paragraphs']};self.ms={m['id']:(self.c['id'],p['id'],m)for p in self.c['paragraphs']for m in p['mentions']};self.rs=json.loads((ROOT/'corpus/nanqishu/043-xieyue-assertions.json').read_text())['assertions'];self.hs=json.loads((ROOT/'corpus/nanqishu/043-xieyue-titles.json').read_text())['holdings'];self.es={e['id']:e for e in json.loads((ROOT/'corpus/nanqishu/043-xieyue-life-events.json').read_text())['events']};self.proposal=self.c['annotation']['title_proposals'][-1]
 def test_source_relations(self):
  for a in self.rs:
   if a['predicate']=='maternal_role':self.assertTrue(maternal_role_valid(a,self.ps),a['id'])
   else:self.assertTrue(valid(a,self.ps,self.rs),a['id'])
 def test_reversed_and_mixed_roles_rejected(self):
  for old in self.rs[:-1]:
   a=copy.deepcopy(old);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(valid(a,self.ps,self.rs))
  a=copy.deepcopy(self.rs[0]);a['qualifiers']['source_clause_binding']['roles']['father']=a['qualifiers']['source_clause_binding']['roles']['grandfather'];self.assertFalse(valid(a,self.ps,self.rs))
 def test_four_brothers_only_relative_to_head(self):
  rs=[a for a in self.rs if a['predicate']=='brother'];self.assertEqual(len(rs),4);self.assertEqual(len({a['object_person_id']for a in rs}),1)
  for old in rs:
   a=copy.deepcopy(old);a['qualifiers']['relative_birth_order']['older_ordinal']=1;self.assertFalse(valid(a,self.ps,self.rs));a=copy.deepcopy(old);a['qualifiers']['shared_mother']=True;self.assertFalse(valid(a,self.ps,self.rs))
 def test_mother_not_birth_mother_or_fathers_spouse(self):
  rs=[a for a in self.rs if a['predicate']=='maternal_role'];self.assertEqual(len(rs),2);self.assertNotEqual(rs[0]['object_person_id'],rs[1]['object_person_id'])
  a=copy.deepcopy(rs[0]);a['qualifiers']['biological_mother']=True;self.assertFalse(maternal_role_valid(a,self.ps))
  a=copy.deepcopy(rs[0]);a['qualifiers']['father_person_id']=self.rs[0]['object_person_id'];self.assertFalse(maternal_role_valid(a,self.ps))
 def test_marriage_not_aborted_princess(self):
  a=copy.deepcopy(next(a for a in self.rs if a['predicate']=='spouse'));p=self.ps[a['evidence'][0]['paragraph_id']][1];princess=next(m for m in p['mentions']if m['surface']=='公主');self.assertIsNone(princess['person_id']);a['qualifiers']['source_clause_binding']['roles']['daughter']=princess['id'];self.assertFalse(valid(a,self.ps,self.rs))
 def test_changed_literal_even_with_fresh_hash_fails(self):
  a=copy.deepcopy(next(a for a in self.rs if a['predicate']=='spouse'));ps=copy.deepcopy(self.ps);p=ps[a['evidence'][0]['paragraph_id']][1];p['text']=p['text'].replace('以女結婚','以女未婚');a['evidence'][0]['quote']=p['text'];a['qualifiers']['source_clause_binding']['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();self.assertFalse(valid(a,ps,self.rs))
 def test_posthumous_recipient_is_resumed_topic(self):
  h=next(h for h in self.hs if h['mode']=='posthumous_grant');self.assertTrue(gift_valid(h,self.ps,self.ms,self.es));a=copy.deepcopy(h);a['person_id']=self.ms[a['posthumous_basis']['roles']['possessive']][2]['person_id'];self.assertFalse(gift_valid(a,self.ps,self.ms,self.es));a=copy.deepcopy(h);a['posthumous_basis']['roles']['possessive']=a['posthumous_basis']['roles']['head'];self.assertFalse(gift_valid(a,self.ps,self.ms,self.es))
 def test_mourning_end_not_memorial_or_death_year(self):
  h=next(h for h in self.hs if 'end_basis'in h);self.assertTrue(mourning_end_valid(h,self.ps,self.ms));a=copy.deepcopy(h);a['end_basis']['source_term']='有司奏免';self.assertFalse(mourning_end_valid(a,self.ps,self.ms));a=copy.deepcopy(h);a['effective_period']['end']['date_expression']='永泰元年';self.assertFalse(mourning_end_valid(a,self.ps,self.ms));a=copy.deepcopy(h);a['title']='司徒左長史';self.assertFalse(mourning_end_valid(a,self.ps,self.ms))
 def test_decline_not_completed_by_command(self):
  self.assertTrue(declined_valid(self.proposal,self.c));a=copy.deepcopy(self.proposal);a['outcome']='assumed';self.assertFalse(declined_valid(a,self.c));a=copy.deepcopy(self.proposal);a['resumed_decline_context']['command_issuer_mention_id']=a['person_mention_id'];self.assertFalse(declined_valid(a,self.c));self.assertFalse(any(h['title']=='長兼侍中'for h in self.hs))
 def test_dates_ages_and_places_no_inferences(self):
  self.assertEqual(self.es['le-nanqi043-xieyue-yue']['normalized_date']['year'],498)
  for age in self.c['annotation']['age_assertions']:self.assertIsNone(age['birth_year'])
  for h in self.hs:
   if 'end_basis'not in h:self.assertEqual(h['effective_period']['end']['status'],'unknown')
  self.assertFalse(any(e['event_type']=='birth'for e in self.es.values()));self.assertEqual(len(self.hs),39)
  for h in self.hs:
   for a in h['attestations']:
    if 'normalized_date_range'in a:self.assertNotIn('year',a['normalized_date_range']);self.assertEqual(a['normalized_date_range']['source_stage'],'初')
if __name__=='__main__':unittest.main()
