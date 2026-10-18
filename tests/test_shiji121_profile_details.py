# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((ROOT/rel).read_text())
def fixture():return read('tests/fixtures/shiji121-profile-detail.json')
class ProfileDetailSourceTests(unittest.TestCase):
    def test_jiaoxi_received_words_and_two_anchors_are_preserved(self):
        f=fixture();self.assertEqual(len(f['mentions']),2)
        for row in f['mentions']:
            p=next(p for p in read(row['path'])['paragraphs'] if p['id']==row['paragraph_id'])
            self.assertEqual(p['text'],row['text']);self.assertEqual(next(m for m in p['mentions'] if m['id']==row['marker']['id']),row['marker'])
        self.assertEqual({r['marker']['surface'] for r in f['mentions']},{'繆西王','膠西王'})
    def test_earlier_king_is_not_merged_and_parentage_is_retained(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        self.assertNotIn('6hs_665_32d',people);self.assertIn('yqp_nlb_p1p_ACAN',people);self.assertIn('yqp_nlb_p1p_ABB',people)
        assertions=read('corpus/shiji/059-assertions.json')['assertions']
        own=[a for a in assertions if a['subject_person_id']=='yqp_nlb_p1p_ACAN']
        self.assertEqual({a['object_person_id'] for a in own if a['predicate']=='father'},{'yqp_nlb_p1p_ACA'})
        self.assertEqual({a['object_person_id'] for a in own if a['predicate']=='mother'},{'dlu_57f_6uq'})
    def test_dismissal_ends_remain_undated_and_office_specific(self):
        holdings={h['id']:h for h in read('corpus/shiji/121-titles.json')['holdings']}
        for hid,person,title in [('th-shiji121-011','jh5_a7h_pvv','太子少傅'),('th-shiji121-014','wxo_k8i_1it','太中大夫'),('th-shiji121-023','b1w_3li_mim','清河王太傅')]:
            h=holdings[hid];self.assertEqual((h['person_id'],h['title']),(person,title));end=h['effective_period']['end']
            self.assertEqual((end['status'],end['event_type']),('source_event','explicit_end'));self.assertIsNone(end['date_expression']);self.assertNotIn('normalized_date',end);self.assertNotIn('normalized_date_range',end)
            self.assertTrue(any('免' in e['quote'] for e in end['evidence']))
        self.assertEqual(holdings['th-shiji121-022']['effective_period']['end']['status'],'unknown')
    def test_compound_names_and_royal_surname_evidence_are_distinct(self):
        names={n['person_id']:n for n in read('data/corpus/profile-names.json')['records']}
        for pid,surname,ming in [('482_ly0_otk','顓孫','師'),('oxa_rta_lvd','澹臺','滅明'),('7c4_6v2_yvm','端木','賜')]:
            self.assertEqual((names[pid]['surname'],names[pid]['ming']),(surname,ming));self.assertFalse(names[pid]['human_reviewed'])
        for pid,zi in [('t7x_2x7_1fc','子路'),('482_ly0_otk','子張'),('oxa_rta_lvd','子羽'),('z8l_wje_08d','子夏'),('7c4_6v2_yvm','子貢'),('66i_9gx_pc4','子木'),('fp6_ia6_7yw','仲尼')]:
            self.assertEqual(names[pid]['zi'],zi);self.assertIn('字'+zi,names[pid]['quote'])
        king=names['yqp_nlb_p1p_ACAN'];self.assertEqual((king['title'],king['surname'],king['ming']),('膠西于王','劉','端'))
        ev=next(e for e in king['component_evidence'] if 'surname' in e['field_names']);self.assertEqual(ev['basis'],'documented_paternal_lineage_context');self.assertEqual(ev['source_assertion_id'],'a-shiji059-011')
        self.assertNotIn('劉端',king['quote'])
class ProfileDetailPublicTests(unittest.TestCase):
    def test_retired_generic_profile_is_removed_and_sources_are_joined(self):
        for folder in ['exports/persons','data/corpus/profiles']:self.assertFalse((ROOT/folder/'6hs_665_32d.json').exists())
        profile=read('data/corpus/profiles/yqp_nlb_p1p_ACAN.json');self.assertTrue({'c-shiji-059-wuzong','c-shiji-121-rulin'}.issubset({o['chapter_id'] for o in profile['occurrences']}))
        self.assertEqual({r['object_person_id'] for r in profile['preferred_relations'] if r['predicate']=='father' and r['subject_person_id']==profile['id']},{'yqp_nlb_p1p_ACA'})
    def test_exported_compound_names_keep_surname_and_full_ming(self):
        for pid,surname,ming in [('482_ly0_otk','顓孫','師'),('oxa_rta_lvd','澹臺','滅明'),('7c4_6v2_yvm','端木','賜'),('fp6_ia6_7yw','孔','丘')]:
            for folder in ['exports/persons','data/corpus/profiles']:
                data=read(folder+'/'+pid+'.json');self.assertTrue(any(n['surname']==surname and n['ming']==ming for n in data['name_components']))
    def test_public_office_end_events_are_not_synthetic_years(self):
        for pid,hid in [('jh5_a7h_pvv','th-shiji121-011'),('wxo_k8i_1it','th-shiji121-014'),('b1w_3li_mim','th-shiji121-023')]:
            p=read('data/corpus/profiles/'+pid+'.json');h=next(h for h in p['titles'] if h['id']==hid)
            self.assertEqual(h['effective_period']['end']['event_type'],'explicit_end');self.assertIsNone(h['effective_period']['end']['date_expression'])
if __name__=='__main__':unittest.main()
