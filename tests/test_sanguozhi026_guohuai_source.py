import json,hashlib,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'corpus/sanguozhi/026-guohuai.json').read_text());PS={p['id'].rsplit(':',1)[-1]:p for p in C['paragraphs']};REG={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']}
def hits(unit,surface):return[m for m in PS[unit]['mentions']if m['surface']==surface]
class GuohuaiSourceTests(unittest.TestCase):
 def test_complete_extent_and_layers(self):
  self.assertEqual(len(PS),18);self.assertEqual(sum(p['text_layer']=='witness_appended_pei_songzhi_note'for p in PS.values()),3);self.assertFalse(C['source']['image_verified']);self.assertIn('未匯',C['source']['extent'])
 def test_exact_projection(self):
  raw=(R/C['source']['raw_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),C['source']['raw_file_sha256']);lines=raw.decode().splitlines(keepends=True)
  for p in PS.values():
   fs=p['source_position']['source_fragments'];self.assertEqual(''.join(f['text']for f in fs),p['text'])
   for f in fs:self.assertEqual(lines[f['line']-1][f['raw_start']:f['raw_end']],f['text'])
 def test_all_reverse_endpoints_and_exact_spans(self):
  for p in PS.values():
   ranges=[]
   for m in p['mentions']:
    self.assertEqual(p['text'][m['start']:m['end']],m['surface']);self.assertTrue(all(m['end']<=a or m['start']>=b for a,b in ranges));ranges.append((m['start'],m['end']))
    if m['kind']!='person':continue
    row=REG[m['person_id']];self.assertTrue(any(m['id']in a['mention_ids']and a['surface']==m['surface']for a in row['aliases']));self.assertTrue(any(e['mention_id']==m['id']and e['quote']==m['surface']for e in row['evidence']))
 def test_false_character_splits_absent(self):
  self.assertFalse(any(m['start']==25 for m in PS['unit004']['mentions']));self.assertFalse(any(m['surface']=='正'and m['start']==0 for m in PS['unit015']['mentions']));self.assertFalse(any(m['surface']=='展' for m in PS['unit014']['mentions']));self.assertFalse(any(m['surface']=='備'for m in PS['unit006']['mentions']))
 def test_guoyi_other_family_not_used(self):
  self.assertEqual(hits('unit016','奕')[0]['person_id'],'r02_hoi_pu7_ACA');self.assertTrue(all(m.get('person_id')!='344_68f_98e_A'for p in PS.values()for m in p['mentions']));self.assertEqual(hits('unit016','泰業')[0]['person_id'],'r02_hoi_pu7_ACA')
 def test_guohuai_common_event_and_emperor_scope(self):
  self.assertEqual(hits('unit001','郭淮')[0]['person_id'],'r02_hoi_pu7_AA');self.assertEqual(hits('unit003','文帝')[0]['person_id'],'tix_jqk_w1o');self.assertEqual(hits('unit013','朕')[0]['person_id'],'1b6_503_da8');self.assertNotEqual(hits('unit003','文帝')[0]['person_id'],hits('unit013','朕')[0]['person_id'])
 def test_variants_not_normalized(self):
  self.assertIn('父緼',PS['unit002']['text']);self.assertIn('父縕',PS['unit018']['text']);self.assertIn('縕作蘊',PS['unit018']['text']);self.assertEqual(hits('unit002','緼')[0]['person_id'],hits('unit018','蘊')[0]['person_id'])
 def test_unnamed_title_son_not_heir(self):
  one=hits('unit013','一子')[0];self.assertEqual(one['kind'],'unresolved');self.assertIsNone(one['person_id']);self.assertNotEqual(one.get('person_id'),hits('unit015','統')[0]['person_id'])
 def test_kin_roles_not_false_ranking(self):
  self.assertNotEqual(hits('unit016','配')[0]['person_id'],hits('unit015','統')[0]['person_id']);self.assertEqual(hits('unit016','女')[0]['person_id'],'4rl_6u1_b3j');self.assertTrue(any('父歸屬未定'in s for s in C['annotation']['limitations']))
 def test_no_unstated_fathers_added_by_later_typed_sets(self):
  path=R/'corpus/sanguozhi/026-guohuai-assertions.json'
  if not path.exists():return
  pairs={(a['subject_person_id'],a['object_person_id'])for a in json.loads(path.read_text())['assertions']if a['predicate']=='father'}
  self.assertNotIn((hits('unit002','緼')[0]['person_id'],hits('unit002','全')[0]['person_id']),pairs)
  self.assertNotIn((hits('unit016','豫')[0]['person_id'],hits('unit016','配')[0]['person_id']),pairs)
 def test_work_citations_preserve_layer(self):
  self.assertEqual(hits('unit014','世語')[0]['work_id'],'w-shiyu-sgz027-reference');self.assertEqual(hits('unit016','晉諸公贊')[0]['work_id'],'w-jinzhugongzan-sgz022-luyu-reference');self.assertEqual(hits('unit016','山濤啓事')[0]['kind'],'work');self.assertFalse(hits('unit016','山濤'))
 def test_metadata_three_layers(self):
  d=json.loads((R/'registry/work-provenance.json').read_text());b=d['text_bases'][C['source_id']];self.assertIsNone(b['edition_id']);self.assertIsNone(b['earliest_extant_basis_edition_id']);self.assertEqual(b['status'],'not_researched');self.assertEqual(d['works']['w-guoshi-pu-sgz026-reference']['composition']['assertions'],[])
if __name__=='__main__':unittest.main()
