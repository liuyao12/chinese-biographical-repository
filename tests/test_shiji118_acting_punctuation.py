# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.office_attributions import punctuation_attribution_errors
ROOT=Path(__file__).resolve().parents[1]
class ActingPunctuation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        c=json.loads((ROOT/'corpus/shiji/118.json').read_text());cls.ps={p['id']:(c['id'],p)for p in c['paragraphs']};cls.ms={m['id']:(c['id'],p['id'],m)for p in c['paragraphs']for m in p['mentions']};cls.hs={h['id']:h for h in json.loads((ROOT/'corpus/shiji/118-titles.json').read_text())['holdings']};cls.h=cls.hs['th-shiji118-fengjing-acting-yushi']
    def test_parallel_syntax_supports_fengjing_without_repunctuating_received_text(self):
        self.assertEqual(punctuation_attribution_errors(self.h,self.ps,self.ms),[]);self.assertEqual(self.h['person_id'],'74s_z7l_t28');self.assertEqual(self.h['appointment_role'],'acting');self.assertIn('典客臣馮敬、行御史大夫事宗正臣逸',self.ps['c-shiji-118-huainan:p004'][1]['text']);self.assertEqual(self.h['punctuation_attribution']['preferred_segmentation'],'典客臣馮敬行御史大夫事、宗正臣逸')
    def test_prior_offices_remain_separate_from_acting_office(self):
        self.assertEqual((self.hs['th-shiji118-010']['person_id'],self.hs['th-shiji118-010']['title']),('74s_z7l_t28','典客'));self.assertEqual((self.hs['th-shiji118-011']['person_id'],self.hs['th-shiji118-011']['title']),('vhn_2qv_ziz','宗正'));self.assertNotIn('appointment_role',self.hs['th-shiji118-011'])
    def test_annotation_regnal_numbers_do_not_become_office_endpoints(self):
        self.assertEqual(self.h['mode'],'attestation')
        for boundary in self.h['effective_period'].values():self.assertEqual(boundary,{'status':'unknown','date_expression':None,'evidence':[]})
        self.assertTrue(any('宋祁' in ref['quote'] for ref in self.h['punctuation_attribution']['references']))
    def test_readable_quotes_keep_raw_markers_separately_and_cannot_change_words(self):
        refs=self.h['punctuation_attribution']['references'];self.assertTrue(any('<pb:' in ref['quote'] for ref in refs))
        for ref in refs:self.assertNotIn('¶',ref['display_quote']);self.assertNotIn('<pb:',ref['display_quote'])
        h=copy.deepcopy(self.h);h['punctuation_attribution']['references'][0]['display_quote']='合成錯字';self.assertTrue(punctuation_attribution_errors(h,self.ps,self.ms))
    def test_wrong_actor_unfixed_parallel_or_formal_grant_is_rejected(self):
        for change in ['wrong_actor','same_alternative','grant','formal','human','wrong_phrase','unfixed','wrong_parallel']:
            h=copy.deepcopy(self.h);a=h['punctuation_attribution']
            if change=='wrong_actor':h['person_id']='vhn_2qv_ziz'
            if change=='same_alternative':a['alternative_person_mention_id']=a['person_mention_id']
            if change=='grant':h['mode']='grant'
            if change=='formal':h['appointment_role']='regular'
            if change=='human':a['human_reviewed']=True
            if change=='wrong_phrase':a['received_segment']='宗正臣逸'
            if change=='unfixed':
                for ref in a['references']:ref['source_commit']=''
            if change=='wrong_parallel':
                for ref in a['references']:ref['quote']='合成錯誤：宗正逸行御史大夫事'
            self.assertTrue(punctuation_attribution_errors(h,self.ps,self.ms),change)

if __name__=='__main__':unittest.main()
