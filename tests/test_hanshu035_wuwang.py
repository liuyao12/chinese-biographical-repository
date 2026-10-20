import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
class HanshuWu(unittest.TestCase):
 def test_partial_fixed_witness_and_stable_section_positions(self):
  c=read('corpus/hanshu/035.json');self.assertEqual(c['source']['revision_id'],2605377);self.assertEqual(c['source']['html_sha256'],'2e018b66d35e2de08408e9123eeb1e48966d649e98c66f2b89d4e11ef4811f9f');self.assertFalse(c['source']['image_verified']);self.assertEqual(c['source']['text_scope'],'partial_chapter');self.assertEqual([p['id'].rsplit(':',1)[-1]for p in c['paragraphs']],['p001','p003','p008','p009','p010','p011','p014','p018']);self.assertEqual(c['text_sha256'],hashlib.sha256('\n\n'.join(p['text']for p in c['paragraphs']).encode()).hexdigest())
 def test_all_selected_mentions_have_exact_offsets(self):
  c=read('corpus/hanshu/035.json');self.assertEqual(sum(len(p['mentions'])for p in c['paragraphs']),72)
  for p in c['paragraphs']:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
  self.assertTrue(any('爰盎' in p['text']and '泰常'in p['text']for p in c['paragraphs']));self.assertTrue(any('朝錯'in p['text']for p in c['paragraphs']))
 def test_prince_decision_has_both_events_in_both_books(self):
  e=read('corpus/hanshu/035-equivalences.json')['decisions'][0];self.assertEqual(e['person_ids'],['yqp_nlb_p1p_CAE']);self.assertTrue(e['identity_materialized']);self.assertEqual(len(e['evidence']),4);self.assertEqual({x['work_id']for x in e['evidence']},{'w-hanshu','w-shiji'});self.assertTrue(any('吳王太子駒亡走閩越'in x['quote']for x in e['evidence']));self.assertTrue(any('吳王子子華、子駒亡走閩越'in x['quote']for x in e['evidence']))
 def test_other_sons_are_not_merged_and_both_parent_sources_remain(self):
  rows=read('corpus/shiji/106-assertions.json')['assertions'];a=[a for a in rows if a['id']in ['a-shiji106-005','a-shiji106-007']];self.assertEqual(len(a),2);self.assertEqual({x['subject_person_id']for x in a},{'yqp_nlb_p1p_CAE'});self.assertEqual({x['object_person_id']for x in a},{'yqp_nlb_p1p_CA'});self.assertEqual(len({x['evidence'][0]['paragraph_id']for x in a}),2)
  people={p['id']for p in read('registry/persons.json')['persons']};self.assertTrue({'yqp_nlb_p1p_CAA','yqp_nlb_p1p_CAB','yqp_nlb_p1p_CAD','yqp_nlb_p1p_CAE'}.issubset(people));self.assertNotIn('yqp_nlb_p1p_CAC',people);self.assertFalse((ROOT/'exports/persons/yqp_nlb_p1p_CAC.json').exists())
 def test_name_is_attested_without_supplying_surname(self):
  n=next(n for n in read('data/corpus/profile-names.json')['records']if n['person_id']=='yqp_nlb_p1p_CAE');self.assertEqual((n['title'],n['surname'],n['ming']),('吳王太子',None,'駒'));self.assertEqual(n['quote'],'吳王太子駒亡走閩越。');self.assertEqual(n['chapter_id'],'c-hanshu-035-jingyanwu');self.assertIn('子駒',n['additional_names'])
 def test_work_catalog_tracks_all_imported_hanshu_books(self):
  from scripts.table_evidence import load_tables
  c=read('data/corpus/hanshu/index.json');books={x['number']:x for x in c['chapters']}
  body_books={int(json.loads(p.read_text())['book_id'].rsplit('-',1)[1])for p in (ROOT/'corpus/hanshu').glob('[0-9][0-9][0-9].json')}
  native=[t for t in load_tables(ROOT).values()if t['source']['work_id']=='w-hanshu']
  table_books={int(t['source']['book_id'].rsplit('-',1)[1])for t in native}
  self.assertEqual(set(books),body_books|table_books);self.assertEqual(books[35]['text_scope'],'partial_chapter');self.assertEqual(books[35]['paragraph_count'],8)
  for table in native:
   entry=next(e for e in c['chapters']if e.get('table_id')==table['id'])
   self.assertEqual(entry['available'],'table');self.assertEqual(entry['book_id'],table['source']['book_id']);self.assertEqual(entry['chapter_id'],table['source']['chapter_id']);self.assertEqual(entry['text_scope'],table['source']['text_scope']);self.assertNotIn('path',entry)
