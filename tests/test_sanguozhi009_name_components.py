import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CaoNameComponents(unittest.TestCase):
 def records(self):return json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']
 def test_given_and_courtesy_names_have_distinct_exact_source_anchors(self):
  chapter=json.loads((ROOT/'corpus/sanguozhi/009-caozhen.json').read_text());ps={p['id']:p for p in chapter['paragraphs']}
  for proposal,ming,zi in [('proposal-sgz009-names-zhen','真','子丹'),('proposal-sgz009-names-shuang','爽','昭伯')]:
   matches=[r for r in self.records()if r.get('source_proposal_id')==proposal];self.assertEqual(len(matches),1);r=matches[0];self.assertEqual((r['surname'],r['ming'],r['zi']),('曹',ming,zi));self.assertFalse(r['human_reviewed']);self.assertIn('字'+zi,r['quote'])
   for field,a in r['component_source_anchors'].items():
    p=ps[a['paragraph_id']];m=next(m for m in p['mentions']if m['id']==a['person_mention_id']);self.assertEqual(m['person_id'],r['person_id']);self.assertLessEqual(m['start'],a['start']);self.assertLessEqual(a['end'],m['end']);self.assertEqual(p['text'][a['start']:a['end']],r[field]);self.assertEqual(a['surface'],r[field])
 def test_prior_independent_cao_shuang_sources_are_retained(self):
  records=self.records();ids={r.get('source_proposal_id')for r in records if r['person_id']=='30k_jzz_tpd_AA'};self.assertTrue({'proposal-wang34-028','proposal-sanguozhi028-wangling-016','proposal-sgz009-names-shuang'}<=ids)
 def test_xiaozhi_is_not_written_into_zi_or_former_given_name(self):
  row=next(r for r in self.records()if r.get('source_proposal_id')=='proposal-sgz009-names-shuang');self.assertEqual(row['zi'],'昭伯');self.assertNotIn('former_ming',row);self.assertNotIn('黙',row['additional_names'])
if __name__=='__main__':unittest.main()
