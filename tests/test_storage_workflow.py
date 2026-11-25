import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.corpus_overlay import edited_inputs
from scripts.profile_passages import ReaderPassages
from scripts.stage_chapter_links import materialize


class StorageWorkflowTests(unittest.TestCase):
    def test_mutations_are_private_and_discarded_after_an_exception(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'input.json'
            source.write_bytes(b'original')
            with self.assertRaises(ZeroDivisionError), edited_inputs(root) as changes:
                self.assertEqual(source.read_bytes(), b'original')
                self.assertFalse(changes)
                with source.open('ab') as stream:
                    stream.write(b' edit')
                self.assertEqual(source.stat().st_size, len(b'original edit'))
                self.assertEqual(source.read_bytes(), b'original edit')
                (root / 'new.json').write_bytes(b'private')
                self.assertTrue((root / 'new.json').is_file())
                self.assertEqual(len(changes), 2)
                raise ZeroDivisionError
            self.assertEqual(source.read_bytes(), b'original')
            self.assertFalse((root / 'new.json').exists())

    def test_public_link_is_materialized_once_and_quote_uses_code_points(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            native = root / 'corpus/shiji/001.json'
            native.parent.mkdir(parents=True)
            witness = dict(id='c1', work_id='w1', book_id='b1', source_id='s1')
            native.write_text(json.dumps(dict(witness, record_type='marked_chapter',
                source={'edition':'A'}, paragraphs=[dict(id='p1',text='甲𠮷乙',mentions=[])])))
            url = Path('data/corpus/shiji/001.json')
            site = root / 'staged'
            for base in (root, site):
                (base / url).parent.mkdir(parents=True)
                (base / url).symlink_to('../../../corpus/shiji/001.json')
            materialize(root, site)
            self.assertFalse((site / url).is_symlink())
            self.assertEqual((site / url).read_bytes(), native.read_bytes())
            reader = ReaderPassages(site)
            row = dict(chapter_id='c1', work_id='w1', book_id='b1', source_id='s1', paragraph_id='p1')
            profile = dict(occurrences=[dict(row,quote='𠮷乙')])
            compact = reader.convert(profile)
            self.assertEqual(compact['occurrences'][0]['quote_span'], [1,3])
            self.assertEqual(reader.convert(compact, expand=True), profile)
            compact['occurrences'][0]['quote_span'][1] = 5
            with self.assertRaises(ValueError):
                reader.convert(compact, expand=True)
