"""Malformed binding boundary regression; actual received noble/date proof remains required."""
import copy,json,unittest
from pathlib import Path
from scripts.received_career_roles import holding_valid
from scripts.validate_corpus import normalized_date_errors
from scripts.fixed_zhou041_wangbao import proof
ROOT=Path(__file__).resolve().parents[1]

class ZhouDispatchBoundary(unittest.TestCase):
 def test_none_binding_returns_false(self):
  self.assertFalse(holding_valid({'source_career_role':None},{},ROOT))
 def test_string_binding_returns_false(self):
  self.assertFalse(holding_valid({'source_career_role':'not-a-binding'},{},ROOT))
 def test_list_binding_returns_false(self):
  self.assertFalse(holding_valid({'source_career_role':[]},{},ROOT))
 def test_original_non_dict_h_contract_preserved(self):
  for h in [None,'not-a-holding',[],42]:
   with self.subTest(h=h):self.assertFalse(holding_valid(h,{},ROOT))
 def test_unknown_role_kind_is_not_validated(self):
  ch,_,_=proof(ROOT)
  for h in json.loads((ROOT/'corpus/zhoushu/041-wangbao-ws2432538-titles.json').read_bytes())['holdings']:
   wrong=copy.deepcopy(h);wrong['source_career_role']['kind']='unknown_zhou041_role'
   self.assertFalse(holding_valid(wrong,ch,ROOT))
 def test_known_kind_alone_is_not_a_source_proof(self):
  self.assertFalse(holding_valid({'source_career_role':{'kind':'fixed_zhou041_explicit_noble_rank'}},{},ROOT))
 def test_actual_legal_noble_rank_records_remain_valid(self):
  ch,_,roles=proof(ROOT)
  hs=json.loads((ROOT/'corpus/zhoushu/041-wangbao-ws2432538-titles.json').read_bytes())['holdings']
  self.assertEqual(len(hs),2)
  for h in hs:self.assertEqual(h['person_id'],roles['$bao']);self.assertTrue(holding_valid(h,ch,ROOT))
 def test_actual_557_date_remains_valid_and_556_is_rejected(self):
  ch,_,_=proof(ROOT);h=json.loads((ROOT/'corpus/zhoushu/041-wangbao-ws2432538-titles.json').read_bytes())['holdings'][1]
  date=h['effective_period']['start']['normalized_date'];self.assertEqual(date['year'],557)
  self.assertEqual(normalized_date_errors(date,{ch['id']:ch},ROOT,h,'start'),[])
  wrong=copy.deepcopy(date);wrong['year']=wrong['era_year']=556
  self.assertTrue(normalized_date_errors(wrong,{ch['id']:ch},ROOT,h,'start'))

if __name__=='__main__':unittest.main()
