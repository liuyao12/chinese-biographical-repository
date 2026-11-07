import copy,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.work_provenance import validate,inventory
from scripts.lu_near_paternal_family import proof,read
class LuWorkOrdinalSuccessor(unittest.TestCase):
 def overlay(self,changes):
  old=Path.read_text
  def text(p,*a,**k):
   if p.is_relative_to(ROOT)and str(p.relative_to(ROOT))in changes:return json.dumps(changes[str(p.relative_to(ROOT))],ensure_ascii=False)
   return old(p,*a,**k)
  old_bytes=Path.read_bytes
  def binary(p):
   if p.is_relative_to(ROOT)and str(p.relative_to(ROOT))in changes:return json.dumps(changes[str(p.relative_to(ROOT))],ensure_ascii=False).encode()
   return old_bytes(p)
  stack=ExitStack();stack.enter_context(patch.object(Path,'read_text',text));stack.enter_context(patch.object(Path,'read_bytes',binary));return stack
 def test_registered_work_has_unknown_scaffold(self):
  d=read(ROOT,'registry/work-provenance.json');validate(d,ROOT);w=d['works']['w-shishuoxinyu'];self.assertEqual(w['title'],'世說新語');self.assertEqual(w['composition'],{'status':'not_researched','assertions':[]});self.assertEqual(d['text_bases']['s-shishuo-shangyu-lu-near-family']['work_id'],w['work_id'])
 def test_missing_registered_work_refused(self):
  d=read(ROOT,'registry/work-provenance.json');del d['works']['w-shishuoxinyu']
  with self.assertRaises((AssertionError,KeyError)):validate(d,ROOT)
 def test_registered_work_without_source_still_requires_provenance(self):
  d=read(ROOT,'registry/work-provenance.json');works=read(ROOT,'registry/works.json');works['works'].append({'id':'w-test-missing-no-source','title':'測試缺履歷'})
  with self.overlay({'registry/works.json':works}),self.assertRaisesRegex(AssertionError,'作品履歷須涵蓋'):validate(d,ROOT)
 def test_kang_second_is_scoped_and_wrong_values_refused(self):
  c,roles,sources,sides,names=proof(ROOT);path='corpus/sanguozhi/sgz058-lu-near-family-assertions.json';d=sides[path];a=next(a for a in d['assertions']if a['id']=='a-lu-near-kang-father-xun');o=a['qualifiers']['source_reported_ordinal'];self.assertEqual(o['value'],2);self.assertEqual(o['source_number'],'次');self.assertEqual(o['parent_person_id'],roles['$xun']);self.assertEqual(o['scope'],'sons_of_reported_father');self.assertFalse(o['preferred_all_sibling_order_selected'])
  for key,value in [('value',3),('scope','all_siblings'),('parent_person_id',roles['$jun'])]:
   wrong=copy.deepcopy(d);next(a for a in wrong['assertions']if a['id']=='a-lu-near-kang-father-xun')['qualifiers']['source_reported_ordinal'][key]=value
   with self.overlay({path:wrong}),self.assertRaises(AssertionError):proof(ROOT)
if __name__=='__main__':unittest.main()
