import copy,json,hashlib,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_jin098_wangdun_career as career
from scripts import fixed_jin098_wangdun_comparison as core
from scripts.received_career_roles import holding_valid,detail_valid
from scripts.validate_corpus import title_proposal_errors,normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class CareerPhase1(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=career.read(ROOT,career.CH);cls.roles,cls.t=career.prepared(cls.ch,ROOT);cls.hs=cls.t['title_record']['holdings'];cls.ds=cls.t['detail_record']['records'];cls.qs=cls.t['annotation']['title_proposals'];cls.people={p['id']:p for p in career.read(ROOT,'registry/persons.json')['persons']};cls.records=[cls.ch,cls.t['title_record'],cls.t['detail_record']]
 def test_all45_normal_dispatch(self):
  self.assertEqual((len(self.hs),len(self.qs),len(self.ds)),(25,7,13));hs={h['id']:h for h in self.hs}
  for h in self.hs:self.assertTrue(holding_valid(h,self.ch,ROOT),h['id'])
  for q in self.qs:self.assertEqual(title_proposal_errors(q,self.ch,set(self.people),hs,ROOT),[],q['id'])
  for d in self.ds:self.assertTrue(detail_valid(d,self.ch,hs,ROOT),d['id'])
 def test_no_unassumed_or_self_in_holdings(self):
  self.assertFalse(any(h['title']in('丞相','江州牧','武昌郡公','荊州牧','尚書','揚州牧')for h in self.hs));self.assertTrue(all(h['effective_period']['end']==dict(status='unknown',date_expression=None,evidence=[])for h in self.hs));self.assertTrue(all('normalized_date'not in h['effective_period']['start']for h in self.hs))
 def test_unknown_chu_is_not_year1(self):
  rows={h['title']:h for h in self.hs if h['title']in('中書監','征南大將軍')};self.assertEqual(rows['中書監']['effective_period']['start']['date_expression'],'永嘉初');self.assertEqual(rows['征南大將軍']['effective_period']['start']['date_expression'],'建武初')
  for h in rows.values():
   x=copy.deepcopy(h);x['effective_period']['start']['normalized_date']={'year':307};self.assertFalse(holding_valid(x,self.ch,ROOT))
 def test_not_borrow_daos_situ_or_false_bounty(self):
  for title in('司徒','五千戶侯'):
   h=copy.deepcopy(self.hs[0]);h['title']=title;self.assertFalse(holding_valid(h,self.ch,ROOT))
 def test_wrong_subject_or_mid(self):
  for key,value in [('person_id',self.roles['dao']),('mode','self_proclamation'),('status','editorial_provisional')]:
   h=copy.deepcopy(self.hs[0]);h[key]=value;self.assertFalse(holding_valid(h,self.ch,ROOT))
  h=copy.deepcopy(self.hs[0]);h['source_career_role']['recipient_mention_id']=core.CID+':p001:m0017';self.assertFalse(holding_valid(h,self.ch,ROOT))
 def test_not_accepted_proposal_into_holding(self):
  for q in self.qs:
   x=copy.deepcopy(q);x['outcome']='not_reported';self.assertTrue(title_proposal_errors(x,self.ch,set(self.people),{},ROOT));self.assertFalse(holding_valid(x,self.ch,ROOT))
 def test_private_roles_machine_readable(self):
  d,=[d for d in self.ds if d['kind']=='source_self_assumption'];self.assertEqual(d['values']['authority'],'self_assumed');self.assertEqual(d['values']['appointing_person_id'],self.roles['dun']);self.assertEqual(d['values']['role_name'],'揚州牧');self.assertIs(d['values']['court_appointment_attested'],False)
  x=copy.deepcopy(d);x['values']['authority']='court_granted';self.assertFalse(detail_valid(x,self.ch,{},ROOT))
  m,=[d for d in self.ds if d['kind']=='military_authority'];self.assertIsNone(m['values']['role_name']);self.assertEqual([r['source_name']for r in m['values']['command_regions']],['寧','益'])
 def test_token_guards_and_ritual_exemptions_distinct(self):
  token=[d for d in self.ds if d['kind']=='military_token_authority'];self.assertEqual({d['source_term']for d in token},{'假節','黃龯'});self.assertTrue(all(d['values']['conferred_powers_not_further_inferred']is True for d in token));self.assertEqual(len([d for d in self.ds if d['kind']=='ceremonial_guard_complement']),1);self.assertEqual({d['source_term']for d in self.ds if d['kind']=='ritual_and_duty_exemption'},{'奏事不名','入朝不趨','劍覆上殿'})
 def test_staff_and_fief_are_different_numbers(self):
  staff,=[d for d in self.ds if d['kind']=='staff_complement'];self.assertEqual([x['reported_count']for x in staff['values']['roles']],[2,2,2]);q,=[q for q in self.qs if q['title']=='武昌郡公'];self.assertEqual(q['reported_households']['value'],10000);self.assertEqual(q['reported_households']['scope'],'offered_appointment_not_assumed');self.assertIsNone(q['reported_households']['actual_revenue'])
  x=copy.deepcopy(q);x['reported_households']['actual_revenue']=10000;self.assertTrue(title_proposal_errors(x,self.ch,set(self.people),{},ROOT))
 def test_323_exact_source_and_not_death(self):
  rows=[d for d in self.ds if d.get('normalized_date',{}).get('event_evidence_binding',{}).get('kind')=='fixed_jin098_career_local_year'];self.assertEqual(len(rows),6)
  for d in rows:self.assertEqual(normalized_date_errors(d['normalized_date'],{self.ch['id']:self.ch},ROOT,d,'source_detail'),[])
  d=rows[0]
  for key,value in [('year',324),('source_expression','太寧元年'),('human_reviewed',True)]:
   n=copy.deepcopy(d['normalized_date']);n[key]=value;self.assertTrue(normalized_date_errors(n,{self.ch['id']:self.ch},ROOT,d,'source_detail'))
  for mutation in ['wrong_dynasty','wrong_era','wrong_number','cross_paragraph']:
   n=copy.deepcopy(d['normalized_date'])
   if mutation=='wrong_dynasty':n['references'][0]['columns']['dynasty']='魏'
   elif mutation=='wrong_era':n['regnal_year_mapping']['era_name']='永嘉'
   elif mutation=='wrong_number':n['regnal_year_mapping']['regnal_year']=2
   else:n['event_evidence_binding']['date_anchor']['paragraph_id']=core.CID+':p034'
   self.assertTrue(normalized_date_errors(n,{self.ch['id']:self.ch},ROOT,d,'source_detail'),mutation)
  self.assertTrue(normalized_date_errors(d['normalized_date'],{self.ch['id']:self.ch},ROOT,d,'life_event'))
 def test_catalog_no_missing_either_owner(self):
  career.catalog_valid(self.records,self.people,ROOT)
  for r in self.records:
   rows=[copy.deepcopy(x)for x in self.records if x is not r]
   with self.assertRaises(ValueError):career.catalog_valid(rows,self.people,ROOT)
  for key in('career_stage','title_proposals','life_stage','age_assertions'):
   rows=copy.deepcopy(self.records);rows[0]['annotation'].pop(key)
   with self.assertRaises(ValueError):career.catalog_valid(rows,self.people,ROOT)
 def test_source_body_unchanged_and_all44_slots_mapped(self):
  rows=self.hs+self.qs+self.ds;slots=[r.get('source_career_role',r.get('source_appointment_context'))['slot_id']for r in rows];self.assertEqual(len(set(slots)),45);self.assertIn('career-p011-staff-complement',slots)
  view=career.joint_stripped_chapter(self.ch,ROOT);expected=core.expand(core.fixed(ROOT,'ner-template.json'),self.roles);self.assertTrue(core.same(view,expected));self.assertEqual(sum(m['kind']!='work'for p in view['paragraphs']for m in p['mentions']),511);self.assertEqual({m['id']for p in view['paragraphs']for m in p['mentions']if m['kind']=='work'},{'c-jinshu-098-wangdun-comparison:p037:w0017'});self.assertEqual(sum(len(p['mentions'])for p in view['paragraphs']),512)
 def test_wrong_passed_chapter_and_raw_scope(self):
  ch=copy.deepcopy(self.ch);ch['paragraphs'][0]['text']+='改'
  with self.assertRaises(ValueError):career.prepared(ch,ROOT)
  ch=copy.deepcopy(self.ch);ch['paragraphs'][18]['text_layer']='received_compiler_appraisal'
  with self.assertRaises(ValueError):career.prepared(ch,ROOT)
 def test_old_no_stage_unrelated_catalog_unchanged(self):
  with tempfile.TemporaryDirectory()as d:career.catalog_valid([],{},Path(d))
 def mini(self):
  td=tempfile.TemporaryDirectory();root=Path(td.name);seen=set();old=core.path
  def track(r,rel):seen.add(rel);return old(r,rel)
  with patch.object(core,'path',track):
   career.prepared(self.ch,ROOT);core.validate_ner(self.ch,ROOT)
  for rel in seen:
   q=root/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,q)
  return td,root
 def test_consistent_UID_rekey_closure_and_one_end_rejected(self):
  td,r=self.mini();old=self.roles['dun'];new='r7q_v9p_2zt'
  def rec(x):
   if isinstance(x,dict):return{k:rec(v)for k,v in x.items()}
   if isinstance(x,list):return[rec(v)for v in x]
   return new if x==old else x
  try:
   for directory in['registry','corpus']:
    for q in(r/directory).rglob('*.json'):q.write_text(json.dumps(rec(json.loads(q.read_bytes())),ensure_ascii=False))
   c=career.read(r,career.CH);roles,t=career.prepared(c,r);self.assertEqual(roles['dun'],new);self.assertTrue(core.validate_ner(c,r));h=t['title_record']['holdings'][0];self.assertTrue(holding_valid(h,c,r));self.assertEqual(title_proposal_errors(t['annotation']['title_proposals'][0],c,{p['id']for p in career.read(r,'registry/persons.json')['persons']},{},r),[])
   bad=copy.deepcopy(h);bad['person_id']=old;self.assertFalse(holding_valid(bad,c,r))
  finally:td.cleanup()
 def test_actual_row_hash_drift_and_shadow_sidecar(self):
  td,r=self.mini()
  try:
   # Calendar is additionally read by date_valid; copy actual fixed capture explicitly.
   cal=career.fixed(ROOT,'calendar-row-proof.json');q=r/cal['existing_capture_path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/cal['existing_capture_path'],q);d=next(d for d in self.ds if d.get('normalized_date',{}).get('event_evidence_binding',{}).get('kind')=='fixed_jin098_career_local_year');self.assertTrue(career.date_valid(d['normalized_date'],d,'source_detail',{self.ch['id']:self.ch},r));q.write_bytes(q.read_bytes().replace(b'323',b'324',1));self.assertFalse(career.date_valid(d['normalized_date'],d,'source_detail',{self.ch['id']:self.ch},r))
   shadow=r/'corpus/jinshu/098-shadow-titles.json';shadow.write_text(json.dumps(self.t['title_record']))
   with self.assertRaises(ValueError):career.prepared(self.ch,r)
  finally:td.cleanup()
 def test_owners_cannot_overlap_annotation_keys(self):
  from scripts import fixed_jin098_wangdun_life as life
  old=life.prepared
  def conflict(ch,root):
   rs,t=old(ch,root);t=copy.deepcopy(t);t['life_annotation']['career_stage']='fixed_jin098_career_p001_p019';return rs,t
  with patch.object(life,'prepared',conflict):
   with self.assertRaises(ValueError):career.joint_stripped_chapter(self.ch,ROOT)
if __name__=='__main__':unittest.main()
