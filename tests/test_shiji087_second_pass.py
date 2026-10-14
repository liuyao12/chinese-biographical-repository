import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LisiEvidenceTests(unittest.TestCase):
    def read(self, suffix, key):
        return json.loads((ROOT / ('corpus/shiji/087-' + suffix + '.json')).read_text())[key]

    def test_mengyi_identity_preserves_conflicting_narratives(self):
        decision = next(d for d in self.read('equivalences', 'decisions') if d['id'] == 'eq-shiji087-mengyi')
        self.assertEqual(decision['person_ids'], ['dxo_6ig_5eg'])
        self.assertTrue(decision['identity_materialized'])
        self.assertFalse(decision['human_reviewed'])
        quotes = {e['paragraph_id']: e['quote'] for e in decision['evidence']}
        self.assertIn('且蒙恬已死，蒙毅將兵居外', quotes['c-shiji-087-lisi:p019'])
        self.assertIn('遂殺之', quotes['c-shiji-088-mengtian:p009'])
        self.assertIn('乃吞藥自殺', quotes['c-shiji-088-mengtian:p010'])
        event = next(e for e in self.read('life-events', 'events') if e['person_id'] == 'dxo_6ig_5eg')
        self.assertIn('殺大臣蒙毅等', event['source_term'])
        self.assertNotIn('normalized_date', event)
        self.assertIn('死亡次序', decision['rationale'])

    def test_late_actors_keep_event_and_kinship_limits(self):
        ds = {d['id']: d for d in self.read('equivalences', 'decisions')}
        pei = ds['eq-shiji087-late-pei']
        quotes = [e['quote'] for e in pei['evidence']]
        self.assertTrue(any('子嬰立三月' in q for q in quotes))
        self.assertTrue(any('子嬰為秦王四十六日' in q for q in quotes))
        self.assertTrue(any('以秦王屬吏' in q for q in quotes))
        wang = ds['eq-shiji087-late-wangli']
        self.assertEqual(wang['canonical_person_id'], 'gdj_k53_v1x_*A')
        self.assertTrue(any('王翦之孫王離' in e['quote'] for e in wang['evidence']))
        self.assertIn('不由被俘補死亡', wang['rationale'])
        zhang = ds['eq-shiji087-late-zhang']
        self.assertTrue(any('矯王令以誅吳叔' in e['quote'] for e in zhang['evidence']))
        self.assertIn('不把「破逐廣等兵」讀成章邯親手殺吳廣', zhang['rationale'])

    def test_shen_han_are_individuals_and_separator_stays_text(self):
        chapter = json.loads((ROOT / 'corpus/shiji/087.json').read_text())
        for end, start in [('p023', 67), ('p025', 228), ('p025', 387)]:
            p = next(p for p in chapter['paragraphs'] if p['id'].endswith(':' + end))
            self.assertEqual(p['text'][start:start + 3], '申、韓')
            ms = [m for m in p['mentions'] if start <= m['start'] < start + 3]
            self.assertEqual([(m['surface'], m['person_id']) for m in ms], [('申', 'vtn_thh_540'), ('韓', 'n2o_l90_fnm')])
            self.assertEqual([(m['start'], m['end']) for m in ms], [(start, start + 1), (start + 2, start + 3)])
        han = next(d for d in self.read('equivalences', 'decisions') if d['id'] == 'eq-shiji087-school-han')
        self.assertIn('引述不等於親聞口授', han['rationale'])
        self.assertFalse(han['human_reviewed'])

    def test_accession_is_not_the_following_regnal_year_or_burial_month(self):
        titles = {h['id']: h for h in self.read('titles', 'holdings')}
        hu = titles['th-shiji087-020']
        self.assertEqual(hu['mode'], 'accession')
        self.assertEqual(hu['kind'], 'imperial_rank')
        date = hu['effective_period']['start']['normalized_date']
        self.assertEqual(date['era_year'], 210)
        self.assertEqual(date['year'], -209)
        self.assertNotIn('month', date)
        self.assertIn('子胡亥立，為二世皇帝', date['basis']['reference_event_quote'])
        self.assertNotIn('normalized_date', titles['th-shiji087-018']['effective_period']['start'])
        self.assertEqual(titles['th-shiji087-010']['effective_period']['start']['normalized_date']['era_year'], 221)
        death = next(e for e in self.read('life-events', 'events') if e['id'] == 'le-shiji087-010')
        self.assertEqual(death['normalized_date']['era_year'], 207)
        self.assertEqual(hu['effective_period']['end']['status'], 'unknown')
        self.assertIn('不能據該格把所有後續事件一律定', death['normalized_date']['rationale'])

    def test_qin_king_scopes_distinguish_departure_from_successor(self):
        chapter = json.loads((ROOT / 'corpus/shiji/087.json').read_text())
        paragraphs = {p['id'].rsplit(':', 1)[1]: p for p in chapter['paragraphs']}
        for m in paragraphs['p002']['mentions']:
            if m['surface'] == '秦王':
                self.assertEqual(m['person_id'], 'jik_qff_1cj')
        for key in ['p003', 'p004', 'p009']:
            for m in paragraphs[key]['mentions']:
                if m['surface'] == '秦王':
                    self.assertEqual(m['person_id'], 'ao3_0fy_d45_AAA')
        self.assertTrue(any(m.get('person_id') == 'ao3_0fy_d45_AA' for m in paragraphs['p003']['mentions']))

    def test_custody_and_requested_burial_do_not_become_death(self):
        events = self.read('life-events', 'events')
        self.assertFalse(any(e['person_id'] == 'yad_hp5_rax' and e['evidence'][0]['paragraph_id'].endswith(':p017') for e in events))
        self.assertFalse(any(e['person_id'] == '172_ij7_8yf' for e in events))
        child = next(e for e in events if e['person_id'] == '49g_7az_e4i_B')
        self.assertNotIn('normalized_date', child)
        self.assertIn('夷三族', child['source_term'])
        self.assertNotIn('腰斬', child['source_term'])

    def test_death_year_preserves_source_month_and_precision(self):
        events = self.read('life-events', 'events')
        for pid, year, phrase in [('49g_7az_e4i', 208, '二世二年七月'), ('ao3_0fy_d45_AAA', 210, '其年七月')]:
            event = next(e for e in events if e['person_id'] == pid)
            self.assertEqual(event['date_expression'], phrase)
            date = event['normalized_date']
            self.assertEqual(date['era_year'], year)
            self.assertEqual(date['year'], 1 - year)
            self.assertEqual(date['precision'], 'year')
            self.assertFalse(date['human_reviewed'])
            self.assertNotIn('month', date)

    def test_origin_service_and_quoted_legend_keep_distinct_roles(self):
        addresses = self.read('addresses', 'assertions')
        own = [a for a in addresses if a['person_id'] == '49g_7az_e4i']
        self.assertEqual({(a['relation'], a['place']['source_name']) for a in own}, {('biographical_origin', '楚上蔡'), ('death_place', '咸陽市')})
        self.assertFalse(any(a['person_id'] == '172_ij7_8yf' and a['relation'] == 'burial_place' for a in addresses))
        legend = next(a for a in addresses if a['person_id'] == 'z9y_ry1_zee')
        self.assertIn('二世引韓子', legend['interpretation_note'])
        self.assertIsNone(legend['place']['modern_identification'])

    def test_four_qin_rulers_remain_distinct_in_allusion(self):
        ch = json.loads((ROOT / 'corpus/shiji/087.json').read_text())
        p = next(p for p in ch['paragraphs'] if p['id'].endswith(':p005'))
        rulers = {m['person_id'] for m in p['mentions'] if m['surface'] in ['繆公', '孝公', '惠王', '昭王']}
        self.assertEqual(len(rulers), 4)
        self.assertIn('ao3_0fy_d45', rulers)
        shang = [m for p in ch['paragraphs'] for m in p['mentions'] if m['surface'] in ['商鞅', '商君']]
        self.assertTrue(shang)
        self.assertTrue(all(m['person_id'] == '2wp_usr_ncd' for m in shang))
        # 群稱四君不另造人物，也不按王稱批次接到當時的始皇。
        self.assertTrue(all(m.get('person_id') is None for m in p['mentions'] if m['surface'] == '四君'))
        self.assertNotIn('ao3_0fy_d45_AAA', rulers)

    def test_huayang_peer_is_not_the_queen(self):
        ch = json.loads((ROOT / 'corpus/shiji/087.json').read_text())
        p = next(p for p in ch['paragraphs'] if p['id'].endswith(':p005'))
        m = next(m for m in p['mentions'] if m['surface'] == '華陽')
        self.assertEqual(m['person_id'], '4tv_nhj_oxt')
        source = json.loads((ROOT / 'corpus/shiji/072.json').read_text())
        p = next(p for p in source['paragraphs'] if p['id'].endswith(':p002'))
        self.assertIn('同父弟曰羋戎，為華陽君', p['text'])
        self.assertTrue(any(m['surface'] == '羋戎' and m['person_id'] == '4tv_nhj_oxt' for m in p['mentions']))
