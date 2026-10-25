# coding:utf-8
from pathlib import Path
import json,copy,hashlib,unittest
R=Path(__file__).resolve().parents[1];CID='c-jinshu-043-guoshu'
class GuoshuSourceTests(unittest.TestCase):
 def test_nearest_parent_close_preserves_full_unit(self):
  from scripts.fixed_biography_subsections import project
  raw='===甲===\n甲傳全文。\n\n==乙==\n乙文。\n';a,z,ps,excluded=project(raw,'甲傳','===甲===','==乙==');self.assertEqual([p['text']for p in ps],['甲傳全文。']);self.assertEqual(raw[z:z+5],'==乙==')
  with self.assertRaises(AssertionError):project('===甲===\n甲文\n===近節===\n近文\n==父節==\n','甲傳','===甲===','==父節==')
  with self.assertRaises(AssertionError):project(raw,'甲傳','===甲===','===乙===')
 def test_all_registered_selectors_keep_existing_scope_and_fidelity(self):
  from scripts.fixed_attached_subsection_selection import errors,required_ref_error
  pins=json.loads((R/'scripts/fixed_attached_subsection_witnesses.json').read_text())['chapters'];chapters={}
  for f in(R/'corpus').glob('*/*.json'):
   c=json.loads(f.read_text())
   if c.get('id')in pins:chapters[c['id']]=c
  self.assertTrue({'c-jinshu-044-luchen-cuiyue','c-jinshu-043-wangyan','c-jinshu-043-wangcheng',CID}<=set(chapters))
  for cid,pin in pins.items():
   c=chapters[cid];b=json.loads((R/pin['projection_ref']).read_text());self.assertEqual(required_ref_error(c,R),[]);self.assertEqual(errors(c,R,b),[])
 def test_complete_five_received_paragraphs_and_contextual_name_readings(self):
  c=json.loads((R/'corpus/jinshu/043-guoshu.json').read_text());self.assertEqual(len(c['paragraphs']),5);self.assertEqual(sum(len(p['text'])for p in c['paragraphs']),862);self.assertTrue(c['paragraphs'][0]['text'].startswith('郭舒，字稚行。'));self.assertTrue(c['paragraphs'][-1]['text'].endswith('表為梁州刺史。病卒。'))
  cases=c['annotation']['source_reading_cases'];name=next(x for x in cases if x['id'].endswith('zongxin-reading'));self.assertEqual((name['received_surface'],name['preferred_name_reading']),('宗庾廞','宗廞'));self.assertIn('王暠',c['paragraphs'][-1]['text']);self.assertIn('硃雲',c['paragraphs'][-1]['text'])
  source=json.loads((R/'corpus/jinshu/076.json').read_text());wangyi=next(m['person_id']for p in source['paragraphs']for m in p['mentions']if m['id']=='c-jinshu-076-wangyi-family:p001:m0000');ms=[m for p in c['paragraphs']for m in p['mentions']if m['surface']in('王暠','暠')];self.assertEqual(len(ms),2);self.assertTrue(all(m['person_id']==wangyi for m in ms))
  # Ordinary quality 弘量 and nested landowner我 must not point to劉弘/王敦.
  p=c['paragraphs'][2];i=p['text'].index('弘量');self.assertFalse(any(m['start']<=i<m['end']for m in p['mentions']));p=c['paragraphs'][-1];i=p['text'].index('我地');m=next(m for m in p['mentions']if m['start']==i);self.assertEqual((m['kind'],m['person_id']),('unresolved',None))
if __name__=='__main__':unittest.main()
