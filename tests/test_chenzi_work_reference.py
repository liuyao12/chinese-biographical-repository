"""同一來源稱謂按語境分人／書，不能全域替換陳子。"""
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
J=lambda rel:json.loads((ROOT/rel).read_text())
PAR='c-houhanshu-062-xunhan-zhongchen:chen:chen-ji-body';MID=PAR+':m0039'
class ChenziWorkTests(unittest.TestCase):
 def test_book_anchor_keeps_id_and_offset(self):
  c=J('corpus/houhanshu/062.json');p=next(p for p in c['paragraphs']if p['id']==PAR);m=next(m for m in p['mentions']if m['id']==MID)
  self.assertEqual((m['start'],m['end'],m['surface']),(39,41,'陳子'));self.assertEqual(p['text'][39:41],'陳子');self.assertEqual(m['kind'],'work');self.assertIsNone(m['person_id']);self.assertEqual(m['work_id'],'w-chenzi')
 def test_person_reverse_index_only_this_book_removed(self):
  p=next(p for p in J('registry/persons.json')['persons']if p['id']=='9w8_tqh_ysn_A');self.assertFalse(any(e.get('mention_id')==MID for e in p['evidence']));self.assertFalse(any(MID in a['mention_ids']for a in p['aliases']))
  self.assertTrue(any(a['surface']=='紀'and a['mention_ids']for a in p['aliases']))
  other='c-sanguozhi-022-chenqun-chentai:p003:m0085';self.assertFalse(any(other in a['mention_ids']for a in p['aliases']));self.assertFalse(any(e.get('mention_id')==other for e in p['evidence']))
 def test_reference_only_has_complete_paragraph_not_imported_book(self):
  w=next(w for w in J('registry/works.json')['works']if w['id']=='w-chenzi');self.assertEqual(w['status'],'referenced_only');self.assertEqual(w['books'],[]);self.assertEqual(w['author'],'陳紀')
  e=next(e for e in w['reference_attestations']if e['mention_id']==MID);p=next(p for p in J('corpus/houhanshu/062.json')['paragraphs']if p['id']==PAR);self.assertEqual(e['quote'],p['text'])
if __name__=='__main__':unittest.main()
