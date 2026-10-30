from tests.portable_fixture_copy import fixture_copy2
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.validate_corpus import parallel_event_date, validate
ROOT = Path(__file__).resolve().parents[1]


def _copy_source_fixture(root):
    for name in ('registry','corpus','source-evidence','sources','scripts','docs','schema','data/historical-tables'):
        (root/name).parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(ROOT/name,root/name, copy_function=fixture_copy2)
    (root/'data/corpus').mkdir(parents=True,exist_ok=True)
    for name in ('profile-names.json','chapter-directory.json'):
        shutil.copy2(ROOT/'data/corpus'/name,root/'data/corpus'/name)

class ChunshenEvidenceTests(unittest.TestCase):
    def test_unmodified_source_fixture_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            _copy_source_fixture(root)
            self.assertEqual(validate(root),[])

    def test_parallel_event_and_year_have_separate_exact_source_urls(self):
        data = json.loads((ROOT/'corpus/shiji/078-life-events.json').read_text())
        event = data['events'][1]
        date = event['normalized_date']
        self.assertEqual((date['era_year'], date['year']), (263, -262))
        self.assertNotEqual(date['basis']['reference_url'], date['basis']['reference_year_url'])
        self.assertTrue(parallel_event_date(date))
        changed = copy.deepcopy(date)
        changed['basis']['reference_year_url'] = changed['basis']['reference_url']
        self.assertFalse(parallel_event_date(changed))
        changed = copy.deepcopy(date)
        changed['references'][0]['url'] = changed['basis']['reference_year_url']
        self.assertFalse(parallel_event_date(changed))

    def test_chunshen_death_does_not_set_title_endpoints_or_burial(self):
        events = json.loads((ROOT/'corpus/shiji/078-life-events.json').read_text())['events']
        death = next(e for e in events if e['person_id']=='e79_ty0_mkx')
        self.assertEqual(death['normalized_date']['era_year'], 238)
        self.assertIn('斬其頭', death['source_term'])
        addresses = json.loads((ROOT/'corpus/shiji/078-addresses.json').read_text())['assertions']
        self.assertTrue({('biographical_origin','楚'), ('death_place','棘門')}.issubset({(a['relation'], a['place']['source_name']) for a in addresses if a['person_id']=='e79_ty0_mkx'}))
        self.assertFalse(any(a['relation']=='burial_place' for a in addresses))

    def test_grant_year_does_not_inherit_death_as_title_end(self):
        holdings = json.loads((ROOT/'corpus/shiji/078-titles.json').read_text())['holdings']
        selected = [h for h in holdings if h['id'] in ('th-shiji078-010','th-shiji078-011')]
        self.assertEqual(len(selected), 2)
        for h in selected:
            self.assertEqual(h['effective_period']['start']['date_expression'], '考烈王元年')
            self.assertEqual(h['effective_period']['start']['normalized_date']['era_year'], 262)
            self.assertEqual(h['effective_period']['end']['status'], 'unknown')
            self.assertNotIn('normalized_date', h['effective_period']['end'])

    def test_request_without_approval_cannot_be_recorded_as_granted_fief(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_source_fixture(root)
            path = root/'corpus/shiji/078-addresses.json'
            data = json.loads(path.read_text())
            address = next(a for a in data['assertions'] if a['id']=='pa-shiji078-005')
            address['source_term'] = '請封於江東'
            path.write_text(json.dumps(data, ensure_ascii=False))
            self.assertIn('准封地望須保存提請與明示允許，不得只據請封記實授', validate(root))

    def test_lu_start_year_keeps_different_dismissal_chronologies(self):
        holdings = json.loads((ROOT/'corpus/shiji/078-titles.json').read_text())['holdings']
        lu = next(h for h in holdings if h['id']=='th-shiji078-013')
        self.assertEqual(lu['effective_period']['start']['normalized_date']['era_year'], 249)
        self.assertNotIn('normalized_date', lu['effective_period']['end'])
        self.assertIn('九年', lu['effective_period']['end']['evidence'][0]['quote'])
        table = json.loads((ROOT/'data/historical-tables/shiji-015.json').read_text())
        cell = next(c for f in table['fragments'] for r in f['rows'] for c in r['cells'] if c['id']=='shiji-015-r240-c01')
        self.assertEqual(cell['text'], '十。相國呂不韋免。齊、趙來，置酒。太后入咸陽。大索。')
        xun = next(h for h in holdings if h['id']=='th-shiji078-012')
        self.assertEqual(xun['effective_period']['start']['date_expression'], '春申君相楚八年')
        self.assertNotIn('normalized_date', xun['effective_period']['start'])

    def test_reported_zhu_hai_variant_does_not_merge_zhu_ying_with_wei_retainer(self):
        chapter = json.loads((ROOT/'corpus/shiji/078.json').read_text())
        variant = next(v for v in chapter['annotation']['reported_variants'] if v['reported_reading']=='朱亥')
        self.assertFalse(variant['adopted'])
        self.assertEqual(variant['person_ids'], ['sxb_x2z_83z'])
        self.assertEqual(variant['received_reading'], '朱英')
        paragraph = next(p for p in chapter['paragraphs'] if p['id']==variant['paragraph_id'])
        self.assertIn('朱英知言不用', paragraph['text'])
        wei = json.loads((ROOT/'corpus/shiji/077.json').read_text())
        ids = {m['person_id'] for p in wei['paragraphs'] for m in p['mentions'] if m['surface']=='朱亥'}
        self.assertEqual(ids, {'88w_qqj_hs8'})
        self.assertNotIn('sxb_x2z_83z', ids)
