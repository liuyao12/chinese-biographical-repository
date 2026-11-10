"""Fixed WYD051 limited family / WYD005 complete opening phase, with mutable person IDs."""
import copy,json,unittest
from pathlib import Path
from scripts import fixed_wuyingdian_song051_family_phase as m
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog,bundle
from scripts.validation_context import scope
ROOT=Path(__file__).resolve().parents[1]
class FamilyPhase(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch,cls.roles,cls.contract,cls.facts,cls.names=m.context(ROOT);cls.catalog=load_catalog(ROOT)
 def test_current_sources_full_raw_and_partial_scope(self):
  self.assertEqual(m.source_errors(json.loads((ROOT/m.CH).read_bytes()),ROOT),[]);intro=json.loads((ROOT/m.INTRO_CH).read_bytes());self.assertEqual(m.source_errors005(intro,ROOT),[]);self.assertEqual(sum(len(p['mentions'])for p in self.ch['paragraphs']),49);self.assertEqual(sum(len(p['mentions'])for p in intro['paragraphs']),14);self.assertEqual(sum(p['annotation_status']=='pending'for p in self.ch['paragraphs']),40)
 def test_two_reported_two_are_unaccepted(self):
  ds=json.loads((ROOT/m.IDENTITIES).read_bytes())['decisions'];reports=[r for d in ds for r in d.get('source_ordinal_readings',[])];self.assertEqual({r['person_id']for r in reports},{self.roles['yiqing'],self.roles['yizong']})
  for r in reports:self.assertIs(type(r['reported_ordinal']),int);self.assertEqual(r['reported_ordinal'],2);self.assertIsNone(r['accepted_birth_order']);self.assertIsNone(r['scope_interpretation'])
 def test_history_does_not_create_permanent_adoption(self):
  d=next(d for d in json.loads((ROOT/m.IDENTITIES).read_bytes())['decisions']if d['id']=='d-song051-phase1-taizu');h=d['historical_succession_reading'];self.assertEqual([e['event_type']for e in h['events']],['raised_by','ordered_succession','ritual_objection','returned_to_original_line','heir_confirmed']);self.assertTrue(all(e['date_expression']is None and e['current_parent_edge_created']is False for e in h['events']));self.assertFalse(any(a['predicate']=='adoptive_father'and a['subject_person_id']==self.roles['taizu']for a in self.facts['assertions']))
 def test_wendi_named_birth_father_not_caretaker(self):
  a=json.loads((ROOT/m.INTRO_FACTS).read_bytes())['assertions'][0];self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),(self.roles['taizu'],'father',self.roles['gaozu']));self.assertEqual(a['qualifiers']['reported_son_ordinal']['value'],3);self.assertIn('武帝第三子也',a['evidence'][0]['quote'])
 def test_clans_literal_unknown_ming_and_no_mother_inference(self):
  for role,surname in [('tan_taifei','檀'),('cao_taifei','曹')]:
   n=next(n for n in self.names['records']if n['id']=='name-song051-phase1-literal-clan-'+role);self.assertEqual(n['surname'],surname);self.assertIsNone(n['ming']);self.assertEqual(n['clan_style']['kind'],'received_clan_appellation')
  self.assertFalse(any(a['predicate']in('mother','adoptive_mother','spouse')for a in self.facts['assertions']))
 def test_json_comparator_preserves_types(self):
  for a,b in [((),()),([],()),((),[]),(True,1),(0,False),(float('nan'),float('nan')),({1:'x'},{1:'x'})]:self.assertFalse(m.same(a,b))
  self.assertTrue(m.same({'x':[1,False,None]},{'x':[1,False,None]}))
 def test_source_body_flag_or_nearest_ruler_cannot_change(self):
  c=json.loads((ROOT/m.CH).read_bytes());c['paragraphs'][0]['mentions']=tuple(c['paragraphs'][0]['mentions']);self.assertTrue(m.source_errors(c,ROOT));c=json.loads((ROOT/m.CH).read_bytes());c['annotation']['human_reviewed']=0;self.assertTrue(m.source_errors(c,ROOT));c=json.loads((ROOT/m.INTRO_CH).read_bytes());mark=next(m for p in c['paragraphs']for m in p['mentions']if m['surface']=='上');mark['person_id']=self.roles['jinandi'];self.assertTrue(m.source_errors005(c,ROOT))
 def test_actual_family_and_bundle_keep_biological_and_adoptive_separate(self):
  sm,_=load_assemblies(ROOT,self.catalog);gui=sm[self.roles['gui_zong_brother']];self.assertEqual(gui['parent_person_id'],self.roles['yibin']);self.assertEqual(gui['parent_connection']['type'],'shared_father_through_sibling')
  with scope(ROOT):b=bundle(self.roles['yiqing'],root=ROOT,include_provisional=True,catalog=self.catalog)
  self.assertTrue(any(a['predicate']=='father'and a['object_person_id']==self.roles['daolian']for a in b['relations']));self.assertTrue(any(a['predicate']=='adoptive_father'and a['object_person_id']==self.roles['daogui']for a in b['relations']));self.assertTrue(any(n.get('surname')=='劉'and n.get('ming')=='義慶'for n in b['name_components']))
if __name__=='__main__':unittest.main()
