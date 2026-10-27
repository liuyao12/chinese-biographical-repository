import copy,json,tempfile,unittest
from pathlib import Path
from scripts.formal_source_citations import citation_index,source_caption,load_citation_index
class FormalCitationTests(unittest.TestCase):
 def setUp(self):
  self.r={'works':[{'id':'w-jinshu','title':'晉書','books':[{'id':'b-jinshu-079','work_id':'w-jinshu','title':'卷七十九'}]}]}
  self.d={'schema_version':1,'works':[{'work_id':'w-jinshu','title':'晉書','books':[{'book_id':'b-jinshu-079','title':'卷七十九','citation_title':'謝尚 謝安'}]}]}
  self.c={'work_id':'w-jinshu','book_id':'b-jinshu-079','title':'謝氏家族選段及完整單元（編輯選錄題）','source':{'title':'數位底本研究題'},'scope':'partial'}
 def test_exact_formal_title_preserves_raw_record(self):
  before=copy.deepcopy(self.c);self.assertEqual(source_caption(self.c,citation_index(self.r,self.d)),'《晉書・謝尚 謝安》');self.assertEqual(self.c,before)
 def test_ordinal_or_words_inside_real_title_not_trimmed(self):
  self.d['works'][0]['books'][0]['citation_title']='七略第一 完整單元';self.assertEqual(source_caption(self.c,citation_index(self.r,self.d)),'《晉書・七略第一 完整單元》')
 def test_exact_book_not_selection_or_nearest(self):
  idx=citation_index(self.r,self.d)
  for patch in [{'work_id':'w-other'},{'book_id':'b-jinshu-091'},{'book_id':None}]:
   with self.assertRaises(ValueError):source_caption(dict(self.c,**patch),idx)
 def test_missing_directory_book_rejected(self):
  self.d['works'][0]['books']=[]
  with self.assertRaises(ValueError):source_caption(self.c,citation_index(self.r,self.d))
 def test_registry_only_work_uses_registered_book(self):
  self.d['works']=[];self.assertEqual(source_caption(self.c,citation_index(self.r,self.d)),'《晉書・卷七十九》')
 def test_blank_citation_uses_formal_book_title(self):
  self.d['works'][0]['books'][0]['citation_title']='';self.assertEqual(source_caption(self.c,citation_index(self.r,self.d)),'《晉書・卷七十九》')
 def test_duplicate_and_wrong_membership_fail_closed(self):
  for kind in ['work','book','membership','title']:
   r=copy.deepcopy(self.r);d=copy.deepcopy(self.d)
   if kind=='work':d['works'].append(copy.deepcopy(d['works'][0]))
   if kind=='book':d['works'][0]['books'].append(copy.deepcopy(d['works'][0]['books'][0]))
   if kind=='membership':r['works'][0]['books'][0]['work_id']='w-other'
   if kind=='title':d['works'][0]['books'][0]['citation_title']=[]
   with self.assertRaises(ValueError):citation_index(r,d)
 def test_load_native_files(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);(root/'registry').mkdir();(root/'data/corpus').mkdir(parents=True)
   (root/'registry/works.json').write_text(json.dumps(self.r));(root/'data/corpus/chapter-directory.json').write_text(json.dumps(self.d))
   self.assertEqual(source_caption(self.c,load_citation_index(root)),'《晉書・謝尚 謝安》')
 def test_actual_exporter_source_column_and_reference_definition(self):
  from unittest.mock import patch
  from scripts import export_person_bundles as exporter
  record=dict(self.c,record_type='marked_chapter',source_id='s-test',source={'url':'https://example.test/fixed'})
  person={'label':'謝安'};pid='abc_def_123'
  result={'identity_policy':{},'person_ids':[pid],'family_tree_decisions':[]}
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);(root/'registry').mkdir();(root/'data/corpus').mkdir(parents=True)
   (root/'registry/works.json').write_text(json.dumps(self.r));(root/'data/corpus/chapter-directory.json').write_text(json.dumps(self.d))
   before=copy.deepcopy(record)
   with patch.object(exporter,'load_catalog',return_value=({pid:person},[record])),patch.object(exporter,'bundle',return_value=result),patch.object(exporter,'load_assemblies',return_value=({},{})),patch.object(exporter,'index_counts',return_value={'most_mentioned_source_ids':['s-test']}),patch('scripts.calendar_wiring.export_calendar_contexts'):
    exporter.export(root)
   md=(root/'exports/persons/unconnected.md').read_text()
   self.assertIn('[《晉書・謝尚 謝安》][1]',md);self.assertIn('[1]: https://example.test/fixed',md)
   self.assertNotIn('編輯選錄題',md);self.assertEqual(record,before)
   self.assertEqual(json.loads((root/'exports/persons'/ (pid+'.json')).read_text()),result)
if __name__=='__main__':unittest.main()
