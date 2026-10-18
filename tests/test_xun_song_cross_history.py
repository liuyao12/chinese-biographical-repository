import json
import unittest
from pathlib import Path

from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog

ROOT=Path(__file__).resolve().parents[1]
STEM='yoo_ox0_545'


class XunSongSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=load_catalog(ROOT)
        cls.mapping,cls.members=load_assemblies(ROOT,cls.catalog)

    def test_yun_han_yun_song_bridge_and_children_share_documented_paternal_root(self):
        for child,parent in [('BAB','BA'),('BABA','BAB'),('BABAA','BABA'),('BABAAA','BABAA'),
                             ('BABAAAA','BABAAA'),('BABAAAB','BABAAA'),('BABAAAC','BABAAA')]:
            self.assertEqual(self.members[STEM+'_'+child]['parent_person_id'],STEM+'_'+parent)

    def test_two_sibling_based_fathers_remain_inferences_not_fabricated_source_claims(self):
        for suffix in ['BAC','BAD']:
            row=self.members[STEM+'_'+suffix]
            self.assertEqual(row['parent_person_id'],STEM+'_BA')
            self.assertIsNone(row['source_assertion_id'])
            self.assertIn(row['parent_connection']['type'],['shared_father_through_sibling','shared_father_through_sibling_chain'])

    def test_maternal_grandfather_and_care_do_not_become_paternal_ancestry_or_adoption(self):
        data=json.loads((ROOT/'corpus/jinshu/075-assertions.json').read_text())['assertions']
        maternal=next(a for a in data if a['predicate']=='grandfather' and a['qualifiers'].get('lineage')=='maternal')
        self.assertEqual(maternal['subject_person_id'],STEM+'_BABAAA')
        self.assertNotIn(maternal['object_person_id'],self.members)
        self.assertFalse(any(a['predicate'].startswith('adoptive') for a in data))

    def test_unnamed_women_do_not_acquire_a_given_name_or_assumed_birth_children(self):
        records=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']
        zhong=next(n for n in records if n.get('clan_style',{}).get('value')=='鍾氏' and n.get('zi')=='琰')
        self.assertIsNone(zhong['ming'])
        wife=next(n for n in records if n.get('clan_style',{}).get('value')=='司馬氏')
        self.assertIsNone(wife['ming'])
        relations=json.loads((ROOT/'corpus/sanguozhi/010-assertions.json').read_text())['assertions']
        self.assertFalse(any(a['predicate']=='mother' and a['object_person_id']==wife['person_id'] for a in relations))

    def test_digital_force_count_stays_distinct_from_the_modern_quotation(self):
        chapter=json.loads((ROOT/'corpus/jinshu/096.json').read_text())
        self.assertIn('乃率勇士數千人',next(p['text'] for p in chapter['paragraphs']if 'xunguan' in p['id']))
        review=json.loads((ROOT/'docs/source-reviews/jinshu096-xunguan-force-count.json').read_text())
        self.assertEqual(review['reported_reading'],'數十人')
        self.assertFalse(review['printed_edition_directly_checked'])

    def test_era_windows_do_not_supply_undated_han_death_or_guangyang_grant_year(self):
        titles=json.loads((ROOT/'corpus/sanguozhi/010-titles.json').read_text())['holdings']
        guangyang=next(h for h in titles if h['person_id']==STEM+'_BABA' and h['title']=='廣陽鄉侯')
        self.assertIsNone(guangyang['effective_period']['start']['date_expression'])
        self.assertNotIn('normalized_date_range',guangyang['effective_period']['start'])
        office=next(h for h in titles if h['person_id']==STEM+'_BAA' and h['title']=='司空')
        window=office['effective_period']['start']['normalized_date_range']
        self.assertEqual([window[k]['year']for k in ['earliest','latest']],[264,265])
        self.assertEqual(window['calendar'],'chinese_civil')
        self.assertNotIn('year',window)

    def test_reburial_360_is_not_a_death_year_or_his_mothers_burial_location(self):
        event=json.loads((ROOT/'corpus/jinshu/075-events.json').read_text())['events'][0]
        self.assertEqual((event['event_type'],event['burial_kind'],event['normalized_date']['year']),('burial','reburial',360))
        self.assertNotIn('place',event)
