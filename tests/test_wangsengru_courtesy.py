from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.person_bundle import validate_courtesy_name


ROOT = Path(__file__).resolve().parents[1] / 'corpus'


class WangsengruCourtesyTests(unittest.TestCase):
    def test_each_history_explicitly_names_the_same_person_twice(self):
        for stem in ('liangshu/033-wangsengru', 'nanshi/059-wangsengru'):
            with self.subTest(stem=stem):
                p = json.loads((ROOT / (stem + '.json')).read_bytes())['paragraphs'][0]
                records = json.loads((ROOT / (stem + '-name-components.json')).read_bytes())['records']
                n, = [row for row in records if row['person_id'] == '59d_72d_924_AAA']
                self.assertEqual((n['ming'], n['zi']), ('僧孺', '僧孺'))
                validate_courtesy_name(n, p)
                with self.assertRaises(ValueError):
                    validate_courtesy_name(n)
                with self.assertRaises(ValueError):
                    validate_courtesy_name(dict(n, quote='王僧孺字僧孺'), p)
                for index in (0, 1):
                    wrong = deepcopy(p)
                    wrong['mentions'][index]['person_id'] = 'other-person'
                    with self.assertRaises(ValueError):
                        validate_courtesy_name(n, wrong)
