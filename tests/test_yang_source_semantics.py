# coding: utf-8
import unittest,json,copy,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));P=ROOT/'tests/fixtures/yang-source';R=ROOT
from scripts.person_bundle import bundle,load_catalog
from scripts.family_assemblies import load_assemblies
from scripts.render_corpus import render
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();D=J(ROOT/'corpus/sanguozhi/019-yangxiu.json');PAR=D['paragraphs'];IDS=J(P/'ids.json');ID={**IDS['existing'],**IDS['new']};CAT=load_catalog(ROOT)
class YangSourceSemantics(unittest.TestCase):
 def test_complete_unit_exact_source_fragments(self):
  units=J(P/'units.json');self.assertEqual(len(units),7);self.assertEqual(sum(len(x['text'])for x in units),1971)
  for u,p in zip(units,PAR):self.assertEqual(u['text'],p['text']);self.assertEqual(''.join(x['selected_text']for x in u['source_fragments']),p['text'])
  self.assertTrue(PAR[0]['text'].startswith('太祖既慮'));self.assertTrue(PAR[-1]['text'].endswith('俊太傅椽'))

 def test_layers_and_original_glyphs(self):
  self.assertEqual(PAR[0]['text_layer'],'received_chapter');self.assertTrue(all(p['text_layer']=='witness_appended_pei_songzhi_note'for p in PAR[1:]));self.assertIn('脩',PAR[1]['text']);self.assertIn('修',PAR[1]['text']);self.assertIn('裘頠',PAR[5]['text']);self.assertIn('俊宇惠彦',PAR[6]['text']);self.assertIn('翼州記',PAR[5]['text']);self.assertEqual((R/'corpus/sanguozhi/019-yangxiu.xml').read_text(),render(D))

 def test_fixed_source_no_image_claim(self):
  self.assertEqual(D['source']['source_commit'],'214fcafa79894355909c9d8c2c1533089e7791c6');self.assertFalse(D['source']['image_verified']);self.assertEqual(D['source']['response_sha256'],H(P/'KR2a0012_019.txt'));self.assertEqual(J(P/'retrieval-limitations.json')['no_wikisource_collation_claim'],True)

 def test_exact_nonoverlap_mentions(self):
  # 原人物辨識批217錨含兩個後經古注辨為書名的未決錨；另增10個書名，不算新增人物。
  ms=[m for p in PAR for m in p['mentions']];works=[m for m in ms if m['kind']=='work']
  self.assertEqual(len(works),12);self.assertEqual(sum(m['kind']!='work' for m in ms)+2,217)
  for mid,surface,wid in [('m1033','吕氏','w-lushichunqiu-sgz019-reference'),('m1035','淮南','w-huainan-sgz019-reference')]:
   m=next(m for m in ms if m['id']=='c-sanguozhi-019-yangxiu:p002:'+mid);self.assertEqual((m['surface'],m['kind'],m['work_id']),(surface,'work',wid));self.assertIsNone(m['person_id'])
  for p in PAR:
   end=0
   for m in p['mentions']:self.assertGreaterEqual(m['start'],end);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']

 def hit(self,p,text,offset=0):
  at=p['text'].index(text)+offset;return next(m for m in p['mentions']if m['start']==at)

 def test_nested_letter_speakers(self):
  p=PAR[1];self.assertEqual(self.hit(p,'吾自得之')['person_id'],ID['丁敬禮']);self.assertEqual(self.hit(p,'吾常歎此')['person_id'],ID['曹植']);self.assertEqual(self.hit(p,'我固自以死')['person_id'],ID['楊脩']);self.assertEqual(self.hit(p,'吾王')['person_id'],ID['曹魏太祖'])

 def test_xiu_variant_and_liu_xiu_distinct(self):
  self.assertEqual(self.hit(PAR[1],'投修',1)['person_id'],ID['楊脩']);self.assertEqual(self.hit(PAR[2],'名脩',1)['person_id'],ID['劉脩']);self.assertNotEqual(ID['劉脩'],ID['楊脩'])

 def test_mao_names_distinct(self):
  self.assertEqual(self.hit(PAR[1],'王髦')['person_id'],ID['王髦']);self.assertEqual(self.hit(PAR[5],'髦字士彦')['person_id'],ID['楊髦']);self.assertNotEqual(ID['王髦'],ID['楊髦'])

 def test_exact_direct_kinship_only(self):
  a=J(P/'assertion-delta.json');self.assertEqual(len(a),7);self.assertEqual(sum(x['predicate']=='father'for x in a),6);b=next(x for x in a if x['predicate']=='brother');self.assertEqual((b['subject_person_id'],b['object_person_id']),(ID['楊嶠'],ID['楊俊']));self.assertIsNone(b['qualifiers']['relative_birth_order']['older_ordinal']);self.assertFalse(any(x['subject_person_id']==ID['楊俊']and x['predicate']=='father'for x in a));self.assertFalse(any(x['predicate']in ['mother','spouse','ancestor','birth']for x in a))

 def test_family_assembly_and_reviewed_jun(self):
  sm,assemblies=load_assemblies(R,CAT);self.assertEqual(sm[ID['楊俊']]['parent_person_id'],ID['楊準']);self.assertIsNone(sm[ID['楊俊']]['source_assertion_id']);self.assertEqual(sm[ID['楊俊']]['parent_connection']['type'],'shared_father_through_sibling');self.assertEqual(sm[ID['楊髦']]['parent_person_id'],ID['楊準']);self.assertEqual(sm[ID['劉脩']]['parent_person_id'],ID['劉表'])

 def test_unknowns_and_variant_not_forced(self):
  ms=[m for p in PAR for m in p['mentions']];self.assertEqual(sum(m['kind']=='unresolved'for m in ms),29);self.assertFalse(any(m['kind']=='unresolved' and m['surface'] in ['吕氏','淮南'] for m in ms))
  for s in ['袁氏','墨瞿','孔公','惠子','仲山','惠彦']:self.assertTrue(all(m['person_id']is None for m in ms if m['surface']==s))
  self.assertNotEqual(ID['楊俊'],'05q_rr2_8ki');self.assertNotEqual(ID['楊準'],'3ea_uzt_2n2')

 def test_memory_bundles_and_connected_ids(self):
  for p in J(P/'registry-delta.json')['add_persons']:
   # Frozen import IDs are historical; resolve each exact source occurrence in current markup.
   anchors={e['mention_id']:e['quote'] for e in p['evidence']}
   marks=[m for para in PAR for m in para['mentions'] if m['id'] in anchors]
   self.assertEqual({m['id'] for m in marks},set(anchors))
   self.assertTrue(all(m['surface']==anchors[m['id']] for m in marks))
   current_ids={m['person_id'] for m in marks};self.assertEqual(len(current_ids),1)
   current_id=next(iter(current_ids))
   d=bundle(current_id,root=ROOT,catalog=CAT,include_provisional=True);self.assertEqual(d['canonical_person_id'],current_id);self.assertTrue(d['mentions'])
  d=bundle(ID['楊髦'],root=ROOT,catalog=CAT,include_provisional=True)
  sm,rows=load_assemblies(ROOT,CAT);pid=ID['楊髦'];chain=[]
  while pid:
   chain.append(pid);pid=rows.get(pid,{}).get('parent_person_id')
  self.assertEqual(chain,[ID[k] for k in ['楊髦','楊準','楊囂','楊脩','楊彪']])
 def test_reviewed_ids_and_song_taizu_remain_distinct(self):
  sm,_=load_assemblies(ROOT,CAT);self.assertIn(ID['楊俊'],sm);self.assertNotIn('4cf_598_af9',CAT[0]);self.assertNotIn('c43_8dc_649',CAT[0]);self.assertIn('dad_b77_b38',CAT[0]);ch=J(ROOT/'corpus/songshu/053-yu-dengzhi.json');p=next(p for p in ch['paragraphs'] if p['id'].endswith('line062'));taizu=next(m for m in p['mentions'] if m['surface']=='太祖');caogong=next(m for m in p['mentions'] if m['surface']=='曹公');self.assertNotEqual(taizu['person_id'],caogong['person_id']);self.assertEqual(caogong['person_id'],'dad_b77_b38')
