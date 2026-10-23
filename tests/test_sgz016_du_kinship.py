# coding: utf-8
from pathlib import Path
import copy,json,sys,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import fixed_kanripo_fact_slots as facts

class DuKinship(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/sanguozhi/016-duji-dushu.json').read_bytes());cls.all_rs=facts.records(cls.ch,ROOT);cls.rs=[r for r in cls.all_rs if 'predicate'in r];cls.by={r['fixed_source_fact_binding']['slot']:r for r in cls.rs}
 def test_complete_44_received_and_note_units(self):
  self.assertEqual(len(self.ch['paragraphs']),44);self.assertEqual(len(self.rs),9);self.assertEqual(len(self.all_rs),36);self.assertEqual({p['source_position']['source_layer']for p in self.ch['paragraphs']},{'received_body','pei_annotation'})
 def test_all_source_records_validate(self):
  self.assertTrue(all(facts.valid(r,self.ch,ROOT)for r in self.rs))
 def test_all_endpoint_directions_are_fixed(self):
  for r in self.rs:
   with self.subTest(slot=r['id']):
    a=copy.deepcopy(r);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(facts.valid(a,self.ch,ROOT))
 def test_four_direct_parent_claims(self):
  names=['shu-father-ji','pre-father-shu','xi-father-pre','yi-father-xi'];self.assertTrue(all(self.by[n]['predicate']=='father'for n in names))
  for left,right in zip(names,names[1:]):self.assertEqual(self.by[left]['subject_person_id'],self.by[right]['object_person_id'])
 def test_siblings_are_younger_subjects(self):
  for n in ['li-younger-brother-shu','kuan-younger-brother-shu']:
   a=self.by[n];self.assertEqual(a['predicate'],'brother');self.assertEqual(a['qualifiers']['relative_birth_order']['younger_person_id'],a['subject_person_id']);self.assertEqual(a['qualifiers']['relative_birth_order']['older_person_id'],a['object_person_id']);self.assertNotIn('shared_father',a['qualifiers']);self.assertNotIn('shared_mother',a['qualifiers'])
 def test_kuan_keeps_alternative_reference(self):
  self.assertEqual(self.by['kuan-younger-brother-shu']['qualifiers']['source_interpretation_status'],'contextual_preferred');self.assertTrue(self.by['kuan-younger-brother-shu']['qualifiers']['source_reference_qualification']['alternative_reference_mention_id'])
 def test_source_does_not_add_father_to_brothers(self):
  for n in ['li-younger-brother-shu','kuan-younger-brother-shu']:
   a=copy.deepcopy(self.by[n]);a['predicate']='father';self.assertFalse(facts.valid(a,self.ch,ROOT))
 def test_no_birth_mother_from_stepmother(self):
  a=copy.deepcopy(self.by['ji-stepmother']);self.assertEqual(a['predicate'],'stepmother');a['predicate']='mother';self.assertFalse(facts.valid(a,self.ch,ROOT))
 def test_cousin_not_exact_shared_ancestor(self):
  a=copy.deepcopy(self.by['bin-older-agnatic-cousin-pre']);s=a['qualifiers']['kinship_structure'];self.assertEqual(s['generation_difference'],0);self.assertEqual(s['subject_relative_age'],'older');self.assertIsNone(s['distance']);self.assertIsNone(s['common_ancestor_person_id']);s['distance']=2;self.assertFalse(facts.valid(a,self.ch,ROOT))
 def test_affinity_not_princess_source_father(self):
  a=self.by['pre-father-in-law-xuanwang'];self.assertEqual(a['predicate'],'father_in_law');self.assertTrue(a['qualifiers']['unidentified_spouse_in_this_source']);self.assertFalse(any(m['surface']=='高陸公主'for p in self.ch['paragraphs']for m in p['mentions']))
 def test_source_layer_change_rejected(self):
  c=copy.deepcopy(self.ch);c['paragraphs'][43]['text_layer']='received_chapter';self.assertFalse(facts.valid(self.rs[0],c,ROOT))
 def test_original_text_change_rejected(self):
  c=copy.deepcopy(self.ch);c['paragraphs'][22]['text']+='子';self.assertFalse(facts.valid(self.rs[0],c,ROOT))
 def test_other_named_person_cannot_replace_endpoint(self):
  a=copy.deepcopy(self.by['pre-father-shu']);wrong=next(m for m in self.ch['paragraphs'][40]['mentions']if m['id'].endswith(':m0025'));a['object_person_id']=wrong['person_id'];a['evidence'][0]['object_person_mention_id']=wrong['id'];self.assertFalse(facts.valid(a,self.ch,ROOT))
 def test_unknown_key_rejected(self):
  c=copy.deepcopy(self.ch);c['annotation']['fixed_kanripo_fact_slots_ref']['key']='not-a-trusted-key';self.assertFalse(facts.valid(self.rs[0],c,ROOT))
 def test_required_pin_binding_cannot_disappear(self):
  path=ROOT/'scripts/fixed_kanripo_witness_pins.json';data=json.loads(path.read_bytes());data['chapter_bindings'].pop(self.ch['id']);original=Path.read_text
  def read(p,*a,**kw):return json.dumps(data)if p==path else original(p,*a,**kw)
  with patch.object(Path,'read_text',read):self.assertFalse(facts.valid(self.rs[0],self.ch,ROOT))
 def test_projection_coshift_rejected(self):
  path=ROOT/self.ch['annotation']['fixed_kanripo_projection_ref'];data=json.loads(path.read_bytes());u=data['unit'];u['start']+=1;u['end']+=1
  for p in data['paragraphs']:p['raw_positions']=[x+1 for x in p['raw_positions']]
  original=Path.read_text
  def read(p,*a,**kw):return json.dumps(data)if p==path else original(p,*a,**kw)
  with patch.object(Path,'read_text',read):self.assertFalse(facts.valid(self.rs[0],self.ch,ROOT))
 def test_missing_source_projection_rejected(self):
  c=copy.deepcopy(self.ch);c['annotation'].pop('fixed_kanripo_projection_ref');self.assertFalse(facts.valid(self.rs[0],c,ROOT))
 def test_legacy_025_api_and_exact_records_unchanged(self):
  r=json.loads(facts.RECIPE_PATH.read_text());ch=json.loads((ROOT/r['chapter_path']).read_bytes());rr,roles=facts.grammar(ch,ROOT);self.assertEqual(rr,r);expected=[facts.expand(s['record'],roles)for s in r['slots']];self.assertEqual(facts.records(ch,ROOT),expected);self.assertTrue(all(facts.valid(a,ch,ROOT)for a in expected))

 def test_coherent_pronoun_reassignment_breaks_received_identity_thread(self):
  c=copy.deepcopy(self.ch);a=copy.deepcopy(self.by['ji-stepmother']);mid=a['evidence'][0]['subject_person_mention_id'];wrong=self.by['pre-father-shu']['subject_person_id']
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m['id']==mid:m['person_id']=wrong
  a['subject_person_id']=wrong;self.assertFalse(facts.valid(a,c,ROOT))
 def test_legacy_keyless_paragraph_api_is_preserved(self):
  recipe=json.loads(facts.RECIPE_PATH.read_text());ch=json.loads((ROOT/recipe['chapter_path']).read_bytes());paragraphs={p['id']:(ch['id'],p)for p in ch['paragraphs']};rows=facts.records(ch,ROOT)
  keyless=[a for a in rows if 'key'not in a['fixed_source_fact_binding']];self.assertTrue(keyless)
  self.assertTrue(all(facts.valid_from_paragraphs(a,paragraphs,ROOT)for a in keyless))

if __name__=='__main__':unittest.main()
