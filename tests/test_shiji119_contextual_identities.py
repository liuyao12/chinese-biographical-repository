import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
class XunliContextualIdentities(unittest.TestCase):
 def test_three_rulers_share_existing_cross_chapter_identities(self):
  expected={'q8m_d0c_kq3':7,'q8m_d0c_kq3_AEA':5,'6di_ywz_ju4_AAA':4}
  ch=read('corpus/shiji/119.json');counts={p:0 for p in expected}
  for paragraph in ch['paragraphs']:
   for m in paragraph['mentions']:
    if m.get('person_id')in counts:
     counts[m['person_id']]+=1;self.assertEqual(paragraph['text'][m['start']:m['end']],m['surface'])
  self.assertEqual(counts,expected)
  decisions=read('corpus/shiji/119-identities.json')['decisions']
  for pid in expected:
   d=next(d for d in decisions if d['person_id']==pid)
   self.assertEqual(d['scope'],'cross_chapter');self.assertGreaterEqual(len(d['chapter_ids']),2)
   self.assertFalse(d['human_reviewed'])
 def test_killer_is_the_existing_unnamed_father_not_a_new_person(self):
  ch=read('corpus/shiji/119.json');p=next(p for p in ch['paragraphs']if p['id'].endswith(':p010'))
  self.assertIn('相追之，乃其父也',p['text']);self.assertIn('殺人者，臣之父也',p['text'])
  for mid in ['c-shiji-119-xunli:m010-0025','c-shiji-119-xunli:m010-0055']:
   m=next(m for m in p['mentions']if m['id']==mid);self.assertEqual((m['surface'],m['person_id'],m['kind']),('殺人者','ufr_eoj_xit','person'))
  relation=next(a for a in read('corpus/shiji/119-assertions.json')['assertions']if a['id']=='a-shiji119-001')
  self.assertEqual((relation['subject_person_id'],relation['object_person_id']),('ufr_eoj_xit_A','ufr_eoj_xit'))
 def test_zheng_zhao_is_not_silently_changed_to_a_different_ruler(self):
  ch=read('corpus/shiji/119.json');p=next(p for p in ch['paragraphs']if p['id'].endswith(':p006'));m=next(m for m in p['mentions']if m['surface']=='鄭昭君');self.assertEqual(m['person_id'],'htl_6mt_8sq')
  d=next(d for d in read('corpus/shiji/119-identities.json')['decisions']if d['id']=='d-shiji119-zheng-ruler-limit')
  self.assertEqual(d['confidence_level'],'inconclusive');ref=d['references'][0];self.assertIn('子産不事昭君',ref['display_quote']);self.assertIn('徐摯',ref['quote']);self.assertIn('徐贄',p['text']);self.assertFalse(ref['image_verified']);self.assertNotIn('preferred_reading',d)
  self.assertEqual(ref['display_quote'],re.sub(r'[\s¶/]','',re.sub(r'<pb:[^>]*>','',ref['quote'])))
 def test_twenty_six_source_years_do_not_supply_absolute_dates(self):
  h=next(h for h in read('corpus/shiji/119-titles.json')['holdings']if h['id']=='th-shiji119-005');d=h['reported_duration'];self.assertEqual((d['value'],d['source_number'],d['source_term'],d['unit']),(26,'二十六','治鄭二十六年','title_year'))
  self.assertEqual(d['counting'],'unspecified_source_years')
  for endpoint in h['effective_period'].values():self.assertIsNone(endpoint['date_expression'])
  self.assertEqual(d['evidence'],h['evidence'])
 def test_retired_ruler_candidates_are_removed_after_reference_migration(self):
  ids={p['id']for p in read('registry/persons.json')['persons']}
  for old in ['1kr_t55_e8m','d1k_jtj_7sy','6r6_00u_xxf']:
   self.assertNotIn(old,ids)
   for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/(old+'.json')).exists())
if __name__=='__main__':unittest.main()
