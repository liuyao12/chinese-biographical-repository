"""Fixed-source regression; run after identity materialization."""
from pathlib import Path
import json,unittest
from scripts.retired_person_ids import retired_person_ids,assert_not_retired
ROOT=Path(__file__).resolve().parents[1]
class WangSuiIdentity(unittest.TestCase):
 def test_source_spellings_and_independent_namesakes(self):
  a=json.loads((ROOT/'corpus/jinshu/035-pei-family.json').read_text());b=json.loads((ROOT/'corpus/jinshu/043-wangrong.json').read_text())
  p=next(p for p in a['paragraphs']if p['id'].endswith(':p011'));q=next(p for p in b['paragraphs']if p['id'].endswith(':p014'))
  sui=next(m for m in p['mentions']if m['id'].endswith(':m0022'));wan=next(m for m in q['mentions']if m['id'].endswith(':m0001'))
  self.assertEqual((sui['surface'],wan['surface']),('王綏','萬'));self.assertEqual(sui['person_id'],wan['person_id'])
  allpeople={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  original=[m for c in [a,b]for p in c['paragraphs']for m in p['mentions']if m.get('person_id')==sui['person_id'] and m['id']!='c-jinshu-035-peikai-family:p019:m0036'];self.assertEqual(len(original),7)
  group=next(m for p in a['paragraphs']for m in p['mentions']if m['id']=='c-jinshu-035-peikai-family:p019:m0036');self.assertEqual(group['person_id'],sui['person_id'])
  self.assertEqual({x['surface']for x in allpeople[sui['person_id']]['aliases']},{'王綏','綏','汝','萬'})
  self.assertNotEqual(sui['person_id'],'a8f_ec8_e74_AAAAABA');self.assertNotEqual(sui['person_id'],'vk5_fsh_iyt')
  self.assertNotIn('mqn_4g3_dcx',allpeople);self.assertFalse(any('mqn_4g3_dcx'in p.get('id_aliases',[])for p in allpeople.values()))
 def test_typed_retirement_and_ancient_note_layers(self):
  self.assertIn('mqn_4g3_dcx',retired_person_ids(ROOT))
  with self.assertRaises(ValueError):assert_not_retired('mqn_4g3_dcx',ROOT)
  e=ROOT/'source-evidence/wangsui-wanzi-identity';notes=json.loads((e/'ancient-note-layout-reconstruction.json').read_text())
  joined=''.join(n['visible_reconstructed']for n in notes if n['unit']=='賞譽第29條')
  self.assertIn('晉諸公賛曰王綏字萬子辟太尉掾不就年十九卒',joined)
  self.assertIn('戎子萬有美號而太肥戎令食穅而肥愈甚也',joined)
if __name__=='__main__':unittest.main()
