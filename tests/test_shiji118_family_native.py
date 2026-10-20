# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.table_evidence import first_holder_parent_errors
ROOT=Path(__file__).resolve().parents[1]
class HuainanFamilyNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        cls.c=json.loads((ROOT/'corpus/shiji/118.json').read_text())
        cls.mentions={m['id'].split(':')[-1]:m for p in cls.c['paragraphs']for m in p['mentions']}
        cls.assertions=json.loads((ROOT/'corpus/shiji/118-assertions.json').read_text())['assertions']
        cls.native=json.loads((ROOT/'corpus/shiji/019-assertions.json').read_text())['assertions']
        cls.t19=json.loads((ROOT/'data/historical-tables/shiji-019.json').read_text())
    def test_qian_uses_same_family_root_and_evidenced_father(self):
        self.assertNotIn('5th_oxr_3i6',self.people)
        p=self.people['yqp_nlb_p1p_AFAC'];self.assertEqual(p['family_path']['parent_person_id'],'yqp_nlb_p1p_AFA')
        a=next(a for a in self.assertions if a['id']=='a-shiji118-qian-father')
        self.assertEqual((a['subject_person_id'],a['object_person_id']),('yqp_nlb_p1p_AFAC','yqp_nlb_p1p_AFA'))
        self.assertIn('而淮南獨二子，一為太子',a['evidence'][0]['quote'])
        para=next(p for p in self.c['paragraphs']if p['id'].endswith(':p020'))
        self.assertEqual(p['family_path']['evidence'][0]['quote'],para['text'])
    def test_mother_and_spouse_endpoints_do_not_confuse_generations(self):
        a={a['id']:a for a in self.assertions}
        self.assertEqual(a['a-shiji118-qian-wife-mother']['subject_person_id'],'cb7_dmm_znn')
        self.assertEqual(a['a-shiji118-qian-wife-mother']['object_person_id'],'a7k_sl0_d7u_A')
        self.assertEqual(a['a-shiji118-qian-spouse']['subject_person_id'],'yqp_nlb_p1p_AFAC')
        self.assertEqual(a['a-shiji118-qian-spouse']['object_person_id'],'cb7_dmm_znn')
        self.assertEqual(a['a-shiji118-008']['subject_person_id'],'yqp_nlb_p1p_AFAC')
        self.assertEqual(a['a-shiji118-008']['object_person_id'],'8ie_pfa_02i')
        self.assertIn('謝歸去之',a['a-shiji118-qian-spouse']['interpretation_note'])
    def test_daughter_occurrence_id_remains_daughter(self):
        daughter=self.mentions['m016-0078'];mother=self.mentions['m016-0078-mother']
        self.assertEqual((daughter['person_id'],daughter['start'],daughter['end'],daughter['surface']),('cb7_dmm_znn',81,82,'女'))
        self.assertEqual((mother['person_id'],mother['start'],mother['end'],mother['surface']),('a7k_sl0_d7u_A',78,81,'修成君'))
    def test_seven_liwang_mother_ids_remain_mother_not_son(self):
        sons=[m for k,m in self.mentions.items()if k.startswith('m001-')and k.endswith('-child')]
        self.assertEqual(len(sons),7)
        for son in sons:
            key=son['id'].split(':')[-1][:-6];mother=self.mentions[key]
            self.assertEqual(son['person_id'],'yqp_nlb_p1p_AF');self.assertEqual(son['surface'],'厲王')
            self.assertEqual(mother['person_id'],'kuc_m3w_ux2');self.assertEqual(mother['surface'],'母')
            self.assertEqual(son['end'],mother['start'])
        self.assertEqual(self.mentions['m016-0054']['surface'],'王后荼')
    def test_native_candidates_are_retired_and_cross_book_evidence_present(self):
        old={'33x_wkp_7gc','83k_ey4_ntw','boo_4gm_5gs','stn_7hr_r02'}
        candidates=json.loads((ROOT/'data/historical-tables/person-candidates.json').read_text())['persons']
        self.assertFalse(old.intersection(p['id']for p in candidates))
        for nr,pid in [(18,'yqp_nlb_p1p_AFA'),(19,'yqp_nlb_p1p_AFB'),(20,'yqp_nlb_p1p_AFC'),(21,'yqp_nlb_p1p_AFD')]:
            cell=next(c for f in self.t19['fragments']for row in f['rows']for c in row['cells']if c['id']==f'shiji-019-t3-r{nr:03}-c02')
            self.assertTrue(all(m['person_id']==pid for m in cell['person_mentions']))
            self.assertTrue(all(m['identity_evidence'][0]['person_id']==pid for m in cell['person_mentions']))
            self.assertEqual(self.people[pid]['evidence_scope'],'corpus_and_native_table_mentions')
    def test_all_four_native_father_links_are_first_holder_claims(self):
        self.assertEqual(len(self.native),4)
        for a in self.native:
            self.assertEqual(a['predicate'],'father');self.assertEqual(a['object_person_id'],'yqp_nlb_p1p_AF')
            self.assertEqual(first_holder_parent_errors(a['evidence'][0],{'shiji-019':self.t19},a['subject_person_id'],a['object_person_id'],'father'),[])
    def test_synthetic_grandson_phrase_cannot_become_father(self):
        a=self.native[0];t=copy.deepcopy(self.t19);e=copy.deepcopy(a['evidence'][0]);cell=next(c for f in t['fragments']for row in f['rows']for c in row['cells']if c['id']==e['table_cell_id']);cell['text']=cell['text'].replace('子侯','孫侯');e['quote']=cell['text']
        errors=first_holder_parent_errors(e,{'shiji-019':t},a['subject_person_id'],a['object_person_id'],'father')
        self.assertTrue(any('父系原格須明言' in x for x in errors))
    def test_synthetic_later_holder_cannot_borrow_parent_column(self):
        a=self.native[0];e=copy.deepcopy(a['evidence'][0]);e['subject_mention_id']='shiji-019-t3-r018-c02-m001'
        self.assertTrue(first_holder_parent_errors(e,{'shiji-019':self.t19},a['subject_person_id'],a['object_person_id'],'father'))
    def test_seven_years_have_month_specific_parallel_proof_not_fake_days(self):
        hs=json.loads((ROOT/'corpus/shiji/118-titles.json').read_text())['holdings']
        for hid in ['019','020','021','022','024','025','026']:
            h=next(h for h in hs if h['id']=='th-shiji118-'+hid);start=h['effective_period']['start'];date=start['normalized_date'];month='五月'if int(hid)<=22 else'四月';year=172 if int(hid)<=22 else 164
            self.assertEqual((date['era'],date['era_year'],date['year']),('BCE',year,1-year));self.assertIn(month,date['basis']['reference_event_quote']);self.assertNotIn('month',date);self.assertNotIn('day',date)
            self.assertTrue(any(r['scope']=='received_calendar_rule'and'以十月'in r['quote']for r in date['references']))
            for ref in date['references']:
                if ref.get('table_id')in ['shiji-017','shiji-019']:
                    table=json.loads((ROOT/f"data/historical-tables/{ref['table_id']}.json").read_text());cell=next(c for f in table['fragments']for row in f['rows']for c in row['cells']if c['id']==ref['table_cell_id']);self.assertIn(ref['quote'],cell['text']);self.assertEqual(ref['source_revision'],table['source']['revision'])
if __name__=='__main__':unittest.main()
