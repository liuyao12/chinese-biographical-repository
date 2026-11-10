import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
try:
 from scripts.wyd_song063_basics import build,PATH,BASE,witness_valid,date_valid,validate_surname
 from scripts.validate_corpus import normalized_date_errors
 from scripts.preferred_name_components import reading_errors
except ImportError:
 from wyd_song063_basics import build,PATH,BASE,witness_valid,date_valid,validate_surname
 from validate_corpus import normalized_date_errors
 from preferred_name_components import reading_errors
ROOT=Path(__file__).resolve().parents[1]
class SourceBasics(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/PATH).read_bytes());self.data=build(self.ch,ROOT)
 def test_true_source_and_numbered_death(self):
  witness_valid(self.ch,ROOT);event=self.data['life_events'][0]
  self.assertEqual(normalized_date_errors(event['normalized_date'],{self.ch['id']:self.ch},ROOT,event,'life_event'),[])
  self.assertEqual(event['normalized_date']['year'],430);self.assertEqual(event['date_expression'],'七年')
  self.assertTrue(all('birth_year'not in n for n in self.data['name_components']))
 def test_no_absolute_sibling_ordinal_or_cousin_degree(self):
  a=self.data['assertions'];self.assertEqual(a[0]['qualifiers']['relative_birth_order']['younger_ordinal'],None)
  self.assertEqual(a[1]['qualifiers']['kinship_structure']['distance'],None)
  self.assertEqual(a[3]['qualifiers']['birth_order']['ordinal'],None)
  self.assertEqual(self.data['addresses'][0]['relation'],'biographical_origin')
 def test_stage_binding_cannot_be_removed_with_current_typed_sidecars(self):
  c=copy.deepcopy(self.ch);del c['annotation']['fixed_wyd063_basic_facts']
  with self.assertRaises(ValueError):witness_valid(c,ROOT)
 def test_wrong_date_person_year_or_missing_binding_record_rejects(self):
  e=self.data['life_events'][0]
  for record in [None,[],[1],'bad',3,{}]:
   self.assertTrue(normalized_date_errors(e['normalized_date'],{self.ch['id']:self.ch},ROOT,record,'life_event'))
  for k,v in [('year',425),('year',429),('source_expression','元嘉七年')]:
   d=copy.deepcopy(e['normalized_date']);d[k]=v;self.assertFalse(date_valid(d,e,{self.ch['id']:self.ch},ROOT))
  other=copy.deepcopy(e);other['person_id']=self.data['assertions'][0]['object_person_id'];self.assertFalse(date_valid(e['normalized_date'],other,{self.ch['id']:self.ch},ROOT))
 def test_wrong_kinship_or_birthplace_payload_rejected_by_full_source_gate(self):
  raw=Path.read_bytes
  for suffix,key,index,field,value in [('assertions','assertions',0,'predicate','father'),('addresses','assertions',0,'relation','birth_place')]:
   path=ROOT/(BASE+suffix+'.json');d=json.loads(raw(path));d[key][index][field]=value
   def reader(p):return json.dumps(d,ensure_ascii=False).encode()if p.resolve()==path.resolve()else raw(p)
   with patch.object(Path,'read_bytes',reader):
    with self.assertRaises(ValueError):witness_valid(self.ch,ROOT)
 def test_context_surnames_require_real_assertion_and_literal_is_unchanged(self):
  names=self.data['name_components'];facts=self.data['assertions'];cs={self.ch['id']:self.ch}
  for n in names:
   if n.get('surname_basis'):
    validate_surname(n,names,cs,facts,ROOT)
    with self.assertRaises(ValueError):validate_surname(n,names,cs,[],ROOT)
   elif n['id']!='n-song063-wyd-tanshou-literal':self.assertIsNone(n['surname'])

class VariantReading(unittest.TestCase):
 def setUp(self):
  self.chapters={}
  for rel in ['corpus/songshu/063-wyd1739-wangtanshou.json','corpus/nanqishu/033-wangsengqian.json']:
   c=json.loads((ROOT/rel).read_bytes());self.chapters[c['id']]=c
  self.names=json.loads((ROOT/'data/corpus/profile-names.json').read_bytes())['records']+json.loads((ROOT/(BASE+'name-components.json')).read_bytes())['records']
  self.r=json.loads((ROOT/(BASE+'preferred-name-readings.json')).read_bytes())['readings'][0]
 def test_actual_legacy_idless_and_all_records(self):
  self.assertEqual(reading_errors(self.r,self.names,self.chapters),[])
  self.assertTrue(any(ref['record']['id']is None for ref in self.r['records']))
  self.assertEqual(len(self.r['records']),3)
 def test_wrong_person_missing_locator_value_or_judgment_rejected(self):
  for change in ['person','missing','value','judgment','duplicate']:
   r=copy.deepcopy(self.r)
   if change=='person':r['person_id']='different_person'
   elif change=='missing':r['records'].pop()
   elif change=='value':r['preferred_value']='僧乾'
   elif change=='judgment':r['basis']['rationale']=''
   else:r['records'].append(copy.deepcopy(r['records'][0]))
   self.assertTrue(reading_errors(r,self.names,self.chapters))
  self.assertTrue(reading_errors(self.r,self.names+[copy.deepcopy(self.names[-1])],self.chapters))
  self.assertTrue(reading_errors(self.r,self.names,{k:v for k,v in self.chapters.items()if k==next(iter(self.chapters))}))
 def test_full_canonical_rekey_and_third_spelling_scope(self):
  old=self.r['person_id'];new='a1b_c2d_e3f'
  def rew(x):
   if isinstance(x,dict):return{k:rew(v)for k,v in x.items()}
   if isinstance(x,list):return[rew(v)for v in x]
   return new if x==old else x
  self.assertEqual(reading_errors(rew(self.r),rew(self.names),rew(self.chapters)),[])
  third=dict(self.names[-1],id='unlisted-third',person_id=old,ming='僧乾')
  self.assertEqual(reading_errors(self.r,self.names+[third],self.chapters),[])
 def test_old_same_paragraph_contract_stays_strict(self):
  pid='old_person';ms=[{'id':'m1','kind':'person','person_id':pid,'start':0,'end':1,'surface':'甲'},{'id':'m2','kind':'person','person_id':pid,'start':1,'end':2,'surface':'乙'}]
  c={'id':'chapter','source_id':'source','paragraphs':[{'id':'paragraph','text':'甲乙','mentions':ms}]};names=[{'id':'n'+str(i),'person_id':pid,'chapter_id':c['id'],'paragraph_id':'paragraph','surname':None,'ming':x,'quote':'甲乙'}for i,x in enumerate(['甲','乙'])]
  r={'id':'old_reading','person_id':pid,'field':'ming','preferred_value':'甲','source_values':['甲','乙'],'records':[{'record':n,'anchor':ms[i],'source_id':'source'}for i,n in enumerate(names)],'status':'editorial_provisional','human_reviewed':False,'rationale':'同段異字暫選','coverage':'listed_records_only','basis':{'kind':'same_paragraph_mixed_name_spellings','source_id':'source','chapter_id':'chapter','paragraph_id':'paragraph','quote':'甲乙','anchors':ms}}
  self.assertEqual(reading_errors(r,names,{'chapter':c}),[])
  r['source_values']=['僧䖍','僧虔'];self.assertTrue(reading_errors(r,names,{'chapter':c}))
class TitlePreference(unittest.TestCase):
 def setUp(self):
  try:from scripts.person_bundle import load_catalog
  except ImportError:from person_bundle import load_catalog
  self.people,self.records=load_catalog(ROOT)
 def test_actual_attestation_and_transaction_cache(self):
  try:from scripts.profile_title_preferences import choice
  except ImportError:from profile_title_preferences import choice
  title=next(r for r in self.records if r.get('record_type')=='profile_title_preference_set')['decisions'][0]
  selected=choice(self.records,self.people,title['person_id'],ROOT)
  self.assertEqual(selected['title'],'太保');self.assertEqual(selected['mode'],'attestation')
  with patch('scripts.profile_title_preferences.resolve' if 'scripts.profile_title_preferences'in __import__('sys').modules else 'profile_title_preferences.resolve',side_effect=AssertionError('rescan')):
   self.assertEqual(choice(self.records,self.people,title['person_id'],ROOT)['title'],'太保')
  with self.assertRaises(ValueError):choice(self.records,self.people,title['person_id'],ROOT/'other-root')
 def test_copied_catalog_is_revalidated_and_bad_choices_rejected(self):
  try:from scripts.profile_title_preferences import choice
  except ImportError:from profile_title_preferences import choice
  self.assertIs(type(copy.deepcopy(self.records)),list)
  for change in ['person','proposal','title','time','duplicate']:
   records=copy.deepcopy(self.records);pref=next(r for r in records if r.get('record_type')=='profile_title_preference_set');d=pref['decisions'][0];original=d['person_id']
   if change=='person':d['person_id']=next(p for p in self.people if p!=original)
   elif change=='proposal':d['holding_id']='not-assumed-proposal'
   elif change=='title':next(h for r in records if r.get('record_type')=='title_holding_assertion_set' for h in r['holdings'] if h['id']==d['holding_id'])['title']='太傅'
   elif change=='time':d['temporal_claim']='430'
   else:pref['decisions'].append(dict(d,id=d['id']+'-duplicate'))
   with self.assertRaises(ValueError):choice(records,self.people,original,ROOT)
 def test_selected_raw_dependency_change_rejected_without_reusing_old_index(self):
  try:from scripts.profile_title_preferences import choice
  except ImportError:from profile_title_preferences import choice
  d=next(r for r in self.records if r.get('record_type')=='profile_title_preference_set')['decisions'][0];raw=Path.read_bytes
  ch=next(r for r in self.records if r.get('id')=='c-songshu-063-wyd1739-wangtanshou');target=ROOT/ch['source']['raw_file']
  def reader(p):return raw(p)+b'bad'if p.resolve()==target.resolve()else raw(p)
  with patch.object(Path,'read_bytes',reader):
   with self.assertRaises(ValueError):choice(self.records,self.people,d['person_id'],ROOT)

if __name__=='__main__':unittest.main()
