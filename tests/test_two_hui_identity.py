# coding:utf-8
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.two_hui_identity import validate,OLD,DID
from scripts.fixed_wikisource_units import source_errors
from scripts.person_bundle import load_catalog,bundle
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
from scripts.person_ids import allocate_person_id
R=Path(__file__).resolve().parents[1];CH='corpus/sanguozhi/023-peiqian-ws2376966.json'
class TwoHuiIdentity(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.ch=json.loads((R/CH).read_bytes());c.pid=validate(R);c.catalog=load_catalog(R)
 def test_current_identity_and_actual_source_API(self):
  self.assertEqual(set(self.catalog[0]),{p['id']for p in json.loads((R/'registry/persons.json').read_bytes())['persons']});self.assertNotIn(OLD,self.catalog[0]);b=bundle(self.pid,root=R,catalog=self.catalog,include_provisional=True);self.assertEqual(b['canonical_person_id'],self.pid);self.assertEqual(b['id_aliases'],[]);self.assertTrue({'c-sanguozhi-010-xunyu-xunyou-jiaxu','c-sanguozhi-023-peiqian-ws2376966'}<={m['chapter_id']for m in b['mentions']});self.assertFalse(any(m.get('person_id')==OLD for m in b['mentions']));self.assertEqual(b['person_ids'],[self.pid]);self.assertFalse(any(p['id']==OLD for p in b['persons']))
  with self.assertRaisesRegex(ValueError,'未知人物 ID'):bundle(OLD,root=R,catalog=self.catalog)
 def test_retirement_reservation_does_not_resolve_an_alias(self):
  ids=retired_person_ids(R);self.assertIn(OLD,ids);self.assertTrue(allocation_conflicts(OLD,ids));self.assertFalse(self.catalog[0][self.pid].get('id_aliases'))
  token='047850e7d'+'a0bc1de2f'
  with patch('scripts.person_ids.secrets.choice',side_effect=list(token)):self.assertEqual(allocate_person_id(set(self.catalog[0]),root=R),'a0b_c1d_e2f')
 def test_original_metadata_full_notes_and_reverse_union(self):
  before=json.loads((R/'source-evidence/two-hui-identity/original-fields.json').read_bytes())['person_records_before'];actor=self.catalog[0][self.pid];self.assertEqual([x['identity_note']for x in actor['identity_review_history']],[x['identity_note']for x in before]);self.assertEqual([x['review']for x in actor['identity_review_history']],[x['review']for x in before]);self.assertFalse(any(x['human_reviewed']for x in actor['identity_review_history']))
  for original in before:
   for e in original['evidence']:self.assertIn(e,actor['evidence'])
   for alias in original['aliases']:self.assertTrue(any(a['surface']==alias['surface']and set(alias['mention_ids'])<=set(a['mention_ids'])for a in actor['aliases']))
 def test_literal_anchor_has_same_ID_and_name_not_just_nearby_person(self):
  c=json.loads((R/'corpus/sanguozhi/010.json').read_bytes());p=next(p for p in c['paragraphs']if p['id'].endswith(':u029'));m=next(m for m in p['mentions']if m['id'].endswith(':m0324'));self.assertEqual((m['surface'],m['start'],m['end']),('裴徽',324,326));self.assertEqual(m['person_id'],self.pid);self.assertIn('裴徽通彼我之懐為二家騎驛',p['text'])
 def test_missing_or_misdirected_single_source_and_metadata_loss_fail(self):
  raw=Path.read_bytes
  for case in ['endpoint','reverse','note','review','unknown','case']:
   reg=json.loads(raw(R/'registry/persons.json'));actor=next(x for x in reg['persons']if x['id']==self.pid);c10=json.loads(raw(R/'corpus/sanguozhi/010.json'));c=copy.deepcopy(self.ch)
   if case=='endpoint':next(m for p in c10['paragraphs']for m in p['mentions']if m['id'].endswith('u029:m0324'))['person_id']='kbq_kjc_n2f_A'
   elif case=='reverse':actor['evidence']=[e for e in actor['evidence']if not e['mention_id'].endswith('u029:m0324')]
   elif case=='note':actor['identity_review_history'][0]['identity_note']='刪除先前限定'
   elif case=='review':actor['identity_review_history'][0]['review']='human_reviewed'
   elif case=='unknown':actor['historicity']='invented'
   else:c['annotation']['resolved_identity_reviews']=[]
   def reader(p):
    if p.resolve()==(R/'registry/persons.json').resolve():return json.dumps(reg,ensure_ascii=False).encode()
    if p.resolve()==(R/'corpus/sanguozhi/010.json').resolve():return json.dumps(c10,ensure_ascii=False).encode()
    return raw(p)
   with patch.object(Path,'read_bytes',reader):self.assertTrue(source_errors(c,R),case)
 def test_no_other_family_rekey_or_he_shao_adoption(self):
  cases=self.ch['annotation']['unresolved_identity_cases'];self.assertTrue(any(c['id']=='case-sgz023-he-shao-deferred'and c['status']=='unresolved'for c in cases));self.assertEqual({x['person_id']for x in self.ch['annotation']['resolved_identity_reviews']},{self.pid});self.assertEqual(DID,'d-sgz023-hui-explicit-xuncan-reference')
if __name__=='__main__':unittest.main()
