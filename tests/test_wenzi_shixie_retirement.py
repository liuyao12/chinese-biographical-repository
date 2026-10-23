import json,hashlib,copy,tempfile,unittest
from pathlib import Path
from scripts.retired_person_ids import retired_person_ids,assert_not_retired,allocation_conflicts
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1];OLD='rm7_r3k_g21';KEEP='cno_x3i_mx4';BASE='source-evidence/wenzi-shixie-identity-merge';DID='d-wenzi-shixie-cross-event'
class WenziRetirement(unittest.TestCase):
 def test_old_current_identity_absent_permanently_reserved_no_alias(self):
  cat=load_catalog(R);self.assertNotIn(OLD,cat[0]);self.assertEqual(cat[0][KEEP]['label'],'士燮');self.assertFalse(cat[0][KEEP].get('id_aliases'));self.assertIn(OLD,retired_person_ids(R));self.assertTrue(allocation_conflicts(OLD,retired_person_ids(R)));self.assertTrue(allocation_conflicts(OLD+'_A',retired_person_ids(R)))
  with self.assertRaises(ValueError):assert_not_retired(OLD,R)
  with self.assertRaises(ValueError):bundle(OLD,root=R,catalog=cat)
 def test_five_source_anchors_and_literal_father_son_distinction(self):
  p27=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());p32=json.loads((R/'corpus/shiji/032.json').read_text());p39=json.loads((R/'corpus/shiji/039.json').read_text());ms={m['id']:(p,m)for c in [p27,p32,p39]for p in c['paragraphs']for m in p['mentions']};expected=['c-shiji-032-qi:m057-0133','c-shiji-039-jin:m111-0051','c-sanguozhi-027-wangchang:unit005:m0417','c-sanguozhi-027-wangchang:unit006:m0003','c-sanguozhi-027-wangchang:unit006:m0084']
  for mid in expected:
   p,m=ms[mid];self.assertEqual(m['person_id'],KEEP);self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
  self.assertEqual(ms['c-sanguozhi-027-wangchang:unit006:m0089'][1]['person_id'],'23d_95b_500');self.assertNotEqual(KEEP,'rf6_xhq_gm3');self.assertIn('若范匄對秦客',ms[expected[2]][0]['text'])
 def test_resolved_case_binds_materialized_equivalence_and_supported_decision(self):
  c=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());case=next(x for x in c['annotation']['resolved_identity_cases']if x['id']=='case-sgz027-wenzi-shixie-existing-duplicate');self.assertEqual(case['person_id'],KEEP);self.assertEqual(case['identity_equivalence_decision_ids'],['eq-wenzi-shixie-materialized']);eq=json.loads((R/'corpus/sanguozhi/027-wenzi-equivalences.json').read_text())['decisions'][0];self.assertEqual(eq['person_ids'],[KEEP]);self.assertTrue(eq['identity_materialized']);d=next(x for x in json.loads((R/'corpus/sanguozhi/027-wangchang-identities.json').read_text())['decisions']if x['id']==DID);self.assertEqual(d['scope'],'cross_chapter');self.assertEqual(len(d['chapter_ids']),3)
 def test_fixed_ancient_commentary_explicit_name_role_and_counterexample(self):
  raw=(R/BASE/'primary/guoyu012-2150401.wikitext').read_bytes();meta=json.loads((R/BASE/'primary/guoyu012-metadata.json').read_text());self.assertEqual(hashlib.sha256(raw).hexdigest(),meta['raw_sha256']);text=raw.decode();self.assertIn('文子，范燮。',text);self.assertIn('欒書將中軍，士燮佐之。',text);self.assertIn('匄，范文子之子宣子也。',text)
 def test_retirement_receipt_failclosed_mixed_owner_wrong_status_and_old_registration(self):
  receipt=json.loads((R/BASE/'annotation-chain.json').read_text());decision=next(x for x in json.loads((R/'corpus/sanguozhi/027-wangchang-identities.json').read_text())['decisions']if x['id']==DID)
  for mutate in ['valid','mixed','unresolved','registered_old']:
   with tempfile.TemporaryDirectory()as t:
    root=Path(t);(root/'source-evidence/case').mkdir(parents=True);(root/'registry').mkdir();(root/'corpus/book').mkdir(parents=True);rc=copy.deepcopy(receipt);d=copy.deepcopy(decision);people=[{'id':KEEP}]
    if mutate=='mixed':rc['family_id']='family-fake'
    if mutate=='unresolved':d['status']='unresolved'
    if mutate=='registered_old':people.append({'id':OLD})
    (root/'source-evidence/case/annotation-chain.json').write_text(json.dumps(rc));(root/'registry/persons.json').write_text(json.dumps({'persons':people}));(root/'corpus/book/001-identities.json').write_text(json.dumps({'record_type':'person_identity_decision_set','decisions':[d]}))
    if mutate=='valid':self.assertIn(OLD,retired_person_ids(root))
    else:
     with self.assertRaises(ValueError):retired_person_ids(root)
 def test_current_endpoint_scan_and_no_new_family_or_biographical_facts(self):
  for area in ['corpus','registry','sources']:
   for f in (R/area).rglob('*.json'):self.assertNotIn(OLD,f.read_text(),str(f))
  for f in (R/'source-evidence').rglob('*.json'):
   if BASE in str(f):continue
   self.assertNotIn(OLD,f.read_text(),str(f))
  cat=load_catalog(R);b=bundle(KEEP,root=R,catalog=cat);self.assertEqual(b['id_aliases'],[]);self.assertEqual(b['person_ids'],[KEEP])
if __name__=='__main__':unittest.main()
