import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text())

def para(number):
    return read('corpus/shiji/098.json')['paragraphs'][number - 1]

def ids(number, surface):
    return {m['person_id'] for m in para(number)['mentions']
            if m['kind'] == 'person' and m['surface'] == surface}

class FuJinCoreIdentityTests(unittest.TestCase):
    def test_two_hanxins_follow_different_campaigns(self):
        for n, surface in [(2, '淮陰'), (7, '楚王信'), (10, '淮陰侯')]:
            self.assertEqual(ids(n, surface), {'ofc_8ei_jb7'})
        self.assertEqual(ids(8, '韓信'), {'l9e_fbr_36a_*A'})
        self.assertIn('取楚王信', para(7)['text'])
        self.assertIn('攻韓信平城下', para(8)['text'])
        b = read('exports/persons/ofc_8ei_jb7.json')
        self.assertNotIn('l9e_fbr_36a_*A', b['person_ids'])

    def test_short_names_and_titles_resolve_without_adding_surnames_to_text(self):
        for n, surface, pid in [(2, '參', '37j_16p_7n8'),
                                (3, '勃', 'koy_6jg_gcc'),
                                (3, '哙', 'b1r_inb_fts')]:
            self.assertEqual(ids(n, surface), {pid})
        self.assertIn('以相國代丞相哙擊豨', para(3)['text'])
        self.assertEqual(ids(3, '相國'), {'w8j_vnd_rs4'})
        holdings = read('corpus/shiji/098-titles.json')['holdings']
        self.assertEqual(next(h for h in holdings if h['id']=='th-shiji098-016')['person_id'], 'b1r_inb_fts')
        self.assertEqual(next(h for h in holdings if h['id']=='th-shiji098-018')['person_id'], 'w8j_vnd_rs4')

    def test_same_noble_title_does_not_merge_different_subjects(self):
        self.assertEqual(ids(7, '信武侯'), {'7dv_lqp_y4z'})
        self.assertEqual(ids(10, '信武侯'), {'fvm_66f_0k3'})
        self.assertEqual(ids(12, '昌'), {'fvm_66f_0k3_A'})
        self.assertIn('三十一年', para(4)['text'])

    def test_equivalence_evidence_is_queryable_in_each_person_bundle(self):
        eq = [d for d in read('corpus/shiji/098-equivalences.json')['decisions']
              if d['id'].startswith('eq-shiji098-core-')]
        self.assertEqual(len(eq), 10)
        for decision in eq:
            self.assertTrue(decision['identity_materialized'])
            b = read('exports/persons/'+decision['canonical_person_id']+'.json')
            actual = next(x for x in b['equivalence_decisions'] if x['id']==decision['id'])
            self.assertTrue(any(e['chapter_id']=='c-shiji-098-fujin' for e in actual['evidence']))
            self.assertTrue(all(e['mention_ids'] for e in actual['evidence']))
        self.assertFalse(next(b for b in read('corpus/progress.json')['books'] if b['book_id']=='b-shiji-098')['complete'])

    def test_eleven_retired_ids_have_no_registry_or_public_files(self):
        registered = {p['id'] for p in read('registry/persons.json')['persons']}
        for old in ['nrp_vv5_hry','5k8_ms4_y3k','mfd_hor_95c','hjx_5rx_wzu',
                    'ebz_s7c_pds','1tz_1iv_r3r','rdw_qwe_aa0','och_1lh_hgs',
                    'rzl_t6n_y63','jki_ijf_2w1','rke_c0u_y8f']:
            self.assertNotIn(old, registered)
            self.assertFalse((ROOT / ('exports/persons/'+old+'.json')).exists())
            self.assertFalse((ROOT / ('data/corpus/profiles/'+old+'.json')).exists())

class FuJinTableKinshipTests(unittest.TestCase):
    def test_jiangling_names_reconcile_but_jingdi_king_stays_separate(self):
        self.assertEqual(ids(7, '江陵王'), {'bwv_ob8_6xi_A'})
        for number, surface, paragraph in [('008','臨江王驩',55),('051','臨江王共尉',3),('093','共尉',9)]:
            p=read('corpus/shiji/'+number+'.json')['paragraphs'][paragraph-1]
            self.assertTrue(any(m['surface']==surface and m['person_id']=='bwv_ob8_6xi_A' for m in p['mentions']))
        p=read('corpus/shiji/122.json')['paragraphs'][6]
        self.assertTrue(any(m['surface']=='臨江王' and m['person_id']=='3sg_5re_qc2' for m in p['mentions']))

    def test_generals_reconcile_without_merging_same_name_fragments(self):
        for n,s,pid in [(1,'龍且','sr6_5zr_1f3'),(7,'項悍','xtl_sr1_di0'),(8,'敞','h6b_bxc_9d4')]:
            self.assertEqual(ids(n,s),{pid})
        b=read('exports/persons/h6b_bxc_9d4.json')
        self.assertNotIn('0sz_508_6cb',b['person_ids'])
        eq=next(d for d in b['equivalence_decisions'] if d['id']=='eq-shiji098-followup-houchang')
        self.assertEqual(eq['references'][0]['quote'],'小顏云侯敞。')
        self.assertFalse(eq['references'][0]['image_verified'])

    def test_table_parent_is_parseable_and_not_a_fabricated_prose_passage(self):
        b=read('exports/persons/bwv_ob8_6xi_A.json')
        a=next(a for a in b['preferred_relations'] if a['id']=='a-shiji016-linjiang-father')
        self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('bwv_ob8_6xi_A','father','bwv_ob8_6xi'))
        e=a['evidence'][0]
        self.assertEqual((e['kind'],e['table_cell_id'],e['quote']),('table_cell','shiji-016-t2-r033-c04','臨江王驩。始，敖子。'))
        self.assertNotIn('paragraph_id',e)
        self.assertEqual(b['assembled_identity']['parent_person_id'],'bwv_ob8_6xi')
        self.assertTrue(any(p['id']==e['table_cell_id'] and p['text']==e['quote'] for p in b['table_passages']))
        self.assertFalse(any(p['id']==e['table_cell_id'] for p in b['passages']))
        self.assertTrue(any(s['source_id']==e['source_id'] and s['book_id']=='b-shiji-016' for s in b['sources']))
        parent=read('exports/persons/bwv_ob8_6xi.json')
        self.assertTrue(any(a['id']=='a-shiji016-linjiang-father' for a in parent['relations']))

    def test_existing_ten_tables_have_registered_work_book_chapter_ids(self):
        work=next(w for w in read('registry/works.json')['works'] if w['id']=='w-shiji')
        books={b['id']:b for b in work['books']}
        index=read('data/historical-tables/index.json')['tables']
        self.assertEqual(len(index),10)
        for item in index:
            source=read(item['path'])['source']
            self.assertEqual(books[source['book_id']]['work_id'],source['work_id'])
            self.assertIn(source['chapter_id'],books[source['book_id']]['chapter_ids'])

    def test_seven_superseded_ids_have_no_public_alias_files(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        for old in ['can_0qj_fka','8e4_llb_ya6','fxc_ppb_ofs','4rt_vz6_obh','ex1_pps_iby','xea_8m8_6dh','stm_voa_t08']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT / ('exports/persons/'+old+'.json')).exists())
            self.assertFalse((ROOT / ('data/corpus/profiles/'+old+'.json')).exists())
