# coding: utf-8
import unittest,json,copy,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.person_bundle import bundle,load_catalog
from scripts.era_only_dates import valid
from scripts.validate_corpus import normalized_date_errors,source_age_number
R=ROOT;P=ROOT/'tests/fixtures/connected-facts';J=lambda p:json.loads(p.read_text());read=J
OPS=J(P/'facts.json')['operations'];SNAP=J(P/'sources.json')
def records(op):
 d=J(ROOT/op['path'])
 for key in op['array'].split('.'):d=d[key]
 return d
CAT=load_catalog(ROOT);CS={d['id']:d for f in (ROOT/'corpus').rglob('*.json') if (d:=J(f)).get('record_type')=='marked_chapter'}
QI=next(e for e in J(ROOT/'corpus/nanqishu/034-yugaozhi-life-events.json')['events'] if e['id']=='le-yu8-qi-death')['normalized_date'];PIDS=['4qr_wrk_3vd_DDBB','719_b25_cc3_AA']
class YuConnectedFacts(unittest.TestCase):
 def test_ai_review_does_not_claim_human_review(self):
  assemblies=J(ROOT/'registry/family-assemblies.json')['assemblies']
  member=next(m for a in assemblies for m in a['members'] if m['person_id']==PIDS[0])
  self.assertEqual(member['parent_connection']['type'],'shared_father_through_sibling')
  self.assertIs(member['parent_connection']['human_reviewed'],False)
  data=bundle(PIDS[0],root=ROOT,catalog=CAT,include_provisional=True)
  self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']==PIDS[0] for a in data['relations']))
 def test_exact_source_and_formal_records(self):
  for rel in ['corpus/songshu/053-yu-dengzhi.json','corpus/nanqishu/034-yugaozhi.json']:
   d=J(ROOT/rel)
   for key,value in SNAP[rel].items():self.assertEqual(d[key],value)
  for op in OPS:
   if op['packet']=='yu':
    by={a['id']:a for a in records(op)}
    for a in op['append']:self.assertEqual(by[a['id']],a)
 def test_pending_unassumed_patron_and_memory_bundles(self):
  by={r['id']:r for r in J(ROOT/'data/research/early-medieval-family-pending.json')['records']}
  expected=J(P/'facts.json')['pending_append']
  for r in expected:self.assertEqual(by[r['id']],r)
  pending=next(r for r in expected if r['proposal'].get('patron_person_id'));self.assertEqual(pending['proposal']['patron_person_id'],'e9f_a95_f00')
  for pid,year in zip(PIDS,[450,491]):
   d=bundle(pid,root=ROOT,catalog=CAT,include_provisional=True);self.assertEqual(d['canonical_person_id'],pid)
   es=[e for e in d['life_events'] if e['id'].startswith('le-yu8-')];self.assertEqual(len(es),1);self.assertEqual(es[0]['normalized_date']['year'],year)
 def test_original_quote_mismatch_rejected(self):
  d=copy.deepcopy(QI);d['original_quote']+='偽';self.assertFalse(valid(d,source_age_number,CS))
 def test_unassumed_and_unapproved_not_holdings(self):
  hs=[h for f in (ROOT/'corpus').rglob('*-titles.json')for h in J(f)['holdings']if h['id'].startswith('th-yu8-')];self.assertFalse(any(h['title']in ['尚書度支郎','驃騎主簿','丹陽尹']for h in hs));self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in hs));self.assertFalse(any(h['title']=='侍中'and h['person_id']==PIDS[1]and h['mode']=='grant'for h in hs))

 def test_two_deaths_ages_no_birth_no_burial(self):
  for book,path,year,age in [('song','songshu/053-yu-dengzhi',450,63),('qi','nanqishu/034-yugaozhi',491,51)]:
   es=J(R/f'corpus/{path}-life-events.json')['events'];e=next(e for e in es if e['id']==f'le-yu8-{book}-death');self.assertEqual(e['normalized_date']['year'],year);self.assertEqual(e['normalized_date']['calendar'],'chinese_civil');d=J(R/f'corpus/{path}.json');a=next(a for a in d['annotation']['age_assertions']if a['id']==f'age-yu8-{book}-death');self.assertEqual(a['value'],age);self.assertIsNone(a['birth_year']);self.assertEqual(a['age_context']['life_event_id'],e['id'])

 def test_era_only_positive(self):self.assertTrue(valid(QI,source_age_number,CS));self.assertEqual(normalized_date_errors(QI,CS),[])

 def test_era_only_negative_year_and_subject(self):
  for key,value in [('year',492),('era_only_context',dict(QI['era_only_context'],subject_person_id=PIDS[0]))]:
   d=copy.deepcopy(QI);d[key]=value;self.assertFalse(valid(d,source_age_number,CS))

 def test_era_only_negative_gap_revision_and_other_era(self):
  for change in ['gap','revision','era']:
   cs=copy.deepcopy(CS);ch=cs['c-nanqishu-034-yugaozhi'];p=next(p for p in ch['paragraphs'] if p['id']==QI['era_only_context']['antecedent_paragraph_id']);q=next(p for p in ch['paragraphs'] if p['id']==QI['era_only_context']['event_paragraph_id'])
   if change=='gap':q['source_position']['first_line']+=2
   if change=='revision':q['source_position']['revision_id']+=1
   if change=='era':p['text']=p['text'].replace('永明中','建元中')
   self.assertFalse(valid(QI,source_age_number,cs),change)

 def test_no_era_midpoint_or_birth_inference(self):
  self.assertEqual(QI['year'],491);self.assertEqual(QI['regnal_year_mapping']['regnal_year'],9);self.assertEqual(QI['era_only_context']['era_expression'],'永明中');self.assertNotIn('birth_year',QI)

