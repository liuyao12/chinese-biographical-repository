"""Actual source strata and the two direct paternal ID paths, without new ancestry."""
import copy,json,unittest
from pathlib import Path
from scripts.fixed_nanqi047_source import errors
from scripts.houhan_text_layers import layer_errors
from scripts.person_ids import family_path_errors
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
class SourceLayerPaths(unittest.TestCase):
 def test_qing_is_qualified_independent_appendix(self):
  c=read('corpus/nanqishu/047-qing-collation.json');p=c['paragraphs'][0]
  self.assertEqual(p['text_layer'],'witness_appended_qing_siku_collation');self.assertEqual(errors(c,R),[]);self.assertEqual(layer_errors(p),[])
  for key,value in [('period','南齊'),('image_verified',True),('scope','received_biography')]:
   bad=copy.deepcopy(p);bad['layer_attribution'][key]=value;self.assertTrue(layer_errors(bad))
 def test_appraisal_and_praise_cannot_be_mixed(self):
  c=read('corpus/nanqishu/047-compiler-appraisal.json');self.assertEqual(errors(c,R),[])
  self.assertEqual([p['text_layer']for p in c['paragraphs']],['received_compiler_appraisal','received_compiler_praise'])
  for i in range(2):
   bad=copy.deepcopy(c);bad['paragraphs'][i]['text_layer']='received_chapter';self.assertTrue(errors(bad,R))
 def test_two_paths_are_existing_explicit_fathers(self):
  people={p['id']:p for p in read('registry/persons.json')['persons']};assertions=read('corpus/nanqishu/047-xietiao-assertions.json')['assertions']
  for aid in ['a-nanqi047-xietiao-father','a-nanqi047-wife-father']:
   a=next(a for a in assertions if a['id']==aid);person=people[a['subject_person_id']];p=person['family_path'];self.assertEqual(p['parent_person_id'],a['object_person_id']);self.assertEqual(p['source_assertion_id'],aid);self.assertEqual(p['evidence'],a['evidence']);self.assertEqual(family_path_errors(person['id'],p),[]);self.assertIs(p['human_reviewed'],False)
   bad=copy.deepcopy(p);bad['generation_distance']=2;self.assertTrue(family_path_errors(person['id'],bad))
if __name__=='__main__':unittest.main()
