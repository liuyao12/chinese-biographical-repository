from pathlib import Path
import copy,json,unittest
from unittest.mock import patch
from scripts import fixed_kanripo_fact_slots as f
from scripts.surname_from_father import validate as surname_valid
ROOT=Path(__file__).resolve().parents[1]
class CaorenChunSuccessionSurname(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/sanguozhi/009-caoren-caochun.json').read_bytes());self.rows=f.records(self.ch,ROOT);self.hs={r['id']:r for r in self.rows if'attestations'in r};self.rs=[r for r in self.rows if'predicate'in r];self.new=[h for h in self.hs.values()if h.get('inherited_title_binding',{}).get('kind')=='fixed_kanripo_named_father_rank_succession']
 def check(self,h):return f.inherited_surface_valid(h,h['attestations'][0],self.ch,self.hs,self.rs,ROOT)
 def test_four_source_qualified_rank_links(self):
  self.assertEqual(len(self.new),4)
  for h in self.new:
   self.assertTrue(self.check(h));p=self.hs[h['inheritance']['predecessor_holding_id']];self.assertEqual(h['title'],p['title']);self.assertFalse(p['mode'].startswith('posthumous'));self.assertIsNone(h['effective_period']['start']['date_expression'])
 def test_wrong_posthumous_parent_and_inherited_year(self):
  h=self.new[0];post=next(p for p in self.hs.values()if p['mode']=='posthumous_naming')
  x=copy.deepcopy(h);x['inheritance']['predecessor_holding_id']=post['id'];self.assertFalse(self.check(x))
  x=copy.deepcopy(h);x['inherited_title_binding']['father_assertion_id']='not_the_father';self.assertFalse(self.check(x))
  dated=next(p for p in self.hs.values()if'normalized_date_range'in p['effective_period']['start']);x=copy.deepcopy(h);x['effective_period']['start']['normalized_date_range']=dated['effective_period']['start']['normalized_date_range'];self.assertFalse(self.check(x))
 def test_actual_event_reciprocal_reference(self):
  h=self.new[0];path=ROOT/'corpus/sanguozhi/009-caoren-caochun-person-events.json';raw=path.read_bytes();payload=json.loads(raw);eid=h['inherited_title_binding']['succession_event_id'];next(v for v in payload['events']if v['id']==eid)['title_holding_id']='wrong_holding';real=f.json.loads
  def changed(v,*args,**kw):return copy.deepcopy(payload)if v==raw else real(v,*args,**kw)
  with patch.object(f.json,'loads',side_effect=changed):self.assertFalse(self.check(h))
 def test_literal_null_and_qualified_surname(self):
  names=[r for r in self.rows if'surname'in r];n=next(n for n in names if n['id']=='nc-sgz009-cc-chun-contextual-cao');literal=next(x for x in names if x['id']=='nc-sgz009-cc-chun');self.assertIsNone(literal['surname']);self.assertEqual(n['surname'],'曹');surname_valid(n,names,{self.ch['id']:self.ch},self.rs,ROOT)
  for field in ['seed_name_record_id','seed_full_name_mention_id']:
   x=copy.deepcopy(n);x['surname_basis'][field]='wrong'
   with self.assertRaises(ValueError):surname_valid(x,names,{self.ch['id']:self.ch},self.rs,ROOT)
if __name__=='__main__':unittest.main()
