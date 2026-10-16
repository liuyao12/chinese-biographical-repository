import copy
import json
import unittest
from pathlib import Path
from scripts.historical_tables import validate_identity_evidence

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
def han():return read('corpus/hanshu/041.json')
def ids(n,term):return {m['person_id'] for m in han()['paragraphs'][n-1]['mentions'] if m['surface']==term}
def bundle(pid):return read('exports/persons/'+pid+'.json')
ROOT_ID='fvm_66f_0k3'
YING=ROOT_ID+'_C'
JU=ROOT_ID+'_CA'

class HanshuZhouCrossReadingTests(unittest.TestCase):
    def test_partial_received_text_keeps_actual_digital_characters(self):
        c=han()
        self.assertEqual(len(c['paragraphs']),3)
        self.assertTrue(c['paragraphs'][0]['text'].startswith('周惞，沛人也。'))
        self.assertIn('更封惞為糨城侯',c['paragraphs'][2]['text'])
        self.assertNotIn('䣙城侯',c['paragraphs'][2]['text'])
        self.assertEqual(c['source']['revision_id'],2342290)
        self.assertEqual(c['source']['text_scope'],'partial_chapter')
        self.assertEqual(c['source']['review_status'],'text_checked')
        self.assertFalse(c['source']['image_verified'])
        self.assertTrue(all(':p-zhou-' in p['id'] for p in c['paragraphs']))
        progress=next(b for b in read('corpus/progress.json')['books'] if b['book_id']=='b-hanshu-041')
        self.assertFalse(progress['complete'])
        self.assertEqual(progress['person_status'],'in_progress')

    def test_emperor_references_exclude_bashang_place_and_collective_qin(self):
        self.assertEqual(ids(1,'上'),{'yqp_nlb_p1p_A'})
        self.assertEqual(ids(2,'上'),{'yqp_nlb_p1p_A'})
        p=han()['paragraphs'][0];at=p['text'].index('霸上')+1
        self.assertFalse(any(m['start']<=at<m['end'] for m in p['mentions']))
        p=han()['paragraphs'][1];at=p['text'].index('秦攻破天下')
        self.assertFalse(any(m['start']<=at<m['end'] for m in p['mentions']))
        self.assertEqual(ids(1,'韓信'),{'ofc_8ei_jb7'})

    def test_source_parent_claims_are_both_preserved_and_one_is_selected(self):
        b=bundle(JU)
        claims={a['id']:a for a in b['relations'] if a['subject_person_id']==JU and a['predicate']=='father'}
        self.assertEqual(claims['a-shiji098-006']['object_person_id'],ROOT_ID)
        self.assertEqual(claims['a-hanshu041-zhou-003']['object_person_id'],YING)
        self.assertEqual({a['object_person_id'] for a in b['preferred_relations'] if a['subject_person_id']==JU and a['predicate']=='father'},{YING})
        d=next(d for d in b['family_tree_decisions'] if d['id']=='ft-hanshu041-zhou-ju-parent')
        self.assertIn('a-shiji098-006',d['excluded_assertion_ids'])
        self.assertFalse(d['human_reviewed'])
        self.assertNotIn('ancestors',b)
        self.assertEqual(b['assembled_identity']['parent_person_id'],YING)
        self.assertTrue(any(a['subject_person_id']==YING and a['predicate']=='father' and a['object_person_id']==ROOT_ID for a in bundle(YING)['preferred_relations']))

    def test_death_year_does_not_leak_to_son_or_grandson(self):
        events=read('corpus/hanshu/041-life-events.json')['events']
        root=next(e for e in events if e['person_id']==ROOT_ID)
        son=next(e for e in events if e['person_id']==YING)
        self.assertEqual(root['date_expression'],'孝文五年')
        r=root['normalized_date_range']
        self.assertEqual((r['earliest']['era_year'],r['latest']['era_year']),(176,175))
        self.assertIsNone(son['date_expression'])
        self.assertNotIn('normalized_date_range',son)
        self.assertNotIn('normalized_date',son)
        self.assertFalse(any(e['person_id']==JU for e in events))

    def test_title_reading_is_flat_parseable_and_does_not_rewrite_source(self):
        b=bundle(ROOT_ID)
        h=next(h for h in b['title_holdings'] if h['id']=='th-hanshu041-zhou-004')
        r=next(r for r in b['preferred_title_readings'] if r['holding_id']==h['id'])
        self.assertEqual(h['title'],'糨城侯')
        self.assertEqual((r['source_title'],r['preferred_title']),('糨城侯','䣙城侯'))
        self.assertEqual(r['status'],'editorial_provisional')
        d=next(d for d in b['identity_decisions'] if d['id']==r['decision_id'])
        self.assertEqual(d['preferred_reading']['person_mention_id'],h['attestations'][0]['person_mention_id'])
        self.assertFalse(d['references'][0]['image_verified'])
        p=read('data/corpus/profiles/'+ROOT_ID+'.json')
        self.assertNotIn('糨城侯',p['names'])
        self.assertEqual(p['preferred_title_readings'][0]['preferred_title'],'䣙城侯')

    def test_title_year_range_remains_a_title_endpoint(self):
        b=bundle(ROOT_ID)
        r=next(r for r in b['date_range_normalizations'] if r['record_id']=='th-hanshu041-zhou-004')
        self.assertEqual((r['date_role'],r['endpoint']),('title_period','start'))
        self.assertEqual((r['earliest']['era_year'],r['latest']['era_year']),(196,195))
        self.assertNotIn('event_type',r)
        h=next(h for h in b['title_holdings'] if h['id']==r['record_id'])
        self.assertEqual(h['effective_period']['end']['status'],'unknown')

    def test_origin_is_not_a_birthplace_or_modern_jurisdiction(self):
        a=read('corpus/hanshu/041-addresses.json')['assertions'][0]
        self.assertEqual((a['relation'],a['place']['source_name']),('biographical_origin','沛'))
        self.assertIsNone(a['place']['modern_identification'])

    def test_table_people_link_to_canonical_profiles_and_keep_spelling(self):
        table=read('data/historical-tables/shiji-018.json')
        cells={c['id']:c for f in table['fragments'] for row in f['rows'] for c in row['cells']}
        for cid,surface,pid in [('shiji-018-t1-r005-c03','靖','w8j_vnd_rs4_A'),('shiji-018-t1-r063-c06','應',YING),('shiji-018-t1-r063-c06','中居',JU)]:
            self.assertTrue(any(m['surface']==surface and m['person_id']==pid for m in cells[cid]['person_mentions']))
        self.assertIn('侯中居元年',cells['shiji-018-t1-r063-c06']['text'])
        self.assertIn('頃侯靖元年',cells['shiji-018-t1-r005-c03']['text'])

    def test_table_evidence_is_checked_against_hanshu_not_shiji_same_volume(self):
        table=read('data/historical-tables/shiji-018.json')
        m=next(m for f in table['fragments'] for row in f['rows'] for cell in row['cells']
               for m in cell['person_mentions'] if m['surface']=='中居' and m['person_id']==JU)
        validate_identity_evidence(m,ROOT)
        wrong=copy.deepcopy(m);wrong['identity_evidence'][0]['source_revision']=1
        with self.assertRaises(AssertionError):validate_identity_evidence(wrong,ROOT)
        wrong=copy.deepcopy(m);wrong['identity_evidence'][0]['book_id']='b-shiji-041'
        with self.assertRaises(AssertionError):validate_identity_evidence(wrong,ROOT)

    def test_other_work_occurrences_and_names_are_available_without_nlu(self):
        b=bundle(ROOT_ID)
        self.assertTrue(any(s['work_id']=='w-hanshu' for s in b['sources']))
        p=read('data/corpus/profiles/'+ROOT_ID+'.json')
        self.assertTrue(any(x.get('work_id')=='w-hanshu' and x['chapter_id']==han()['id'] and len(x['paragraph_ids'])==3 for x in p['occurrences']))
        for pid in [ROOT_ID,YING,JU,'bwv_ob8_6xi_A']:
            p=read('data/corpus/profiles/'+pid+'.json')
            self.assertEqual(len(p['name_components']),1)
            self.assertTrue(p['name_components'][0]['title'])
            self.assertTrue(p['name_components'][0]['surname'])
            self.assertTrue(p['name_components'][0]['ming'])

    def test_old_table_and_family_ids_have_no_current_records_or_files(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        candidates={p['id'] for p in read('data/historical-tables/person-candidates.json')['persons']}
        for old in ['1we_mne_w25','a1c_h91_cfl','xjk_vf7_dh0','pjq_jpg_3kv','n0z_zzu_7uj','34k_pxx_zvb','0s7_5d3_4ox','jw1_des_ort','pri_i0o_0kd',ROOT_ID+'_B']:
            self.assertNotIn(old,people|candidates)
            self.assertFalse((ROOT/('data/corpus/profiles/'+old+'.json')).exists())
            self.assertFalse((ROOT/('exports/persons/'+old+'.json')).exists())
