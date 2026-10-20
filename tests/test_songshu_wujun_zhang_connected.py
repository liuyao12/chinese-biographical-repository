# coding: utf-8
from pathlib import Path
import json,copy,unittest
from scripts.ancestry_chain import consecutive_ancestor_parent_valid,explicit_four_ancestor_sequence_valid
R=Path(__file__).resolve().parents[1]
ROOT='d50_8f5_wul'
RETIRED=('igs_pxh_opu','k78_5u7_lsl','5qw_4hm_mer','kqk_vbm_s4y','c8k_paq_5hq','8ea_e24_a17','oya_kv4_mgn','33h_ci5_0p1','a16_631_e88','clx_5bj_yy4','hda_u2r_vnc','hct_xgk_qyk','58a_u1n_fuh','91u_epx_zxw','cmq_zhw_kme','3lb_yew_ir1')
def read(p):return json.loads((R/p).read_bytes())
F=next(f for f in read('registry/family-assemblies.json')['assemblies']if f['id']=='family-song053-wujun-zhang-jia');ROWS={m['person_id']:m for m in F['members']}
ASSERT={a['id']:a for name in ('046-zhangshao','059-zhangchang','053-zhangmaodu')for a in read('corpus/songshu/'+name+'-assertions.json')['assertions']}
C=read('corpus/songshu/053-zhangmaodu.json');CH={C['id']:C};M=ROWS[ROOT+'_A']
class ConnectedZhang(unittest.TestCase):
 def test_retired_ids_not_active_or_aliases(self):
  pp=read('registry/persons.json')['persons'];self.assertFalse(set(RETIRED)&{p['id']for p in pp});self.assertFalse(set(RETIRED)&{a for p in pp for a in p.get('id_aliases',[])})
 def test_seventeen_unique_canonical_members(self):
  self.assertEqual(len(ROWS),17);self.assertEqual(F['root_person_id'],ROOT)
  for p,m in ROWS.items():self.assertEqual(m['source_person_ids'],[p]);self.assertEqual(m['representative_source_person_id'],p)
 def test_four_generation_explicit_sequence_accepted(self):self.assertTrue(consecutive_ancestor_parent_valid(M,ROWS,ASSERT,CH))
 def test_wrong_distance_rejected(self):
  aa=copy.deepcopy(ASSERT);aa['a-song053-zhangmaodu-004']['qualifiers']['generation_distance']=5;self.assertFalse(consecutive_ancestor_parent_valid(M,ROWS,aa,CH))
 def test_different_subject_rejected(self):
  aa=copy.deepcopy(ASSERT);aa['a-song053-zhangmaodu-004']['subject_person_id']=ROOT+'_AAAC';self.assertFalse(consecutive_ancestor_parent_valid(M,ROWS,aa,CH))
 def test_missing_father_claim_rejected(self):
  aa=copy.deepcopy(ASSERT);del aa['a-song053-zhangmaodu-001'];self.assertFalse(consecutive_ancestor_parent_valid(M,ROWS,aa,CH))
 def test_maternal_grandfather_rejected(self):
  aa=copy.deepcopy(ASSERT);aa['a-song053-zhangmaodu-002']['qualifiers']['lineage']='maternal';self.assertFalse(consecutive_ancestor_parent_valid(M,ROWS,aa,CH))
 def test_unbound_source_role_rejected(self):
  aa=copy.deepcopy(ASSERT);aa['a-song053-zhangmaodu-004']['qualifiers']['source_term']='髙祖';self.assertFalse(consecutive_ancestor_parent_valid(M,ROWS,aa,CH))
 def test_missing_ancestor_name_anchor_rejected(self):
  ch=copy.deepcopy(CH);p=ch[C['id']]['paragraphs'][0];p['mentions']=[m for m in p['mentions']if m.get('person_id')!=ROOT];self.assertFalse(consecutive_ancestor_parent_valid(M,ROWS,ASSERT,ch))
 def test_direct_conflicting_father_rejected(self):
  aa=copy.deepcopy(ASSERT);aa['counterexample']={'id':'counterexample','predicate':'father','subject_person_id':ROOT+'_A','object_person_id':ROOT+'_AAAC'};self.assertFalse(consecutive_ancestor_parent_valid(M,ROWS,aa,CH))
 def test_negated_or_variant_sequence_rejected_after_reanchoring(self):
  for marker in ('非','未','不','或云'):
   aa=copy.deepcopy(ASSERT);ch=copy.deepcopy(CH);para=ch[C['id']]['paragraphs'][0];old=para['text'];at=old.index('曾祖澄');text=old[:at]+marker+old[at:];para['text']=text
   for mention in para['mentions']:
    if mention['start']>=at:mention['start']+=len(marker);mention['end']+=len(marker)
   for a in aa.values():
    for evidence in a.get('evidence',[]):
     if evidence.get('chapter_id')==C['id'] and evidence.get('paragraph_id')==para['id']:evidence['quote']=text
   member=copy.deepcopy(M)
   for ref in member['parent_connection']['references']:ref['quote']=text
   self.assertFalse(explicit_four_ancestor_sequence_valid(aa['a-song053-zhangmaodu-003'],aa['a-song053-zhangmaodu-004'],aa,ch),marker)
   self.assertFalse(consecutive_ancestor_parent_valid(member,ROWS,aa,ch),marker)
 def test_five_shared_fathers_have_two_original_claims(self):
  mm=[m for m in ROWS.values()if m.get('parent_connection',{}).get('type')=='shared_father_through_sibling'];self.assertEqual(len(mm),5)
  for m in mm:
   c=m['parent_connection'];self.assertFalse(c['human_reviewed']);self.assertEqual(c['status'],'contextual_provisional');self.assertIn(c['sibling_assertion_id'],ASSERT);self.assertIn(c['sibling_father_assertion_id'],ASSERT)
 def test_editorial_parents_do_not_rewrite_direct_claims(self):
  self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==ROOT+'_AAAAB'for a in ASSERT.values()));self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==ROOT+'_A'for a in ASSERT.values()))
 def test_ambiguous_046_yan_jing_not_shao_children(self):
  aa=read('corpus/songshu/046-zhangshao-assertions.json')['assertions'];self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']in(ROOT+'_AAAAA',ROOT+'_AAAAB')for a in aa))
 def test_distant_and_ambiguous_jin_excluded(self):
  self.assertNotIn('ea5_zvr_hlp',ROWS);self.assertNotIn('k87_bb8_slb',ROWS);self.assertNotIn('2hb_pso_2r9',ROWS)
if __name__=='__main__':unittest.main(verbosity=2)
