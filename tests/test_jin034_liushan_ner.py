from pathlib import Path
import unittest,json,copy
from scripts.fixed_witness_fact_slots import grammar,records
ROOT=Path(__file__).resolve().parents[1]
class LiushanNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/jinshu/034-yanghu.json').read_text());cls.p=next(p for p in cls.c['paragraphs']if p['id'].endswith(':p018'));cls.ms=[m for m in cls.p['mentions']if m['surface']=='劉禪']
 def test_two_exact_original_name_spans_and_one_source_identity(self):
  self.assertEqual(len(self.ms),2);self.assertEqual(len({m['person_id']for m in self.ms}),1);self.assertEqual(len({m['id']for m in self.ms}),2)
  for m in self.ms:self.assertEqual(self.p['text'][m['start']:m['end']],'劉禪');self.assertEqual(m['status'],'source_explicit')
  self.assertIn('至劉禪降服',self.p['text']);self.assertIn('侈于劉禪',self.p['text'])
 def test_liushan_is_not_sunhao_and_reverse_evidence_complete(self):
  pid=self.ms[0]['person_id'];sun=next(m['person_id']for m in self.p['mentions']if m['surface']=='孫皓');self.assertNotEqual(pid,sun);people=json.loads((ROOT/'registry/persons.json').read_text())['persons'];p=next(x for x in people if x['id']==pid)
  self.assertEqual({e['mention_id']for e in p['evidence']if e['chapter_id']==self.c['id']},{m['id']for m in self.ms});self.assertEqual(p['label'],'劉禪')
 def test_family37_facts_remain_full_after_ner(self):
  rs=records(self.c,ROOT);family=[v for v in rs if v['fixed_source_fact_binding']['slot'].startswith(('kin_','detail_'))];self.assertEqual(len(family),37);self.assertEqual({v['fixed_source_fact_binding']['slot'] for v in family},{'kin_'+str(n).zfill(3) for n in range(1,32)}|{'detail_'+str(n).zfill(3) for n in range(1,7)})
 def test_coherent_collapse_into_sunhao_is_rejected(self):
  c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id'].endswith(':p018'));sun=next(m['person_id']for m in p['mentions']if m['surface']=='孫皓')
  for m in p['mentions']:
   if m['surface']=='劉禪':m['person_id']=sun
  with self.assertRaises(AssertionError):grammar(c,ROOT)
 def test_missing_one_or_both_new_name_marks_is_rejected(self):
  for allmarks in [False,True]:
   c=copy.deepcopy(self.c);p=next(p for p in c['paragraphs']if p['id'].endswith(':p018'));gone={m['id']for m in self.ms}if allmarks else{self.ms[0]['id']};p['mentions']=[m for m in p['mentions']if m['id']not in gone]
   with self.assertRaises((AssertionError,IndexError)):grammar(c,ROOT)
