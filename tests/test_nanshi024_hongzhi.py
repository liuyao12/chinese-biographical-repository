import json
from copy import deepcopy
from pathlib import Path
import unittest
from scripts.nanshi024_wanghongzhi import errors, kin_valid, proposal_valid

ROOT=Path(__file__).resolve().parents[1]
def read(f):return json.loads((ROOT/f).read_text())

class NanshiHongzhi(unittest.TestCase):
    def test_grandfather_mother_and_custody(self):
        ch=read('corpus/nanshi/024.json');d=read('corpus/nanshi/024-assertions.json')
        self.assertFalse(errors(ch,ROOT));q=next(a for a in d['assertions'] if a['id']=='a-nanshi024-wanghongzhi-care')
        self.assertTrue(kin_valid(q,ch,ROOT));bad=deepcopy(q);bad['predicate']='father';self.assertFalse(kin_valid(bad,ch,ROOT))
        p=next(p for p in ch['paragraphs'] if p['id'].endswith('line077'));p['text']=p['text'].replace('母隨兄','每隨兄')
        self.assertTrue(errors(ch,ROOT))

    def test_declined_office_and_direct_name_components(self):
        ch=read('corpus/nanshi/024.json');q=next(p for p in ch['annotation']['title_proposals'] if p['id']=='tp-nanshi024-wanghongzhi-tongzhi');self.assertTrue(proposal_valid(q,ch));q['outcome']='accepted';self.assertFalse(proposal_valid(q,ch))
        rec=read('corpus/nanshi/024-name-components.json')['records'];n=[r for r in rec if r['id'].startswith('nc-nanshi024-wanghongzhi-')];self.assertEqual(len(n),2)
        self.assertNotIn('surname',n[0]);self.assertEqual(n[0]['zi'],'方平');self.assertEqual(n[1]['surname'],'王');self.assertNotIn('zi',n[1]);self.assertIn('王弘之',n[1]['quote'])
