# coding: utf-8
"""跨史家族整合的來源路徑、同人及衝突資訊保全。"""
import json
import unittest
from pathlib import Path
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies
ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT / name).read_text())

class ParallelAristocraticFamilies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people = {p['id']: p for p in read('registry/persons.json')['persons']}
        _, cls.assembled = load_assemblies(ROOT, load_catalog(ROOT))
    def test_cross_history_parent_paths_are_traced_from_evidence(self):
        for start, expected in [
            ('a8f_ec8_e74_AAAAABA', ['王綏','王愉','王坦之','王述','王承','王湛','王昶','王澤']),
            ('2r1_zso_fl1_DAA', ['謝靈運','謝瑍','謝玄','謝奕']),
            ('a11_d36_c74_DBA', ['庾登之','庾廓（宋書原稱）','庾蘊','庾冰'])]:
            names=[];seen=set();pid=start
            while pid:
                self.assertNotIn(pid, seen);seen.add(pid)
                names.append(self.people[pid]['label']);row=self.assembled[pid]
                if row.get('parent_person_id'):
                    self.assertTrue(row.get('source_assertion_id') or row.get('parent_connection'))
                pid=row.get('parent_person_id')
            self.assertEqual(names, expected)
    def test_simultaneous_rekey_keeps_three_distinct_wang_sons(self):
        self.assertEqual([self.people['a8f_ec8_e74_'+tail]['label'] for tail in ['AAAAAB','AAAAAC','AAAAAD']], ['王愉','王國寶','王忱'])
        self.assertEqual(len({self.people['a8f_ec8_e74_'+tail]['id'] for tail in ['AAAAAB','AAAAAC','AAAAAD']}),3)
    def test_conflicting_reported_ordinals_remain_numeric_without_preference(self):
        c=read('corpus/jinshu/042-taiyuan-wang.json')['annotation']['birth_order_conflicts'][0]
        rows={a['id']:a for a in read('corpus/jinshu/042-taiyuan-wang-assertions.json')['assertions']}
        self.assertIsNone(c['preferred_assertion_id']);self.assertIsNone(c['preferred_ordinal'])
        self.assertEqual({v['ordinal'] for v in c['candidates']},{1,2})
        for v in c['candidates']:
            a=rows[v['assertion_id']]
            self.assertEqual(a['qualifiers']['reported_birth_order']['ordinal'],v['ordinal'])
            self.assertEqual(a['evidence'],v['evidence'])
            self.assertFalse(a['qualifiers']['reported_birth_order']['selected_for_default_order'])
    def test_cross_packet_identifications_are_one_identity_with_all_passages(self):
        ds=read('corpus/jinshu/079-parallel-family-identities.json')['decisions']
        self.assertEqual(len(ds),3)
        for label,pid in [('庾冰','a11_d36_c74'),('王戎','48e_04a_3d8'),('郗超','57b_1cb_a1b')]:
            self.assertEqual([p['id'] for p in self.people.values() if p['label']==label],[pid])
            d=next(d for d in ds if d['person_id']==pid)
            self.assertGreaterEqual(len(d['chapter_ids']),2)
            self.assertEqual(set(d['chapter_ids']),{e['chapter_id'] for e in d['evidence']})
    def test_replaced_public_ids_do_not_survive_as_people_or_aliases(self):
        for pid in ['jiu_zvj_hbl','jiu_zvj_hbl_A','buj_vep_6oq','rcx_di4_v37','e3f_d0s_c13','r3n_se4_89p','ff4_gpn_jji']:
            self.assertNotIn(pid,self.people)
            self.assertFalse((ROOT / 'exports/persons' / (pid+'.json')).exists())
            self.assertFalse(any(pid in p.get('id_aliases',[]) for p in self.people.values()))

    def test_east_sea_prince_yue_has_one_identity_across_received_passages(self):
        pid = '9o2_vhv_r7y'
        self.assertNotIn('169_279_d9c', self.people)
        decision = read('corpus/jinshu/075-simayue-identities.json')['decisions'][0]
        self.assertEqual(decision['person_id'], pid)
        self.assertEqual(set(decision['chapter_ids']), {
            'c-songshu-060-xunbozi', 'c-jinshu-065-wangdao-family',
            'c-jinshu-075-taiyuan-wang'})
        for path in ['songshu/060', 'jinshu/065', 'jinshu/075-taiyuan-wang']:
            chapter = read('corpus/' + path + '.json')
            mentions = [m for p in chapter['paragraphs'] for m in p['mentions']
                        if m.get('surface') == '東海王越']
            self.assertTrue(mentions)
            self.assertTrue(all(m.get('person_id') == pid for m in mentions))
        self.assertFalse(any('169_279_d9c' in p.get('id_aliases', [])
                             for p in self.people.values()))
