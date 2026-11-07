import copy,json,hashlib
from unittest.mock import patch
from scripts import fixed_jin034_yanghu_ner as core,fixed_jin034_core_kinship as m
from scripts.source_family_counts import close_kin_counts
from tests.test_jin034_yanghu_ner import YangHuNER
from tests.jin034_phase_fixture import synchronized_minimal_parent_pins
class CoreKinship(YangHuNER):
 def test_literal_kinship_and_maternal_limits(self):
  b,r,people,ch=m.state(self.T);a=core.read(self.T,m.AP)['assertions'];self.assertEqual(len(a),27)
  by={x['id']:x for x in a};self.assertEqual(by['a-jin034-fa-birthmother']['object_person_id'],r['qianmu_kong']);self.assertEqual(by['a-jin034-hu-mother-general']['predicate'],'maternal_role');self.assertIsNone(by['a-jin034-hu-mother-general']['qualifiers']['biological_mother']);self.assertEqual(by['a-jin034-son-in-law']['subject_person_id'],r['unnamed_son_in_law']);self.assertEqual(by['a-jin034-son-in-law']['object_person_id'],r['yang_hu']);self.assertNotIn('reported_ordinal',by['a-jin034-fa-older-brother']['qualifiers'])
 def test_source_reports_scope_not_lifetime(self):
  reports=core.read(self.T,m.CP)['reports'];self.assertEqual(len(reports),6);by={x['source_binding']['slot']:x for x in reports};self.assertIsNone(by['sons-plural']['reported_count']);self.assertIsNone(by['no-sons-in-anecdote']['accepted_lifetime_child_count']);self.assertEqual(by['nine-generations']['unit'],'reported_generations');self.assertIsNone(by['nine-generations']['person_path']);self.assertTrue(by['daughter-existence']['existence']);self.assertEqual(by['daughter-existence']['bounds']['lower'],1);self.assertIsNone(by['daughter-existence']['daughter_person_id']);self.assertIsNone(by['faxing-unnamed-brother-line']['unnamed_brother_person_id'])
 def _self_consistent_wrong_assertion(self,slot,fn):
  self.change(m.AP,lambda d:fn(next(a for a in d['assertions']if a['id']=='a-jin034-'+slot)))
  b=core.read(self.T,m.EP);fn(next(a for a in b['expected_documents'][m.AP]['assertions']if a['id']=='a-jin034-'+slot));p=self.T/m.EP;p.write_text(json.dumps(b,ensure_ascii=False)+'\n')
  with patch.object(m,'PROOF_SHA',hashlib.sha256(p.read_bytes()).hexdigest()),synchronized_minimal_parent_pins(self.T):
   with self.assertRaises(ValueError):core.accepted_state(self.T)
 def test_mother_cannot_become_birthmother_even_template_changed(self):self._self_consistent_wrong_assertion('hu-mother-general',lambda a:a.update(predicate='mother'))
 def test_brother_cannot_copy_father_even_template_changed(self):self._self_consistent_wrong_assertion('cheng-maternal-brother',lambda a:a.update(predicate='father',object_person_id=self.r['yang_dao']))
 def test_previous_mother_not_stepmother(self):self._self_consistent_wrong_assertion('hu-previous-mother',lambda a:a.update(predicate='stepmother'))
 def test_ritual_cannot_be_birthfather(self):self._self_consistent_wrong_assertion('pian-ritual-successor',lambda a:a.update(predicate='father'))
 def test_declined_ji_not_completed_successor(self):self._self_consistent_wrong_assertion('pian-ritual-successor',lambda a:a.update(subject_person_id=self.r['yang_ji']))
 def test_single_end_missing_reverse_rejected(self):
  self.change(m.AP,lambda d:d['assertions'][0].update(object_person_id=self.r['yang_cheng']))
  with self.assertRaises(ValueError):m.state(self.T)
 def test_missing_family_sidecar(self):
  p=self.T/m.AP;raw=p.read_bytes();p.unlink()
  try:
   with self.assertRaises((ValueError,OSError)):m.state(self.T)
  finally:p.write_bytes(raw)
 def test_generic_dispatch_rejects_unknown_owner(self):
  people={p['id']:p for p in core.read(self.T,'registry/persons.json')['persons']};records=self.records()+[core.read(self.T,m.AP),core.read(self.T,m.CP)];records[-1]['owner']='unknown_family_owner'
  with self.assertRaisesRegex(ValueError,'未知來源親屬報數owner'):close_kin_counts(records,people,self.T,set(people))
 def test_wrong_external_sex_qualification(self):
  rel=core.BASE+'kinship-references/caiyong-sex-reading.json';self.change(rel,lambda x:x.update(fixed_revision_content_retrieved=True))
  b=core.read(self.T,m.EP);b['reference_pins'][rel]=hashlib.sha256((self.T/rel).read_bytes()).hexdigest();p=self.T/m.EP;p.write_text(json.dumps(b,ensure_ascii=False)+'\n')
  with patch.object(m,'PROOF_SHA',hashlib.sha256(p.read_bytes()).hexdigest()),synchronized_minimal_parent_pins(self.T):
   with self.assertRaisesRegex(ValueError,'蔡邕性別參讀取得/版本資格'):m.state(self.T)
 def test_no_extra_assertion_same_source(self):
  self.change(m.AP,lambda x:x['assertions'].append(copy.deepcopy(x['assertions'][0])))
  with self.assertRaises(ValueError):m.state(self.T)

 def test_liang_paternal_preference_keeps_unknown_father(self):
  a=next(a for a in core.read(self.T,m.AP)['assertions']if a['id']=='a-jin034-liang-grandfather');self.assertEqual(a['qualifiers']['lineage'],'paternal');self.assertIsNone(a['qualifiers']['father_person_id']);self.assertIsNone(a['qualifiers']['lineage_reading']['father_person_id']);self.assertEqual(a['qualifiers']['lineage_reading']['status'],'editorial_provisional')
 def test_liang_wrong_father_zhi_even_template_pin_changed(self):
  self._self_consistent_wrong_assertion('liang-grandfather',lambda a:a['qualifiers'].update(father_person_id=self.r['yang_zhi']))

 def test_unrelated_partial_catalog_keeps_old_no_source_behavior(self):
  self.assertEqual(close_kin_counts([],{},self.T,{'not-a-source-person'}),[])
 def test_related_partial_catalog_cannot_drop_source(self):
  with self.assertRaises(ValueError):close_kin_counts([],self.people,self.T,{self.r['yang_hu']})

 def _self_consistent_wrong_count(self,slot,fn):
  self.change(m.CP,lambda d:fn(next(a for a in d['reports']if a['source_binding']['slot']==slot)))
  b=core.read(self.T,m.EP);fn(next(a for a in b['expected_documents'][m.CP]['reports']if a['source_binding']['slot']==slot));p=self.T/m.EP;p.write_text(json.dumps(b,ensure_ascii=False)+'\n')
  with patch.object(m,'PROOF_SHA',hashlib.sha256(p.read_bytes()).hexdigest()),synchronized_minimal_parent_pins(self.T):
   with self.assertRaisesRegex(ValueError,'來源報數/存在/世距/故事範圍'):core.accepted_state(self.T)
 def test_nine_generations_not_nine_people_even_template_pin_changed(self):self._self_consistent_wrong_count('nine-generations',lambda r:r.update(unit='persons'))
 def test_story_no_zi_not_lifetime_child_zero_even_template_pin_changed(self):self._self_consistent_wrong_count('no-sons-in-anecdote',lambda r:r.update(accepted_lifetime_child_count=0))

 def test_refused_succession_reading_not_completed_even_template_pin_changed(self):
  gp=self.b['groups_path'];self.change(gp,lambda d:next(r for r in d['unresolved_readings']if r['id']=='reading-jin034-ji-declined-ritual-succession')['qualifiers'].update(outcome='assumed'))
  b=core.read(self.T,m.EP);next(r for r in b['group_reading_additions']if r['id']=='reading-jin034-ji-declined-ritual-succession')['qualifiers']['outcome']='assumed';p=self.T/m.EP;p.write_text(json.dumps(b,ensure_ascii=False)+'\n')
  with patch.object(m,'PROOF_SHA',hashlib.sha256(p.read_bytes()).hexdigest()),synchronized_minimal_parent_pins(self.T):
   with self.assertRaisesRegex(ValueError,'qualified母系/拒嗣讀法'):core.accepted_state(self.T)
