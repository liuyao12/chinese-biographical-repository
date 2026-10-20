# coding: utf-8
"""Complete fixed Wei shu 038 source regression; no private packet dependencies."""
import unittest,json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CID='c-weishu-weishou-038-wanghuilong';PREFIX='corpus/weishu-weishou/038-wanghuilong'
def read(n):return json.loads((ROOT/n).read_text())
class WeiShu038Source(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read(PREFIX+'.json');cls.ps={p['id'].split(':')[-1]:p for p in cls.c['paragraphs']};cls.ids=read('tests/fixtures/weishu038-wanghuilong.json')['identities'];cls.rels=read(PREFIX+'-assertions.json')['assertions'];cls.ts=read(PREFIX+'-titles.json')['holdings'];cls.audit=read('source-evidence/weishu038-wang44-consumption.json')['proposal_records']
 def test_fixed_whole_unit_and_shared_appraisal(self):
  self.assertEqual(len(self.c['paragraphs']),9);self.assertEqual(sum(len(p['text'])for p in self.c['paragraphs']),2189);self.assertTrue(self.ps['unit001']['text'].startswith('王慧龍自云'));self.assertTrue(self.ps['unit008']['text'].endswith('遵業子松年尚書庫部郎'));self.assertTrue(self.ps['shared-appraisal']['text'].startswith('史臣曰刁雍'));self.assertEqual(len(self.ps['shared-appraisal']['text']),85)
  raw=(ROOT/self.c['source']['raw_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),'07faab280233959bfa89a0354119c2b67f7ad1f23c1e1b8ebd67deb6927e6deb');self.assertEqual(self.c['source']['source_commit'],'17b6525eb5aaa878b9640f5a61e90da934ce5fc4')
 def test_every_unicode_anchor_and_raw_position(self):
  raw=(ROOT/self.c['source']['raw_path']).read_text().splitlines();count=0
  for p in self.c['paragraphs']:
   end=0;positions=p['source_position']['raw_character_positions'];self.assertEqual(len(positions),len(p['text']))
   self.assertEqual(''.join(raw[a['line']-1][a['column']]for a in positions),p['text'])
   for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end'];count+=1
  self.assertEqual(count,328)
 def test_native_xml_is_canonical_and_text_exact(self):
  from scripts.render_corpus import render
  self.assertEqual((ROOT/(PREFIX+'.xml')).read_text(),render(self.c));xp=ET.fromstring((ROOT/(PREFIX+'.xml')).read_text());self.assertEqual([''.join(p.itertext())for p in xp.findall('p')],[p['text']for p in self.c['paragraphs']])
 def test_explicit_four_generation_chain(self):
  for child,parent in [('寳興','慧龍'),('瓊','寳興'),('遵業','瓊'),('松年','遵業')]:self.assertTrue(any(a['predicate']=='father'and a['subject_person_id']==self.ids[child]and a['object_person_id']==self.ids[parent]for a in self.rels))
  root=self.ids['慧龍'];self.assertEqual([self.ids[k]for k in ['寳興','瓊','遵業','松年']],[root+'_A',root+'_AA',root+'_AAA',root+'_AAAA'])
 def test_claimed_grandfather_never_becomes_plain_parent(self):
  self.assertFalse(any(a['subject_person_id']==self.ids['慧龍']and a['predicate']in ['father','grandfather','adoptive_father']for a in self.rels));cases=[r for r in self.audit if r['category']=='contested_parentage'];self.assertEqual(len(cases),2);self.assertTrue(all(r['claim']['selected']is False and r['claim']['adoption']is False for r in cases));self.assertIn('其自言也如此',self.ps['unit001']['text']);self.assertIn('僧彬所通生也',self.ps['unit002']['text'])
 def test_cui_tian_daughter_not_cui_hao_daughter(self):
  a=next(a for a in self.rels if a['subject_person_id']==self.ids['慧龍妻']and a['predicate']=='father');self.assertEqual(a['object_person_id'],self.ids['恬']);self.assertNotEqual(a['object_person_id'],self.ids['浩']);self.assertIn('崔浩弟恬',a['evidence'][0]['quote'])
 def test_lu_wife_source_slots_and_unknown_mother_not_forced(self):
  self.assertNotEqual(self.ids['遐前妻'],self.ids['遐後妻']);candidate=next(r for r in self.audit if r['category']=='maternal_aunt')['claim']['wife_identity_comparison'];self.assertIsNone(candidate['selected_same_person']);self.assertIsNone(candidate['selected_distinct_people']);self.assertNotEqual(self.ids['寳興母'],self.ids['慧龍妻']);self.assertFalse(any(a['predicate']in ['mother','adoptive_mother']for a in self.rels));self.assertTrue(any(r['category']=='maternal_role'and r['claim']['biological']is None for r in self.audit))
 def test_qiong_daughters_not_merged_or_made_mothers(self):
  self.assertNotEqual(self.ids['瓊長女'],self.ids['瓊盧女']);self.assertTrue(any(a['predicate']=='spouse'and a['subject_person_id']==self.ids['瓊長女']and a['object_person_id']==self.ids['高祖']for a in self.rels));self.assertTrue(any(a['predicate']=='spouse'and a['subject_person_id']==self.ids['瓊盧女']and a['object_person_id']==self.ids['道亮']for a in self.rels))
 def test_source_ordinals_and_unknown_three_sons(self):
  a=next(a for a in self.rels if a['subject_person_id']==self.ids['遵業']and a['predicate']=='father');o=a['qualifiers']['birth_order'];self.assertEqual(o['ordinal'],1);self.assertEqual(o['position'],'eldest');e=o['evidence'][0];p=next(p for p in self.c['paragraphs']if p['id']==e['paragraph_id']);self.assertEqual(p['text'][e['start']:e['end']],'長子遵業');r=next(r for r in self.audit if r['category']=='children_count'and r['person_source_key']=='瓊');self.assertEqual(r['claim']['sons'],4);self.assertEqual(r['claim']['unknown_names'],3)
 def test_assassin_spellings_and_interlocutor(self):
  p=self.ps['unit004'];m=next(m for m in p['mentions']if m['surface']=='老子');self.assertEqual(m['person_id'],self.ids['彦之']);self.assertTrue(any(m['surface']=='呂𤣥伯'and m['person_id']==self.ids['元伯']for m in p['mentions']));self.assertTrue(any(m['surface']=='吕元伯'and m['person_id']==self.ids['元伯']for m in self.ps['unit005']['mentions']))
 def test_lacuna_and_identity_candidates(self):
  self.assertIn('嘗盛服(闕/)寵勢亦不足恨',self.ps['unit007']['text']);self.assertEqual(sum(p['text'].count('(闕/)')for p in self.c['paragraphs']),1)
  for surface in ['王騰','王顯','元又','東海']:
   self.assertTrue(any(m['surface']==surface and m['kind']=='unresolved'and m['person_id']is None for p in self.c['paragraphs']for m in p['mentions']))
 def test_appointment_not_assumption_or_terminal_death(self):
  r=next(r for r in self.audit if r['category']=='appointment_not_assumed');self.assertFalse(r['claim']['assumed_post']);h=next(h for h in self.ts if h['title']=='虎牢鎮都副將');self.assertEqual(h['mode'],'grant');self.assertEqual(sum(h['effective_period']['end']['status']!='unknown'for h in self.ts),2)
 def test_death_age_and_lifetime_age_not_births(self):
  aa=self.c['annotation']['age_assertions'];self.assertEqual(len(aa),2);fourteen=next(a for a in aa if a['value']==14);seventyfour=next(a for a in aa if a['value']==74);self.assertEqual(fourteen['age_context'],{'kind':'during_life'});self.assertEqual(seventyfour['age_context']['kind'],'at_death');self.assertTrue(all(a['birth_year']is None for a in aa))
 def test_no_point_for_middle_era_or_unknown_qiong_death(self):
  ranges=[h['effective_period']['start']['normalized_date_range']for h in self.ts if 'normalized_date_range'in h['effective_period']['start']];self.assertEqual(len(ranges),3);self.assertTrue(all('year'not in d and d['precision']=='year_range'for d in ranges));events=read(PREFIX+'-life-events.json')['events'];q=next(e for e in events if e['person_id']==self.ids['瓊']);self.assertIsNone(q['date_expression']);self.assertNotIn('normalized_date',q)
 def test_posthumous_not_lifetime_titles(self):
  naming=[h for h in self.ts if h['mode']=='posthumous_naming'];self.assertEqual([h['title']for h in naming],['穆侯']);typed=[r for r in self.audit if r['category']=='title'and r['claim']['mode']=='posthumous_grant'];self.assertEqual(len(typed),6);self.assertTrue(all(r['consumption']['state']=='native'and 'native_candidate'in r for r in typed));self.assertFalse(any(h['title']=='荆州刺史'and h['person_id']==self.ids['慧龍']and h['mode']!='posthumous_grant'for h in self.ts));self.assertEqual(len([h for h in self.ts if h['mode']=='posthumous_grant']),6)
 def test_group_office_anchor_points_to_actual_clause(self):
  for h in self.ts:
   if h['title']=='司徒左長史'and h['person_id']==self.ids['遵業']:self.assertEqual(self.ps['unit008']['text'][h['attestations'][0]['start']-1:h['attestations'][0]['end']],'轉司徒左長史')
   if h['title']=='黄門郎'and h['person_id']in [self.ids['翻'],self.ids['誦']]:self.assertEqual(self.ps['unit008']['text'][h['attestations'][0]['start']-2:h['attestations'][0]['end']],'並領黄門郎')
 def test_full_ledger_and_false_review(self):
  self.assertEqual(len(self.audit),460);self.assertEqual(len({r['id']for r in self.audit}),460);self.assertTrue(all(r['human_reviewed']is False for r in self.audit));self.assertEqual(len(self.rels),19);self.assertEqual(len(self.ts),65)
if __name__=='__main__':unittest.main()
