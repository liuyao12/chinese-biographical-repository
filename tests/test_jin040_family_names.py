# coding: utf-8
from pathlib import Path
import json,copy,unittest,hashlib
from scripts.fixed_biography_names import component_valid,validate_surname
R=Path(__file__).resolve().parents[1];C=json.loads((R/'corpus/jinshu/040-jiachong-family.json').read_text());NS=json.loads((R/'corpus/jinshu/040-jiachong-family-name-components.json').read_text())['records'];AA=json.loads((R/'corpus/jinshu/040-jiachong-family-assertions.json').read_text())['assertions']
class FamilyNameTests(unittest.TestCase):
 def test_all_actual_components_and_23_paths(self):
  self.assertEqual(len(NS),123);self.assertEqual(sum('surname_basis'in n for n in NS),23)
  for n in NS:
   self.assertTrue(component_valid(n,C,R,AA),n['id'])
   if 'surname_basis'in n:validate_surname(n,NS,{C['id']:C},AA,R)
 def test_wrong_person_even_when_same_paragraph(self):
  for n in NS:
   p=next(p for p in C['paragraphs']if p['id']==n['paragraph_id']);other=next((m for m in p['mentions']if m.get('person_id')and m['person_id']!=n['person_id']),None)
   if other:
    b=copy.deepcopy(n);b['person_id']=other['person_id'];self.assertFalse(component_valid(b,C,R,AA))
 def test_other_person_courtesy_not_borrowed(self):
  rows=[n for n in NS if n.get('zi')];self.assertEqual(len(rows),7)
  for n in rows:
   b=copy.deepcopy(n);b['zi']='他字';self.assertFalse(component_valid(b,C,R,AA))
 def test_no_courtesy_as_given_name(self):
  n=next(n for n in NS if n.get('zi')=='公閭');b=copy.deepcopy(n);p,m=next((p,m)for p in C['paragraphs']for m in p['mentions']if m['surface']=='賈公閭');b.update(ming='公閭',paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id']);b.pop('zi');bind=b['fixed_biography_name_binding'];bind.update(zi_mention_id=None,name_mention_id=m['id'],paragraph_sha256=hashlib.sha256(p['text'].encode()).hexdigest());self.assertFalse(component_valid(b,C,R,AA))
 def test_alias_is_not_former_name_or_absolute_year(self):
  rows=[n for n in NS if n.get('additional_name_components')];self.assertEqual(len(rows),2)
  for n in rows:
   self.assertEqual(n['additional_name_components'][0]['chronology'],'unspecified')
   b=copy.deepcopy(n);b['former_ming']=b['additional_name_components'][0]['value'];self.assertFalse(component_valid(b,C,R,AA))
   b=copy.deepcopy(n);b['additional_name_components'][0]['chronology']='earlier';self.assertFalse(component_valid(b,C,R,AA))
 def test_clan_only_not_invented_given_name(self):
  rows=[n for n in NS if n['fixed_biography_name_binding']['mode']=='clan_only'];self.assertEqual(len(rows),2)
  for n in rows:
   self.assertIsNone(n['ming']);b=copy.deepcopy(n);b['ming']='婉';self.assertFalse(component_valid(b,C,R,AA))
 def test_title_not_family_name_or_given_name(self):
  n=next(n for n in NS if n['fixed_biography_name_binding']['mode']=='titled_given'and n['ming']=='旦');self.assertIsNone(n['surname']);b=copy.deepcopy(n);b['surname']='公';self.assertFalse(component_valid(b,C,R,AA))
 def test_han_jia_source_uses_not_preferred_or_dated(self):
  rows=[n for n in NS if n.get('source_name_usage')];self.assertEqual({n['surname']for n in rows},{'韓','賈'});self.assertEqual(len({n['person_id']for n in rows}),1)
  for n in rows:
   self.assertIsNone(n['source_name_usage']['change_year']);b=copy.deepcopy(n);b['source_name_usage']['preferred']=True;self.assertFalse(component_valid(b,C,R,AA));b=copy.deepcopy(n);b['source_name_usage']['change_year']=282;self.assertFalse(component_valid(b,C,R,AA))
 def test_structural_id_label_cannot_supply_surname(self):
  n=next(n for n in NS if n.get('surname_basis'));b=copy.deepcopy(n);b['surname_basis']['kind']='from_family_id'
  with self.assertRaises(ValueError):validate_surname(b,NS,{C['id']:C},AA,R)
 def test_steps_cannot_skip_generation_or_invent_parent(self):
  for n in NS:
   if 'surname_basis'in n:
    b=copy.deepcopy(n);b['surname_basis']['steps'][0]['generation_after']+=1
    with self.assertRaises(ValueError):validate_surname(b,NS,{C['id']:C},AA,R)
 def test_maternal_spouse_adoption_not_surname_route(self):
  n=next(n for n in NS if n.get('surname_basis'))
  for a in AA:
   if a['predicate']in('mother','maternal_role','spouse','adoptive_father')or a['qualifiers'].get('lineage')=='maternal':
    b=copy.deepcopy(n);b['surname_basis']['steps'][0]['assertion_id']=a['id']
    with self.assertRaises(ValueError):validate_surname(b,NS,{C['id']:C},AA,R)
 def test_consistent_maternal_and_adoptive_routes_are_rejected(self):
  for a in AA:
   if a['predicate']=='mother'and a['qualifiers']['received_family_frame']['rule']=='named_mother_daughter_princess':
    seed=next(n for n in NS if n['person_id']==a['object_person_id']and n['fixed_biography_name_binding']['mode']=='full_name');target=next(n for n in NS if n['person_id']==a['subject_person_id']and n.get('surname_basis'));direction='object_to_subject';delta=1
   elif a['predicate']=='adoptive_father':
    seed=next(n for n in NS if n['person_id']==a['subject_person_id']and n['fixed_biography_name_binding']['mode']=='full_name');target=next(n for n in NS if n['person_id']==a['object_person_id']and n.get('surname_basis'));direction='subject_to_object';delta=-1
   elif a['qualifiers'].get('source_term')=='從舅':
    seed=next(n for n in NS if n['person_id']==a['object_person_id']and n['fixed_biography_name_binding']['mode']=='full_name');target=next(n for n in NS if n['person_id']==a['subject_person_id']and n.get('surname_basis'));direction='object_to_subject';delta=1
   else:continue
   b=copy.deepcopy(target);b['surname']=seed['surname'];basis=b['surname_basis'];basis['seed_name_record_id']=seed['id'];basis['steps']=[{'assertion_id':a['id'],'from_person_id':seed['person_id'],'to_person_id':target['person_id'],'generation_before':0,'generation_after':delta,'traversal':direction}]
   self.assertTrue(component_valid(b,C,R,AA))
   with self.assertRaises(ValueError):validate_surname(b,NS,{C['id']:C},AA,R)
 def test_cycle_duplicate_and_empty_paths_rejected(self):
  n=next(n for n in NS if n.get('surname_basis'))
  for steps in([],n['surname_basis']['steps']*2):
   b=copy.deepcopy(n);b['surname_basis']['steps']=copy.deepcopy(steps)
   with self.assertRaises(ValueError):validate_surname(b,NS,{C['id']:C},AA,R)
 def test_raw_and_original_components_stay_source_scoped(self):
  self.assertEqual(next(n for n in NS if n.get('ming')=='顗'and n.get('surname')=='裴')['surname'],'裴');self.assertEqual(next(n for n in NS if n.get('ming')=='浚'and n.get('surname')=='王')['surname'],'王');self.assertTrue(all(not n.get('preferred')for n in NS))
if __name__=='__main__':unittest.main()
