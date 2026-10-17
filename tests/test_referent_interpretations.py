# coding: utf-8
"""Ancient readings must remain separate from accepted person occurrences."""
import copy
import json
from pathlib import Path
import unittest
from scripts.referent_interpretations import interpretation_errors
from scripts.person_bundle import bundle
ROOT = Path(__file__).resolve().parents[1]

class ReferentInterpretations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=json.loads((ROOT/'corpus/shiji/117.json').read_text())
        cls.people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
    def changed(self):
        c=copy.deepcopy(self.chapter)
        return c,c['annotation']['referent_interpretations'][0]
    def test_real_readings_have_no_materialized_person_or_default(self):
        self.assertEqual(interpretation_errors(self.chapter,self.people),[])
        cases=self.chapter['annotation']['referent_interpretations']
        self.assertEqual([c['source_terms'] for c in cases],[['陽子'],['纖阿'],['鄭女曼姬']])
        self.assertTrue(all(c['default_alternative_id'] is None for c in cases))
        self.assertTrue(any(not a['candidate_person_ids'] for c in cases for a in c['alternatives']))
    def test_candidate_bundle_retains_evidence_without_counting_a_mention(self):
        b=bundle('3go_52y_0mp',include_provisional=True)
        c,=b['referent_interpretations']
        self.assertEqual(c['source_terms'],['陽子'])
        self.assertEqual(c['work_id'],'w-shiji')
        self.assertEqual(c['book_id'],'b-shiji-117')
        self.assertEqual(c['source_id'],'s-shiji117-xiangru')
        p=next(p for p in b['passages'] if p['id']==c['paragraph_id'])
        self.assertIn(c['evidence']['quote'],p['text'])
        self.assertFalse(any(m['id'] in c['target_mention_ids'] for m in b['mentions']))
        self.assertFalse(any(s['source_id']=='s-shiji117-xiangru' for s in b['source_mention_summary']))
    def test_bundle_rejects_a_fabricated_candidate_source(self):
        from scripts.person_bundle import load_catalog
        catalog=copy.deepcopy(load_catalog())
        chapter=next(r for r in catalog[1] if r.get('id')=='c-shiji-117-xiangru')
        chapter['annotation']['referent_interpretations'][0]['evidence']['quote']='捏造引句'
        with self.assertRaisesRegex(ValueError,'確切引句'):
            bundle('3go_52y_0mp',include_provisional=True,catalog=catalog)
    def test_forced_default_is_not_an_identity_decision(self):
        c,case=self.changed();case['default_alternative_id']=case['alternatives'][0]['id']
        self.assertTrue(interpretation_errors(c,self.people))
    def test_generic_group_cannot_acquire_a_person_id(self):
        c=copy.deepcopy(self.chapter);a=c['annotation']['referent_interpretations'][2]['alternatives'][0]
        self.assertEqual(a['referent_kind'],'generic_group')
        a['candidate_person_ids']=['3go_52y_0mp']
        self.assertTrue(interpretation_errors(c,self.people))
    def test_wrong_source_quote_or_another_paragraph_is_rejected(self):
        c,case=self.changed();case['evidence']['quote']='陽子並非原文中的這一整句'
        self.assertTrue(interpretation_errors(c,self.people))
        c,case=self.changed();case['target_mention_ids']=['c-shiji-117-xiangru:m008-0004']
        self.assertTrue(interpretation_errors(c,self.people))
    def test_unsafe_or_unfixed_commentary_is_rejected(self):
        for bad in ['javascript:alert(1)','https://[','https://github.com/example/blob/main/file.txt']:
            with self.subTest(url=bad):
                c,case=self.changed();case['references'][0]['url']=bad
                self.assertTrue(interpretation_errors(c,self.people))
    def test_missing_or_malformed_reference_cannot_hide_a_reading(self):
        for key,value in [('candidate_person_ids',[{}]),('referent_kind',{}),('source_reference_ids',['unknown'])]:
            with self.subTest(key=key):
                c,case=self.changed();case['alternatives'][0][key]=value
                self.assertTrue(interpretation_errors(c,self.people))
        c,case=self.changed();case['references'][0]['read_line_range']=[163,162]
        self.assertTrue(interpretation_errors(c,self.people))
if __name__=='__main__': unittest.main()
