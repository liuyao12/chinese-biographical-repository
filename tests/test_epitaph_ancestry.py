import unittest,json,copy
from pathlib import Path
try:from scripts.epitaph_ancestry import valid
except ImportError:from epitaph_ancestry import valid
ROOT=Path(__file__).resolve().parents[1]
class EpitaphAncestry(unittest.TestCase):
 def setUp(self):
  f=next(x for x in json.loads((ROOT/'registry/family-assemblies.json').read_text())['assemblies']if x['id']=='family-langye-wang-dao');self.rows={r['person_id']:r for r in f['members']};self.m=next(m for m in f['members']if m.get('parent_connection',{}).get('interpretation_basis')=='epitaph_named_family_sequence');self.aa={a['id']:a for a in json.loads((ROOT/'corpus/epitaph-wangminzhi/full-assertions.json').read_text())['assertions']};c=json.loads((ROOT/'corpus/epitaph-wangminzhi/full.json').read_text());self.cs={c['id']:c};self.c=c;self.near=self.aa[self.m['parent_connection']['nearer_ancestor_assertion_id']];self.far=self.aa[self.m['parent_connection']['farther_ancestor_assertion_id']]
 def ok(self):return valid(self.m,self.rows,self.aa,self.cs)
 def test_actual(self):self.assertTrue(self.ok())
 def test_not_direct(self):self.m['source_assertion_id']=self.near['id'];self.assertFalse(self.ok())
 def test_not_source_attested_edge(self):self.m['parent_connection']['status']='source_attested';self.assertFalse(self.ok())
 def test_maternal(self):self.far['qualifiers']['lineage']='maternal';self.assertFalse(self.ok())
 def test_farther_father(self):self.far['predicate']='father';self.assertFalse(self.ok())
 def test_wrong_subject(self):self.near['subject_person_id']=self.far['object_person_id'];self.assertFalse(self.ok())
 def test_reverse(self):self.m['parent_person_id']=self.near['subject_person_id'];self.assertFalse(self.ok())
 def test_wrong_ref_source(self):self.m['parent_connection']['references'][0]['source_id']='wrong';self.assertFalse(self.ok())
 def test_trim_ref(self):self.m['parent_connection']['references'][0]['quote']=self.c['paragraphs'][0]['text'][1:];self.assertFalse(self.ok())
 def test_wrong_quote(self):self.near['evidence'][0]['quote']=self.near['evidence'][0]['quote'][1:];self.assertFalse(self.ok())
 def test_wrong_offset(self):self.c['paragraphs'][0]['mentions'][3]['start']+=1;self.assertFalse(self.ok())
 def test_wrong_named_father_anchor(self):self.near['evidence'][0]['object_person_mention_id']=self.far['evidence'][0]['object_person_mention_id'];self.assertFalse(self.ok())
 def test_conflicting_father(self):
  a=copy.deepcopy(self.near);a['subject_person_id']=self.near['object_person_id'];a['object_person_id']=self.near['subject_person_id'];self.aa['conflict']=a;self.assertFalse(self.ok())
 def test_image_upgrade(self):self.c['source']['transcription_witness']['original_stone_or_rubbing_image_verified']=True;self.assertFalse(self.ok())
 def test_human_upgrade(self):self.m['parent_connection']['human_reviewed']=True;self.assertFalse(self.ok())
 def test_missing_reference(self):self.m['parent_connection']['references'].pop();self.assertFalse(self.ok())
 def test_wrong_ordinal(self):self.near['qualifiers']['birth_order']['ordinal']=2;self.assertFalse(self.ok())
 def test_nested_negation_even_rehash(self):
  import hashlib
  p=self.c['paragraphs'][0];p['text']=p['text'].replace('之孫','非孫');q=self.c['annotation']['epitaph_fact_binding'];q['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest()
  for a in [self.near,self.far]:a['qualifiers']['source_clause_binding']=copy.deepcopy(q);a['evidence'][0]['quote']=p['text']
  for r in self.m['parent_connection']['references']:r['quote']=p['text']
  self.assertFalse(self.ok())
if __name__=='__main__':unittest.main()
