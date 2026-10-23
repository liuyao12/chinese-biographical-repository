# coding: utf-8
import unittest,json,copy,sys,tempfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.fixed_complete_family_career import records,valid,errors,KIND
from scripts.person_bundle import load_catalog
class FixedCompleteFamilyCareerTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/040-jiachong-family.json').read_text());cls.rs=records(cls.ch,ROOT)
 def one(self,category,term,paragraph):
  key={'holding':'source_career_role','detail':'source_career_role','life':'fixed_family_career_binding','address':'fixed_family_career_binding','proposal':'source_appointment_context','age':'fixed_family_career_binding'}[category]
  return copy.deepcopy(next(v for v in self.rs if key in v and v[key]['paragraph_id'].endswith(':p'+str(paragraph).zfill(3))and v.get('title',v.get('source_term'))==term))
 def wrong_recipient(self,v,word):
  k=next(k for k in('source_career_role','source_appointment_context','fixed_family_career_binding')if k in v);p=next(p for p in self.ch['paragraphs']if p['id']==v[k]['paragraph_id']);m=next(m for m in p['mentions']if m.get('surface')==word and m.get('person_id')!=v['person_id']);v['person_id']=m['person_id'];v[k]['person_mention_id']=m['id']
  for e in v['evidence']:e['person_mention_id']=m['id'];e.pop('context',None)
  for a in v.get('attestations',[]):a['person_mention_id']=m['id'];a.pop('context',None)
  if 'person_mention_id'in v:v['person_mention_id']=m['id']
  if 'effective_period'in v and v['effective_period']['start'].get('evidence'):v['effective_period']['start']['evidence']=copy.deepcopy(v['evidence'])
  return v
 def test_all_categories_use_full_received_source(self):
  cat=load_catalog(ROOT);self.assertEqual(errors(ROOT,cat[1]),[])
  self.assertEqual(len(self.ch['paragraphs']),30);self.assertEqual(self.ch['source']['revision_id'],2606035)
 def test_consistent_other_military_recipient_rejected(self):self.assertFalse(valid(self.wrong_recipient(self.one('holding','大都督',14),'楊濟'),self.ch,ROOT))
 def test_consistent_emperor_recipient_rejected(self):self.assertFalse(valid(self.wrong_recipient(self.one('holding','晉國衞將軍',5),'武帝'),self.ch,ROOT))
 def test_death_cannot_move_to_named_son(self):self.assertFalse(valid(self.wrong_recipient(self.one('life','薨',16),'黎民'),self.ch,ROOT))
 def test_omitted_subject_not_preceding_minister(self):self.assertFalse(valid(self.wrong_recipient(self.one('holding','尚書令',7),'裴秀'),self.ch,ROOT))
 def test_qinliang_not_assumed_is_not_a_holding(self):
  qs=[v for v in self.rs if v.get('source_appointment_context',{}).get('paragraph_id','').endswith('p009')];self.assertEqual({q['title']for q in qs},{'使持節','都督秦涼二州諸軍事'});self.assertTrue(all(q['outcome']=='not_assumed'and q['non_assumption_anchor']['surface']=='遂不西行'for q in qs))
  self.assertFalse(any(v.get('source_career_role',{}).get('paragraph_id','').endswith('p009')and v.get('title')in{q['title']for q in qs}for v in self.rs))
 def test_sikong_notice_is_service_unreported_not_declined(self):
  q=self.one('proposal','司空',2);self.assertEqual((q['proposal_kind'],q['outcome']),('appointment_service_unreported','not_reported'));q['outcome']='not_assumed';self.assertFalse(valid(q,self.ch,ROOT))
 def test_rejected_posthumous_name_not_adopted(self):
  q=self.one('proposal','荒',17);self.assertEqual(q['outcome'],'not_enacted');self.assertFalse(any(v.get('title')=='荒'for v in self.rs if'attestations'in v));q['outcome']='granted';self.assertFalse(valid(q,self.ch,ROOT))
 def test_death_year_and_month_do_not_create_birth_or_office_end(self):
  v=self.one('life','薨',16);self.assertEqual((v['normalized_date']['year'],v['source_month_expression'],v['source_month_number']),(282,'四月',4));self.assertNotIn('birth_year',v)
  self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in self.rs if'attestations'in h))
 def test_unknown_later_office_does_not_borrow_death_year(self):
  h=self.one('holding','晉國衞將軍',5);h['effective_period']['start']['normalized_date']=copy.deepcopy(self.one('life','薨',16)['normalized_date']);self.assertFalse(valid(h,self.ch,ROOT))
 def test_lifetime_child_age_and_death_age_remain_distinct(self):
  a=self.one('age','三歲',17);b=self.one('age','年六十六',16);self.assertEqual(a['age_context'],{'kind':'during_life'});self.assertEqual(b['age_context']['kind'],'at_death');self.assertIsNone(a['birth_year']);self.assertIsNone(b['birth_year']);a['birth_year']=280;self.assertFalse(valid(a,self.ch,ROOT))
 def test_source_locality_is_not_birthplace(self):
  a=self.one('address','渤海',20);self.assertEqual(a['relation'],'source_locality_designation');self.assertIsNone(a['qualifiers']['origin_or_residence']);a['relation']='birth_place';self.assertFalse(valid(a,self.ch,ROOT))
 def test_anonymous_grantee_not_assigned_to_named_son(self):
  v=self.one('detail','賜充子弟一人關內侯',6);self.assertIsNone(v['values']['recipient_person_id']);self.assertFalse(v['values']['biological_children_only']);v['values']['recipient_person_id']=self.one('life','發病而死',17)['person_id'];self.assertFalse(valid(v,self.ch,ROOT))
 def test_increases_are_not_totals_or_inherited_by_other_people(self):
  v=self.one('detail','增邑八千戸',15);self.assertEqual((v['values']['value'],v['values']['total']),(8000,None));v['values']['total']=8000;self.assertFalse(valid(v,self.ch,ROOT))
 def test_royal_title_is_inside_its_person_not_houtu(self):
  h=self.one('holding','后',17);m=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['id']==h['attestations'][0]['person_mention_id']);self.assertTrue(m['start']<=h['attestations'][0]['start']<m['end']);self.assertEqual(m['surface'],'賈后')
 def test_missing_typed_slot_rejected(self):
  cat=load_catalog(ROOT);rows=copy.deepcopy(cat[1]);r=next(r for r in rows if r.get('chapter_id')==self.ch['id']and r.get('record_type')=='title_holding_assertion_set');r['holdings'].pop();self.assertTrue(errors(ROOT,rows))
 def test_joint_wife_arrangement_not_military_non_assumption(self):
  qs=[v for v in self.rs if v.get('title')=='左右夫人'];self.assertEqual(len(qs),2);self.assertTrue(all(q['source_outcome']=='declined_joint_wife_arrangement'and q['outcome']=='not_assumed'for q in qs));self.assertEqual(len({q['person_id']for q in qs}),2)
 def test_inheritance_predecessor_is_bound_father_without_fake_title_word(self):
  v=self.one('detail','襲父爵爲侯',1);father=next(m for m in self.ch['paragraphs'][0]['mentions']if m.get('surface')=='逵');self.assertEqual(v['values']['predecessor_person_id'],father['person_id']);self.assertIsNone(v['values']['title']);self.assertEqual(v['values']['resolved_title_status'],'contextual_provisional');v['values']['predecessor_person_id']=v['person_id'];self.assertFalse(valid(v,self.ch,ROOT))
 def test_numeric_source_counts_reject_bool_or_float(self):
  v=self.one('detail','賜充子弟一人關內侯',6)
  for bad in(True,1.0):
   w=copy.deepcopy(v);w['values']['count']=bad;self.assertFalse(valid(w,self.ch,ROOT))
 def test_missing_fixed_witness_contract_is_rejected(self):
  c=copy.deepcopy(self.ch);c['annotation'].pop('fixed_wikisource_unit_ref');self.assertFalse(valid(self.one('holding','尚書郎',1),c,ROOT))
 def test_raw_offset_cosshift_with_new_hash_still_rejected(self):
  from scripts.fixed_wikisource_family_units import project
  from scripts.fixed_wikisource_units import source_errors
  c=copy.deepcopy(self.ch);ref=c['annotation']['fixed_wikisource_unit_ref'];b=json.loads((ROOT/ref).read_text());raw='\n'+(ROOT/b['raw_file']).read_text();sha=hashlib.sha256(raw.encode()).hexdigest();ps,selection=project(raw,c['title']);b['raw_sha256']=sha;b['selection']=selection
  for k in('raw_file_sha256','wikitext_sha256'):c['source'][k]=sha
  c['annotation']['preserved_source_headings']=selection['headings']
  for p,q in zip(c['paragraphs'],ps):p['source_position']=dict(q['source_position'],revision_id=2606035)
  with tempfile.TemporaryDirectory()as td:
   r=Path(td)
   for rel,data in [(b['raw_file'],raw),(ref,json.dumps(b,ensure_ascii=False))]:(r/rel).parent.mkdir(parents=True,exist_ok=True);(r/rel).write_text(data)
   self.assertEqual(source_errors(c,r),[]);self.assertFalse(valid(self.one('holding','尚書郎',1),c,r))
if __name__=='__main__':unittest.main()
