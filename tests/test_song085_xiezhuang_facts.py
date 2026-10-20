# coding: utf-8
"""Source-local facts and guarded 元年 continuation; no private paths/exports."""
from pathlib import Path
import copy,json,sys,unittest,importlib.util
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.validate_corpus import normalized_date_errors,source_age_number
from scripts.relative_regnal_year import relative_regnal_year_valid
from scripts.unassumed_appointments import unassumed_appointment_valid
from scripts.person_bundle import load_catalog,bundle
J=lambda p:json.loads(p.read_text());CH=J(ROOT/'corpus/songshu/085-xiezhuang.json');A=CH['annotation'];H=J(ROOT/'corpus/songshu/085-xiezhuang-titles.json')['holdings'];EV=J(ROOT/'corpus/songshu/085-xiezhuang-life-events.json')['events'];N=[x for x in J(ROOT/'data/corpus/profile-names.json')['records']if str(x.get('id','')).startswith('name-song085-f13-')];P=[x for x in J(ROOT/'data/research/early-medieval-family-pending.json')['records']if x['id'].startswith('pending-song085-f13-')]
def same():return copy.deepcopy(next(h for h in H if h['title']=='吏部尚書'and h['attestations'][0]['date_expression']=='其年')['effective_period']['start']['normalized_date'])
class XiezhuangFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.cat=load_catalog(ROOT)
 def test_scoped_record_counts(self):self.assertEqual((len(H),len(EV),len(N),len(P)),(75,2,32,15));self.assertEqual(len(A['age_assertions']),2);self.assertEqual(len(A['title_proposals']),2)
 def test_source_and_ner_not_changed(self):
  units=J(ROOT/'tests/fixtures/song085-xiezhuang/units.json');self.assertEqual([u['text']for u in units],[p['text']for p in CH['paragraphs']]);self.assertEqual(sum(len(p['mentions'])for p in CH['paragraphs']),193)
 def test_names_not_silent_glyph_conversion(self):
  x=next(n for n in N if n['person_id']=='bst_iv3_2wx');self.assertEqual((x['surname'],x['ming'],x['zi']),('謝','莊','希逸'));self.assertTrue(any(n['surname']=='栁'and n['ming']=='元景'for n in N));self.assertTrue(any(n['ming']=='㪍'for n in N));self.assertFalse(any(n.get('ming')=='君章'for n in N))
 def test_unknown_surnames_and_source_appellations(self):
  self.assertTrue(all(n['surname']is None for n in N if n.get('title')in ('始興王','隨王','廬陵王','新安王')));self.assertTrue(any(n['additional_names']==['宏微']and n['ming']is None for n in N));self.assertTrue(any(n['additional_names']==['管仲']and n['ming']is None for n in N))
 def test_no_inferred_birth_or_death_closure(self):
  self.assertTrue(all(a['birth_year']is None for a in A['age_assertions']));self.assertEqual(sorted(a['value']for a in A['age_assertions']),[7,46]);self.assertFalse(any(e['event_type']=='birth'for e in EV));self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in H if h['title']!='吏部尚書'));self.assertEqual(next(e for e in EV if e['person_id']=='bst_iv3_2wx')['normalized_date']['year'],466)
 def test_retrospective_death_not_current_accession_year(self):
  e=next(e for e in EV if e['person_id']!='bst_iv3_2wx');self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e)
 def test_future_and_ancestral_ages_pending(self):
  x=next(x['proposal']for x in P if x['proposal']['kind']=='future_reported_age');self.assertEqual(x['reported_value'],35);self.assertIsNone(x['normalized_year']);self.assertEqual(sum(x['proposal']['kind']=='unnamed_ancestral_age_report'for x in P),3)
 def test_unassumed_only_preceding_two_posts(self):
  self.assertEqual({x['title']for x in A['title_proposals']},{'長史','臨淮太守'});self.assertTrue(all(unassumed_appointment_valid(x,CH)for x in A['title_proposals']));bad=copy.deepcopy(A['title_proposals'][1]);p=CH['paragraphs'][12];s=p['text'].index('吴郡太守');bad.update(title='吴郡太守',role_anchor={'paragraph_id':p['id'],'start':s,'end':s+4,'surface':'吴郡太守'});self.assertFalse(unassumed_appointment_valid(bad,CH))
 def test_wujun_grant_not_attested_arrival(self):
  x=next(h for h in H if h['title']=='吴郡太守');self.assertEqual(x['mode'],'grant');self.assertNotIn('service_realization',x);self.assertTrue(any(x['proposal']['kind']=='unrealized_reassignment_and_ambiguous_previous_office'for x in P))
 def test_descendant_not_zhuang_posthumous_jinzi(self):
  self.assertFalse(any(h['person_id']=='bst_iv3_2wx'and h['mode']=='posthumous_grant'and h['title']=='金紫光禄大夫'for h in H));q=next(x for x in P if x['proposal']['kind']=='posthumous_grant_recipient_after_descendant_transition');self.assertEqual(set(q['person_ids']),{'bst_iv3_2wx','bst_iv3_2wx_A'});self.assertIsNone(q['proposal']['normalized_year'])
 def test_quoted_ancient_offices_not_song_appointments(self):
  xs=[h for h in H if h['person_id']in ('zus_do8_z1q','ufz_ayn_ylh')];self.assertTrue(xs);self.assertTrue(all(h['mode']=='attestation'and h['attestations'][0]['usage']=='retrospective'and h['attestations'][0]['date_expression']is None for h in xs));self.assertTrue(any(x['proposal'].get('person_id')=='56f_8f7_e9f'for x in P))
 def test_exact_anchors_and_normalized_dates(self):
  ps={p['id']:p for p in CH['paragraphs']}
  for h in H:
   for a in h['attestations']:self.assertEqual(ps[a['paragraph_id']]['text'][a['start']:a['end']],a['surface'])
   for obj in [*h['attestations'],*h['effective_period'].values()]:
    if 'normalized_date'in obj:self.assertEqual(normalized_date_errors(obj['normalized_date'],{CH['id']:CH}),[])
 def test_ten_calendar_expressions_years(self):
  got={(a['paragraph_id'],a['date_expression'],a['normalized_date']['year'])for h in H for a in h['attestations']if 'normalized_date'in a};self.assertIn(('c-songshu-085-xiezhuang:p008','其年',454),got);self.assertIn(('c-songshu-085-xiezhuang:p010','三年',459),got);self.assertIn(('c-songshu-085-xiezhuang:p013','六年',462),got);self.assertEqual(next(h for h in H if h['title']=='吏部尚書'and h['attestations'][0]['date_expression']=='其年')['effective_period']['end']['normalized_date']['year'],456)
 def test_only_current_selection_office_removed(self):
  xs=[h for h in H if h['effective_period']['end']['status']=='source_event'];self.assertEqual(len(xs),2);self.assertTrue(all(x['person_id']=='bst_iv3_2wx'and x['title']=='吏部尚書'for x in xs));self.assertTrue(all(x['person_id']!=''+J(ROOT/'tests/fixtures/song085-xiezhuang/ids.json')['new']['張竒']for x in xs))
 def test_pending_double_index(self):
  d=J(ROOT/'data/research/early-medieval-family-pending.json')
  for r in P:
   for pid in r['person_ids']:self.assertIn(r['id'],d['person_index'][pid])
 def test_memory_bundle_contains_facts_no_export(self):
  b=bundle('bst_iv3_2wx',root=ROOT,catalog=self.cat,include_provisional=True);self.assertTrue(any(h['id'].startswith('th-song085-f13-')for h in b['title_holdings']));self.assertTrue(any(n.get('id','').startswith('name-song085-f13-')for n in b['name_components']));self.assertTrue(any(e['id'].startswith('le-song085-f13-')for e in b['life_events']))
class RegnalYuanGuards(unittest.TestCase):
 def test_yuan_same_year_now_valid_legacy_rejected(self):
  d=same();self.assertTrue(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}));p=ROOT/'tests/fixtures/song085-facts/relative_before.py';spec=importlib.util.spec_from_file_location('legacy_relative',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);self.assertFalse(m.relative_regnal_year_valid(d,source_age_number))
 def test_yuan_is_never_age_number(self):self.assertIsNone(source_age_number('元'))
 def test_wrong_year(self):
  d=same();d['year']=d['era_year']=455;self.assertTrue(normalized_date_errors(d,{CH['id']:CH}))
 def test_yuan_requires_explicit_biographical_scope(self):
  d=same();d.pop('narrative_era_scope');self.assertFalse(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}))
 def test_cross_ruler(self):
  d=same();d['narrative_era_scope']['event_ruler_person_id']='yqp_nlb_p1p_AC';self.assertFalse(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}))
 def test_cross_version(self):
  d=same();d['narrative_era_scope']['source_commit']='wrong';self.assertFalse(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}))
 def test_skipped_body(self):
  d=same();d['narrative_era_scope']['paragraph_ids'].pop(1);self.assertFalse(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}))
 def test_wrong_raw_line(self):
  d=same();d['narrative_era_scope']['full_paragraphs'][0]['source_position']['first_line']+=1;self.assertFalse(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}))
 def test_wrong_unit_subject(self):
  d=same();d['narrative_era_scope']['unit_subject_person_id']='56f_8f7_e9f';self.assertFalse(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}))
 def synthetic(self,kind):
  # Explicitly synthetic equal-length mutations; never written to corpus/exports.
  d=same();ch=copy.deepcopy(CH);p=ch['paragraphs'][7];p['text']='明年'+p['text'][2:];d['source_expression']='明年';d['year']=d['era_year']=455;d['regnal_year_mapping'].update(year_offset=1,target_regnal_year=2);d['relative_year_reference']['source_term']='明年';d['original_quote']=p['text'];d['evidence'][-1]['quote']=p['text'];d['narrative_era_scope']['event_date_anchor']['surface']='明年'
  if kind=='era':ch['paragraphs'][6]['text']='大明元年'+ch['paragraphs'][6]['text'][4:]
  if kind=='ruler':
   q=ch['paragraphs'][6];q['text']='文帝'+q['text'][2:];q['mentions'].append({'id':'synthetic-other-ruler','start':0,'end':2,'surface':'文帝','kind':'person','person_id':'3bh_k4m_fg4'})
  for row in d['narrative_era_scope']['full_paragraphs']:row['quote']=next(x['text']for x in ch['paragraphs']if x['id']==row['paragraph_id'])
  return d,ch
 def test_yuan_next_year_scoped_positive(self):
  d,ch=self.synthetic(None);self.assertTrue(relative_regnal_year_valid(d,source_age_number,{ch['id']:ch}))
 def test_next_year_cannot_cross_era(self):
  d,ch=self.synthetic('era');self.assertFalse(relative_regnal_year_valid(d,source_age_number,{ch['id']:ch}))
 def test_next_year_cannot_cross_ruler(self):
  d,ch=self.synthetic('ruler');self.assertFalse(relative_regnal_year_valid(d,source_age_number,{ch['id']:ch}))
 def test_unmodeled_cinian_not_silently_accepted(self):
  d=same();d['relative_year_reference']['source_term']='次年';d['source_expression']='次年';self.assertFalse(relative_regnal_year_valid(d,source_age_number,{CH['id']:CH}))
if __name__=='__main__':unittest.main()
