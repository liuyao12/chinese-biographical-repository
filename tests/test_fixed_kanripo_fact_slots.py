# coding: utf-8
import unittest,json,copy,sys,tempfile,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from scripts import fixed_kanripo_fact_slots as f
from scripts.validate_corpus import source_age_number,direct_source_age_valid
class FixedKanripoFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/sanguozhi/025-xinpi.json').read_text());cls.v=f.records(cls.c,R);cls.by={v['fixed_source_fact_binding']['slot']:v for v in cls.v}
 def mutate(self,key,fn):
  v=copy.deepcopy(self.by[key]);fn(v);self.assertFalse(f.valid(v,self.c,R))
 def test_all_69_records(self):self.assertEqual(len(self.v),69);self.assertTrue(all(f.valid(v,self.c,R)for v in self.v))
 def test_finite_roles_do_not_use_person_id_allowlist(self):
  c=copy.deepcopy(self.c);ids={m['person_id']for p in c['paragraphs']for m in p['mentions']if m.get('person_id')};mapping={p:'synthetic-person-'+str(i)for i,p in enumerate(sorted(ids))}
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id'):m['person_id']=mapping[m['person_id']]
  got=f.records(c,R);self.assertTrue(all(f.valid(v,c,R)for v in got));self.assertNotEqual(got[0]['subject_person_id'],self.v[0]['subject_person_id'])
 def test_wrong_career_recipient_consistently(self):
  other=self.c['paragraphs'][4]['mentions'][0]
  def change(v):
   v['person_id']=other['person_id'];v['attestations'][0]['person_mention_id']=other['id'];v['evidence'][0]['person_mention_id']=other['id'];v['effective_period']['start']['evidence'][0]['person_mention_id']=other['id']
  self.mutate('holding_018',change)
 def test_prince_accession_not_chensi_wang(self):
  a=self.by['holding_032'];self.assertEqual(a['person_id'],[m for m in self.c['paragraphs'][7]['mentions']if m['kind']=='person'][9]['person_id']);self.mutate('holding_032',lambda v:v.update(person_id=[m for m in self.c['paragraphs'][7]['mentions']if m['kind']=='person'][8]['person_id']))
 def test_shared_office_prefix_not_edict_word(self):
  v=self.by['holding_012'];self.assertEqual(v['attestations'][0]['start'],1053);self.assertEqual(v['source_title_resolution']['resolved_title'],'中書令');self.mutate('holding_012',lambda v:v['attestations'][0].update(start=443,end=444))
 def test_sister_subject_is_named_female_not_narrative_brother(self):
  p=self.c['paragraphs'][7];t=p['text'];female_start=t.index('毗女憲英')+2;male_start=t.index('弟敞')+1
  female=next(m for m in p['mentions']if m['start']==female_start and m['surface']=='憲英');male=next(m for m in p['mentions']if m['start']==male_start and m['surface']=='敞')
  v=self.by['kin_004'];self.assertEqual(v['predicate'],'sister');self.assertEqual(v['subject_person_id'],female['person_id']);self.assertEqual(v['object_person_id'],male['person_id']);self.assertEqual(v['qualifiers']['relative_age'],'older')
  order=v['qualifiers']['relative_birth_order'];self.assertEqual(order['older_person_id'],female['person_id']);self.assertEqual(order['younger_person_id'],male['person_id']);self.assertIsNone(order['older_ordinal']);self.assertIsNone(order['younger_ordinal'])
  e,=v['evidence'];self.assertEqual(e['subject_person_mention_id'],female['id']);self.assertEqual(e['object_person_mention_id'],male['id'])
 def test_consistent_old_wrong_sister_direction_rejected(self):
  v=copy.deepcopy(self.by['kin_004']);v['subject_person_id'],v['object_person_id']=v['object_person_id'],v['subject_person_id'];v['qualifiers']['relative_age']='younger'
  for e in v['evidence']:e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
  self.assertFalse(f.valid(v,self.c,R))
 def test_kinship_reverse_endpoints(self):self.mutate('kin_002',lambda v:v.update(subject_person_id=v['object_person_id'],object_person_id=v['subject_person_id']))
 def test_brother_not_fake_father(self):self.mutate('kin_001',lambda v:v.update(predicate='father'))
 def test_relative_order_not_absolute(self):self.mutate('kin_001',lambda v:v['qualifiers']['relative_birth_order'].update(younger_ordinal=2))
 def test_mother_not_birth_certificate(self):self.assertEqual(self.by['kin_006']['predicate'],'maternal_role');self.mutate('kin_006',lambda v:v.update(predicate='mother'))
 def test_mother_not_sheep_father(self):self.mutate('kin_006',lambda v:v['qualifiers'].update(father_person_id='invented-parent'))
 def test_nephew_not_birth_mother_or_known_path(self):
  for key in ('kin_008','kin_009'):
   self.assertEqual(self.by[key]['qualifiers']['generation_difference'],-1);self.assertIsNone(self.by[key]['qualifiers']['connecting_person_ids']);self.mutate(key,lambda v:v.update(predicate='mother'))
 def test_grandmother_not_father(self):self.assertEqual(self.by['kin_007']['qualifiers']['lineage'],'maternal');self.mutate('kin_007',lambda v:v['qualifiers'].update(mother_person_id='invented-mother'))
 def test_no_age_to_birth_inference(self):self.assertIsNone(self.by['age_001']['birth_year']);self.mutate('age_001',lambda v:v.update(birth_year=191))
 def test_date_not_borrowed_to_xinpi_death(self):self.assertNotIn('normalized_date',self.by['life_002']);self.mutate('life_002',lambda v:v.update(normalized_date=self.by['life_003']['normalized_date']))
 def test_age_79_269_exact_quote(self):
  a=self.by['age_001'];self.assertEqual((a['value'],a['source_number'],a['normalized_date']['year']),(79,'七十有九',269));self.mutate('age_001',lambda v:v.update(value=78))
 def test_date_roles_not_exchange(self):self.mutate('life_003',lambda v:v.update(person_id=self.by['life_002']['person_id']))
 def test_career_end_stays_unknown(self):self.assertTrue(all(v['effective_period']['end']['status']=='unknown'for k,v in self.by.items()if k.startswith('holding_')))
 def test_career_regnal_year_not_tenure(self):self.assertEqual(self.by['holding_018']['effective_period']['start']['normalized_date']['year'],234)
 def test_missing_or_duplicate_slot_rejected(self):
  c=copy.deepcopy(self.c);c['annotation'].pop('age_assertions');c['annotation'].pop('title_proposals');rows=[c,dict(record_type='person_name_component_set',chapter_id=c['id'],records=self.v)]
  self.assertFalse(f.errors(R,rows));rows[1]['records']=self.v[:-1];self.assertTrue(f.errors(R,rows));rows[1]['records']=self.v+[self.v[0]];self.assertTrue(f.errors(R,rows))
 def test_bool_and_float_not_counts(self):
  for val in (True,300.0):self.mutate('detail_002',lambda v:v['values'].update(value=val))
 def test_courtesy_not_other_person(self):self.mutate('name_003',lambda v:v.update(zi='佐治'))
 def test_source_glyph_and_whole_unit_preserved(self):
  c=copy.deepcopy(self.c);c['paragraphs'][0]['text']=c['paragraphs'][0]['text'].replace('毗','丕',1)
  with self.assertRaises(AssertionError):f.records(c,R)
 def test_wrong_revision_rejected(self):
  c=copy.deepcopy(self.c);c['source']['revision_id']='0'*40
  with self.assertRaises(AssertionError):f.records(c,R)
 def test_source_raw_path_cannot_escape(self):
  for path in ('/tmp/elsewhere.txt','source-evidence/../outside.txt'):
   c=copy.deepcopy(self.c);c['source']['raw_path']=path
   with self.assertRaises(AssertionError):f.records(c,R)
 def test_consistent_raw_offset_hash_co_shift_still_rejected(self):
  from scripts.fixed_kanripo_projection import errors as projection_errors
  c=copy.deepcopy(self.c);ref=c['annotation']['fixed_kanripo_projection_ref'];d=json.loads((R/ref).read_text());raw=(R/c['source']['raw_path']).read_bytes();newraw=b' '+raw;sha=hashlib.sha256(newraw).hexdigest();d['raw_file_sha256']=sha;c['source']['raw_file_sha256']=sha;c['source']['response_sha256']=sha
  d['unit']['start']+=1;d['unit']['end']+=1
  for p in d['paragraphs']:p['raw_positions']=[x+1 for x in p['raw_positions']]
  with tempfile.TemporaryDirectory()as temp:
   root=Path(temp)
   for path,content in [(c['source']['raw_path'],newraw),(ref,(json.dumps(d,ensure_ascii=False)+'\n').encode())]:
    q=root/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(content)
   self.assertFalse(projection_errors(c,root))
   with self.assertRaises(AssertionError):f.records(c,root)
 def test_age_conjunction_numerals_general(self):
  for text,n in [('七十有九',79),('十有一',11),('二十有一',21),('七十九',79),('廿有一',21)]:self.assertEqual(source_age_number(text),n)
  for text in ('七十有','七十有有九','七十有零','七十幾九','七十有十九'):self.assertIsNone(source_age_number(text))
  self.assertTrue(direct_source_age_valid(dict(source_number='七十有九',source_term='年至七十有九',value=79)))
  self.assertFalse(direct_source_age_valid(dict(source_number='七十有九',source_term='年至七十有九',value=79.0)))
 def test_contested_dialogue_machine_qualified(self):
  for key in ('holding_016','life_004','life_005','life_006'):
   q=self.by[key]['source_report_qualification'];self.assertFalse(q['preferred_as_independent_historical_event']);self.mutate(key,lambda v:v.pop('source_report_qualification'))
if __name__=='__main__':unittest.main()
