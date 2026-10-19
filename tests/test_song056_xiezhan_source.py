# coding: utf-8
import pathlib,json,hashlib,copy,unittest,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());C=J(ROOT/'corpus/songshu/056-xiezhan.json');A=J(ROOT/'corpus/songshu/056-xiezhan-assertions.json')['assertions'];EV=J(ROOT/'source-evidence/song056-xiezhan-projection.json');RAW=(ROOT/EV['raw_path']).read_text();LINES=RAW.splitlines();Q=J(ROOT/'source-evidence/song056-xiezhan-typed-proposals.json')['proposals'];B=J(ROOT/'source-evidence/song056-huan-identity-bridge.json')
def ms(n):return C['paragraphs'][n-1]['mentions']
def pid(n,t):return next(m['person_id']for m in ms(n)if m['surface']==t)
def valid(d,e):
 try:
  if d['source']['source_commit']!='e80c057667e3c8684f11d5088251e10244d5a264'or hashlib.sha256(RAW.encode()).hexdigest()!=e['source_metadata']['raw_sha256']:return False
  return len(d['paragraphs'])==len(e['paragraphs'])and all(p['id']==pr['paragraph_id']and p['text']==''.join(LINES[x['raw_line']-1][x['raw_start']:x['raw_end']]for x in pr['runs'])for p,pr in zip(d['paragraphs'],e['paragraphs']))
 except(KeyError,IndexError,TypeError):return False
class XiezhanSource(unittest.TestCase):
 def test_complete_unit_boundary(self):
  self.assertEqual(len(C['paragraphs']),3);self.assertEqual(sum(len(p['text'])for p in C['paragraphs']),740);self.assertTrue(C['paragraphs'][0]['text'].startswith('謝瞻字宣逺'));self.assertTrue(C['paragraphs'][-1]['text'].endswith('又早卒無後'));self.assertNotIn('孔琳之字彦琳',''.join(p['text']for p in C['paragraphs']))
 def test_exact_raw_projection(self):self.assertTrue(valid(C,EV))
 def test_reject_silent_huan_correction(self):
  d=copy.deepcopy(C);d['paragraphs'][1]['text']=d['paragraphs'][1]['text'].replace('奐','瑍');self.assertFalse(valid(d,EV))
 def test_reject_other_revision(self):
  d=copy.deepcopy(C);d['source']['source_commit']='0'*40;self.assertFalse(valid(d,EV))
 def test_reject_skipped_raw_line(self):
  e=copy.deepcopy(EV);e['paragraphs'][0]['runs'][0]['raw_line']+=1;self.assertFalse(valid(C,e))
 def test_reject_duplicate_body(self):
  d=copy.deepcopy(C);d['paragraphs'].append(copy.deepcopy(d['paragraphs'][-1]));self.assertFalse(valid(d,EV))
 def test_existing_zhan_and_direct_alternate_name(self):
  for t in ['謝瞻','檐','宣逺','通逺']:self.assertEqual(pid(1,t),'aa6_83c_juy_AAAD')
 def test_third_older_brother_no_absolute_ordinal(self):
  a=next(x for x in A if x['subject_person_id']=='aa6_83c_juy_AAAD'and x['predicate']=='brother');self.assertEqual(a['object_person_id'],'aa6_83c_juy_AAAA');self.assertEqual(a['qualifiers']['source_term'],'第三兄');o=a['qualifiers']['relative_birth_order'];self.assertEqual(o['older_person_id'],'aa6_83c_juy_AAAD');self.assertIsNone(o['older_ordinal']);self.assertIsNone(o['younger_ordinal']);self.assertNotIn('birth_order',a['qualifiers'])
 def test_uncle_care_not_adoption_or_birthmother(self):
  u=pid(1,'劉');self.assertFalse(any(a['object_person_id']==u and a['predicate']in ['mother','adoptive_mother','adoptive_father']for a in A));q=next(q for q in Q if q['kind']=='raised_by_fuyang');self.assertEqual(q['proposed_relationship']['legal_adoption_status'],'not_stated');self.assertFalse(q['proposed_relationship']['biological_parentage_inferred'])
 def test_aunt_is_liu_sister_of_liu(self):
  u=pid(1,'劉');l=pid(1,'柳');a=next(a for a in A if a['predicate']=='sister');self.assertEqual((a['subject_person_id'],a['object_person_id']),(u,l));self.assertEqual(a['qualifiers']['relative_birth_order']['older_person_id'],u);self.assertEqual(pid(1,'姊'),u);self.assertNotEqual(l,'7r6_k52_qji_ABAAAAC')
 def test_huan_bridge_keeps_exact_glyphs_and_layers(self):
  self.assertEqual(pid(2,'奐'),'aa6_83c_juy_CDA');self.assertEqual(B['local_surface'],'奐');self.assertEqual(B['person_id'],'aa6_83c_juy_CDA');self.assertEqual(len(B['evidence']),3);self.assertTrue(any('父瑍' in e['quote']for e in B['evidence']));self.assertTrue(any('父奐' in e['quote']for e in B['evidence']));self.assertEqual(B['reported_variant']['layer'],'qing_collation');self.assertFalse(B['human_reviewed'])
 def test_secretary_refers_deceased_father(self):
  m=next(m for m in ms(2)if m['surface']=='祕書');p=C['paragraphs'][1];self.assertEqual(m['person_id'],'aa6_83c_juy_CDA');self.assertTrue(p['text'][m['start']:].startswith('祕書早亡'));self.assertEqual(sum(m['surface']=='祕書'for m in ms(2)),1)
 def test_guo_is_only_jue_birthmother(self):
  jue=pid(3,'㬭');guo=pid(3,'郭氏');mothers=[a for a in A if a['predicate']=='mother'];self.assertEqual(len(mothers),1);self.assertEqual((mothers[0]['subject_person_id'],mothers[0]['object_person_id']),(jue,guo));self.assertEqual(mothers[0]['qualifiers']['source_term'],'所生母郭氏')
 def test_jue_younger_brother_continuation_is_not_son(self):
  jue=pid(3,'㬭');a=next(a for a in A if a['subject_person_id']==jue and a['predicate']=='brother');self.assertEqual(a['object_person_id'],'aa6_83c_juy_AAAD');self.assertEqual(a['context']['kind'],'adjacent_paragraphs');self.assertEqual(a['context']['paragraph_ids'],[C['paragraphs'][1]['id'],C['paragraphs'][2]['id']]);self.assertFalse(any(a['subject_person_id']==jue and a['predicate']=='father'for a in A))
 def test_shiping_father_is_jue_not_xu(self):
  sp=pid(3,'世平');a=next(a for a in A if a['subject_person_id']==sp and a['predicate']=='father');self.assertEqual(a['object_person_id'],pid(3,'㬭'));self.assertNotEqual(a['object_person_id'],'4y6_myv_ojh');self.assertEqual(pid(3,'其'),pid(3,'㬭'))
 def test_princess_explicit_spouse_no_emperor_father(self):
  p=pid(1,'晉南郡公主');y=pid(1,'羊賁');a=next(a for a in A if a['predicate']=='spouse');self.assertEqual((a['subject_person_id'],a['object_person_id']),(y,p));self.assertEqual(a['qualifiers']['source_term'],'晉南郡公主婚羊賁');self.assertFalse(any(a['subject_person_id']==p and a['predicate']=='father'for a in A))
 def test_langye_title_resolved_by_fixed_chronology(self):
  m=next(m for m in ms(1)if m['surface']=='琅邪王');self.assertEqual(m['person_id'],'ije_ngm_cmj');b=J(ROOT/'source-evidence/song056-langye-dewen-identity.json');self.assertEqual(b['person_id'],m['person_id']);self.assertEqual(b['fixed_witness']['commit'],'82291520954e5af1fdade894971a2f5810fd4e31');self.assertEqual(len(b['complete_contexts']),5);raw=(ROOT/b['fixed_witness']['raw_path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),b['fixed_witness']['raw_sha256']);self.assertTrue(any('道子為桓玄所害'in e['projected_quote']for e in b['complete_contexts']));self.assertTrue(any('以琅邪王徳文為大司馬'in e['projected_quote']for e in b['complete_contexts']));self.assertTrue(any('恭帝諱徳文' in e['projected_quote']for e in b['complete_contexts']));self.assertTrue(any(x['person_id']=='dkn_ge4_286_AAAAAAAFA'for x in b['rejected_candidates']))
 def test_langye_not_liuyu_or_dead_daozi(self):
  self.assertNotIn(pid(1,'琅邪王'),['3dv_ken_w58','dkn_ge4_286_AAAAAAAFA']);b=J(ROOT/'source-evidence/song056-langye-dewen-identity.json');self.assertEqual(b['local_evidence']['sequence'],['楚臺祕書郎','髙祖鎮軍','琅邪王大司馬參軍'])
 def test_langye_exact_context_anchors(self):
  b=J(ROOT/'source-evidence/song056-langye-dewen-identity.json')
  for e in b['complete_contexts']:
   a=e['anchor'];self.assertEqual(e['projected_quote'][a['start']:a['end']],a['surface']);self.assertEqual(hashlib.sha256(e['projected_quote'].encode()).hexdigest(),e['quote_sha256'])
 def test_minister_dachen_is_hui_not_first_person(self):
  self.assertEqual(pid(1,'大臣'),'aa6_83c_juy_AAAA');self.assertEqual(pid(1,'臣'),'aa6_83c_juy_AAAD');self.assertEqual(sum(m['surface']=='臣'for m in ms(1)),1)
 def test_you_and_wo_speech_endpoints(self):
  self.assertTrue(all(m['person_id']=='aa6_83c_juy_AAAA'for m in ms(1)if m['surface']=='汝'));self.assertTrue(all(m['person_id']=='aa6_83c_juy_AAAD'for m in ms(1)if m['surface']=='吾'));self.assertEqual(pid(2,'汝'),'aa6_83c_juy_AAAD')
 def test_no_agnatic_cousin_made_sibling(self):
  self.assertFalse(any({a['subject_person_id'],a['object_person_id']}=={'aa6_83c_juy_AAAD','aa6_83c_juy_CDAA'}and a['predicate']=='brother'for a in A));self.assertTrue(any(q['kind']=='agnatic_uncle_and_cousin_source_terms'for q in Q))
 def test_inherited_067_and_053_identities_preserved(self):
  ps={p['id']:p for p in J(ROOT/'registry/persons.json')['persons']};self.assertIn('apr_7dg_tdd_A',ps);self.assertIn('262_d54_a5e',ps);self.assertEqual(ps['aa6_83c_juy_AAAD']['label'],'謝瞻');self.assertTrue((ROOT/'corpus/songshu/053-xiefangming.json').exists());self.assertTrue((ROOT/'corpus/songshu/053-yu-dengzhi.json').exists())
 def test_source_only_no_office_age_records(self):
  f=ROOT/'source-evidence/song056-f20-consumption-review.json';baseline=J(f)['source_only_annotation']if f.exists()else C['annotation']
  self.assertNotIn('title_proposals',baseline);self.assertNotIn('age_assertions',baseline);self.assertFalse(C['source']['image_verified']);self.assertTrue(all(a['human_reviewed']is False for a in A))
 def test_age_thirty_is_hui_not_zhan(self):
  q=next(q for q in Q if q['kind']=='reported_age'and q['value']==30);self.assertEqual(q['person_ids'],['aa6_83c_juy_AAAA']);self.assertTrue(all(q.get('birth_year')is None for q in Q if q['kind'].startswith('reported_')))
 def test_unassumed_secretary_not_automatically_refused_later_offices(self):
  q=next(q for q in Q if q['evidence']['anchor']['surface']=='固辭不就');self.assertEqual(q['proposed_mode'],'unassumed');self.assertFalse(any(q.get('proposed_mode')=='unassumed'and q['evidence']['anchor']['surface']in ['司空長史','黄門郎']for q in Q))
 def test_raw_selected_runs_unique_and_complete(self):
  pairs=[(r['raw_line'],i)for p in EV['paragraphs']for r in p['runs']for i in range(r['raw_start'],r['raw_end'])];self.assertEqual(len(pairs),len(set(pairs)));expected=[(ln,i)for ln in range(13,54)if not LINES[ln-1].startswith('<pb:')for i,c in enumerate(LINES[ln-1])if c!='¶'];self.assertEqual(pairs,expected)
 def test_typed_proposal_anchors(self):
  ps={p['id']:p for p in C['paragraphs']}
  for q in Q:
   e=q['evidence'];a=e['anchor'];self.assertEqual(ps[e['paragraph_id']]['text'][a['start']:a['end']],a['surface']);self.assertEqual(e['quote'],ps[e['paragraph_id']]['text']);self.assertEqual(q['status'],'not_imported')
 def test_xml_and_person_spans(self):
  for p in C['paragraphs']:
   last=0
   for m in p['mentions']:self.assertGreaterEqual(m['start'],last);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);last=m['end']
  x=ET.parse(ROOT/'corpus/songshu/056-xiezhan.xml').getroot();self.assertEqual([''.join(p.itertext())for p in x.findall('p')],[p['text']for p in C['paragraphs']])
if __name__=='__main__':unittest.main()
