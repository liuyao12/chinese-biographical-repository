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
    def test_cross_chapter_identity_needs_both_sources(self):
        def mutate(d):
            decision=next(v for v in d['decisions'] if v['scope']=='cross_chapter')
            decision['evidence']=decision['evidence'][:1]
        self.change('corpus/shiji/002-identities.json',mutate)
        self.assertTrue(any('各篇證據' in e for e in v.validate(self.root)))
    def test_relationship_requires_exact_source(self):
        def mutate(d):d['assertions'][0]['evidence'][0]['source_id']='s-shiji-001-wudi'
        self.change('corpus/shiji/002-assertions.json',mutate)
        self.assertTrue(any('來源 ID 不符' in e for e in v.validate(self.root)))
    def test_relationship_unknown_person_rejected(self):
        def mutate(d):d['assertions'][0]['object_person_id']='missing'
        self.change('corpus/shiji/002-assertions.json',mutate)
        self.assertTrue(any('引用未知人物' in e for e in v.validate(self.root)))
    def test_xia_context_does_not_merge_officials_across_generations(self):
        chapter=json.loads((self.root/'corpus/shiji/002.json').read_text())
        paragraph=next(p for p in chapter['paragraphs'] if '羲、和湎淫' in p['text'])
        mention=next(m for m in paragraph['mentions'] if m['surface']=='羲、和')
        self.assertIsNone(mention['person_id'])
        start=paragraph['text'].index('作胤征')+1
        self.assertFalse(any(m['kind']=='person' and m['start']==start for m in paragraph['mentions']))

    def test_yin_same_title_keeps_distinct_people(self):
        d=json.loads((self.root/'corpus/shiji/003.json').read_text())
        def people_at(n,surface):
            return {m['person_id'] for m in d['paragraphs'][n-1]['mentions'] if m['surface']==surface}
        self.assertTrue(people_at(7,'武王').isdisjoint(people_at(30,'武王')))
        self.assertTrue(people_at(11,'太丁').isdisjoint(people_at(26,'帝太丁')))
        self.assertEqual(len(people_at(7,'武王')),1)
        self.assertEqual(len(people_at(30,'武王')),1)
    def test_distinction_rejects_same_person_twice(self):
        def mutate(d):
            ids=d['distinctions'][0]['person_ids'];ids[1]=ids[0]
        self.change('corpus/shiji/003-distinctions.json',mutate)
        self.assertTrue(any('區分端點無效' in e for e in v.validate(self.root)))
    def test_distinction_needs_each_person_evidence(self):
        self.change('corpus/shiji/003-distinctions.json',lambda d:d['distinctions'][0].update(evidence=d['distinctions'][0]['evidence'][:1]))
        self.assertTrue(any('各端點證據' in e for e in v.validate(self.root)))
    def test_yin_book_title_is_not_person_occurrence(self):
        d=json.loads((self.root/'corpus/shiji/003.json').read_text())
        for n,term in [(4,'作湯征'),(5,'作女鳩女房'),(17,'仲丁書'),(20,'作盤庚'),(23,'高宗肜日')]:
            p=d['paragraphs'][n-1];start=p['text'].index(term);end=start+len(term)
            self.assertFalse(any(m['kind']=='person' and start<=m['start']<end for m in p['mentions']))
        self.assertTrue(any(m['kind']=='person' and m['start']==0 for m in d['paragraphs'][3]['mentions']))
    def test_yin_verb_yi_is_not_an_unrelated_person(self):
        d=json.loads((self.root/'corpus/shiji/003.json').read_text())
        for n,term in [(28,'益收'),(28,'益廣'),(29,'益疏')]:
            p=d['paragraphs'][n-1];start=p['text'].index(term)
            self.assertFalse(any(m['kind']=='person' and m['start']==start for m in p['mentions']))

    def test_partial_chapter_cannot_claim_first_pass(self):
        self.change('corpus/shiji/004.json',lambda d:d['paragraphs'][-1].update(annotation_status='pending',mentions=[]))
        self.assertTrue(any('不得宣稱首輪完成' in e for e in v.validate(self.root)))
    def test_partial_progress_cannot_skip_pending_paragraphs(self):
        def mutate(d):
            next(b for b in d['books'] if b['book_id']=='b-shiji-004')['person_status']='named_mentions_first_pass'
        self.change('corpus/shiji/004.json',lambda d:d['paragraphs'][-1].update(annotation_status='pending',mentions=[]))
        self.change('corpus/progress.json',mutate)
        self.assertTrue(any('有待標註段落' in e for e in v.validate(self.root)))
    def test_zhou_qi_verb_is_not_a_person(self):
        d=json.loads((self.root/'corpus/shiji/004.json').read_text())
        p=d['paragraphs'][0]
        for term in ('棄之隘巷','棄渠中','初欲棄之'):
            start=p['text'].index(term)+(2 if term=='初欲棄之' else 0)
            self.assertFalse(any(m['kind']=='person' and m['start']==start for m in p['mentions']))
    def test_zhou_boyi_is_distinct_from_shun_official(self):
        d=json.loads((self.root/'corpus/shiji/004.json').read_text())
        m=next(m for m in d['paragraphs'][6]['mentions'] if m['surface']=='伯夷')
        self.assertNotEqual(m['person_id'],'cbr-p000047')

    def test_unresolved_identity_rejects_unknown_candidate(self):
        def mutate(d):d['annotation']['unresolved_identity_cases'][0]['candidate_person_ids'][0]='missing'
        self.change('corpus/shiji/004.json',mutate)
        self.assertTrue(any('候選人物無效' in e for e in v.validate(self.root)))
    def test_unresolved_identity_requires_candidate_evidence(self):
        def mutate(d):d['annotation']['unresolved_identity_cases'][0]['paragraph_ids']=['c-shiji-004-zhou:p083']
        self.change('corpus/shiji/004.json',mutate)
        self.assertTrue(any('各候選人物的段落證據' in e for e in v.validate(self.root)))
    def test_zhou_succession_preserves_explicit_generations(self):
        d=json.loads((self.root/'corpus/shiji/004-assertions.json').read_text())
        claims={(a['subject_person_id'],a['predicate'],a['object_person_id']) for a in d['assertions']}
        self.assertIn(('cbr-p000227','father','cbr-p000226'),claims)
        self.assertIn(('cbr-p000227','grandfather','cbr-p000222'),claims)
        self.assertNotIn(('cbr-p000227','father','cbr-p000222'),claims)

    def test_epithet_context_is_not_a_name(self):
        d=json.loads((self.root/'corpus/shiji/001.json').read_text())
        for p in d['paragraphs']:
            for term in ('軒轅之丘','象以典刑','夔夔唯謹','九男皆益篤'):
                if term in p['text']:
                    start=p['text'].index(term)
                    for m in p['mentions']:
                        self.assertFalse(m['kind']=='person' and start<=m['start']<start+len(term))
if __name__=='__main__':unittest.main()
