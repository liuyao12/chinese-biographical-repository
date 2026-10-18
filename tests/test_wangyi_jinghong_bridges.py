import copy
import hashlib
import json
import unittest
from pathlib import Path
from scripts.biographical_kinship import child_continuation_errors
from scripts.family_assemblies import load_assemblies
from scripts.maternal_cousins import maternal_cousin_valid
from scripts.person_bundle import load_catalog, validate_courtesy_name, validate_parallel_given_name
from scripts.posthumous_gifts import posthumous_gift_valid
from scripts.validate_corpus import title_proposal_errors

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class WangYiJinghongBridges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j = read('corpus/jinshu/076.json')
        cls.song = read('corpus/songshu/066.json')
        cls.people = {p['label']: p['id'] for p in read('registry/persons.json')['persons']}
        cls.jrels = read('corpus/jinshu/076-assertions.json')['assertions']
        cls.srels = read('corpus/songshu/066-assertions.json')['assertions']
        cls.holdings = read('corpus/jinshu/076-titles.json')['holdings']
        cls.paras = {p['id']: (c['id'], p) for c in [cls.j, cls.song] for p in c['paragraphs']}
        cls.mentions = {m['id']: (c['id'], p['id'], m) for c in [cls.j, cls.song]
                        for p in c['paragraphs'] for m in p['mentions']}

    def test_same_wang_family_is_reached_from_xie_maternal_grandfather(self):
        _, rows = load_assemblies(ROOT, load_catalog(ROOT))
        root = self.people['王仁']
        for child, father in [('王廙','王正'), ('王頤之','王廙'), ('王胡之','王廙'),
                              ('王茂之','王胡之'), ('王敬弘','王茂之')]:
            self.assertEqual(rows[self.people[child]]['parent_person_id'], self.people[father])
            self.assertEqual(rows[self.people[child]]['root_person_id'], root)
        hu = rows[self.people['王胡之']]
        self.assertEqual(hu['parent_connection']['type'], 'parent_between_consecutive_ancestors')
        self.assertIsNone(hu['source_assertion_id'])
        self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']==self.people['王胡之']
                             for a in self.jrels + self.srels))
        grand = next(a for a in read('corpus/jinshu/079-assertions.json')['assertions']
                     if a['predicate']=='grandfather')
        self.assertEqual(grand['object_person_id'], self.people['王胡之'])
        self.assertEqual(grand['qualifiers']['lineage'], 'maternal')
        self.assertNotEqual(rows[self.people['謝重']]['root_person_id'], root)

    def test_maternal_and_paternal_cousins_are_separate_machine_readable_relations(self):
        maternal = next(a for a in self.jrels if a['predicate']=='maternal_cousin')
        agnatic = next(a for a in self.jrels if a['predicate']=='agnatic_cousin')
        self.assertTrue(maternal_cousin_valid(maternal, self.paras))
        self.assertEqual(maternal['object_person_id'], self.people['晉元帝'])
        self.assertEqual(agnatic['object_person_id'], self.people['王導'])
        self.assertEqual(maternal['qualifiers']['kinship_structure']['maternal_path'], 'mother_sister_son')
        self.assertEqual(maternal['qualifiers']['relative_birth_order']['scope'], 'maternal_cousins')
        for mutator in [lambda a:a['qualifiers']['kinship_structure'].update(lineage='paternal'),
                        lambda a:a.update(object_person_id=self.people['王導']),
                        lambda a:a['qualifiers']['kinship_structure'].update(maternal_path=None),
                        lambda a:a['qualifiers']['relative_birth_order'].update(older_person_id=self.people['王廙'])]:
            bad=copy.deepcopy(maternal);mutator(bad)
            self.assertFalse(maternal_cousin_valid(bad, self.paras))

    def test_junshuai_is_not_the_short_person_name_jun(self):
        p = next(p for p in self.j['paragraphs'] if '廙性俊率' in p['text'])
        at = p['text'].index('俊率')
        self.assertFalse(any(m['start']<=at<m['end'] for m in p['mentions']))
        self.assertTrue(any(m['surface']=='俊' and m['person_id']==self.people['馬俊'] for m in p['mentions']))

    def test_child_continuation_preserves_the_complete_preceding_biography_paragraph(self):
        a = next(a for a in self.jrels if a.get('context',{}).get('kind')=='biographical_child_continuation')
        self.assertEqual(child_continuation_errors(a,self.j), [])
        self.assertEqual([self.paras[e['paragraph_id']][1]['source_position']['first_line'] for e in a['evidence']], [41,43])
        bad=copy.deepcopy(a);bad['evidence']=bad['evidence'][1:]
        self.assertTrue(child_continuation_errors(bad,self.j))
        self.assertEqual(a['subject_person_id'],self.people['王頤之'])
        self.assertEqual(a['object_person_id'],self.people['王廙'])

    def test_declined_offices_and_later_ancestral_usage_do_not_prove_service(self):
        proposals=self.j['annotation']['title_proposals']
        self.assertEqual({p['title'] for p in proposals},{'西中郎將','司州刺史','假節'})
        for p in proposals:
            self.assertEqual(title_proposal_errors(p,self.j,set(self.people.values())),[])
            self.assertFalse(any(h['person_id']==p['person_id'] and h['title']==p['title'] for h in self.holdings))
        usage=next(h for h in read('corpus/songshu/066-titles.json')['holdings'] if h['person_id']==self.people['王胡之'])
        self.assertEqual(usage['title'],'司州刺史')
        self.assertEqual(usage['mode'],'attestation')
        self.assertEqual(usage['effective_period']['start']['status'],'unknown')
        self.assertEqual(usage['effective_period']['end']['status'],'unknown')

    def test_explicit_posthumous_gifts_do_not_invent_a_zhui_character(self):
        gifts=[h for h in self.holdings if h['mode']=='posthumous_grant']
        self.assertEqual({h['title'] for h in gifts},{'侍中','驃騎將軍'})
        for h in gifts:
            self.assertTrue(posthumous_gift_valid(h,self.paras,self.mentions))
            self.assertEqual(h['posthumous_basis']['grant_term'],'贈侍中、驃騎將軍')
            self.assertNotIn('追贈',h['posthumous_basis']['source_term'])
            self.assertIsNone(h['effective_period']['start']['date_expression'])
            bad=copy.deepcopy(h);bad['person_id']=self.people['王敦']
            self.assertFalse(posthumous_gift_valid(bad,self.paras,self.mentions))
            bad=copy.deepcopy(h);bad['posthumous_basis']['grant_term']='追贈'+h['title']
            self.assertFalse(posthumous_gift_valid(bad,self.paras,self.mentions))
        self.assertTrue(all(h['mode']!='posthumous_grant' for h in self.holdings if h['title']=='武陵縣侯'))

    def test_given_name_yuzhi_and_courtesy_jinghong_have_separate_primary_evidence(self):
        n=next(n for n in read('data/corpus/profile-names.json')['records'] if n['person_id']==self.people['王敬弘'])
        self.assertEqual((n['surname'],n['ming'],n['zi']),('王','裕之','敬弘'))
        validate_courtesy_name(n);validate_parallel_given_name(n)
        for ming in ['裕','敬弘']:
            bad=copy.deepcopy(n);bad['ming']=ming
            with self.assertRaises(ValueError):validate_parallel_given_name(bad)
        bad=copy.deepcopy(n);bad['references'][0]['raw_context_quote']='=王裕之='
        bad['references'][0]['raw_context_quote_sha256']=hashlib.sha256('=王裕之='.encode()).hexdigest()
        with self.assertRaises(ValueError):validate_parallel_given_name(bad)
        bad=copy.deepcopy(n);bad['zi_basis']['marker_anchor']['start']+=1
        with self.assertRaises(ValueError):validate_courtesy_name(bad)
        bad=copy.deepcopy(n);bad['zi_basis']['human_reviewed']=True
        with self.assertRaises(ValueError):validate_courtesy_name(bad)

    def test_digital_apparatus_is_not_received_text_or_an_image_collation(self):
        p=self.song['paragraphs'][0]
        self.assertNotIn('<ref>',p['text'])
        excerpt=self.song['source']['normalization']['excerpts'][0]
        self.assertIn('<ref>',excerpt['raw_quote'])
        self.assertEqual(excerpt['removed_digital_editorial_notes'][0]['text_layer'],'modern_digital_apparatus')
        self.assertTrue(all(v['status']=='reported_not_collated' and v['adopted']is False and v['image_verified']is False
                            for v in self.song['annotation']['reported_variants']))
        review=read('docs/source-reviews/wangjinghong-digital-name-and-omission.json')
        self.assertTrue(review['ordinary_nanshi']['observed_heading']['not_name_authority'])
        self.assertFalse(review['kanripo_jinshu_scope']['volume076_present'])

    def test_four_undated_deaths_do_not_share_a_background_year(self):
        events=read('corpus/jinshu/076-life-events.json')['events']
        self.assertEqual({e['person_id'] for e in events},{self.people[n] for n in ['王廙母（未名）','王廙','石季龍','王胡之']})
        self.assertTrue(all(e['date_expression']is None and 'normalized_date'not in e for e in events))
        self.assertFalse(any(a['predicate']=='spouse' and a['subject_person_id']==self.people['王廙母（未名）'] for a in self.jrels))
        origin=read('corpus/songshu/066-addresses.json')['assertions']
        self.assertEqual(len(origin),1)
        self.assertEqual(origin[0]['person_id'],self.people['王敬弘'])
        self.assertIsNone(origin[0]['place']['modern_identification'])

    def test_short_names_and_emperor_titles_keep_contextual_identity(self):
        decisions=read('corpus/jinshu/076-identities.json')['decisions']
        d=next(d for d in decisions if d['id']=='d-jinshu076-mingdi-crownprince')
        self.assertEqual(d['person_id'],self.people['晉明帝'])
        self.assertEqual(set(d['surfaces']),{'明帝','皇太子'})
        p=next(p for p in self.j['paragraphs'] if p['source_position']['first_line']==41)
        self.assertTrue(all(m['person_id']==self.people['晉元帝'] for m in p['mentions'] if m['surface']=='帝'))
        warm=next(d for d in decisions if d['person_id']==self.people['溫嶠'])
        self.assertIn('溫太真',warm['surfaces'])
        self.assertIn('溫嶠，字太真',warm['references'][0]['quote'])


if __name__ == '__main__':
    unittest.main()
