"""來源原字不同仍須指同一有完整事件橋的既有身份。"""
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1];J=lambda r:json.loads((ROOT/r).read_text());PID='57e_9c9_e55'
class DumiIdentityTests(unittest.TestCase):
 def test_source_mentions_keep_different_glyphs_and_same_identity(self):
  specs=[('corpus/houhanshu/062.json','c-houhanshu-062-xunhan-zhongchen:hanzhong:han-shao-rong-body:m0147','杜密'),('corpus/sanguozhi/010.json','c-sanguozhi-010-xunyu-xunyou-jiaxu:xunyou:u002:m0033','杜宻')]
  for path,mid,s in specs:
   p,m=next((p,m)for p in J(path)['paragraphs']for m in p['mentions']if m['id']==mid);self.assertEqual(m['person_id'],PID);self.assertEqual(m['surface'],s);self.assertEqual(p['text'][m['start']:m['end']],s)
 def test_evidence_alias_is_source_index_not_compatibility_alias(self):
  people=J('registry/persons.json')['persons'];p=next(p for p in people if p['id']==PID);self.assertEqual(p['label'],'杜宻');self.assertFalse(p.get('id_aliases'))
  mid='c-houhanshu-062-xunhan-zhongchen:hanzhong:han-shao-rong-body:m0147';self.assertEqual([p['id']for p in people if any(e.get('mention_id')==mid for e in p['evidence'])],[PID])
  self.assertTrue(any(a['surface']=='杜密'and mid in a['mention_ids']for a in p['aliases']))
  bridge=J('source-evidence/houhan062-hanzhong-identity-bridges.json');self.assertEqual(bridge['existing_person_ids']['杜密'],PID);self.assertFalse(any(x['label']=='杜密'for x in bridge['new_people']))
 def test_external_primary_context_not_marked_whole_volume(self):
  p=J('source-evidence/houhan062-dumi-context-identity.json');self.assertFalse(p['image_verified']);self.assertFalse(p['human_reviewed']);body=p['excerpts'][1]['body']['text'];self.assertTrue(body.startswith('杜宻字周甫潁川陽城人也'));self.assertTrue(body.endswith('明年坐黨事被徴自殺'));self.assertIn('與李膺俱坐',body)
  self.assertIn('第二獨立古史',p['parallel_digital_witness']['qualification']);d=next(d for d in J('corpus/houhanshu/062-identities.json')['decisions']if d['id']=='d-houhan062-dumi-shared-identity-01');self.assertEqual(d['person_id'],PID);self.assertEqual(len(d['evidence']),2);self.assertFalse(d['human_reviewed'])
if __name__=='__main__':unittest.main()
