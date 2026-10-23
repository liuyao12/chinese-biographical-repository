from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
class Wang080Unresolved(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/jinshu/080-wangxizhi.json').read_text());cls.ps={p['id'].rsplit(':',1)[-1]:p for p in cls.c['paragraphs']};cls.q=json.loads((ROOT/cls.c['annotation']['unresolved_mention_review_ref']).read_text());cls.by={e['received_surface']:e for e in cls.q['entries']}
 def test_every_original_null_has_disposition(self):self.assertEqual(len(self.q['entries']),11);self.assertEqual(len(self.by),11);self.assertEqual(sum(e['disposition']=='resolved_or_split'for e in self.q['entries']),4);self.assertEqual(sum(m['kind']=='unresolved'for p in self.c['paragraphs']for m in p['mentions']),7)
 def test_two_compounds_split_at_original_codepoints(self):
  for term in ['巢許','稷契']:
   ms=self.by[term]['resolution']['resolved_mentions'];self.assertEqual(''.join(m['surface']for m in ms),term);self.assertEqual(len(ms),2);self.assertNotEqual(ms[0]['person_id'],ms[1]['person_id']);self.assertEqual(ms[0]['end'],ms[1]['start'])
 def test_xu_is_not_same_event_speaker_xuxun(self):
  ms=self.ps['p029']['mentions'];xu=next(m['person_id']for m in ms if m['surface']=='許'and m['start']==69);speaker=next(m['person_id']for m in ms if m['surface']=='許詢');self.assertNotEqual(xu,speaker)
 def test_previous_emperor_uses_succession_context(self):
  prev=next(m['person_id']for m in self.ps['p046']['mentions']if m['surface']=='先帝');current=next(m['person_id']for m in self.ps['p046']['mentions']if m['surface']=='孝武帝');local_jianwen=next(m['person_id']for m in self.ps['p008']['mentions']if m['surface']=='會稽王');self.assertNotEqual(prev,current);self.assertEqual(prev,local_jianwen)
 def test_known_sets_are_not_single_person_unknown(self):
  for term in ['二尊','其父子']:
   self.assertEqual(self.by[term]['category'],'exact_known_person_set');self.assertEqual(len(set(self.by[term]['known_person_ids'])),2)
 def test_brother_not_assigned_to_named_father(self):
  e=self.by['兄'];self.assertEqual(e['category'],'anonymous_relative_identity_unresolved');self.assertTrue(e['semantic_constraints']['object_older_than_subject']);self.assertEqual(e['semantic_constraints']['object_generation_relative_to_subject'],0);self.assertIsNone(e['semantic_constraints']['object_person_id']);self.assertIsNone(e['semantic_constraints']['child_father_identity']);self.assertEqual(e['initial_source_only_scope_capture']['qualification'],'historical_source_only_scope_superseded');self.assertTrue(all(r['status']=='source_attested'and r.get('native_assertion_id')for r in e['source_semantic_relations']))
  native=json.loads((ROOT/'corpus/jinshu/080-wangxizhi-assertions.json').read_text());byid={a['id']:a for a in native['assertions']}
  for r in e['source_semantic_relations']:
   a=byid[r['native_assertion_id']];self.assertEqual((a['predicate'],a['subject_person_id'],a['object_person_id']),(r['predicate'],r['subject_person_id'],r['object_person_id']))
   if a['predicate']=='paternal_uncle':self.assertIsNone(a['qualifiers']['father_person_id'])
 def test_lao_surface_remains_lao(self):self.assertEqual(next(m['surface']for m in self.ps['p027']['mentions']if m['surface']=='老氏'),'老氏');self.assertNotIn('李耳',self.ps['p027']['text'])
 def test_review_empty_capture_explicitly_superseded(self):
  d=json.loads((ROOT/'source-evidence/jin080-wangxizhi-source/identity-review.json').read_text());self.assertEqual(len(d['unresolved']),7);self.assertEqual(d['unresolved_review_initial_capture']['value'],[]);self.assertIn('erroneously empty',d['unresolved_review_initial_capture']['qualification'])
if __name__=='__main__':unittest.main()
