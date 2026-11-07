import copy,json,unittest
from pathlib import Path
from scripts.wyd_song051_yixin import state,non_person_component_valid
from scripts.lexical_annotations import non_person_errors
ROOT=Path(__file__).resolve().parents[1]
class AnnotationCorrections(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch,cls.roles,cls.c,cls.docs=state(ROOT);cls.p=next(p for p in cls.ch['paragraphs']if p['id'].endswith(':p019'));cls.m=next(m for m in cls.p['mentions']if m['id'].endswith(':m0172'))
 def test_exact_received_office_component_retains_original_MID(self):
  self.assertEqual(self.m['surface'],'振');self.assertEqual(self.m['kind'],'non_person');self.assertIsNone(self.m['person_id']);self.assertTrue(non_person_component_valid(self.m,self.p['text'],self.ch,ROOT));self.assertEqual(non_person_errors(self.m,self.p['text'],chapter=self.ch,root=ROOT),[])
 def test_wrong_owner_kind_surface_or_position_is_rejected(self):
  for field,value in [('person_id',self.roles['dg_huanzhen']),('kind','person'),('surface','武'),('start',173),('end',174),('human_reviewed',True),('lexical_role','verb')]:
   m=copy.deepcopy(self.m);m[field]=value;self.assertFalse(non_person_component_valid(m,self.p['text'],self.ch,ROOT))
 def test_full_source_root_and_context_are_required(self):
  for ch,root,text in [(None,ROOT,self.p['text']),(self.ch,None,self.p['text']),({},ROOT,self.p['text']),(self.ch,ROOT,'振武將軍')]:self.assertTrue(non_person_errors(self.m,text,chapter=ch,root=root))
  ch=copy.deepcopy(self.ch);ch['source']['raw_sha256']='0'*64;self.assertTrue(non_person_errors(self.m,self.p['text'],chapter=ch,root=ROOT))
 def test_original_six_real_huanzhen_and_no_false_reverse_edges(self):
  mids=[m['id']for p in self.ch['paragraphs']for m in p['mentions']if m.get('person_id')==self.roles['dg_huanzhen']];self.assertEqual(len(mids),6);self.assertNotIn(self.m['id'],mids)
  people=json.loads((ROOT/'registry/persons.json').read_text())['persons'];self.assertFalse(any(self.m['id']in a.get('mention_ids',[])for p in people for a in p.get('aliases',[])));self.assertFalse(any(e.get('mention_id')==self.m['id']for p in people for e in p.get('evidence',[])))
 def test_lushiheng_is_existing_source_seed_and_fixed_primary_courtesy_bridge(self):
  m=next(m for m in self.p['mentions']if m['id'].endswith(':m0004'));self.assertEqual(m['surface'],'陸士衡');self.assertEqual(m['person_id'],self.roles['correction_lushiheng']);d,=self.docs['corpus/songshu/051-wyd1739-annotation-correction-identities.json']['decisions'];self.assertEqual(d['person_id'],m['person_id']);self.assertEqual(d['references'][0]['revision_id'],2605147);self.assertIn('陸機，字士衡',d['references'][0]['quote']);self.assertFalse(d['human_reviewed'])
 def test_no_global_zhen_ban_and_legacy_office_component_stays_strict(self):
  def m(surface,term,role,start=0):return dict(kind='non_person',person_id=None,status='contextual_provisional',surface=surface,start=start,end=start+len(surface),basis_quote=term,lexical_role=role,interpretation_note='synthetic lexical boundary test',reviewer='AI test',human_reviewed=False)
  self.assertEqual(non_person_errors(m('太子','太子太傅','office_title_component'),'太子太傅'),[]);self.assertTrue(non_person_errors(m('太子','太子將軍','office_title_component'),'太子將軍'));self.assertTrue(non_person_errors(m('振','振武將軍','office_title_component'),'振武將軍'))
  self.assertEqual(non_person_errors(m('王','王濟北','verb'),'王濟北'),[]);self.assertEqual(non_person_errors(m('相','數使使相交','reciprocal_adverb',3),'數使使相交'),[])
if __name__=='__main__':unittest.main()
