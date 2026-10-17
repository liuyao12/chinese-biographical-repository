# coding:utf-8
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.validate_corpus import validate
from scripts.table_evidence import load_tables,table_evidence_errors,table_family_path_errors
from scripts.person_bundle import bundle
R=Path(__file__).resolve().parents[1];CHI='yqp_nlb_p1p_ABFAC';JOY='yqp_nlb_p1p_ABFA';FU='yqp_nlb_p1p_ABFAB'
def load(f):return json.loads((R/f).read_text())
class CrossCellChengyangFather(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(R);cls.assertions=load('corpus/shiji/021-assertions.json')['assertions'];cls.a=cls.assertions[0];cls.e=cls.a['evidence'][0];cls.person=next(p for p in load('registry/persons.json')['persons']if p['id']==CHI)
 def bad(self,e,ts=None,predicate='father',subject=CHI,parent=JOY):self.assertTrue(table_evidence_errors(e,ts or self.tables,subject,parent,predicate))
 def test_two_original_rows_explicitly_name_the_same_father(self):
  for a in self.assertions:
   e=a['evidence'][0];self.assertEqual(a['object_person_id'],JOY);self.assertEqual(table_evidence_errors(e,self.tables,a['subject_person_id'],JOY,'father'),[]);self.assertEqual(e['quote'],'城陽共王子。');self.assertIn('侯劉'+('齒'if a['subject_person_id']==CHI else'福')+'元年',e['subject_quote']);self.assertNotIn('paragraph_id',e)
 def test_cross_row_subject_cannot_borrow_another_sons_parent_cell(self):self.bad(dict(self.e,subject_table_cell_id='shiji-021-t1-r099-c03'))
 def test_cross_cell_model_cannot_reverse_parent_or_use_grandfather(self):self.bad(self.e,subject=JOY,parent=CHI);self.bad(self.e,predicate='grandfather')
 def test_fixed_source_revision_and_both_full_cell_quotes_are_required(self):
  for k,v in [('source_revision','0'),('quote','共王子'),('subject_quote','劉齒'),('chapter_id','c-shiji-114-dongyue'),('relationship_layout','any_cells')]:self.bad(dict(self.e,**{k:v}))
 def test_missing_or_other_person_anchor_cannot_establish_father(self):
  for k in ['subject_mention_id','object_mention_id']:self.bad(dict(self.e,**{k:'missing'}))
 def test_earlier_nonempty_holder_column_rejects_successor(self):
  ts=copy.deepcopy(self.tables);c=next(c for f in ts['shiji-021']['fragments']for r in f['rows']for c in r['cells']if c['id']=='shiji-021-t1-r098-c02');c['text']='synthetic prior holder';self.bad(self.e,ts)
 def test_grandson_label_is_not_a_father_assertion(self):
  ts=copy.deepcopy(self.tables);c=next(c for f in ts['shiji-021']['fragments']for r in f['rows']for c in r['cells']if c['id']==self.e['table_cell_id']);c['text']='城陽共王孫。';self.bad(dict(self.e,quote=c['text']),ts)
 def test_same_cell_later_holder_is_not_the_original_kings_son(self):
  ts=copy.deepcopy(self.tables);c=next(c for f in ts['shiji-021']['fragments']for r in f['rows']for c in r['cells']if c['id']==self.e['subject_table_cell_id']);prefix='侯甲元年。';c['text']=prefix+c['text']
  for m in c['person_mentions']:m['start']+=len(prefix);m['end']+=len(prefix)
  self.bad(dict(self.e,subject_quote=c['text']),ts)
 def test_offspan_parent_label_is_rejected(self):
  ts=copy.deepcopy(self.tables);c=next(c for f in ts['shiji-021']['fragments']for r in f['rows']for c in r['cells']if c['id']==self.e['table_cell_id']);c['person_mentions'][0]['end']+=1;self.bad(self.e,ts)
 def test_family_path_binds_the_exact_same_assertion_and_endpoints(self):
  p=self.person['family_path'];self.assertEqual(table_family_path_errors(CHI,p,self.tables,self.assertions),[])
  for k,v in [('source_assertion_id','missing'),('parent_person_id',FU),('connection','grandfather')]:self.assertTrue(table_family_path_errors(CHI,dict(p,**{k:v}),self.tables,self.assertions))
 def test_family_path_cannot_replace_child_source_cell(self):
  p=copy.deepcopy(self.person['family_path']);p['evidence'][0]['subject_table_cell_id']='shiji-021-t1-r099-c03';self.assertTrue(table_family_path_errors(CHI,p,self.tables,self.assertions))
 def test_bundle_includes_both_cells_without_joining_them_into_prose(self):
  b=bundle(CHI,R);cells={c['id']:c for c in b['table_passages']};self.assertEqual(cells[self.e['table_cell_id']]['text'],self.e['quote']);self.assertEqual(cells[self.e['subject_table_cell_id']]['text'],self.e['subject_quote']);self.assertFalse(any(p['text']==self.e['quote']+self.e['subject_quote']for p in b['passages']))
 def test_new_family_path_does_not_invent_order_mother_or_shared_mother(self):
  p=self.person['family_path'];self.assertEqual((p['parent_person_id'],p['generation_distance']),(JOY,1));self.assertTrue(CHI.startswith(JOY));self.assertNotIn('birth_order',p);a=self.a;self.assertNotIn('birth_order',a['qualifiers']);self.assertNotIn('shared_mother',a['qualifiers']);self.assertFalse(any(a['predicate']=='mother'for a in bundle(CHI,R)['relations']))
 def test_old_id_is_absent_from_registry_and_all_editable_json(self):
  self.assertNotIn('v3b_rv7_5cd',{p['id']for p in load('registry/persons.json')['persons']})
  for directory,pattern in [('corpus','*/*.json'),('registry','*.json'),('data/historical-tables','*.json')]:
   for p in (R/directory).glob(pattern):self.assertNotIn('v3b_rv7_5cd',p.read_text(),str(p))
 def test_native_and_prose_father_evidence_is_independent_of_file_order(self):
  original=Path.glob
  for reverse in [False,True]:
   def ordered(path,pattern):return iter(sorted(original(path,pattern),key=str,reverse=reverse))
   with patch.object(Path,'glob',ordered):self.assertEqual(validate(R),[],reverse)
if __name__=='__main__':unittest.main()
