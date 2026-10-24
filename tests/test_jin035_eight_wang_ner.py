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
 def test_source_local_person_has_reverse_evidence(self):
  self.assertEqual(self.m['kind'],'person');self.assertNotEqual(self.pid,'35b_mo3_adg');n=self.people[self.pid];self.assertEqual(n['label'],'王玄');self.assertEqual(n['aliases'],[{'surface':'王玄','mention_ids':[MID]}]);self.assertEqual(n['evidence'][0]['mention_id'],MID);self.assertIn('是否同人尚未定',n['identity_note'])
 def test_comparison_is_neither_title_nor_eight_princes(self):
  n=self.people['8sa_o0b_y2i'];self.assertEqual(n['label'],'王澄');self.assertIn('八名王氏人物',n['identity_note']);self.assertIn('不是王爵',n['identity_note']);self.assertEqual(n['aliases'],[{'surface':'王澄','mention_ids':[PAR+':m0041']}])
  self.assertFalse(any(h.get('person_id')in(self.pid,'8sa_o0b_y2i')for r in self.rows for h in r.get('holdings',[])))
 def test_no_parent_or_cross_chapter_alias(self):
  self.assertFalse(any(self.pid in(a.get('subject_person_id'),a.get('object_person_id'))for r in self.rows for a in r.get('assertions',[])));case=next(c for c in self.ch['annotation']['unresolved_identity_cases']if c['id']=='ic-jin035-wangxuan-endingyun');self.assertEqual(case['status'],'unresolved');self.assertEqual(case['candidate_person_ids'],[self.pid,'35b_mo3_adg']);self.assertNotIn(self.pid,json.dumps(self.people['35b_mo3_adg']['aliases']))
 def test_cheng_three_roles_remain_unresolved(self):
  c=next(c for c in self.ch['annotation']['unresolved_identity_cases']if c['id']=='ic-jin035-cheng');self.assertEqual(c['status'],'unresolved');self.assertEqual(c['candidate_person_ids'],['8sa_o0b_y2i','a8f_ec8_e74_ABC','rlk_lzd_86c']);self.assertEqual({q['role']for q in c['candidate_qualifications']},{'source_local_referent','contextual_candidate_not_identified','known_other_lineage_countercandidate'});self.assertIn('c-jinshu-043-wangyan:p006',c['paragraph_ids']);self.assertIn('c-jinshu-042-taiyuan-wang:line042',c['paragraph_ids'])
 def test_fixed_witness_unchanged(self):
  self.assertEqual(hashlib.sha256((R/self.ch['source']['raw_file']).read_bytes()).hexdigest(),self.ch['source']['wikitext_sha256']);self.assertEqual(self.ch['source']['revision_id'],2506399)
 def test_original_mid_and_unrelated_names_preserved(self):
  self.assertEqual(len(self.p['mentions']),16);self.assertEqual(self.m['id'],MID);self.assertEqual(next(m for m in self.p['mentions']if m['surface']=='王澄')['person_id'],'8sa_o0b_y2i');self.assertEqual(next(m for m in self.p['mentions']if m['surface']=='王衍')['person_id'],'b0c_13f_c3a')
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
