from pathlib import Path
from copy import deepcopy
import json,unittest
from scripts.nanqi043_wangsiyuan import errors, proposal_valid, funeral_award, kin_valid
ROOT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((ROOT/('corpus/nanqishu/043-'+n+'.json')).read_text())
class WangSiyuan(unittest.TestCase):
    def test_unassumed_offices_and_resumed_subject(self):
        ch=read('wangsiyuan');self.assertFalse(errors(ch,ROOT));ps=ch['annotation']['title_proposals'];self.assertEqual(len(ps),7);self.assertTrue(all(proposal_valid(q,ch) for q in ps));h=read('wangsiyuan-titles')['holdings'];self.assertTrue(set(x['title']for x in ps).isdisjoint(x['title']for x in h));pr=deepcopy(ps[-1]);pr['person_id']='i08_s4b_5bb';self.assertFalse(proposal_valid(pr,ch));es={e['id']:e for e in read('wangsiyuan-life-events')['events']};e=es['le-nanqi043-wangsiyuan-death'];self.assertEqual(e['normalized_date']['year'],500);self.assertEqual(e['evidence'][0]['context']['quote'],'思遠清脩，立身簡潔。');self.assertTrue(all(funeral_award(a,ch,es,ROOT)for a in h if a['mode'].startswith('posthumous_')))
    def test_two_brothers_and_gu(self):
        ch=read('wangsiyuan');k=read('wangsiyuan-assertions')['assertions'];s=[a for a in k if a['predicate']=='brother'];self.assertEqual({a['qualifiers']['source_term']for a in s},{'思遠兄思微','長兄思玄'});self.assertTrue(all(kin_valid(a,ch,ROOT) for a in s));s[0]['subject_person_id']=s[1]['subject_person_id'];self.assertFalse(kin_valid(s[0],ch,ROOT));self.assertIn('迎其兒子',ch['paragraphs'][-1]['text']);self.assertEqual(read('wangsiwei-life-events')['events'][0]['date_expression'],None)
