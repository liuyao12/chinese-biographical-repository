import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUDIT='source-evidence/shiji130-first50-stage2-identity'
def read(rel):return json.loads((ROOT/rel).read_bytes())
class ShijiStage2SourceIdentity(unittest.TestCase):
 def test_all_complete_contexts_and_83_actual_source_endpoints(self):
  review=read(AUDIT+'/complete-context-reading.json');self.assertEqual(len(review['groups']),24);self.assertTrue(review['same_work_parallel_is_not_independent_witness'])
  chapters={d['id']:d for p in(ROOT/'corpus').glob('*/*.json')if(d:=json.loads(p.read_bytes())).get('record_type')=='marked_chapter'};markers={m['id']:(c,p,m)for c in chapters.values()for p in c['paragraphs']for m in p.get('mentions',[])};allmids=[]
  for g in review['groups']:
   allmids+=g['source_MIDs']
   for mid in g['source_MIDs']:
    c,p,m=markers[mid];self.assertEqual(m['person_id'],g['person_id']);self.assertEqual(m['kind'],'person');self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
   for f in g['source_frames']:
    c=chapters[f['dimensions']['id']];self.assertEqual({k:c[k]for k in f['dimensions']},f['dimensions']);self.assertEqual(c['source'],f['source']);p=next(p for p in c['paragraphs']if p['id']==f['paragraph_id']);self.assertEqual(p['text'],f['text']);self.assertEqual(p.get('text_layer'),f['text_layer'])
  self.assertEqual(len(allmids),83);self.assertEqual(len(set(allmids)),83)
 def test_retired_source_roots_are_not_active_or_query_aliases(self):
  people=read('registry/persons.json')['persons'];pids={p['id']for p in people};old=[]
  for f in(ROOT/AUDIT).glob('retirement-*.json'):
   d=json.loads(f.read_bytes());old+=d['retired_person_ids'];self.assertEqual(d['retirement_policy'],'audit_only_not_canonical_not_alias_not_reusable');self.assertIs(d['person_aliases_created'],False)
  self.assertEqual(len(old),26);self.assertEqual(len(set(old)),26);self.assertFalse(pids&set(old));self.assertFalse(any(a['surface']in old for p in people for a in p['aliases']))
 def test_hanfei_expansion_preserves_actual_event_words(self):
  review=read(AUDIT+'/complete-context-reading.json');g=next(g for g in review['groups']if g['identity_decision_id'].endswith('-24'));self.assertEqual(len(g['source_MIDs']),10)
  c6=read('corpus/shiji/006.json');c45=read('corpus/shiji/045.json');c63=read('corpus/shiji/063.json');p13=next(p for p in c6['paragraphs']if p['id'].endswith(':p013'));p34=next(p for p in c45['paragraphs']if p['id'].endswith(':p034'));p24=next(p for p in c63['paragraphs']if p['id'].endswith(':p024'))
  self.assertIn('韓非使秦，秦用李斯謀，留非',p13['text']);self.assertIn('使韓非使秦，秦留非',p34['text']);self.assertIn('李斯使人遺非藥，使自殺',p24['text'])

 def test_prior_source_metadata_is_retained_without_overwriting_keeper(self):
  review=read(AUDIT+'/complete-context-reading.json');decisions=read('corpus/shiji/130-identities.json')['decisions'];count=0
  for g in review['groups']:
   d=next(d for d in decisions if d['id']==g['identity_decision_id']);self.assertEqual(d['prior_source_qualifications'],g['prior_source_qualifications']);count+=len(d['prior_source_qualifications'])
   for q in d['prior_source_qualifications']:
    self.assertTrue(q['source_mention_ids']);self.assertTrue(set(q['source_mention_ids'])<=set(g['source_MIDs']));self.assertIn('label',q['metadata']);self.assertNotIn('id',q['metadata'])
  self.assertEqual(count,26)
  last=review['groups'][-1];self.assertTrue(any('identity_note'in q['metadata']and q['metadata'].get('review')=='ai_provisional'for q in last['prior_source_qualifications']))
