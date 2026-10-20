"""近世父系可推導、遠祖和兄姊的未明父系不可填補。"""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
class WangYiConnected(unittest.TestCase):
 def test_three_retired_ids_have_no_registry_aliases(self):
  retired={'ymz_r2c_cek','864_b79_ed2','d1p_4ah_jgs'}
  people=read('registry/persons.json')['persons'];self.assertFalse(retired&{p['id']for p in people});self.assertFalse(any(retired&set(p.get('id_aliases',[]))for p in people))
 def test_source_relations_are_preserved_and_only_endpoint_rekeyed(self):
  rows={r['id']:r for r in read('corpus/songshu/046-wangyi-assertions.json')['assertions']}
  self.assertEqual((rows['a-song046-wangyi-001']['subject_person_id'],rows['a-song046-wangyi-001']['object_person_id']),('qsd_v11_ya1_AA','qsd_v11_ya1_A'))
  self.assertEqual((rows['a-song046-wangyi-002']['predicate'],rows['a-song046-wangyi-002']['object_person_id']),('grandfather','qsd_v11_ya1'))
  self.assertFalse(any(r['subject_person_id']=='qsd_v11_ya1_A'and r['predicate']=='father'for r in rows.values()))
 def test_inferred_middle_edge_is_qualified_and_anchored_to_two_source_claims(self):
  a=next(a for a in read('registry/family-assemblies.json')['assemblies']if a['id']=='family-song046-wangyi-hong');m=next(m for m in a['members']if m['person_id']=='qsd_v11_ya1_A');self.assertIsNone(m['source_assertion_id']);self.assertEqual(m['parent_person_id'],'qsd_v11_ya1');c=m['parent_connection'];self.assertEqual(c['type'],'parent_between_consecutive_ancestors');self.assertEqual(c['chain_subject_person_id'],'qsd_v11_ya1_AA');self.assertEqual({r['assertion_id']for r in c['references']},{'a-song046-wangyi-001','a-song046-wangyi-002'});self.assertFalse(c['human_reviewed'])
 def test_no_shared_father_is_added_for_brother_or_sister_or_remote_ancestor(self):
  a=next(a for a in read('registry/family-assemblies.json')['assemblies']if a['id']=='family-song046-wangyi-hong');self.assertEqual({m['person_id']for m in a['members']},{'qsd_v11_ya1','qsd_v11_ya1_A','qsd_v11_ya1_AA','qsd_v11_ya1_AAA'});rows=read('corpus/songshu/046-wangyi-assertions.json')['assertions'];self.assertFalse(any(r['predicate']=='father'and r['subject_person_id']in {'lrq_cdc_wxj','380_854_d21'}for r in rows));self.assertFalse(any(r['object_person_id']=='cqk_f8b_cjq'for r in rows))
 def test_original_mention_ids_and_history_decision_ids_survive(self):
  c=read('corpus/songshu/046-wangyi.json');p=c['paragraphs'][0];self.assertEqual(p['text'],'王懿字仲德太原祁人自言漢司徒允弟幽州刺史懋七世孫也祖宏事石季龍父苖事苻堅皆為二千石');self.assertEqual(next(m['person_id']for m in p['mentions']if m['id']=='c-songshu-046-wangyi:p001:m0000'),'qsd_v11_ya1_AA');self.assertEqual(read('corpus/songshu/046-wangyi-identities.json')['decisions'][0]['id'],'d-song046-wangyi-001')
if __name__=='__main__':unittest.main()
