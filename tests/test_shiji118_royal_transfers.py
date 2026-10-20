# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.royal_transfers import royal_transfer_errors
from scripts.table_evidence import load_tables,table_regnal_range_errors,calendar_rule_attested
ROOT=Path(__file__).resolve().parents[1]
class HuainanRoyalTransfers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        c=json.loads((ROOT/'corpus/shiji/118.json').read_text());cls.ps={p['id']:(c['id'],p)for p in c['paragraphs']};cls.ms={m['id']:(c['id'],p['id'],m)for p in c['paragraphs']for m in p['mentions']};cls.hs={h['id']:h for h in json.loads((ROOT/'corpus/shiji/118-titles.json').read_text())['holdings']};cls.tables=load_tables(ROOT)
    def test_two_transfers_end_old_roles_at_same_source_event(self):
        for key in ['th-shiji118-bo-jibei-transfer','th-shiji118-ci-hengshan-transfer']:
            h=self.hs[key];self.assertEqual(royal_transfer_errors(h,self.hs,self.ps,self.ms),[]);a=h['effective_period']['start'];b=self.hs[h['transfer_basis']['previous_holding_id']]['effective_period']['end'];self.assertEqual((a['event_type'],b['event_type']),('transfer','explicit_end'));self.assertEqual(a['normalized_date_range'],b['normalized_date_range']);d=a['normalized_date_range'];self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(154,153));self.assertEqual(table_regnal_range_errors(d,a['date_expression'],self.tables,self.ms),[])
    def test_royal_predicate_keeps_original_word_and_territory(self):
        h=self.hs['th-shiji118-bo-jibei-transfer'];self.assertEqual(h['title'],'王');self.assertEqual(h['jurisdictions'][0]['source_name'],'濟北');self.assertEqual(h['attestations'][0]['surface'],'王');self.assertEqual(self.ms['c-shiji-118-huainan:m014-0163'][2]['kind'],'non_person')
    def test_wrong_person_role_and_inferred_death_end_are_rejected(self):
        base=self.hs['th-shiji118-bo-jibei-transfer']
        for change in ['wrong_person','posthumous_predecessor','death_end','wrong_actor','missing_previous','cycle']:
            h=copy.deepcopy(base);hs=copy.deepcopy(self.hs);prior=hs[h['transfer_basis']['previous_holding_id']]
            if change=='wrong_person':prior['person_id']='synthetic-other'
            if change=='posthumous_predecessor':prior['mode']='posthumous_naming'
            if change=='death_end':prior['effective_period']['end']['event_type']='death'
            if change=='wrong_actor':h['transfer_basis']['actor_mention_id']='c-shiji-118-huainan:m014-0182'
            if change=='missing_previous':h['transfer_basis']['previous_holding_id']='synthetic-missing'
            if change=='cycle':prior['transfer_basis']={'previous_holding_id':h['id']}
            self.assertTrue(royal_transfer_errors(h,hs,self.ps,self.ms),change)
    def test_year_prefix_does_not_borrow_unrelated_prince_appointment_month(self):
        h=self.hs['th-shiji118-bo-jibei-transfer'];a=h['effective_period']['start'];d=copy.deepcopy(a['normalized_date_range']);self.assertEqual(d['regnal_year_table']['regnal_year_span'],{'start':0,'end':1,'surface':'四'});self.assertTrue(any('四月己巳立太子'in x['quote']for x in d['references']));self.assertNotIn('month',d['earliest']);self.assertNotIn('day',d['latest'])
        d['regnal_year_table']['regnal_year_span']={'start':2,'end':3,'surface':'四'};self.assertTrue(table_regnal_range_errors(d,a['date_expression'],self.tables,self.ms))
    def test_received_calendar_text_is_a_separate_fixed_witness(self):
        d=self.hs['th-shiji118-bo-jibei-transfer']['effective_period']['start']['normalized_date_range'];ref=next(r for r in d['references']if r['scope']=='received_calendar_rule');self.assertNotIn('建亥',ref['quote']);self.assertTrue(calendar_rule_attested(ref,'han_tenth_month_before_taichu','建亥'))
        for changes in [{'quote':'十月'},{'source_commit':''},{'image_verified':True}]:
            r=copy.deepcopy(ref);r.update(changes);self.assertFalse(calendar_rule_attested(r,'han_tenth_month_before_taichu','建亥'))
    def test_posthumous_names_do_not_supply_the_death_or_transfer_year(self):
        z=self.hs['th-shiji118-bo-zhen-posthumous'];self.assertEqual(z['mode'],'posthumous_naming');self.assertIsNone(z['effective_period']['start']['date_expression']);self.assertNotIn('normalized_date_range',z['effective_period']['start']);self.assertEqual(z['naming_basis']['death_term'],'及薨')
        li=self.hs['th-shiji118-023'];self.assertEqual(li['mode'],'posthumous_grant');self.assertIn('追尊',li['posthumous_basis']['source_term']);self.assertEqual(li['attestations'][0]['usage'],'retrospective');d=li['effective_period']['start']['normalized_date_range'];self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(169,168))
    def test_three_native_occurrences_have_individual_canonical_anchors(self):
        t=self.tables['shiji-017'];cells={x['id']:x for f in t['fragments']for row in f['rows']for x in row['cells']}
        self.assertEqual([(m['surface'],m['person_id'])for m in cells['shiji-017-t1-r054-c07']['person_mentions']],[('勃','yqp_nlb_p1p_AFB'),('貞王','yqp_nlb_p1p_AFB')]);self.assertEqual(cells['shiji-017-t1-r054-c04']['person_mentions'][0]['person_id'],'yqp_nlb_p1p_AFC');self.assertEqual(cells['shiji-017-t1-r054-c07']['text'],'衡山王勃徙濟北十二年。是為貞王。')
if __name__=='__main__':unittest.main()
