from pathlib import Path
import json,unittest
from scripts.nanshi024_guhaozhi import errors,death_valid
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
class GuHaozhi(unittest.TestCase):
    def test_age_is_bound_to_gu(self):
        ch=read('corpus/nanqishu/043-guhaozhi.json');e,=read('corpus/nanqishu/043-guhaozhi-life-events.json')['events'];a,=ch['annotation']['age_assertions'];self.assertEqual(a['value'],49);self.assertEqual(a['age_context']['life_event_id'],e['id']);self.assertTrue(death_valid(e,e['evidence'][0],ch,ROOT));e['person_id']='0cf_pqs_mnm';self.assertFalse(death_valid(e,e['evidence'][0],ch,ROOT))
    def test_embedded_account_starts_at_zi(self):
        ch=read('corpus/nanshi/024-guhaozhi.json');p=ch['paragraphs'][0];self.assertTrue(p['text'].startswith('暠之字士明'));self.assertFalse(errors(ch,ROOT));p['text']='思遠迎其妻子，'+p['text'];self.assertTrue(errors(ch,ROOT))
