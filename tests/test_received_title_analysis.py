import unittest,json,copy,hashlib
from pathlib import Path
from scripts import jin064_wudi_family_sources as owner
from scripts.validate_corpus import title_attestation_text_valid,normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class ReceivedTitleAnalysis(unittest.TestCase):
 def fixture(self):
  raw=lambda p:(ROOT/p).read_bytes();return raw,{p['id']:p for p in json.loads(raw('registry/persons.json'))['persons']}
 def setup(self):
  raw,people=self.fixture();c,r,docs=owner._proof(raw,people);ch=docs[c['chapter_path']];hs=next(d['holdings']for d in docs.values()if d.get('record_type')=='title_holding_assertion_set');return raw,people,c,r,docs,ch,hs
 def test_01_three_normalized_rank_grants_and_three_undated_designations(self):
  _,_,_,_,_,ch,hs=self.setup();grants=[h for h in hs if h['mode']=='grant'];self.assertEqual([h['title']for h in grants],['城陽王','東海王','始平王']);self.assertEqual([h['effective_period']['start']['normalized_date']['year']for h in grants],[269,273,277])
  for h in hs:self.assertTrue(title_attestation_text_valid(h,h['attestations'][0],ch))
  for h in hs:
   if h['mode']=='attestation':self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertNotIn('normalized_date',h['effective_period']['start'])
 def test_02_ordinary_date_validation_and_received_month_retained(self):
  _,_,_,_,_,ch,hs=self.setup()
  for h in hs:
   if h['mode']=='grant':self.assertEqual(normalized_date_errors(h['effective_period']['start']['normalized_date'],{ch['id']:ch},bound_record=h,bound_role='start'),[])
  h=next(h for h in hs if h['title']=='東海王');self.assertEqual(h['effective_period']['start']['date_expression'],'泰始九年五月');self.assertEqual(h['effective_period']['start']['normalized_date']['precision'],'year');self.assertNotIn('month',h['effective_period']['start']['normalized_date'])
 def test_03_source_compound_attestation_not_silently_rewritten(self):
  _,_,_,_,_,ch,hs=self.setup()
  for h in hs:
   if h['mode']=='grant':self.assertNotEqual(h['attestations'][0]['surface'],h['title']);self.assertEqual(h['received_title_analysis']['surface_anchor']['surface'],h['attestations'][0]['surface']);self.assertIsNone(h['received_title_analysis']['posthumous_date'])
 def invalid(self,change):
  _,_,_,_,_,ch,hs=self.setup();h=copy.deepcopy(next(h for h in hs if h['mode']=='grant'));change(h);self.assertFalse(title_attestation_text_valid(h,h['attestations'][0],ch))
 def test_04_full_posthumous_designation_not_lifetime_granted_title(self):
  def change(h):h['title']=h['attestations'][0]['surface'];h['received_title_analysis']['normalized_title']=h['title']
  self.invalid(change)
 def test_05_posthumous_date_cannot_borrow_grant_year(self):self.invalid(lambda h:h['received_title_analysis'].update(posthumous_date={'year':269}))
 def test_06_grant_cannot_apply_to_epithet(self):self.invalid(lambda h:h['received_title_analysis'].update(grant_applies_to='rank_and_posthumous_name'))
 def test_07_wrong_person_rejected(self):
  _,_,_,r,_,_,_=self.setup();self.invalid(lambda h:h.update(person_id=r['wu']))
 def test_08_wrong_segment_or_boolean_position_rejected(self):
  self.invalid(lambda h:h['received_title_analysis']['rank_anchor'].update(start=0));self.invalid(lambda h:h['received_title_analysis']['surface_anchor'].update(start=False))
 def test_09_false_not_zero_and_unknown_analysis_metadata_rejected(self):
  self.invalid(lambda h:h['received_title_analysis'].update(human_reviewed=0));self.invalid(lambda h:h['received_title_analysis'].update(unreviewed_extra=True))
 def test_10_wrong_grant_event_or_attestation_rejected(self):
  self.invalid(lambda h:h['effective_period']['start'].update(event_type='posthumous_naming'));self.invalid(lambda h:h['attestations'][0].update(surface=h['title']))
 def test_11_original_literal_and_shared_suffix_paths_unchanged(self):
  h={'title':'原稱','unknown_metadata':{'keep':True}};a={'surface':'原稱'};self.assertTrue(title_attestation_text_valid(h,a,{}));self.assertFalse(title_attestation_text_valid(h,{'surface':'他稱'},{}));self.assertTrue(title_attestation_text_valid(h,{'surface':'他稱'},{},True));self.assertEqual(h['unknown_metadata'],{'keep':True})
 def test_12_primary_reference_retains_observed_revision_limits(self):
  _,_,_,_,_,_,hs=self.setup();h=next(h for h in hs if h['title']=='東海王');ref=h['references'][0];self.assertIn('復以第六子祗為東海王',ref['quote']);self.assertFalse(ref['fixed_body_obtained']);self.assertIsNone(ref['actual_print_edition']);self.assertEqual(ref['scope'],'parallel_literal_rank_only_not_source_of_064_date')
 def test_13_missing_or_changed_holding_is_owned_not_optional(self):
  raw,people,c,r,docs,ch,hs=self.setup();path=next(p for p,d in docs.items()if d.get('record_type')=='title_holding_assertion_set');bad=copy.deepcopy(docs[path]);bad['holdings']=bad['holdings'][1:];b=json.dumps(bad,ensure_ascii=False).encode()
  with self.assertRaises(AssertionError):owner._proof(lambda p:b if p==path else raw(p),people)
 def test_14_unknown_chapter_metadata_and_primary_qualification_not_masked(self):
  raw,people,c,r,docs,ch,hs=self.setup();bad=copy.deepcopy(ch);bad['source']['image_verified']=True;b=json.dumps(bad,ensure_ascii=False).encode()
  with self.assertRaises(AssertionError):owner._proof(lambda p:b if p==c['chapter_path']else raw(p),people)
 def test_15_general_parser_accepts_same_glyph_in_territory_and_epithet(self):
  _,_,_,_,_,ch,hs=self.setup();h=copy.deepcopy(next(h for h in hs if h['mode']=='grant'));q=copy.deepcopy(ch);b=h['received_title_analysis'];p=next(p for p in q['paragraphs']if p['id']==b['paragraph_id']);p['text']='安陽安王'+p['text'][4:];m=next(m for m in p['mentions']if m['id']==b['person_mention_id']);m['surface']='安陽安王'+m['surface'][4:];h['title']='安陽王';b['normalized_title']='安陽王';b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();b['surface_anchor']['surface']='安陽安王';b['territory_anchor']['surface']='安陽';b['posthumous_anchor']['surface']='安';h['attestations'][0]['surface']='安陽安王';h['evidence'][0]['quote']=p['text'];h['effective_period']['start']['evidence'][0]['quote']=p['text'];self.assertTrue(title_attestation_text_valid(h,h['attestations'][0],q))
 def test_16_normal_export_projection_preserves_source_and_analysis(self):
  from scripts.table_person_profiles import project_title_holdings
  _,_,_,_,_,_,hs=self.setup();before=copy.deepcopy(hs);titles=project_title_holdings(hs,{h['person_id']for h in hs});self.assertEqual(hs,before);self.assertEqual(len(titles),6)
  for src,out in zip(hs,titles):
   self.assertEqual({k:v for k,v in out.items()if k!='period'},src)
   if src['mode']=='grant':self.assertIn(str(src['effective_period']['start']['normalized_date']['year']),out['period'])
   else:self.assertEqual(out['period'],'未定 → 未定')
if __name__=='__main__':unittest.main()
