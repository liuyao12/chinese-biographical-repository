import unittest,json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(p):return json.loads((R/p).read_text())
class CaoXiuSource(unittest.TestCase):
 def setUp(self):self.c=J('corpus/sanguozhi/009-caoxiu.json');self.ps=self.c['paragraphs'];self.a=J('corpus/sanguozhi/009-caoxiu-assertions.json')['assertions'];self.x=J('source-evidence/sgz009-caoxiu/projection.json')
 def mention(self,n,context,term):
  p=self.ps[n-1];i=p['text'].index(context)+context.index(term);return next(m for m in p['mentions']if m['start']==i)
 def test_complete_unit_and_layers_not_whole_book(self):
  self.assertEqual(self.x['source_lines'],[272,308]);self.assertEqual(len(self.ps),8);self.assertEqual([p['text_layer']for p in self.ps],['received_chapter','witness_appended_pei_songzhi_note']*4);self.assertIn('曹休字文烈',self.ps[0]['text']);self.assertTrue(self.ps[-1]['text'].endswith('戰敗死'));self.assertNotIn('曹真字子丹',''.join(p['text']for p in self.ps));self.assertFalse(self.c['source']['image_verified']);self.assertFalse(self.c['annotation']['human_reviewed'])
 def test_raw_sha_and_each_character_projection(self):
  raw=(R/'source-evidence/sgz009-caoxiu/primary009.txt').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),self.x['source_sha256']);positions=[]
  for p,u in zip(self.ps,self.x['units']):
   self.assertEqual(p['text'],''.join(z['character']for z in u['character_projection']))
   for z in u['character_projection']:self.assertEqual(self.x['full_context']['projected_text'][z['projected_offset']],z['character']);positions.append(z['projected_offset'])
  expected=[i for i,c in enumerate(self.x['full_context']['projected_text'])if c not in '()'];self.assertEqual(positions,expected)
 def test_all_anchors_and_xml_text(self):
  for p in self.ps:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
   for a,b in zip(p['mentions'],p['mentions'][1:]):self.assertLessEqual(a['end'],b['start'])
  ps=ET.fromstring((R/'corpus/sanguozhi/009-caoxiu.xml').read_text()).findall('p');self.assertEqual([''.join(p.itertext())for p in ps],[p['text']for p in self.ps])
 def test_emperor_changes_inside_complete_body(self):
  self.assertEqual(self.mention(5,'帝征孫權','帝')['person_id'],'tix_jqk_w1o');self.assertEqual(self.mention(5,'眀帝即位','眀帝')['person_id'],'932_46f_026');self.assertEqual(self.mention(5,'太和二年帝為','帝')['person_id'],'932_46f_026');self.assertEqual(self.mention(7,'初文帝分','文帝')['person_id'],'tix_jqk_w1o')
 def test_not_taizu_biological_or_adoptive_son(self):
  xiu='h7n_w5t_i1c_AA';taizu='dad_b77_b38';self.assertFalse(any(a['subject_person_id']==xiu and a['object_person_id']==taizu and a['predicate']in['father','adoptive_father']for a in self.a));self.assertEqual(self.mention(3,'此吾家千里駒','此')['person_id'],xiu);self.assertEqual(self.mention(3,'其實帥也','其')['person_id'],xiu)
 def test_direct_father_and_nonexhaustive_succession(self):
  zhao=self.mention(5,'子肇嗣','肇')['person_id'];xing=self.mention(7,'子興嗣','興')['person_id'];shu=self.mention(8,'肇孫攄','攄')['person_id'];self.assertTrue(any(a['predicate']=='father'and a['subject_person_id']==zhao and a['object_person_id']=='h7n_w5t_i1c_AA'for a in self.a));self.assertTrue(any(a['predicate']=='father'and a['subject_person_id']==xing and a['object_person_id']==zhao for a in self.a));self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==shu for a in self.a));self.assertTrue(any(a['predicate']=='grandfather'and a['subject_person_id']==shu and a['object_person_id']==zhao for a in self.a))
 def test_brother_direction_not_absolute_birth_order(self):
  a=next(a for a in self.a if a['predicate']=='brother');self.assertEqual(a['subject_person_id'],self.mention(7,'肇弟纂','纂')['person_id']);self.assertEqual(a['object_person_id'],self.mention(7,'肇弟纂','肇')['person_id']);self.assertNotIn('ordinal',a['qualifiers'])
 def test_pei_quotations_and_original_glyphs(self):
  self.assertEqual(self.ps[1]['source_position']['cited_work'],'魏書');self.assertEqual(self.ps[5]['source_position']['cited_work'],'世語');self.assertEqual(self.ps[7]['source_position']['cited_work'],'張隠文士傳');self.assertIn('攄字顔逺',self.ps[-1]['text']);self.assertIn('襄陽太守',self.ps[-1]['text']);self.assertIn('向呉',self.ps[-1]['text']);self.assertNotIn('向吳',self.ps[-1]['text'])
 def test_unknown_family_members_are_not_named_people(self):
  father=self.mention(1,'喪父','父')['person_id'];mother=self.mention(1,'老母','母')['person_id'];grand=self.mention(2,'休祖父','祖父')['person_id'];self.assertEqual(len({father,mother,grand}),3);reg={p['id']:p for p in J('registry/persons.json')['persons']};self.assertTrue(all('未名'in reg[p]['label']for p in [father,mother,grand]));self.assertFalse(any(a['predicate']=='biological_mother'for a in self.a))
 def test_primary_context_does_not_create_false_meeting(self):
  own=[a for a in self.a if a['id'].startswith('a-sgz009-caoxiu54a-')];self.assertEqual(len(own),7);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']=='h7n_w5t_i1c_AAA*A'for a in own));self.assertIn('曹顏遠',next(p for p in J('registry/persons.json')['persons']if p['id']=='h7n_w5t_i1c_AAA*A')['label'])
