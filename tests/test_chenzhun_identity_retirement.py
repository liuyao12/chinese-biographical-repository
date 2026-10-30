"""陳氏譜與宋060兩奏議共用同一太尉廣陵公身份。"""
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1];CANON='9w8_tqh_ysn_B*AA'
def J(p):return json.loads((ROOT/p).read_text())
class ChenzhunIdentityTests(unittest.TestCase):
 def test_song_mentions_use_existing_canonical(self):
  c=J('corpus/songshu/060.json');wanted={'c-songshu-060-xunbozi:p003:m0122','c-songshu-060-xunbozi:p004:m0271'};ms=[m for p in c['paragraphs']for m in p['mentions']if m['id']in wanted];self.assertEqual(len(ms),2);self.assertTrue(all(m['person_id']==CANON for m in ms));self.assertEqual({m['surface']for m in ms},{'陳准','准'})
 def test_seven_generation_statement_not_new_fathers(self):
  a=next(a for a in J('corpus/songshu/060-assertions.json')['assertions']if a['id']=='a-songshu060-family-012');self.assertEqual(a['object_person_id'],CANON);self.assertEqual(a['predicate'],'ancestor');self.assertEqual(a['qualifiers']['source_term'],'七世祖');self.assertEqual(a['qualifiers']['generation_distance'],7);fa=J('registry/family-assemblies.json');self.assertFalse(any(m['person_id']=='lir_36y_g5d'and m.get('parent_person_id')==CANON for f in fa['assemblies']for m in f['members']))
 def test_chenpu_and_jin089_retained(self):
  c=J('corpus/jinshu/089-jishao.json');m=next(m for p in c['paragraphs']for m in p['mentions']if m['surface']=='陳准');self.assertEqual(m['person_id'],CANON);reg=J('registry/persons.json');p=next(p for p in reg['persons']if p['id']==CANON);sources={e['source_id']for e in p['evidence']};self.assertTrue({'s-songshu-060-xunbozi','s-sanguozhi-022-chenqun-chentai','s-jinshu-089-jishao'}<=sources)
 def test_pei_remains_unresolved_candidate(self):
  c=J('corpus/jinshu/089-jishao.json');m=next(m for p in c['paragraphs']for m in p['mentions']if m['surface']=='裴頠');self.assertEqual(m['kind'],'unresolved');self.assertEqual(m['candidate_person_ids'],['svm_6fh_34r'])
if __name__=='__main__':unittest.main()
