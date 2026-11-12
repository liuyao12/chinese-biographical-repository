import json
import unittest
from pathlib import Path
from scripts.wyd_song051_p018 import assertion_records, name_components, title_uses, markers
ROOT=Path(__file__).resolve().parents[1]
CID='c-songshu-051-wyd1739-zongshi'
class Song051Boundary(unittest.TestCase):
 def setUp(self):
  self.chapter=json.loads((ROOT/'corpus/songshu/051-wyd1739.json').read_text())
  self.p19=next(p for p in self.chapter['paragraphs']if p['id'].endswith(':p019'))
 def test_p019_name_zi_and_two_labeled_literary_titles(self):
  for mid,start,end,surface,pid in [('m0068',90,92,'道規','3qs_nqa_ioa_AAC'),('m0069',93,95,'道則','3qs_nqa_ioa_AAC'),('m0070',95,97,'高祖','3qs_nqa_ioa_AAA'),('m0071',106,108,'高祖','3qs_nqa_ioa_AAA')]:
   marker=next(m for m in self.p19['mentions']if m['id']==self.p19['id']+':'+mid)
   self.assertEqual((marker['start'],marker['end'],marker['surface'],marker['person_id']),(start,end,surface,pid))
   self.assertEqual(self.p19['text'][start:end],surface)
  record,=name_components(ROOT)['records']
  self.assertEqual((record['person_id'],record['ming'],record['zi']),('3qs_nqa_ioa_AAC','道規','道則'))
  self.assertEqual(record['source_zi_binding']['surface'],'字道則')
  titles=[u for u in title_uses(self.chapter)if u['id'].startswith('tu-song051-p019-gaozu')]
  self.assertEqual({u['person_mention_id'].rsplit(':',1)[-1]for u in titles},{'m0070','m0071'})
 def test_daogui_is_source_attested_younger_brother_of_liuyu(self):
  a=next(a for a in assertion_records(ROOT)if a['id']=='a-song051-p019-daogui-younger-brother-of-liuyu')
  self.assertEqual((a['subject_person_id'],a['object_person_id'],a['qualifiers']['subject_relative_age']),('3qs_nqa_ioa_AAC','3qs_nqa_ioa_AAA','younger'))
  ev,=a['evidence'];self.assertEqual(ev['subject_person_mention_id'],self.p19['id']+':m0068');self.assertEqual(ev['object_person_mention_id'],self.p19['id']+':m0070')
 def test_registry_reverse_refs_and_public_person_bundles(self):
  registry={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  for pid,mid,surface in [('3qs_nqa_ioa_AAC',self.p19['id']+':m0068','道規'),('3qs_nqa_ioa_AAC',self.p19['id']+':m0069','道則'),('3qs_nqa_ioa_AAA',self.p19['id']+':m0070','高祖'),('3qs_nqa_ioa_AAA',self.p19['id']+':m0071','高祖')]:
   person=registry[pid]
   self.assertTrue(any(e.get('mention_id')==mid and e.get('quote')==surface for e in person['evidence']))
   if surface not in ('高祖',):self.assertTrue(any(a['surface']==surface and mid in a['mention_ids']for a in person['aliases']))
  profile=json.loads((ROOT/'data/corpus/profiles/3qs_nqa_ioa_AAC.json').read_text())
  self.assertTrue(any(n['id']=='name-song051-p019-daogui-zi' and n.get('zi')=='道則'for n in profile['name_components']))
  self.assertTrue(any(u['id']=='tu-song051-p019-linchuan-liewuwang'for u in profile['source_title_uses']))
 def test_contract_mentions_match_exported_chapter(self):
  contract=markers(ROOT)
  for row in contract:
   if row['paragraph_id'].endswith(':p019'):
    p=next(p for p in self.chapter['paragraphs']if p['id']==row['paragraph_id'])
    self.assertIn(row['marker'],p['mentions'])
    self.assertEqual(p['text'][row['marker']['start']:row['marker']['end']],row['marker']['surface'])
if __name__=='__main__':unittest.main()
