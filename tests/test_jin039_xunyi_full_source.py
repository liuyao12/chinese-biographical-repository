import unittest,json,hashlib,copy,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];J=lambda p:json.loads(p.read_text());C=J(R/'corpus/jinshu/039.json');P=J(R/'source-evidence/jin039-xunyi-full-projection.json');RAW=(R/'sources/jinshu/039-ws2108782.wikitext').read_bytes();LINES=RAW.decode().splitlines()
def projection_valid(c):
 try:
  ps={p['id']:p for p in c['paragraphs']}
  if hashlib.sha256(RAW).hexdigest()!=P['raw_sha256']or c['source']['revision_id']!=2108782:return False
  for u in P['units']:
   line=LINES[u['source_line']-1]
   if line!=u['raw_line']or hashlib.sha256(line.encode()).hexdigest()!=u['raw_line_sha256']:return False
   if u['display_text']!=''.join(line[i]for i in u['display_to_raw_columns']):return False
   if ''.join(ps[x['paragraph_id']]['text']for x in u['parts'])!=u['display_text']:return False
  return True
 except(KeyError,IndexError,TypeError):return False

def ys(chapter):
 return [p for p in chapter['paragraphs'] if ':yi-intro:' in p['id'] or ':yi-full:' in p['id']]
class XunYiFull(unittest.TestCase):
 def test_same_fixed_revision_body_and_boundaries(self):
  self.assertTrue(projection_valid(C));self.assertEqual(LINES[49],'==荀顗==');self.assertEqual(LINES[64],'==荀勖==');self.assertTrue(ys(C)[7]['text'].endswith('宋受禪，國除。'))
 def test_old_three_paragraphs_and_all_anchors_unchanged(self):
  self.assertTrue(all(p in C['paragraphs'] for p in P['old_paragraphs_preserved']));self.assertGreaterEqual(len(C['paragraphs']),10);self.assertIn(':yi-full:tail001',ys(C)[1]['id'])
 def test_reading_order_complete_original_units(self):
  self.assertEqual([ys(C)[i]['source_position']['first_line']for i in range(8)],[51,51,53,55,57,59,61,63]);self.assertEqual(next(p for p in C['paragraphs']if ':xu-intro:'in p['id'])['source_position']['first_line'],66)
 def test_no_duplicate_intro(self):
  self.assertFalse(ys(C)[1]['text'].startswith('荀顗'));self.assertEqual(sum('荀顗，字景倩' in p['text']for p in C['paragraphs']),1)
 def test_all_unicode_nonoverlapping_exact(self):
  seen=set()
  for p in C['paragraphs']:
   end=0
   for m in p['mentions']:
    self.assertNotIn(m['id'],seen);seen.add(m['id']);self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
 def test_digital_wiki_and_year_template_layers(self):
  mark=[m for u in P['units']for m in u['digital_markup']];self.assertEqual({m['kind']for m in mark},{'wikilink','digital_year_link_template'});self.assertTrue(any(m['raw']=='{{YL|泰始十年}}'for m in mark));self.assertIn('泰始十年',ys(C)[5]['text']);self.assertNotIn('{{',ys(C)[5]['text'])
 def test_reject_missing_tail_and_country_succession(self):
  bad=copy.deepcopy(C);bad['paragraphs'].remove(next(p for p in bad['paragraphs'] if p['id']==ys(C)[1]['id']));self.assertFalse(projection_valid(bad));bad=copy.deepcopy(C);next(p for p in bad['paragraphs'] if p['id']==ys(C)[7]['id'])['text']=next(p for p in bad['paragraphs'] if p['id']==ys(C)[7]['id'])['text'][:-2];self.assertFalse(projection_valid(bad))
 def test_reject_silent_glyph_and_missing_year_payload(self):
  bad=copy.deepcopy(C);next(p for p in bad['paragraphs'] if p['id']==ys(C)[7]['id'])['text']=next(p for p in bad['paragraphs'] if p['id']==ys(C)[7]['id'])['text'].replace('恆','恒');self.assertFalse(projection_valid(bad));bad=copy.deepcopy(C);next(p for p in bad['paragraphs'] if p['id']==ys(C)[5]['id'])['text']=next(p for p in bad['paragraphs'] if p['id']==ys(C)[5]['id'])['text'].replace('泰始十年','');self.assertFalse(projection_valid(bad))
 def test_books_are_non_person_and_mothers_are_distinct(self):
  ms=[m for p in ys(C)[1:-2]for m in p['mentions']];rows=J(R/'source-evidence/jin039-xunyi-nonperson-proposals.json')['records'];self.assertEqual({r['surface']for r in rows},{'易','三禮','正德','大豫','晉禮','子'});self.assertTrue(all(r['person_id']is None for r in rows));moms=[m for m in ys(C)[3]['mentions']if m['surface']=='母'];self.assertEqual(len(moms),2);self.assertNotEqual(moms[0]['interpretation_note'],moms[1]['interpretation_note']);self.assertTrue(all(m['person_id']is None for m in moms))
 def test_no_named_brother_xuan_or_fictional_son(self):
  self.assertFalse(any(m['surface']=='玄'for m in ys(C)[7]['mentions']));self.assertTrue(all(m['person_id']is None for m in ys(C)[7]['mentions']if m['surface']=='子'))
 def test_source_birth_order_preserved_not_inferred(self):
  aa=J(R/'corpus/jinshu/039-assertions.json')['assertions'];old=next(a for a in aa if a['id']=='a-jinshu039-xun-001');self.assertEqual(old['qualifiers']['birth_order']['ordinal'],6);self.assertEqual(old['qualifiers']['source_term'],'魏太尉彧之第六子也。')
 def test_new_father_facts_not_adoptive_or_ritual(self):
  aa=[a for a in J(R/'corpus/jinshu/039-assertions.json')['assertions']if'-yi-full-'in a['id']];self.assertEqual(len(aa),5);self.assertEqual(sum(a['predicate']=='father'for a in aa),3);self.assertFalse(any(a['predicate']in['adoptive_father','ritual_successor_of']for a in aa))

 def test_fufeng_jun_reuses_existing_identity_by_full_title_bridge(self):
  bridge=J(R/'source-evidence/jin039-fufeng-jun-existing-bridge.json');self.assertIn('扶風武王駿',bridge['existing_native_paragraph']['text']);m=next(m for m in ys(C)[1]['mentions']if m['surface']=='扶風王駿');self.assertEqual(m['person_id'],bridge['person_id']);self.assertTrue(any(m.get('person_id')==bridge['person_id']and m['surface']=='駿'for m in bridge['existing_native_paragraph']['mentions']))
