import unittest,json,re,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
J=lambda p:json.loads(p.read_text());D=J(ROOT/'corpus/songshu/075-wangsengda.json');A=J(ROOT/'corpus/songshu/075-wangsengda-assertions.json')['assertions'];I=J(ROOT/'tests/fixtures/song075-wangsengda/person-ids.json');B={p['source_position']['first_line']:p for p in D['paragraphs']}
def at(line,start):return next(m for m in B[line]['mentions']if m['start']==start)
class Song075WangsengdaSource(unittest.TestCase):
 def test_raw_revision_and_twenty_full_paragraphs(self):
  raw=(ROOT/'tests/fixtures/song075-wangsengda/fixed1997722.wikitext').read_text();self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(),D['source']['wikitext_sha256']);self.assertEqual(D['source']['revision_id'],1997722);lines=raw.splitlines();self.assertEqual(lines[8],'==王僧達==');self.assertEqual(lines[49],'==顏竣==');self.assertEqual(len(D['paragraphs']),20);self.assertEqual(sum(len(p['text'])for p in D['paragraphs']),4038)
  for p in D['paragraphs']:
   line=lines[p['source_position']['first_line']-1];line=line[1:]if line.startswith(':')else line;self.assertEqual(re.sub(r'<ref>.*?</ref>','',line),p['text'])
 def test_petitions_son_and_appended_subao_are_not_truncated(self):
  self.assertTrue(B[18]['text'].startswith('臣衰索餘生'));self.assertTrue(B[24]['text'].endswith('存沒銘分。'));self.assertTrue(B[32]['text'].startswith('臣自審庸短'));self.assertTrue(B[38]['text'].endswith('哀申此請。'));self.assertTrue(B[46]['text'].startswith('子道琰'));self.assertTrue(B[48]['text'].endswith('與闍共伏誅。'))
 def test_all_anchors_exact_and_nonoverlap(self):
  n=0;unknown=0
  for p in D['paragraphs']:
   end=0
   for m in p['mentions']:self.assertLessEqual(end,m['start']);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end'];n+=1;unknown+=m['kind']=='unresolved'
  self.assertEqual((n,unknown),(193,15))
 def test_pronouns_are_scoped_not_nearest_name(self):
  self.assertEqual(at(32,350)['person_id'],I['xi']);self.assertEqual(at(44,462)['person_id'],I['hong']);self.assertEqual(at(34,31)['person_id'],I['wen']);self.assertEqual(at(34,32)['person_id'],I['sengda']);self.assertEqual(at(36,133)['person_id'],I['xiaowu'])
  p=B[14];m=next(m for m in p['mentions']if m['start']==p['text'].index('王出赴難'));self.assertEqual(m['person_id'],I['sengda'])
 def test_unresolved_fraudulent_ji_and_petition_lingbao_not_forced(self):
  p=B[28];s=p['text'].index('注以為己子')+3;m=at(28,s);self.assertIsNone(m['person_id']);self.assertEqual(set(m['candidate_person_ids']),{I['sengda'],I['zuoyong']})
  p=B[32];m=at(32,p['text'].index('靈寶'));self.assertIsNone(m['person_id']);self.assertEqual(m['candidate_person_ids'],[I['lingbao']])
 def test_contemporaries_reuse_ids_and_homonyms_stay_distinct(self):
  self.assertEqual(I['shen'],'408_ce3_5d8');self.assertEqual(I['sengqian'],'7r6_k52_qji_ABAAAAEB');self.assertNotEqual(I['wangtian'],'7r6_k52_qji_ABAAC');self.assertEqual(I['jun'],'3b1_39e_aa6');self.assertNotEqual(I['lingbao'],'u9s_w6j_8mc_AAF');self.assertEqual(I['shao'],'fof_k8v_7md')
 def test_no_fake_father_adoption_or_mother_from_fraud(self):
  self.assertTrue({f'a-song075-sengda-{i:03d}'for i in range(1,11)}<={a['id']for a in A});self.assertFalse(any(a['subject_person_id']in[I['lingbao'],I['que']]and a['predicate']in['father','adoptive_father']for a in A));self.assertFalse(any(a['predicate']=='adoptive_father'for a in A));self.assertFalse(any(a['subject_person_id']==I['daoyan']and a['predicate']=='mother'for a in A))
 def test_mother_role_not_forced_biological(self):
  a=next(a for a in A if a['predicate']=='mother');self.assertEqual(a['subject_person_id'],I['sengda']);self.assertEqual(a['qualifiers']['biological_parentage'],'not_independently_established')
 def test_child_continuation_is_sengda_not_hong(self):
  a=next(a for a in A if a['id']=='a-song075-sengda-010');self.assertEqual(a['object_person_id'],I['sengda']);self.assertEqual(a['subject_person_id'],I['daoyan']);self.assertEqual(a['context']['paragraph_ids'],[B[44]['id'],B[46]['id']]);self.assertEqual(B[44]['source_position']['last_line']+1,B[46]['source_position']['first_line'])
 def test_cousins_and_uncle_do_not_create_unknown_fathers(self):
  for key in ['que','xiu']:
   self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==I[key]for a in A))
  self.assertEqual(len([a for a in A if a['predicate']=='agnatic_cousin']),2)
  for a in A:
   if a['predicate']=='agnatic_cousin':self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id'])
 def test_apparatus_and_digital_headings_are_separate(self):
  notes=D['source']['normalization']['collation_apparatus'];self.assertEqual(len(notes),7);self.assertTrue(all(p['text_layer']=='received_chapter'for p in D['paragraphs']));self.assertFalse(any('<ref>'in p['text']or'各本並'in p['text']for p in D['paragraphs']));self.assertFalse(D['source']['image_verified']);self.assertFalse(D['annotation']['human_reviewed'])
 def test_reported_age_does_not_imply_birth_year(self):
  self.assertIn('時年三十六',B[44]['text']);self.assertIn('黎氓□□',B[20]['text'])
  for a in D['annotation'].get('age_assertions',[]):
   if any(e.get('paragraph_id')==B[44]['id']for e in a.get('evidence',[])):self.assertIsNone(a.get('birth_year'))
if __name__=='__main__':unittest.main()
