import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TeachingSources(unittest.TestCase):
 def test_twelve_teacher_assertions_have_explicit_student_and_teacher_anchors(self):
  rows=[]
  for n in ['104','105']:
   c=json.loads((ROOT/f'corpus/shiji/{n}.json').read_text());ps={p['id']:p for p in c['paragraphs']}
   a=json.loads((ROOT/f'corpus/shiji/{n}-assertions.json').read_text())
   for r in a['assertions']:
    if r['predicate']!='teacher':continue
    rows.append(r)
    for e in r['evidence']:
     p=ps[e['paragraph_id']];self.assertIn(r['qualifiers']['source_term'],e['quote'])
     for role in ['subject','object']:
      m=next(m for m in p['mentions'] if m['id']==e[role+'_person_mention_id']);self.assertEqual(m['person_id'],r[role+'_person_id'])
  self.assertEqual(len(rows),12)
 def test_unnamed_yangqing_teacher_and_zibao_are_not_invented(self):
  rows=json.loads((ROOT/'corpus/shiji/105-assertions.json').read_text())['assertions'];rows=[r for r in rows if r['predicate']=='teacher'];self.assertFalse(any(r['subject_person_id']=='1y5_eke_4gl' for r in rows));c=json.loads((ROOT/'corpus/shiji/105.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith('p006'));zibao=next(m['person_id']for m in p['mentions']if m['surface']=='子豹');self.assertFalse(any(r['subject_person_id']==zibao for r in rows))
