"""Actual Song052 complete-role templates; six records, not complete career coverage."""
import copy,json,unittest
from pathlib import Path
try:
    from scripts.received_career_roles import holding_valid
except ImportError:
    from received_career_roles import holding_valid
ROOT=Path(__file__).resolve().parents[1]
class SixTitles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((ROOT/'corpus/songshu/052-xiejingren.json').read_text());d=json.loads((ROOT/'corpus/songshu/052-xiejingren-titles.json').read_text());ids={'th-song052-career-'+x for x in('044','045','049','050','052','076')};cls.hs=[h for h in d['holdings']if h['id']in ids]
    def test_six_actual_titles(self):
        self.assertEqual(len(self.hs),6)
        self.assertEqual({h['title']for h in self.hs},{'金紫光禄大夫','散騎常侍','衞軍長史','司徒左長史','鄱陽太守','西陽太守'})
        for h in self.hs:self.assertTrue(holding_valid(h,self.c,root=ROOT),h['id']);self.assertIsNone(h['effective_period']['end']['date_expression'])
    def test_posthumous_stays_posthumous(self):
        for old in self.hs:
            if old['mode']!='posthumous_grant':continue
            h=copy.deepcopy(old);h['mode']='grant';h['effective_period']['start']['event_type']='grant';h.pop('posthumous_basis')
            self.assertFalse(holding_valid(h,self.c,root=ROOT))
    def test_wrong_recipient_and_role(self):
        for old in self.hs:
            h=copy.deepcopy(old);h['person_id']='synthetic_unrelated';self.assertFalse(holding_valid(h,self.c,root=ROOT))
        h=copy.deepcopy(next(h for h in self.hs if h['title']=='衞軍長史'));ms={m['id']:m for p in self.c['paragraphs']for m in p['mentions']};b=h['source_career_role'];wrong=next(k for k,v in b['roles'].items()if ms[v]['person_id']!=h['person_id'])
        b['recipient_role']=wrong;h['person_id']=ms[b['roles'][wrong]]['person_id'];h['evidence'][0]['person_mention_id']=b['roles'][wrong];h['attestations'][0]['person_mention_id']=b['roles'][wrong]
        self.assertFalse(holding_valid(h,self.c,root=ROOT))
    def test_missing_roles_shifted_span_or_borrowed_death_year(self):
        for edit in('role','span','year','end'):
            h=copy.deepcopy(self.hs[0]);b=h['source_career_role']
            if edit=='role':b['roles'].pop(next(iter(b['roles'])))
            elif edit=='span':h['attestations'][0]['start']+=1
            elif edit=='year':h['effective_period']['start']['date_expression']='十二年'
            else:h['effective_period']['end']=dict(status='source_event',event_type='death',date_expression='十二年',evidence=h['evidence'])
            self.assertFalse(holding_valid(h,self.c,root=ROOT),edit)
    def test_other_paragraph_and_source_revision(self):
        for edit in('source','quote'):
            c=copy.deepcopy(self.c);h=copy.deepcopy(self.hs[0])
            if edit=='source':c['source']['revision_id']='unreviewed_revision'
            else:h['evidence'][0]['quote']=h['evidence'][0]['quote'][:-1]
            self.assertFalse(holding_valid(h,c,root=ROOT),edit)
    def test_attainment_and_null_periods_preserved(self):
        h=next(h for h in self.hs if h['title']=='西陽太守');self.assertEqual(h['mode'],'attestation');self.assertEqual(h['appointment_role'],'reported_attainment')
        for h in self.hs:
            self.assertFalse(any(k in h['effective_period']['start']for k in('normalized_date','normalized_date_range')))
            self.assertEqual(h['effective_period']['end'],dict(status='unknown',date_expression=None,evidence=[]))
if __name__=='__main__':unittest.main()
