from pathlib import Path
import unittest,json,copy,tempfile,hashlib
from unittest.mock import patch
from scripts.fixed_witness_fact_slots import records,valid,recipes,grammar,expand
from scripts.fixed_witness_parallel_dates import normalized_valid,prove,value_at,file
ROOT=Path(__file__).resolve().parents[1]
class YanghuCareer(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/034-yanghu.json').read_text());cls.all=records(cls.ch,ROOT);cls.rs=[v for v in cls.all if v['fixed_source_fact_binding']['slot'].startswith('career_')];cls.by={v['fixed_source_fact_binding']['slot'].removeprefix('career_'):v for v in cls.rs};cls.recipe=recipes()['jin034-yanghu-family'];cls.chapters={cls.ch['id']:cls.ch}
 def reject(self,key,fn):
  v=copy.deepcopy(self.by[key]);fn(v);self.assertFalse(valid(v,self.ch,ROOT))
 def test_all150_source_slots_and_original37_still_complete(self):
  self.assertEqual((len(self.all),len(self.rs)),(150,113));self.assertEqual({v['fixed_source_fact_binding']['slot']for v in self.all if not v['fixed_source_fact_binding']['slot'].startswith('career_')},{'kin_'+str(i).zfill(3)for i in range(1,32)}|{'detail_'+str(i).zfill(3)for i in range(1,7)})
  for v in self.all:self.assertTrue(valid(v,self.ch,ROOT),v['id'])
 def test_all41_holding9_death6_places2_real_ages55_details(self):
  self.assertEqual({k:sum(s['category']==k for s in self.recipe['slots']if s['slot'].startswith('career_'))for k in ['holding','life','address','age','detail']},{'holding':41,'life':9,'address':6,'age':2,'detail':55})
 def test_every_new_date_has_exact_bound_proof(self):
  proofs=[p for p in self.recipe['date_proofs']if p.get('kind')=='fixed_archived_parallel_year'];self.assertEqual(len(proofs),19)
  for p in proofs:
   v=next(v for v in self.rs if v['fixed_source_fact_binding']['slot']==p['slot']);self.assertTrue(normalized_valid(value_at(v,p['record_path']),v,p['bound_role'],self.chapters,ROOT))
 def test_known_years_and_unknown_ends(self):
  for k,y in [('guanzhong',260),('jupingzi',264),('zhongjun',265),('sanqi',265),('jupinghou',265),('jingzhou',269),('jiajie',269),('zhengnan',276),('kaifu',276),('pian-juping',281)]:
   h=self.by[k];self.assertEqual(h['effective_period']['start']['normalized_date']['year'],y);self.assertEqual(h['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]})
  self.assertEqual(self.by['hu-death']['normalized_date']['year'],278)
 def test_right_and_left_pushe_not_merged_or_forced_same_appointment(self):
  h=self.by['youpu'];self.assertEqual(h['title'],'尚書右僕射');self.assertNotIn('normalized_date',h['effective_period']['start']);v=self.by['left-right-pushe']['values'];self.assertEqual(v['parallel_title'],'尚書左僕射');self.assertEqual(v['parallel_year'],268);self.assertEqual(v['event_identity_or_sequence'],'unresolved');self.reject('youpu',lambda x:x['effective_period']['start'].update(normalized_date=self.by['jingzhou']['effective_period']['start']['normalized_date']))
 def test_not_every_office_gets_neighboring_event_year(self):
  for k in ['zhongshu','mishu','xiangguo','youpu','weijiang','cheqi','pingnan','posthumous-shizhong','posthumous-taifu','posthumous-cheng','wife-wansui','faxing-juping']:self.assertNotIn('normalized_date',self.by[k]['effective_period']['start'])
 def test_summons_and_refused_noble_offers_not_holdings(self):
  titles={v['title']for v in self.rs if'title'in v and'kind'in v and'effective_period'in v};self.assertNotIn('郡公',titles);self.assertNotIn('南城侯',titles);self.assertNotIn('秀才',titles)
  self.assertEqual(self.by['unnamed-jungong-declined']['values']['offered_households'],3000);self.assertEqual(self.by['nancheng-declined']['values']['outcome'],'not_assumed');self.assertTrue(self.by['nancheng-official-use']['values']['actual_acceptance_not_inferred']);self.assertEqual(self.by['posthumous-restore-juping']['values']['restored_title'],'钜平侯')
 def test_cheqi_refusal_denied_does_not_make_nonassumption(self):
  self.assertEqual(self.by['cheqi']['mode'],'grant');self.assertEqual(self.by['cheqi-refusal-denied']['values']['decision'],'not_permitted');self.assertIs(self.by['cheqi-refusal-denied']['values']['actual_non_assumption'],False)
 def test_employer_titles_not_subordinate_titles(self):
  self.assertEqual(self.by['yi-yuan']['title'],'掾');self.assertEqual(self.by['yi-yuan']['employment_context']['employer_title'],'車騎');self.assertEqual(self.by['liang-canjun']['title'],'參軍');self.assertEqual(self.by['liang-canjun']['employment_context']['employer_title'],'太傅');self.reject('liang-canjun',lambda v:v.update(title='太傅'))
 def test_army_organs_not_appointments(self):
  h={v['title']for v in self.rs if'effective_period'in v and v['person_id']==self.by['hu-death']['person_id']};self.assertNotIn('南中郎將',h);self.assertNotIn('江北都督',h);self.assertTrue(self.by['command-expansion']['values']['both_not_subject_appointments'])
 def test_posthumous_not_lifetime_and_named_title_formation(self):
  for k in ['posthumous-shizhong','posthumous-taifu','yi-posthumous-zhennan']:self.assertEqual(self.by[k]['mode'],'posthumous_grant')
  self.assertEqual(self.by['posthumous-cheng']['mode'],'posthumous_naming');self.assertEqual(self.by['jupinghou']['title_formation']['previous_holding_id'],self.by['jupingzi']['id']);self.assertEqual(self.by['jupinghou']['attestations'][0]['surface'],'進本爵為侯')
 def test_birth_not_inferred_age_and_legend_separate(self):
  a=self.by['hu-death-age58'];self.assertEqual(a['value'],58);self.assertIsNone(a['birth_year']);self.assertEqual(a['age_context']['life_event_id'],self.by['hu-death']['id']);self.assertEqual(self.by['hu-age12']['age_context'],{'kind':'during_life'});self.assertEqual(self.by['age5-legend']['values']['age'],5);self.assertTrue(self.by['age5-legend']['values']['not_used_as_documented_age']);self.assertIsNone(self.by['under60-prophecy']['values']['actual_age']);self.reject('hu-death-age58',lambda v:v.update(birth_year=221))
 def test_luoyang_death_place_is_qualified_two_paragraph_interpretation(self):
  a=self.by['hu-death-place-context'];self.assertEqual(a['relation'],'death_place');self.assertEqual(a['place']['source_name'],'洛陽');self.assertEqual(a['qualifiers']['interpretation_status'],'contextual_provisional');self.assertEqual(a['qualifiers']['linked_death_event_id'],self.by['hu-death']['id']);self.assertTrue(a['qualifiers']['secondary_evidence'][0]['paragraph_id'].endswith(':p028'));self.reject('hu-death-place-context',lambda v:v['qualifiers'].update(interpretation_status='source_explicit'))
 def test_assigned_burial_land_not_actual_grave_and_shrine_not_grave(self):
  self.assertTrue(self.by['assigned-burial-land']['values']['actual_burial_completion_not_attested']);self.assertEqual(self.by['ancestral-burial-request']['values']['outcome'],'not_permitted');self.assertFalse(self.by['xianshan-memorial']['values']['is_burial_site']);self.assertFalse(any(v.get('relation')=='burial_place'for v in self.rs))
 def test_unknown_relative_deaths_not_borrow_main_death_year(self):
  for k in ['father-death','mother-death','fa-death','cheng-death','pian-death','faxing-execution','yi-killed','liang-killed']:self.assertNotIn('normalized_date',self.by[k])
 def test_households_belong_to_named_recipients(self):
  self.assertEqual(self.by['guanzhong-households']['values']['count'],100);self.assertEqual(self.by['jupingzi-households']['values']['count'],600);self.assertEqual(self.by['caixi-households']['values']['count'],300);self.assertEqual(self.by['wife-households']['values']['count'],5000);self.assertEqual(self.by['faxing-households']['values']['count'],5000);self.assertNotEqual(self.by['wife-households']['person_id'],self.by['hu-death']['person_id']);self.reject('wife-households',lambda v:v.update(person_id=self.by['hu-death']['person_id']))
 def test_duration_numbers_not_bogus_tenures(self):
  self.assertIsNone(self.by['provisions-not-tenure']['values']['office_tenure_years']);self.assertIsNone(self.by['career-tenplus']['values']['office_holding_id']);self.assertIsNone(self.by['open-office-years']['values']['duration_years']);self.assertIsNone(self.by['shu-conquest-thirteen-years']['values']['derived_calendar_year']);self.assertEqual(self.by['two-courts-career']['values']['regime_count'],2);self.assertIsNone(self.by['conquest-two-after-death']['values']['subject_age'])
 def test_four_unarrived_clerks_are_not_assigned_four_named_people(self):self.assertEqual(self.by['four-clerks-not-arrived']['values']['reported_count'],4);self.assertTrue(self.by['four-clerks-not-arrived']['values']['named_assignees_not_inferred'])
 def test_whole_death_date_moved_consistently_to_duyu_rejected(self):
  v=copy.deepcopy(self.by['hu-death']);p=next(p for p in self.ch['paragraphs']if p['id'].endswith(':p028'));du=next(m for m in p['mentions']if m['surface']=='杜預');v['person_id']=du['person_id']
  for e in v['evidence']:e['person_mention_id']=du['id']
  v['normalized_date']['evidence']=copy.deepcopy(v['evidence']);self.assertFalse(normalized_valid(v['normalized_date'],v,'life_event',self.chapters,ROOT));self.assertFalse(valid(v,self.ch,ROOT))
 def test_correct_date_wrong_endpoint_or_fake_end_rejected(self):
  v=self.by['jingzhou'];d=v['effective_period']['start']['normalized_date'];self.assertFalse(normalized_valid(d,v,'end',self.chapters,ROOT));self.assertFalse(normalized_valid(d,self.by['youpu'],'start',self.chapters,ROOT))
 def test_changed_regnal_number_or_unit_heading_rejected(self):
  proof=copy.deepcopy(next(p for p in self.recipe['date_proofs']if p['slot']=='career_hu-death'));v=self.by['hu-death'];d=v['normalized_date'];proof['regnal_year']=1
  with self.assertRaises(AssertionError):prove(d,v,proof,self.recipe,self.ch,ROOT)
  proof=copy.deepcopy(next(p for p in self.recipe['date_proofs']if p['slot']=='career_hu-death'));proof['primary']['complete_unit']['end']+=1
  with self.assertRaises(AssertionError):prove(d,v,proof,self.recipe,self.ch,ROOT)
 def test_raw_prefix_shift_even_with_metadata_rehash_rejected_by_independent_pin(self):
  proof=copy.deepcopy(next(p for p in self.recipe['date_proofs']if p['slot']=='career_hu-death'));rawpath=ROOT/proof['primary']['raw_path'];metapath=ROOT/proof['primary']['metadata_path'];old=Path.read_bytes;raw=b'\n'+old(rawpath);meta=json.loads(old(metapath));meta['raw_sha256']=hashlib.sha256(raw).hexdigest()
  def shift(v):
   if isinstance(v,dict):
    if type(v.get('start'))is int and type(v.get('end'))is int:v['start']+=1;v['end']+=1
    for x in v.values():shift(x)
   elif isinstance(v,list):
    for x in v:shift(x)
  shift(proof['primary'])
  def read(p):return raw if p==rawpath else json.dumps(meta).encode()if p==metapath else old(p)
  with patch.object(Path,'read_bytes',read),self.assertRaises(AssertionError):prove(self.by['hu-death']['normalized_date'],self.by['hu-death'],proof,self.recipe,self.ch,ROOT)
 def test_source_evidence_path_and_middle_symlink_escape_rejected(self):
  with tempfile.TemporaryDirectory()as t:
   r=Path(t);(r/'source-evidence').mkdir();(r/'outside').mkdir();(r/'outside/a').write_bytes(b'ok');(r/'source-evidence/link').symlink_to(r/'outside',target_is_directory=True)
   for p in ['../outside/a','outside/a','source-evidence/link/a']:
    with self.assertRaises((AssertionError,OSError)):file(r,p)

 def test_quoted_memorial_speaker_is_not_emperor_or_named_interlocutor(self):
  for key in ['cheqi-refusal-denied','shu-conquest-thirteen-years']:
   v=copy.deepcopy(self.by[key]);v['person_id']=self.by['father-death']['person_id'];self.assertFalse(valid(v,self.ch,ROOT))
 def test_real_cli_consistent_wrong_death_recipient_rejected(self):
  import subprocess,sys
  code="""import runpy,json
from pathlib import Path
from unittest.mock import patch
p=Path('corpus/jinshu/034-yanghu-life-events.json').resolve();ch=json.loads(Path('corpus/jinshu/034-yanghu.json').read_text());du=next(m for q in ch['paragraphs']if q['id'].endswith(':p028')for m in q['mentions']if m['surface']=='杜預');d=json.loads(p.read_text());v=next(x for x in d['events']if x['id']=='le-jin034-yanghu-hu-death');v['person_id']=du['person_id']
for e in v['evidence']:e['person_mention_id']=du['id']
v['normalized_date']['evidence']=v['evidence'];old=Path.read_text
def read(q,*a,**kw):return json.dumps(d,ensure_ascii=False)if q.resolve()==p else old(q,*a,**kw)
with patch.object(Path,'read_text',read):runpy.run_path('scripts/validate_corpus.py',run_name='__main__')
"""
  p=subprocess.run([sys.executable,'-c',code],cwd=ROOT,text=True,capture_output=True);self.assertEqual(p.returncode,1,p.stdout+p.stderr);self.assertNotIn('Traceback',p.stdout+p.stderr)

 def test_consistently_extending_annual_unit_across_next_year_rejected(self):
  import re
  proof=copy.deepcopy(next(p for p in self.recipe['date_proofs']if p['slot']=='career_hu-death'));b=proof['primary'];text=(ROOT/b['raw_path']).read_text();oldend=b['complete_unit']['end'];n=re.search(r'(?m)^==[^=\n]+==',text[oldend+1:]);self.assertIsNotNone(n);end=oldend+1+n.start();b['complete_unit']['end']=end;b['complete_unit']['quote']=text[b['complete_unit']['start']:end];b['next_unit_boundary']=text[end:text.index('\n',end)]
  with self.assertRaises(AssertionError):prove(self.by['hu-death']['normalized_date'],self.by['hu-death'],proof,self.recipe,self.ch,ROOT)
 def test_metadata_path_cannot_escape_source_evidence(self):
  proof=copy.deepcopy(next(p for p in self.recipe['date_proofs']if p['slot']=='career_hu-death'));proof['primary']['metadata_path']='source-evidence/../../metadata.json'
  with self.assertRaises(AssertionError):prove(self.by['hu-death']['normalized_date'],self.by['hu-death'],proof,self.recipe,self.ch,ROOT)
