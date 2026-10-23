"""當前022人物錨與非人物詞的來源回歸；不依賴私人包。"""
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=lambda p:json.loads((R/p).read_text())
C=J('corpus/sanguozhi/022-chenqun-chentai.json');D=J('source-evidence/sanguozhi022-ner-review/review.json');CP=C['id'];PS={p['id']:p for p in C['paragraphs']};M={m['id']:m for p in C['paragraphs']for m in p['mentions']}
class SourceNER(unittest.TestCase):
 def test_three_non_person_links_absent_current(self):
  removed={CP+':p001:m0905',CP+':p003:m0084',CP+':p010:m1454'}
  self.assertTrue(removed.isdisjoint(M));reg=J('registry/persons.json');live=json.dumps(reg,ensure_ascii=False)
  for mid in removed:self.assertNotIn(mid,live)
  self.assertTrue({'e03_b20_30c','9w8_tqh_ysn_A','9w8_tqh_ysn_AA'}<={r['id']for r in reg['persons']})
 def test_received_words_preserved(self):
  self.assertEqual(PS[CP+':p001']['text'][905:906],'布');self.assertEqual(PS[CP+':p003']['text'][84:85],'之');self.assertEqual(PS[CP+':p010']['text'][1454:1455],'己')
 def test_jun_preference_and_non_person_alternative(self):
  m=M[CP+':p001:m1623'];self.assertEqual(m['person_id'],'9w8_tqh_ysn_AA');self.assertEqual(m['status'],'contextual_provisional')
  d=D['structured_decisions'][0];self.assertEqual(d['preferred_person_id'],m['person_id']);self.assertEqual(d['alternatives'],[{'classification':'generic_role','generic_role':'君主','person_id':None}])
  for e in d['evidence']:
   p=next(p for p in C['paragraphs']if p['id']==e['paragraph_id']);self.assertEqual(p['text'][e['start']:e['end']],e['quote'])
  self.assertIn('頃之為司空',d['evidence'][0]['quote']);self.assertIn('君之職',d['evidence'][1]['quote'])
 def test_he_and_yi_are_not_blind_lexical_removals(self):
  for mid in [CP+':p007:m0036',CP+':p007:m0117',CP+':p001:m1810']:self.assertEqual(M[mid]['kind'],'person');self.assertIsNotNone(M[mid]['person_id'])
  self.assertEqual(M[CP+':p007:m0036']['person_id'],M[CP+':p007:m0117']['person_id'])
 def test_all_disposition_anchors_remain_exact(self):
  for d in D['dispositions']:
   p=next(p for p in C['paragraphs']if p['id']==d['paragraph_id']);self.assertEqual(p['text'][d['start']:d['end']],d['surface'])
  self.assertEqual({d['paragraph_id']for d in D['dispositions']},{p['id']for p in C['paragraphs']})
 def test_audit_not_presented_as_current(self):
  r=J('source-evidence/pei-weishu-author-identity/review.json');self.assertIn('audit_before_quote_units',json.dumps(r));q=r['ner_snapshot_qualifications'];self.assertEqual(q[-1]['scope'],'reading_snapshot_not_current_annotations');self.assertEqual(q[-1]['decision_path'],'source-evidence/sanguozhi022-ner-review/review.json')
if __name__=='__main__':unittest.main()
