import copy
import hashlib
import json
import unittest
from pathlib import Path
from scripts.title_successions import succession_valid
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def chapter():return read('corpus/hanshu/041.json')
def para(key):return next(p for p in chapter()['paragraphs'] if p['id'].endswith(':p-'+key))
def ids(key,term):return {m['person_id'] for m in para(key)['mentions'] if m['surface']==term}
class HanshuFuJinTests(unittest.TestCase):
    def test_eight_new_paragraphs_preserve_zhou_ids_and_original_text(self):
        c=chapter();self.assertEqual(len(c['paragraphs']),11)
        z=[p for p in c['paragraphs'] if ':p-zhou-' in p['id']]
        self.assertEqual(hashlib.sha256('\n\n'.join(p['text'] for p in z).encode()).hexdigest(),'44191b56613a6486f0b5b3f39dbf6f27bf2233ab8908d10a94bc4690019338c8')
        self.assertEqual(c['source']['revision_id'],2342290)
        self.assertEqual(c['source']['text_scope'],'partial_chapter')
        self.assertFalse(c['source']['image_verified'])
        self.assertFalse(next(b for b in read('corpus/progress.json')['books'] if b['book_id']=='b-hanshu-041')['complete'])
    def test_two_han_xins_are_separated_by_chen_and_pingcheng(self):
        self.assertEqual(ids('fu-002','淮陰'),{'ofc_8ei_jb7'})
        self.assertEqual(ids('jin-003','楚王信'),{'ofc_8ei_jb7'})
        self.assertEqual(ids('jin-004','韓信'),{'l9e_fbr_36a_*A'})
    def test_zhao_state_is_not_a_surname_in_the_chaoge_passage(self):
        self.assertEqual(ids('fu-001','趙賁'),{'bwv_p3h_q1j'})
        self.assertEqual(ids('jin-003','賁'),{'phx_lyu_9ym'})
        p=para('jin-003');at=p['text'].index('趙賁')
        self.assertFalse(any(m['start']<=at<m['end'] for m in p['mentions']))
        d=next(d for d in read('corpus/hanshu/041-identities.json')['decisions'] if d['id'].startswith('d-hanshu041-fujin-') and d['person_id']=='phx_lyu_9ym')
        image=next(r for r in d['references'] if r.get('image_verified'))
        self.assertEqual(image['pdf_page'],42);self.assertEqual(len(image['witness_sha256']),64)
        self.assertEqual(image['verification_scope'],'specified_quote_only_in_parallel_witness')
    def test_office_holders_follow_syntax_not_the_nearest_name(self):
        p=para('fu-003');chancellors=[m['person_id'] for m in p['mentions'] if m['surface']=='丞相']
        self.assertEqual(chancellors,['b1r_inb_fts','w8j_vnd_rs4'])
        self.assertEqual(ids('fu-002','相國'),{'37j_16p_7n8'})
        self.assertEqual(ids('jin-004','丞相'),{'h6b_bxc_9d4'})
    def test_great_grandson_does_not_invent_intermediate_hanshu_fathers(self):
        aa=read('corpus/hanshu/041-assertions.json')['assertions']
        a=next(a for a in aa if a['id']=='a-hanshu041-fu-001')
        self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('w8j_vnd_rs4_AAA','great_grandfather','w8j_vnd_rs4'))
        self.assertFalse(any(a['subject_person_id']=='w8j_vnd_rs4_AAA' and a['predicate']=='father' for a in aa))
    def test_deaths_keep_their_own_years_and_unknown_execution_year(self):
        ee={e['id']:e for e in read('corpus/hanshu/041-life-events.json')['events']}
        for key,years in [('le-hanshu041-fu-001',(191,190)),('le-hanshu041-jin-001',(184,183))]:
            r=ee[key]['normalized_date_range'];self.assertEqual((r['earliest']['era_year'],r['latest']['era_year']),years)
        e=ee['le-hanshu041-fu-002'];self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date_range',e)
        self.assertEqual(e['source_term'],'誅')
    def test_military_starting_places_are_not_native_places(self):
        aa=read('corpus/hanshu/041-addresses.json')['assertions']
        for pid,place in [('w8j_vnd_rs4','橫陽'),('7dv_lqp_y4z','宛朐')]:
            a=next(a for a in aa if a['person_id']==pid)
            self.assertEqual(a['relation'],'service_location');self.assertEqual(a['place']['source_name'],place)
            self.assertIn(a['qualifiers']['source_position'],a['source_term'])
            self.assertIsNone(a['place']['modern_identification'])
    def test_source_variants_are_preserved_without_silent_correction(self):
        self.assertIn('觞、郯',para('jin-003')['text']);self.assertIn('至五石',para('jin-004')['text'])
        vv=chapter()['annotation']['reported_variants']
        for received,reported in [('觞','鄫'),('五石','五百石')]:
            v=next(v for v in vv if v['received_reading']==received)
            self.assertEqual(v['reported_reading'],reported);self.assertFalse(v['adopted']);self.assertFalse(v['image_verified'])
    def test_posthumous_names_do_not_borrow_the_death_year_as_naming_year(self):
        hh=read('corpus/hanshu/041-titles.json')['holdings']
        for title in ['景侯','肅侯']:
            h=next(h for h in hh if h['id'].startswith(('th-hanshu041-fu-','th-hanshu041-jin-')) and h['title']==title)
            self.assertEqual(h['mode'],'posthumous_naming');self.assertIsNone(h['effective_period']['start']['date_expression'])
        self.assertFalse(any(h['person_id']=='7dv_lqp_y4z_A' and h['id'].startswith('th-hanshu041-jin-') for h in hh))
        for h in read('corpus/shiji/098-titles.json')['holdings']:
            if h['title'] in ['景侯','肅侯']:
                self.assertEqual(h['mode'],'posthumous_naming');self.assertIsNone(h['effective_period']['start']['date_expression'])
    def test_successions_link_real_parent_titles_and_reject_false_office_or_parent(self):
        aa=read('corpus/hanshu/041-assertions.json')['assertions'];hh={h['id']:h for h in read('corpus/hanshu/041-titles.json')['holdings']}
        pp={p['id']:(chapter()['id'],p) for p in chapter()['paragraphs']}
        claims=[a for a in aa if 'succession' in a.get('qualifiers',{})];self.assertEqual(len(claims),3)
        for a in claims:self.assertTrue(succession_valid(a,hh,pp))
        a=next(a for a in claims if a['id']=='a-hanshu041-jin-001')
        for change in ['office','father','no_succession','extra_date','outside_quote']:
            bad=copy.deepcopy(a);s=bad['qualifiers']['succession']
            if change=='office':s['predecessor_holding_id']='th-hanshu041-jin-004'
            elif change=='father':s['predecessor_person_id']='w8j_vnd_rs4'
            elif change=='no_succession':s['source_term']='子亭'
            elif change=='extra_date':s['normalized_date']={'year':-183}
            else:bad['evidence'][0]['quote']='子亭嗣'
            self.assertFalse(succession_valid(bad,hh,pp),change)
    def test_known_person_name_components_remain_source_bound(self):
        for pid,title,surname,ming in [('7dv_lqp_y4z_A','信武侯','靳','亭'),('w8j_vnd_rs4_AAA','陽陵侯','傅','偃')]:
            p=read('data/corpus/profiles/'+pid+'.json');self.assertEqual(len(p['name_components']),1)
            n=p['name_components'][0];self.assertEqual((n['title'],n['surname'],n['ming']),(title,surname,ming))
            self.assertEqual(n['chapter_id'],chapter()['id']);self.assertNotIn('ancestors',p)
