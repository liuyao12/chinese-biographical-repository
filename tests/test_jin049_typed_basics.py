import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
from scripts.fixed_jin049_jikang_rendered_comparison import CH,BASE,validate_source,source_errors,_typed
from scripts.age_context import age_context_valid
ROOT=Path(__file__).resolve().parents[1]
class Jin049TypedBasics(unittest.TestCase):
 def setUp(self):self.ch=json.loads((ROOT/CH).read_bytes())
 def test_actual_source_and_scope(self):
  self.assertTrue(validate_source(self.ch,ROOT));self.assertNotIn('景元',''.join(p['text']for p in self.ch['paragraphs']));self.assertEqual(len(self.ch['paragraphs']),17)
 def test_ages_context(self):
  ev={x['id']:x for x in json.loads((ROOT/'corpus/jinshu/049-jikang-rendered-comparison-life-events.json').read_bytes())['events']}
  ages=self.ch['annotation']['age_assertions'];self.assertEqual([x['value']for x in ages],[40,13,8]);self.assertTrue(all(age_context_valid(a,ev)for a in ages));self.assertTrue(all(a['birth_year']is None and a['date_expression']is None for a in ages))
  a=copy.deepcopy(ages[1]);a['age_context']={'kind':'at_death','life_event_id':ev[next(iter(ev))]['id']};self.assertFalse(age_context_valid(a,ev))
 def test_wrong_age_birth_year_or_subject(self):
  for key,val in [('value',41),('birth_year',224),('person_id','wrong'),('source_number','十三')]:
   c=copy.deepcopy(self.ch);c['annotation']['age_assertions'][0][key]=val;self.assertTrue(source_errors(c,ROOT))
 def test_birthplace_and_wrong_office_or_death_end_rejected(self):
  contract=_typed(ROOT);read=Path.read_bytes
  for filename,change in [('addresses',lambda d:d['assertions'][0].update(relation='birth_place')),('titles',lambda d:d['holdings'][0].update(title='太僕')),('titles',lambda d:d['holdings'][0]['effective_period']['end'].update(status='source_event',date_expression='死亡')),('life-events',lambda d:d['events'][0].update(date_expression='景元中'))]:
   path=ROOT/('corpus/jinshu/049-jikang-rendered-comparison-'+filename+'.json');d=json.loads(read(path));change(d);raw=json.dumps(d,ensure_ascii=False).encode()
   with patch.object(Path,'read_bytes',lambda p:raw if p==path else read(p)):self.assertTrue(source_errors(self.ch,ROOT),filename)
 def test_untouched_original_source(self):
  for field,value in [('human_reviewed',True),('model','wrong')]:
   c=copy.deepcopy(self.ch);c['annotation'][field]=value;self.assertTrue(source_errors(c,ROOT))
if __name__=='__main__':unittest.main()
