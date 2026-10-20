import copy,json,unittest
from pathlib import Path
from scripts.biographical_ancestry import biographical_zu_fu_parent_valid
ROOT=Path(__file__).resolve().parents[1]
class BiographicalAncestryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.assemblies=json.loads((ROOT/'registry/family-assemblies.json').read_text())['assemblies']
  cls.ch=json.loads((ROOT/'corpus/songshu/041-parents.json').read_text())
  cls.assertions={a['id']:a for a in json.loads((ROOT/'corpus/songshu/041-parents-kinship-assertions.json').read_text())['assertions']}
 def case(self,index=0):
  a=next(a for a in self.assemblies if a['id']==['family-song041-zhao-biao','family-song041-xiao-liang'][index]);rows={m['person_id']:copy.deepcopy(m) for m in a['members']};member=next(m for m in rows.values() if m.get('parent_connection',{}).get('interpretation_basis')=='biographical_zu_fu_sequence');return member,rows,copy.deepcopy(self.assertions),{self.ch['id']:copy.deepcopy(self.ch)}
 def test_direct_script_import_path(self):
  import types,sys
  from unittest.mock import patch
  helper=types.ModuleType('biographical_ancestry');exec(compile((ROOT/'scripts/biographical_ancestry.py').read_text(),str(ROOT/'scripts/biographical_ancestry.py'),'exec'),helper.__dict__)
  direct=types.ModuleType('ancestry_chain');exec(compile((ROOT/'scripts/ancestry_chain.py').read_text(),str(ROOT/'scripts/ancestry_chain.py'),'exec'),direct.__dict__)
  with patch.dict(sys.modules,{'biographical_ancestry':helper}):self.assertTrue(direct.consecutive_ancestor_parent_valid(*self.case()))
 def test_two_qualified_opening_sequences(self):
  for i in range(2):
   args=self.case(i);self.assertTrue(biographical_zu_fu_parent_valid(*args));far=args[2][args[0]['parent_connection']['farther_ancestor_assertion_id']];self.assertEqual(far['qualifiers']['lineage'],'unspecified')
 def test_maternal_ancestor_rejected(self):
  a=self.case();a[2][a[0]['parent_connection']['farther_ancestor_assertion_id']]['qualifiers']['lineage']='maternal';self.assertFalse(biographical_zu_fu_parent_valid(*a))
 def test_missing_subject_anchor_rejected(self):
  a=self.case();p=next(iter(a[3].values()))['paragraphs'][0];p['mentions']=[m for m in p['mentions'] if m['start']!=0];self.assertFalse(biographical_zu_fu_parent_valid(*a))
 def test_rebound_grandfather_span_rejected(self):
  a=self.case();far=a[2][a[0]['parent_connection']['farther_ancestor_assertion_id']];p=next(iter(a[3].values()))['paragraphs'][0]
  for m in p['mentions']:
   if m.get('person_id')==far['object_person_id']:m['person_id']='different_person'
  self.assertFalse(biographical_zu_fu_parent_valid(*a))
 def test_cross_paragraph_evidence_rejected(self):
  a=self.case();a[2][a[0]['parent_connection']['nearer_ancestor_assertion_id']]['evidence'][0]['paragraph_id']='different';self.assertFalse(biographical_zu_fu_parent_valid(*a))
 def test_direct_conflicting_father_rejected(self):
  a=self.case();a[2]['conflict']={'predicate':'father','subject_person_id':a[0]['source_person_ids'][0],'object_person_id':'other'};self.assertFalse(biographical_zu_fu_parent_valid(*a))
 def test_raw_direct_father_not_fabricated(self):
  a=self.case();self.assertIsNone(a[0]['source_assertion_id']);self.assertFalse(any(v['predicate']=='father' and v['subject_person_id'] in a[0]['source_person_ids'] for v in a[2].values()))
 def test_qualified_references_required(self):
  a=self.case();a[0]['parent_connection']['references'][0]['scope']='';self.assertFalse(biographical_zu_fu_parent_valid(*a))
if __name__=='__main__':unittest.main()
