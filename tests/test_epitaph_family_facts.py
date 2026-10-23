import unittest,json,copy,hashlib
from pathlib import Path
try:
 from scripts.epitaph_family_facts import errors
 from scripts.validate_corpus import source_age_number
except ImportError:
 from epitaph_family_facts import errors
 from validate_corpus import source_age_number
ROOT=Path(__file__).resolve().parents[1]
class EpitaphFacts(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'corpus/epitaph-wangminzhi/full.json').read_text());self.rs=[json.loads(p.read_text())for p in (ROOT/'corpus/epitaph-wangminzhi').glob('full-*.json')if not p.name.endswith('identities.json')]
  self.a=next(r for r in self.rs if r['record_type']=='person_assertion_set')['assertions'];self.e=next(r for r in self.rs if r['record_type']=='person_life_event_assertion_set')['events'][0];self.ns=next(r for r in self.rs if r['record_type']=='person_name_component_set')['records'];self.ads=next(r for r in self.rs if r['record_type']=='person_address_assertion_set')['assertions']
 def valid(self):return not errors({self.c['id']:self.c},self.rs)
 def test_positive(self):self.assertTrue(self.valid())
 def test_reverse_father(self):
  a=self.a[0];a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(self.valid())
 def test_grandfather_not_father(self):self.a[1]['predicate']='father';self.assertFalse(self.valid())
 def test_invent_fathers_father(self):
  a=copy.deepcopy(self.a[1]);a['subject_person_id']=self.a[0]['object_person_id'];self.a.append(a);self.assertFalse(self.valid())
 def test_ordinal_two(self):self.a[0]['qualifiers']['birth_order']['ordinal']=2;self.assertFalse(self.valid())
 def test_sibling_reverse(self):
  o=self.a[3]['qualifiers']['relative_birth_order'];o['older_person_id'],o['younger_person_id']=o['younger_person_id'],o['older_person_id'];self.assertFalse(self.valid())
 def test_sibling_absolute_order(self):self.a[3]['qualifiers']['relative_birth_order']['younger_ordinal']=2;self.assertFalse(self.valid())
 def test_sibling_shared_mother(self):self.a[3]['qualifiers']['shared_mother']=True;self.assertFalse(self.valid())
 def test_spouse_biological_mother(self):self.a[2]['predicate']='mother';self.assertFalse(self.valid())
 def test_wrong_mention(self):self.a[0]['evidence'][0]['object_person_mention_id']=self.a[1]['evidence'][0]['object_person_mention_id'];self.assertFalse(self.valid())
 def test_wrong_offset(self):self.c['paragraphs'][0]['mentions'][1]['start']+=1;self.assertFalse(self.valid())
 def test_trim_quote(self):self.a[0]['evidence'][0]['quote']=self.a[0]['evidence'][0]['quote'][1:];self.assertFalse(self.valid())
 def test_wrong_source(self):self.a[0]['evidence'][0]['source_id']='different-source';self.assertFalse(self.valid())
 def test_no_original_image_upgrade(self):self.c['source']['transcription_witness']['original_stone_or_rubbing_image_verified']=True;self.assertFalse(self.valid())
 def test_no_birth(self):self.c['annotation']['age_assertions'][0]['birth_year']=331;self.assertFalse(self.valid())
 def test_age_29(self):self.c['annotation']['age_assertions'][0]['value']=29;self.assertFalse(self.valid())
 def test_death_year_wrong(self):self.e['normalized_date']['year']=359;self.e['normalized_date']['era_year']=359;self.assertFalse(self.valid())
 def test_death_subject_father(self):self.e['person_id']=self.a[0]['object_person_id'];self.assertFalse(self.valid())
 def test_death_month_wrong(self):self.e['epitaph_date_parts']['month']=4;self.assertFalse(self.valid())
 def test_death_day_wrong(self):self.e['epitaph_date_parts']['day']=10;self.assertFalse(self.valid())
 def test_burial_inherits_death_date(self):self.ads[1]['date_expression']=self.e['date_expression'];self.assertFalse(self.valid())
 def test_burial_normalized(self):self.ads[1]['normalized_date']=self.e['normalized_date'];self.assertFalse(self.valid())
 def test_wife_zi_not_ming(self):
  n=next(n for n in self.ns if n.get('zi')=='女式');n['ming']='女式';self.assertFalse(self.valid())
 def test_unstated_surname(self):next(n for n in self.ns if n['ming']=='興之')['surname']='王';self.assertFalse(self.valid())
 def test_sibling_names_swap_ids(self):
  x,y=self.ns[-2:];x['person_id'],y['person_id']=y['person_id'],x['person_id'];self.assertFalse(self.valid())
 def test_missing_binding(self):del self.c['annotation']['epitaph_fact_binding'];self.assertFalse(self.valid())
 def test_negative_clause_even_rehashed(self):
  p=self.c['paragraphs'][0];p['text']=p['text'].replace('之元子','非元子');b=self.c['annotation']['epitaph_fact_binding'];b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
  for a in self.a:a['qualifiers']['source_clause_binding']=copy.deepcopy(b);a['evidence'][0]['quote']=p['text']
  self.assertFalse(self.valid())
 def test_compact_numerals(self):
  for text,value in [('廿',20),('廿八',28),('卅',30),('卅九',39),('二十八',28)]:self.assertEqual(source_age_number(text),value)
  for text in ['廿十','廿零','卅十','廿八九','二廿','廿元']:self.assertIsNone(source_age_number(text))
if __name__=='__main__':unittest.main()
