# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.posthumous_gifts import posthumous_gift_valid
from scripts.validate_corpus import normalized_date_errors
ROOT=Path(__file__).resolve().parents[1];PREFIX='corpus/weishu-weishou/024-cuixuanbo'
def read(n):return json.loads((ROOT/n).read_text())
class Cui47Consumption(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read(PREFIX+'.json');cls.hs=read(PREFIX+'-titles.json')['holdings'];cls.es=read(PREFIX+'-life-events.json')['events'];cls.h=next(h for h in cls.hs if h['id']=='th-cui53-f052');cls.e=next(e for e in cls.es if e['id']=='le-cui53-f180');cls.audit=read('source-evidence/cui53-typed-ledger.json');cls.fixture=read('tests/fixtures/cui47-consumption-guards.json');cls.pars={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']};cls.ms={m['id']:(cls.c['id'],p['id'],m)for p in cls.c['paragraphs']for m in p['mentions']}
 def test_existing_ids_and_unique_deaths(self):
  self.assertEqual(len(self.hs),self.fixture['title_count']);self.assertEqual(len(self.es),self.fixture['death_count']);self.assertEqual(sum(e['id']=='le-cui53-f159'for e in self.es),1);self.assertEqual(sum(e['id']=='le-cui53-f180'for e in self.es),1)
 def test_qualified_posthumous_not_living(self):
  self.assertEqual(self.h['mode'],'posthumous_grant');self.assertTrue(posthumous_gift_valid(self.h,self.pars,self.ms,{e['id']:e for e in self.es}));self.assertEqual(self.h['attestations'],self.fixture['old_title']['attestations']);self.assertEqual(self.h['evidence'],self.fixture['old_title']['evidence']);self.assertIsNone(self.h['effective_period']['start']['date_expression']);self.assertIsNone(self.h['posthumous_basis']['issuer']['person_id'])
 def test_no_living_grant_or_ancestor_conversion(self):
  bad=copy.deepcopy(self.h);bad['mode']='grant';self.assertFalse(posthumous_gift_valid(bad,self.pars,self.ms,{e['id']:e for e in self.es}));ancestor=next(h for h in self.hs if h['id']=='th-cui53-f034');self.assert_ancestor_attestation(ancestor)
 def test_443_is_same_death_original_wording(self):
  self.assertEqual(self.e['person_id'],'xb3_qm5_kf6');self.assertEqual(self.e['source_term'],'真君四年卒');self.assertEqual(self.e['date_expression'],'真君四年');self.assertEqual(self.e['normalized_date']['year'],443);self.assertEqual(self.e['evidence'],self.fixture['old_death']['evidence']);self.assertEqual(normalized_date_errors(self.e['normalized_date'],{self.c['id']:self.c},root=ROOT),[])
 def test_418_hong_not_replaced_by_443(self):
  e=next(e for e in self.es if e['id']=='le-cui53-f159');self.assertEqual(e,self.fixture['hong_death']);self.assertEqual(e['normalized_date']['year'],418)
 def test_wrong_polity_year_and_witness(self):
  for key,value in [('ruler_person_id','other'),('omitted_prefix','wrong')]:
   d=copy.deepcopy(self.e['normalized_date']);d['era_name_bridge'][key]=value;self.assertTrue(normalized_date_errors(d,{self.c['id']:self.c},root=ROOT))
  d=copy.deepcopy(self.e['normalized_date']);d['year']=444;self.assertTrue(normalized_date_errors(d,{self.c['id']:self.c},root=ROOT))
 def test_no_death_cutoff_or_birth(self):
  self.assertEqual([[h['id'],h['effective_period']['end']]for h in self.hs],self.fixture['old_ends']);self.assertTrue(all(a['birth_year']is None for a in self.c['annotation'].get('age_assertions',[])))
 def test_full_ledger_same_proposal_ids(self):
  self.assertEqual([r['proposal_id']for r in self.audit['records']],self.fixture['ledger_ids']);r=next(r for r in self.audit['records']if r['proposal_id']=='cui53-f052');self.assertEqual(r['native_ids'],['th-cui53-f052']);self.assertEqual(r['consumption'],'native_title_assertion');r=next(r for r in self.audit['records']if r['proposal_id']=='cui53-f180');self.assertEqual(r['native_ids'],['le-cui53-f180']);self.assertTrue(r['value']['native_abbreviation_mapping_supported'])
 def test_mirror_exact_for_two_records(self):
  d=read('source-evidence/cui53-facts-delta.json');self.assertEqual(next(h for h in d['titles']['holdings']if h['id']==self.h['id']),self.h);self.assertEqual(next(e for e in d['life']['events']if e['id']==self.e['id']),self.e)

 def test_root_column_guard_both_entries(self):
  from scripts.primary_era_abbreviation import valid
  for columns in [None,[],'bad',0,False,'missing']:
   d=copy.deepcopy(self.e['normalized_date'])
   if columns=='missing':d['references'][0].pop('columns')
   else:d['references'][0]['columns']=columns
   self.assertIs(valid(d,{self.c['id']:self.c},ROOT),False);self.assertTrue(normalized_date_errors(d,{self.c['id']:self.c},root=ROOT))

 def assert_ancestor_attestation(self,holding):
  # Retired cvr_exv_dku is not a query alias; use the reviewed fixed source anchor.
  p=next(p for p in self.c['paragraphs']if p['id']=='c-weishu-weishou-024-cuixuanbo:p001');m=next(m for m in p['mentions']if m['id']==p['id']+':m0019')
  self.assertEqual(m['surface'],'林');self.assertEqual(holding['person_id'],m['person_id']);self.assertEqual(holding['mode'],'attestation')
  self.assertEqual(holding['evidence'][0]['person_mention_id'],m['id']);self.assertEqual(holding['evidence'][0]['quote'],p['text']);self.assertEqual(holding['attestations'][0]['person_mention_id'],m['id'])
 def test_ancestor_wrong_person_or_living_grant_still_rejected(self):
  original=next(h for h in self.hs if h['id']=='th-cui53-f034')
  for key,value in [('person_id','cvr_exv_dku'),('person_id',self.h['person_id']),('mode','grant')]:
   bad=copy.deepcopy(original);bad[key]=value
   with self.assertRaises(AssertionError):self.assert_ancestor_attestation(bad)
