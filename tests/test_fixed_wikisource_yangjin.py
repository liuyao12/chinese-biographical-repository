# coding: utf-8
import unittest,json,copy,hashlib,tempfile
from pathlib import Path
from scripts.fixed_wikisource_units import source_errors,unit_son_count_valid,unit_group_age_bound_valid,unit_numbered_son_valid,biography_former_ming_valid
from scripts.chinese_civil_years import numeral
R=Path(__file__).resolve().parents[1];BASE='corpus/weishu-weishou/058-yangjin'
class YangjinCompleteUnit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/(BASE+'.json')).read_text());cls.a=json.loads((R/(BASE+'-assertions.json')).read_text())['assertions'];cls.ps={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']}
 def test_complete_actual_raw_and_no_duplicate_appraisal(self):
  self.assertEqual(source_errors(self.c,R),[]);self.assertEqual(len(self.c['paragraphs']),26);self.assertEqual(sum(len(p['mentions'])for p in self.c['paragraphs']),235);self.assertEqual(len(self.c['annotation']['modern_collation_reports']),4);self.assertNotIn('shared_appraisal_context',self.c['annotation'])
 def test_cosshift_all_offsets_and_hash_cannot_fake_raw(self):
  c=copy.deepcopy(self.c);p=c['paragraphs'][0]['source_position'];p['raw_start']+=1;p['raw_end']+=1;p['raw_character_offsets']=[v+1 for v in p['raw_character_offsets']];p['projection_sha256']=hashlib.sha256((json.dumps(p['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest();self.assertTrue(source_errors(c,R))
 def test_physical_full_raw_tamper_outside_retained_unit(self):
  with tempfile.TemporaryDirectory(prefix='yangjin-physical-')as tmp:
   root=Path(tmp).resolve();names=[self.c['annotation']['fixed_wikisource_unit_ref'],self.c['source']['raw_path']]
   for rel in names:
    p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);self.assertTrue(p.resolve().is_relative_to(root));p.write_bytes((R/rel).read_bytes())
   self.assertEqual(source_errors(self.c,root),[]);p=root/names[1];p.write_bytes(b' '+p.read_bytes());self.assertTrue(source_errors(self.c,root))
 def test_received_layer_modern_refs_and_whole_unit_not_optional(self):
  for mode in ('omit','ref','note','layer'):
   c=copy.deepcopy(self.c)
   if mode=='omit':c['paragraphs'].pop(10)
   elif mode=='ref':c['annotation']['modern_collation_reports'].pop()
   elif mode=='note':c['paragraphs'][2]['attached_note_to_paragraph_id']='fake'
   else:c['paragraphs'][2]['text_layer']='commentary'
   self.assertTrue(source_errors(c,R),mode)
 def test_six_sons_does_not_invent_named_sons(self):
  a=self.c['annotation']['family_count_reports'][0];self.assertTrue(unit_son_count_valid(a,self.c,R,numeral));self.assertEqual(a['reported_count'],6)
  for key,value in [('reported_count',5),('named_member_person_ids',['invented']),('complete_named_list',True),('parent_person_id','wrong')]:
   b=copy.deepcopy(a);b[key]=value;self.assertFalse(unit_son_count_valid(b,self.c,R,numeral),key)
 def test_explicit_sending_sons_has_source_parent_and_ordinal(self):
  aa=[a for a in self.a if a.get('qualifiers',{}).get('source_clause_binding',{}).get('kind')=='named_parent_sending_numbered_son'];self.assertEqual(len(aa),2)
  for a in aa:
   self.assertTrue(unit_numbered_son_valid(a,self.ps,{self.c['id']:self.c},R))
   for mode in ('parent','number','quote','term'):
    b=copy.deepcopy(a)
    if mode=='parent':b['object_person_id']=b['subject_person_id']
    elif mode=='number':b['qualifiers']['birth_order']['ordinal']+=1
    elif mode=='term':b['qualifiers']['birth_order']['source_term']='第四子'
    else:b['evidence'][0]['quote']='omitted'
    self.assertFalse(unit_numbered_son_valid(b,self.ps,{self.c['id']:self.c},R),mode)
 def test_group_over_sixty_not_exact_or_death_age(self):
  aa=[a for a in self.c['annotation']['age_assertions']if 'received_unit_age_binding'in a];self.assertEqual(len(aa),2)
  for a in aa:
   self.assertTrue(unit_group_age_bound_valid(a,self.c,R,numeral))
   for key,value in [('value',60),('person_id','wrong'),('birth_year',470),('age_context',{'kind':'at_death'})]:
    b=copy.deepcopy(a);b[key]=value;self.assertFalse(unit_group_age_bound_valid(b,self.c,R,numeral),key)
 def test_approaching_thirty_unknown_births_and_no_inherited_death_years(self):
  ages=self.c['annotation']['age_assertions'];near=next(a for a in ages if a.get('source_term')=='年近三十');self.assertIsNone(near['value']);self.assertTrue(all(a['birth_year']is None for a in ages));events=json.loads((R/(BASE+'-life-events.json')).read_text())['events'];self.assertEqual(len(events),11);self.assertEqual([e['normalized_date']['year']for e in events if 'normalized_date'in e],[531]);self.assertTrue(all('normalized_date'not in e for e in events if e['person_id']!=next(e['person_id']for e in events if 'normalized_date'in e)))
 def test_original_name_grant_roles_not_same_paragraph_guess(self):
  name=json.loads((R/(BASE+'-name-components.json')).read_text())['records'][0];p=self.c['paragraphs'][0];self.assertTrue(biography_former_ming_valid(name,p))
  for mode in ('ruler','person','marker','quote'):
   n=copy.deepcopy(name)
   if mode=='ruler':n['former_ming_basis']['ruler_mention_id']=n['person_mention_id']
   elif mode=='person':n['person_id']='wrong'
   elif mode=='marker':n['former_ming_basis']['source_marker_anchor']['surface']='本字'
   else:n['quote']='omitted'
   self.assertFalse(biography_former_ming_valid(n,p),mode)
 def test_contextual_rong_empresses_and_collateral_ancestor(self):
  ps=self.c['paragraphs'];a=[m for m in ps[7]['mentions']if m['surface']=='榮'];self.assertTrue(a);self.assertEqual({m['person_id']for m in a},{'rje_523_lkh'});self.assertTrue(any(m['person_id']=='d52_81d_e8e'for m in ps[9]['mentions']));self.assertTrue(any(m['person_id']=='ad8_il0_mf4'for m in ps[0]['mentions']));self.assertTrue(any(m['person_id']=='e8c_ec1_579'for m in ps[3]['mentions']));self.assertFalse(any(a['subject_person_id']==next(m['person_id']for m in ps[10]['mentions']if m['surface']=='遁')and a['predicate']=='grandfather'for a in self.a))
 def test_source_words_unresolved_kin_and_non_death_phrases_preserved(self):
  t='\n'.join(p['text']for p in self.c['paragraphs']);self.assertIn('薛脩禮',t);self.assertIn('詔聽二萬',t);self.assertIn('年十五六',t);self.assertIn('陷關西',t);self.assertIn('城東十里被殺',t);self.assertTrue(all(n['image_verified']is False for n in self.c['annotation']['modern_collation_reports']))
 def test_titles_posthumous_source_usages_not_lifetime_tenures(self):
  hs=json.loads((R/(BASE+'-titles.json')).read_text())['holdings'];self.assertEqual(len(hs),159);self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in hs));post=[h for h in hs if h['attestations'][0]['usage']=='posthumous_usage'];self.assertTrue(post);self.assertTrue(all(h['mode']=='attestation' and h['effective_period']['start']['status']=='unknown'for h in post));self.assertFalse(any(h['title']=='內典書'for h in hs))
