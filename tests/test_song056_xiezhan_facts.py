# coding: utf-8
from pathlib import Path
import sys,json,hashlib,copy,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.validate_corpus import normalized_date_errors
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.age_context import age_context_valid
from scripts.office_transfers import office_transfer_valid
from scripts.person_bundle import load_catalog,bundle
J=lambda p:json.loads(p.read_text());E=lambda d:(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode();H=lambda b:hashlib.sha256(b).hexdigest()
C=J(ROOT/'corpus/songshu/056-xiezhan.json');P=C['paragraphs'];HS=[h for h in J(ROOT/'corpus/songshu/056-xiezhan-titles.json')['holdings']if h['id'].startswith('th-song056-f20-')];LE=[e for e in J(ROOT/'corpus/songshu/056-xiezhan-life-events.json')['events']if e['id'].startswith('le-song056-f20-')];AD=[a for a in J(ROOT/'corpus/songshu/056-xiezhan-addresses.json')['assertions']if a['id'].startswith('pa-song056-f20-')];N=[n for n in J(ROOT/'data/corpus/profile-names.json')['records']if n.get('id','').startswith('name-song056-f20-')];AG=[a for a in C['annotation']['age_assertions']if a['id'].startswith('age-song056-f20-')];TP=[a for a in C['annotation']['title_proposals']if a['id'].startswith('tp-song056-f20-')];REVIEW=J(ROOT/'source-evidence/song056-f20-consumption-review.json');RETAIN=J(ROOT/'source-evidence/song056-f20-retained-proposals.json')['proposals'];BYE={e['id']:e for e in LE}
def who(n,t):return next(m['person_id']for m in P[n-1]['mentions']if m['surface']==t)
def event(pid):return next(e for e in LE if e['person_id']==pid)
def qp(num):return next(q for q in RETAIN if q.get('source_proposal_id',q['id'])==f'proposal-song056-xiezhan-{num:03d}')
class XiezhanFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.cat=load_catalog(ROOT)
 def test_scoped_counts(self):self.assertEqual((len(HS),len(N),len(LE),len(AG),len(AD),len(TP)),(23,19,4,3,4,1));self.assertEqual(REVIEW['formal_record_count'],54)
 def test_source_and_ner_exactly_preserved(self):
  self.assertEqual(H(E(P)),REVIEW['source_paragraphs_sha256']);self.assertEqual(H(E(C['source'])),REVIEW['source_metadata_sha256']);self.assertEqual(sum(len(p['mentions'])for p in P),98);self.assertEqual(sum(len(p['text'])for p in P),740)
 def test_original_source_annotation_evidence_bound(self):
  b=REVIEW['source_only_annotation'];self.assertEqual(H(E(b)),REVIEW['source_only_annotation_sha256']);self.assertNotIn('age_assertions',b);self.assertNotIn('title_proposals',b);self.assertFalse(b['human_reviewed']);self.assertEqual(len(REVIEW['source_chapter_sha256']),64)
 def test_zhan_two_names_and_courtesy_pairings(self):
  ns=[n for n in N if n['person_id']=='aa6_83c_juy_AAAD'];self.assertEqual({(n['surname'],n['ming'],n['zi'])for n in ns},{('謝','瞻','宣逺'),('謝','檐','通逺')});self.assertEqual(len(ns),2)
 def test_jue_preserves_glyph_and_zi(self):
  n=next(n for n in N if n.get('zi')=='宣鏡');self.assertEqual(n['ming'],'㬭');self.assertIsNone(n['surname']);self.assertNotEqual(n['ming'],'爵')
 def test_huan_name_is_same_identity_not_silent_text_fix(self):
  n=next(n for n in N if n.get('ming')=='奐');self.assertEqual(n['person_id'],'aa6_83c_juy_CDA');self.assertIn('靈運父奐',P[1]['text']);self.assertNotIn('父瑍',P[1]['text'])
 def test_unsupplied_surnames_not_backfilled(self):
  for pid in [who(1,'柳'),who(3,'㬭'),who(3,'世平')]:self.assertTrue(all(n['surname']is None for n in N if n['person_id']==pid))
 def test_mother_surnames_without_given_names(self):
  for pid,sur in [(who(1,'劉'),'劉'),(who(3,'郭氏'),'郭')]:
   n=next(n for n in N if n['person_id']==pid);self.assertEqual(n['surname'],sur);self.assertIsNone(n['ming'])
 def test_hongwei_not_fabricated_ming(self):
  n=next(n for n in N if n['person_id']=='b60_740_5f6_A');self.assertIsNone(n['ming']);self.assertEqual(n['additional_names'],['𢎞微'])
 def test_patron_titles_belong_to_patrons(self):
  self.assertTrue(any(h['title']=='安西'and h['person_id']=='9j5_n7n_c3u'for h in HS));self.assertTrue(any(h['title']=='鎮軍'and h['person_id']=='3dv_ken_w58'for h in HS));self.assertTrue(any(h['title']=='大司馬'and h['person_id']=='ije_ngm_cmj'for h in HS));self.assertFalse(any(h['person_id']=='aa6_83c_juy_AAAD'and h['title']in ['安西','鎮軍','大司馬']for h in HS))
 def test_princess_title_does_not_add_imperial_father(self):
  h=next(h for h in HS if h['title']=='南郡公主');self.assertEqual(h['person_id'],who(1,'晉南郡公主'));self.assertEqual(h['mode'],'attestation');self.assertTrue(all(x['attestations'][0]['date_expression']is None for x in HS if x['person_id']==h['person_id']))
 def test_unassumed_secretary_positive(self):
  t=TP[0];self.assertEqual(t['title'],'祕書丞');self.assertTrue(unassumed_appointment_valid(t,C));self.assertEqual(t['complete_non_assumption_expression'],'固辭不就');a=t['complete_non_assumption_anchor'];self.assertEqual(P[2]['text'][a['start']:a['end']],'固辭不就');self.assertFalse(any(h['title']=='祕書丞'for h in HS))
 def test_unassumed_does_not_cover_later_offices(self):
  t=copy.deepcopy(TP[0]);a=P[2]['text'].index('司空長史');t.update(title='司空長史',role_anchor={'paragraph_id':P[2]['id'],'start':a,'end':a+4,'surface':'司空長史'});self.assertFalse(unassumed_appointment_valid(t,C));self.assertFalse(any(h['title']in ['司空長史','黄門郎']for h in HS))
 def test_unassumed_wrong_subject_rejected(self):
  t=copy.deepcopy(TP[0]);t['person_id']='4y6_myv_ojh';self.assertFalse(unassumed_appointment_valid(t,C))
 def test_noncontinuous_shared_suffix_not_invented(self):
  self.assertFalse(any(h['person_id']=='aa6_83c_juy_AAAD'and h['title']=='鎮軍參軍'for h in HS));self.assertEqual(qp(11)['facts_phase_disposition'],'partially_adopted');self.assertIn('參軍',qp(11)['retained_reason'])
 def test_district_names_not_office_titles(self):
  self.assertFalse(any(h['title']in ['吴興郡','吴興太守','吴郡太守']for h in HS));self.assertEqual(qp(19)['status'],'not_imported');self.assertEqual(qp(21)['status'],'not_imported')
 def test_invitation_not_active_holding(self):
  self.assertTrue(qp(28)['retained_reason']);self.assertTrue(qp(29)['retained_reason']);self.assertFalse(any(h['title']in ['司空長史','黄門郎']for h in HS))
 def test_explicit_transfer_and_broader_list(self):
  pmap={p['id']:(C['id'],p)for p in P};mmap={m['id']:(C['id'],p['id'],m)for p in P for m in p['mentions']};h=next(h for h in HS if h['mode']=='transfer');self.assertEqual(h['title'],'主簿');self.assertTrue(office_transfer_valid(h,pmap,mmap));fallback=[h for h in HS if h.get('source_appointment_classification')];self.assertEqual(len(fallback),4);self.assertTrue(all(h['mode']=='grant'for h in fallback))
 def test_exact_title_anchors(self):
  ps={p['id']:p for p in P}
  for h in HS:
   for a in h['attestations']:self.assertEqual(ps[a['paragraph_id']]['text'][a['start']:a['end']],a['surface'])
 def test_explicit_regnal_death_years_chinese_calendar(self):
  self.assertEqual(event('aa6_83c_juy_AAAD')['normalized_date']['year'],421);self.assertEqual(event(who(3,'㬭'))['normalized_date']['year'],426)
  for e in LE:
   if e.get('normalized_date'):self.assertEqual(normalized_date_errors(e['normalized_date'],{C['id']:C}),[]);self.assertEqual(e['normalized_date']['calendar'],'chinese_civil')
 def test_wrong_normalized_year_rejected(self):
  d=copy.deepcopy(event('aa6_83c_juy_AAAD')['normalized_date']);d['year']=d['era_year']=422;self.assertTrue(normalized_date_errors(d,{C['id']:C}))
 def test_changed_era_not_accepted(self):
  d=copy.deepcopy(event(who(3,'㬭'))['normalized_date']);d['regnal_year_mapping']['era_name']='永初';self.assertTrue(normalized_date_errors(d,{C['id']:C}))
 def test_no_copied_dates_for_father_or_son(self):
  for pid in ['aa6_83c_juy_CDA',who(3,'世平')]:self.assertIsNone(event(pid)['date_expression']);self.assertNotIn('normalized_date',event(pid))
 def test_three_ages_and_no_birth_inference(self):
  self.assertEqual(sorted(a['value']for a in AG),[6,31,35]);self.assertTrue(all(a['birth_year']is None for a in AG));self.assertFalse(any(e['event_type']=='birth'for e in LE));self.assertTrue(all(age_context_valid(a,BYE)for a in AG))
 def test_childhood_age_not_death_age(self):
  a=next(a for a in AG if a['value']==6);self.assertEqual(a['age_context'],{'kind':'during_life'});self.assertIsNone(a['date_expression']);self.assertEqual(a['complete_reported_expression'],'年六嵗')
 def test_wrong_person_death_age_link_rejected(self):
  a=copy.deepcopy(next(a for a in AG if a['value']==35));a['age_context']['life_event_id']=event(who(3,'㬭'))['id'];self.assertFalse(age_context_valid(a,BYE))
 def test_hui_age_thirty_not_erased_or_formalized(self):
  q=qp(33);self.assertEqual(q['value'],30);self.assertEqual(q['person_ids'],['aa6_83c_juy_AAAA']);self.assertEqual(q['complete_reported_expression'],'弟年始三十');self.assertFalse(any(a['value']==30 for a in AG))
 def test_numeric_relative_position_three_preserved(self):
  q=qp(5);self.assertEqual(q['reported_relative_position'],3);self.assertIsNone(q['absolute_birth_order']);self.assertEqual(q['source_number'],'三')
 def test_care_duration_and_approximate_age_not_birth(self):
  self.assertIsNone(qp(36)['value']);self.assertEqual(qp(45)['value'],10);self.assertEqual(qp(45)['approximation'],'over');self.assertIsNone(qp(45)['calendar_year']);self.assertIsNone(qp(45).get('birth_year'))
 def test_no_death_closure_or_office_date_from_dasima(self):
  self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in HS));self.assertTrue(all(h['attestations'][0]['date_expression']is None for h in HS));self.assertTrue(all('normalized_date'not in h['effective_period']['start']for h in HS))
 def test_origin_service_residence_not_death_place(self):
  self.assertEqual(sum(a['relation']=='biographical_origin'for a in AD),1);self.assertEqual(sum(a['relation']=='service_location'for a in AD),2);self.assertEqual(sum(a['relation']=='residence'for a in AD),1);self.assertFalse(any(a['relation']=='death_place'for a in AD));self.assertTrue(all(a['place']['modern_identification']is None for a in AD))
 def test_parent_inferences_deferred_no_rekey(self):
  self.assertTrue(qp(46)['inference']);self.assertTrue(qp(47)['reversible']);self.assertFalse(qp(46)['remapping_applied']);self.assertFalse(qp(47)['remapping_applied']);ps={p['id']for p in J(ROOT/'registry/persons.json')['persons']};self.assertIn('aa6_83c_juy_AAAD',ps);self.assertIn(who(3,'㬭'),ps)
 def test_all_47_consumption_rows_and_retained_18(self):
  self.assertEqual(len(REVIEW['records']),47);self.assertEqual(len({r['source_proposal_id']for r in REVIEW['records']}),47);self.assertEqual(len(RETAIN),18);self.assertTrue(REVIEW['not_active_research_append'])
 def test_retained_source_anchors_exact(self):
  ps={p['id']:p for p in P}
  for q in RETAIN:
   if'evidence'not in q:continue
   e=q['evidence'];a=e['anchor'];self.assertEqual(ps[e['paragraph_id']]['text'][a['start']:a['end']],a['surface']);self.assertEqual(e['quote'],ps[e['paragraph_id']]['text'])
 def test_memory_bundles_contain_exact_new_records(self):
  wanted={r['person_id']for r in [*HS,*N,*LE,*AG,*AD,*TP]}
  for pid in wanted:
   b=bundle(pid,root=ROOT,catalog=self.cat,include_provisional=True)
   for key,records in [('title_holdings',HS),('name_components',N),('life_events',LE),('age_assertions',AG),('address_assertions',AD),('title_proposals',TP)]:
    actual={r.get('id')for r in b.get(key,[])if r.get('id')};self.assertTrue({r['id']for r in records if r['person_id']==pid}<=actual,(pid,key))
 def test_new_facts_do_not_claim_human_or_image_review(self):
  self.assertFalse(C['source']['image_verified']);self.assertTrue(all(r['human_reviewed']is False for r in [*HS,*N,*LE,*AG,*AD,*TP]))
if __name__=='__main__':unittest.main()
