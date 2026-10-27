"""Source-bound identity qualifications; IDs resolve from native MIDs."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(rel):return json.loads((ROOT/rel).read_text())
def mark(rel,mid):
 return next(m for p in load(rel)['paragraphs']for m in p['mentions']if m['id']==mid)
def decision(mid):
 found=[d for f in (ROOT/'corpus').glob('*/*identities.json')for d in json.loads(f.read_text()).get('decisions',[])if mid in d.get('identification_basis',{}).get('target_mention_ids',[])]
 return next(d for d in found if d['id'].startswith('d-shiji130-remaining11-'))
class RemainingContextIdentityTests(unittest.TestCase):
 def test_sima_ang_source_and_table_share_preserved_qualified_family(self):
  pid=mark('corpus/shiji/130.json','c-shiji-130-taishigong:m002-0146')['person_id']
  self.assertEqual(mark('corpus/shiji/007.json','c-shiji-007-xiangyu:m021-0385')['person_id'],pid)
  table=load('data/historical-tables/shiji-016.json');m=next(m for f in table['fragments']for r in f['rows']for cell in r['cells']for m in cell.get('person_mentions',[])if m['id']=='shiji-016-t2-r002-c18-m000');self.assertEqual(m['person_id'],pid)
  p=next(p for p in load('registry/persons.json')['persons']if p['id']==pid);f=p['family_path'];self.assertEqual(f['generation_distance'],4);self.assertEqual(f['intermediate_person_ids'],[None,None,None]);self.assertEqual(f['status'],'contextual_provisional');self.assertIs(f['human_reviewed'],False)
  q=decision(SIMA_MID)['identity_scope_qualifications'];self.assertIs(q['family_confidence_upgraded'],False);self.assertIs(q['voluntary_surrender_inferred'],False)
 def test_tairen_source_historicity_remains_separate(self):
  a=decision(TAIR1);b=decision(TAIR2);self.assertEqual(a['person_id'],b['person_id']);self.assertEqual(a['prior_source_qualifications'][0]['metadata']['historicity'],'historical_tradition');self.assertEqual(b['prior_source_qualifications'][0]['metadata']['historicity'],'legendary_tradition')
  self.assertIs(a['identity_scope_qualifications']['ten_children_birth_assertions_added'],False)
 def test_dongsheng_context_preference_does_not_authenticate_quotation(self):
  d=decision(DONG);self.assertEqual(d['source_context_confidence'],'medium_high_contextual');self.assertEqual(d['confidence_level'],'moderate');self.assertIs(d['identity_scope_qualifications']['quote_attribution_verified'],False);self.assertIs(d['human_reviewed'],False)
 def test_taicheng_name_is_not_replaced_by_different_event_actor(self):
  d=decision(TAICHENG);q=d['identity_scope_qualifications']['event_alignment'];self.assertIs(q['resolved'],False);self.assertIs(q['actor_reassigned_to_yan'],False)
  self.assertIn('剔成',mark('corpus/shiji/130.json',TAICHENG)['surface'])

SIMA_MID='c-jinshu-001-sima-near-ancestry:p001:m0100'
TAIR1='c-shiji-130-taishigong:m047-0031'
TAIR2='c-shiji-049-waiqi:m001-0071'
DONG='c-shiji-130-taishigong:m009-0028'
TAICHENG='c-shiji-130-taishigong:m050-0051'
