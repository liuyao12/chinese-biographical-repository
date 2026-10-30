"""The retyped anchors retain exact source positions and registry evidence."""
import copy,json,unittest
from pathlib import Path
from scripts.snapshot_test_expectations import ROWS,current_snapshot,historical_snapshot
R=Path(__file__).resolve().parents[1]
class StandaloneZhiSnapshotContract(unittest.TestCase):
 def test_exact_338_source_anchors_and_reverse_evidence(self):
  self.assertEqual(len(ROWS),338)
  people={p['id']:p for p in json.loads((R/'registry/persons.json').read_bytes())['persons']};chapters={}
  for mid,row in ROWS.items():
   if row['path'] not in chapters:chapters[row['path']]=json.loads((R/row['path']).read_bytes())
   ch=chapters[row['path']];p=next(p for p in ch['paragraphs'] if p['id']==row['paragraph_id']);m=next(m for m in p['mentions'] if m['id']==mid)
   self.assertEqual(p['text'],row['text']);self.assertEqual(m,row['mention']);self.assertEqual(p['text'][m['start']:m['end']],'之');self.assertEqual(m['kind'],'pronoun')
   person=people[m['person_id']];self.assertTrue(any(e.get('mention_id')==mid and e.get('quote')=='之' for e in person['evidence']));self.assertFalse(any(mid in a.get('mention_ids',[]) for a in person['aliases']))
 def test_only_explicit_mids_and_standalone_glyph_are_normalized(self):
  row=copy.deepcopy(next(iter(ROWS.values()))['mention']);old=historical_snapshot(row);self.assertEqual(old['kind'],'person');self.assertEqual(current_snapshot(old),row)
  for change in [{'id':'unregistered-mid'},{'surface':'王羲之'}]:
   value=dict(old,**change);self.assertEqual(current_snapshot(value),value)
  value=dict(old,start=old['start']+1)
  with self.assertRaises(AssertionError):current_snapshot(value)

 def test_split_xuxianzhi_is_name_fragment_not_pronoun(self):
  c=json.loads((R/'corpus/songshu/044-wyd1739.json').read_bytes());ps={p['id'].split(':')[-1]:p for p in c['paragraphs']};self.assertTrue(ps['p007']['text'].endswith('晦同産以下羡'));self.assertTrue(ps['p008']['text'].startswith('之諸姪咸無所染'))
  m=next(m for m in ps['p008']['mentions'] if m['id'].endswith(':m0000'));self.assertEqual(m['kind'],'person');self.assertEqual(m['person_id'],'4y6_myv_ojh');self.assertEqual(m['surface'],'之')
