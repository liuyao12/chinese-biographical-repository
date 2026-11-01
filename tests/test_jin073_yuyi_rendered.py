"""Bounded Jin073 source-owned roles; no global name inference."""
import copy,json,unittest
from pathlib import Path
from scripts import fixed_jin073_yuyi_rendered as f
ROOT=Path(__file__).resolve().parents[1]
class YuyiRenderedSource(unittest.TestCase):
 def test_full_received_unit_and_reciprocal_names(self):
  ch,c,r,w=f.proof(ROOT);self.assertEqual(len(ch['paragraphs']),13);self.assertIn('高敗',ch['paragraphs'][1]['text']);self.assertIn('五呂將軍',ch['paragraphs'][2]['text']);self.assertIn('江[A170]',ch['paragraphs'][11]['text']);self.assertIn('而方之。而方之',ch['paragraphs'][12]['text'])
 def test_pronouns_not_aliases_and_exact_scope(self):
  ch,c,r,w=f.proof(ROOT)
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='pronoun':
     self.assertTrue(f.source_reference(m,p['text']));bad=copy.deepcopy(m);bad['surface']='吾';self.assertFalse(f.source_reference(bad,p['text']))
 def test_caller_owner_loss_refused(self):
  people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']};records=[json.loads(p.read_text())for p in(ROOT/'corpus').glob('*/*.json')];ch,c,r,w=f.proof(ROOT);pid=r['$fangzhi'];people[pid]['evidence']=[];records=[d for d in records if d.get('record_type')!='person_name_component_set' or not any(n.get('chapter_id')==f.CID for n in d.get('records',[]))]
  with self.assertRaises((AssertionError,ValueError)):f.guard_bundle(ROOT,pid,people,records)
 def test_ordinal_and_life_reports_cannot_swap(self):
  ch,c,r,w=f.proof(ROOT);a=copy.deepcopy(w[f.CH[:-5]+'-assertions.json']['assertions'][1]);a['qualifiers']['birth_order']['ordinal']=1;self.assertFalse(f.family_valid(a,ROOT));age=copy.deepcopy(ch['annotation']['age_assertions'][2]);age['age_context']={'kind':'at_death','life_event_id':'x'};self.assertFalse(f.age_valid(age,ch,ROOT))

 def test_literal_surname_and_courtesy_name_not_guessed(self):
  ch,c,r,w=f.proof(ROOT);names=w[f.CH[:-5]+'-name-components.json']['records'];wrong=copy.deepcopy(next(n for n in names if n['id']=='name-jin073-yuyi-yi'));wrong['surname']='梁'
  with self.assertRaises(AssertionError):f.validate_surname(wrong,names,{f.CID:ch},{},ROOT)
 def test_no_verb_tong_or_mythical_fangxiang_person(self):
  ch,c,r,w=f.proof(ROOT)
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m.get('source_identity_role')=='tong':self.assertIn('以兄子統為尋陽太守',p['text'][max(0,m['start']-3):m['end']+7])
    self.assertNotEqual(m['surface'],'方相')
 def test_only_explicit_death_has_numeric_year(self):
  ch,c,r,w=f.proof(ROOT);events=w[f.CH[:-5]+'-life-events.json']['events'];self.assertEqual(len(events),8)
  for e in events:
   if e['person_id']==r['$yi']:self.assertEqual(e['normalized_date']['year'],345)
   else:self.assertNotIn('normalized_date',e)
  self.assertEqual([a['age_context']['kind']for a in ch['annotation']['age_assertions']],['during_life','at_death','during_life'])

 def test_hongyuan_reference_layer_and_huangji_unresolved(self):
  ch,c,r,w=f.proof(ROOT);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='洪遠');self.assertEqual(m['person_id'],r['$yinrong']);h=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='黃季');self.assertEqual(h['kind'],'unresolved');self.assertIsNone(h['person_id']);ref=json.loads((ROOT/'source-evidence/jin073-yuyi-ws2296501/hongyuan-quanjinwen-reference.json').read_text());self.assertEqual(ref['material_layer'],'later_compiler_author_headnote_reference');self.assertIn('融字洪远',ref['headnote_original_quote'])

 def test_jiang_lacuna_identity_is_separate_from_unknown_glyph(self):
  ch,c,r,w=f.proof(ROOT);p=ch['paragraphs'][11];m=next(m for m in p['mentions']if m['surface']=='江[A170]');self.assertEqual(m['kind'],'person');self.assertEqual(m['person_id'],r['$jiangbin']);self.assertTrue(f.source_lacuna_reference(m,p['text']));self.assertIsNone(m['source_surface_lacuna']['resolved_original_grapheme']);people={a['id']:a for a in json.loads((ROOT/'registry/persons.json').read_text())['persons']};self.assertFalse(any(m['id']in a['mention_ids']for a in people[r['$jiangbin']]['aliases']));self.assertTrue(any(e['mention_id']==m['id']for e in people[r['$jiangbin']]['evidence']));bad=copy.deepcopy(m);bad['source_surface_lacuna']['resolved_original_grapheme']='虨';self.assertFalse(f.source_lacuna_reference(bad,p['text']))

 def test_two_literal_titles_keep_unknown_times(self):
  ch,c,r,w=f.proof(ROOT);rows=w[f.CH[:-5]+'-titles.json']['holdings'];self.assertEqual([(h['title'],h['kind'],h['mode'])for h in rows],[('都亭侯','noble_rank','grant'),('肅','honorific','posthumous_naming')])
  for h in rows:self.assertEqual(h['person_id'],r['$yi']);self.assertIsNone(h['effective_period']['start']['date_expression']);self.assertNotIn('normalized_date',h['effective_period']['start']);self.assertEqual(h['effective_period']['end']['status'],'unknown')
