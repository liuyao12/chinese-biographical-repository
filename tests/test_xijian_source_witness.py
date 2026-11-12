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

    def test_wikisource_volume_heading_is_paratext_not_received_body(self):
        chapter = json.loads((ROOT / 'corpus/jinshu/067-xijian-family.json').read_text())
        heading = '溫嶠郗鑒〈（子愔 愔子超 愔弟曇 叔父隆）〉'
        self.assertNotIn(heading, [p['text'] for p in chapter['paragraphs']])
        self.assertEqual(chapter['annotation']['source_paratext'][0]['text'], heading)
        self.assertEqual(chapter['annotation']['source_paratext'][0]['kind'],
                         'wikisource_volume_heading_with_editorial_kinship_note')
        self.assertFalse(any(m['id'].startswith(chapter['id'] + ':p009:')
                             for p in chapter['paragraphs'] for m in p['mentions']))

    def test_retired_source_ids_have_no_active_identity_aliases(self):
        retired = {'6lr_zci_i0j', 'ier_lqj_x4q', 'e5k_f2i_cog',
                   '57b_1cb_a1b', 'ebb_5a7_96e'}
        registry = json.loads((ROOT / 'registry/persons.json').read_text())
        self.assertFalse(retired.intersection(p['id'] for p in registry['persons']))
        self.assertFalse(any(retired.intersection(p.get('id_aliases', []))
                             for p in registry['persons']))
        index = json.loads((ROOT / 'exports/persons/index.json').read_text())
        self.assertFalse(retired.intersection(p['person_id'] for p in index['persons']))
        self.assertFalse(retired.intersection(index.get('id_aliases', {})))


if __name__ == '__main__':
    unittest.main()
