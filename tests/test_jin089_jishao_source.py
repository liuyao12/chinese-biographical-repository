"""嵇紹完整本傳來源邊界；不依賴私有封存路徑。"""
import json,unittest,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(p):return json.loads((ROOT/p).read_text())
class JishaoSourceTests(unittest.TestCase):
 def setUp(self):
  self.c=J('corpus/jinshu/089-jishao.json');self.ps=self.c['paragraphs'];self.ids={p['id']:p for p in self.ps}
 def test_complete_eight_paragraphs(self):
  self.assertEqual(len(self.ps),8);self.assertTrue(self.ps[0]['text'].startswith('嵇紹，字延祖'));self.assertTrue(self.ps[-1]['text'].endswith('為弋陽侯。'));self.assertFalse(any(p['text'].startswith('含字君道')for p in self.ps));self.assertFalse(self.c['source']['image_verified']);self.assertFalse(self.c['annotation']['human_reviewed'])
 def test_exact_mention_and_xml(self):
  x=ET.parse(ROOT/'corpus/jinshu/089-jishao.xml').getroot()
  for p,xp in zip(self.ps,x.findall('p')):
   self.assertEqual(''.join(xp.itertext()),p['text']);end=0
   for m in p['mentions']:
    self.assertLessEqual(end,m['start']);self.assertEqual(p['text'][m['start']:m['end']],m['surface']);end=m['end']
 def test_qin_and_chen_are_different(self):
  chen=next(m for m in self.ps[2]['mentions']if m['surface']=='陳准');qin=next(m for m in self.ps[6]['mentions']if m['surface']=='秦准');self.assertEqual(chen['person_id'],'9w8_tqh_ysn_B*AA');self.assertNotEqual(chen['person_id'],qin['person_id'])
 def test_uncertain_pei_not_third_identity(self):
  m=next(m for m in self.ps[1]['mentions']if m['surface']=='裴頠');self.assertEqual(m['kind'],'unresolved');self.assertEqual(m['candidate_person_ids'],['kbq_kjc_n2f_AAB'])
 def test_nonperson_terms_not_named_people(self):
  cases=[(0,'康誥'),(3,'臣之事君'),(4,'萬姓顒'),(4,'公服'),(6,'祠乙太牢'),(7,'曠而有檢')]
  for n,t in cases:
   p=self.ps[n];a=p['text'].index(t);self.assertFalse(any(a<=m['start']<a+len(t)for m in p['mentions']),t)
 def test_variants_preserved_not_corrected(self):
  self.assertIn('萬姓顒，',self.ps[4]['text']);self.assertIn('祠乙太牢',self.ps[6]['text']);self.assertIn('長子軫',self.ps[7]['text']);d=J('source-evidence/jin089-jishao-source-quality.json');self.assertEqual(len(d['differences']),3);self.assertFalse(d['independent_ancient_testimony'])
 def test_only_direct_kinship_and_missing_father(self):
  a=J('corpus/jinshu/089-jishao-assertions.json')['assertions'];self.assertEqual(len(a),3);self.assertEqual([r['predicate']for r in a],['father','father','grandfather']);self.assertFalse(any(r['predicate']in ['birth_mother','adoptive_father','spouse']for r in a));typed=J('source-evidence/jin089-jishao-typed-proposals.json')['proposals'];self.assertTrue(any(r['kind']=='mother_role_unspecified'and r['biological_mother']is None for r in typed));self.assertTrue(any(r['kind']=='agnatic_grandnephew_and_title_successor'and r['adoptive_father_person_id']is None for r in typed))
 def test_rejected_miu_is_not_awarded_name(self):
  p=self.ps[2];a=p['text'].index('繆');self.assertFalse(any(m['start']<=a<m['end']for m in p['mentions']));typed=J('source-evidence/jin089-jishao-typed-proposals.json')['proposals'];r=next(x for x in typed if x['kind']=='rejected_posthumous_proposal');self.assertIsNone(r['adopted_title']);self.assertIn('時雖不從',r['source_term'])
if __name__=='__main__':unittest.main()
