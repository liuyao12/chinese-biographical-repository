import unittest,copy,json
from pathlib import Path
from scripts.profile_title_preferences import PreferenceCatalog,choice
from scripts.person_bundle import load_catalog,bundle
try:from tests.test_profile_title_preferences import fixture
except ImportError:from test_profile_title_preferences import fixture
ROOT=Path(__file__).resolve().parents[1]
class CatalogCopies(unittest.TestCase):
 def test_shallow_copy_is_editable_list_without_index(self):
  rows,people,h,d,c=fixture();tx=PreferenceCatalog(rows,people,ROOT);other=copy.copy(tx);self.assertIs(type(other),list);self.assertFalse(hasattr(other,'_profile_title_index'));other.append({'record_type':'synthetic_extra'});self.assertEqual(choice(other,people,h['person_id'],ROOT),choice(tx,people,h['person_id'],ROOT))
 def test_deepcopy_loses_index_and_keeps_independent_rows(self):
  rows,people,h,d,c=fixture();tx=PreferenceCatalog(rows,people,ROOT);other=copy.deepcopy(tx);self.assertIs(type(other),list);self.assertFalse(hasattr(other,'_profile_title_index'));self.assertIsNot(other[0],tx[0]);self.assertEqual(choice(other,people,h['person_id'],ROOT),choice(tx,people,h['person_id'],ROOT))
 def test_edited_deepcopy_holding_source_or_title_revalidated(self):
  for mode in('holding','source','title'):
   rows,people,h,d,c=fixture();tx=PreferenceCatalog(rows,people,ROOT);other=copy.deepcopy(tx)
   if mode=='holding':other[1]['holdings'][0]['mode']='grant'
   elif mode=='source':other[0]['paragraphs'][0]['text']='非'+other[0]['paragraphs'][0]['text']
   else:other[-1]['decisions'][0]['source_ref']['surface']='太保'
   self.assertRaises(ValueError,choice,other,people,h['person_id'],ROOT);self.assertIsNotNone(choice(tx,people,h['person_id'],ROOT))
 def test_nested_catalog_deepcopy_real_bundle_stays_equal(self):
  cat=load_catalog(ROOT);row=next(r for r in cat[1]if r.get('record_type')=='profile_title_preference_set');pid=row['decisions'][0]['person_id'];baseline=bundle(pid,root=ROOT,catalog=cat,include_provisional=True);other=copy.deepcopy(cat);self.assertIs(type(other[1]),list);self.assertEqual(bundle(pid,root=ROOT,catalog=other,include_provisional=True),baseline)
 def test_real_selected_holding_mutation_has_no_copied_index_bypass(self):
  cat=load_catalog(ROOT);other=copy.deepcopy(cat);d=next(r for r in other[1]if r.get('record_type')=='profile_title_preference_set')['decisions'][0];h=next(h for r in other[1]for h in r.get('holdings',[])if h['id']==d['holding_id']);h['title']='太保';self.assertRaises(ValueError,bundle,d['person_id'],root=ROOT,catalog=other,include_provisional=True)
if __name__=='__main__':unittest.main()
