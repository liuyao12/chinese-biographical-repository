import unittest,json,copy,tempfile,xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
from scripts.lexical_annotations import non_person_errors
from scripts.source_non_person_retirement import reservation_ids,REVIEW_PATH,RECEIPT_PATH
from scripts.retired_person_ids import retired_person_ids,assert_not_retired,allocation_conflicts
from scripts.person_ids import allocate_person_id

class SourceNonPersonRetirementTests(unittest.TestCase):
 def setUp(self):
  self.root=Path(__file__).resolve().parents[1];self.chapter=json.loads((self.root/'corpus/shiji/130.json').read_text());self.paragraph=next(p for p in self.chapter['paragraphs']if p['id']=='c-shiji-130-taishigong:p049');self.mark=next(m for m in self.paragraph['mentions']if m['id']=='c-shiji-130-taishigong:m049-0025');self.review=json.loads((self.root/REVIEW_PATH).read_text());self.receipt=json.loads((self.root/RECEIPT_PATH).read_text());self.old=self.review['prior_editorial_record']['id'];self.context={'root':self.root,'chapter':self.chapter,'paragraph':self.paragraph}
 def test_fixed_context_and_literal_components(self):
  self.assertEqual(non_person_errors(self.mark,self.paragraph['text'],self.context),[]);self.assertEqual(self.mark['surface'],'衛頃');self.assertEqual(self.mark['person_id'],None);self.assertEqual([(x['role'],x['surface'])for x in self.mark['components']],[('polity','衛'),('predicate','頃')]);self.assertEqual(self.mark['components'][1]['editorial_reading'],'傾');self.assertFalse(self.mark['human_reviewed'])
 def test_no_context_or_wrong_source_never_accepted(self):
  self.assertTrue(non_person_errors(self.mark,self.paragraph['text']))
  for ctx in [None,[],{'root':self.root,'chapter':[],'paragraph':self.paragraph},{**self.context,'chapter':{**self.chapter,'id':'wrong'}},{**self.context,'chapter':{**self.chapter,'record_type':'not-marked'}}]:self.assertTrue(non_person_errors(self.mark,self.paragraph['text'],ctx))
 def test_wrong_mid_kind_components_and_qualification_rejected(self):
  for field,value in [('id','wrong-mid'),('person_id',self.old),('kind','person'),('lexical_role','verb'),('start',24),('surface','衛傾'),('human_reviewed',0)]:
   m=copy.deepcopy(self.mark);m[field]=value;self.assertTrue(non_person_errors(m,self.paragraph['text'],self.context),field)
  m=copy.deepcopy(self.mark);m['components'].reverse();self.assertTrue(non_person_errors(m,self.paragraph['text'],self.context))
 def test_xml_and_original_text(self):
  tree=ET.parse(self.root/'corpus/shiji/130.xml');p=next(x for x in tree.getroot().iter('p')if x.get('id')==self.paragraph['id']);self.assertEqual(''.join(p.itertext()),self.paragraph['text']);m=next(x for x in p if x.get('id')==self.mark['id']);self.assertEqual(m.tag,'seg');self.assertEqual(m.get('type'),'non-person');self.assertEqual(m.get('subtype'),'polity_predicate');self.assertIsNone(m.get('ref'))
 def test_negative_receipt_not_positive_identity_or_redirect(self):
  self.assertEqual(reservation_ids(self.root,self.root/RECEIPT_PATH,self.receipt),[self.old]);self.assertNotIn('identity_decision_id',self.receipt);self.assertFalse(self.receipt['person_aliases_created']);people=json.loads((self.root/'registry/persons.json').read_text())['persons'];self.assertFalse(any(p['id']==self.old for p in people))
  for field,value in [('record_type','editorial_annotation_rekey_receipt'),('non_person_review_id','wrong'),('review_sha256','0'*64),('retired_person_ids',['zzq_111_222']),('person_aliases_created',0)]:
   r=copy.deepcopy(self.receipt);r[field]=value
   with self.assertRaises(ValueError):reservation_ids(self.root,self.root/RECEIPT_PATH,r)
 def test_reserved_and_real_allocator(self):
  retired=retired_person_ids(self.root);self.assertIn(self.old,retired);self.assertTrue(allocation_conflicts(self.old,retired))
  with self.assertRaises(ValueError):assert_not_retired(self.old,self.root)
  chars=iter(self.old.replace('_','')+'zzq999888')
  with patch('scripts.person_ids.secrets.choice',side_effect=lambda _:next(chars))as pick:self.assertEqual(allocate_person_id(set(),root=self.root),'zzq_999_888');self.assertEqual(pick.call_count,18)
 def test_old_person_api_rejected(self):
  from scripts.person_bundle import load_catalog,bundle
  cat=load_catalog(self.root)
  for policy in [False,True]:
   with self.assertRaises((ValueError,KeyError)):bundle(self.old,self.root,include_provisional=policy,catalog=cat)
 def test_legacy_verb_still_uses_original_two_argument_api(self):
  m={'kind':'non_person','person_id':None,'status':'contextual_provisional','lexical_role':'verb','surface':'王','start':0,'end':1,'basis_quote':'王濟北','interpretation_note':'王為動詞','human_reviewed':False,'reviewer':'AI'};self.assertEqual(non_person_errors(m,'王濟北'),[])
  bad={**m,'person_id':'zzq_111_222'};self.assertTrue(non_person_errors(bad,'王濟北'))

 def test_missing_negative_receipt_blocks_real_allocator_in_temporary_root(self):
  with tempfile.TemporaryDirectory()as directory:
   root=Path(directory);(root/'corpus/shiji').mkdir(parents=True);(root/'corpus/shiji/130.json').write_text(json.dumps({'paragraphs':[{'mentions':[self.mark]}]}))
   with self.assertRaises(ValueError):allocate_person_id(set(),root=root)
