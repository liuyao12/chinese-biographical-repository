# coding: utf-8
from pathlib import Path
import copy,json,unittest
try:
 from scripts.song041_source_context import temporal_errors,unresolved_kin_errors,kin_clause_valid,same_year_birth_day_conflict_valid,marital_birth_context_valid
 from scripts.validate_corpus import normalized_date_errors
 from scripts.life_event_dates import date_decision_errors
except ImportError:
 from song041_source_context import temporal_errors,unresolved_kin_errors,kin_clause_valid,same_year_birth_day_conflict_valid,marital_birth_context_valid
 from validate_corpus import normalized_date_errors
 from life_event_dates import date_decision_errors
R=Path(__file__).resolve().parents[1]
class Song041KinLifeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/songshu/041-parents.json').read_text());c1=json.loads((R/'corpus/songshu/001-parents-reference.json').read_text());cls.chapters={c['id']:c for c in[cls.c,c1]};cls.paragraphs={p['id']:(c['id'],p)for c in[cls.c,c1]for p in c['paragraphs']};cls.people={p['id']for p in json.loads((R/'registry/persons.json').read_text())['persons']};cls.temporal=json.loads((R/'corpus/songshu/041-parents-temporal.json').read_text());cls.relations=json.loads((R/'corpus/songshu/041-parents-kinship-assertions.json').read_text())['assertions'];cls.life=[e for f in('041-parents-life-events.json','001-parents-reference-life-events.json')for e in json.loads((R/'corpus/songshu'/f).read_text())['events']]
 def test_native_time_contexts_and_non_event_boundaries(self):
  self.assertEqual(temporal_errors(self.temporal,self.chapters,self.people,normalized_date_errors,{e['id']:e for e in self.life}),[]);self.assertEqual(len(self.temporal['records']),15)
  rows={r['id']:r for r in self.temporal['records']};self.assertEqual(rows['ta-song041-103']['normalized_date']['year'],416);self.assertEqual(rows['ta-song041-110']['duration']['operator'],'gt');self.assertIsNone(rows['ta-song041-110']['normalized_date']);self.assertTrue(rows['ta-song041-111']['prospective']);self.assertIsNone(rows['ta-song041-111']['duration'])
  self.assertTrue(temporal_errors(self.temporal,self.chapters,self.people,normalized_date_errors,{}))
  for identifier,field,value in [('ta-song041-110','normalized_date',rows['ta-song041-109']['normalized_date']),('ta-song041-111','duration',{'value':100}),('ta-song041-105','person_id','3qs_nqa_ioa_AA'),('ta-song041-109','source_term','永初元年')]:
   t=copy.deepcopy(self.temporal);row=next(r for r in t['records']if r['id']==identifier);row[field]=value;self.assertTrue(temporal_errors(t,self.chapters,self.people,normalized_date_errors,{e['id']:e for e in self.life}))
 def test_same_year_different_month_day_conflict_not_general_bypass(self):
  d=json.loads((R/'corpus/songshu/041-parents-birth-date-decisions.json').read_text())['decisions'][0];events={e['id']:e for e in self.life};self.assertEqual(date_decision_errors(d,events,[],self.people),[])
  selected=[events[x]for x in d['candidate_event_ids']];self.assertTrue(same_year_birth_day_conflict_valid(d,selected,[(363,363),(363,363)]))
  for mutate in ('preferred','wrongyear','death','sameday','unknown_scope'):
   dd=copy.deepcopy(d);ee=copy.deepcopy(events)
   if mutate=='preferred':dd['preferred_event_id']=d['candidate_event_ids'][0];dd['status']='editorial_provisional'
   elif mutate=='wrongyear':ee[d['candidate_event_ids'][1]]['normalized_date'].update(year=364,era_year=364)
   elif mutate=='death':ee[d['candidate_event_ids'][1]]['event_type']='death'
   elif mutate=='sameday':ee[d['candidate_event_ids'][1]]['source_term']=ee[d['candidate_event_ids'][0]]['source_term']
   else:dd['comparison_scope']='anything'
   self.assertTrue(date_decision_errors(dd,ee,[],self.people),mutate)
 def test_unresolved_dishun_never_creates_a_parent_or_ordinal(self):
  r=self.c['annotation']['unresolved_kinship_references'][0];self.assertEqual(unresolved_kin_errors(r,self.chapters,self.people),[])
  for key,value in [('father_person_id','r5n_x7v_cwf_A'),('generation_difference',-2),('preferred_reference_person_id','r5n_x7v_cwf_AA'),('source_kin_term','從子')]:
   bad=copy.deepcopy(r);bad[key]=value;self.assertTrue(unresolved_kin_errors(bad,self.chapters,self.people))
  self.assertFalse(any(a['subject_person_id']=='lc5_nwz_ikf'and a['predicate']in('father','adoptive_father')for a in self.relations))
 def test_ritual_and_stepfamily_roles_have_literal_edges_not_biological_guesses(self):
  byid={a['id']:a for a in self.relations}
  for key in('a-song041-kin-009','a-song041-kin-006-xiao'):
   a=byid[key];self.assertTrue(kin_clause_valid(a,self.paragraphs,self.relations))
   for field,value in [('subject_person_id','r5n_x7v_cwf_A'),('object_person_id','3qs_nqa_ioa_AA')]:
    bad=copy.deepcopy(a);bad[field]=value;self.assertFalse(kin_clause_valid(bad,self.paragraphs,self.relations))
  a=copy.deepcopy(byid['a-song041-kin-006-xiao']);a['qualifiers']['biological_lineage']='maternal';self.assertFalse(kin_clause_valid(a,self.paragraphs,self.relations));a=copy.deepcopy(byid['a-song041-kin-009']);a['qualifiers']['legal_adoption_status']='adopted';self.assertFalse(kin_clause_valid(a,self.paragraphs,self.relations))
 def test_marital_context_requires_explicit_birth_and_both_marriage_partners(self):
  a=next(a for a in self.relations if a['id']=='a-song041-kin-016-daolian');self.assertTrue(marital_birth_context_valid(a,self.paragraphs,self.relations))
  for predicate in ('mother','spouse'):
   self.assertFalse(marital_birth_context_valid(a,self.paragraphs,[r for r in self.relations if r['predicate']!=predicate]))
  bad=copy.deepcopy(a);bad['subject_person_id']='ph1_ms8_hyq_ABA';self.assertFalse(marital_birth_context_valid(bad,self.paragraphs,self.relations))
 def test_all59_dispositions_and_life_place_age_boundaries(self):
  d=json.loads((R/'source-evidence/song041-kinlife/consumption-disposition.json').read_text());self.assertEqual(len(d['records']),59)
  known={x['id']for x in self.relations+self.life+self.c['annotation']['age_assertions']+self.temporal['records']+self.c['annotation']['unresolved_kinship_references']}
  known.update(x['id']for x in json.loads((R/'corpus/songshu/041-parents-addresses.json').read_text())['assertions'])
  self.assertTrue(all(set(r['record_ids']).issubset(known)for r in d['records']))
  self.assertEqual(len(self.life),7);deaths=[x for x in self.life if x['event_type']=='death'];self.assertEqual(len(deaths),5)
  self.assertTrue(all(x.get('normalized_date')is None for x in deaths if x['person_id']in('3qs_nqa_ioa_AA','r5n_x7v_cwf_AA','lc5_nwz_ikf')))
  ages=self.c['annotation']['age_assertions'];self.assertEqual({a['value']for a in ages},{21,81});self.assertTrue(all(a['birth_year']is None for a in ages))
  addresses=json.loads((R/'corpus/songshu/041-parents-addresses.json').read_text())['assertions'];self.assertEqual(len(addresses),12);self.assertFalse(any('／'in a['place']['source_name']for a in addresses));self.assertFalse(any(a['place']['source_name']=='五百戸'for a in addresses));self.assertTrue(all(a['place']['modern_identification']is None for a in addresses))
if __name__=='__main__':unittest.main()
