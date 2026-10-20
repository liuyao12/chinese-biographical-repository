import copy,json,re,unittest
from pathlib import Path
from scripts.person_bundle import bundle,validate_courtesy_name,validate_former_given_name,validate_name_component_alternatives
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class XiangruCommentaryNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.names={n['person_id']:n for n in read('data/corpus/profile-names.json')['records']}
 def test_xiangru_explicit_current_form_courtesy_and_early_name(self):
  n=self.names['usb_lgr_ksa'];self.assertEqual((n['surname'],n['ming'],n['zi'],n['former_ming']),('司馬','相如','長卿','犬子'));self.assertEqual(n['additional_names'],['長卿','犬子']);self.assertIn('故其親名之曰犬子',n['quote']);self.assertIn('更名相如',n['quote']);self.assertIsNone(n['title']);validate_courtesy_name(n);validate_former_given_name(n)
 def test_former_name_cannot_be_same_as_current_courtesy_or_unsourced(self):
  n=self.names['usb_lgr_ksa']
  for former in ['相如','長卿',None,'',' 犬子']:
   x=copy.deepcopy(n);x['former_ming']=former
   with self.assertRaises(ValueError):validate_former_given_name(x)
  x=copy.deepcopy(n);x['ming']=None
  with self.assertRaises(ValueError):validate_former_given_name(x)
 def test_former_name_and_renaming_must_be_in_same_cited_context(self):
  x=copy.deepcopy(self.names['usb_lgr_ksa']);x['quote']='故其親名之曰犬子。';x['references']=[{'quote':'更名相如。'}]
  with self.assertRaises(ValueError):validate_former_given_name(x)
  x['quote']='此為合成別名犬子。更名相如。';x['references']=[]
  with self.assertRaises(ValueError):validate_former_given_name(x)
 def test_zhuangji_default_and_xuguang_courtesy_claim_are_separate(self):
  n=self.names['g8d_9kf_uqg'];self.assertEqual((n['title'],n['surname'],n['ming']),('夫子','莊','忌'));self.assertNotIn('zi',n);self.assertEqual(n['additional_names'],['嚴忌']);self.assertIn('避諱',n['note']);a=n['component_alternatives'][0];self.assertEqual(a['components'],{'surname':None,'ming':'忌','zi':'夫子'});self.assertEqual(a['status'],'source_claim_not_selected');self.assertEqual(a['source_terms'],{'ming':'名忌','zi':'字夫子'});validate_name_component_alternatives(n)
 def test_alternative_preserves_fixed_witness_and_range_fingerprint(self):
  a=self.names['g8d_9kf_uqg']['component_alternatives'][0];ref=a['reference'];self.assertIn(ref['source_commit'],ref['url']);self.assertEqual(ref['source_blob_sha'],'ccded97eee2542083010172d857d6251a09a126c');self.assertRegex(ref['response_sha256'],r'^[0-9a-f]{64}$');self.assertEqual(ref['response_extent'],{'first_line':1,'last_line':100,'partial_file':True});self.assertIn('名忌字夫子',re.sub(r'[()/¶\s]','',ref['raw_quote']));self.assertFalse(ref['image_verified'])
 def test_alternative_cannot_silently_become_selected_or_forge_source_words(self):
  for key,value in [('status','selected'),('source_terms',{'ming':'名忌','zi':'字錯'})]:
   x=copy.deepcopy(self.names['g8d_9kf_uqg']);x['component_alternatives'][0][key]=value
   with self.assertRaises(ValueError):validate_name_component_alternatives(x)
 def test_lin_note_adds_zhao_context_without_independent_vote_claim(self):
  d=next(d for d in read('corpus/shiji/117-equivalences.json')['decisions']if d['id']=='eq-shiji117-opening-linxiangru');self.assertEqual(d['confidence_level'],'moderate');self.assertEqual(d['references'][0]['quote'],'六國時趙人也');self.assertIn('不當獨立史事票數',d['rationale']);self.assertIn('六國時趙人也',d['references'][0]['raw_quote']);self.assertFalse(d['human_reviewed'])
 def test_person_source_bundle_carries_machine_readable_name_fields(self):
  b=bundle('usb_lgr_ksa',R);n=next(n for n in b['name_components']if n['person_id']=='usb_lgr_ksa');self.assertEqual(n['zi'],'長卿');self.assertEqual(n['former_ming'],'犬子');self.assertEqual(n['work_id'],'w-shiji');self.assertEqual(n['chapter_id'],'c-shiji-117-xiangru');self.assertIn('source_id',n)
if __name__=='__main__':unittest.main()
