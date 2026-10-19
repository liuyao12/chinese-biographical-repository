# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((ROOT/n).read_text())
class SongWangPhase5(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=read('corpus/songshu/042.json');cls.b=read('corpus/songshu/063-wanghua-tanshou.json');cls.r=read('corpus/songshu/042-assertions.json')['assertions']+read('corpus/songshu/063-wanghua-tanshou-assertions.json')['assertions'];cls.people={p['label']:p for p in read('registry/persons.json')['persons']};cls.ps={p['id']:p for c in [cls.a,cls.b]for p in c['paragraphs']}
 def test_complete_units_keep_received_text_and_partial_volume_scope(self):
  self.assertEqual([len(c['paragraphs'])for c in [self.a,self.b]],[27,15]);self.assertEqual(sum(len(p['text'])for p in self.ps.values()),9734)
  self.assertEqual(self.a['paragraphs'][0]['id'],'c-songshu-042-wanghong:p001');self.assertEqual(len(self.a['paragraphs'][0]['mentions']),5)
  self.assertEqual(self.a['paragraphs'][-1]['source_position']['first_line'],97);self.assertEqual(self.b['paragraphs'][-1]['source_position']['first_line'],39)
  for c in [self.a,self.b]:self.assertEqual(c['source']['text_scope'],'partial_chapter');self.assertFalse(c['source']['image_verified'])
 def test_variant_is_source_scoped_without_changing_text_or_creating_wangyi(self):
  p=next(p for p in self.a['paragraphs']if p['id'].endswith('line095'));self.assertIn('虞弟抑，光祿大夫。抑弟孺',p['text']);self.assertNotIn('王抑',self.people)
  self.assertEqual({m['person_id']for m in p['mentions']if m['surface']=='抑'},{self.people['王柳']['id']})
  self.assertFalse(any(m['surface']=='抑'for p in self.a['paragraphs']if p['id'].endswith('line063')for m in p['mentions']))
 def test_sengqian_existing_id_and_direct_father_are_preserved(self):
  pid=self.people['王僧虔']['id'];self.assertEqual(pid,'7r6_k52_qji_ABAAAAEB');a=next(a for a in self.r if a['subject_person_id']==pid and a['predicate']=='father');self.assertEqual(a['object_person_id'],self.people['王曇首']['id']);self.assertEqual(a['qualifiers']['birth_order']['ordinal'],None)
  self.assertFalse(any(p['id']=='n06_l4p_v9e'for p in self.people.values()))
 def test_zhong_is_a_younger_brother_without_an_invented_father(self):
  pid=self.people['王終']['id'];a=next(a for a in self.r if a['subject_person_id']==pid);self.assertEqual(a['predicate'],'brother');self.assertEqual(a['object_person_id'],self.people['王長']['id']);self.assertFalse(any(a['subject_person_id']==pid and a['predicate']=='father'for a in self.r));self.assertNotIn('family_path',self.people['王終'])
 def test_source_mothers_do_not_create_spouses_or_shared_birth_mothers(self):
  maternal=[a for a in self.r if a['predicate']=='mother'];self.assertEqual(len(maternal),3);self.assertTrue(all(a['qualifiers']['biological_parentage']=='not_independently_established'for a in maternal));self.assertFalse(any(a['predicate']=='spouse'for a in self.r));self.assertFalse(any(a['subject_person_id']==self.people['王終']['id']and a['predicate']=='mother'for a in self.r))
 def test_hua_family_and_anonymous_daughter_are_not_taiyuan_wang(self):
  hua=self.people['王華']['id'];a=next(a for a in self.r if a['subject_person_id']==hua and a['predicate']=='father');self.assertEqual(a['object_person_id'],self.people['王廞']['id']);self.assertTrue(hua.startswith('7r6_k52_qji_'));self.assertNotEqual(hua[:11],'a8f_ec8_e74')
  a=next(a for a in self.r if a['subject_person_id']==self.people['王廞女']['id']);self.assertEqual(a['object_person_id'],self.people['王廞']['id'])
 def test_sons_and_cousins_keep_relation_types_without_new_common_ancestors(self):
  cousins=[a for a in self.r if a['predicate']=='agnatic_cousin'];self.assertEqual(len(cousins),5)
  for a in cousins:self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id']);self.assertIsNone(a['qualifiers']['kinship_structure']['distance'])
  fathers={a['subject_person_id']:a['object_person_id']for a in self.r if a['predicate']=='father'};self.assertEqual(fathers[self.people['王僧綽']['id']],self.people['王曇首']['id']);self.assertEqual(fathers[self.people['王嗣']['id']],self.people['王華']['id'])
 def test_all_exact_anchors_have_actual_source_characters(self):
  for c in [self.a,self.b]:
   for p in c['paragraphs']:
    for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
  for a in self.r:
   if 'source_term_anchor'in a:x=a['source_term_anchor'];self.assertEqual(self.ps[x['paragraph_id']]['text'][x['start']:x['end']],x['surface'])
if __name__=='__main__':unittest.main()
