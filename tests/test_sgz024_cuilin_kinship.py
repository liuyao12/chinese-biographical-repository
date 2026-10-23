from pathlib import Path
import json,copy,unittest
from scripts.fixed_kanripo_fact_slots import records,valid,errors,grammar
from scripts.fixed_kanripo_projection import errors as projection_errors
from scripts.person_bundle import load_catalog
ROOT=Path(__file__).resolve().parents[1];KEY='sgz024-cuilin-four-kinship';CID='c-sanguozhi-024-cuilin'
class CuilinKinship(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/sanguozhi/024-cuilin.json').read_bytes());cls.facts=records(cls.ch,ROOT);cls.by={a['id'].removeprefix('a-sgz024-cuilin-'):a for a in cls.facts};cls.roles=[[m for m in p['mentions']if m['kind']=='person']for p in cls.ch['paragraphs']]
 def test_full_ten_units_and_projection_pin(self):self.assertEqual(len(self.ch['paragraphs']),10);self.assertEqual(projection_errors(self.ch,ROOT),[]);self.assertEqual(len(self.facts),4);self.assertTrue(all(valid(a,self.ch,ROOT)for a in self.facts))
 def test_father_from_son_word_not_inheritance_alone(self):
  a=self.by['shu-father-lin'];self.assertEqual(a['predicate'],'father');self.assertEqual(a['subject_person_id'],self.roles[8][3]['person_id']);self.assertEqual(a['object_person_id'],self.roles[8][1]['person_id']);self.assertEqual(a['qualifiers']['source_term'],'子述嗣')
 def test_younger_brother_direction_without_parent_or_absolute_rank(self):
  a=self.by['sui-younger-brother-shu'];q=a['qualifiers'];self.assertEqual(a['subject_person_id'],self.roles[9][1]['person_id']);self.assertEqual(a['object_person_id'],self.roles[9][0]['person_id']);self.assertEqual(q['relative_age'],'younger');self.assertNotIn('shared_father',q);self.assertNotIn('shared_mother',q);self.assertIsNone(q['relative_birth_order']['older_ordinal']);self.assertIsNone(q['relative_birth_order']['younger_ordinal'])
 def test_grandfather_two_generations_parent_unknown(self):
  a=self.by['wei-grandfather-lin'];q=a['qualifiers'];self.assertEqual(a['predicate'],'grandfather');self.assertEqual(a['subject_person_id'],self.roles[9][7]['person_id']);self.assertEqual(a['object_person_id'],self.roles[9][6]['person_id']);self.assertEqual(q['lineage'],'paternal');self.assertEqual(q['generation_distance'],2);self.assertEqual(q['generation_difference'],-2);self.assertIsNone(q['parent_person_id']);self.assertEqual(q['intermediate_person_ids'],[None])
 def test_collateral_elder_is_object_not_common_ancestor(self):
  a=self.by['lin-younger-agnatic-cousin-yan'];q=a['qualifiers'];s=q['kinship_structure'];self.assertEqual(a['subject_person_id'],self.roles[0][0]['person_id']);self.assertEqual(a['object_person_id'],self.roles[0][2]['person_id']);self.assertEqual(s['generation_difference'],0);self.assertTrue(s['collateral']);self.assertEqual(s['subject_relative_age'],'younger');self.assertIsNone(s['distance']);self.assertIsNone(s['common_ancestor_person_id']);self.assertEqual(q['relative_birth_order']['older_person_id'],a['object_person_id']);self.assertEqual(q['relative_birth_order']['scope'],'agnatic_cousins')
 def test_received_vs_pei_layers_preserved(self):
  self.assertEqual(self.ch['paragraphs'][8]['text_layer'],'received_chapter');self.assertEqual(self.ch['paragraphs'][9]['text_layer'],'witness_appended_pei_songzhi_note');self.assertTrue(self.ch['paragraphs'][9]['text'].startswith('晉諸公贊曰'))
 def test_new_xiang_anchor_not_regressed(self):
  m=next(m for m in self.ch['paragraphs'][0]['mentions']if m['id'].endswith(':m0194'));self.assertEqual((m['surface'],m['start'],m['end']),('相',193,194))
 def test_direction_reversed_rejected(self):
  for source in self.facts:
   a=copy.deepcopy(source);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(valid(a,self.ch,ROOT))
 def test_coherently_other_person_and_evidence_rejected(self):
  a=copy.deepcopy(self.by['wei-grandfather-lin']);m=self.roles[9][9];a['subject_person_id']=m['person_id'];a['evidence'][0]['subject_person_mention_id']=m['id'];self.assertFalse(valid(a,self.ch,ROOT))
 def test_coherent_brother_other_person_both_ends_rejected(self):
  a=copy.deepcopy(self.by['sui-younger-brother-shu']);x,y=self.roles[9][2],self.roles[9][9];a['subject_person_id']=x['person_id'];a['object_person_id']=y['person_id'];a['evidence'][0].update(subject_person_mention_id=x['id'],object_person_mention_id=y['id']);a['qualifiers']['relative_birth_order'].update(older_person_id=y['person_id'],younger_person_id=x['person_id']);self.assertFalse(valid(a,self.ch,ROOT))
 def test_grandchild_parent_not_shu_sui_or_invented(self):
  for parent in[self.roles[9][0]['person_id'],self.roles[9][1]['person_id'],'not-a-person']:
   a=copy.deepcopy(self.by['wei-grandfather-lin']);a['qualifiers'].update(parent_person_id=parent,intermediate_person_ids=[parent]);self.assertFalse(valid(a,self.ch,ROOT))
 def test_cousin_degree_or_shared_ancestor_not_inferred(self):
  for field,val in[('distance',2),('common_ancestor_person_id',self.roles[0][0]['person_id']),('generation_difference',-1)]:
   a=copy.deepcopy(self.by['lin-younger-agnatic-cousin-yan']);a['qualifiers']['kinship_structure'][field]=val;self.assertFalse(valid(a,self.ch,ROOT))
 def test_brother_father_or_absolute_rank_not_added(self):
  a=copy.deepcopy(self.by['sui-younger-brother-shu']);a['qualifiers']['shared_father']=True;self.assertFalse(valid(a,self.ch,ROOT));a=copy.deepcopy(self.by['sui-younger-brother-shu']);a['qualifiers']['relative_birth_order']['younger_ordinal']=2;self.assertFalse(valid(a,self.ch,ROOT))
 def test_wrong_witness_layers_and_source_text_rejected(self):
  for change in('revision','layer','text'):
   ch=copy.deepcopy(self.ch)
   if change=='revision':ch['source']['revision_id']='wrong'
   elif change=='layer':ch['paragraphs'][9]['text_layer']='received_chapter'
   else:ch['paragraphs'][9]['text']=ch['paragraphs'][9]['text'].replace('述弟隨','隨弟述')
   self.assertFalse(valid(self.facts[0],ch,ROOT))
 def test_projection_ref_and_wrong_slot_rejected(self):
  ch=copy.deepcopy(self.ch);ch['annotation'].pop('fixed_kanripo_projection_ref');self.assertFalse(valid(self.facts[0],ch,ROOT));a=copy.deepcopy(self.facts[0]);a['fixed_source_fact_binding']['slot']='wrong';self.assertFalse(valid(a,self.ch,ROOT))
 def test_missing_duplicate_and_extra_facts_rejected(self):
  for facts in(self.facts[:-1],self.facts+[self.facts[0]],self.facts+[dict(self.facts[0],id='invented')]):
   self.assertTrue(errors(ROOT,[self.ch,dict(record_type='person_assertion_set',chapter_id=CID,assertions=facts)]))
 def test_no_new_source_father_for_sui_or_wei(self):
  self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']in(self.roles[9][1]['person_id'],self.roles[9][7]['person_id'])for a in self.facts))
if __name__=='__main__':unittest.main()
