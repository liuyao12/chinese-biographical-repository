from pathlib import Path
import copy,json,unittest
from scripts import fixed_kanripo_fact_slots as f
from scripts.validate_corpus import normalized_date_errors
from scripts.fixed_kanripo_slot_dates import valid as direct_date_valid
from scripts.noble_transfers import noble_transfer_errors
ROOT=Path(__file__).resolve().parents[1]
class CaorenAdoptionGuards(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/sanguozhi/009-caoren-caochun.json').read_bytes());self.rows=f.records(self.ch,ROOT);self.hs={v['id']:v for v in self.rows if'attestations'in v};self.rs=[v for v in self.rows if'predicate'in v];self.chs={self.ch['id']:self.ch}
 def test_missing_or_malformed_bound_date_context_is_error_not_exception(self):
  record=next(v for v in self.rows if'normalized_date'in v);d=record['normalized_date'];self.assertEqual(normalized_date_errors(d,self.chs,ROOT,record,'death'),[])
  for bad in [None,1,['bad'],'bad',{},dict(evidence=[]),dict(evidence='bad'),dict(evidence=[1])]:
   self.assertTrue(normalized_date_errors(d,{},ROOT,bad,'death'));self.assertFalse(direct_date_valid(d,bad,self.ch,ROOT))
 def test_four_specific_rank_replacements(self):
  hs=[h for h in self.hs.values()if'transfer_basis'in h];self.assertEqual(len(hs),4)
  for h in hs:
   self.assertTrue(f.noble_replacement_valid(h,self.hs,{}, {},self.chs,ROOT));self.assertEqual(noble_transfer_errors(h,self.hs,{}, {},self.chs,root=ROOT),[]);previous=self.hs[h['previous_holding_id']];self.assertEqual(previous['effective_period']['end']['evidence'],h['effective_period']['start']['evidence']);self.assertFalse(previous['mode'].startswith('posthumous'))
  self.assertEqual({h['transfer_basis']['interpretation_status']for h in hs},{'explicit_source_transfer','contextual_source_rank_progression'})
 def test_wrong_parent_posthumous_or_missing_event_end(self):
  h=next(h for h in self.hs.values()if'transfer_basis'in h)
  for mutate in [lambda v:v.update(person_id='foreign'),lambda v:v.update(mode='posthumous_naming'),lambda v:v['effective_period'].update(end=dict(status='unknown',date_expression=None,evidence=[]))]:
   hs=copy.deepcopy(self.hs);mutate(hs[h['previous_holding_id']]);self.assertFalse(f.noble_replacement_valid(h,hs,{}, {},self.chs,ROOT))
 def test_no_parent_year_in_accession_start(self):
  for h in self.hs.values():
   if'inherited_title_binding'not in h:continue
   self.assertIsNone(h['effective_period']['start']['date_expression']);self.assertNotIn('normalized_date',h['effective_period']['start']);self.assertNotIn('normalized_date_range',h['effective_period']['start']);self.assertTrue(f.inherited_surface_valid(h,h['attestations'][0],self.ch,self.hs,self.rs,ROOT))
if __name__=='__main__':unittest.main()
