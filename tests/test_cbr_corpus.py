import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('corpus_validator',ROOT/'scripts/validate_corpus.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for folder in ('registry','corpus'):shutil.copytree(ROOT/folder,self.root/folder)
    def change(self,path,fn):
        p=self.root/path;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d,ensure_ascii=False))
    def test_corpus(self):self.assertEqual(v.validate(self.root),[])
    def test_unknown_person_rejected(self):
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0]['mentions'][0].update(person_id='missing'))
        self.assertTrue(any('未知人物' in e for e in v.validate(self.root)))
    def test_changed_offsets_rejected(self):
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0]['mentions'][0].update(start=1))
        self.assertTrue(any('位置不符' in e for e in v.validate(self.root)))
    def test_wrong_book_rejected(self):
        self.change('corpus/shiji/001.json',lambda d:d.update(book_id='b-shiji-002'))
        self.assertTrue(any('歸屬不符' in e for e in v.validate(self.root)))
    def test_xml_text_drift_rejected(self):
        p=self.root/'corpus/shiji/001.xml';p.write_text(p.read_text().replace('生而神靈','改竄正文',1))
        self.assertTrue(any('正文還原' in e for e in v.validate(self.root)))
    def test_unresolved_does_not_claim_person(self):
        def mutate(d):next(m for p in d['paragraphs'] for m in p['mentions'] if m['kind']=='unresolved').update(person_id='cbr-p000001')
        self.change('corpus/shiji/001.json',mutate)
        self.assertTrue(any('不得暗選' in e for e in v.validate(self.root)))
    def test_epithet_context_is_not_a_name(self):
        d=json.loads((self.root/'corpus/shiji/001.json').read_text())
        for p in d['paragraphs']:
            for term in ('軒轅之丘','象以典刑','夔夔唯謹','九男皆益篤'):
                if term in p['text']:
                    start=p['text'].index(term)
                    for m in p['mentions']:
                        self.assertFalse(m['kind']=='person' and start<=m['start']<start+len(term))
if __name__=='__main__':unittest.main()
