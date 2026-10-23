# coding: utf-8
import unittest,json,copy
from pathlib import Path
from scripts.received_biography_facts import valid,validate_surname
R=Path(__file__).resolve().parents[1];B=R/'corpus/sanguozhi';read=lambda p:json.loads(p.read_bytes())
class GuojiaTypedFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read(B/'014-guojia.json');cls.rs={k:read(B/('014-guojia-'+k+'.json')) for k in('addresses','assertions','life-events','person-events','titles','source-details','name-components')};cls.rows=[x for d in cls.rs.values()for k in('assertions','events','holdings','records')for x in d.get(k,[])if 'source_fact_frame'in x]+cls.c['annotation']['age_assertions']
 def row(self,id):return copy.deepcopy(next(x for x in self.rows if x['id']==id))
 def test_all_actual_role_bound_records(self):
  self.assertEqual(len(self.rows),30)
  for x in self.rows:
   with self.subTest(id=x['id']):self.assertTrue(valid(x,self.c,R))
 def test_same_source_surnames_not_id_derived(self):
  ns=self.rs['name-components']['records'];aa=self.rs['assertions']['assertions']
  for n in ns[1:]:validate_surname(n,ns,{self.c['id']:self.c},aa,R)
  self.assertEqual([n['surname']+n['ming']for n in ns],['郭嘉','郭奕','郭深','郭獵','郭敞'])
 def test_grandson_never_becomes_son(self):
  x=self.row('a-sgz014-guo-4');self.assertIsNone(x['qualifiers']['parent_person_id']);self.assertEqual(x['qualifiers']['intermediate_person_ids'],[None]);x['predicate']='father';self.assertFalse(valid(x,self.c,R))
 def test_wrong_parent_and_succession_direction(self):
  x=self.row('a-sgz014-guo-3');x['object_person_id']=self.row('a-sgz014-guo-1')['object_person_id'];self.assertFalse(valid(x,self.c,R))
  x=self.row('pe-sgz014-guo-succession-shen');x['person_id'],x['predecessor_person_id']=x['predecessor_person_id'],x['person_id'];self.assertFalse(valid(x,self.c,R))
 def test_death_subject_cannot_be_patron(self):
  x=self.row('le-sgz014-guo-jia-body');p=next(p for p in self.c['paragraphs']if p['id']==x['evidence'][0]['paragraph_id']);m=next(m for m in p['mentions']if m['id']==x['source_fact_frame']['roles']['patron']);x['person_id']=m['person_id'];x['evidence'][0]['person_mention_id']=m['id'];self.assertFalse(valid(x,self.c,R))
 def test_no_campaign_year_as_source_death_year(self):
  x=self.row('le-sgz014-guo-jia-body');self.assertIsNone(x['date_expression']);x['normalized_date']={'year':207};self.assertFalse(valid(x,self.c,R))
 def test_age_upper_bound_and_lifetime_are_distinct(self):
  x=self.row('age-sgz014-guo-lt40');self.assertIsNone(x['value']);self.assertEqual(x['bounds']['upper'],40);self.assertFalse(x['bounds']['upper_inclusive']);x['value']=40;self.assertFalse(valid(x,self.c,R))
  x=self.row('age-sgz014-guo-27');x['age_context']={'kind':'at_death','life_event_id':'le-sgz014-guo-jia-body'};self.assertFalse(valid(x,self.c,R))
 def test_age_not_birth_estimate(self):
  x=self.row('age-sgz014-guo-38');x['birth_year']=170;self.assertFalse(valid(x,self.c,R))
 def test_source_requests_not_grants(self):
  for id in('increase-body','increase-weishu','heir-memorial'):
   x=self.row('sd-sgz014-guo-'+id);x['values']['enactment_status']='granted';self.assertFalse(valid(x,self.c,R))
 def test_original_count_unit_and_heir_recipient(self):
  x=self.row('sd-sgz014-guo-increase-body');self.assertEqual(x['values']['increase_unit_source_name'],'尸');x['values']['increase_unit_source_name']='户';self.assertFalse(valid(x,self.c,R))
  x=self.row('sd-sgz014-guo-heir-memorial');x['person_id']='344_68f_98e';self.assertFalse(valid(x,self.c,R))
 def test_service_not_office_tenure(self):
  x=self.row('sd-sgz014-guo-duration-army');self.assertIsNone(x['values']['value']);self.assertEqual(x['values']['lower_exclusive'],10);x['values']['office_tenure']=True;self.assertFalse(valid(x,self.c,R))
 def test_recruitment_does_not_make_situ(self):
  x=self.row('pe-sgz014-guo-recruit');self.assertEqual(x['recruiting_organ_source_name'],'司徒府');self.assertFalse(x['service_attested']);x['office_title']='司徒';self.assertFalse(valid(x,self.c,R))
 def test_nomination_not_assumed_office(self):
  x=self.row('sd-sgz014-guo-nomination');self.assertEqual(x['values']['office_source_name'],'司空軍祭酒');x['values']['assumption_attested_by_this_clause']=True;self.assertFalse(valid(x,self.c,R))
 def test_posthumous_name_not_inherited_fief(self):
  x=self.row('th-sgz014-guo-posthumous');self.assertEqual(x['kind'],'honorific');self.assertEqual(x['mode'],'posthumous_naming');x['kind']='noble_rank';self.assertFalse(valid(x,self.c,R))
  self.assertTrue(all(x['title']is None for x in self.rs['person-events']['events']if x['event_type']=='noble_title_succession'))
 def test_truncated_rank_or_office_rejected(self):
  x=self.row('th-sgz014-guo-rank');x['title']='洧陽亭';f=x['source_fact_frame'];f['fields']['rank']['surface']='洧陽亭';f['fields']['rank']['end']-=1;f['scope_anchor']['surface']=f['scope_anchor']['surface'][:-1];f['scope_anchor']['end']-=1;x['attestations'][0]['surface']='洧陽亭';x['attestations'][0]['end']-=1;self.assertFalse(valid(x,self.c,R))
  x=self.row('th-sgz014-guo-chang-office');x['title']='散騎';f=x['source_fact_frame'];f['fields']['office']['surface']='散騎';f['fields']['office']['end']-=2;f['scope_anchor']['surface']=f['scope_anchor']['surface'][:-2];f['scope_anchor']['end']-=2;x['attestations'][0]['surface']='散騎';x['attestations'][0]['end']-=2;self.assertFalse(valid(x,self.c,R))
 def test_arbitrary_scope_shift_or_note_layer_rejected(self):
  x=self.row('a-sgz014-guo-2');x['source_fact_frame']['scope_anchor']['start']+=1;self.assertFalse(valid(x,self.c,R))
  x=self.row('a-sgz014-guo-4');x['source_fact_frame']['source_layer']='received_chapter';self.assertFalse(valid(x,self.c,R))
 def test_surname_no_shortcut_or_spouse(self):
  ns=self.rs['name-components']['records'];aa=self.rs['assertions']['assertions'];n=copy.deepcopy(ns[-1]);n['surname_basis']['assertion_ids']=['a-sgz014-guo-1']
  with self.assertRaises(ValueError):validate_surname(n,ns,{self.c['id']:self.c},aa,R)
  n=copy.deepcopy(ns[3]);bb=copy.deepcopy(aa);bb[1]['predicate']='spouse'
  with self.assertRaises(ValueError):validate_surname(n,ns,{self.c['id']:self.c},bb,R)
if __name__=='__main__':unittest.main()
