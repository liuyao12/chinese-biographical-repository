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
  self.assertTrue(all(p in C['paragraphs']for p in P['old_paragraphs_preserved']));old_ids={p['id'] for p in P['old_paragraphs_preserved']};self.assertEqual([p for p in C['paragraphs'] if p['id'] in old_ids],P['old_paragraphs_preserved']);self.assertEqual(PS[P['old_paragraphs_preserved'][8]['id']],P['old_paragraphs_preserved'][8]);self.assertEqual(len(PS[P['old_paragraphs_preserved'][8]['id']]['text']),35);self.assertEqual(len(P['old_paragraphs_preserved'][9]['text']),14)
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
  people=J(R/'registry/persons.json')['persons'];aa=J(R/'corpus/jinshu/039-assertions.json')['assertions'];shi=next(p for p in people if p['label']=='識（畯弟之子、畯嗣）');self.assertNotIn('family_path',shi);self.assertFalse(any(a['subject_person_id']==shi['id']and a['predicate']=='father'for a in aa));self.assertFalse(any(a['subject_person_id']=='537_48d_739'and a['predicate']=='father'and a['object_person_id']=='yoo_ox0_545_FAAAB'for a in aa));wang=next(p for p in people if p['label']=='汪（荀邃子）');self.assertNotEqual(wang['id'],'yoo_ox0_545_E')
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
  self.assertEqual(len(mids),len(set(mids)));ms=[m for p in C['paragraphs']if':xu-full:'in p['id']for m in p['mentions']if m['surface']=='綽'];self.assertTrue(ms);self.assertTrue(all(m['person_id']is None and m['candidate_person_ids']==['537_48d_739']for m in ms))

 def test_book_classification_not_office_or_document_verb(self):
  rows=J(R/'source-evidence/jin039-xunxu-nonperson-proposals.json')['records']
  for row in rows:
   if row['surface']=='書':
    t=PS[row['paragraph_id']]['text'];self.assertEqual(t[row['start']-1:row['end']+1],'《書》')
  p=next(p for p in C['paragraphs']if':xu-full:l098'in p['id']);self.assertFalse(any(m.get('person_id')=='yoo_ox0_545_FAAA' and m['surface']=='君'and p['text'][max(0,m['start']-1):m['end']]=='諸君'for m in p['mentions']))
