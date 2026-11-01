"""Regression checks at the finite source consumer's actual bundle boundary."""
import copy,json,unittest
from pathlib import Path
from scripts import jin038_wen_children_source as source
ROOT=Path(__file__).resolve().parents[1]
def replace_endpoint(value,old,new):
 if type(value)is str:return new if value==old else value
 if type(value)is list:return[replace_endpoint(v,old,new)for v in value]
 if type(value)is dict:return{k:replace_endpoint(v,old,new)for k,v in value.items()}
 return value
class Jin038ChildrenGuardBoundary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=ROOT;cls.c,cls.roles,cls.docs=source.proof(ROOT);cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']};cls.records=list(cls.docs.values());cls.owners={m['person_id']for d in cls.records for p in d.get('paragraphs',[])for m in p.get('mentions',[])if m.get('person_id')};cls.outside=next(p for p in cls.people if p not in cls.owners)
 def test_real_source_owner_positive(self):
  self.assertIsNone(source.guard_bundle(self.root,self.roles['bing'],self.people,self.records))
 def test_moved_whole_source_actor_query_new_owner_rejected(self):
  records=replace_endpoint(self.records,self.roles['bing'],self.outside)
  with self.assertRaises(ValueError):source.guard_bundle(self.root,self.outside,self.people,records)
 def test_moved_name_only_query_new_owner_rejected(self):
  records=copy.deepcopy(self.records)
  for d in records:
   if d.get('record_type')=='person_name_component_set':
    for n in d['records']:
     if n['person_id']==self.roles['jian']:n['person_id']=self.outside
  with self.assertRaises(ValueError):source.guard_bundle(self.root,self.outside,self.people,records)
 def test_reverse_only_new_owner_and_missing_source_records_rejected(self):
  people=copy.deepcopy(self.people);people[self.outside]['evidence']+=copy.deepcopy([e for e in people[self.roles['bing']]['evidence']if e.get('chapter_id')==self.c['chapter_id']])
  with self.assertRaises(ValueError):source.guard_bundle(self.root,self.outside,people,[])
 def test_original_owner_reverse_and_names_loss_rejected(self):
  people=copy.deepcopy(self.people);pid=self.roles['jian'];people[pid]['evidence']=[];records=[d for d in self.records if d.get('record_type')!='person_name_component_set']
  with self.assertRaises(ValueError):source.guard_bundle(self.root,pid,people,records)
 def test_extra_owned_record_and_bool_type_mutation_rejected(self):
  records=copy.deepcopy(self.records);chapter=next(d for d in records if d.get('record_type')=='marked_chapter');chapter['paragraphs'][0]['mentions'][0]['start']=False
  with self.assertRaises(ValueError):source.guard_bundle(self.root,self.roles['jing_senior'],self.people,records)
 def test_genuine_unrelated_request_unchanged(self):
  self.assertIsNone(source.guard_bundle(self.root,self.outside,self.people,self.records))
 def test_unrelated_malformed_nested_marker_is_not_new_entry_exception(self):
  records=self.records+[{'id':'unrelated-test-record','paragraphs':[{'mentions':[{'id':[],'person_id':self.outside}]}]}]
  self.assertIsNone(source.guard_bundle(self.root,self.outside,self.people,records))
if __name__=='__main__':unittest.main()
