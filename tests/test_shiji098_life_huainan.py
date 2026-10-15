import json
import unittest
from pathlib import Path
from scripts.family_assemblies import load_assemblies
from scripts.person_bundle import load_catalog
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
class FuJinLifeAndHuainanTests(unittest.TestCase):
    def test_same_an_is_identified_by_shared_events_not_title_alone(self):
        for book,n,term in [('098',4,'淮南王'),('107',26,'淮南王安'),('118',15,'淮南王安')]:
            p=read('corpus/shiji/'+book+'.json')['paragraphs'][n-1]
            self.assertTrue(any(m['surface']==term and m.get('person_id')=='yqp_nlb_p1p_AFA' for m in p['mentions']))
        eq=next(d for d in read('corpus/shiji/098-equivalences.json')['decisions'] if d['id']=='eq-shiji098-huainan-an')
        self.assertTrue(eq['identity_materialized'])
        self.assertIn('元狩元年',eq['references'][0]['quote'])
        self.assertIn('霸上',eq['rationale'])
    def test_explicit_father_replaces_missing_generation_without_losing_grandfather(self):
        source,_=load_assemblies(ROOT,load_catalog(ROOT));person=source['yqp_nlb_p1p_AFA']
        self.assertEqual(person['parent_person_id'],'yqp_nlb_p1p_AF')
        self.assertEqual(person['source_assertion_id'],'a-shiji118-003')
        claim=next(a for a in read('corpus/shiji/107-assertions.json')['assertions'] if a['id']=='a-shiji107-015')
        self.assertEqual(claim['subject_person_id'],person['person_id'])
        self.assertEqual(claim['predicate'],'grandfather')
        self.assertEqual(claim['object_person_id'],'yqp_nlb_p1p_A')
    def test_six_deaths_have_own_source_person_anchors(self):
        c=read('corpus/shiji/098.json');paragraphs={p['id']:p for p in c['paragraphs']}
        events=read('corpus/shiji/098-life-events.json')['events'];self.assertEqual(len(events),6)
        for event in events:
            e=event['evidence'][0];p=paragraphs[e['paragraph_id']]
            self.assertIn(e['quote'],p['text']);self.assertIn(event['source_term'],e['quote'])
            m=next(m for m in p['mentions'] if m['id']==e['person_mention_id'])
            self.assertEqual(m['person_id'],event['person_id'])
    def test_unknown_relative_years_do_not_become_absolute_death_years(self):
        events=read('corpus/shiji/098-life-events.json')['events']
        for event in events[1:4]:
            self.assertNotIn('normalized_date',event);self.assertNotIn('normalized_date_range',event)
        self.assertEqual(events[3]['date_expression'],'三十一年')
    def test_pre_taichu_deaths_are_ranges_with_calendar_evidence(self):
        events=read('corpus/shiji/098-life-events.json')['events']
        for index,years in [(0,(191,190)),(4,(184,183)),(5,(176,175))]:
            r=events[index]['normalized_date_range']
            self.assertEqual((r['earliest']['era_year'],r['latest']['era_year']),years)
            self.assertEqual(r['year_numbering'],'astronomical')
            self.assertTrue(any(x.get('text_layer')=='suoyin_commentary' and '建亥' in x['quote'] for x in r['references']))
    def test_three_retired_ids_are_absent_from_registry_and_public_files(self):
        ids={p['id'] for p in read('registry/persons.json')['persons']}
        for old in ['tk5_g6e_rh8','yqp_nlb_p1p_A*A','brp_v5i_sjg']:
            self.assertNotIn(old,ids)
            for folder in ['exports/persons','data/corpus/profiles']:
                self.assertFalse((ROOT/folder/(old+'.json')).exists())

    def test_recorded_death_does_not_automatically_end_attested_titles(self):
        holdings=read('corpus/shiji/098-titles.json')['holdings']
        for record_id in ['th-shiji098-001','th-shiji098-002','th-shiji098-003']:
            h=next(h for h in holdings if h['id']==record_id)
            self.assertEqual(h['effective_period']['end']['status'],'unknown')

    def test_direct_grandfather_and_father_chain_resolve_to_one_gaozu(self):
        profile=read('data/corpus/profiles/yqp_nlb_p1p_AFA.json')
        direct={a['object_person_id'] for a in profile['preferred_relations']
                if a['subject_person_id']==profile['id'] and a['predicate']=='grandfather'}
        father=read('data/corpus/profiles/yqp_nlb_p1p_AF.json')
        inherited={a['object_person_id'] for a in father['preferred_relations']
                   if a['subject_person_id']==father['id'] and a['predicate']=='father'}
        self.assertEqual(direct,{'yqp_nlb_p1p_A'})
        self.assertEqual(inherited,{'yqp_nlb_p1p_A'})
