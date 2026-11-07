"""One explicit author self-commentary identity; ROOT-only, portable, no file mutations."""
import json,hashlib,unittest,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Song067LisiSelfCommentary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/songshu/067-xielingyun.json').read_text());cls.p=next(p for p in cls.c['paragraphs']if p['id']=='c-songshu-067-xielingyun:p006');cls.seed=json.loads((ROOT/'corpus/shiji/087.json').read_text());cls.q=next(p for p in cls.seed['paragraphs']if p['id']=='c-shiji-087-lisi:p033');cls.sm=next(m for m in cls.q['mentions']if m['id']=='c-shiji-087-lisi:m033-0008');cls.pid=cls.sm['person_id'];cls.m=next(m for m in cls.p['mentions']if m['id']=='c-songshu-067-xielingyun:p006:m00263');cls.person=next(p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']if p['id']==cls.pid);cls.ref=json.loads((ROOT/'source-evidence/song067-lisi-selfcommentary-reading.json').read_text());cls.decision=json.loads((ROOT/'corpus/songshu/067-lisi-selfcommentary-identities.json').read_text())['decisions'][0]
 def test_actual_source_mid_and_specific_parallel(self):
  self.assertEqual((self.m['kind'],self.m['person_id'],self.m['surface'],self.m['start'],self.m['end']),('person',self.pid,'李斯',263,265));self.assertEqual(self.p['text'][263:265],'李斯');self.assertIn('牽黃犬俱出上蔡東門',self.q['text']);self.assertEqual(self.sm['surface'],'斯');self.assertNotIn('candidate_person_ids',self.m);self.assertNotIn('unresolved_reason',self.m)
 def test_author_self_commentary_not_outer_author(self):
  layer=self.ref['self_commentary_layer'];self.assertEqual(layer['kind'],'author_self_commentary');self.assertEqual(self.p['text'][layer['start']:layer['end']],layer['quote']);self.assertIn('牽犬李斯之歎聽鶴/陸機',layer['quote']);self.assertEqual(self.ref['own_context_units'][-1]['end'],291);self.assertTrue(self.p['text'][291:].startswith('若夫巢穴'));self.assertNotEqual(self.pid,next(m['person_id']for m in next(p for p in self.c['paragraphs']if p['id']=='c-songshu-067-xielingyun:p001')['mentions']if m['surface']=='謝靈運'))
 def test_exact_alias_and_complete_reverse(self):
  mid=self.m['id'];self.assertTrue(any(a['surface']=='李斯'and mid in a['mention_ids']for a in self.person['aliases']));e={k:self.c[k]for k in('work_id','book_id','source_id')}|{'chapter_id':self.c['id'],'paragraph_id':self.p['id'],'mention_id':mid,'quote':'李斯'};self.assertIn(e,self.person['evidence'])
 def test_complete_crosschapter_decision_and_old_annotation_qualification(self):
  d=self.decision;self.assertEqual(d['person_id'],self.pid);self.assertEqual(d['scope'],'cross_chapter');self.assertEqual(set(d['chapter_ids']),{self.c['id'],self.seed['id']});self.assertEqual([e['quote']for e in d['evidence']],[self.p['text'],self.q['text']]);self.assertEqual(d['prior_annotation_qualification']['original_marker']['kind'],'unresolved');self.assertFalse(d['human_reviewed']);self.assertIsNone(d['model'])
 def test_fixed_raw_projection_and_inherited_witness_qualification(self):
  self.assertEqual(hashlib.sha256((ROOT/self.ref['source_raw_path']).read_bytes()).hexdigest(),self.ref['source_raw_sha256']);self.assertEqual(self.c['source']['source_commit'],'e80c057667e3c8684f11d5088251e10244d5a264');self.assertEqual(self.c['source']['base_edition'],'WYG');self.assertFalse(self.c['source']['image_verified']);self.assertFalse(self.ref['human_reviewed']);self.assertFalse(self.ref['image_verified'])
 def test_normal_xml_preserves_all_text_and_resolves_only_named_anchor(self):
  x=ET.parse(ROOT/'corpus/songshu/067-xielingyun.xml').getroot();self.assertEqual([''.join(q.itertext())for q in x.findall('p')],[q['text']for q in self.c['paragraphs']]);m=next(n for n in x.iter('persName')if n.get('id')==self.m['id']);self.assertEqual(m.get('ref'),self.pid);self.assertEqual(m.text,'李斯')
if __name__=='__main__':unittest.main()
