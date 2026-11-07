"""Readonly current-source controls for the bounded 031 remaining-title phase."""
from pathlib import Path
import copy,json,hashlib,unittest
from scripts import fixed_jin031_jia_full_ner as ner, fixed_jin031_jia_typed as typed
from scripts import fixed_jin031_jia_remaining_titles as more
from scripts.noble_transfers import noble_transfer_errors
from scripts.royal_transfers import royal_transfer_errors
ROOT=Path(__file__).resolve().parents[1]
class RemainingTitles(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.paths=typed.fixture_paths(ROOT);cls.hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in cls.paths};cls.ch=ner.core.read(ROOT,ner.core.CH);cls.r,cls.b=ner.prepared(cls.ch,ROOT);cls.ps={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.ms={m['id']:(cls.ch['id'],p['id'],m)for p in cls.ch['paragraphs']for m in p['mentions']};cls.hs=ner.core.read(ROOT,'corpus/jinshu/031-jia-comparison-titles.json')['holdings'];cls.by={h['id']:h for h in cls.hs};cls.chapters={cls.ch['id']:cls.ch}
 @classmethod
 def tearDownClass(cls):assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in cls.hashes.items())
 def change_records(self):return[self.by['th-jin031-more-guo-yicheng'],self.by['th-jin031-more-linhai-renamed']]
 def error(self,h,holdings=None,chapters=True,root=True):
  holdings=self.by if holdings is None else holdings;chs=self.chapters if chapters is True else chapters;rt=ROOT if root else None
  if h['kind']=='noble_rank':return noble_transfer_errors(h,holdings,self.ps,self.ms,chs,root=rt)
  return royal_transfer_errors(h,holdings,self.ps,self.ms,chapters=chs,root=rt)
 def test_original_204_mids_and_old_typed_exact(self):
  old=ner.core.expand(json.loads((ROOT/ner.EP).read_bytes())['chapter_template'],self.r);oldids={m['id']:m for p in old['paragraphs']for m in p['mentions']};actual={m['id']:m for p in self.ch['paragraphs']for m in p['mentions']};self.assertTrue(all(actual[mid]==value for mid,value in oldids.items()));self.assertEqual(set(actual)-set(oldids),{self.ch['id']+':p004:m0092'});self.assertEqual(sum(m['kind'] in ('person','pronoun')for m in oldids.values()),204);self.assertEqual(sum(m['kind'] in ('person','pronoun')for m in actual.values()),205)
  before=json.loads((ROOT/typed.EP).read_bytes());expected=ner.core.expand(before['expected_documents']['corpus/jinshu/031-jia-comparison-titles.json'],self.r)['holdings'];self.assertEqual(self.hs[:11],expected);self.assertEqual(len(self.hs),30)
  for key in ['age_assertions','age_difference_assertions']:self.assertEqual(self.ch['annotation'][key],ner.core.expand(before['annotation_additions'][key],self.r))
 def test_all_19_holdings_are_source_owned_and_undated(self):
  for h in self.hs[11:]:
   self.assertTrue(typed.holding_valid(h,self.ch,ROOT));self.assertTrue(all(h['effective_period'][end]['date_expression']is None and 'normalized_date'not in h['effective_period'][end]for end in ['start','end']))
 def test_transfer_requires_root_and_actual_chapter(self):
  for h in self.change_records():
   self.assertEqual(self.error(h),[]);self.assertTrue(self.error(h,root=False));self.assertTrue(self.error(h,chapters=None));self.assertTrue(self.error(h,chapters={'foreign':self.ch}))
 def test_wrong_previous_person_missing_or_unknown_previous(self):
  for h in self.change_records():
   pid=h['transfer_basis']['previous_holding_id'];rows=copy.deepcopy(self.by);rows[pid]['person_id']=self.r['huidi'];self.assertTrue(self.error(h,rows));rows=copy.deepcopy(self.by);rows.pop(pid);self.assertTrue(self.error(h,rows));bad=copy.deepcopy(h);bad['transfer_basis']['previous_holding_id']='missing';self.assertTrue(self.error(bad))
 def test_same_change_end_and_start_evidence_cannot_drift(self):
  for h in self.change_records():
   rows=copy.deepcopy(self.by);pid=h['transfer_basis']['previous_holding_id'];rows[pid]['effective_period']['end']['evidence'][0]['person_mention_id']=self.r['huidi'];self.assertTrue(self.error(h,rows));bad=copy.deepcopy(h);bad['effective_period']['start']['date_expression']='元康元年';self.assertTrue(self.error(bad));bad=copy.deepcopy(h);bad['effective_period']['start']['evidence'][0]['quote']='改封';self.assertTrue(self.error(bad))
 def test_unknown_kind_fake_owner_or_foreign_chapter_rejected(self):
  for h in self.change_records():
   bad=copy.deepcopy(h);bad['transfer_basis']['kind']='unknown';self.assertTrue(self.error(bad));bad=copy.deepcopy(h);bad['person_id']=self.r['huidi'];self.assertTrue(self.error(bad));bad=copy.deepcopy(h);bad['evidence'][0]['chapter_id']='foreign';self.assertTrue(self.error(bad))
 def test_same_person_wrong_span_or_extra_annotation_rejected(self):
  for h in self.change_records():
   for change in ['start','extra']:
    ms=copy.deepcopy(self.ms);mid=h['transfer_basis']['actor_mention_id']
    if change=='start':ms[mid][2]['start']+=1
    else:ms[mid][2]['extra_annotation']='not_actual_body'
    self.assertFalse(more.transfer_valid(h,self.by,self.ps,ms,self.chapters,ROOT))
 def test_suffixes_are_qualified_not_original_contiguous_names(self):
  for h in self.change_records()+[self.by['th-jin031-more-linhai-prior-qinghe']]:
   self.assertIn('shared_title_suffix',h);self.assertNotEqual(h['attestations'][0]['surface'],h['title']);bad=copy.deepcopy(h);bad['shared_title_suffix']['suffix_anchor']['surface']='王';self.assertFalse(typed.holding_valid(bad,self.ch,ROOT))
 def test_zhonghou_no_real_removal_and_group_not_people(self):
  h=self.by['th-jin031-more-chu-zhonghou'];self.assertEqual(h['title'],'中候');self.assertEqual(h['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]});self.assertIsNone(h['source_reading_qualification']['actual_outcome']);self.assertFalse(h['source_reading_qualification']['actual_removal_asserted'])
  group=ner.core.read(ROOT,more.proof(ROOT)['group_path']);self.assertEqual(group['source_reported_member_count'],3);self.assertEqual(group['individual_person_ids'],[]);self.assertEqual(group['status'],'pending_source_group_api_integration')
 def test_new_mid_caller_reverse_and_one_endpoint_cannot_be_faked(self):
  b,r,people=ner.source_context(ROOT);records=[ner.core.read(ROOT,rel)for rel in [ner.core.CH,ner.core.NS,ner.NSN,ner.core.AD,ner.IP]+list(typed.proof(ROOT)['expected_documents'])];ner.guard_bundle(ROOT,r['simawei'],people,records)
  bad=copy.deepcopy(people);mid=self.ch['id']+':p004:m0092';bad[r['simawei']]['evidence']=[e for e in bad[r['simawei']]['evidence']if e.get('mention_id')!=mid]
  with self.assertRaises(ValueError):ner.guard_bundle(ROOT,r['simawei'],bad,records)
  h=copy.deepcopy(self.by['th-jin031-more-chu-zhonghou']);h['person_id']=r['simaliang'];self.assertFalse(typed.holding_valid(h,self.ch,ROOT))
if __name__=='__main__':unittest.main(verbosity=2)
