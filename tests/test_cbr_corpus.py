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
        def mutate(d):next(m for p in d['paragraphs'] for m in p['mentions'] if m['kind']=='unresolved').update(person_id='8jz_o3s_obt')
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
        self.assertNotEqual(m['person_id'],'uxv_pg9_8rm')

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
        self.assertIn(('ttx_okj_hbd','father','qk9_ejk_fnc'),claims)
        self.assertIn(('ttx_okj_hbd','grandfather','f3g_x6y_1iy'),claims)
        self.assertNotIn(('ttx_okj_hbd','father','f3g_x6y_1iy'),claims)

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

    def test_suoyin_layer_mismatch_and_unknown_layer_rejected(self):
        # Synthetic edits verify that a commentary cannot silently become body text.
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0].update(text_layer='witness_appended_suoyin_zan'))
        xml=self.root/'corpus/shiji/001.xml'
        xml.write_text(xml.read_text().replace('<p id="c-shiji-001-wudi:p001"','<p text-layer="witness_appended_suoyin_zan" id="c-shiji-001-wudi:p001"',1))
        self.assertEqual(v.validate(self.root),[])
        xml.write_text(xml.read_text().replace('text-layer="witness_appended_suoyin_zan"','text-layer="received_chapter"',1))
        self.assertTrue(any('文字層次不符' in e for e in v.validate(self.root)))
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0].update(text_layer='synthetic_unknown_layer'))
        self.assertTrue(any('文字層次無效' in e for e in v.validate(self.root)))

    def test_chu_note_layer_must_match_xml(self):
        # Synthetic attribution checks the layer boundary, not historical authorship.
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0].update(text_layer='witness_appended_chu_note'))
        xml=self.root/'corpus/shiji/001.xml'
        xml.write_text(xml.read_text().replace('<p id="c-shiji-001-wudi:p001"','<p text-layer="witness_appended_chu_note" id="c-shiji-001-wudi:p001"',1))
        self.assertEqual(v.validate(self.root),[])
        xml.write_text(xml.read_text().replace('text-layer="witness_appended_chu_note"','text-layer="received_chapter"',1))
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
        relations=[a for a in data['assertions'] if a['subject_person_id']=='ob7_g6i_7pp']
        people=json.loads((self.root/'registry/persons.json').read_text())['persons']
        bo=next(p['id'] for p in people if p['label']=='項伯')
        self.assertEqual({(a['predicate'],a['object_person_id']) for a in relations},{('paternal_uncle','5xt_rg8_7zs_A'),('paternal_uncle',bo)})
        self.assertEqual(relations[0]['qualifiers']['source_term'],'季父')
    def test_huaiwang_grandson_phrase_keeps_two_generations(self):
        chapter=json.loads((self.root/'corpus/shiji/007.json').read_text())
        p=chapter['paragraphs'][5]
        grandfather=p['text'].index('乃求楚懷王')+2
        grandson=p['text'].index('立以為楚懷王')+3
        mentions={m['start']:m for m in p['mentions']}
        self.assertEqual(mentions[grandfather]['person_id'],'c2w_s7g_en0')
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

    def test_equivalence_keeps_published_dangyang_mentions(self):
        c=json.loads((self.root/'corpus/shiji/007.json').read_text())
        old=[m for p in c['paragraphs'][:12] for m in p['mentions'] if m['surface']=='當陽君']
        self.assertTrue(old)
        self.assertEqual({m['person_id'] for m in old},{'1cd_mzr_sj4'})
        decision=json.loads((self.root/'corpus/shiji/007-equivalences.json').read_text())['decisions'][0]
        self.assertEqual(set(decision['person_ids']),{'1cd_mzr_sj4','zxd_afr_2xg'})
        self.assertEqual(decision['canonical_person_id'],'zxd_afr_2xg')
        self.assertEqual(v.validate(self.root),[])
    def test_equivalence_rejects_unrelated_quote(self):
        def mutate(d):d['decisions'][0]['evidence'][0]['quote']='故立布為九江王'
        self.change('corpus/shiji/007-equivalences.json',mutate)
        self.assertTrue(any('同指決定提及不在精確引句' in e for e in v.validate(self.root)))
    def test_equivalence_rejects_invalid_representative(self):
        self.change('corpus/shiji/007-equivalences.json',lambda d:d['decisions'][0].update(canonical_person_id='ao3_0fy_d45_AAA'))
        self.assertTrue(any('代表不在端點' in e for e in v.validate(self.root)))
    def test_equivalence_rejects_canonical_cycle(self):
        def mutate(d):
            other=json.loads(json.dumps(d['decisions'][0]));other['id']='synthetic-cycle';other['canonical_person_id']='1cd_mzr_sj4';d['decisions'].append(other)
        self.change('corpus/shiji/007-equivalences.json',mutate)
        self.assertTrue(any('同指決定代表循環' in e for e in v.validate(self.root)))
    def test_xiangyu_verb_ji_and_ritual_names_do_not_create_kin(self):
        c=json.loads((self.root/'corpus/shiji/007.json').read_text())
        p=c['paragraphs'][16];a=p['text'].index('籍吏民')
        self.assertFalse(any(m['kind']=='person' and m['start']==a for m in p['mentions']))
        claims=json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())['assertions']
        self.assertFalse(any(a['subject_person_id']=='ob7_g6i_7pp' and a['predicate'] in ('ancestor','father') for a in claims))
        self.assertFalse(any(a['object_person_id']=='ddb_l4j_4j2' for a in claims))
    def test_title_grant_is_separate_from_retrospective_attestation(self):
        holdings=json.loads((self.root/'corpus/shiji/007-titles.json').read_text())['holdings']
        h=next(h for h in holdings if h['title']=='赤泉侯')
        self.assertEqual(h['effective_period']['start']['evidence'][0]['paragraph_id'],'c-shiji-007-xiangyu:p042')
        self.assertTrue(any(a['paragraph_id']=='c-shiji-007-xiangyu:p041' and a['usage']=='retrospective' for a in h['attestations']))
        self.assertEqual(h['effective_period']['end']['status'],'unknown')
        lu=next(h for h in holdings if h['title']=='魯公')
        self.assertTrue(any(a['usage']=='posthumous_usage' for a in lu['attestations']))
        self.assertEqual(lu['effective_period']['end']['status'],'unknown')
    def test_title_period_rejects_unsourced_date(self):
        self.change('corpus/shiji/007-titles.json',lambda d:d['holdings'][0]['effective_period']['start'].update(date_expression='合成日期'))
        self.assertTrue(any('稱號日期表述不在端點證據' in e for e in v.validate(self.root)))
    def test_title_period_rejects_death_as_automatic_end(self):
        def mutate(d):
            h=d['holdings'][0];h['effective_period']['end']={'status':'source_event','event_type':'death','date_expression':None,'evidence':h['evidence']}
        self.change('corpus/shiji/007-titles.json',mutate)
        self.assertTrue(any('死亡或首次用稱不得自動替代起訖' in e for e in v.validate(self.root)))
    def test_title_occurrence_rejects_wrong_person(self):
        def mutate(d):d['holdings'][0]['attestations'][0]['person_mention_id']='c-shiji-007-xiangyu:m001-0000'
        self.change('corpus/shiji/007-titles.json',mutate)
        self.assertTrue(any('稱號用稱人物提及不符' in e for e in v.validate(self.root)))
    def test_sister_assertion_follows_subject_orientation(self):
        people=json.loads((self.root/'registry/persons.json').read_text())['persons']
        ids={p['label']:p['id'] for p in people}
        claims=json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())['assertions']
        a=next(a for a in claims if a['qualifiers']['source_term']=='兄')
        self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),(ids['呂后'],'sister',ids['周呂侯（呂后兄）']))

    def test_unknown_title_endpoint_cannot_hide_normalized_year(self):
        self.change('corpus/shiji/007-titles.json',lambda d:d['holdings'][0]['effective_period']['end'].update(year=207))
        self.assertTrue(any('不能暗補正規化日期' in e for e in v.validate(self.root)))

    def test_gaozu_hanxin_ambiguity_is_preserved(self):
        chapter=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=chapter['paragraphs'][29]
        bare=next(m for m in p['mentions'] if m['surface']=='韓信')
        self.assertIsNone(bare['person_id'])
        named=next(m for m in p['mentions'] if m['surface']=='韓太尉信')
        adviser=next(m for m in chapter['paragraphs'][26]['mentions'] if m['surface']=='韓信')
        self.assertNotEqual(named['person_id'],adviser['person_id'])
        case=chapter['annotation']['unresolved_identity_cases'][0]
        self.assertEqual(set(case['candidate_person_ids']),{named['person_id'],adviser['person_id']})

    def test_gaozu_conditional_and_impersonated_titles_are_unresolved(self):
        chapter=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=chapter['paragraphs'][21]
        mentions=[m for m in p['mentions'] if m['surface']=='秦王']
        self.assertTrue(all(m['person_id'] is not None for m in mentions[:-1]))
        self.assertIsNone(mentions[-1]['person_id'])
        p=chapter['paragraphs'][39]
        a=p['text'].index('詐為漢王')+2
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))
        self.assertTrue(any(m['kind']=='unresolved' and m['start']<=a<m['end'] for m in p['mentions']))

    def test_gaozu_qi_king_in_execution_is_tian_guang(self):
        c=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=c['paragraphs'][43]
        named=next(m for m in p['mentions'] if m['surface']=='田廣')
        a=p['text'].index('齊王烹')
        king=next(m for m in p['mentions'] if m['start']==a)
        han=next(m for m in p['mentions'] if m['surface']=='韓信')
        self.assertEqual(king['person_id'],named['person_id'])
        self.assertNotEqual(king['person_id'],han['person_id'])

    def test_gaozu_successor_emperor_and_nonpersonal_words(self):
        c=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=c['paragraphs'][87]
        successor=next(m for m in p['mentions'] if m['surface']=='孝惠帝')
        emperor=next(m for m in p['mentions'] if m['surface']=='皇帝')
        self.assertEqual(successor['person_id'],emperor['person_id'])
        for n,word in [(60,'通侯籍'),(73,'甚有信'),(88,'上尊號')]:
            p=c['paragraphs'][n-1];a=p['text'].index(word)
            pos=a+2 if n in (60,73) else a
            self.assertFalse(any(m['person_id'] and m['start']<=pos<m['end'] for m in p['mentions']))

    def test_gaozu_title_deposition_requires_explicit_evidence(self):
        h=json.loads((self.root/'corpus/shiji/008-titles.json').read_text())['holdings']
        ends=[x['effective_period']['end'] for x in h if x['effective_period']['end']['status']=='source_event']
        self.assertEqual(len(ends),3)
        self.assertTrue(all(x['event_type']=='deposition' and '廢' in x['evidence'][0]['quote'] for x in ends))
        father=next(x for x in h if x['title']=='太上皇')
        self.assertEqual(father['effective_period']['end']['status'],'unknown')

    def test_lvhou_titles_do_not_merge_mother_and_daughter(self):
        c=json.loads((self.root/'corpus/shiji/009.json').read_text())
        p=c['paragraphs'][0]
        mother=next(m for m in p['mentions'] if m['surface']=='呂太后')
        daughter=next(m for m in p['mentions'] if m['surface']=='魯元太后')
        self.assertNotEqual(mother['person_id'],daughter['person_id'])
        queen=next(m for m in c['paragraphs'][4]['mentions'] if m['surface']=='王太后')
        self.assertEqual(queen['person_id'],daughter['person_id'])

    def test_lvhou_zhao_king_changes_after_ruyi_death(self):
        c=json.loads((self.root/'corpus/shiji/009.json').read_text())
        p=c['paragraphs'][3]
        king=next(m for m in p['mentions'] if m['start']==p['text'].index('友為趙王')+2)
        friend=next(m for m in p['mentions'] if m['surface']=='友')
        previous=next(m for m in p['mentions'] if m['surface']=='趙王')
        self.assertEqual(king['person_id'],friend['person_id'])
        self.assertNotEqual(king['person_id'],previous['person_id'])

    def test_lvhou_bo_family_queen_is_not_empress_lv(self):
        c=json.loads((self.root/'corpus/shiji/009.json').read_text())
        p=c['paragraphs'][29];a=p['text'].index('太后家薄氏')
        queen=next(m for m in p['mentions'] if m['start']==a)
        bo=next(m for m in c['paragraphs'][2]['mentions'] if m['surface']=='薄夫人')
        lv=next(m for m in c['paragraphs'][0]['mentions'] if m['surface']=='呂太后')
        self.assertEqual(queen['person_id'],bo['person_id'])
        self.assertNotEqual(queen['person_id'],lv['person_id'])
        p=c['paragraphs'][21];a=p['text'].index('語在齊王語')+2
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))

    def test_cross_chapter_equivalence_requires_every_declared_chapter(self):
        self.change('corpus/shiji/010-equivalences.json',lambda d:d['decisions'][0]['evidence'].pop(0))
        self.assertTrue(any('同指決定缺少各篇證據' in e for e in v.validate(self.root)))

    def test_cross_chapter_equivalence_cannot_hide_as_single_chapter(self):
        self.change('corpus/shiji/010-equivalences.json',lambda d:d['decisions'][0].update(scope='same_chapter'))
        self.assertTrue(any('同指決定範圍與篇數不符' in e for e in v.validate(self.root)))

    def test_wendi_successor_and_other_word_are_separate(self):
        c=json.loads((self.root/'corpus/shiji/010.json').read_text())
        previous=next(m for m in c['paragraphs'][37]['mentions'] if m['surface']=='孝文皇帝')
        successor=next(m for m in c['paragraphs'][38]['mentions'] if m['surface']=='皇帝')
        self.assertNotEqual(previous['person_id'],successor['person_id'])
        p=c['paragraphs'][36];a=p['text'].index('佗不在令中')
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))
        p=c['paragraphs'][29];a=p['text'].index('古者天子')+2
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))

    def test_jingdi_same_given_name_sheng_stays_separate(self):
        c=json.loads((self.root/'corpus/shiji/011.json').read_text())
        son=next(m for m in c['paragraphs'][3]['mentions'] if m['surface']=='子勝')
        uncle=next(m for m in c['paragraphs'][16]['mentions'] if m['surface']=='弟勝')
        self.assertNotEqual(son['person_id'],uncle['person_id'])

    def test_jingdi_king_mother_is_not_king(self):
        c=json.loads((self.root/'corpus/shiji/011.json').read_text())
        p=c['paragraphs'][7]
        mother=next(m for m in p['mentions'] if m['surface']=='膠東王太后')
        son=next(m for m in p['mentions'] if m['surface']=='膠東王')
        self.assertNotEqual(mother['person_id'],son['person_id'])
        titles=json.loads((self.root/'corpus/shiji/011-titles.json').read_text())['holdings']
        queen=next(h for h in titles if h['title']=='皇后')
        self.assertEqual(queen['person_id'],mother['person_id'])


    def test_adjacent_relation_requires_explicit_context(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            del a['context']
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('端點未見' in e for e in v.validate(self.root)))

    def test_adjacent_relation_rejects_reversed_evidence(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            a['evidence'].reverse()
            a['context']['paragraph_ids'].reverse()
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('相鄰兩段' in e for e in v.validate(self.root)))

    def test_adjacent_relation_requires_endpoint_in_quote(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            a['evidence'][0]['quote']='好儒學'
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('未見於引句' in e for e in v.validate(self.root)))

    def test_adjacent_relation_context_must_match_evidence(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            a['context']['paragraph_ids'][1]=a['context']['paragraph_ids'][0]
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('相鄰兩段' in e for e in v.validate(self.root)))


    def test_title_antecedent_rejects_wrong_holder_anchor(self):
        def mutate(d):
            h=next(h for h in d['holdings'] if h['title']=='膠西王')
            e=next(e for e in h['evidence'] if 'context' in e)
            e['context']['person_mention_id']='c-shiji-059-wuzong:m001-0000'
        self.change('corpus/shiji/059-titles.json',mutate)
        self.assertTrue(any('前段錨點或引句無效' in e for e in v.validate(self.root)))

    def test_title_antecedent_rejects_nonadjacent_paragraph(self):
        def mutate(d):
            h=next(h for h in d['holdings'] if h['title']=='膠西王')
            e=next(e for e in h['evidence'] if 'context' in e)
            e['context']['paragraph_id']='c-shiji-059-wuzong:p013'
        self.change('corpus/shiji/059-titles.json',mutate)
        self.assertTrue(any('前段錨點或引句無效' in e for e in v.validate(self.root)))

    def test_kinship_default_must_match_recorded_alternative(self):
        def mutate(d):
            d['annotation']['kinship_interpretation_cases'][0]['default_alternative_id'] = 'invented'
        self.change('corpus/shiji/100.json', mutate)
        self.assertTrue(any('親屬預設選項' in error for error in v.validate(self.root)))

    def test_migration_snapshot_allows_later_canonical_people(self):
        self.change('registry/person-id-migrations.json', lambda d: d.update(person_count=d['person_count'] - 1))
        self.assertEqual(v.validate(self.root), [])

    def test_migration_snapshot_rejects_impossible_count(self):
        self.change('registry/person-id-migrations.json', lambda d: d.update(person_count=10**9))
        self.assertTrue(any('全面遷移範圍' in e for e in v.validate(self.root)))

    def test_title_numeric_year_rejects_bce_numbering_error(self):
        def mutate(d):
            h = next(h for h in d['holdings'] if h['title'] == '太常')
            h['effective_period']['start']['normalized_date']['year'] = -154
        self.change('corpus/shiji/101-titles.json', mutate)
        self.assertTrue(any('天文年' in e for e in v.validate(self.root)))

    def test_title_numeric_year_must_anchor_its_own_event(self):
        def mutate(d):
            h = next(h for h in d['holdings'] if h['title'] == '太常')
            date = h['effective_period']['start']['normalized_date']
            date['original_quote'] = '三年正月乙巳'
        self.change('corpus/shiji/101-titles.json', mutate)
        self.assertTrue(any('本筆事件證據' in e for e in v.validate(self.root)))

    def test_posthumous_huainan_title_of_son_is_not_the_father(self):
        d = json.loads((self.root/'corpus/shiji/010.json').read_text())
        m = next(m for p in d['paragraphs'] for m in p['mentions'] if m['id'] == 'c-shiji-010-wendi:m023-0149')
        self.assertEqual(m['surface'], '淮南王')
        self.assertEqual(m['kind'], 'unresolved')
        self.assertIsNone(m['person_id'])
        reg = json.loads((self.root/'registry/persons.json').read_text())
        father = next(p for p in reg['persons'] if p['id'] == 'yqp_nlb_p1p_AF')
        self.assertNotIn(m['id'], {e['mention_id'] for e in father['evidence']})

    def test_appended_zhengyi_layer_requires_matching_xml(self):
        def mutate(d):
            d['paragraphs'][-1]['text_layer'] = 'witness_appended_zhengyi_note'
        self.change('corpus/shiji/103.json', mutate)
        self.assertTrue(any('XML 文字層次不符' in e for e in v.validate(self.root)))
        from scripts.render_corpus import render
        chapter = json.loads((self.root/'corpus/shiji/103.json').read_text())
        (self.root/'corpus/shiji/103.xml').write_text(render(chapter))
        self.assertEqual(v.validate(self.root), [])

    def test_ancestral_origin_cannot_invent_named_ancestor(self):
        def mutate(d):
            a = next(a for a in d['assertions'] if a['relation'] == 'ancestral_origin')
            a['qualifiers']['ancestor_person_id'] = a['person_id']
        self.change('corpus/shiji/103-addresses.json', mutate)
        self.assertTrue(any('祖先出身不得暗補' in error for error in v.validate(self.root)))


    def test_daughter_birth_order_scope_preserves_unknown_ordinal(self):
        d=json.loads((self.root/'corpus/shiji/105-assertions.json').read_text())
        order=d['assertions'][0]['qualifiers']['birth_order']
        self.assertEqual(order['scope'],'daughters_of_parent')
        self.assertIsNone(order['ordinal'])
        self.assertEqual(order['position'],'younger_or_youngest')
        self.assertEqual(v.validate(self.root),[])
        def mutate(d):
            d['assertions'][0]['qualifiers']['birth_order']['scope']='unknown_sequence'
        self.change('corpus/shiji/105-assertions.json',mutate)
        self.assertTrue(any('排行序列範圍未知' in e for e in v.validate(self.root)))

if __name__=='__main__':unittest.main()
