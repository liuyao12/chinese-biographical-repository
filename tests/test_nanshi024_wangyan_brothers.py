from copy import deepcopy
from pathlib import Path
import json,unittest
from scripts.nanshi024_wangyan_brothers import errors, kin_valid, death_valid
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())

class WangYanFamilyAccounts(unittest.TestCase):
    def test_distinguishes_three_mentions_of_zhan(self):
        ch=read('corpus/nanshi/024-wangdeyuan.json');p=ch['paragraphs'][0];ids={m['surface']:m['person_id']for m in p['mentions']};self.assertEqual(ids['湛'],ids['德元']);self.assertEqual(len({ids['湛'],ids['江湛'],ids['劉湛']}),3);self.assertEqual(ch['annotation']['person_reference_occurrences'][0]['person_id'],'kix_r92_2ed');self.assertFalse(errors(ch,ROOT));m=next(m for m in p['mentions']if m['surface']=='江湛');m['person_id']=ids['湛'];self.assertTrue(errors(ch,ROOT))

    def test_sibling_order_and_execution_witnesses(self):
        for work,number in [('nanshi','024'),('nanqishu','042')]:
            stem=f'corpus/{work}/{number}-wangxu-yan';ch=read(stem+'.json');kin,=read(stem+'-assertions.json')['assertions'];self.assertTrue(kin_valid(kin,ch,ROOT));bad=deepcopy(kin);bad['qualifiers']['relative_birth_order']['older_person_id']=kin['object_person_id'];self.assertFalse(kin_valid(bad,ch,ROOT));rows=read(stem+'-life-events.json')['events'];self.assertEqual(len(rows),3 if work=='nanqishu' else 2);self.assertTrue(all(row['date_expression'] is None and death_valid(row,row['evidence'][0],ch,ROOT) for row in rows));self.assertEqual(('蕭季敞' in ch['paragraphs'][0]['text']),work=='nanqishu');self.assertNotIn('黃門郎',[v['title']for v in read(stem+'-titles.json')['holdings']]);self.assertTrue(any(m['kind']=='unresolved'and m['surface']=='黃門郎'for m in ch['paragraphs'][0]['mentions']))
