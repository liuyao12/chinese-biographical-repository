# coding: utf-8
import unittest,json,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());C=J(R/'corpus/jinshu/039.json');P=J(R/'source-evidence/jin039-xunxu-full-projection.json');RAW=(R/'sources/jinshu/039-ws2108782.wikitext').read_bytes();LINES=RAW.decode().splitlines();PS={p['id']:p for p in C['paragraphs']}
def valid(c,proof=None):
 proof=proof or P
 try:
  ps={p['id']:p for p in c['paragraphs']}
  if hashlib.sha256(RAW).hexdigest()!=proof['raw_sha256']or c['source']['revision_id']!=2108782:return False
  for u in proof['units']:
   line=LINES[u['source_line']-1]
   if line!=u['raw_line']or hashlib.sha256(line.encode()).hexdigest()!=u['raw_line_sha256']:return False
   if u['display_text']!=''.join(line[i]for i in u['display_to_raw_columns']):return False
   if ''.join(ps[x['paragraph_id']]['text']for x in u['parts'])!=u['display_text']:return False
  return True
 except(KeyError,IndexError,TypeError):return False
class XunXuFull(unittest.TestCase):
 def test_full_fixed_body_and_boundary(self):
  self.assertTrue(valid(C));self.assertEqual(LINES[64],'==荀勖==');self.assertEqual(LINES[135],'==馮紞==');self.assertEqual(len(P['units']),34);self.assertEqual(sum(len(u['display_text'])for u in P['units']),4903);self.assertTrue(next(p for p in C['paragraphs'] if p['id']=='c-jinshu-039-wangxun-feng:xu-full:l134')['text'].endswith('諡曰定。'))
 def test_all_old_paragraph_objects_mentions_unchanged(self):
  self.assert_old_paragraphs_preserved(C);self.assertEqual(len(PS[P['old_paragraphs_preserved'][8]['id']]['text']),35);self.assertEqual(len(P['old_paragraphs_preserved'][9]['text']),14)
 def test_order_no_duplicate_old_raw_positions(self):
  for u in P['units']:
   a=0
   for part in u['parts']:self.assertEqual(part['start'],a);a=part['end']
   self.assertEqual(a,len(u['display_text']))
  a=next(i for i,p in enumerate(C['paragraphs'])if ':xu-sons:'in p['id']);self.assertEqual(C['paragraphs'][a-1]['source_position']['first_line'],100);self.assertEqual(C['paragraphs'][a+1]['source_position']['first_line'],102)
 def test_quote_four_paragraphs_and_digital_layers(self):
  units={u['source_line']:u for u in P['units']};self.assertTrue(any(m['kind']=='digital_quote_open'for m in units[83]['digital_markup']));self.assertTrue(any(m['kind']=='digital_quote_close'for m in units[89]['digital_markup']));self.assertIn(85,units);self.assertIn(87,units);self.assertTrue(any(m['kind']=='digital_year_link'for u in P['units']for m in u['digital_markup']))
 def test_negative_missing_tail_end_and_silent_glyph(self):
  for line in [66,100,134]:
   bad=copy.deepcopy(C);p=next(p for p in bad['paragraphs']if':xu-full:'in p['id']and p['source_position']['first_line']==line);p['text']=p['text'][:-1];self.assertFalse(valid(bad))
  bad=copy.deepcopy(P);bad['units'][0]['display_to_raw_columns'][0]+=1;self.assertFalse(valid(C,bad))
 def test_negative_duplicate_old_excerpt_or_wrong_revision(self):
  bad=copy.deepcopy(C);p=next(p for p in bad['paragraphs']if':xu-full:l100'in p['id']);p['text']+=P['old_paragraphs_preserved'][9]['text'];self.assertFalse(valid(bad));bad=copy.deepcopy(C);bad['source']['revision_id']=2108783;self.assertFalse(valid(bad))
 def test_no_fictional_father_or_same_label_merge(self):
  people=J(R/'registry/persons.json')['persons'];aa=J(R/'corpus/jinshu/039-assertions.json')['assertions'];shi=next(p for p in people if p['label']=='識（畯弟之子、畯嗣）');self.assertNotIn('family_path',shi);self.assertFalse(any(a['subject_person_id']==shi['id']and a['predicate']=='father'for a in aa));wang=next(p for p in people if p['label']=='汪（荀邃子）');self.assertNotEqual(wang['id'],'yoo_ox0_545_E')
 def test_wei_labels_same_issued_ids_and_bridge(self):
  people={p['id']:p for p in J(R/'registry/persons.json')['persons']};self.assertEqual(people['1b6_503_da8']['label'],'曹芳');self.assertEqual(people['d6b_ea7_928']['label'],'曹髦');bridge=J(R/'source-evidence/jin039-wei-monarch-fixed-identity-bridge.json');self.assertEqual(bridge['bridge']['commit'],'214fcafa79894355909c9d8c2c1533089e7791c6');self.assertTrue(bridge['source_quality']['body_duplicate_blocks']['body_text_exact_equal'])
 def test_wangjun_two_contexts_and_wangshen_counterevidence(self):
  body=lambda line:next(p for p in C['paragraphs']if':xu-full:'in p['id']and p['source_position']['first_line']==line)
  one=next(m for m in body(76)['mentions']if m['surface']=='王浚');two=next(m for m in body(107)['mentions']if m['surface']=='王浚');self.assertEqual(one['person_id'],'36c_6b6_4b3');self.assertNotEqual(one['person_id'],two['person_id']);shen=next(m for m in body(70)['mentions']if m['surface']=='王深');self.assertNotEqual(shen['person_id'],'7r6_k52_qji_ABAAAABA')
 def test_marriage_completed_not_all_intentions(self):
  aa=[a for a in J(R/'corpus/jinshu/039-assertions.json')['assertions']if'-xu-full-'in a['id']];self.assertEqual(sum(a['predicate']=='spouse'for a in aa),1);self.assertEqual(next(a for a in aa if a['predicate']=='spouse')['qualifiers']['source_term'],'遂成婚');self.assertFalse(any('欲納' in a.get('qualifiers',{}).get('source_term','')for a in aa))
 def test_all_mentions_exact_unique_and_candidates_not_active(self):
  mids=[]
  for p in C['paragraphs']:
   end=0
   for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end'];mids.append(m['id'])
  self.assertEqual(len(mids),len(set(mids)));ms=[m for p in C['paragraphs']if':xu-full:'in p['id']for m in p['mentions']if m['surface']=='綽'];self.assertTrue(ms);decision=J(R/'corpus/jinshu/039-xunchuo-identities.json')['decisions'][0];self.assertTrue(all(m['kind']=='person'and m['person_id']==decision['person_id']and not m.get('candidate_person_ids')for m in ms))

 def test_book_classification_not_office_or_document_verb(self):
  rows=J(R/'source-evidence/jin039-xunxu-nonperson-proposals.json')['records']
  for row in rows:
   if row['surface']=='書':
    t=PS[row['paragraph_id']]['text'];self.assertEqual(t[row['start']-1:row['end']+1],'《書》')
  p=next(p for p in C['paragraphs']if':xu-full:l098'in p['id']);self.assertFalse(any(m.get('person_id')=='yoo_ox0_545_FAAA' and m['surface']=='君'and p['text'][max(0,m['start']-1):m['end']]=='諸君'for m in p['mentions']))

 def test_xunchuo_reviewed_bridge_and_father_not_inferred_from_capture(self):
  decision=J(R/'corpus/jinshu/039-xunchuo-identities.json')['decisions'][0];pid=decision['person_id'];p102=PS['c-jinshu-039-wangxun-feng:xu-full:l102'];p104=PS['c-jinshu-039-wangxun-feng:xu-full:l104'];other=J(R/'corpus/jinshu/035-pei-family.json');p13=next(p for p in other['paragraphs']if p['id'].endswith(':p013'))
  def bridge(cross,local,d):
   corpus={p['id']:p for p in [p102,local,cross]}
   if d.get('status')!='contextual_provisional'or d.get('human_reviewed')is not False:return False
   if not all(e['paragraph_id']in corpus and e['quote']==corpus[e['paragraph_id']]['text']for e in d['evidence']):return False
   marks=[m for p in [p102,local]for m in p['mentions']if m['surface']in ['綽','彥舒']]
   if len(marks)!=3 or any(m.get('kind')!='person'or m.get('person_id')!=d['person_id']or m.get('candidate_person_ids')for m in marks):return False
   return ('永嘉末，為司空從事中郎，沒于石勒，為勒參軍' in local['text']and '永嘉末，王浚為石勒所破' in cross['text']and any(m['surface']=='荀綽'and m.get('person_id')==d['person_id']for m in cross['mentions']))
  self.assertTrue(bridge(p13,p104,decision));bad=copy.deepcopy(p104);bad['text']=bad['text'].replace('石勒','石虎');self.assertFalse(bridge(p13,bad,decision));bad=copy.deepcopy(p13)
  for m in bad['mentions']:
   if m['surface']=='荀綽':m['person_id']='yoo_ox0_545_FAAAB'
  self.assertFalse(bridge(bad,p104,decision))
  aa=J(R/'corpus/jinshu/039-assertions.json')['assertions'];fact=next(a for a in aa if a['id']=='a-jin039-xunchuo-father-001');self.assertEqual(fact['subject_person_id'],pid);e=fact['evidence'][0];self.assertEqual(e['quote'],p102['text']);anchor=e['relationship_anchor'];self.assertEqual(p102['text'][anchor['start']:anchor['end']],'輯子綽');mm={m['id']:m for m in p102['mentions']};self.assertEqual(mm[e['subject_person_mention_id']]['person_id'],pid);self.assertEqual(mm[e['object_person_mention_id']]['person_id'],fact['object_person_id']);self.assertEqual(mm[e['object_person_mention_id']]['surface'],'輯');self.assertEqual(fact['predicate'],'father');self.assertEqual(fact['status'],'source_attested')

 def projected_old_paragraphs(self):
  # Keep the historical full-source capture byte-exact; only its reviewed 羊祜 endpoint changes.
  q=J(R/'source-evidence/yang-family-assembly/current-source-projections/jin039-xunxu-full-projection.json');raw=(R/'source-evidence/jin039-xunxu-full-projection.json').read_bytes()
  self.assertEqual(q['historical_file'],'source-evidence/jin039-xunxu-full-projection.json');self.assertEqual(hashlib.sha256(raw).hexdigest(),q['historical_sha256']);self.assertFalse(q['person_aliases_created'])
  receipt=J(R/q['mapping_receipt_ref']);self.assertIn('cys_s5z_uqq',receipt['retired_person_ids']);self.assertFalse(receipt['person_aliases_created'])
  c=J(R/'corpus/jinshu/034-yanghu.json');m=next(m for p in c['paragraphs']for m in p['mentions']if m['id']=='c-jinshu-034-yanghu:p001:m0000');self.assertEqual(m['surface'],'羊祜')
  expected=copy.deepcopy(P['old_paragraphs_preserved']);changed=0
  for p in expected:
   for mention in p['mentions']:
    if mention.get('person_id')=='cys_s5z_uqq':mention['person_id']=m['person_id'];changed+=1
  self.assertEqual(changed,1);self.assertEqual(q['records']['old_paragraphs_preserved'],expected)
  return expected
 def assert_old_paragraphs_preserved(self,c):
  expected=self.projected_old_paragraphs();old_ids={p['id']for p in expected};self.assertEqual([p for p in c['paragraphs']if p['id']in old_ids],expected)
 def test_old_capture_projection_rejects_retired_id_and_source_mutation(self):
  expected=self.projected_old_paragraphs();pid=next(p['id']for p in P['old_paragraphs_preserved']if any(m.get('person_id')=='cys_s5z_uqq'for m in p['mentions']));mid=next(m['id']for p in P['old_paragraphs_preserved']for m in p['mentions']if m.get('person_id')=='cys_s5z_uqq')
  for field in ['person_id','text','start','surface']:
   bad=copy.deepcopy(C);p=next(p for p in bad['paragraphs']if p['id']==pid);m=next(m for m in p['mentions']if m['id']==mid)
   if field=='person_id':m[field]='cys_s5z_uqq'
   elif field=='text':p[field]+='異'
   elif field=='start':m[field]+=1
   else:m[field]='異'
   with self.assertRaises(AssertionError):self.assert_old_paragraphs_preserved(bad)
