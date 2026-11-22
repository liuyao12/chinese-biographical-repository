from copy import deepcopy
from pathlib import Path
import json
import unittest
from scripts.song093_wyd import errors, kin_valid, proposal_valid

ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())

class Song93Palace(unittest.TestCase):
    def test_printed_families_and_glyphs(self):
        ch=read('corpus/songshu/093-wanghongzhi-wyd.json')
        self.assertFalse(errors(ch,ROOT))
        t=ch['paragraphs'][0]['text']
        self.assertEqual(t.count('𢎞'),16);self.assertEqual(t.count('𤣥'),1)
        self.assertIn('何淮',t);self.assertIn('每隨兄',t)
        bad=deepcopy(ch);bad['paragraphs'][0]['text']=t.replace('每隨兄','母隨兄')
        self.assertTrue(errors(bad,ROOT))
        rows=read('corpus/songshu/093-wanghongzhi-wyd-assertions.json')['assertions']
        self.assertFalse(any(row['predicate']=='mother' for row in rows))
        care=next(r for r in rows if r['predicate']=='raised_by');self.assertTrue(kin_valid(care,ch,ROOT))
        care['predicate']='father';self.assertFalse(kin_valid(care,ch,ROOT))

    def test_edition_boundaries_and_declined_offices(self):
        tan=read('corpus/songshu/093-wangtansheng-wyd.json');r=read('corpus/songshu/093-ruanwanling-wyd.json')
        self.assertFalse(errors(tan,ROOT));self.assertFalse(errors(r,ROOT))
        p=tan['paragraphs'][0];self.assertEqual(p['source_position']['column_projection'][0]['column_from_right'],4)
        self.assertTrue(p['text'].endswith('終於中散大夫'));p['source_position']['column_projection'][0]['start']-=1
        self.assertTrue(errors(tan,ROOT));prop=r['annotation']['title_proposals'][0];self.assertTrue(proposal_valid(prop,r))
        prop['title']='左民尚書';self.assertFalse(proposal_valid(prop,r))
