import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class XijianSourceWitnessTests(unittest.TestCase):
    def test_hash_names_the_captured_excerpt_not_remote_wikitext(self):
        chapter = json.loads((ROOT / 'corpus/jinshu/067-xijian-family.json').read_text())
        source = chapter['source']
        excerpt = (ROOT / source['raw_file']).read_bytes()
        self.assertEqual(hashlib.sha256(excerpt).hexdigest(), source['excerpt_file_sha256'])
        self.assertFalse(source['source_wikitext_captured'])
        self.assertIn('非來源頁面wikitext', source['normalization']['extraction_note'])
        self.assertIn('oldid=2592755', source['permalink'])


if __name__ == '__main__':
    unittest.main()
