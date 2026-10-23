"""008全年／077完整本傳來源界線；不依賴私有暫存包。"""
import json,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
class CompleteSources(unittest.TestCase):
 def setUp(self):
  self.a=read('corpus/jinshu/008-yonghe5.json');self.b=read('corpus/jinshu/077-yinhao.json');self.e=ROOT/'source-evidence/jin008077'
 def test_complete_extents_and_original_words(self):
  self.assertEqual(len(self.a['paragraphs']),1);self.assertEqual(len(self.b['paragraphs']),15)
  self.assertTrue(self.a['paragraphs'][0]['text'].startswith('五年春正月'));self.assertFalse(self.a['paragraphs'][0]['text'].startswith('永和'))
  self.assertIn('朝過欲遂',self.b['paragraphs'][5]['text']);self.assertIn('開江西田',self.b['paragraphs'][5]['text']);self.assertIn('末忍誅殛',self.b['paragraphs'][7]['text'])
 def test_all_anchors_exact_and_source_qualification(self):
  for c in [self.a,self.b]:
   self.assertFalse(c['source']['image_verified']);self.assertFalse(c['annotation']['human_reviewed'])
   for p in c['paragraphs']:
    for m in p['mentions']:self.assertEqual(p['text'][m['start']:m['end']],m['surface'])
 def test_full_raw_projection(self):
  for number,key,c in [(8,'jin008-yonghe5',self.a),(77,'jin077-yinhao',self.b)]:
   raw=(self.e/f'primary{number:03}.txt').read_bytes();pr=json.loads((self.e/(key+'-projection.json')).read_text());self.assertEqual(hashlib.sha256(raw).hexdigest(),pr['source_sha256']);lines=raw.decode().splitlines();ts=[]
   for u in pr['units']:
    t=lines[u['raw_line']-1][u['raw_start']:u['raw_end']];self.assertEqual(t,u['text']);ts.append(t[4:]if t.startswith('::　　')else t)
   self.assertEqual([p['text']for p in c['paragraphs']],[''.join(ts)]if number==8 else ts)
 def test_debate_speakers_and_cai_mo(self):
  p=self.b['paragraphs'][7];a=p['text'].index('前司徒臣謨')+3;m=next(m for m in p['mentions']if m['start']==a);self.assertEqual(m['person_id'],'b98_957_r7h')
  p=self.b['paragraphs'][9];a=p['text'].index('君何如我');self.assertEqual(next(m for m in p['mentions']if m['start']==a)['person_id'],'djo_u3b_i9w_A')
 def test_wangkan_scoped_identity_not_earlier_xukan(self):
  d=read('corpus/jinshu/008077-parallel-identities.json');x=next(x for x in d['decisions']if x['person_id']=='bqs_gsj_v46');self.assertIn('王龕',x['surfaces']);self.assertIn('徐龕',x['surfaces']);self.assertIn('不是早先',x['rationale']);self.assertNotEqual(x['person_id'],'acd_5d4_b62')
  p=self.a['paragraphs'][0];m=next(m for m in p['mentions']if m['surface']=='李農');self.assertNotEqual(m['person_id'],'s97_5zh_wpe')
 def test_direct_family_terms_not_extended(self):
  a=read('corpus/jinshu/077-yinhao-assertions.json')['assertions'];father=next(x for x in a if x['subject_person_id']=='djo_u3b_i9w_A'and x['predicate']=='father');self.assertEqual(father['object_person_id'],'djo_u3b_i9w');uncle=next(x for x in a if x['predicate']=='paternal_uncle');self.assertEqual(uncle['object_person_id'],'ali_hbb_4bn')
  self.assertFalse(any(x['predicate']=='maternal_uncle'for x in a));self.assertFalse(any(x['predicate']=='brother'and set([x['subject_person_id'],x['object_person_id']])=={'djo_u3b_i9w','ali_hbb_4bn'}for x in a))
 def test_continuous_son_evidence_not_fake_father_anchor(self):
  a=next(x for x in read('corpus/jinshu/077-yinhao-assertions.json')['assertions']if x['subject_person_id']=='djo_u3b_i9w_AA');self.assertEqual(a['object_person_id'],'djo_u3b_i9w_A');self.assertEqual(a['context']['kind'],'biographical_child_continuation');self.assertEqual(len(a['evidence']),2);self.assertTrue(a['evidence'][1]['quote'].startswith('子涓'))
 def test_uncertainties_preserved_as_typed(self):
  p=read('source-evidence/jin008077/retained-proposals.json');types={x['kind']for x in p['proposals']};self.assertTrue({'mistaken_belief','conditional_offer','unrealized_appointment','kinship_unspecified','chronology_source_doubt'}<=types)
 def test_caoyanyuan_complete_fixed_primary_bridge(self):
  p=read('source-evidence/jin008077/caoyanyuan-name-bridge.json');raw=(self.e/'jin090-fixed.txt').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),p['primary_context']['raw_sha256']);self.assertIn('曹攄，字顏遠',p['primary_context']['complete_unit']);self.assertFalse(p['image_verified']);self.assertEqual(p['person_id'],'h7n_w5t_i1c_AAA*A')

 def test_wangxizhi_is_not_wuling_xi(self):
  p=self.b['paragraphs'][4];m=next(m for m in p['mentions']if m['surface']=='王羲之');self.assertEqual(m['person_id'],'7r6_k52_qji_ABDCB');self.assertNotEqual(m['person_id'],'dkn_ge4_286_AAAAAAAD')
  p=self.b['paragraphs'][11];m=next(m for m in p['mentions']if m['surface']=='武陵王晞');self.assertEqual(m['person_id'],'dkn_ge4_286_AAAAAAAD');self.assertNotEqual(m['person_id'],'7r6_k52_qji_ABDCB')

 def test_prior_emperor_has_complete_caimo_context(self):
  p=self.b['paragraphs'][7];m=next(m for m in p['mentions']if m['surface']=='先帝');self.assertEqual(m['person_id'],'qpk_4pt_y6r');context=read('source-evidence/jin008077/caimo-kangdi-context.json');self.assertEqual([p['raw_line']for p in context['paragraphs']],[93,95,97]);self.assertIn('康帝即位',context['paragraphs'][0]['quote']);self.assertIn('謨先帝師傅',context['paragraphs'][2]['quote'])
 def test_murong_glyph_bridge_is_local_not_global(self):
  context=read('source-evidence/jin008077/murong-source-context.json');self.assertEqual(context['conclusion']['person_id'],'yvd_fyi_r56');self.assertIn('慕容儁，字宣英',context['paragraphs'][0]['quote']);self.assertIn('拜俊',context['paragraphs'][0]['quote']);self.assertIn('段蘭之子龕',context['paragraphs'][1]['quote']);self.assertFalse(context['image_verified'])
