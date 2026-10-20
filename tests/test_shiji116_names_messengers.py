import copy,json,unittest
from pathlib import Path
from scripts.person_bundle import bundle
from scripts.consolidate_person_ids import reference_files
from scripts.validate_corpus import reported_relationship_errors
R=Path(__file__).resolve().parents[1]
OLD={'348_22z_ti1':'11q_2yl_qzt','d65_9vi_t06':'miw_t0v_k64'}
def read(p):return json.loads((R/p).read_text())
class XinanyiNamesMessengers(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=read('corpus/shiji/116.json');cls.para=next(p for p in cls.chapter['paragraphs']if p['id'].endswith('p002'));cls.variant=next(v for v in cls.chapter['annotation']['reported_variants']if v['component']=='reported_kinship')
 def test_two_explicit_names_do_not_invent_surnames(self):
  names={n['person_id']:n for n in read('data/corpus/profile-names.json')['records']}
  for pid,title,ming in [('98i_dd4_aof','夜郎侯','多同'),('h0h_wsl_1nf','滇王','嘗羌')]:
   n=names[pid];self.assertEqual((n['title'],n['surname'],n['ming']),(title,None,ming));self.assertTrue(any('683113d4baf6febecaf2ccb7913df87c4d68d454'in r['url']for r in n['references']))
  self.assertIn('當羌',names['h0h_wsl_1nf']['additional_names'])
 def test_two_duplicate_envoy_ids_are_retired_from_all_editable_references(self):
  pids={p['id']for p in read('registry/persons.json')['persons']};self.assertFalse(set(OLD)&pids)
  for p in reference_files(R):
   for old in OLD:self.assertNotIn(old,p.read_text(),str(p))
 def test_dayuan_mentions_and_different_missions_remain_explicit(self):
  c=read('corpus/shiji/123.json');p=next(p for p in c['paragraphs']if p['id'].endswith('p023'));self.assertIn('漢既滅越',p['text']);self.assertEqual({m['surface']:m['person_id']for m in p['mentions']if m['surface']in ['柏始昌','呂越人']},{'柏始昌':'11q_2yl_qzt','呂越人':'miw_t0v_k64'})
  ds=[d for d in read('corpus/shiji/116-equivalences.json')['decisions']if d['id'].startswith('eq-shiji116-envoy-')];self.assertEqual(len(ds),2)
  for d in ds:self.assertTrue(d['identity_materialized']);self.assertIn('不同次任務',d['rationale'])
 def test_office_location_and_earlier_residence_are_not_birthplaces(self):
  a=read('corpus/shiji/116-addresses.json')['assertions'];places={x['id']:x for x in a}
  self.assertEqual((places['pa-shiji116-002']['relation'],places['pa-shiji116-002']['place']['source_name']),('service_location','番陽'));self.assertEqual((places['pa-shiji116-003']['relation'],places['pa-shiji116-003']['place']['source_name']),('residence','大夏'))
  for key in ['pa-shiji116-002','pa-shiji116-003']:self.assertIsNone(places[key]['date_expression']);self.assertIsNone(places[key]['place']['modern_identification']);self.assertTrue(all(places[key]['source_term']in e['quote']for e in places[key]['evidence']))
 def test_zhuangqiao_kingship_is_an_attestation_with_unknown_period(self):
  h=next(h for h in read('corpus/shiji/116-titles.json')['holdings']if h['id']=='th-shiji116-019');self.assertEqual((h['person_id'],h['title'],h['mode']),('b1y_l5y_xmz','王','attestation'));self.assertEqual(h['jurisdictions'][0]['source_name'],'滇');self.assertTrue(all(x['status']=='unknown'for x in h['effective_period'].values()));self.assertIn('王滇',h['evidence'][0]['quote'])
 def test_commentary_brother_claim_is_typed_but_not_a_family_edge(self):
  v=self.variant;self.assertEqual(reported_relationship_errors(v,self.para),[]);self.assertFalse(v['adopted']);self.assertEqual(v['reported_relationship']['object_generation_relative_to_subject'],0)
  p=bundle('b1y_l5y_xmz',R);self.assertTrue(any(a['predicate']=='ancestor'and a['object_person_id']=='q8m_d0c_kq3'for a in p['relations']));self.assertFalse(any(a['predicate']=='brother'and a['object_person_id']=='q8m_d0c_kq3'for a in p['relations']))
 def test_commentary_cannot_invert_age_or_promote_unadopted_claim(self):
  for change in ['age','adoption','generation']:
   v=copy.deepcopy(self.variant)
   if change=='age':v['reported_relationship']['older_person_id']='b1y_l5y_xmz'
   elif change=='adoption':v['adopted']=True
   else:v['reported_relationship']['object_generation_relative_to_subject']=-1
   self.assertTrue(reported_relationship_errors(v,self.para),change)
 def test_commentary_subject_and_object_must_match_lemma_and_younger_brother_phrase(self):
  v=copy.deepcopy(self.variant);r=v['reported_relationship'];r['subject_person_id'],r['object_person_id']=r['object_person_id'],r['subject_person_id'];r['older_person_id'],r['younger_person_id']=r['younger_person_id'],r['older_person_id'];self.assertTrue(reported_relationship_errors(v,self.para))
  v=copy.deepcopy(self.variant);v['raw_quote']='synthetic nonmatching quotation';self.assertTrue(reported_relationship_errors(v,self.para))
 def test_late_qing_opinion_keeps_uncertainty_and_unknown_publication_year(self):
  v=next(v for v in self.chapter['annotation']['reported_variants']if v['received_reading']=='常頞');self.assertEqual(v['reported_reading'],'嘗破');ref=v['study_references'][0];self.assertEqual(ref['quote'],'案常頞疑是人姓名');self.assertIsNone(ref['publication_year']);self.assertEqual(ref['opinion_validation'],'not_attempted');self.assertEqual(ref['reported_hanshu_reading'],'常破')
if __name__=='__main__':unittest.main()
