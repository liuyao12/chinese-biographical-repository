import copy
import json
import unittest
from pathlib import Path
from scripts.current_office_death import current_office_death_valid

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    # The real source anchors are needed to check that only its last named office
    # ends here; this never generates synthetic source data in the repository.
    c = json.loads((ROOT / 'corpus/songshu/060.json').read_text())
    h = next(h for h in json.loads((ROOT / 'corpus/songshu/060-titles.json').read_text())['holdings'] if h['title'] == '東陽太守')
    paragraphs = {p['id']: (c['id'], p) for p in c['paragraphs']}
    mentions = {m['id']: (c['id'], p['id'], m) for p in c['paragraphs'] for m in p['mentions']}
    return h, paragraphs, mentions


class CurrentOfficeDeathTests(unittest.TestCase):
    def test_actual_local_graduated_office_death(self):
        self.assertTrue(current_office_death_valid(*fixture()))

    def test_other_offices_cannot_inherit_death(self):
        for title in ['太子僕', '御史中丞', '司徒左長史']:
            h, p, m = fixture(); h['title'] = title
            h['end_basis']['source_term'] = title + '。元嘉十五年，卒官'
            self.assertFalse(current_office_death_valid(h, p, m))

    def test_wrong_person_or_attestation_rejected(self):
        h, p, m = fixture(); h['person_id'] = 'someone-else'
        self.assertFalse(current_office_death_valid(h, p, m))
        h, p, m = fixture(); h['attestations'][0]['start'] += 1
        self.assertFalse(current_office_death_valid(h, p, m))

    def test_death_must_be_local_and_same_evidence(self):
        h, p, m = fixture(); h['end_basis']['source_term'] = '卒官'
        self.assertFalse(current_office_death_valid(h, p, m))
        h, p, m = fixture(); h['end_basis']['evidence'] = []
        self.assertFalse(current_office_death_valid(h, p, m))
