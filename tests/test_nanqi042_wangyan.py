from copy import deepcopy
from pathlib import Path
import json,unittest
from scripts.nanqi042_wangyan import errors, kin_valid, proposal_valid
ROOT=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((ROOT/p).read_text())
class WangYan(unittest.TestCase):
    def test_unassumed_and_imperial_charges(self):
        ch=rd('corpus/nanqishu/042-wangyan.json');self.assertFalse(errors(ch,ROOT));pr=ch['annotation']['title_proposals'];self.assertEqual({p['title']for p in pr},{'射聲校尉','左衞將軍','給事中','冠軍將軍','司徒左長史','濟陽太守','江州刺史'});self.assertTrue(all(proposal_valid(p,ch)for p in pr));q=deepcopy(pr[-1]);q['outcome']='held';self.assertFalse(proposal_valid(q,ch));self.assertEqual(len([e for e in ch['annotation']['narrative_readings']if e['event_type']=='charge']),3);self.assertEqual(ch['source']['related_excerpt']['chapter_id'],'c-nanqishu-042-wangyan-father-and-grandfather')
    def test_shengfu_and_chuji(self):
        ch=rd('corpus/songshu/072-linhe-zichan.json');k=rd('corpus/songshu/072-linhe-zichan-assertions.json')['assertions'];f,a=k;self.assertEqual(f['qualifiers']['birth_order']['ordinal'],18);self.assertEqual(a['predicate'],'adoptive_father');self.assertNotEqual(a['object_person_id'],f['object_person_id']);self.assertTrue(kin_valid(a,ch,ROOT));a['object_person_id']=f['object_person_id'];self.assertFalse(kin_valid(a,ch,ROOT))
