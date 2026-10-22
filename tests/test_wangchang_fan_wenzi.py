import json,hashlib,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];BASE='source-evidence/sanguozhi027-fan-wenzi';PRE='c-sanguozhi-027-wangchang:'
class FanWenzi(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/sanguozhi/027-wangchang.json').read_text());cls.ms={m['id']:(p,m)for p in cls.c['paragraphs']for m in p['mentions']};cls.review=json.loads((R/BASE/'decision.json').read_text());cls.rows={x['mention_id']:x for x in cls.review['decisions']};cls.decs=json.loads((R/'corpus/sanguozhi/027-wangchang-identities.json').read_text())['decisions']
 def test_seven_exact_name_anchors_not_pronouns(self):
  self.assertEqual(len(self.rows),7)
  for mid,row in self.rows.items():
   p,m=self.ms[mid];self.assertEqual(p['text'][row['start']:row['end']],row['surface']);self.assertEqual(m['kind'],'person');self.assertEqual(m['person_id'],row['person_id']);self.assertEqual(m['status'],'contextual_provisional')
  for mid in ['unit006:m0032','unit006:m0050','unit006:m0051','unit006:m0059']:self.assertEqual(self.ms[PRE+mid][1]['kind'],'unresolved')
 def test_received_fangai_and_quoted_error_are_not_same_event_role(self):
  event=self.rows[PRE+'unit005:m0417'];literal=self.rows[PRE+'unit006:m0089'];self.assertEqual(event['surface'],literal['surface']);self.assertNotEqual(event['person_id'],literal['person_id']);self.assertEqual(event['reading_role'],'event_role_editorial_preferred');self.assertEqual(literal['reading_role'],'metalinguistic_received_name');self.assertTrue(literal['does_not_assert_literal_person_participated']);self.assertEqual(event['event_role_person_id'],literal['event_role_person_id']);self.assertEqual(event['received_name_person_id'],literal['person_id'])
 def test_preferred_reading_does_not_change_received_glyph_or_global_alias(self):
  d=next(x for x in self.decs if x['id']=='d-sgz027-wenzi-event-role');reading=d['preferred_reading'];self.assertEqual(reading['received_surface'],'范匄');self.assertEqual(reading['preferred_surface'],'范燮');self.assertTrue(reading['source_spelling_is_not_alias']);v=next(v for v in self.c['annotation']['reported_variants']if v['id']==reading['variant_id']);self.assertFalse(v['adopted']);self.assertFalse(v['image_verified']);self.assertEqual(v['status'],'reported_not_collated');self.assertIn('此云范匄盖誤',v['quote']);self.assertIn('若范匄對秦客',self.ms[PRE+'unit005:m0417'][0]['text'])
 def test_wuzi_is_shihui_not_wangji_or_other_wuzi(self):
  ids={self.ms[PRE+x][1]['person_id']for x in ['unit005:m0423','unit006:m0010','unit006:m0036']};self.assertEqual(ids,{'wt0_abc_2sk'});self.assertNotIn('a8f_ec8_e74_ABB',ids)
 def test_registry_reverse_evidence_only_exact_mentions(self):
  reg={p['id']:p for p in json.loads((R/'registry/persons.json').read_text())['persons']}
  for mid,row in self.rows.items():
   p=reg[row['person_id']];self.assertTrue(any(e.get('mention_id')==mid and e['quote']==row['surface']for e in p['evidence']));self.assertTrue(any(a['surface']==row['surface']and mid in a['mention_ids']for a in p['aliases']))
 def test_fixed_primary_bytes_and_exact_read_spans(self):
  meta=json.loads((R/BASE/'primary/metadata.json').read_text());raw=(R/BASE/'primary/guoyu011-1998990.wikitext').read_bytes();self.assertEqual(meta['revision_id'],1998990);self.assertEqual(hashlib.sha256(raw).hexdigest(),meta['raw_sha256']);response=(R/BASE/'primary/guoyu011-response.json').read_bytes();self.assertEqual(hashlib.sha256(response).hexdigest(),meta['response_sha256']);refs=json.loads((R/BASE/'parallel-reading.json').read_text())['references'];ref=next(x for x in refs if x['path'].startswith('primary/'));self.assertEqual(raw.decode()[ref['raw_start']:ref['raw_end']],ref['quote']);self.assertIn('武子，晉正卿士會',ref['quote']);self.assertIn('燮，武子之子文子也',ref['quote']);self.assertIn('燮也受命於中軍',ref['quote'])
 def test_existing_wenzi_identity_materialized_source_first(self):
  case=next(x for x in self.c['annotation']['resolved_identity_cases']if x['id']=='case-sgz027-wenzi-shixie-existing-duplicate');self.assertEqual(case['status'],'contextual_provisional');self.assertEqual(case['person_id'],'cno_x3i_mx4');self.assertEqual(case['identity_equivalence_decision_ids'],['eq-wenzi-shixie-materialized']);self.assertFalse(any(x['id']==case['id']for x in self.c['annotation']['unresolved_identity_cases']))
 def test_all_original_text_layers_source_fields_exact(self):
  cap=json.loads((R/BASE/'complete-unit-reading.json').read_text());self.assertEqual([{k:p[k]for k in ['id','text','text_layer','source_position']if k in p}for p in self.c['paragraphs']],cap['paragraphs']);self.assertEqual(len(self.c['paragraphs']),20)
if __name__=='__main__':unittest.main()
