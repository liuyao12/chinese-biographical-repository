# coding: utf-8
"""固定本傳全文、字元投影與親屬語義；全部依ROOT，不依賴私有包。"""
import pathlib,json,hashlib,copy,unittest,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
J=lambda p:json.loads(p.read_text())
C=J(ROOT/'corpus/songshu/067-xielingyun.json');A=J(ROOT/'corpus/songshu/067-xielingyun-assertions.json')['assertions'];E=J(ROOT/'source-evidence/song067-lingyun-projection.json');RAW=(ROOT/E['raw_path']).read_text();LINES=RAW.splitlines()
def projection_valid(chapter,evidence):
 try:
  if hashlib.sha256(RAW.encode()).hexdigest()!=evidence['source_metadata']['raw_sha256']:return False
  if chapter['source']['source_commit']!=evidence['source_metadata']['commit']:return False
  for p,pr in zip(chapter['paragraphs'],evidence['projection']['paragraphs']):
   if p['id']!=pr['paragraph_id']:return False
   out=''
   for run in pr['runs']:
    if run['paragraph_start']!=len(out):return False
    out+=LINES[run['raw_line']-1][run['raw_start']:run['raw_end']]
    if run['paragraph_end']!=len(out):return False
   if out!=p['text']:return False
  return True
 except (KeyError,IndexError,TypeError):return False
class Song067Source(unittest.TestCase):
 def test_fixed_revision_and_full_boundary(self):
  self.assertEqual(C['source']['source_commit'],'e80c057667e3c8684f11d5088251e10244d5a264');self.assertEqual(len(C['paragraphs']),11);self.assertTrue(C['paragraphs'][0]['text'].startswith('謝靈運陳郡陽夏人也祖𤣥'));self.assertTrue(C['paragraphs'][-1]['text'].endswith('子鳯蚤卒'))
 def test_raw_projection_every_character(self):self.assertTrue(projection_valid(C,E))
 def test_reject_silent_glyph_replacement(self):
  d=copy.deepcopy(C);d['paragraphs'][0]['text']=d['paragraphs'][0]['text'].replace('𤣥','玄',1);self.assertFalse(projection_valid(d,E))
 def test_reject_changed_gap_code(self):
  d=copy.deepcopy(C);d['paragraphs'][5]['text']=d['paragraphs'][5]['text'].replace('&KR','&BAD',1);self.assertFalse(projection_valid(d,E))
 def test_reject_shifted_raw_line(self):
  e=copy.deepcopy(E);e['projection']['paragraphs'][0]['runs'][0]['raw_line']+=1;self.assertFalse(projection_valid(C,e))
 def test_reject_cross_revision(self):
  d=copy.deepcopy(C);d['source']['source_commit']='0'*40;self.assertFalse(projection_valid(d,E))
 def test_no史臣_or_qing考證_as_body(self):
  t=''.join(p['text']for p in C['paragraphs']);self.assertNotIn('史臣曰',t);self.assertNotIn('宋書卷六十七考證',t);self.assertIn('史臣曰',RAW);self.assertIn('考證',RAW)
 def test_self_commentary_kept_and_layered(self):
  layers=E['text_layers']['layers'];self.assertTrue(any(x['kind']=='author_self_commentary'and'文成張良'in x['quote']for x in layers));self.assertIn('文成張良',C['paragraphs'][5]['text'])
 def test_all_layers_exact(self):
  ps={p['id']:p for p in C['paragraphs']}
  for x in E['text_layers']['layers']:self.assertEqual(ps[x['paragraph_id']]['text'][x['start']:x['end']],x['quote'])
 def test_all_mentions_exact_sorted_nonoverlap(self):
  ids=set()
  for p in C['paragraphs']:
   last=0
   for m in p['mentions']:
    self.assertNotIn(m['id'],ids);ids.add(m['id']);self.assertGreaterEqual(m['start'],last);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);last=m['end']
 def test_cross_jin_song_ids_retained(self):
  ms=[m for p in C['paragraphs']for m in p['mentions']];self.assertTrue(any(m['surface']=='𤣥'and m['person_id']=='aa6_83c_juy_CD'for m in ms));self.assertTrue(any(m['surface']=='瑍'and m['person_id']=='aa6_83c_juy_CDA'for m in ms));self.assertTrue(any(m['surface']=='謝靈運'and m['person_id']=='aa6_83c_juy_CDAA'for m in ms))
 def test_direct_father_and_grandfather_distinct(self):
  self.assertTrue(any(a['subject_person_id']=='aa6_83c_juy_CDAA'and a['predicate']=='father'and a['object_person_id']=='aa6_83c_juy_CDA'for a in A));self.assertTrue(any(a['subject_person_id']=='aa6_83c_juy_CDAA'and a['predicate']=='grandfather'and a['object_person_id']=='aa6_83c_juy_CD'for a in A));self.assertFalse(any(a['subject_person_id']=='aa6_83c_juy_CDAA'and a['predicate']=='father'and a['object_person_id']=='aa6_83c_juy_CD'for a in A))
 def test_first_me_is玄_not_lingyun(self):self.assertEqual(next(m for m in C['paragraphs'][0]['mentions']if m['surface']=='我')['person_id'],'aa6_83c_juy_CD')
 def test_embedded臣顗_not_outer_author(self):
  p=C['paragraphs'][9];a=p['text'].index('臣顗');m=next(m for m in p['mentions']if m['start']==a);self.assertEqual(m['surface'],'臣');self.assertNotEqual(m['person_id'],'aa6_83c_juy_CDAA')
 def test_feng_is_son_not_世子_title(self):
  p=C['paragraphs'][-1];self.assertIn('傳於世子鳯',p['text']);self.assertFalse(any(m['surface']=='世子'for m in p['mentions']));self.assertTrue(any(a['subject_person_id']=='aa6_83c_juy_CDAAA'and a['predicate']=='father'and a['object_person_id']=='aa6_83c_juy_CDAA'for a in A))
 def test_huilian_father_not_lingyun(self):
  x=next(a for a in A if a['id']=='a-song067-lingyun-004');self.assertEqual(x['object_person_id'],'apr_7dg_tdd');self.assertNotEqual(x['subject_person_id'],'aa6_83c_juy_CDAAA')
 def test_cousins_not_shared_father_or_absolute_order(self):
  xs=[a for a in A if a['predicate']=='agnatic_cousin'];self.assertEqual(len(xs),4)
  for a in xs:self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id']);self.assertNotIn('shared_father',a['qualifiers']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_landscape_guang_and_gu_not_people(self):
  p=C['paragraphs'][5];self.assertFalse(any(m['start']==561 for m in p['mentions']));self.assertEqual([m['start']for m in p['mentions']if m['surface']=='孤'],[154]);self.assertTrue(any(m['start']==8915 and m['surface']=='廣'for m in p['mentions']))
 def test_xijingxing_reuses_xichao_after_fixed_name_bridge(self):
  p=C['paragraphs'][5];self.assertTrue(any(m['surface']=='郗景興'and m['person_id']=='57b_1cb_a1b'for m in p['mentions']))
 def test_external_bridges_keep_complete_paragraph_and_original_wording(self):
  x=J(ROOT/'source-evidence/song067-xichao-name-bridge.json');self.assertEqual(x['external_primary_source']['revision_id'],2592755);self.assertIn('超字景興，一字嘉賓。',x['external_primary_source']['complete_paragraph']);self.assertIn('嘉賓，超小字也',x['existing_native_source']['quote']);self.assertFalse(x['human_reviewed'])
 def test_zhongxuan_is_comparison_not_changyu_alias(self):
  p=C['paragraphs'][7];m=next(m for m in p['mentions']if m['surface']=='仲宣');self.assertEqual(m['person_id'],'ad4_a63_862');self.assertNotEqual(m['person_id'],next(m['person_id']for m in p['mentions']if m['surface']=='何長瑜'));b=J(ROOT/'source-evidence/song067-wangcan-name-bridge.json');self.assertEqual(b['external_primary_source']['selected_primary_clause'],'王粲字仲宣')
 def test_no_birthmother_or_unapproved_remap(self):self.assertFalse(any(a['predicate']in ['mother','adoptive_mother','adoptive_father']for a in A));self.assertTrue(all(a['human_reviewed']is False for a in A))
 def test_unresolved_ancient_terms_not_guessed(self):
  ms=[m for p in C['paragraphs']for m in p['mentions']];self.assertTrue(any(m['surface']=='霍生'and m['person_id']is None for m in ms));self.assertTrue(any(m['surface']=='王琇'and m['person_id']is None for m in ms))
 def test_no_age_or_title_facts_in_source_only(self):self.assertNotIn('age_assertions',C['annotation']);self.assertNotIn('title_proposals',C['annotation']);self.assertFalse(C['source']['image_verified']);self.assertFalse(C['annotation']['human_reviewed'])
 def test_xml_roundtrip(self):
  x=ET.parse(ROOT/'corpus/songshu/067-xielingyun.xml').getroot();self.assertEqual([''.join(p.itertext())for p in x.findall('p')],[p['text']for p in C['paragraphs']])
if __name__=='__main__':unittest.main()
