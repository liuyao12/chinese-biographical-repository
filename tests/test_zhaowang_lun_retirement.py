# coding:utf-8
import json,copy,tempfile,unittest,itertools,string
from pathlib import Path
from unittest.mock import patch
from scripts.retired_person_ids import retired_person_ids,assert_not_retired,allocation_conflicts
from scripts.person_ids import allocate_person_id,allocate_child_id
R=Path(__file__).resolve().parents[1];OLD='bav_adk_phh';KEEP='dkn_ge4_286_AAAAG';BASE='source-evidence/zhaowang-lun-identity-retirement';DID='d-jinshu075-zhaowang-lun-crossidentity'
class ZhaoWangLunRetirement(unittest.TestCase):
 def test_two_precise075_mentions_and_source_text_preserved(self):
  c=json.loads((R/'corpus/jinshu/075.json').read_text());reading=json.loads((R/BASE/'identity-reading.json').read_text())['source_reading'][0]
  self.assertEqual([(p['id'],p['text'])for p in c['paragraphs']],[(p['id'],p['text'])for p in reading['paragraphs']]);p=c['paragraphs'][0];ms=[m for m in p['mentions']if m['id']in[p['id']+':m0179',p['id']+':m0189']];self.assertEqual([m['surface']for m in ms],['趙王倫','倫']);self.assertEqual({m['person_id']for m in ms},{KEEP})
 def test_new024_two_precise_mentions_also_joined(self):
  c=json.loads((R/'corpus/sanguozhi/024-cuilin.json').read_text());p=c['paragraphs'][9];ms=[m for m in p['mentions']if m['id']in[p['id']+':m0017',p['id']+':m0026']];self.assertEqual([m['surface']for m in ms],['趙王倫','倫']);self.assertEqual({m['person_id']for m in ms},{KEEP})
 def test_registry_union_and_no_alias(self):
  people={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']};self.assertNotIn(OLD,people);self.assertIn(KEEP,people);self.assertFalse(any(OLD in p.get('id_aliases',[])for p in people.values()));self.assertIn('c-jinshu-075-xunsong-families:xunsong-intro:p001:m0179',{e['mention_id']for e in people[KEEP]['evidence']})
 def test_permanent_allocator_skips_retired_root_and_descendants(self):
  retired=retired_person_ids(R);self.assertIn(OLD,retired);self.assertTrue(allocation_conflicts(OLD+'_A',retired))
  with self.assertRaises(ValueError):assert_not_retired(OLD,R)
  with self.assertRaises(ValueError):allocate_child_id(OLD,[],root=R)
  used={p['id']for p in json.loads((R/'registry/persons.json').read_text())['persons']};token=next('zzzzzzz'+a+b for a,b in itertools.product(string.ascii_lowercase,repeat=2)if '_'.join(('zzzzzzz'+a+b)[i:i+3]for i in(0,3,6))not in used|set(retired));want='_'.join(token[i:i+3]for i in(0,3,6))
  with patch('scripts.person_ids.secrets.choice',side_effect=list(OLD.replace('_','')+token)):self.assertEqual(allocate_person_id(used,root=R),want)
 def test_exact_historical_captures_and_no_old_active_projection(self):
  q=json.loads((R/BASE/'historical-captures.json').read_text());import hashlib
  self.assertEqual(len(q['captures']),11);self.assertEqual(len(q['updated_active_projection_files']),10)
  for x in q['captures']:self.assertEqual(hashlib.sha256((R/x['path']).read_bytes()).hexdigest(),x['sha256'])
  for x in q['updated_active_projection_files']:self.assertNotIn(OLD,(R/x['path']).read_text())
 def temp_receipt(self,r,change):
  receipt=json.loads((R/BASE/'annotation-chain.json').read_text());change(receipt);p=r/BASE/'annotation-chain.json';p.parent.mkdir(parents=True);p.write_text(json.dumps(receipt));d=json.loads((R/'corpus/jinshu/075-identities.json').read_text());d['decisions']=[x for x in d['decisions']if x['id']==DID];p=r/'corpus/jinshu/075-identities.json';p.parent.mkdir(parents=True);p.write_text(json.dumps(d));p=r/'registry/persons.json';p.parent.mkdir(parents=True);p.write_text(json.dumps({'persons':[{'id':KEEP}]}))
 def test_mixed_receipt_or_missing_owner_rejected(self):
  for change in [lambda d:d.update(family_id='family-false-owner'),lambda d:d.update(identity_decision_id='d-missing')]:
   with self.subTest(change=change),tempfile.TemporaryDirectory()as td:
    r=Path(td);self.temp_receipt(r,change)
    with self.assertRaises(ValueError):retired_person_ids(r)
 def test_old_profile_paths_absent(self):
  for directory in('exports/persons','data/corpus/profiles'):self.assertFalse((R/directory/(OLD+'.json')).exists())
if __name__=='__main__':unittest.main()
