# coding: utf-8
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def para(n,k):return next(p for p in load('corpus/shiji/'+n+'.json')['paragraphs']if p['id'].endswith(':p'+str(k).zfill(3)))
def cells():return {c['id']:c for f in load('data/historical-tables/shiji-020.json')['fragments']for row in f['rows']for c in row['cells']}
class WeiFinalLinks(unittest.TestCase):
 def test_gonggao_is_tuidang_without_fabricated_generation(self):
  p=para('111',39);self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='弓高侯'),'l9e_fbr_36a_*AB');a=next(a for a in load('corpus/shiji/111-assertions.json')['assertions']if a['id']=='a-shiji111-028');self.assertEqual(a['predicate'],'ancestor');self.assertEqual(a['object_person_id'],'l9e_fbr_36a_*AB');self.assertEqual(a['qualifiers']['source_term'],'弓高侯庶孫');self.assertNotIn('generation_distance',a['qualifiers']);self.assertIn('庶孫',p['text'])
 def test_two_resolved_titles_and_cross_chapter_events(self):
  for k,s,pid in [(33,'太后','6d6_eg1_o3a_A'),(41,'樓船將軍','jk8_8gt_vmi')]:
   m=next(m for m in para('111',k)['mentions']if m['surface']==s);self.assertEqual(m['person_id'],pid);self.assertEqual(m['kind'],'person')
  ds=load('corpus/shiji/111-identities.json')['decisions'];d=next(d for d in ds if d['id']=='d-shiji111-final-taihou');self.assertEqual(len(d['references']),2);self.assertIn('王太后後孝景帝十六歲，以元朔四年崩',para('049',25)['text']);self.assertTrue(any(e['paragraph_id']=='c-shiji-115-chaoxian:p007'for d in ds if d['id']=='d-shiji111-final-louchuan'for e in d['evidence']))
 def test_table_links_keep_spelling_and_similar_names_separate(self):
  cs=cells()
  for cid,s,pid in [('r010-c03','趙安稽','m77_ykm_b9r'),('r035-c04','復陸支','wt3_fvo_jk6'),('r036-c04','伊即軒','fzx_a7k_725'),('r038-c04','衛山','2c4_hnz_3k9')]:
   m=cs['shiji-020-t1-'+cid]['person_mentions'][0];self.assertEqual((m['surface'],m['person_id']),(s,pid));self.assertTrue(m['identity_evidence'])
  self.assertEqual(cs['shiji-020-t1-r029-c05']['person_mentions'][0]['person_id'],'1iq_zk5_ksi');self.assertNotEqual(cs['shiji-020-t1-r029-c05']['person_mentions'][0]['person_id'],cs['shiji-020-t1-r036-c04']['person_mentions'][0]['person_id']);self.assertEqual(next(m['person_id']for m in para('115',5)['mentions']if m['surface']=='衛山'),'1a3_sos_b0l')
 def test_named_king_and_commander_are_person_markers(self):
  cs=cells()
  for cid,s,pid in [('r035-c01','因淳王','wt3_fvo_jk6'),('r036-c01','樓剸王','fzx_a7k_725'),('r038-c01','驃騎將軍','3tw_nq2_gyn')]:
   c=cs['shiji-020-t1-'+cid];m=next(m for m in c['person_mentions']if m['surface']==s);self.assertEqual(m['person_id'],pid);self.assertEqual(c['text'][m['start']:m['end']],s)
 def test_retired_ids_removed(self):
  for pid in ['rbh_rw8_8se','1bz_a7y_o2d','52u_xjr_oek','5i5_c55_894','w0b_xoz_gcd']:
   self.assertNotIn(pid,{p['id']for p in load('registry/persons.json')['persons']});self.assertNotIn(pid,{p['id']for p in load('data/historical-tables/person-candidates.json')['persons']})
   for folder in ['data/corpus/profiles','exports/persons']:self.assertFalse((R/folder/(pid+'.json')).exists())
 def test_editorial_notes_reflect_current_identities(self):
  text=' '.join(load('corpus/shiji/111.json')['annotation']['limitations']);self.assertNotIn('樓船將軍留未解錨點',text);self.assertNotIn('太后崩的太后身份暫未解',text);self.assertNotIn('王夫人身份仍分開',text);self.assertNotIn('未據記憶補劉據',text)
