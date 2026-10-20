# coding: utf-8
import pathlib,json,hashlib,copy,unittest,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());C=J(ROOT/'corpus/songshu/053-xiefangming.json');A=J(ROOT/'corpus/songshu/053-xiefangming-assertions.json')['assertions'];EV=J(ROOT/'source-evidence/song053-fangming-projection.json');RAW=(ROOT/EV['raw_path']).read_text();LINES=RAW.splitlines()
def valid(d,e):
 try:
  if d['source']['source_commit']!='e80c057667e3c8684f11d5088251e10244d5a264'or hashlib.sha256(RAW.encode()).hexdigest()!=e['source_metadata']['raw_sha256']:return False
  return len(d['paragraphs'])==len(e['paragraphs'])and all(p['id']==pr['paragraph_id']and p['text']==''.join(LINES[x['raw_line']-1][x['raw_start']:x['raw_end']]for x in pr['runs'])for p,pr in zip(d['paragraphs'],e['paragraphs']))
 except (KeyError,TypeError,IndexError):return False
class FangmingSource(unittest.TestCase):
 def test_complete_body_and_boundary(self):
  self.assertEqual(len(C['paragraphs']),6);self.assertEqual(sum(len(p['text'])for p in C['paragraphs']),1329);self.assertTrue(C['paragraphs'][0]['text'].startswith('謝方明陳郡陽夏'));self.assertTrue(C['paragraphs'][-1]['text'].endswith('臨川内史'));self.assertNotIn('江夷字茂遠',''.join(p['text']for p in C['paragraphs']))
 def test_raw_projection(self):self.assertTrue(valid(C,EV))
 def test_reject_changed_raw_glyph(self):
  d=copy.deepcopy(C);d['paragraphs'][2]['text']=d['paragraphs'][2]['text'].replace('没','陷',1);self.assertFalse(valid(d,EV))
 def test_reject_shifted_raw_line(self):
  e=copy.deepcopy(EV);e['paragraphs'][0]['runs'][0]['raw_line']+=1;self.assertFalse(valid(C,e))
 def test_reject_other_revision(self):
  d=copy.deepcopy(C);d['source']['source_commit']='0'*40;self.assertFalse(valid(d,EV))
 def test_book053_other_source_preserved(self):
  old=J(ROOT/'corpus/songshu/053-yu-dengzhi.json');self.assertEqual(old['id'],'c-songshu-053-yu-dengzhi');w=next(x for x in J(ROOT/'registry/works.json')['works']if x['id']=='w-songshu');b=next(x for x in w['books']if x['number']==53);self.assertIn(old['id'],b['chapter_ids']);self.assertIn(C['id'],b['chapter_ids'])
 def test_existing_apr_and_issued_huilian(self):
  ms=[m for p in C['paragraphs']for m in p['mentions']];self.assertTrue(any(m['surface']=='謝方明'and m['person_id']=='apr_7dg_tdd'for m in ms));self.assertTrue(any(m['surface']=='惠連'and m['person_id']=='apr_7dg_tdd_A'for m in ms))
 def test_father_and_grandfather_not_swapped(self):
  self.assertTrue(any(a['subject_person_id']=='apr_7dg_tdd'and a['predicate']=='father'and a['object_person_id']=='1a3_b0c_e6d'for a in A));self.assertTrue(any(a['subject_person_id']=='apr_7dg_tdd'and a['predicate']=='grandfather'and a['object_person_id']=='1b1_d4d_bb8'for a in A));self.assertFalse(any(a['subject_person_id']=='apr_7dg_tdd'and a['predicate']=='father'and a['object_person_id']=='1b1_d4d_bb8'for a in A))
 def test_no_direct_chong_father_tie_in_native(self):self.assertFalse(any(a['subject_person_id']=='1a3_b0c_e6d'and a['predicate']=='father'and a['object_person_id']=='1b1_d4d_bb8'for a in A))
 def test_chong_provisional_and_dependent_nanshi(self):
  e=J(ROOT/'source-evidence/song053-chong-identity-review.json');self.assertEqual(e['status'],'editorial_provisional_identity_adoption');self.assertFalse(e['human_reviewed']);self.assertIn('非額外獨立',e['dependent_parallel']['note']);self.assertGreaterEqual(len(e['evidence']),4)
 def test_no_fangming_adoption(self):self.assertFalse(any(a['subject_person_id']=='apr_7dg_tdd'and a['predicate']=='adoptive_father'for a in A))
 def test_bofu_miao_not_father_or_son(self):
  self.assertTrue(any(a['predicate']=='paternal_uncle'and a['object_person_id']=='1b1_d4d_bb8_A'for a in A));self.assertFalse(any(a['predicate']=='father'and a['object_person_id']=='1b1_d4d_bb8_A'for a in A))
 def test_jingren_two_people(self):
  x=J(ROOT/'source-evidence/song053-xiejingren-name-bridge.json');pid=x['person_id'];self.assertNotEqual(pid,'740_57f_3ec');self.assertTrue(any(m['surface']=='景仁'and m['person_id']==pid for m in C['paragraphs'][0]['mentions']));self.assertTrue(any(m['surface']=='殷景仁'and m['person_id']=='740_57f_3ec'for m in C['paragraphs'][-1]['mentions']))
 def test_jingren_direct_name_bridge(self):
  x=J(ROOT/'source-evidence/song053-xiejingren-name-bridge.json');self.assertEqual(x['nanshi019']['revision_id'],1531762);self.assertEqual(x['nanshi019']['selected_clause'],'謝裕字景仁');self.assertIn('謝裕字景仁',x['nanshi019']['complete_raw_introductory_paragraph']);self.assertNotIn('裕',C['paragraphs'][0]['text'])
 def test_refused_marriage_not_spouse(self):self.assertFalse(any(a['predicate']=='spouse'for a in A));self.assertTrue(any('欲以女嫁方明'==a['qualifiers']['source_term']and a['predicate']=='father'for a in A))
 def test_mother_not_birthmother(self):self.assertFalse(any(a['predicate']in ['mother','adoptive_mother','stepmother']for a in A));self.assertTrue(any(m['surface']=='母'for m in C['paragraphs'][2]['mentions']))
 def test_sister_no_shared_parents_invented(self):
  a=next(a for a in A if a['predicate']=='sister');self.assertNotIn('shared_father',a['qualifiers']);self.assertNotIn('shared_mother',a['qualifiers']);self.assertIsNone(a['qualifiers']['relative_birth_order']['younger_ordinal'])
 def test_huixuan_brother_not_son_or_heir(self):
  x=next(a for a in A if a['predicate']=='brother');self.assertEqual(x['object_person_id'],'apr_7dg_tdd_A');self.assertFalse(any(a['subject_person_id']==x['subject_person_id']and a['predicate']in ['father','adoptive_father','ritual_successor_of']for a in A));self.assertIn('無子弟惠宣',C['paragraphs'][-1]['text'])
 def test_bofu_older_than_father_is_typed_not_child_vs_uncle(self):
  qs=J(ROOT/'source-evidence/song053-fangming-typed-proposals.json')['proposals'];q=next(x for x in qs if x['kind']=='paternal_uncle_older_than_named_father');c=q['proposed_constraint'];self.assertEqual((c['older_person_id'],c['younger_person_id'],c['operator']),('1b1_d4d_bb8_A','1a3_b0c_e6d','lt'));self.assertIsNone(c['older_ordinal']);self.assertIsNone(c['younger_ordinal']);self.assertEqual(q['status'],'not_imported')
 def test_bare_mother_and_huixuan_father_not_forced_by_model(self):
  qs=J(ROOT/'source-evidence/song053-fangming-typed-proposals.json')['proposals'];m=next(x for x in qs if x['kind']=='maternal_role_bare_unnamed_mother')['proposed_relationship'];self.assertIsNone(m['biological_mother']);self.assertIsNone(m['father_person_id']);self.assertTrue(any(x['kind']=='parent_through_younger_brother'and x['status']=='not_imported'for x in qs))
 def test_qinshu_no_absolute_order(self):self.assertTrue(all('birth_order'not in a['qualifiers']for a in A));self.assertTrue(all(a.get('qualifiers',{}).get('kinship_structure',{}).get('common_ancestor_person_id')is None for a in A))
 def test_yin_self_age_not_huilian(self):
  p=C['paragraphs'][-1];self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='臣'),'740_57f_3ec');self.assertEqual(next(m['person_id']for m in p['mentions']if m['surface']=='小兒'),'740_57f_3ec')
 def test_wangteng_unresolved_no_new_person(self):self.assertTrue(any(m['surface']=='王騰'and m['person_id']is None for m in C['paragraphs'][2]['mentions']))
 def test_no_birthyear_or_formal_offices_dates(self):self.assertNotIn('age_assertions',C['annotation']);self.assertNotIn('title_proposals',C['annotation']);self.assertFalse(C['source']['image_verified']);self.assertTrue(all(a['human_reviewed']is False for a in A))
 def test_anchors_and_xml_exact(self):
  for p in C['paragraphs']:
   last=0
   for m in p['mentions']:self.assertGreaterEqual(m['start'],last);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);last=m['end']
  x=ET.parse(ROOT/'corpus/songshu/053-xiefangming.xml').getroot();self.assertEqual([''.join(p.itertext())for p in x.findall('p')],[p['text']for p in C['paragraphs']])
if __name__=='__main__':unittest.main()
