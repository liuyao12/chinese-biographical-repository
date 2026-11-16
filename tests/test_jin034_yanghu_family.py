import unittest,json,copy
from pathlib import Path
from scripts.fixed_witness_fact_slots import records,valid,errors
ROOT=Path(__file__).resolve().parents[1]
class YanghuFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/034-yanghu.json').read_bytes());cls.allrows=records(cls.ch,ROOT);cls.rows=[v for v in cls.allrows if v['fixed_source_fact_binding']['slot'].startswith(('kin_','detail_'))];cls.by={v['fixed_source_fact_binding']['slot']:v for v in cls.rows}
 def reject(self,k,fn):
  v=copy.deepcopy(self.by[k]);fn(v);self.assertFalse(valid(v,self.ch,ROOT))
 def test_complete37_exact_source_bound_slots(self):
  self.assertEqual(len(self.rows),37);self.assertEqual(set(self.by),{'kin_'+str(n).zfill(3) for n in range(1,32)}|{'detail_'+str(n).zfill(3) for n in range(1,7)});self.assertTrue(all(valid(v,self.ch,ROOT) for v in self.allrows));self.assertEqual(len(self.ch['paragraphs']),41);self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),6567)
  for v in self.rows:self.assertTrue(valid(v,self.ch,ROOT),v['id'])
 def test_father_and_two_ancestries_not_missing_father(self):
  self.assertEqual(self.by['kin_001']['predicate'],'father');self.assertEqual(self.by['kin_002']['predicate'],'grandfather');self.assertEqual(self.by['kin_003']['qualifiers']['lineage'],'maternal')
  self.reject('kin_002',lambda v:v.update(predicate='father'))
 def test_elder_queen_and_older_brothers(self):
  for k in ['kin_004','kin_009','kin_013']:self.assertEqual(self.by[k]['qualifiers']['relative_age'],'younger')
  self.assertEqual(self.by['kin_006']['qualifiers']['relative_age'],'older');self.reject('kin_004',lambda v:v['qualifiers'].update(relative_age='older'))
 def test_wifes_father_is_ba_not_wei(self):
  self.assertEqual(self.by['kin_007']['object_person_id'],self.by['kin_006']['subject_person_id']);self.assertNotEqual(self.by['kin_007']['object_person_id'],self.by['kin_006']['object_person_id'])
  self.reject('kin_007',lambda v:v.update(object_person_id=self.by['kin_006']['object_person_id']))
 def test_prior_birth_and_care_mothers_remain_distinct(self):
  self.assertEqual(self.by['kin_010']['predicate'],'maternal_role');self.assertEqual(self.by['kin_010']['qualifiers']['role'],'prior_mother');self.assertEqual(self.by['kin_012']['object_person_id'],self.by['kin_010']['object_person_id']);self.assertNotEqual(self.by['kin_012']['object_person_id'],self.by['kin_014']['object_person_id']);self.assertEqual(self.by['kin_016']['predicate'],'raised_by');self.assertEqual(self.by['kin_016']['object_person_id'],self.by['kin_014']['object_person_id'])
  self.assertEqual(self.by['kin_014']['qualifiers']['maternal_interpretation']['status'],'contextual_preferred');self.reject('kin_016',lambda v:v.update(predicate='mother'))
 def test_eldest_son_one_but_other_brothers_no_ranks(self):
  b=self.by['kin_017']['qualifiers']['birth_order'];self.assertEqual((b['ordinal'],b['scope']),(1,'sons_of_parent'))
  for k in ['kin_018','kin_019','kin_020']:self.assertIsNone(self.by[k]['qualifiers']['relative_birth_order']['younger_ordinal'])
  self.reject('kin_018',lambda v:v['qualifiers']['relative_birth_order'].update(younger_ordinal=2))
 def test_faxing_five_generations_below_unknown_brother(self):
  q=self.by['kin_029']['qualifiers'];self.assertEqual(q['object_generation_relative_to_subject'],-5);self.assertEqual([x['generation_distance']for x in q['source_generation_steps']],[4,1]);self.assertIsNone(q['unnamed_ancestor_role']['person_id']);self.assertIsNone(q['connecting_person_ids'])
  for n in [-4,5,False]:self.reject('kin_029',lambda v,n=n:v['qualifiers'].update(object_generation_relative_to_subject=n))
  self.reject('kin_029',lambda v:v['qualifiers']['unnamed_ancestor_role'].update(person_id=self.by['kin_009']['object_person_id']))
 def test_distant_cousin_has_no_invented_common_ancestor(self):
  q=self.by['kin_025']['qualifiers']['kinship_structure'];self.assertIsNone(q['distance']);self.assertIsNone(q['common_ancestor_person_id']);self.assertEqual(q['generation_difference'],0)
  self.reject('kin_025',lambda v:v['qualifiers']['kinship_structure'].update(common_ancestor_person_id=self.by['kin_001']['object_person_id']))
 def test_ritual_successor_not_biological_or_adopted_father(self):
  self.assertEqual(self.by['kin_030']['predicate'],'ritual_successor_of');self.assertEqual(self.by['kin_030']['qualifiers']['legal_adoption_status'],'not_stated');self.reject('kin_030',lambda v:v.update(predicate='father'))
 def test_unnamed_soninlaw_no_manufactured_daughter(self):
  a=self.by['kin_031'];self.assertEqual(a['predicate'],'father_in_law');self.assertEqual(a['object_person_id'],self.by['kin_001']['subject_person_id']);self.assertIsNone(a['qualifiers']['spouse_person_id']);self.assertIsNone(a['qualifiers']['child_person_id'])
  def swap(v):
   v['subject_person_id'],v['object_person_id']=v['object_person_id'],v['subject_person_id']
   for e in v['evidence']:e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
  self.reject('kin_031',swap)
 def test_no_missing_or_duplicate_bound_record(self):
  self.assertFalse(errors(ROOT,[self.ch,dict(chapter_id=self.ch['id'],records=[v for v in self.allrows if v not in self.ch['annotation'].get('age_assertions',[])])]))
  for rs in [[v for v in self.allrows[1:] if v not in self.ch['annotation'].get('age_assertions',[])],[v for v in self.allrows if v not in self.ch['annotation'].get('age_assertions',[])]+[self.rows[0]]]:self.assertTrue(errors(ROOT,[self.ch,dict(chapter_id=self.ch['id'],records=rs)]))
if __name__=='__main__':unittest.main()

class TrueCliNegative(unittest.TestCase):
 def test_coherent_soninlaw_reversal_rejected_by_real_main(self):
  import subprocess,sys
  code='''from pathlib import Path
import json,runpy,sys
from unittest.mock import patch
root=Path(sys.argv[1]);target=root/'corpus/jinshu/034-yanghu-assertions.json';old=Path.read_text;data=json.loads(old(target));v=next(a for a in data['assertions']if a['id']=='a-jin034-yanghu-unnamed-soninlaw');v['subject_person_id'],v['object_person_id']=v['object_person_id'],v['subject_person_id']
for e in v['evidence']:e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
def read(p,*a,**kw):return json.dumps(data,ensure_ascii=False)if p==target else old(p,*a,**kw)
sys.path.insert(0,str(root/'scripts'));sys.path.insert(0,str(root))
with patch.object(Path,'read_text',read):runpy.run_path(str(root/'scripts/validate_corpus.py'),run_name='__main__')
'''
  p=subprocess.run([sys.executable,'-c',code,str(ROOT)],capture_output=True,text=True)
  self.assertEqual(p.returncode,1,p.stdout+p.stderr);self.assertIn('固定',p.stderr)

class SourceReportQualifications(YanghuFamily):
 def test_rejected_proposals_are_not_executed_adoptions(self):
  for k in ['detail_001','detail_002']:
   v=self.by[k]['values'];self.assertEqual(v['proposal_status'],'not_accepted');self.assertIs(v['actual_adoption_attested'],False);self.reject(k,lambda x:x['values'].update(actual_adoption_attested=True))
 def test_children_speech_and_two_heir_reports_do_not_count_all_children(self):
  for k in ['detail_003','detail_004','detail_005']:
   self.assertIsNone(self.by[k]['values']['individual_count']);self.assertIs(self.by[k]['values']['biological_children_only'],False);self.reject(k,lambda x:x['values'].update(individual_count=0))
  self.assertIn('miraculous',self.by['detail_005']['values']['scope'])
 def test_nine_generations_report_is_not_synthetic_ancestry(self):
  v=self.by['detail_006']['values'];self.assertEqual(v['reported_generations'],9);self.assertIsNone(v['named_ancestor_chain'])
  self.reject('detail_006',lambda x:x['values'].update(named_ancestor_chain=[self.by['kin_001']['object_person_id']]))
