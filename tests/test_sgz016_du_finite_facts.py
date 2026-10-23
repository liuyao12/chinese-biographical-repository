# coding:utf-8
import copy,json,unittest,sys,hashlib
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from scripts.fixed_kanripo_fact_slots import records,valid,errors
from scripts.person_bundle import load_catalog
CID='c-sanguozhi-016-duji-dushu'
class DuFiniteFactsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=load_catalog(R);cls.rows=list(cls.catalog[1]);cls.ch=next(c for c in cls.rows if c.get('id')==CID);cls.facts=records(cls.ch,R)
 def fact(self,slot):return copy.deepcopy(next(v for v in self.facts if v['fixed_source_fact_binding']['slot']==slot))
 def mutate(self,slot,fn):
  v=self.fact(slot);fn(v);self.assertFalse(valid(v,self.ch,R))
 def test_36_slots_keep_nine_kin_and_27_new_claims(self):
  self.assertEqual(len(self.facts),36);self.assertEqual(errors(R,self.rows),[]);self.assertEqual(sum('predicate'in v for v in self.facts),9)
 def test_eight_names_six_new_courtesy_two_independent_witnesses(self):
  ns=[v for v in self.facts if 'ming'in v];self.assertEqual(len(ns),8);self.assertEqual({n['zi']for n in ns},{'伯侯','務伯','務仲','務叔','元凱','世嘏','洪治','世將'});self.assertEqual(self.fact('name_kuan')['ming'],'寛');self.assertNotIn('surname_basis',self.fact('name_ji'));self.assertEqual(len(self.fact('name_yi')['surname_basis']['assertion_ids']),4)
 def test_ages_never_become_birth_year(self):
  for s,n in [('age_ji_20',20),('age_ji_62',62),('age_shu_52',52),('age_li_21',21),('age_kuan_42',42)]:
   v=self.fact(s);self.assertEqual(v['value'],n);self.assertIsNone(v['birth_year']);self.assertNotIn('normalized_date',v)
  self.assertIn('神異',self.fact('age_ji_62')['interpretation_note']);self.assertIn('書信',self.fact('age_shu_52')['interpretation_note'])
 def test_age_52_not_death_age_or_year_252(self):
  self.mutate('age_shu_52',lambda v:v.update(age_context={'kind':'at_death','life_event_id':'le-sgz016-du-death_shu'}));self.mutate('age_shu_52',lambda v:v.update(birth_year=201));self.mutate('age_shu_52',lambda v:v.update(date_expression='嘉平四年'))
 def test_courtesy_not_sibling_rank(self):
  for s in('name_shu','name_li','name_kuan'):
   self.assertNotIn('ordinal',self.fact(s));self.assertNotIn('birth_order',self.fact(s))
 def test_wrong_name_same_paragraph_and_cross_paragraph_zi(self):
  for s in('name_li','name_kuan','name_yi','name_bin'):
   self.mutate(s,lambda v:v.update(zi='務伯'))
 def test_wrongrecipient_consistently_changed_record_evidence(self):
  bad=self.fact('death_shu');other=self.fact('name_yu');bad['person_id']=other['person_id'];bad['evidence'][0]['person_mention_id']=next(m['id']for m in self.ch['paragraphs'][40]['mentions']if m.get('person_id')==other['person_id']);bad['normalized_date']['evidence']=copy.deepcopy(bad['evidence']);self.assertFalse(valid(bad,self.ch,R))
 def test_context_places_not_modernized_or_conflated(self):
  self.assertEqual(self.fact('construction_ji')['place']['source_name'],'陶河');self.assertEqual(self.fact('death_place_ji')['place']['source_name'],'孟津');self.assertEqual(self.fact('death_place_shu')['place']['source_name'],'章武郡');self.mutate('construction_ji',lambda v:v.update(relation='death_place'));self.mutate('death_place_shu',lambda v:v['place'].update(source_name='幽州'))
 def test_252_is_era_year_not_elapsed_four_or_ganlu(self):
  d=self.fact('death_shu')['normalized_date'];self.assertEqual(d['year'],252);self.assertEqual(d['source_expression'],'四年');self.assertEqual(d['regnal_year_mapping']['era_name'],'嘉平');self.assertNotIn('month',d)
  for year in(253,259):self.mutate('death_shu',lambda v:v['normalized_date'].update(year=year,era_year=year))
 def recipe_mutation(self,fn):
  p=R/'scripts/fixed_kanripo_additional_fact_slots.json';d=json.loads(p.read_text());fn(d['recipes']['sgz016-duji-dushu-kinship']);original=Path.read_text
  def read(q,*a,**kw):return json.dumps(d,ensure_ascii=False)if q==p else original(q,*a,**kw)
  with patch.object(Path,'read_text',read):
   with self.assertRaises((AssertionError,KeyError,ValueError)):records(self.ch,R)
 def test_surname_maternal_spousal_adoption_and_reversed_edge_rejected(self):
  for pred in('mother','spouse','adoptive_father'):
   self.recipe_mutation(lambda r:next(s['record']for s in r['slots']if s['slot']=='shu-father-ji').update(predicate=pred))
  def reverse(r):
   a=next(s['record']for s in r['slots']if s['slot']=='shu-father-ji');a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
  self.recipe_mutation(reverse)
 def test_cycle_and_familyid_seed_cannot_supply_surname(self):
  self.mutate('name_yi',lambda v:v['surname_basis']['assertion_ids'].append(v['surname_basis']['assertion_ids'][0]));self.mutate('name_bin',lambda v:v['surname_basis'].update(kind='family_id_surname'))
 def test_coherent_recipe_wrong_subject_rejected(self):
  def change(r):
   a=next(s['record']for s in r['slots']if s['slot']=='death_shu');a['person_id']={'$person':[43,0]};a['evidence'][0]['person_mention_id']={'$mention':[43,0]}
  self.recipe_mutation(change)
 def test_calendar_row_and_era_coherent_swap_rejected(self):
  def change(r):
   d=next(s['record']for s in r['slots']if s['slot']=='death_shu')['normalized_date'];d['year']=d['era_year']=259;d['regnal_year_mapping'].update(era_name='甘露',start_ce_year=256,end_ce_year=259);d['references'][0]['columns'].update(era_name='甘露',first_year='256',last_year='259')
  self.recipe_mutation(change)
 def test_body_date_anchor_swap_and_skipped_new_era_rejected(self):
  for text in('甘露元年','正始元年'):
   c=copy.deepcopy(self.ch);c['paragraphs'][38]['text']=text+c['paragraphs'][38]['text'];self.assertTrue(errors(R,[c]))
 def test_note_cannot_be_body_era_context(self):
  c=copy.deepcopy(self.ch);c['paragraphs'][37]['source_position']['source_layer']='received_body';self.assertFalse(valid(self.fact('death_shu'),c,R))
 def test_pin_and_native_co_shift_still_rejected(self):
  c=copy.deepcopy(self.ch);p=c['paragraphs'][40];p['text']='甲'+p['text'];self.assertFalse(valid(self.fact('death_shu'),c,R))
 def test_coherent_semantic_place_and_age_change_rejected(self):
  self.recipe_mutation(lambda r:next(s['record']for s in r['slots']if s['slot']=='construction_ji').update(relation='death_place'))
  self.recipe_mutation(lambda r:next(s['record']for s in r['slots']if s['slot']=='age_li_21').update(age_context={'kind':'during_life'}))
 def test_raw_projection_pin_recipe_coshift_rehash_cannot_replace_fixed_witness(self):
  from scripts.fixed_kanripo_projection import errors as projection_errors
  c=copy.deepcopy(self.ch);pp=R/c['annotation']['fixed_kanripo_projection_ref'];projection=json.loads(pp.read_text());rp=R/projection['raw_file'];raw='甲'+rp.read_text();digest=hashlib.sha256(raw.encode()).hexdigest();projection['raw_file_sha256']=digest
  projection['unit']['start']+=1;projection['unit']['end']+=1
  for p in projection['paragraphs']:p['raw_positions']=[x+1 for x in p['raw_positions']]
  c['source']['response_sha256']=digest;pinpath=R/'scripts/fixed_kanripo_witness_pins.json';pins=json.loads(pinpath.read_text());pins['witnesses'][projection['witness_key']]['raw_sha256']=digest
  recipepath=R/'scripts/fixed_kanripo_additional_fact_slots.json';recipes=json.loads(recipepath.read_text());recipes['recipes']['sgz016-duji-dushu-kinship']['raw_sha256']=digest
  overrides={pp:json.dumps(projection),pinpath:json.dumps(pins),recipepath:json.dumps(recipes),rp:raw};ot=Path.read_text;ob=Path.read_bytes
  def read(p,*a,**kw):return overrides[p]if p in overrides else ot(p,*a,**kw)
  def readb(p,*a,**kw):return overrides[p].encode()if p in overrides else ob(p,*a,**kw)
  with patch.object(Path,'read_text',read),patch.object(Path,'read_bytes',readb):
   self.assertEqual(projection_errors(c,R),[])
   with self.assertRaises(AssertionError):records(c,R)
 def test_unknown_years_stay_unknown(self):
  for s in('death_ji','death_stepmother','death_li','death_kuan','death_bin','death_yi'):self.assertNotIn('normalized_date',self.fact(s))
 def test_native_cli_consistent_wrongrecipient_no_disk_mutation(self):
  from scripts import validate_corpus
  path=R/'corpus/sanguozhi/016-duji-dushu-life-events.json';before=path.read_bytes();d=json.loads(before);bad=next(v for v in d['events']if v['id']=='le-sgz016-du-death_shu');other=self.fact('name_yu');bad['person_id']=other['person_id'];bad['evidence'][0]['person_mention_id']=next(m['id']for m in self.ch['paragraphs'][40]['mentions']if m.get('person_id')==other['person_id']);bad['normalized_date']['evidence']=copy.deepcopy(bad['evidence']);original=Path.read_text
  def read(p,*a,**kw):return json.dumps(d,ensure_ascii=False)if p==path else original(p,*a,**kw)
  with patch.object(Path,'read_text',read),patch.object(validate_corpus,'ROOT',R):
   original_validate=validate_corpus.validate
   with patch.object(validate_corpus,'validate',lambda:original_validate(R)):self.assertEqual(validate_corpus.main(),1)
  self.assertEqual(path.read_bytes(),before)
if __name__=='__main__':unittest.main()
