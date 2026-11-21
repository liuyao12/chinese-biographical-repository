from copy import deepcopy
from pathlib import Path
import json,unittest
from scripts.nanshi024_wangsiyuan import errors,kin_valid,funeral_award
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
class WangSiyuan(unittest.TestCase):
    def test_grandfathers_siblings_and_orphaned_daughter(self):
        ch=read('corpus/nanshi/024-wangsiyuan.json');self.assertFalse(errors(ch,ROOT));K=read('corpus/nanshi/024-wangsiyuan-assertions.json')['assertions'];a=next(x for x in K if x['id'].endswith('-maternal-granddad'));self.assertEqual(a['object_person_id'],'qav_j5i_grm');self.assertTrue(kin_valid(a,ch,ROOT));a['object_person_id']='7r6_k52_qji_ABDACAB';self.assertFalse(kin_valid(a,ch,ROOT));self.assertEqual({x['subject_person_id']for x in K if x['predicate']=='brother'},{'7r6_k52_qji_ABDACABCA','7r6_k52_qji_ABDACABCB'});g=next(x for x in K if x['id'].endswith('-jing-princess'));self.assertEqual(g['object_person_id'],'ccd_af3_98e_A');self.assertEqual(ch['paragraphs'][-1]['text'][-5:],'經恤甚至。')
    def test_awards_and_spoken_names(self):
        ch=read('corpus/nanshi/024-wangsiyuan.json');deaths={e['id']:e for e in read('corpus/nanshi/024-wangsiyuan-life-events.json')['events']};h=[o for o in read('corpus/nanshi/024-wangsiyuan-titles.json')['holdings'] if o['mode'].startswith('posthumous_')];self.assertEqual(len(h),2);self.assertTrue(all(funeral_award(o,ch,deaths,ROOT)for o in h));h[0]['person_id']='i08_s4b_5bb';self.assertFalse(funeral_award(h[0],ch,deaths,ROOT));self.assertEqual({r['referent_role']for r in ch['annotation']['person_reference_occurrences']if r['surface']=='阿戎'},{'third_person','speaker_self'})
