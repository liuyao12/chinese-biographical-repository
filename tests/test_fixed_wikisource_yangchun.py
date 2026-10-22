# coding: utf-8
import unittest,json,copy,tempfile,hashlib
from pathlib import Path
from scripts.fixed_wikisource_units import source_errors,ordinal_uncle_valid,kin_age_designation_valid
R=Path(__file__).resolve().parents[1];CH='corpus/weishu-weishou/058-yangchun'
class FixedWikisourceYangchun(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/(CH+'.json')).read_text());cls.a=json.loads((R/(CH+'-assertions.json')).read_text())['assertions'];cls.ps={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']}
 def test_full_actual_raw_and_common_witness(self):self.assertEqual(source_errors(self.c,R),[])
 def test_independent_physical_fixture_and_unretained_raw_tamper(self):
  binding=json.loads((R/self.c['annotation']['fixed_wikisource_unit_ref']).read_text())
  with tempfile.TemporaryDirectory(prefix='yangchun-')as tmp:
   r=Path(tmp).resolve();names=[self.c['annotation']['fixed_wikisource_unit_ref'],binding['raw_file'],'corpus/weishu-weishou/058-yangbo-yangkan.json']
   for name in names:
    dst=r/name;dst.parent.mkdir(parents=True,exist_ok=True);self.assertTrue(dst.resolve().is_relative_to(r));dst.write_bytes((R/name).read_bytes());self.assertFalse(dst.is_symlink())
   self.assertEqual(source_errors(self.c,r),[]);p=r/binding['raw_file'];p.write_bytes(b' '+p.read_bytes());self.assertTrue(source_errors(self.c,r))
 def test_cosshift_projection_rejected(self):
  c=copy.deepcopy(self.c);p=c['paragraphs'][0]['source_position'];p['raw_start']+=1;p['raw_end']+=1;p['raw_character_offsets']=[v+1 for v in p['raw_character_offsets']];p['projection_sha256']=hashlib.sha256((json.dumps(p['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest();self.assertTrue(source_errors(c,R))
 def test_modern_ref_cannot_be_dropped_or_called_body(self):
  for key in ('modern_collation_reports','shared_appraisal_context'):
   c=copy.deepcopy(self.c)
   if key=='modern_collation_reports':c['annotation'][key].pop()
   else:c['annotation'][key]['independent_witness']=True
   self.assertTrue(source_errors(c,R))
 def test_received_layer_and_all_paragraphs_required(self):
  for mode in ('omit','layer','note'):
   c=copy.deepcopy(self.c)
   if mode=='omit':c['paragraphs'].pop(10)
   elif mode=='layer':c['paragraphs'][0]['text_layer']='commentary'
   else:c['paragraphs'][0]['attached_note_to_paragraph_id']='fake'
   self.assertTrue(source_errors(c,R))
 def test_uncle_designation_not_father_order(self):
  a=next(a for a in self.a if 'source_uncle_ordinal'in a['qualifiers']);self.assertTrue(ordinal_uncle_valid(a,self.ps));self.assertNotIn('birth_order',a['qualifiers'])
  for mode in ('reverse','number','term'):
   b=copy.deepcopy(a)
   if mode=='reverse':b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id']
   elif mode=='number':b['qualifiers']['source_uncle_ordinal']['value']=5
   else:b['qualifiers']['source_uncle_ordinal']['source_term']='第六子'
   self.assertFalse(ordinal_uncle_valid(b,self.ps))
 def test_quoted_80_is_null_approximation_not_75_or_77(self):
  a=next(a for a in self.c['annotation']['age_assertions']if 'kin_age_designation'in a);self.assertTrue(kin_age_designation_valid(a,self.c,R));self.assertIsNone(a['value']);self.assertEqual(a['approximation']['target_age'],80);self.assertIsNone(a['birth_year']);self.assertNotIn('bounds',a)
  ordinary=[a for a in self.c['annotation']['age_assertions']if 'kin_age_designation'not in a];self.assertEqual(sorted(a['value']for a in ordinary),[9,65,75,77]);self.assertTrue(all(a['birth_year']is None for a in ordinary))
 def test_quoted_age_wrong_person_parent_number_exactness_rejected(self):
  a=next(a for a in self.c['annotation']['age_assertions']if 'kin_age_designation'in a)
  for mode in ('exact','birth','number','speaker','father','bounds','speech'):
   b=copy.deepcopy(a)
   if mode=='exact':b['value']=80
   elif mode=='birth':b['birth_year']=450
   elif mode=='number':b['approximation']['target_age']=77
   elif mode=='speaker':b['kin_age_designation']['speaker_person_id']=b['person_id']
   elif mode=='father':b['kin_age_designation']['father_assertion_id']='absent'
   elif mode=='bounds':b['bounds']={'lower':80}
   else:b['kin_age_designation']['speech_start_anchor']['start']+=1
   self.assertFalse(kin_age_designation_valid(b,self.c,R),mode)
 def test_quote_roles_and_original_anomalous_words(self):
  p=self.c['paragraphs'];self.assertIn('自爾至今二十年',p[12]['text']);self.assertIn('弟息五人',p[22]['text']);self.assertTrue(any(m.get('person_id')is None and m['surface']=='高祖'for m in p[14]['mentions']));a=next(a for a in self.a if 'source_uncle_ordinal'in a['qualifiers']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_commuted_death_and_no_office_end_inference(self):
  es=json.loads((R/(CH+'-life-events.json')).read_text())['events'];hs=json.loads((R/(CH+'-titles.json')).read_text())['holdings'];self.assertEqual(len(es),13);self.assertEqual(sum('normalized_date'in e for e in es),1);self.assertEqual(next(e['normalized_date']['year']for e in es if 'normalized_date'in e),531);self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in hs))
