# coding: utf-8
import copy,json,re,unittest
from pathlib import Path
from scripts.age_approximations import adjacent_age_errors
from scripts.person_bundle import validate_full_name
ROOT=Path(__file__).resolve().parents[1]
class HuainanAgeNameReadings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'corpus/shiji/118.json').read_text());cls.p=next(p for p in cls.c['paragraphs']if p['id'].endswith(':p011'));cls.ages=[a for a in cls.c['annotation']['age_assertions']if a['id'].startswith('age-shiji118-four-children-')];cls.names={n['person_id']:n for n in json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']}
    def test_four_named_brothers_keep_original_adjacent_numerals(self):
        self.assertEqual({a['person_id']for a in self.ages},{'yqp_nlb_p1p_AFA','yqp_nlb_p1p_AFB','yqp_nlb_p1p_AFC','yqp_nlb_p1p_AFD'})
        for age in self.ages:
            self.assertEqual(adjacent_age_errors(age,self.p),[]);self.assertIsNone(age['value']);self.assertEqual(age['approximation'],{'kind':'adjacent_age_numbers','numbers':[7,8]});self.assertNotIn('bounds',age);self.assertIsNone(age['birth_year'])
    def test_exact_age_bounds_and_birth_year_are_rejected(self):
        for changes in [{'value':7},{'bounds':{'lower':7,'upper':8}},{'birth_year':-178},{'counting':'nominal_age'},{'source_term':'七八歲'},{'reporting_status':'direct_report'}]:
            age=copy.deepcopy(self.ages[0]);age.update(changes);self.assertTrue(adjacent_age_errors(age,self.p),changes)
    def test_numerals_are_adjacent_integers_and_match_the_original(self):
        for approx in [{'kind':'adjacent_age_numbers','numbers':[7,9]},{'kind':'adjacent_age_numbers','numbers':[7.0,8]},{'kind':'adjacent_age_numbers','numbers':[True,8]},{'kind':'strict_range','numbers':[7,8]}]:
            age=copy.deepcopy(self.ages[0]);age['approximation']=approx;self.assertTrue(adjacent_age_errors(age,self.p),approx)
        age=copy.deepcopy(self.ages[0]);age['source_number']='七九';self.assertTrue(adjacent_age_errors(age,self.p))
    def test_group_members_and_count_must_match_real_name_anchors(self):
        for change in ['extra_member','false_count','bool_count','omit_member','unknown_subset']:
            age=copy.deepcopy(self.ages[0]);g=age['group_reference']
            if change=='extra_member':g['person_ids'][1]='synthetic_unmentioned_person'
            if change=='false_count':g['declared_member_count']=5
            if change=='bool_count':g['declared_member_count']=True
            if change=='omit_member':g['person_ids'].pop()
            if change=='unknown_subset':g['additional_members_unknown']=True
            self.assertTrue(adjacent_age_errors(age,self.p),change)
    def test_evidence_binds_same_person_group_and_age_phrase(self):
        for field,value in [('person_mention_id','synthetic-missing'),('quote','皆七八歲'),('paragraph_id','synthetic-paragraph')]:
            age=copy.deepcopy(self.ages[0]);age['evidence'][0][field]=value;self.assertTrue(adjacent_age_errors(age,self.p))
        age=copy.deepcopy(self.ages[0]);age['approximation_interpretation']['human_reviewed']=True;self.assertTrue(adjacent_age_errors(age,self.p))
    def test_numeric_report_year_keeps_the_same_month_specific_event_proof(self):
        for age in self.ages:
            date=age['normalized_date'];self.assertEqual((date['era'],date['era_year'],date['year']),('BCE',172,-171));self.assertEqual(date['original_quote'],self.p['text']);self.assertIn('五月丙午',date['basis']['reference_event_quote']);self.assertNotIn('month',date);self.assertNotIn('day',date)
    def test_unknown_surnames_and_both_received_name_spellings_are_retained(self):
        for pid,ming,title,alias in [('2nl_q1p_8z0','緩',None,'樓緩'),('rvm_asd_jj3','織','南海王','王織')]:
            name=self.names[pid];self.assertIsNone(name['surname']);self.assertEqual(name['ming'],ming);self.assertEqual(name['title'],title);self.assertIn(alias,name['additional_names']);para=next(p for p in self.c['paragraphs']if p['id']==name['paragraph_id']);self.assertIn(alias,para['text']);self.assertFalse(name['human_reviewed'])
            for ref in name['references']:
                raw=re.sub(r'[\s/¶]','',re.sub(r'<pb:[^>]*>','',ref['raw_quote']));self.assertIn(ref['quote'],raw);self.assertIn(ref['source_commit'],ref['url']);self.assertFalse(ref['image_verified'])
        self.assertTrue(any('不言其姓'in x['quote']for x in self.names['2nl_q1p_8z0']['references']));self.assertTrue(any('南海王織'in x['quote']for x in self.names['rvm_asd_jj3']['references']))
    def test_meihe_is_a_whole_name_reading_not_an_invented_surname_split(self):
        name=self.names['f6b_bwf_4dq'];validate_full_name(name);self.assertEqual(name['full_name'],'枚赫');self.assertIsNone(name['surname']);self.assertIsNone(name['ming']);self.assertIn('救赫',name['additional_names'])
        occurrences=[m for p in self.c['paragraphs']for m in p['mentions']if m.get('person_id')=='f6b_bwf_4dq'];self.assertEqual([m['surface']for m in occurrences],['救赫','救赫']);self.assertEqual([m['id'].split(':')[-1]for m in occurrences],['m027-0519','m029-0218'])
    def test_whole_name_requires_fixed_received_spelling_and_no_segmentation(self):
        base=self.names['f6b_bwf_4dq']
        for changes in [{'surname':'枚'},{'ming':'赫'},{'quote':None},{'full_name':'合成未見姓名'}]:
            name=copy.deepcopy(base);name.update(changes)
            with self.assertRaises(ValueError):validate_full_name(name)
        wrong=copy.deepcopy(base);wrong['full_name_basis']['source_term']='陳喜';para=next(p for p in self.c['paragraphs']if p['id']==wrong['paragraph_id'])
        with self.assertRaises(ValueError):validate_full_name(wrong,para)
        for key,value in [('source_commit',None),('quote','合成未見引句'),('image_verified',True)]:
            name=copy.deepcopy(base)
            for ref in name['references']:ref[key]=value
            with self.assertRaises(ValueError):validate_full_name(name)
if __name__=='__main__':unittest.main()
