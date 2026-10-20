import unittest,json
from pathlib import Path
from scripts.person_bundle import bundle,load_catalog
from scripts.family_assemblies import load_assemblies
R=Path(__file__).resolve().parents[1]
G='h7n_w5t_i1c';F=G+'_A';X=G+'_AA';Z=G+'_AAA';S=G+'_AAA*A';E=G+'_AAAA';B=G+'_AAB'
def J(p):return json.loads((R/p).read_text())
class CaoConnectedFamily(unittest.TestCase):
 def setUp(self):self.family=next(a for a in J('registry/family-assemblies.json')['assemblies']if a['id']=='family-caoxiu-zhao-shu');self.rows={r['person_id']:r for r in self.family['members']};self.a=J('corpus/sanguozhi/009-caoxiu-assertions.json')['assertions']
 def test_earliest_attested_grandfather_root(self):self.assertEqual(self.family['root_person_id'],G);self.assertEqual(set(self.rows),{G,F,X,Z,S,E,B});self.assertEqual(self.rows[X]['parent_person_id'],F);self.assertEqual(self.rows[Z]['parent_person_id'],X);self.assertEqual(self.rows[E]['parent_person_id'],Z)
 def test_no_fake_father_of_father_source(self):self.assertIsNone(self.rows[F]['source_assertion_id']);self.assertEqual(self.rows[F]['parent_connection']['type'],'parent_between_body_and_attached_note_ancestors');self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==F for a in self.a))
 def test_unknown_caoshu_father_is_not_xing(self):self.assertIsNone(self.rows[S]['parent_person_id']);self.assertEqual(self.rows[S]['ancestor_person_id'],Z);self.assertEqual(self.rows[S]['generation_distance'],2);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==S for a in self.a));people={p['id']for p in J('registry/persons.json')['persons']};self.assertNotIn(G+'_AAA*',people)
 def test_zuan_same_father_is_editorial_not_birth_order(self):r=self.rows[B];self.assertEqual(r['parent_person_id'],X);self.assertIsNone(r['source_assertion_id']);self.assertEqual(r['parent_connection']['type'],'shared_father_through_sibling');self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==B for a in self.a));t=next(t for t in J('source-evidence/sgz009-caoxiu/typed-boundaries.json')if t['id']=='sgz00954a-zhao-zuan-relative-order');self.assertEqual((t['older_person_id'],t['younger_person_id'],t['operator']),(Z,B,'lt'));self.assertIsNone(t['absolute_ordinal'])
 def test_mother_does_not_spread_to_descendants(self):m=[a for a in self.a if a['predicate']=='mother'];self.assertEqual(len(m),1);self.assertEqual(m[0]['subject_person_id'],X);self.assertNotIn(m[0]['object_person_id'],self.rows);self.assertFalse(any(a['predicate']=='biological_mother'for a in self.a))
 def test_family_not_linked_to_cao_cao(self):self.assertNotIn('dad_b77_b38',self.rows);self.assertFalse(any(a['predicate']in['father','adoptive_father']and a['subject_person_id']==X and a['object_person_id']=='dad_b77_b38'for a in self.a))
 def test_real_bundles_have_single_person_and_correct_ancestor(self):
  cat=load_catalog(R);sm,_=load_assemblies(R,cat)
  for pid in self.rows:
   b=bundle(pid,root=R,catalog=cat,include_provisional=True);b['assembled_identity']=sm[pid];self.assertEqual(b['person_ids'],[pid]);self.assertEqual(b['assembled_identity']['root_person_id'],G)
  b=bundle(S,root=R,catalog=cat,include_provisional=True);b['assembled_identity']=sm[S];self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==S for a in b['relations']));self.assertEqual(b['assembled_identity']['ancestor_person_id'],Z)
 def test_cao_xiu_not_reassigned_to_grandfather(self):people=J('registry/persons.json')['persons'];x=[p for p in people if p['label']=='曹休'];self.assertEqual([p['id']for p in x],[X]);self.assertIn('未名祖父',next(p for p in people if p['id']==G)['label']);self.assertTrue(all(m.get('human_reviewed',False)is False for m in self.rows.values()))
