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

    def test_qin_sisters_keep_literal_kinship_and_anonymity(self):
        c=json.loads((self.root/'corpus/shiji/005.json').read_text())
        a=json.loads((self.root/'corpus/shiji/005-assertions.json').read_text())
        sister=next(m for m in c['paragraphs'][20]['mentions'] if m['surface']=='姊')
        claim=next(a for a in a['assertions'] if a['subject_person_id']==sister['person_id'] and a['predicate']=='sister')
        self.assertEqual(claim['qualifiers']['source_term'],'姊')
        self.assertIn('晉太子申生姊也',claim['evidence'][0]['quote'])
        p=next(p for p in json.loads((self.root/'registry/persons.json').read_text())['persons'] if p['id']==sister['person_id'])
        self.assertFalse(any(a['surface']=='穆姬' for a in p['aliases']))

    def test_qin_qi_daogong_resolved_per_occurrence(self):
        c=json.loads((self.root/'corpus/shiji/005.json').read_text())
        p=c['paragraphs'][45]
        def at(term):
            start=p['text'].index(term)+term.index('悼公')
            return next(m['person_id'] for m in p['mentions'] if m['start']==start)
        self.assertEqual(at('悼公二年'),at('秦悼公'))
        self.assertEqual(at('是為悼公'),at('齊人弒悼公'))
        self.assertNotEqual(at('悼公二年'),at('是為悼公'))
    def test_shangjun_title_and_work_pointer_are_distinct(self):
        c=json.loads((self.root/'corpus/shiji/005.json').read_text())
        p=c['paragraphs'][57];start=p['text'].index('商君語')
        self.assertFalse(any(m['kind']=='person' and start<=m['start']<start+3 for m in p['mentions']))
        p=c['paragraphs'][60]
        title=next(m for m in p['mentions'] if m['surface']=='商君')
        name=next(m for m in p['mentions'] if m['surface']=='衛鞅')
        self.assertEqual(title['person_id'],name['person_id'])
        self.assertEqual(title['kind'],'person')

    def test_appended_note_layer_survives_xml(self):
        c=json.loads((self.root/'corpus/shiji/006.json').read_text())
        self.assertEqual(next(p for p in c['paragraphs'] if p['id']=='c-shiji-006-shihuang:p106')['text_layer'],'received_chapter')
        self.assertEqual(next(p for p in c['paragraphs'] if p['id']=='c-shiji-006-shihuang:p107')['text_layer'],'witness_appended_bangu_note')
        p=self.root/'corpus/shiji/006.xml'
        p.write_text(p.read_text().replace('text-layer="witness_appended_bangu_note"','text-layer="received_chapter"',1))
        self.assertTrue(any('文字層次不符' in e for e in v.validate(self.root)))

    def test_shihuang_dd_quotes_preserve_order_and_xml_text(self):
        c=json.loads((self.root/'corpus/shiji/006.json').read_text())
        ids=[p['id'] for p in c['paragraphs']]
        self.assertEqual(sum(p.get('source_block_kind')=='witness_dd' for p in c['paragraphs']),16)
        self.assertLess(ids.index('c-shiji-006-shihuang:p029'),ids.index('c-shiji-006-shihuang:p029:block01'))
        self.assertLess(ids.index('c-shiji-006-shihuang:p029:block01'),ids.index('c-shiji-006-shihuang:p030'))
        p=next(p for p in c['paragraphs'] if p['id']=='c-shiji-006-shihuang:p029:block01')
        self.assertTrue(p['text'].startswith('維二十八年，皇帝作始'))
        self.assertEqual(v.validate(self.root),[])

    def test_shihuang_conflicting_genealogy_claims_are_preserved(self):
        c=json.loads((self.root/'corpus/shiji/006.json').read_text())
        by={p['id']:p for p in c['paragraphs']}
        p=by['c-shiji-006-shihuang:p085']
        person=next(m['person_id'] for m in p['mentions'] if m['surface']=='靈公')
        claims=json.loads((self.root/'corpus/shiji/006-assertions.json').read_text())['assertions']
        selected=[a for a in claims if a['subject_person_id']==person and a['predicate']=='father' and a['evidence'][0]['paragraph_id'] in ('c-shiji-006-shihuang:p085','c-shiji-006-shihuang:p086')]
        self.assertEqual(len(selected),2)
        self.assertEqual(len({a['object_person_id'] for a in selected}),2)
        self.assertTrue(any('生靈公' in a['evidence'][0]['quote'] for a in selected))
        self.assertTrue(any('昭子子也' in a['evidence'][0]['quote'] for a in selected))

    def test_epithet_context_is_not_a_name(self):
        d=json.loads((self.root/'corpus/shiji/001.json').read_text())
        for p in d['paragraphs']:
            for term in ('軒轅之丘','象以典刑','夔夔唯謹','九男皆益篤'):
                if term in p['text']:
                    start=p['text'].index(term)
                    for m in p['mentions']:
                        self.assertFalse(m['kind']=='person' and start<=m['start']<start+len(term))
    def test_xiangyu_paternal_uncle_does_not_create_father(self):
        data=json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())
        relations=[a for a in data['assertions'] if a['subject_person_id']=='cbr-p000610']
        self.assertEqual([(a['predicate'],a['object_person_id']) for a in relations],[('paternal_uncle','cbr-p000603')])
        self.assertEqual(relations[0]['qualifiers']['source_term'],'季父')
    def test_huaiwang_grandson_phrase_keeps_two_generations(self):
        chapter=json.loads((self.root/'corpus/shiji/007.json').read_text())
        p=chapter['paragraphs'][5]
        grandfather=p['text'].index('乃求楚懷王')+2
        grandson=p['text'].index('立以為楚懷王')+3
        mentions={m['start']:m for m in p['mentions']}
        self.assertEqual(mentions[grandfather]['person_id'],'cbr-p000505')
        self.assertNotEqual(mentions[grandfather]['person_id'],mentions[grandson]['person_id'])
        relation=next(a for a in json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())['assertions'] if a['predicate']=='grandfather')
        self.assertEqual(relation['subject_person_id'],mentions[grandson]['person_id'])
        self.assertEqual(relation['object_person_id'],mentions[grandfather]['person_id'])
    def test_kuaiji_governor_succession_not_same_title_identity(self):
        p=json.loads((self.root/'corpus/shiji/007.json').read_text())['paragraphs'][2]
        governor=p['text'].index('會稽守通')
        successor=p['text'].rindex('會稽守')
        mentions={m['start']:m for m in p['mentions']}
        self.assertEqual(mentions[governor]['kind'],'person')
        self.assertEqual(mentions[successor]['kind'],'unresolved')
        self.assertIsNone(mentions[successor]['person_id'])

if __name__=='__main__':unittest.main()
