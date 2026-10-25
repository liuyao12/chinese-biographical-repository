import unittest,json,copy,tempfile,hashlib
from pathlib import Path
from scripts.fixed_wikisource_family_units import project,errors
from scripts.fixed_wikisource_units import source_errors
from scripts.person_bundle import load_catalog,bundle
R=Path(__file__).resolve().parents[1];REL='corpus/jinshu/040-jiachong-family.json'
class JiaChongSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((R/REL).read_text());cls.ps={p['id'].rsplit(':',1)[-1]:p for p in cls.ch['paragraphs']};cls.b=json.loads((R/cls.ch['annotation']['fixed_wikisource_unit_ref']).read_text());cls.records=json.loads((R/'source-evidence/jin040-jiachong-family/identity-records.json').read_text());cls.ids={x['key']:x['person_id']for x in cls.records};cls.catalog=load_catalog(R)
 def test_complete_30_raw_projection_and_subheadings(self):
  self.assertEqual(source_errors(self.ch,R),[]);self.assertEqual(len(self.ch['paragraphs']),30);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),6078);self.assertEqual(len(self.b['selection']['headings']),6)
  self.assertTrue(self.ps['p001']['text'].startswith('賈充，字公閭'));self.assertTrue(self.ps['p030']['text'].endswith('卒，諡曰烈。'));self.assertEqual(self.b['selection']['following_heading'],'==楊駿==')
 def test_change_glyph_even_with_rehashed_chapter_rejected(self):
  c=copy.deepcopy(self.ch);c['paragraphs'][28]['text']=c['paragraphs'][28]['text'].replace('裴顗','裴頠');c['text_sha256']=hashlib.sha256('\n\n'.join(p['text']for p in c['paragraphs']).encode()).hexdigest();self.assertTrue(errors(c,R,self.b))
 def test_omit_attached_biography_or_co_shift_offsets_rejected(self):
  c=copy.deepcopy(self.ch);c['paragraphs'].pop(16);self.assertTrue(errors(c,R,self.b))
  c=copy.deepcopy(self.ch);p=c['paragraphs'][0];p['source_position']['raw_start']+=1;p['source_position']['raw_end']+=1;p['source_position']['raw_character_offsets']=[x+1 for x in p['source_position']['raw_character_offsets']];p['source_position']['projection_sha256']=hashlib.sha256((json.dumps(p['source_position']['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest();self.assertTrue(errors(c,R,self.b))
 def test_title_not_added_as_body_and_revision_bound(self):
  c=copy.deepcopy(self.ch);c['paragraphs'][0]['text']='賈充'+c['paragraphs'][0]['text'];self.assertTrue(errors(c,R,self.b));b=copy.deepcopy(self.b);b['source_revision']+=1;self.assertTrue(errors(self.ch,R,b))
 def test_raw_symlink_escape_rejected(self):
  with tempfile.TemporaryDirectory()as tmp:
   t=Path(tmp);(t/'sources').mkdir();(t/'sources/witnesses').symlink_to(R/'sources/witnesses',target_is_directory=True);self.assertTrue(errors(self.ch,t,self.b))
 def test_synthetic_complete_family_and_unsupported_markup(self):
  raw='==甲==\n甲。\n===子乙===\n乙-{後}-至。\n==丙==\n丙。\n';p,b=project(raw,'甲傳');self.assertEqual([x['text']for x in p],['甲。','乙後至。']);self.assertEqual(len(b['headings']),2)
  with self.assertRaises(AssertionError):project(raw.replace('乙-{後}-至。','乙{{未知|甲}}。'),'甲傳')
 def ms(self,n,s):return[m for m in self.ps[n]['mentions']if m['surface']==s]
 def test_wu_sunxiu_not_zhao_sunxiu_and_wangjun_not_northern(self):
  self.assertNotEqual(self.ms('p011','孫秀')[0]['person_id'],'8x5_e5i_yle');self.assertEqual(self.ms('p015','王浚')[0]['person_id'],'36c_6b6_4b3');self.assertNotEqual(self.ms('p015','王浚')[0]['person_id'],'9c1_ff0_1b5')
 def test_received_peiyi_link_not_glyph_correction(self):
  m=self.ms('p029','裴顗')[0];self.assertEqual(m['person_id'],'4ni_4t1_4o9_AAB');self.assertNotIn('裴頠',self.ps['p029']['text']);self.assertIn('裴顗',self.ps['p029']['text'])
 def test_wives_daughters_and_mothers_distinct(self):
  self.assertNotEqual(self.ids['郭槐'],self.ids['李氏〔賈充前妻，李豐女〕']);self.assertNotEqual(self.ms('p009','女')[0]['person_id'],self.ms('p010','女')[0]['person_id']);self.assertEqual(self.ms('p018','女')[0]['person_id'],self.ids['郭槐'])
  self.assertEqual({m['person_id']for m in self.ms('p018','母')},{self.ids['柳氏〔賈充母〕'],self.ids['李氏〔賈充前妻，李豐女〕'],self.ids['母〔劉含母，毌丘儉孫女〕']})
 def test_dream_no_invented_emperor_and_no_clan_as_person(self):
  for surface in ['府公','公','吾子','吾孫']:self.assertTrue(all(m['kind']=='unresolved'and m['person_id']is None for m in self.ms('p024',surface)))
  for surface in ['賈','裴','王']:self.assertTrue(all(m['kind']=='unresolved'for m in self.ms('p025',surface)))
 def test_hanxian_candidate_not_automatic_merge(self):
  r=next(r for r in self.records if r['key']=='韓咸');self.assertTrue(r['is_new']);self.assertEqual(r['cross_source_candidates'],['131_3e1_b6e']);self.assertNotEqual(r['person_id'],'131_3e1_b6e');self.assertIn('非',r['identity_note'])
 def test_emperors_scope_and_reciprocal_registry(self):
  self.assertEqual(self.ms('p005','帝')[0]['person_id'],'hgm_jvn_hle');self.assertEqual({m['person_id']for m in self.ms('p004','帝')},{'dkn_ge4_286_AAAAI'});self.assertEqual(self.ms('p022','帝')[0]['person_id'],'7e0_f69_1ac')
  people,_=self.catalog
  for p in self.ch['paragraphs']:
   for m in p['mentions']:
    self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
    if m['kind']=='person':self.assertTrue(any(e.get('mention_id')==m['id']and e['quote']==m['surface']for e in people[m['person_id']]['evidence']))
 def test_original_source_separate_from_typed_kin_or_false_named_work(self):
  self.assertNotIn('assertions',json.loads((R/'corpus/jinshu/040-jiachong-family.json').read_text()));self.assertTrue(all(m['kind']=='unresolved'for m in self.ms('p018','女訓')));self.assertNotEqual(self.ids['乳母〔黎民所戀，郭槐殺〕'],self.ids['乳母〔次男所戀，郭槐殺〕'])
if __name__=='__main__':unittest.main()
