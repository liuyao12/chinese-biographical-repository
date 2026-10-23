# coding: utf-8
"""Actual fixed witnesses plus negative role/frame/day mutations; no name/ID lookup."""
import unittest,json,copy,hashlib
from pathlib import Path
from scripts.archived_parallel_death import valid,date_parts_valid
from scripts.biography_family_clause import valid as family_valid
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
class ArchivedExecutionTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch={c['id']:c for k in ['jiong','yi']for c in [load('corpus/jinshu/059-'+k+'.json')]};cls.paras={p['id']:(c['id'],p)for c in cls.ch.values()for p in c['paragraphs']};cls.events=[e for k in ['jiong','yi']for e in load('corpus/jinshu/059-'+k+'-life-events.json')['events']if 'normalized_date'in e];cls.kin=[a for k in ['jiong','yi']for a in load('corpus/jinshu/059-'+k+'-assertions.json')['assertions']]
 def yi(self):return copy.deepcopy(next(e for e in self.events if 'source_date_parts'in e))
 def test_both_actual_years_and_local_death_day(self):
  self.assertEqual({e['normalized_date']['year']for e in self.events},{302,304})
  for e in self.events:self.assertTrue(valid(e['normalized_date'],e,self.ch,ROOT))
  self.assertTrue(date_parts_valid(self.yi(),self.ch,ROOT))
 def test_wrong_year_is_not_an_alternative_frame(self):
  e=self.yi();e['normalized_date'].update(year=303,era_year=303);self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_shift_all_role_positions_even_with_new_retained_fragments(self):
  e=self.yi();b=e['normalized_date']['archived_death_year'];raw=(ROOT/b['archive']['raw_file']).read_text()
  for key in ['event_anchor','victim_anchor','actor_anchor','year_anchor']:
   a=b[key];a['start']+=1;a['end']+=1;a['quote']=raw[a['start']:a['end']]
  self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_incomplete_fixed_unit(self):
  e=self.yi();u=e['normalized_date']['archived_death_year']['archive']['complete_units'][0];u['raw']=u['raw'][:500];u['raw_end']=u['raw_start']+500;u['sha256']=hashlib.sha256(u['raw'].encode()).hexdigest();self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_hidden_editorial_origin(self):
  e=self.yi();ch=copy.deepcopy(self.ch);b=e['normalized_date']['archived_death_year']['origin'];p=next(p for p in ch[b['chapter_id']]['paragraphs']if p['id']==b['paragraph_id']);p['annotator']='synthetic';self.assertFalse(valid(e['normalized_date'],e,ch,ROOT))
 def test_actor_is_not_victim(self):
  e=self.yi();b=e['normalized_date']['archived_death_year'];b['origin']['person_mention_id']=b['origin']['actor_person_mention_id'];self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_deposition_day_not_death_day(self):
  e=self.yi();e['source_date_parts']['day']=25;self.assertFalse(date_parts_valid(e,self.ch,ROOT))
 def test_rebound_death_day_still_must_match_actual_words(self):
  e=self.yi();e['source_date_parts']['day']=25;e['normalized_date']['archived_death_year']['local_month_day_confirmation']['day']=25;self.assertFalse(date_parts_valid(e,self.ch,ROOT))
 def test_competing_annal_is_not_erased(self):
  e=self.yi();del e['normalized_date']['archived_death_year']['rejected_context'];self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_table_row_is_independent_numeric_anchor(self):
  e=self.yi();r=e['normalized_date']['references'][0];r['full_row']=r['full_row'].replace('304','303');self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_unrelated_local_date_scope(self):
  e=self.yi();e['normalized_date']['archived_death_year']['local_month_day_confirmation']['person_mention_id']=e['normalized_date']['archived_death_year']['origin']['actor_person_mention_id'];self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_rejected_placement_year_is_numeric_but_not_promoted(self):
  e=self.yi();b=e['normalized_date']['archived_death_year'];self.assertEqual(b['rejected_context']['year_placement']['year'],303);b['rejected_context']['year_placement']['year']=302;self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_era_table_response_preserves_actual_bytes(self):
  e=self.yi();r=e['normalized_date']['references'][0];normalized=hashlib.sha256((ROOT/r['archived_file']).read_text().encode()).hexdigest();self.assertNotEqual(normalized,r['response_sha256']);r['response_sha256']=normalized;self.assertFalse(valid(e['normalized_date'],e,self.ch,ROOT))
 def test_calendar_components_are_integers_not_booleans(self):
  e=self.yi();e['source_date_parts']['month']=True;self.assertFalse(date_parts_valid(e,self.ch,ROOT))
 def test_every_actual_direct_family_clause(self):
  self.assertEqual(len(self.kin),8)
  for a in self.kin:self.assertTrue(family_valid(a,self.paras,self.kin),a['id'])
 def test_same_mother_does_not_supply_ordinal_or_named_mother(self):
  a=copy.deepcopy(next(a for a in self.kin if a['predicate']=='brother'));a['qualifiers']['relative_birth_order']={'older_person_id':a['object_person_id']};self.assertFalse(family_valid(a,self.paras,self.kin));a['qualifiers'].pop('relative_birth_order');a['qualifiers']['mother_person_id']='synthetic_mother';self.assertFalse(family_valid(a,self.paras,self.kin))
 def test_child_list_does_not_imply_absolute_order(self):
  a=copy.deepcopy(next(a for a in self.kin if 'recalled_three_sons'in a['qualifiers']['source_clause_binding']['rule']));a['qualifiers']['birth_order']={'ordinal':1};self.assertFalse(family_valid(a,self.paras,self.kin))
 def test_murdering_actor_is_not_childs_father(self):
  a=copy.deepcopy(next(a for a in self.kin if 'son_after_named_murder'in a['qualifiers']['source_clause_binding']['rule']));b=a['qualifiers']['source_clause_binding'];p=self.paras[a['evidence'][0]['paragraph_id']][1];m=next(m for m in p['mentions']if m['id']==b['roles']['actor']);a['object_person_id']=m['person_id'];a['evidence'][0]['object_person_mention_id']=m['id'];self.assertFalse(family_valid(a,self.paras,self.kin))
 def test_ordinal_six_is_not_birth_year(self):
  a=copy.deepcopy(next(a for a in self.kin if 'birth_order'in a['qualifiers']));a['qualifiers']['birth_order']['ordinal']=5;self.assertFalse(family_valid(a,self.paras,self.kin))
 def test_rule_accepts_other_literal_person_tokens(self):
  t='侯丙，字元常，君丁之子也。';ms=[dict(id='m1',start=0,end=2,surface='侯丙',kind='person',person_id='synthetic_child'),dict(id='m2',start=7,end=9,surface='君丁',kind='person',person_id='synthetic_parent')];p=dict(id='synthetic:p1',text=t,text_layer='received_chapter',source_position=dict(revision_id=123),mentions=ms);a=dict(subject_person_id='synthetic_child',object_person_id='synthetic_parent',predicate='father',status='source_attested',human_reviewed=False,evidence=[dict(chapter_id='synthetic',paragraph_id=p['id'],quote=t,subject_person_mention_id='m1',object_person_mention_id='m2')],qualifiers=dict(source_term='君丁之子也',lineage='paternal',source_clause_binding=dict(kind='biography_family_clause',rule='close_family_direct_head_son',roles=dict(child='m1',parent='m2'),clause_start=0,clause_end=len(t),paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),revision_id=123)));self.assertTrue(family_valid(a,{p['id']:('synthetic',p)}));quoted=copy.deepcopy(p);quoted['text']='「'+t+'」'
  for m in quoted['mentions']:m['start']+=1;m['end']+=1
  a['evidence'][0]['quote']=quoted['text'];b=a['qualifiers']['source_clause_binding'];b.update(clause_start=1,clause_end=len(t)+1,paragraph_sha256=hashlib.sha256(quoted['text'].encode()).hexdigest());self.assertFalse(family_valid(a,{p['id']:('synthetic',quoted)}))
if __name__=='__main__':unittest.main()
