# coding: utf-8
"""Fixed-witness Jin039 dates: native-only fixtures, no external packages or network."""
from pathlib import Path
import copy,json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.validate_corpus import normalized_date_errors
from scripts.era_stage_dates import staged_scope_valid,binding_valid
from scripts.civil_era_ranges import civil_era_range_errors
fix=json.loads((Path(__file__).parent/'fixtures/jin039-era-stage38.json').read_text(encoding='utf-8'))
ch=fix['chapter'];chs={ch['id']:ch};r,rr=fix['holdings']
d=r['effective_period']['start']['normalized_date'];dr=rr['effective_period']['start']['normalized_date_range']
class Jin039EraStageNativeTests(unittest.TestCase):
 def test_real282(self):self.assertEqual(normalized_date_errors(d,chs),[]);self.assertTrue(binding_valid(d,r,'start'))
 def test_no_ruler(self):self.assertFalse(any('ruler'in k for k in d['narrative_era_scope']))
 def test_real_initial_range(self):self.assertEqual(civil_era_range_errors(dr,rr['evidence'],'元康初'),[]);self.assertNotIn('year',dr)
 def bad(self,path,value):
  z=copy.deepcopy(d);o=z
  for k in path[:-1]:o=o[k]
  o[path[-1]]=value;self.assertFalse(staged_scope_valid(z,chs))
 def test_wrong_revision(self):self.bad(['narrative_era_scope','revision_id'],123)
 def test_wrong_witness(self):self.bad(['narrative_era_scope','witness_sha256'],'0'*64)
 def test_subject_switch(self):
  z=copy.deepcopy(chs);pp=z[ch['id']]['paragraphs'][0];pp['mentions'].append({'kind':'person','person_id':'other','start':70,'end':71});self.assertFalse(staged_scope_valid(d,z))
 def text_bad(self,old,new):
  self.assertEqual(len(old),len(new));z=copy.deepcopy(chs);dd=copy.deepcopy(d);pp=z[ch['id']]['paragraphs'][0];pp['text']=pp['text'].replace(old,new);dd['narrative_era_scope']['full_paragraph']=pp['text'];dd['evidence'][-1]['quote']=pp['text'];self.assertFalse(staged_scope_valid(dd,z))
 def test_intervening_speech(self):self.text_bad('與諸王侯','曰諸王侯')
 def test_intervening_era(self):self.text_bad('與諸王','元康初')
 def test_intervening_number_year(self):self.text_bad('與諸王','二年王')
 def test_event_anchor_other_paragraph(self):self.bad(['narrative_era_scope','event_date_anchor','paragraph_id'],'other')
 def test_title_bound_to_other_record(self):
  z=copy.deepcopy(r);z['title']='其他';self.assertFalse(binding_valid(d,z,'start'))
 def test_wrong_full_quote(self):self.bad(['narrative_era_scope','full_paragraph'],'三年除')
 def test_wrong_subject(self):self.bad(['narrative_era_scope','unit_subject_person_id'],'other')
 def test_borrowed_ruler(self):self.bad(['narrative_era_scope','era_ruler_person_id'],'hgm_jvn_hle')
 def test_wrong_trigger(self):self.bad(['narrative_era_scope','event_binding','source_term_anchor','surface'],'為')
 def test_wrong_title_anchor(self):self.bad(['narrative_era_scope','event_binding','title_anchor','start'],0)
 def test_wrong_year(self):
  z=copy.deepcopy(d);z['year']=283;self.assertTrue(normalized_date_errors(z,chs))
 def test_wrong_record(self):
  z=copy.deepcopy(r);z['person_id']='other';self.assertFalse(binding_valid(d,z,'start'))
 def test_initial_not_first(self):
  z=copy.deepcopy(dr);z['year']=291;self.assertTrue(civil_era_range_errors(z,rr['evidence'],'元康初'))
 def test_initial_requires_qualifier(self):
  z=copy.deepcopy(dr);del z['source_stage'];self.assertTrue(civil_era_range_errors(z,rr['evidence'],'元康初'))
 def test_range_wrong_endpoint(self):
  z=copy.deepcopy(dr);z['latest']['year']=293;self.assertTrue(civil_era_range_errors(z,rr['evidence'],'元康初'))
 def test_old_middle_unchanged(self):
  z=copy.deepcopy(dr);z['source_expression']='元康中';z.pop('source_stage');ev=copy.deepcopy(rr['evidence']);ev[0]['quote']=ev[0]['quote'].replace('元康初','元康中');z['evidence']=ev;z['original_quote']=ev[0]['quote'];self.assertEqual(civil_era_range_errors(z,ev,'元康中'),[])

 def test_initial_qualifier_mismatch(self):
  z=copy.deepcopy(dr);z['source_stage']='末';self.assertTrue(civil_era_range_errors(z,rr['evidence'],'元康初'))
 def test_grant_cannot_bind_end(self):self.assertFalse(binding_valid(d,r,'end'))
 def test_attestation_not_grant(self):
  z=copy.deepcopy(r);z['mode']='attestation';self.assertFalse(binding_valid(d,z,'start'))
if __name__=='__main__':unittest.main()
