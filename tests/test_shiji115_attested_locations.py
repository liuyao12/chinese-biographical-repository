from tests.portable_fixture_copy import fixture_copy2
import copy,json,shutil,tempfile,unittest
from pathlib import Path
from scripts.validate_corpus import validate
from scripts.person_bundle import bundle
R=Path(__file__).resolve().parents[1]
def _copy_source_fixture(root):
    for name in ('registry','corpus','source-evidence','sources','scripts','docs','schema','data/historical-tables'):
        (root/name).parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(R/name,root/name, copy_function=fixture_copy2)
    (root/'data/corpus').mkdir(parents=True,exist_ok=True)
    for name in ('profile-names.json','chapter-directory.json'):
        shutil.copy2(R/'data/corpus'/name,root/'data/corpus'/name)
    # Preserve the declared immutable capture required by the Pei source proof.
    capture='tests/fixtures/occurrence-concordance/original-anchors.json'
    (root/capture).parent.mkdir(parents=True,exist_ok=True)
    fixture_copy2(R/capture,root/capture)

class ChaoxianAttestedLocations(unittest.TestCase):
 def test_unmodified_source_fixture_has_no_errors(self):
  with tempfile.TemporaryDirectory()as temp:
   root=Path(temp);_copy_source_fixture(root);self.assertEqual(validate(root),[])
 def test_origin_residence_and_capital_are_distinct_sourced_relations(self):
  a=json.loads((R/'corpus/shiji/115-addresses.json').read_text())['assertions']
  self.assertEqual([(x['relation'],x['place']['source_name'])for x in a],[('biographical_origin','燕'),('residence','上下鄣'),('capital_location','王險')])
  for x in a:
   self.assertIsNone(x['date_expression']);self.assertIsNone(x['place']['modern_identification']);self.assertTrue(all(x['source_term']in e['quote']for e in x['evidence']))
 def test_person_bundle_keeps_capital_separate_from_individual_residence(self):
  a=bundle('f41_ulg_3u1',R)['address_assertions'];capital=next(x for x in a if x['relation']=='capital_location');self.assertEqual(capital['source_term'],'都王險');self.assertEqual(capital['qualifiers'],{'seat_kind':'royal_capital','source_action':'都'});self.assertFalse(any(x['relation']=='residence'and x['place']['source_name']=='王險'for x in a))
 def test_capital_without_attested_action_or_with_residence_scope_is_rejected(self):
  with tempfile.TemporaryDirectory()as temp:
   root=Path(temp)
   _copy_source_fixture(root)
   p=root/'corpus/shiji/115-addresses.json';d=json.loads(p.read_text());d['assertions'][2]['qualifiers']['seat_kind']='individual_residence';p.write_text(json.dumps(d,ensure_ascii=False));self.assertIn('王都須有都與原地名，不得當籍貫或個人居所',validate(root))
if __name__=='__main__':unittest.main()
