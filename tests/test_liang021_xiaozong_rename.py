import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.person_bundle import validate_former_given_name


class XiaoZongRename(unittest.TestCase):
    def test_received_name_change_requires_the_same_person_on_both_ends(self):
        directory = Path(__file__).resolve().parents[1] / 'corpus/nanshi'
        names = json.loads((directory / '053-xiaozong-wangtai-name-components.json').read_text())
        record = next(n for n in names['records'] if 'former_ming' in n)
        chapter = json.loads((directory / '053-xiaozong-wangtai.json').read_text())
        paragraph = next(p for p in chapter['paragraphs'] if p['id'] == record['paragraph_id'])
        validate_former_given_name(record, paragraph)
        for surface in ('綜', '贊'):
            other = deepcopy(paragraph)
            next(m for m in other['mentions'] if m['surface'] == surface)['person_id'] = 'another-person'
            with self.assertRaises(ValueError):
                validate_former_given_name(record, other)
        with self.assertRaises(ValueError):
            validate_former_given_name(dict(record, quote='贊字德文'), paragraph)
