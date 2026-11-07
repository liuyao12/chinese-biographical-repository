from tests.portable_fixture_copy import fixture_copy2
import copy,json,shutil,tempfile,unittest
from pathlib import Path
from scripts.pei_work_authorities import validate,PATH
from scripts.work_provenance import validate as metadata_validate
R=Path(__file__).resolve().parents[1]
class PeiWorkAuthorityTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'registry').mkdir();shutil.copyfile(R/'registry/works.json',self.root/'registry/works.json');shutil.copytree(R/'source-evidence/pei-work-authorities',self.root/'source-evidence/pei-work-authorities', copy_function=fixture_copy2);self.data=json.loads((R/'registry/work-provenance.json').read_text());self.p=json.loads((self.root/PATH).read_text())
 def tearDown(self):self.tmp.cleanup()
 def save(self): (self.root/PATH).write_text(json.dumps(self.p,ensure_ascii=False,indent=2)+'\n')
 def test_all_archives_and_exact_spans_positive(self):self.assertEqual(8,len(self.p['archives']));self.assertEqual(11,len(self.p['evidence']));self.assertTrue(validate(self.data,self.root))
 def test_whole_metadata_model_positive(self):metadata_validate(json.loads((R/'registry/work-provenance.json').read_text()),R)
 def test_shifted_exact_span_rejected(self):self.p['evidence'][0]['raw_start']+=1;self.save();self.assertRaises(AssertionError,validate,self.data,self.root)
 def test_unused_archive_also_checked(self):
  a=next(a for a in self.p['archives']if 'sgz027' in a['raw_path']);f=self.root/a['raw_path'];f.write_bytes(f.read_bytes()+b'\n');self.assertRaises(AssertionError,validate,self.data,self.root)
 def test_coherent_wrong_author_not_supported_by_catalogue(self):
  a=self.p['authorities'][0];a['author']='王沈';self.save();rows=json.loads((self.root/'registry/works.json').read_text());next(w for w in rows['works']if w['id']==a['work_id'])['author']='王沈';(self.root/'registry/works.json').write_text(json.dumps(rows));self.data['works'][a['work_id']]['author']='王沈';self.assertRaises(AssertionError,validate,self.data,self.root)
 def test_generic_shortname_cannot_replace_received_full_title(self):
  a=self.p['authorities'][1];a['catalogue_attestations'][0]['title_as_received']='世語';a['citation_title']='世語';self.save();rows=json.loads((self.root/'registry/works.json').read_text());next(w for w in rows['works']if w['id']==a['work_id'])['citation_title']='世語';(self.root/'registry/works.json').write_text(json.dumps(rows));self.data['works'][a['work_id']]['citation_title']='世語';self.assertRaises(AssertionError,validate,self.data,self.root)
 def test_catalogue_volume_variants_not_harmonized(self):self.p['authorities'][0]['catalogue_attestations'][0]['volumes']=50;self.p['authorities'][0]['catalogue_attestations'][0]['source_number']='五十';self.save();self.assertRaises(AssertionError,validate,self.data,self.root)
 def test_unresolved_reference_rejected(self):self.data['references'].pop('ref-pei-authority-'+self.p['evidence'][0]['id']);self.assertRaises(KeyError,validate,self.data,self.root)
 def test_numeric_completion_not_inferred_from_author_period(self):self.data['works'][self.p['authorities'][0]['work_id']]['composition']={'status':'reported','assertions':[{'date':{'start_year':239}}]};self.assertRaises(AssertionError,validate,self.data,self.root)
 def test_metadata_intermediate_symlink_rejected(self):
  a=self.p['archives'][0];outside=Path(self.tmp.name+'-external');outside.mkdir();self.addCleanup(shutil.rmtree,outside);f=self.root/a['metadata_path'];shutil.copyfile(f,outside/f.name);link=self.root/'source-evidence/pei-work-authorities/escaped';link.symlink_to(outside,target_is_directory=True);a['metadata_path']='source-evidence/pei-work-authorities/escaped/'+f.name;self.save();self.assertRaises(AssertionError,validate,self.data,self.root)
if __name__=='__main__':unittest.main()
