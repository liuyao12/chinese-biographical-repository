import copy
import json
import unittest
from pathlib import Path
from scripts.unspecified_ancestry import reported_generation_formula_valid
from scripts.validate_corpus import source_age_number

ROOT=Path(__file__).resolve().parents[1]

class SimaNearAncestry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'corpus/jinshu/001.json').read_text())
        cls.p=cls.c['paragraphs'][0]
        cls.a=json.loads((ROOT/'corpus/jinshu/001-assertions.json').read_text())['assertions']
        cls.paras={cls.p['id']:(cls.c['id'],cls.p)}
        cls.f=next(f for f in json.loads((ROOT/'registry/family-assemblies.json').read_text())['assemblies'] if f['id']=='family-sima-jun-near-ancestry')

    def test_near_fathers_are_distinct_from_unadopted_eight_generation_report(self):
        fathers=[a for a in self.a if a['id'].startswith('a-jinshu001-near-father-')]
        self.assertEqual(len(fathers),4)
        remote=next(a for a in self.a if a['predicate']=='ancestor')
        self.assertTrue(reported_generation_formula_valid(remote,self.paras,source_age_number))
        self.assertEqual(remote['qualifiers']['reported_generation_number'],8)
        self.assertIsNone(remote['qualifiers']['generation_distance'])
        self.assertFalse(remote['qualifiers']['adopted_for_family_tree'])
        members={m['person_id'] for m in self.f['members']}
        self.assertNotIn(remote['object_person_id'],members)
        self.assertNotIn('2to_ofg_fuz',members)
        required={p for a in fathers for p in (a['subject_person_id'],a['object_person_id'])}
        required.update(a['subject_person_id'] for a in self.a if a['id']=='a-jinshu001-lang-elder-brother')
        self.assertTrue(required <= members)

    def test_report_cannot_become_exact_adopted_path_or_change_source_count(self):
        a=next(a for a in self.a if a['predicate']=='ancestor')
        for key,value in [('generation_distance',8),('adopted_for_family_tree',True),('reported_generation_number',7),('reported_generation_number',True),('source_number','四')]:
            bad=copy.deepcopy(a);bad['qualifiers'][key]=value
            with self.subTest(key=key,value=value):
                self.assertFalse(reported_generation_formula_valid(bad,self.paras,source_age_number))
        bad=copy.deepcopy(a);bad['evidence'][0]['quote']=bad['qualifiers']['source_term']
        self.assertFalse(reported_generation_formula_valid(bad,self.paras,source_age_number))

    def test_second_son_and_older_brother_remain_separate_constraints(self):
        yi=next(a for a in self.a if a['qualifiers'].get('birth_order'))
        self.assertEqual(yi['qualifiers']['birth_order']['ordinal'],2)
        older=next(a for a in self.a if a['predicate']=='brother')
        self.assertEqual(older['object_person_id'],yi['subject_person_id'])
        order=older['qualifiers']['relative_birth_order']
        self.assertEqual(order['older_person_id'],older['subject_person_id'])
        self.assertIsNone(order['older_ordinal'])
        member=next(m for m in self.f['members'] if m['person_id']==older['subject_person_id'])
        self.assertIsNone(member['source_assertion_id'])
        self.assertEqual(member['parent_connection']['type'],'shared_father_through_sibling')

    def test_later_critical_note_is_separate_from_received_text(self):
        self.assertIn('南陽太守',self.p['text'])
        self.assertNotIn('錢大昕',self.p['text'])
        notes=self.c['source']['normalization']['removed_apparatus']
        self.assertEqual(notes[0]['text_layer'],'later_critical_apparatus')
        self.assertIn('南郡',notes[0]['raw_note'])
        self.assertFalse(notes[0]['collated_by_current_agent'])
        self.assertFalse(self.c['source']['image_verified'])

    def test_legendary_zhongli_is_not_forced_into_one_existing_person(self):
        m=next(m for m in self.p['mentions'] if m['surface']=='重黎')
        self.assertEqual(m['kind'],'unresolved')
        self.assertIsNone(m['person_id'])
        self.assertIn('單名',m['interpretation_note'])

    def test_same_commandery_is_not_confused_with_yangjuns_office(self):
        addresses=json.loads((ROOT/'corpus/jinshu/001-addresses.json').read_text())['assertions']
        yang=next(a for a in addresses if a.get('qualifiers',{}).get('place_resolution'))
        resolution=yang['qualifiers']['place_resolution']
        principal=next(a for a in addresses if a['id']==resolution['reference_address_assertion_id'])
        self.assertEqual(principal['person_id'],resolution['reference_person_id'])
        self.assertEqual(yang['place']['source_name'],'河內')
        self.assertTrue(principal['place']['source_name'].startswith('河內'))
        self.assertIn('同郡楊俊',yang['evidence'][0]['quote'])
        self.assertFalse(any(a['relation']=='birth_place' for a in addresses))

    def test_source_title_usage_does_not_invent_a_lifetime_imperial_accession(self):
        holdings=[h for h in json.loads((ROOT/'corpus/jinshu/001-titles.json').read_text())['holdings']
                  if h['id'].startswith('th-jinshu001-near-')]
        emperor=next(h for h in holdings if h['title']=='宣皇帝')
        self.assertEqual(emperor['mode'],'attestation')
        self.assertEqual(emperor['attestations'][0]['usage'],'retrospective')
        self.assertEqual(emperor['effective_period']['start']['status'],'unknown')
        self.assertFalse(any('normalized_date' in h['effective_period']['start'] for h in holdings))
        wang=next(h for h in holdings if h['title']=='殷王')
        self.assertIsNone(wang['effective_period']['start']['date_expression'])
        self.assertEqual(wang['mode'],'grant')

    def test_orphans_old_ids_are_retired_and_care_does_not_replace_their_father(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for old in ['0k9_2g5_4su','5nd_lzj_e9f']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/('exports/persons/'+old+'.json')).exists())
            self.assertFalse((ROOT/('data/corpus/profiles/'+old+'.json')).exists())
        assertions=json.loads((ROOT/'corpus/jinshu/075-assertions.json').read_text())['assertions']
        for child in ['1ay_9qe_u4h_A','1ay_9qe_u4h_B']:
            self.assertIn(child,people)
            self.assertTrue(any(a['subject_person_id']==child and a['predicate']=='father' and a['object_person_id']=='1ay_9qe_u4h' for a in assertions))
            self.assertFalse(any(a['subject_person_id']==child and a['predicate']=='father' and a['object_person_id']=='yoo_ox0_545_BABAAA' for a in assertions))

if __name__=='__main__':unittest.main()
