# coding: utf-8
from pathlib import Path
import json,copy,unittest
from scripts import biographical_death_year_chain as H
from scripts.validate_corpus import source_age_number
R=Path(__file__).resolve().parents[1]
chapter=json.loads((R/'corpus/songshu/046-wangyi.json').read_text());chapters={chapter['id']:chapter}
event=json.loads((R/'corpus/songshu/046-wangyi-life-events.json').read_text())['events'][0]
class Binding(unittest.TestCase):
 def check(self,e=None,chs=None):return H.valid((e or event)['normalized_date'],e or event,chs or chapters,source_age_number)
 def test_positive(self):self.assertTrue(self.check())
 def test_wrong_year(self):
  e=copy.deepcopy(event);e['normalized_date']['year']=439;self.assertFalse(self.check(e))
 def test_child_cannot_inherit_father_death_year(self):
  e=copy.deepcopy(event);e['person_id']='qsd_v11_ya1_AAA';e['normalized_date']['event_evidence_binding']['person_id']=e['person_id'];self.assertFalse(self.check(e))
 def test_subject_switch(self):
  ch=copy.deepcopy(chapter);p=next(p for p in ch['paragraphs']if p['id'].endswith(':p009'));next(m for m in p['mentions']if m['surface']=='仲德')['person_id']='qsd_v11_ya1_AAA';self.assertFalse(self.check(chs={ch['id']:ch}))
 def test_extra_named_subject_within_death_scope(self):
  ch=copy.deepcopy(chapter);p=next(p for p in ch['paragraphs']if p['id'].endswith(':p009'));p['mentions'].append({'id':p['id']+':synthetic-subject','kind':'person','person_id':'synthetic-other','start':30,'end':31,'surface':p['text'][30:31]});self.assertFalse(self.check(chs={ch['id']:ch}))
 def test_mingnian_cannot_replace_fifteenth(self):
  e=copy.deepcopy(event);e['date_expression']='明年';e['normalized_date']['source_expression']='明年';self.assertFalse(self.check(e))
 def test_wrong_relative_year_arithmetic(self):
  e=copy.deepcopy(event);e['normalized_date']['event_evidence_binding']['year_chain'][2]['regnal_year']=11;self.assertFalse(self.check(e))
 def test_other_reign_insertion(self):
  ch=copy.deepcopy(chapter);p=next(p for p in ch['paragraphs']if p['id'].endswith(':p009'));p['text']=p['text'].replace('十三年','大明十三年');self.assertFalse(self.check(chs={ch['id']:ch}))
 def test_crop_full_paragraph(self):
  e=copy.deepcopy(event);e['normalized_date']['event_evidence_binding']['full_paragraphs'][0]['quote']='元嘉三年';self.assertFalse(self.check(e))
 def test_moved_offset(self):
  e=copy.deepcopy(event);e['normalized_date']['event_evidence_binding']['year_chain'][-1]['anchor']['start']+=1;self.assertFalse(self.check(e))
 def test_drop_chain_stage(self):
  e=copy.deepcopy(event);e['normalized_date']['event_evidence_binding']['year_chain'].pop(2);self.assertFalse(self.check(e))
 def test_wrong_epoch_same_era_name(self):
  e=copy.deepcopy(event);e['normalized_date']['regnal_year_mapping']['start_ce_year']=151;self.assertFalse(self.check(e))
 def test_duplicate_paragraph_id(self):
  ch=copy.deepcopy(chapter);ch['paragraphs'].append(copy.deepcopy(ch['paragraphs'][0]));self.assertFalse(self.check(chs={ch['id']:ch}))
