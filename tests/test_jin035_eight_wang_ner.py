# coding:utf-8
import unittest,json,sys,copy,hashlib
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
CID='c-jinshu-035-peikai-family';PAR=CID+':p019';MID=PAR+':m0061'
class EightWangNERTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts.person_bundle import load_catalog
  cls.people,cls.rows=load_catalog(R);cls.ch=next(c for c in cls.rows if c.get('id')==CID);cls.p=next(p for p in cls.ch['paragraphs']if p['id']==PAR);cls.m=next(m for m in cls.p['mentions']if m['id']==MID);cls.pid=cls.m['person_id']
 def test_full_eight_pairs_and_closing_yun(self):
  self.assertEqual(self.p['text'],'初，裴、王二族盛于魏晉之世，時人以為八裴方八王：徽比王祥，楷比王衍，康比王綏，綽比王澄，瓚比王敦，遐比王導，頠比王戎，邈比王玄雲。');self.assertEqual(self.p['text'].count('比'),8);self.assertEqual((self.m['start'],self.m['end'],self.m['surface']),(61,63,'王玄'));self.assertEqual(self.p['text'][63],'雲');self.assertFalse(any(m['start']<=63<m['end']for m in self.p['mentions']))
 def test_resolved_person_has_source_reverse_evidence(self):
  other=next(c for c in self.rows if c.get('id')=='c-jinshu-043-wangyan');other_pid=next(m['person_id']for p in other['paragraphs']if p['id'].endswith(':p010')for m in p['mentions']if m['id'].endswith(':m0001'));self.assertEqual(self.pid,other_pid);n=self.people[self.pid];self.assertEqual(n['label'],'王玄');self.assertTrue(any(e['mention_id']==MID for e in n['evidence']));self.assertTrue(any(a['surface']=='王玄'and MID in a['mention_ids']for a in n['aliases']))
 def test_comparison_is_neither_title_nor_eight_princes(self):
  cheng=next(m['person_id']for m in self.p['mentions']if m['surface']=='王澄');n=self.people[cheng];self.assertEqual(n['label'],'王澄');self.assertIn('八名王氏人物',n['identity_note']);self.assertIn('不是王爵',n['identity_note']);self.assertTrue(any(a['surface']=='王澄'and PAR+':m0041'in a['mention_ids']for a in n['aliases']));self.assertFalse(any(h.get('person_id')in(self.pid,cheng)and h.get('title')=='王'for r in self.rows for h in r.get('holdings',[])))
 def test_same_person_decisions_are_qualified_not_aliases(self):
  self.assertFalse(any(c['id']=='ic-jin035-wangxuan-endingyun'for c in self.ch['annotation']['unresolved_identity_cases']));ds=[d for r in self.rows if r.get('record_type')=='person_identity_decision_set'for d in r['decisions']];d=next(x for x in ds if x['id']=='d-jin035-wangxuan-crossidentity');self.assertEqual(d['person_id'],self.pid);self.assertFalse(d['human_reviewed']);self.assertEqual(d['status'],'contextual_provisional');self.assertFalse(self.people[self.pid].get('id_aliases'))
 def test_cheng_preferred_same_person_and_daoshen_remains_distinct(self):
  ch=next(c for c in self.rows if c.get('id')=='c-jinshu-043-wangcheng');pid=next(m['person_id']for p in ch['paragraphs']if p['id'].endswith(':p001')for m in p['mentions']if m['id'].endswith(':m0000'));self.assertEqual(next(m['person_id']for m in self.p['mentions']if m['id']==PAR+':m0041'),pid);self.assertFalse(any(c['id']=='ic-jin035-cheng'for c in self.ch['annotation']['unresolved_identity_cases']));c42=next(c for c in self.rows if c.get('id')=='c-jinshu-042-taiyuan-wang');daoshen=next(m['person_id']for p in c42['paragraphs']if p['id'].endswith(':line042')for m in p['mentions']if m['id'].endswith(':m0062'));self.assertNotEqual(pid,daoshen);self.assertIn('道深',self.people[pid]['identity_note']);self.assertNotIn('8sa_o0b_y2i',self.people)
  from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
  retired=retired_person_ids(R);self.assertIn('8sa_o0b_y2i',retired);self.assertTrue(allocation_conflicts('8sa_o0b_y2i_A',retired))
 def test_fixed_witness_unchanged(self):
  self.assertEqual(hashlib.sha256((R/self.ch['source']['raw_file']).read_bytes()).hexdigest(),self.ch['source']['wikitext_sha256']);self.assertEqual(self.ch['source']['revision_id'],2506399)
 def test_original_mid_and_unrelated_names_preserved(self):
  self.assertEqual(len(self.p['mentions']),16);self.assertEqual(self.m['id'],MID);ch=next(c for c in self.rows if c.get('id')=='c-jinshu-043-wangyan');yan=next(m['person_id']for p in ch['paragraphs']if p['id'].endswith(':p001')for m in p['mentions']if m['surface']=='衍');self.assertEqual(next(m for m in self.p['mentions']if m['surface']=='王衍')['person_id'],yan)
 def test_xml_person_excludes_suffix(self):
  from scripts.render_corpus import render
  xml=render(self.ch);self.assertIn('ref="'+self.pid+'">王玄</persName>雲。',xml);self.assertNotIn('>王玄雲</persName>',xml)
 def test_native_cli_wrong_extra_name_character_rejected_in_memory(self):
  from scripts import validate_corpus
  path=R/'corpus/jinshu/035-pei-family.json';before=path.read_bytes();d=json.loads(before);p=next(p for p in d['paragraphs']if p['id']==PAR);m=next(m for m in p['mentions']if m['id']==MID);m.update(end=64,surface='王玄雲');original=Path.read_text
  def read(q,*a,**kw):return json.dumps(d,ensure_ascii=False)if q==path else original(q,*a,**kw)
  with patch.object(Path,'read_text',read),patch.object(validate_corpus,'ROOT',R):
   ov=validate_corpus.validate
   with patch.object(validate_corpus,'validate',lambda:ov(R)):self.assertEqual(validate_corpus.main(),1)
  self.assertEqual(path.read_bytes(),before)
if __name__=='__main__':unittest.main()
