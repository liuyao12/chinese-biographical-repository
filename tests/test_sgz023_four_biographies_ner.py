import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
from scripts.fixed_sgz023_peiqian import errors
from scripts.fixed_sgz023_four_biographies import proof,guard_bundle
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1];CH='corpus/sanguozhi/023-peiqian-ws2376966.json'
class FourBiographiesNER(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.ch=json.loads((ROOT/CH).read_text());cls.people,cls.records=load_catalog(ROOT)
 def altered(self,changes):
  old=Path.read_text
  def read(path,*args,**kw):
   try:r=str(path.relative_to(ROOT))
   except ValueError:return old(path,*args,**kw)
   return json.dumps(changes[r],ensure_ascii=False)if r in changes else old(path,*args,**kw)
  old_bytes=Path.read_bytes
  def read_bytes(path,*args,**kw):
   try:r=str(path.relative_to(ROOT))
   except ValueError:return old_bytes(path,*args,**kw)
   return json.dumps(changes[r],ensure_ascii=False).encode()if r in changes else old_bytes(path,*args,**kw)
  stack=ExitStack();stack.enter_context(patch.object(Path,'read_text',read));stack.enter_context(patch.object(Path,'read_bytes',read_bytes));return stack
 def corrupt_person(self,surface,pid):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']==surface);m['person_id']=pid
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_complete_source_and_four_people(self):
  self.assertEqual(errors(self.ch,ROOT),[]);self.assertEqual(len(self.ch['paragraphs']),14)
  for name in ['嚴幹','李義','韓宣','黃朗','魚豢','游楚','梁習','鄭文信','王惠陽','劉仲始','司馬芝','郝溫','郭端']:self.assertTrue(any(m['surface']==name and m['kind']=='person'for p in self.ch['paragraphs']for m in p['mentions']))
 def test_wrong_qin_xufu_rejected(self):self.corrupt_person('徐福','9nc_i02_15v')
 def test_wrong_caozhi_emperor_rejected(self):self.corrupt_person('臨菑侯植','tix_jqk_w1o')
 def test_wrong_hanxuanzhi_ancient_namesake_rejected(self):self.corrupt_person('韓宣','4e7_nix_4rh')
 def test_gaogan_not_yangan(self):
  m=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['surface']=='高幹');self.assertEqual(m['person_id'],'e06_e9f_c30')
 def test_calendar_kang_false_person_and_reverse_rejected(self):
  ch=copy.deepcopy(self.ch);p=ch['paragraphs'][8];m={'id':p['id']+':m0244','start':244,'end':245,'surface':'康','kind':'person','person_id':'kbq_kjc_n2f_BB','status':'contextual_provisional'};p['mentions'].append(m);p['mentions'].sort(key=lambda m:m['start'])
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_book_title_not_person(self):
  ch=copy.deepcopy(self.ch);m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='《諸葛亮傳》');self.assertEqual(m['kind'],'work' if self.ch['annotation'].get('typed_work_author_ref') else 'unresolved');m.update(kind='person',person_id='d1c_f9d_yc9',status='contextual_provisional')
  with self.altered({CH:ch}):self.assertTrue(errors(ch,ROOT))
 def test_lifeng_name_variant_uses_same_sourced_role(self):
  mm=[m for p in self.ch['paragraphs']for m in p['mentions']if m['surface']=='宣國'];self.assertEqual(len(mm),1);self.assertEqual(mm[0]['person_id'],'wj9_6bo_o54')
 def test_missing_new_person_reverse_and_alias_rejected(self):
  ch=self.ch;m=next(m for p in ch['paragraphs']for m in p['mentions']if m['surface']=='嚴幹');reg=json.loads((ROOT/'registry/persons.json').read_text());p=next(p for p in reg['persons']if p['id']==m['person_id']);p['aliases']=[];p['evidence']=[]
  with self.altered({'registry/persons.json':reg}):self.assertTrue(errors(ch,ROOT))
 def test_parent_relation_direction_remains_guarded(self):
  c=json.loads((ROOT/'source-evidence/sgz023-peiqian-ws2376966/contract.json').read_text());rel=next(r for r in c['sidecar_templates']if 'assertions'in r);d=json.loads((ROOT/rel).read_text());a=d['assertions'][0];a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
  with self.altered({rel:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_repaired_relationship_anchor_cannot_return_to_calendar(self):
  rel='corpus/sanguozhi/023-peiqian-ws2376966-assertions.json';d=json.loads((ROOT/rel).read_text());a=next(a for a in d['assertions']if a['id']=='a-sgz023-peiqian-kang-father-hui');self.assertTrue(a['evidence'][0]['subject_person_mention_id'].endswith(':m0474'));a['evidence'][0]['subject_person_mention_id']='c-sanguozhi-023-peiqian-ws2376966:p009:m0244'
  with self.altered({rel:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_caller_missing_source_sidecar_rejected(self):
  m=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['surface']=='嚴幹');rr=[r for r in self.records if not any(d.get('id','').startswith('d-sgz023-fourner-')for d in r.get('decisions',[]))]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,m['person_id'],self.people,rr)
 def test_normal_API_all_four_author_and_xufu(self):
  for name in ['嚴幹','李義','韓宣','黃朗','魚豢','徐福']:
   m=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['surface']==name);out=bundle(m['person_id'],root=ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertEqual(out['canonical_person_id'],m['person_id']);self.assertTrue(any(e.get('mention_id')==m['id']for p in out['persons']if p['id']==m['person_id']for e in p['evidence']))
 def test_current_hui_API_and_retired_id(self):
  out=bundle('kbq_kjc_n2f_B',root=ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertEqual(out['canonical_person_id'],'kbq_kjc_n2f_B');p=next(p for p in out['persons']if p['id']=='kbq_kjc_n2f_B');self.assertEqual(len(p['identity_review_history']),2)
  with self.assertRaises((ValueError,KeyError)):bundle('047_850_e7d',root=ROOT,include_provisional=True,catalog=(self.people,self.records))
  with self.assertRaises((ValueError,KeyError)):bundle('nx3_l5c_jlj',root=ROOT,include_provisional=True,catalog=(self.people,self.records))
 def test_hui_current_caller_metadata_and_identity_catalog_required(self):
  people=copy.deepcopy(self.people);people['kbq_kjc_n2f_B']['identity_review_history']=[]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,'kbq_kjc_n2f_B',people,self.records)
  records=[r for r in self.records if not any(d.get('id')=='d-sgz023-hui-explicit-xuncan-reference'for d in r.get('decisions',[]))]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,'kbq_kjc_n2f_B',self.people,records)
 def test_hui_split_endpoint_cannot_hide_in_parent_view(self):
  review=json.loads((ROOT/'source-evidence/two-hui-identity/current-review.json').read_text());spec=next(s for s in review['source_roles']if '010' in s['path']);d=json.loads((ROOT/spec['path']).read_text());p=next(p for p in d['paragraphs']if p['id']==spec['paragraph_id']);m=next(m for m in p['mentions']if m['id']==spec['marker']['id']);m['person_id']='047_850_e7d'
  with self.altered({spec['path']:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_hui_guard_runs_on_true_current_caller(self):
  from scripts import two_hui_identity
  original=two_hui_identity.validate
  with patch.object(two_hui_identity,'validate',wraps=original)as called:
   self.assertEqual(errors(self.ch,ROOT),[]);self.assertGreaterEqual(called.call_count,1);self.assertEqual(called.call_args_list[0].args[1],self.ch)
if __name__=='__main__':unittest.main()
