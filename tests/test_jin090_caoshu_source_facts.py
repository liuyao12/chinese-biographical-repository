# coding:utf-8
"""完整曹攄單元的身份、主語、祖孫、官職與日期邊界。"""
import unittest,json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(p):return json.loads((R/p).read_text())
N='source-evidence/jin090-caoshu/'
class CaoShuSource(unittest.TestCase):
 def setUp(self):
  self.c=J('corpus/jinshu/090-caoshu.json');self.ps=self.c['paragraphs'];self.h=J('corpus/jinshu/090-caoshu-titles.json')['holdings'];self.life=J('corpus/jinshu/090-caoshu-life-events.json')['events'];self.a=J('corpus/jinshu/090-caoshu-assertions.json')['assertions'];self.ids={p['label']:p['id']for p in J('registry/persons.json')['persons']}
 def at(self,n,term,token):
  p=self.ps[n-1];i=p['text'].index(term)+term.index(token);return next(m for m in p['mentions']if m['start']==i)
 def test_complete_fixed_three_and_xml(self):
  pr=J(N+'projection.json');raw=(R/(N+'primary090.txt')).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),pr['raw_sha256']);self.assertEqual(len(self.ps),3);ls=raw.decode().splitlines();self.assertEqual([ls[u['raw_line']-1].replace('{{YL|永嘉二年}}','永嘉二年')for u in pr['units']],[p['text']for p in self.ps]);self.assertEqual(ls[pr['heading_line']-1],'==曹攄==');self.assertEqual(ls[pr['next_heading_line']-1],'==潘京==');self.assertEqual([''.join(p.itertext())for p in ET.fromstring((R/'corpus/jinshu/090-caoshu.xml').read_text()).findall('p')],[p['text']for p in self.ps]);self.assertFalse(self.c['source']['image_verified']);self.assertFalse(self.c['annotation']['human_reviewed'])
 def test_all_mentions_exact_without_overlap(self):
  for p in self.ps:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
   for a,b in zip(p['mentions'],p['mentions'][1:]):self.assertLessEqual(a['end'],b['start'])
 def test_same_glyph_different_referents(self):
  widow=self.at(1,'姑以其年少','其')['person_id'];self.assertNotEqual(widow,'h7n_w5t_i1c_AAA*A');self.assertEqual(self.at(1,'攄知其有冤','其')['person_id'],widow);self.assertEqual(self.at(1,'時稱其明','其')['person_id'],'h7n_w5t_i1c_AAA*A')
 def test_royal_speech_subjects(self):
  king=self.at(2,'齊王冏','齊王冏')['person_id'];self.assertEqual(self.at(2,'吾率四海','吾')['person_id'],king);self.assertEqual(self.at(2,'大王之盛','大王')['person_id'],king);self.assertEqual(self.at(2,'於卿意如何','卿')['person_id'],'h7n_w5t_i1c_AAA*A');self.assertEqual(self.at(2,'天子為賊臣','天子')['person_id'],'7e0_f69_1ac');self.assertEqual(self.at(2,'賊臣','賊臣')['kind'],'unresolved')
 def test_highmi_not_han_hong_or_formal_name_jian(self):
  m=self.at(3,'高密王簡','高密王簡');self.assertNotEqual(m['person_id'],'yqp_nlb_p1p_ACAACD');self.assertEqual(self.at(3,'簡遣參軍','簡')['person_id'],m['person_id']);names=[n for n in J('data/corpus/profile-names.json')['records']if n.get('id')=='name-jin090-f53-008'];self.assertEqual(len(names),1);self.assertIsNone(names[0]['ming']);ctx=J(N+'jin037-highmi-context.json');self.assertIn('孝王略，字元簡',ctx['raw_quote']);self.assertFalse(ctx['marked_chapter'])
 def test_grandfather_without_invented_father(self):
  a=next(a for a in self.a if a['id']=='a-jin090-f53-grandfather');self.assertEqual(a['predicate'],'grandfather');self.assertEqual(a['subject_person_id'],'h7n_w5t_i1c_AAA*A');self.assertEqual(a['qualifiers']['source_term'],'祖肇');proposal=J(N+'paternal-interface-proposal.json');self.assertEqual(proposal['known_root_person_id'],'h7n_w5t_i1c_AA');self.assertIsNone(proposal['grandchild_father_person_id']);self.assertFalse(proposal['family_id_rekey_applied']);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']=='h7n_w5t_i1c_AAA*A'for a in self.a))
 def test_unidentified_mother_not_birthmother(self):
  mother=self.at(2,'丁母憂','母')['person_id'];b=next(b for b in J(N+'boundary-proposals.json')if b['id']=='proposal-jin090-mother-unspecified');self.assertEqual(b['object_person_id'],mother);self.assertIsNone(b['biological_mother']);self.assertFalse(b['native_relation_added']);death=next(e for e in self.life if e['id']=='le-jin090-f53-002');self.assertEqual(death['person_id'],mother);self.assertIsNone(death['date_expression']);self.assertNotIn('normalized_date',death)
 def test_widow_not_the_dead_gumu_or_caoshus_spouse(self):
  wid=self.at(1,'寡婦','寡婦')['person_id'];gu=self.at(1,'養姑','姑')['person_id'];self.assertNotEqual(wid,gu);dead=next(e for e in self.life if e['id']=='le-jin090-f53-001');self.assertEqual(dead['person_id'],gu);self.assertFalse(any(e['person_id']==wid for e in self.life));self.assertFalse(any(a['predicate']=='spouse'and 'h7n_w5t_i1c_AAA*A'in[a['subject_person_id'],a['object_person_id']]for a in self.a))
 def test_regrant_two_luoyang_not_single_or_death_closed(self):
  rows=[h for h in self.h if h['person_id']=='h7n_w5t_i1c_AAA*A'and h['title']=='洛陽令'];self.assertEqual(len(rows),2);self.assertEqual({h['mode']for h in rows},{'transfer','grant'});self.assertNotEqual(rows[0]['attestations'][0]['start'],rows[1]['attestations'][0]['start']);self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in rows));self.assertEqual(rows[0]['office_transfer_basis']['source_term'],'轉洛陽令')
 def test_year_308_death_and_no_funeral_year_or_place(self):
  e=next(e for e in self.life if e['id']=='le-jin090-f53-003');self.assertEqual(e['person_id'],'h7n_w5t_i1c_AAA*A');self.assertEqual(e['normalized_date']['year'],308);self.assertEqual(e['source_term'],'軍敗死之');fun=next(e for e in J('corpus/jinshu/090-caoshu-events.json')['events']if e['id']=='pe-jin090-f53-burial');self.assertIsNone(fun['date_expression']);self.assertNotIn('normalized_date',fun);ads=J('corpus/jinshu/090-caoshu-addresses.json')['assertions'];self.assertTrue(any(a['relation']=='death_place'and a['place']['source_name']=='酈縣'for a in ads));self.assertFalse(any(a['relation']=='burial_place'for a in ads));at=self.ps[2]['text'].index('其年');self.assertFalse(any(m['start']==at and m['kind']=='person'for m in self.ps[2]['mentions']))
 def test_common_title_not_emperor_and_ancestor_not_live_grant(self):
  h=next(h for h in self.h if h['title']=='聖君');self.assertEqual(h['person_id'],'h7n_w5t_i1c_AAA*A');self.assertEqual(h['kind'],'honorific');self.assertEqual(h['mode'],'attestation');h=next(h for h in self.h if h['title']=='衛將軍');self.assertEqual(h['mode'],'attestation');self.assertNotIn('normalized_date',h['effective_period']['start'])
 def test_parallel_reading_is_exact_projected_not_silent_correction(self):
  c=J(N+'sanguozhi009-caoxiu-context.json');self.assertFalse(c['marked_chapter']);raw=(R/(N+'sanguozhi009-fixed.txt')).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),c['source_sha256']);self.assertEqual(''.join(x['surface']for x in c['layers']),c['projected_text']);r=next(r for r in c['note_readings']if r['cited_work']=='張隠文士傳');self.assertIn('肇孫攄字顔逺',r['text']);self.assertIn('襄陽太守',r['text']);self.assertIn('向呉戰敗死',r['text'])
  for chunk in r['chunks']:self.assertEqual(c['projected_text'][chunk['source_projected_start']:chunk['source_projected_end']],chunk['surface']);self.assertEqual(r['text'][chunk['reading_start']:chunk['reading_end']],chunk['surface'])
  self.assertTrue(any(h['title']=='襄城太守'for h in self.h));self.assertFalse(any(h['title']=='襄陽太守'for h in self.h))
 def test_full_ledger_and_poem_is_not_meeting(self):
  d=J(N+'complete-reading-ledger.json');self.assertEqual(len(d['records']),42)
  for r in d['records']:
   p=next(p for p in self.ps if p['id']==r['paragraph_id']);a=r['clause_anchor'];self.assertEqual(p['text'][a['start']:a['end']],a['surface']);self.assertEqual(r['quote'],p['text'])
  decisions=J('corpus/jinshu/090-caoshu-identity.json')['decisions'];d=next(d for d in decisions if d['id']=='d-jin090-caoshu-yanyuan');self.assertEqual(d['person_id'],'h7n_w5t_i1c_AAA*A');self.assertIn('引用前人詩不是同時相遇',d['rationale']);self.assertEqual(self.at(3,'父母焉','父母')['kind'],'unresolved')
if __name__=='__main__':unittest.main()
