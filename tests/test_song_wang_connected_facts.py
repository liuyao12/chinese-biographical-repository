# coding: utf-8
import unittest,json,copy,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.person_bundle import bundle,load_catalog
from scripts.era_only_dates import valid
from scripts.validate_corpus import normalized_date_errors,source_age_number
R=ROOT;P=ROOT/'tests/fixtures/connected-facts';J=lambda p:json.loads(p.read_text());read=J
OPS=J(P/'facts.json')['operations'];SNAP=J(P/'sources.json')
def records(op):
 d=J(ROOT/op['path'])
 for key in op['array'].split('.'):d=d[key]
 return d
delta={'changes':[dict(c,add=c['append']) for c in OPS if c['packet']=='wang']};ids=J(P/'wang-ids.json')
H=[x for c in delta['changes'] if c['array']=='holdings' for x in records(c) if x['id'].startswith('th-songwang7-')]
L=[x for c in delta['changes'] if c['array']=='events' for x in records(c) if x['id'].startswith('le-songwang7-')]
class SongWangConnectedFacts(unittest.TestCase):
 def test_source_quotes_ner_and_formal_records_exact(self):
  for rel in ['corpus/songshu/042.json','corpus/songshu/063-wanghua-tanshou.json']:
   d=J(ROOT/rel)
   for key,value in SNAP[rel].items():self.assertEqual(d[key],value)
  for op in OPS:
   if op['packet']=='wang':
    by={a['id']:a for a in records(op)}
    for a in op['append']:self.assertEqual(by[a['id']],a)
 def test_unreceived_titles_never_become_served_offices(self):
  for pid,line,t in [(ids['王弘'],'line059','司空'),(ids['王弘'],'line059','建安郡公'),(ids['王弘'],'line049','寧遠將軍'),(ids['王華'],'line016','驍騎將軍'),(ids['王曇首'],'line031','著作郎')]:
   self.assertFalse(any(h['person_id']==pid and h['title']==t and any(a['paragraph_id'].endswith(line)for a in h['attestations'])for h in H))

 def test_posthumous_distinct_from_lifetime_and_names(self):
  hua=[h for h in H if h['person_id']==ids['王華'] and h['title']in ['散騎常侍','衞將軍']and h['mode']=='posthumous_grant'];self.assertEqual(len(hua),2)
  self.assertEqual(len([h for h in H if h['mode']=='posthumous_naming']),3)

 def test_death_does_not_end_all_titles(self):
  ends=[h for h in H if h['effective_period']['end']['status']!='unknown'];self.assertEqual([(h['person_id'],h['title'])for h in ends],[(ids['王弘'],'司徒')]);self.assertEqual(ends[0]['effective_period']['end']['date_expression'],'六年')

 def test_no_age_derived_birth_and_no_civil_registration_age(self):
  ages=[a for c in delta['changes']if c['array']=='annotation.age_assertions'for a in c['add']];self.assertEqual(sorted(a['value']for a in ages),[13,43,54]);self.assertTrue(all(a['birth_year']is None for a in ages));self.assertFalse(any(x['event_type']=='birth'for x in L));self.assertFalse(any(a['evidence'][0]['paragraph_id'].endswith('line085')for a in ages))

 def test_no_invented_burial(self):
  self.assertFalse(any(a['relation']=='burial_place'for c in delta['changes']if c['array']=='assertions'for a in c['add']))

 def test_year_numbers_and_original_words_retained(self):
  d=read(P/'wang-chronology.json');self.assertTrue(any(x['scope'].startswith('王華卒') and x['year']==427 and x['original_expression']=='四年'for x in d));self.assertTrue(any(x['scope']=='王曇首卒'and x['year']==430 for x in d));self.assertTrue(any(x['scope']=='太保／中書監／其年薨'and x['year']==432 for x in d));self.assertTrue(all(x['year']is None for x in d if x['original_expression'].endswith(('中','末'))))

 def test_wrong_regnal_arithmetic_rejected(self):
  n=next(x['normalized_date']for x in L if 'normalized_date'in x and 'regnal_year_mapping'in x['normalized_date']);bad=copy.deepcopy(n);bad['year']+=1;bad['era_year']+=1;self.assertTrue(normalized_date_errors(bad));self.assertFalse(normalized_date_errors(n))

