"""完整韓鍾來源的角色、字位與反例；只讀實際原生資料，不依賴私有封存路徑。"""
from pathlib import Path
import json,unittest,copy,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.maternal_roles import maternal_role_valid
J=lambda rel:json.loads((ROOT/rel).read_text())
class HanZhongSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=J('corpus/houhanshu/062.json');cls.ps={p['id']:p for p in cls.c['paragraphs']};cls.new=[p for p in cls.c['paragraphs']if ':hanzhong:'in p['id']]
  cls.rel=[a for a in J('corpus/houhanshu/062-assertions.json')['assertions']if a['id'].startswith('a-houhanshu062-hanzhong-')]
 def test_full_units_and_literal_projection(self):
  proof=J('source-evidence/houhan062-hanzhong-projection.json');raw=(ROOT/proof['managed_raw_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),proof['raw_sha256']);lines=raw.decode().splitlines()
  self.assertEqual(len(self.new),8)
  for u in proof['units']:self.assertEqual(''.join(lines[r['raw_line']-1][r['raw_start']:r['raw_end']]for r in u['raw_runs']),u['text'])
  for p in self.new:
   for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
 def test_mother_unspecified_and_negative_birth_father(self):
  a=next(a for a in self.rel if a['predicate']=='maternal_role');ps={k:(self.c['id'],p)for k,p in self.ps.items()};self.assertTrue(maternal_role_valid(a,ps))
  for field,value in [('biological_mother',True),('father_person_id','hsd_7jd_t7u')]:
   bad=copy.deepcopy(a);bad['qualifiers'][field]=value;self.assertFalse(maternal_role_valid(bad,ps))
 def test_mother_wrong_subject_and_quote_rejected(self):
  a=copy.deepcopy(next(a for a in self.rel if a['predicate']=='maternal_role'));ps={k:(self.c['id'],p)for k,p in self.ps.items()}
  a['subject_person_id']='8qt_232_3b9';self.assertFalse(maternal_role_valid(a,ps))
  a=copy.deepcopy(next(a for a in self.rel if a['predicate']=='maternal_role'));a['evidence'][0]['quote']='瑾母膺之姑也';self.assertFalse(maternal_role_valid(a,ps))
 def test_direct_father_and_no_di_to_jin(self):
  pairs={(a['subject_person_id'],a['object_person_id'])for a in self.rel if a['predicate']=='father'}
  self.assertEqual(pairs,{('2i1_5qk_vfp','r9j_2e4_j6o'),('9hu_q3h_aug','hsd_7jd_t7u')})
  self.assertNotIn(('t21_7n1_rl0','hsd_7jd_t7u'),pairs)
 def test_body_grandson_and_quoted_father_separated(self):
  a=next(a for a in self.rel if a['predicate']=='father'and a['subject_person_id']=='9hu_q3h_aug');p=self.ps[a['evidence'][0]['paragraph_id']]
  self.assertEqual(p['text_layer'],'witness_appended_lixian_note');self.assertIn('海内先賢傳',[q['received_title']for q in p['layer_attribution']['quotation_dependencies']])
  g=next(a for a in self.rel if a['predicate']=='grandfather'and a['subject_person_id']=='9hu_q3h_aug');self.assertEqual(self.ps[g['evidence'][0]['paragraph_id']]['text_layer'],'received_chapter')
 def test_sister_wife_not_mother_or_absolute_rank(self):
  s=next(a for a in self.rel if a['predicate']=='spouse');self.assertEqual((s['subject_person_id'],s['object_person_id']),('t21_7n1_rl0','cpd_w3u_3w1'))
  sister=next(a for a in self.rel if a['predicate']=='sister');order=sister['qualifiers']['relative_birth_order'];self.assertEqual(order['older_person_id'],'8qt_232_3b9');self.assertEqual(order['younger_person_id'],'cpd_w3u_3w1')
 def test_death_and_age_subjects_no_inferred_year(self):
  events=[x for x in J('corpus/houhanshu/062-life-events.json')['events']if x['id'].startswith('le-houhan062-hanzhong-')];self.assertEqual(len(events),3)
  self.assertEqual({x['person_id']for x in events},{'r9j_2e4_j6o','2i1_5qk_vfp','foc_gnk_id0'})
  ages=[x for x in self.c['annotation']['age_assertions']if x['id'].startswith('age-houhan062-hanzhong-')];self.assertEqual({(x['person_id'],x['value'])for x in ages},{('2i1_5qk_vfp',70),('foc_gnk_id0',69)})
  for x in ages:self.assertIsNone(x['birth_year']);self.assertIsNone(x['date_expression'])
  for x in events:self.assertIsNone(x['date_expression']);self.assertNotIn('卒保身全家',x['source_term'])
 def test_vocab_not_brother_or_active_appointment(self):
  proposals=J('source-evidence/houhan062-hanzhong-retained-proposals.json');r=proposals['records'];v=next(x for x in r if x['kind']=='vocal_appellation_not_sibling');self.assertFalse(v['sibling_assertion_created'])
  self.assertFalse(any(a['predicate']=='brother'and a['subject_person_id']=='t21_7n1_rl0'and a['object_person_id']=='8qt_232_3b9'for a in self.rel))
  n=next(x for x in r if x.get('service_status')=='not_taken_up');self.assertIn('皆不就',n['source_anchor']['surface'])
 def test_source_qualification_and_indexes(self):
  for p in self.new:self.assertFalse(p['source_position'].get('image_verified',False))
  q=J('source-evidence/houhan062-hanzhong-retained-proposals.json');idx=q['person_index']
  for r in q['records']:
   for pid in r['person_ids']:self.assertIn(r['id'],idx[pid])
if __name__=='__main__':unittest.main()
