import unittest,json,copy,sys
from pathlib import Path
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parents[1]
from scripts.pending_research import pending_errors,validate
D=json.loads((BASE/'data/research/early-medieval-family-pending.json').read_text())
PEOPLE={x['id']for x in json.loads((BASE/'registry/persons.json').read_text())['persons']}
class Tests(unittest.TestCase):
 def test_original_and_cross_history_pending_remain_parseable(self):
  self.assertTrue({'pending-phase5-xi-song-reference','pending-phase5-suyi-death-location'} <= {r['id'] for r in D['records']});self.assertEqual(pending_errors(D,PEOPLE),[])
 def test_native_readonly_base(self):self.assertEqual(validate(BASE),[])
 def test_opaque_proposal_fields_remain_readable(self):
  d=copy.deepcopy(D);d['records'][0]['proposal']['new_source_layer']={'status':'source_attested','raw_unknown_fields':['甲',{'applied':True}]};self.assertEqual(pending_errors(d,PEOPLE),[])
 def test_missing_reverse(self):
  d=copy.deepcopy(D);p=next(iter(d['person_index']));d['person_index'][p].pop();self.assertTrue(pending_errors(d,PEOPLE))
 def test_extra_reverse(self):
  d=copy.deepcopy(D);p=next(iter(d['person_index']));extra=next(r['id']for r in d['records']if p not in r['person_ids']);d['person_index'][p].append(extra);self.assertTrue(pending_errors(d,PEOPLE))
 def test_missing_person_index_key(self):
  d=copy.deepcopy(D);del d['person_index'][next(iter(d['person_index']))];self.assertTrue(pending_errors(d,PEOPLE))
 def test_extra_person_index_key(self):
  d=copy.deepcopy(D);p=next(p for p in PEOPLE if p not in d['person_index']);d['person_index'][p]=[];self.assertTrue(pending_errors(d,PEOPLE))
 def test_old_person_id(self):
  d=copy.deepcopy(D);d['records'][0]['person_ids']=['169_279_d9c'];self.assertNotIn('169_279_d9c',PEOPLE);self.assertTrue(pending_errors(d,PEOPLE))
 def test_nested_old_person_id(self):
  d=copy.deepcopy(D);d['records'][0]['proposal']['recipient_person_id']='retired_person_id';self.assertTrue(pending_errors(d,PEOPLE))
 def test_duplicate_record(self):
  d=copy.deepcopy(D);d['records'].append(copy.deepcopy(d['records'][0]));self.assertTrue(pending_errors(d,PEOPLE))
 def test_duplicate_reverse(self):
  d=copy.deepcopy(D);p=next(iter(d['person_index']));d['person_index'][p].append(d['person_index'][p][0]);self.assertTrue(pending_errors(d,PEOPLE))
 def test_empty_person_list_is_allowed(self):
  d=copy.deepcopy(D);r=next(x for x in d['records']if not x['person_ids']);self.assertTrue(r['id']);self.assertEqual(pending_errors(d,PEOPLE),[])
 def test_active_corpus_cannot_consume_pending(self):
  import tempfile
  with tempfile.TemporaryDirectory(prefix='pending-validator-')as folder:
   root=Path(folder)
   for d in ['registry','data/research','corpus/test']:(root/d).mkdir(parents=True,exist_ok=True)
   (root/'registry/persons.json').write_text(json.dumps({'persons':[{'id':p}for p in PEOPLE]}))
   (root/'data/research/early-medieval-family-pending.json').write_text(json.dumps(D))
   (root/'corpus/test/active.json').write_text(json.dumps({'record_type':'person_assertion_set','assertions':[{'id':D['records'][0]['id'],'status':'source_attested'}]}))
   self.assertTrue(validate(root))
 def test_active_status_on_record(self):
  d=copy.deepcopy(D);d['records'][0]['status']='source_attested';self.assertTrue(pending_errors(d,PEOPLE))
 def test_active_status_on_collection(self):
  d=copy.deepcopy(D);d['status']='active_assertions';self.assertTrue(pending_errors(d,PEOPLE))
 def test_active_flag(self):
  for field in ['active','is_active','adopted','is_adopted','applied']:
   with self.subTest(field=field):
    d=copy.deepcopy(D);d['records'][0][field]=True;self.assertTrue(pending_errors(d,PEOPLE))
 def test_pending_id_as_active_record(self):self.assertTrue(pending_errors(D,PEOPLE,{D['records'][0]['id']}))
if __name__=='__main__':unittest.main(verbosity=2)
