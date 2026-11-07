import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_zhou041_erlu as erlu
from scripts.fixed_zhou041_wangbao import proof
from scripts.source_person_reference_groups import validated_sets,for_people
ROOT=Path(__file__).resolve().parents[1]
class ErLu(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_bytes())['persons']};cls.doc=json.loads((ROOT/erlu.GROUP).read_bytes());cls.ch,cls.contract,cls.roles=proof(ROOT,people=cls.people)
 def overlay(self,rows):
  original=Path.read_bytes
  return patch.object(Path,'read_bytes',lambda p:json.dumps(rows[str(p.relative_to(ROOT))],ensure_ascii=False).encode()if p.is_relative_to(ROOT)and str(p.relative_to(ROOT))in rows else original(p))
 def test_complete_group_runtime_each_member(self):
  self.assertTrue(erlu.group_set_valid(self.doc,self.people,ROOT))
  for m in self.doc['groups'][0]['members']:
   groups,readings,related=for_people([self.doc],self.people,ROOT,{m['person_id']});self.assertEqual(groups,self.doc['groups']);self.assertEqual(readings,[]);self.assertEqual(len(related),2)
 def test_no_direct_mention_or_alias(self):
  marker=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['id']==erlu.MID);self.assertIsNone(marker['person_id']);self.assertEqual(marker['kind'],'unresolved');self.assertNotIn('candidate_person_ids',marker)
  self.assertNotIn('d-zhou041-erlu',[x['id']for x in self.ch['annotation']['unresolved_identity_cases']])
 def test_wrong_member_or_count_rejected(self):
  for mutate in [lambda d:d['groups'][0]['members'].pop(),lambda d:d['groups'][0].update(reported_count=True),lambda d:d['groups'][0].update(reported_count=2.0),lambda d:d['groups'][0].update(completeness='known_subset')]:
   d=copy.deepcopy(self.doc);mutate(d)
   with self.assertRaises((ValueError,AssertionError)):erlu.group_set_valid(d,self.people,ROOT)
 def test_missing_sidecar_caller_rejected(self):
  with self.assertRaises(ValueError):validated_sets([],self.people,ROOT)
 def test_wrong_owner_rejected(self):
  d=copy.deepcopy(self.doc);d['owner']='unknown'
  with self.assertRaises(ValueError):validated_sets([d],self.people,ROOT)
 def test_anchor_becoming_person_rejected(self):
  c=copy.deepcopy(self.ch);m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']==erlu.MID);m.update(kind='person',person_id=self.doc['groups'][0]['members'][0]['person_id'])
  with self.overlay({erlu.CH:c}),self.assertRaises((ValueError,AssertionError)):proof(ROOT,people=self.people)
 def test_member_reverse_and_alias_corruption_rejected(self):
  member=self.doc['groups'][0]['members'][0];pid=member['person_id']
  for typ in ['reverse','alias']:
   people=copy.deepcopy(self.people)
   if typ=='reverse':people[pid]['evidence']=[e for e in people[pid]['evidence']if e.get('mention_id')!=member['evidence']['mention_id']]
   else:people[pid]['aliases'].append({'surface':'二陸','mention_ids':[erlu.MID]})
   with self.assertRaises((ValueError,AssertionError)):erlu.group_set_valid(self.doc,people,ROOT)
 def test_ordinary_bundle_both_members(self):
  from scripts.person_bundle import load_catalog,bundle
  people,records=load_catalog(ROOT)
  for member in self.doc['groups'][0]['members']:
   result=bundle(member['person_id'],ROOT,catalog=(people,records));self.assertIn(self.doc['groups'][0],result['source_person_groups']);self.assertFalse(any(m.get('id')==erlu.MID for m in result['mentions']))
 def test_current_endpoint_rekey_not_permanent_PID_whitelist(self):
  key='candidate_erlu_luji';seed=self.contract['candidate_source_seeds'][key];old=self.roles['$'+key];new='zzz_zzz_zzz';people=copy.deepcopy(self.people);people[new]=people.pop(old);people[new]['id']=new
  ext=json.loads((ROOT/seed['path']).read_bytes());m=next(m for p in ext['paragraphs']for m in p['mentions']if m['id']==seed['marker']['id']);m['person_id']=new;doc=copy.deepcopy(self.doc);doc['groups'][0]['members'][0]['person_id']=new
  extra_path='corpus/jinshu/040-wyd1739-jiachong.json';extra=json.loads((ROOT/extra_path).read_bytes());em=next(m for p in extra['paragraphs']for m in p['mentions']if m['id']==doc['groups'][0]['members'][0]['evidence']['mention_id']);em['person_id']=new
  with self.overlay({seed['path']:ext,extra_path:extra,erlu.GROUP:doc}):self.assertTrue(erlu.group_set_valid(doc,people,ROOT))
 def test_member_native_reverse_counterpart_tamper_rejected(self):
  path='corpus/jinshu/040-wyd1739-jiachong.json';ch=json.loads((ROOT/path).read_bytes());mid=self.doc['groups'][0]['members'][0]['evidence']['mention_id'];m=next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==mid);m['person_id']=self.doc['groups'][0]['members'][1]['person_id']
  with self.overlay({path:ch}),self.assertRaises((ValueError,AssertionError)):erlu.group_set_valid(self.doc,self.people,ROOT)
if __name__=='__main__':unittest.main()
