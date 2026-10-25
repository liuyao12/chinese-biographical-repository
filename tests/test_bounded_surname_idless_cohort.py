"""Optional IDs in unrelated legacy names must not weaken the required cohort."""
from pathlib import Path
import json,copy,unittest
ROOT=Path(__file__).resolve().parents[1]
class IdlessCohort(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  scope=json.loads((ROOT/'tests/fixtures/elided-surname-source-scope.json').read_text());rows=[json.loads((ROOT/rel).read_text())for rel in scope['native_paths']]
  cls.names=[n for r in rows if r.get('record_type')=='person_name_component_set'for n in r['records']];cls.chapters={r['id']:r for r in rows if r.get('record_type')=='marked_chapter'};cls.assertions=[a for r in rows if r.get('record_type')=='person_assertion_set'for a in r['assertions']]
  cls.target=next(n for n in cls.names if n.get('bounded_source_name_binding',{}).get('key')=='legacy-peikai'and not n.get('surname_basis'))
 def check(self,names):
  from scripts.bounded_source_surname import valid
  return valid(self.target,names,self.chapters,self.assertions,ROOT)
 def test_real_legacy_idless_name_coexists(self):
  legacy=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records'];row=next(n for n in legacy if'id'not in n)
  self.assertTrue(self.check(self.names+[copy.deepcopy(row)]));self.assertNotIn('id',row)
 def test_required_missing_duplicate_and_wrong_value_rejected(self):
  rid=self.target['id'];without=[n for n in self.names if n.get('id')!=rid];self.assertFalse(self.check(without));self.assertFalse(self.check(self.names+[copy.deepcopy(self.target)]))
  changed=copy.deepcopy(self.names);next(n for n in changed if n.get('id')==rid)['ming']='不相干字';self.assertFalse(self.check(changed))
 def test_required_missing_id_not_treated_as_unrelated_replacement(self):
  changed=copy.deepcopy(self.names);next(n for n in changed if n.get('id')==self.target['id']).pop('id');self.assertFalse(self.check(changed))
if __name__=='__main__':unittest.main()
