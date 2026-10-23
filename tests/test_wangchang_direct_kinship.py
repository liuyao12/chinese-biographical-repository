import json,unittest
from pathlib import Path
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1]
class DirectKinship(unittest.TestCase):
 def test_three_exact_source_assertions_and_no_invented_father(self):
  c=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());a=json.loads((R/'corpus/sanguozhi/027-wangchang-assertions.json').read_text())['assertions'];ms={m['id']:m for p in c['paragraphs']for m in p['mentions']};ps={p['id']:p for p in c['paragraphs']};rows=[x for x in a if x['id']in ['a-sanguozhi027-wangchang-011','a-sanguozhi027-wangchang-012','a-sanguozhi027-wangchang-013']];self.assertEqual(len(rows),3)
  for x in rows:
   e=x['evidence'][0];self.assertEqual(ms[e['subject_person_mention_id']]['person_id'],x['subject_person_id']);self.assertEqual(ms[e['object_person_mention_id']]['person_id'],x['object_person_id']);self.assertEqual(e['quote'],ps[e['paragraph_id']]['text']);self.assertIn(x['qualifiers']['source_term'],e['quote'])
  mo=rows[-1];self.assertEqual(mo['predicate'],'paternal_uncle');self.assertFalse(any(x['subject_person_id']==mo['subject_person_id']and x['predicate']=='father'for x in a));self.assertEqual([x['predicate']for x in rows],['father','father','paternal_uncle'])
 def test_full_bundles_link_both_ends_without_identity_merge(self):
  cat=load_catalog(R);a=json.loads((R/'corpus/sanguozhi/027-wangchang-assertions.json').read_text())['assertions'][-3:]
  for x in a:
   for pid in [x['subject_person_id'],x['object_person_id']]:self.assertTrue(any(r['id']==x['id']for r in bundle(pid,root=R,catalog=cat)['relations']))
  c=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());cases=[x for x in c['annotation']['unresolved_identity_cases']if x['id'].startswith('case-sgz027-')];self.assertEqual(len(cases),3);self.assertTrue(all(x['status']=='unresolved'for x in cases))
if __name__=='__main__':unittest.main()
