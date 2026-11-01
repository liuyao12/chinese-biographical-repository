import copy,json,unittest
from pathlib import Path
from scripts import fixed_jin037_qiao_cheng_wuji as f
ROOT=Path(__file__).resolve().parents[1]
class QiaoChengWuji(unittest.TestCase):
 def test_complete_units_and_true_parent(self):
  ch,c,r,w=f.proof(ROOT);self.assertEqual(len(ch['paragraphs']),5);a=next(a for a in w[f.CH[:-5]+'-assertions.json']['assertions']if a['id']=='a-jin037-qiao-father-wuji');self.assertEqual(a['subject_person_id'],r['$wuji']);self.assertEqual(a['object_person_id'],r['$cheng']);self.assertTrue(f.family_valid(a,ROOT));bad=copy.deepcopy(a);bad['object_person_id']=r['$wanggao'];self.assertFalse(f.family_valid(bad,ROOT))
 def test_verbs_are_not_names(self):
  ch,c,r,w=f.proof(ROOT)
  for v in c['negative_verb_spans']:
   p=next(p for p in ch['paragraphs']if p['id']==v['paragraph_id']);self.assertFalse(any(m['start']==v['start']for m in p['mentions']))
 def test_death_year_not_birth_or_grant(self):
  ch,c,r,w=f.proof(ROOT);e=next(e for e in w[f.CH[:-5]+'-life-events.json']['events']if e['person_id']==r['$wuji']);self.assertEqual(e['normalized_date']['year'],350);self.assertEqual(e['date_expression'],'永和六年');self.assertIsNone(ch['annotation']['age_assertions'][0]['birth_year'])

 def test_all_seven_paternal_edges_and_ritual_are_distinct(self):
  ch,c,r,w=f.proof(ROOT);aa=w[f.CH[:-5]+'-assertions.json']['assertions'];self.assertEqual(sum(a['predicate']=='father'for a in aa),8);self.assertEqual(sum(a['predicate']=='ritual_successor_of'for a in aa),1);self.assertTrue(all(f.family_valid(a,ROOT)for a in aa));self.assertTrue(all(a['qualifiers'].get('birth_order',{}).get('ordinal')is None for a in aa));self.assertEqual(r['$wuji'].split('_')[0:3],r['$jin'].split('_')[0:3])
