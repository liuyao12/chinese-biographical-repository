import copy,json,unittest,hashlib,re
from pathlib import Path
from scripts.fixed_kanripo_fact_slots import records,valid
ROOT=Path(__file__).resolve().parents[1]
class PeiqianTyped(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/sanguozhi/023-peiqian.json').read_text());cls.rs=[r for r in records(cls.ch,ROOT)if r.get('fixed_source_fact_binding',{}).get('slot','').startswith('pqt-')];cls.by={r['fixed_source_fact_binding']['slot']:r for r in cls.rs}
 def test_all_finite_records_and_exact_types(self):
  self.assertEqual(len(self.rs),68);self.assertEqual(len(self.by),68)
  self.assertTrue(all(valid(r,self.ch,ROOT)for r in self.rs))
 def test_father_direction_and_co_moved_wrong_roles_rejected(self):
  r=copy.deepcopy(self.by['pqt-001']);r['subject_person_id'],r['object_person_id']=r['object_person_id'],r['subject_person_id']
  for e in r['evidence']:e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
  self.assertFalse(valid(r,self.ch,ROOT))
  r=copy.deepcopy(self.by['pqt-001']);r['predicate']='adoptive_father';self.assertFalse(valid(r,self.ch,ROOT))
 def test_hui_brother_not_explicit_mao_father(self):
  self.assertNotIn('pqt-004',self.by);r=self.by['pqt-002'];self.assertEqual(r['predicate'],'brother');self.assertEqual(r['qualifiers']['source_term'],'潛少弟徽')
  o=r['qualifiers']['relative_birth_order'];self.assertEqual(o['younger_person_id'],r['subject_person_id']);self.assertEqual(o['older_person_id'],r['object_person_id'])
 def test_kuo_cross_letter_complete_source_and_no_wrong_father(self):
  r=next(r for r in self.rs if r.get('predicate')=='father'and r['qualifiers']['source_term']=='次廓');self.assertEqual(len(r['evidence']),2);self.assertIn('王曠與司馬越書曰',r['evidence'][0]['quote']);self.assertTrue(r['evidence'][1]['quote'].startswith('次廓'))
  q=copy.deepcopy(r);q['evidence']=q['evidence'][:1];self.assertFalse(valid(q,self.ch,ROOT))
 def test_no_absolute_ordinal_from_source_list_head(self):
  claims=[r for r in self.rs if 'birth_order'in r.get('qualifiers',{})];self.assertEqual(len(claims),1);self.assertEqual(claims[0]['qualifiers']['birth_order']['ordinal'],1);self.assertIn('長子黎',claims[0]['qualifiers']['source_term'])
  for r in self.rs:
   o=r.get('qualifiers',{}).get('relative_birth_order')
   if o:self.assertIsNone(o['older_ordinal']);self.assertIsNone(o['younger_ordinal'])
 def test_congfudi_preserves_specific_literal_without_invented_ancestors(self):
  r=next(r for r in self.rs if r.get('predicate')=='agnatic_cousin');self.assertEqual(r['qualifiers']['source_term'],'頠從父弟邈');self.assertEqual(r['qualifiers']['source_paternal_path_term'],'從父弟');self.assertIsNone(r['qualifiers']['kinship_structure']['common_ancestor_person_id']);self.assertEqual(r['qualifiers']['reported_kinship_path'],['father','brother','son']);self.assertEqual(r['qualifiers']['reported_kinship_path_direction'],'object_to_subject');self.assertEqual(r['qualifiers']['reported_kinship_path_from_person_id'],r['object_person_id']);self.assertEqual(r['qualifiers']['reported_kinship_path_to_person_id'],r['subject_person_id']);self.assertIs(r['qualifiers']['reported_kinship_path_interpretation']['human_reviewed'],False)
  bad=copy.deepcopy(r);bad['qualifiers']['source_paternal_path_term']='從弟';self.assertFalse(valid(bad,self.ch,ROOT));bad=copy.deepcopy(r);bad['qualifiers']['reported_kinship_path_direction']='subject_to_object';self.assertFalse(valid(bad,self.ch,ROOT))
 def test_dates_bind_only_qian_death_not_offices(self):
  ev=next(r for r in self.rs if r.get('event_type')=='death');self.assertEqual(ev['date_expression'],'正始五年');self.assertEqual(ev['normalized_date']['year'],244)
  for r in self.rs:
   if 'attestations'in r:
    self.assertIsNone(r['effective_period']['start']['date_expression'])
    if r['id']=='th-sgz023-peiqian-pqt-049':
     from scripts.fixed_peiqian_structural import office_end_valid
     self.assertEqual(r['end_basis']['departure_event_id'],'pe-sgz023-peiqian-phaseb-005-office-departure');self.assertEqual(r['end_basis']['prior_office_anchor']['surface'],'尚書令');self.assertEqual(r['end_basis']['following_office_anchor']['surface'],'拜光祿大夫');self.assertIsNone(r['effective_period']['end']['date_expression']);self.assertTrue(office_end_valid(r,self.ch,ROOT))
    else:self.assertEqual(r['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]})
    self.assertNotIn('normalized_date',r['effective_period']['end'])
  bad=copy.deepcopy(ev);bad['normalized_date']['year']=245;self.assertFalse(valid(bad,self.ch,ROOT))
 def test_unrealized_duke_and_staff_duty_not_holdings(self):
  hs=[r for r in self.rs if 'attestations'in r];self.assertNotIn('公',[h['title']for h in hs]);self.assertNotIn('參丞相軍事',[h['title']for h in hs]);self.assertTrue(any(r.get('source_term')=='時遠近皆云當為公'for r in self.rs))
  self.assertEqual(next(h for h in hs if h['title']=='太常')['mode'],'posthumous_grant');self.assertEqual(next(h for h in hs if h['title']=='貞侯')['mode'],'posthumous_naming')
 def test_raw_source_wrong_role_or_era_insertion_rejected(self):
  ch=copy.deepcopy(self.ch);p=ch['paragraphs'][6];start=p['text'].index('元康')+1;p['mentions'].append({'id':p['id']+':bad','start':start,'end':start+1,'surface':'康','kind':'person','person_id':next(m['person_id']for m in ch['paragraphs'][9]['mentions']if m['surface']=='康')});p['mentions'].sort(key=lambda m:m['start']);self.assertFalse(valid(self.rs[0],ch,ROOT))
  ch=copy.deepcopy(self.ch);ch['source']['response_sha256']='0'*64;self.assertFalse(valid(self.rs[0],ch,ROOT))
 def test_no_native_marriage_or_mother_fabrication(self):
  self.assertFalse(any(r.get('predicate')in ['spouse','mother','adoptive_father']for r in self.rs));self.assertFalse(any(r.get('event_type')=='birth'for r in self.rs))
 def test_fixed_official_era_row_and_name_variants(self):
  proof=json.loads((ROOT/'source-evidence/sgz023-peiqian-typed/calendar-equivalence.json').read_text());raw=(ROOT/proof['source_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),proof['raw_sha256'])
  if proof.get('source_storage_kind')=='selected_official_table_rows':
   excerpt=json.loads(raw);self.assertEqual(excerpt['record_type'],'official_era_table_row_excerpt_set');self.assertEqual(excerpt['source_response_sha256'],proof['source_response_sha256']);entry,=[r for r in excerpt['rows']if r['row_id']==proof['row_id']];row=entry['complete_html_table_row'];self.assertEqual((entry['dynasty'],entry['era_name'],entry['first_year'],entry['last_year']),('魏','正始',240,249))
  else:row=re.search(r"<tr id='av445'>.*?</tr>",raw.decode(),re.S).group()
  self.assertEqual(row,proof['complete_html_table_row']);self.assertIn('正始',row);self.assertIn('240',row);self.assertIn('249',row)
  ev=next(r for r in self.rs if r.get('event_type')=='death');self.assertEqual(ev['normalized_date']['references'][0]['url'],proof['url']);self.assertEqual(proof['url'],'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1');self.assertEqual(proof['common_era_chinese_civil_year'],240+5-1)
  li=next(r for r in self.rs if r.get('ming')=='黎');self.assertEqual(li['zi'],'伯宗');self.assertEqual(li['additional_names'],['一名演']);self.assertIn('黎字伯宗一名演',li['quote'])
 def test_duration_and_estate_link_exact_holding(self):
  hs={r['id']:r for r in self.rs if 'attestations'in r}
  for kind,title in [('service_duration','代郡太守'),('enfeoffment_households','清陽亭侯')]:
   d=next(r for r in self.rs if r.get('kind')==kind);h=hs[d['values']['linked_holding_id']];self.assertEqual(h['title'],title);self.assertEqual(h['person_id'],d['person_id']);bad=copy.deepcopy(d);bad['values']['linked_holding_id']='th-not-source';self.assertFalse(valid(bad,self.ch,ROOT))
 def test_complete_lexical_child_pages_not_parent_transclusion_claim(self):
  lex=json.loads((ROOT/'source-evidence/sgz023-peiqian-typed/erya-congfudi-lexical-context.json').read_text());self.assertEqual([r['revision']for r in lex['pages']],[1138113,1138114,1138115]);self.assertIs(lex['image_verified'],False);pieces=[]
  for r in lex['pages']:
   raw=(ROOT/r['raw_file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);a=r['unit_slice'];self.assertEqual(raw.decode()[a['start']:a['end']],a['literal']);pieces.append(a['literal'])
  self.assertEqual(''.join(pieces),lex['complete_unit_transcription_wikitext']);self.assertIn(lex['literal_lexical_rule'],pieces[1]);self.assertTrue(pieces[0].startswith('釋親第四'));self.assertTrue(pieces[-1].endswith('宗族'));self.assertIn('母頁revision不凍結嵌入正文',lex['parent_capture_qualification'])
if __name__=='__main__':unittest.main()
