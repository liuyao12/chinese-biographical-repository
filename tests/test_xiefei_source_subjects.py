"""Semantic counterexamples use real same-paragraph identities and valid anchors."""
import copy,json,unittest
from pathlib import Path
from scripts import biography_source_details as rules
ROOT=Path(__file__).resolve().parents[1]
class SourceSubjectTests(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/liangshu/015-xiefei.json').read_text())
  self.records=[json.loads(p.read_text())for p in(ROOT/'corpus/liangshu').glob('015-xiefei-*.json')]
  self.hs={h['id']:h for r in self.records for h in r.get('holdings',[])}
  self.qs={q['id']:q for q in self.ch['annotation']['title_proposals']}
  self.ds={d['id']:d for r in self.records for d in r.get('records',[])}
 def wrong(self,suffix,surface):
  d=copy.deepcopy(self.ds['bd-liang015-xiefei-'+suffix]);p=next(p for p in self.ch['paragraphs']if p['id']==d['source_anchor']['paragraph_id']);m=next(m for m in p['mentions']if m['surface']==surface)
  d['person_id']=m['person_id'];d['evidence'][0]['person_mention_id']=m['id']
  return d
 def check_wrong(self,suffix,surface):
  d=self.wrong(suffix,surface)
  if suffix=='edicts':d['values']['linked_holding_id']=next(h['id']for h in self.hs.values()if h['person_id']==d['person_id']and h['title']=='侍中')
  if suffix=='funeral-gifts':d['values']['recipient_person_id']=d['person_id']
  self.assertFalse(rules.valid(d,self.ch,self.hs,self.qs))
 def test_all_original_details_and_extended_holdings(self):self.assertEqual([],rules.errors({self.ch['id']:self.ch},self.records))
 def test_drafting_is_not_later_wangjian(self):self.check_wrong('edicts','王儉')
 def test_dismissed_is_not_ordering_gaodi(self):self.check_wrong('dismissed','齊高帝')
 def test_mourning_is_not_emperor_mourner(self):self.check_wrong('mourning-retained','輿駕')
 def test_composer_is_child_not_commanding_xiaowu(self):self.check_wrong('dongjingzan','孝武帝')
 def test_funeral_recipient_not_emperor_mourner(self):self.check_wrong('funeral-gifts','輿駕')
 def test_four_friends_not_any_four_people(self):
  h=copy.deepcopy(next(h for h in self.hs.values()if'collective_designation'in h));p=next(p for p in self.ch['paragraphs']if p['id']==h['evidence'][0]['paragraph_id']);m=p['mentions'][0];b=h['collective_designation'];b['member_person_ids'][0]=m['person_id'];b['member_mention_ids'][0]=m['id'];h['person_id']=m['person_id'];h['evidence'][0]['person_mention_id']=m['id']
  self.assertFalse(rules.holding_valid(h,self.ch,self.hs))
 def test_service_duration_not_earlier_doctorate(self):
  h=copy.deepcopy(next(h for h in self.hs.values()if'reported_duration'in h));h['title']='國子博士'
  self.assertFalse(rules.holding_valid(h,self.ch,self.hs))
 def test_unsupported_local_subject_wording_fails_closed(self):
  ch=copy.deepcopy(self.ch);p=ch['paragraphs'][2];p['text']=p['text'].replace('選朏爲長史','選王儉爲長史');d=self.ds['bd-liang015-xiefei-edicts']
  self.assertFalse(rules.source_subject_valid(d,p,ch))
 def test_id_rekey_does_not_need_allowlist(self):
  ch=copy.deepcopy(self.ch);old=ch['paragraphs'][0]['mentions'][0]['person_id'];new='abc_def_123'
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')==old:m['person_id']=new
  d=copy.deepcopy(self.ds['bd-liang015-xiefei-dongjingzan']);d['person_id']=new
  p=ch['paragraphs'][0];self.assertTrue(rules.source_subject_valid(d,p,ch))
if __name__=='__main__':unittest.main()
