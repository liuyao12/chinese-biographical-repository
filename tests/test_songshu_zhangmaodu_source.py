# coding: utf-8
from pathlib import Path
import json,unittest,copy
from scripts.validate_corpus import normalized_date_errors,source_age_number
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'corpus/songshu/053-zhangmaodu.json').read_bytes());P=C['paragraphs'][0];T=P['text'];AA=json.loads((R/'corpus/songshu/053-zhangmaodu-assertions.json').read_bytes())['assertions'];L=json.loads((R/'corpus/songshu/053-zhangmaodu-life-events.json').read_bytes())['events'][0];DATE=L['normalized_date']
def at(term,off=0):i=T.index(term)+off;return next((m for m in P['mentions']if m['start']<=i<m['end']),None)
class ZhangMaoduSource(unittest.TestCase):
 def test_complete_selected_unit_and_exact_raw(self):
  self.assertEqual(len(T),823);self.assertTrue(T.endswith('皆有盛名並早卒'));self.assertNotIn('鏡弟永',T)
  f=json.loads((R/'source-evidence/song053-zhangmaodu-native/reading-input.json').read_bytes());raw=(R/f['raw_path']).read_text().splitlines();self.assertEqual(T,f['text'])
  self.assertEqual(''.join(raw[x['line']-1][x['column']]for x in f['raw_character_positions']),T)
 def test_all_person_markings_remain_provisional(self):self.assertEqual(len(P['mentions']),61);self.assertTrue(all(m['status']=='contextual_provisional'for m in P['mentions']))
 def test_ancestor_high_not_emperor(self):self.assertIsNone(at('髙祖嘉'));self.assertEqual(at('髙祖嘉',2)['person_id'],'d50_8f5_wul')
 def test_later_emperor_resumption(self):self.assertEqual(at('髙祖西伐劉毅')['person_id'],'3qs_nqa_ioa_AAA')
 def test_era_name_not_person_jia(self):self.assertIsNone(at('元嘉元年'))
 def test_langyawang_has_fixed_primary_bridge(self):
  self.assertEqual(at('琅邪王')['person_id'],'ije_ngm_cmj');ref=json.loads((R/'source-evidence/song053-zhangmaodu-native/langyawang-identity-reference.json').read_bytes());self.assertIn('恭帝諱徳文',ref['complete_unit_read']);self.assertFalse(ref['wikipedia_used_as_authority'])
 def test_explicit_yan_father(self):self.assertTrue(any(a['predicate']=='father'and a['subject_person_id']=='d50_8f5_wul_AAAAA'and a['object_person_id']=='d50_8f5_wul_AAAA'for a in AA))
 def test_no_jing_father_inference(self):self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']=='d50_8f5_wul_AAAAB'for a in AA))
 def test_no_yan_shao_father(self):self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']=='d50_8f5_wul_AAAAA'and a['object_person_id']=='d50_8f5_wul_AAAC'for a in AA))
 def test_jing_younger_without_ordinals(self):
  a=next(a for a in AA if a['subject_person_id']=='d50_8f5_wul_AAAAB');o=a['qualifiers']['relative_birth_order'];self.assertEqual(o['older_person_id'],'d50_8f5_wul_AAAAA');self.assertIsNone(o['older_ordinal']);self.assertIsNone(o['younger_ordinal'])
 def test_fourth_ancestor_is_not_father(self):
  a=next(a for a in AA if a['object_person_id']=='d50_8f5_wul');self.assertEqual(a['predicate'],'ancestor');self.assertEqual(a['qualifiers']['generation_distance'],4)
 def test_great_grandfather_not_father(self):self.assertEqual(next(a for a in AA if a['object_person_id']=='d50_8f5_wul_A')['predicate'],'great_grandfather')
 def test_grandfather_not_father(self):self.assertEqual(next(a for a in AA if a['object_person_id']=='d50_8f5_wul_AA')['predicate'],'grandfather')
 def test_lu_topic_stays_separate(self):
  a=next(a for a in AA if a['subject_person_id']=='jif_4nl_z1h');self.assertEqual(a['object_person_id'],'9jp_jmf_6jv');self.assertEqual(a['predicate'],'great_grandfather');self.assertEqual(at('弟子眞',1)['person_id'],'n4m_bun_vsi')
 def test_clan_analogy_not_fake_person(self):self.assertIsNone(at('金張二族'))
 def test_stepmother_not_birth_or_spouse(self):
  a=next(a for a in AA if a['predicate']=='stepmother');self.assertEqual(a['object_person_id'],'2hb_pso_2r9');self.assertIsNone(a['qualifiers']['father_person_id']);self.assertFalse(any(a['predicate']in('mother','spouse')for a in AA))
 def test_origin_original_place(self):
  a=json.loads((R/'corpus/songshu/053-zhangmaodu-addresses.json').read_bytes())['assertions'][0];self.assertEqual(a['place']['source_name'],'呉郡呉');self.assertIsNone(a['place']['modern_identification'])
 def test_next_year_442(self):self.assertEqual(DATE['year'],442);self.assertEqual(DATE['source_expression'],'明年');self.assertFalse(normalized_date_errors(DATE,{C['id']:C},R))
 def test_old_443_rejected(self):
  d=copy.deepcopy(DATE);d['year']=d['era_year']=443;self.assertTrue(normalized_date_errors(d,{C['id']:C},R))
 def test_wrong_offset_rejected(self):
  d=copy.deepcopy(DATE);d['regnal_year_mapping']['year_offset']=2;self.assertTrue(normalized_date_errors(d,{C['id']:C},R))
 def test_wrong_antecedent_rejected(self):
  d=copy.deepcopy(DATE);d['relative_year_reference']['antecedent_expression']='十七年';self.assertTrue(normalized_date_errors(d,{C['id']:C},R))
 def test_67_is_reported_not_birth(self):
  a=C['annotation']['age_assertions'][0];self.assertEqual(a['value'],67);self.assertEqual(source_age_number(a['source_number']),67);self.assertEqual(a['counting'],'unspecified_source_age');self.assertIsNone(a['birth_year'])
 def test_no_distant_genealogy_in_kinship(self):self.assertFalse(any(a['object_person_id']=='ea5_zvr_hlp'for a in AA))
 def test_di_death_not_imposed(self):self.assertNotEqual(L['person_id'],'v3n_puj_x6k');self.assertEqual(L['person_id'],'d50_8f5_wul_AAAA')
if __name__=='__main__':unittest.main(verbosity=2)
