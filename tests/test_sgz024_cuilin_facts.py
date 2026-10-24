from pathlib import Path
import unittest,json,copy
from scripts.fixed_kanripo_fact_slots import records,valid
ROOT=Path(__file__).resolve().parents[1]
class CuilinFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/sanguozhi/024-cuilin.json').read_bytes());cls.all_records=records(cls.ch,ROOT);batch=('shu-father-lin','sui-younger-brother-shu','wei-grandfather-lin','lin-younger-agnatic-cousin-yan','lin','shu','sui','wei','wangxiong','hun-father-xiong','yi-father-xiong','rong-father-hun','yan-father-yi','cheng-father-yi','lin-origin','lin-death','sui-death','lin-posthumous-name');cls.all=[a for a in cls.all_records if a['fixed_source_fact_binding']['slot']in batch];cls.by={a['id']:a for a in cls.all};cls.roles=[[m for m in p['mentions']if m['kind']=='person']for p in cls.ch['paragraphs']]
 def get(self,s):return next(a for a in self.all if a['fixed_source_fact_binding']['slot']==s)
 def test_total_eighteen_keeps_first_four(self):
  self.assertEqual(len(self.all),18);self.assertTrue(all(valid(a,self.ch,ROOT)for a in self.all_records));self.assertEqual(sum(a.get('predicate')=='father'for a in self.all),6)
 def test_lin_literal_name_and_zi(self):
  n=self.get('lin');self.assertEqual((n['surname'],n['ming'],n['zi']),('崔','林','徳儒'));self.assertEqual(n['person_id'],self.roles[0][0]['person_id']);self.assertEqual(n['courtesy_person_mention_id'],self.roles[0][1]['id'])
 def test_sui_surname_chain_does_not_create_father(self):
  n=self.get('sui');self.assertEqual(n['surname'],'崔');self.assertEqual(n['status'],'contextual_provisional');self.assertEqual(n['surname_basis']['steps'][-1]['predicate'],'brother');self.assertFalse(any(a.get('predicate')=='father'and a.get('subject_person_id')==n['person_id']for a in self.all))
 def test_wei_surname_keeps_missing_parent(self):
  self.assertEqual(self.get('wei')['surname_basis']['steps'][0]['predicate'],'grandfather');a=self.get('wei-grandfather-lin');self.assertIsNone(a['qualifiers']['parent_person_id']);self.assertEqual(a['qualifiers']['intermediate_person_ids'],[None])
 def test_wangxiong_full_name_seed_and_zi_thread(self):
  n=self.get('wangxiong');self.assertEqual((n['surname'],n['ming'],n['zi']),('王','雄','元伯'));self.assertEqual(n['source_full_name_seed']['person_id'],n['person_id']);self.assertEqual(n['source_full_name_seed']['person_mention_id'],self.roles[0][10]['id']);self.assertEqual(n['person_mention_id'],self.roles[1][0]['id'])
 def test_five_source_fathers_both_ends(self):
  for slot,child,parent in [('hun-father-xiong',23,22),('yi-father-xiong',24,22),('rong-father-hun',25,26),('yan-father-yi',27,29),('cheng-father-yi',28,29)]:
   a=self.get(slot);self.assertEqual(a['predicate'],'father');self.assertEqual(a['subject_person_id'],self.roles[1][child]['person_id']);self.assertEqual(a['object_person_id'],self.roles[1][parent]['person_id'])
 def test_second_son_two_no_first_born_invention(self):
  q=self.get('yi-father-xiong')['qualifiers']['birth_order'];self.assertEqual(q['ordinal'],2);self.assertEqual(q['scope'],'sons_of_parent');self.assertEqual(q['parent_person_id'],self.get('yi-father-xiong')['object_person_id']);self.assertNotIn('birth_order',self.get('hun-father-xiong')['qualifiers'])
 def test_lin_origin_not_birth_or_children_address(self):
  a=self.get('lin-origin');self.assertEqual(a['relation'],'biographical_origin');self.assertEqual(a['place']['source_name'],'清河東武城');self.assertEqual(a['person_id'],self.roles[0][0]['person_id']);self.assertIsNone(a['place']['modern_identification'])
 def test_death_year_244_with_chinese_source_and_official_era(self):
  a=self.get('lin-death');d=a['normalized_date'];self.assertEqual(a['date_expression'],'正始五年');self.assertEqual(d['year'],244);self.assertEqual(d['calendar'],'chinese_civil');self.assertEqual(d['source_expression'],'正始五年');m=d['regnal_year_mapping'];self.assertEqual((m['start_ce_year'],m['regnal_year'],m['end_ce_year']),(240,5,249));self.assertNotIn('birth_year',a);self.assertNotIn('age',a)
 def test_sui_death_not_lun_301_or_wangjing_zu(self):
  a=self.get('sui-death');self.assertEqual(a['person_id'],self.roles[9][5]['person_id']);self.assertIsNone(a['date_expression']);self.assertNotIn('normalized_date',a);an=a['source_anchor'];p=self.ch['paragraphs'][9]['text'];self.assertEqual(p[an['start']-3:an['end']],'廢錮而卒');self.assertNotEqual(a['person_id'],self.roles[9][9]['person_id'])
 def test_posthumous_title_not_given_to_son_or_dated_244(self):
  a=self.get('lin-posthumous-name');self.assertEqual(a['title'],'孝侯');self.assertEqual(a['person_id'],self.roles[8][1]['person_id']);self.assertNotEqual(a['person_id'],self.roles[8][3]['person_id']);self.assertIsNone(a['effective_period']['start']['date_expression']);self.assertNotIn('normalized_date',a['effective_period']['start']);self.assertEqual(a['effective_period']['end']['status'],'unknown')
 def test_wrong_name_courtesy_and_surname_step_rejected(self):
  for slot in('lin','shu','sui','wei','wangxiong'):
   a=copy.deepcopy(self.get(slot));a['surname']='王'if a['surname']=='崔'else'崔';self.assertFalse(valid(a,self.ch,ROOT))
  a=copy.deepcopy(self.get('wangxiong'));a['courtesy_person_mention_id']=self.roles[0][1]['id'];self.assertFalse(valid(a,self.ch,ROOT))
 def test_surname_route_cannot_choose_father_for_sui_or_wei(self):
  a=copy.deepcopy(self.get('sui'));a['surname_basis']['steps'][-1]['predicate']='father';self.assertFalse(valid(a,self.ch,ROOT));a=copy.deepcopy(self.get('wei'));a['surname_basis']['steps'][0]['to_person_id']=self.roles[9][0]['person_id'];self.assertFalse(valid(a,self.ch,ROOT))
 def test_life_wrong_person_with_consistent_mention_rejected(self):
  for slot,role in [('lin-death',(8,0)),('sui-death',(9,9))]:
   a=copy.deepcopy(self.get(slot));i,j=role;a['person_id']=self.roles[i][j]['person_id'];a['evidence'][0]['person_mention_id']=self.roles[i][j]['id']
   if'normalized_date'in a:a['normalized_date']['evidence'][0]['person_mention_id']=self.roles[i][j]['id']
   self.assertFalse(valid(a,self.ch,ROOT))
 def test_father_wrong_both_ends_and_evidence_rejected(self):
  a=copy.deepcopy(self.get('yan-father-yi'));x,y=self.roles[1][0],self.roles[1][2];a['subject_person_id'],a['object_person_id']=x['person_id'],y['person_id'];a['evidence'][0].update(subject_person_mention_id=x['id'],object_person_mention_id=y['id']);self.assertFalse(valid(a,self.ch,ROOT))
 def test_wrong_ordinal_and_year_rejected(self):
  a=copy.deepcopy(self.get('yi-father-xiong'));a['qualifiers']['birth_order']['ordinal']=1;self.assertFalse(valid(a,self.ch,ROOT));a=copy.deepcopy(self.get('lin-death'));a['normalized_date']['year']=245;self.assertFalse(valid(a,self.ch,ROOT))
 def test_wrong_title_person_with_all_attestations_rejected(self):
  a=copy.deepcopy(self.get('lin-posthumous-name'));pid=self.roles[8][3]['person_id'];mid=self.roles[8][3]['id'];a['person_id']=pid
  for e in a['evidence']+a['effective_period']['start']['evidence']+a['naming_basis']['evidence']:e['person_mention_id']=mid
  a['attestations'][0]['person_mention_id']=mid;self.assertFalse(valid(a,self.ch,ROOT))
 def test_source_no_new_unknown_child_or_wangjing_address(self):
  self.assertFalse(any(a.get('relation')for a in self.all if a.get('person_id')==self.roles[9][9]['person_id']));self.assertFalse(any(a.get('subject_person_id')==self.roles[8][2]['person_id']for a in self.all))
if __name__=='__main__':unittest.main()
