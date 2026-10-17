# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.lexical_annotations import non_person_errors
from scripts.render_corpus import render
ROOT=Path(__file__).resolve().parents[1]
class HuainanFollowupContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'corpus/shiji/118.json').read_text())
        cls.ps={p['id'].split(':')[-1]:p for p in cls.c['paragraphs']}
        cls.ms={m['id'].split(':')[-1]:m for p in cls.c['paragraphs']for m in p['mentions']}
    def test_hengshan_title_switches_from_bo_to_ci_in_same_paragraph(self):
        for key in ['m014-0116','m014-0135','m014-0160','m014-0180']:
            self.assertEqual(self.ms[key]['person_id'],'yqp_nlb_p1p_AFB')
        for key in ['m014-0097','m014-0182','m014-0197']:
            self.assertEqual(self.ms[key]['person_id'],'yqp_nlb_p1p_AFC')
        self.assertEqual(self.ms['m014-0180']['surface'],'貞王')
    def test_royal_verbs_and_reciprocal_adverb_are_not_people(self):
        for key,role in [('m014-0163','verb'),('m014-0191','reciprocal_adverb'),('m014-0201','verb')]:
            m=self.ms[key];self.assertEqual((m['kind'],m['lexical_role'],m['person_id']),('non_person',role,None));self.assertEqual(non_person_errors(m,self.ps['p014']['text']),[])
        xml=render(self.c)
        self.assertIn('type="non-person" subtype="reciprocal_adverb"',xml)
        self.assertNotIn('persName id="c-shiji-118-huainan:m014-0163"',xml)
    def test_classification_rejects_hidden_people_wrong_context_and_false_review(self):
        base=self.ms['m014-0163'];text=self.ps['p014']['text']
        for changes in [{'person_id':'synthetic_person'},{'work_id':'synthetic_work'},{'basis_quote':'數使使相交'},{'human_reviewed':True},{'lexical_role':'king'},{'interpretation_note':''},{'start':164}]:
            m=copy.deepcopy(base);m.update(changes);self.assertTrue(non_person_errors(m,text),changes)
    def test_two_late_officials_and_retrospective_hong_do_not_merge(self):
        for key,pid in [('m017-0308','cps_fbf_cig'),('m017-0459','cps_fbf_cig'),('m023-0128','cps_fbf_cig'),('m029-0278','mux_1ix_zki'),('m029-0280','tmv_5d7_bx2'),('m029-0294','tmv_5d7_bx2')]:self.assertEqual(self.ms[key]['person_id'],pid)
        for key in ['m023-0020','m023-0025','m023-0074']:self.assertIsNone(self.ms[key]['person_id'])
    def test_hong_anchor_stops_before_following_verbs(self):
        for key in ['m017-0349','m017-0430','m017-0480']:
            m=self.ms[key];self.assertEqual((m['surface'],m['end']-m['start']),('中尉',2));self.assertEqual(m['person_id'],'cps_fbf_cig')
    def test_zhangcang_spelling_has_same_office_event_proof_not_character_rule(self):
        reg=json.loads((ROOT/'registry/persons.json').read_text())['persons'];self.assertNotIn('d8n_9iq_w4h',{p['id']for p in reg});self.assertEqual(self.ms['m004-0004']['person_id'],'796_nkw_0jz_A');self.assertEqual(self.ms['m004-0004']['surface'],'張倉')
        eq=next(d for d in json.loads((ROOT/'corpus/shiji/118-equivalences.json').read_text())['decisions']if d['id']=='eq-shiji118-zhangcang-context');self.assertEqual(len(eq['chapter_ids']),2);self.assertTrue(any('丞相張蒼'in r['quote']for r in eq['references']))
        self.assertIsNone(self.ms['m008-0001']['person_id'])
    def test_birth_does_not_borrow_earlier_conception_year(self):
        e=next(e for e in json.loads((ROOT/'corpus/shiji/118-life-events.json').read_text())['events']if e['id']=='le-shiji118-chang-birth');self.assertEqual((e['person_id'],e['event_type']),('yqp_nlb_p1p_AF','birth'));self.assertIsNone(e['date_expression']);self.assertNotIn('normalized_date',e);self.assertIn('已生厲王',e['evidence'][0]['quote'])
    def test_original_places_do_not_replace_burials_or_claim_birthplaces(self):
        aa=json.loads((ROOT/'corpus/shiji/118-addresses.json').read_text())['assertions'];a={a['id']:a for a in aa};self.assertEqual(a['pa-shiji118-001']['relation'],'burial_place');self.assertEqual(a['pa-shiji118-mother-origin']['relation'],'ancestral_origin')
        for key,place in [('pa-shiji118-mother-origin','真定'),('pa-shiji118-jiuhe-origin','江都'),('pa-shiji118-zhuangzhi-origin','壽春')]:self.assertEqual(a[key]['place']['source_name'],place);self.assertIsNone(a[key]['place']['modern_identification']);self.assertNotEqual(a[key]['relation'],'birth_place')
if __name__=='__main__':unittest.main()
