import unittest,json,copy,hashlib
from pathlib import Path
from scripts.fixed_kanripo_projection import errors
ROOT=Path(__file__).resolve().parents[1]
class CaoRenCaoChunSource(unittest.TestCase):
 def chapter(self):return json.loads((ROOT/'corpus/sanguozhi/009-caoren-caochun.json').read_text())
 def test_complete_witness(self):
  c=self.chapter();self.assertEqual(errors(c,ROOT),[]);self.assertEqual(len(c['paragraphs']),9);self.assertEqual(sum(len(p['text'])for p in c['paragraphs']),1498);self.assertEqual(c['paragraphs'][0]['text'],'曹仁字子孝太祖從弟也');self.assertTrue(c['paragraphs'][-1]['text'].endswith('演薨子亮嗣'))
 def test_changed_body_rejected(self):
  c=self.chapter();c['paragraphs'][2]['text']+='偽';self.assertTrue(errors(c,ROOT))
 def test_wrong_note_layer_rejected(self):
  c=self.chapter();c['paragraphs'][1]['text_layer']='received_chapter';self.assertTrue(errors(c,ROOT))
 def test_required_projection_cannot_disappear(self):
  c=self.chapter();del c['annotation']['fixed_kanripo_projection_ref'];self.assertTrue(errors(c,ROOT))
 def test_exact_marks_and_ren_seed(self):
  c=self.chapter();reg=json.loads((ROOT/'registry/persons.json').read_text())['persons'];seed=next(p['id']for p in reg if any(e['mention_id']=='c-sanguozhi-015-wenhui:p003:m0046'for e in p['evidence']));hit=[]
  for p in c['paragraphs']:
   z=0
   for m in p['mentions']:
    self.assertLessEqual(z,m['start']);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);z=m['end']
    if m['kind']=='person'and m['surface']in('曹仁','子孝'):self.assertEqual(m['person_id'],seed);hit.append(m['id'])
  self.assertEqual(len(hit),2)
 def test_books_and_known_collective(self):
  c=self.chapter();ms=[m for p in c['paragraphs']for m in p['mentions']];self.assertEqual(len([m for m in ms if m['kind']=='work']),5);m,=[m for m in ms if m['surface']=='其二女'];self.assertIsNone(m['person_id']);self.assertEqual(m['kind'],'unresolved');self.assertTrue(any(m['surface']=='傳子'and m.get('work_id')=='w-fuzi-pei-reference'for m in ms))
if __name__=='__main__':unittest.main()
