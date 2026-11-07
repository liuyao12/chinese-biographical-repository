# coding: utf-8
import pathlib,json,copy,sys,unittest
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.fixed_liang041_wanggui import proof,errors,guard_bundle,name_contract,uncle_valid,inherited_rank_valid
from scripts.fixed_liang041_taoshiheng import REF,_state,owner_applies
from scripts.person_bundle import load_catalog,bundle
from scripts.validate_corpus import normalized_date_errors,direct_source_age_valid
from scripts.age_context import age_context_valid
class TaoShihengSuccessor(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.ch,cls.parent=proof(ROOT);cls.people,cls.records=load_catalog(ROOT);cls.case=_state(ROOT)[2]
 def altered(self,changes):
  rb=pathlib.Path.read_bytes;rt=pathlib.Path.read_text
  def raw(p,*a,**kw):
   try:r=str(p.relative_to(ROOT))
   except ValueError:return rb(p,*a,**kw)
   return changes[r]if isinstance(changes.get(r),bytes)else(json.dumps(changes[r],ensure_ascii=False)+'\n').encode()if r in changes else rb(p,*a,**kw)
  def text(p,*a,**kw):
   try:r=str(p.relative_to(ROOT))
   except ValueError:return rt(p,*a,**kw)
   return raw(p).decode()if r in changes else rt(p,*a,**kw)
  from contextlib import ExitStack
  stack=ExitStack();stack.enter_context(patch.object(pathlib.Path,'read_bytes',raw));stack.enter_context(patch.object(pathlib.Path,'read_text',text));return stack
 def bad_chapter(self,fn):
  ch=copy.deepcopy(self.ch);fn(ch)
  with self.altered({self.case['chapter_path']:ch}):self.assertTrue(errors(ch,ROOT))
 def test_qualified_source_owner(self):self.assertEqual(errors(self.ch,ROOT),[])
 def test_only_one_received_marker_changes(self):
  parent=json.loads((ROOT/self.case['parent_ref']).read_bytes())['chapter_template'];a={m['id']:m for p in parent['paragraphs']for m in p['mentions']};b={m['id']:m for p in self.ch['paragraphs']for m in p['mentions']};self.assertEqual(a.keys(),b.keys());self.assertEqual([k for k in a if a[k]!=b[k]],[self.case['target_mid']]);self.assertEqual(parent['source'],self.ch['source']);self.assertEqual(parent['text_sha256'],self.ch['text_sha256'])
 def test_wrong_luji_same_zi_rejected(self):self.bad_chapter(lambda c:c['paragraphs'][6]['mentions'][0].update(person_id='69h_uhy_hta'))
 def test_received_shiheng_not_silently_shixing(self):self.bad_chapter(lambda c:c['paragraphs'][6].update(text=c['paragraphs'][6]['text'].replace('陶士衡','陶士行')))
 def test_other_parent_marker_cannot_change(self):self.bad_chapter(lambda c:c['paragraphs'][3]['mentions'][5].update(person_id='gni_7gn_c4a'))
 def test_missing_successor_case_rejected(self):
  with self.altered({REF:b'{}'}):self.assertTrue(errors(self.ch,ROOT))
 def test_missing_new_alias_rejected(self):
  people=copy.deepcopy(self.people);p=people[self.case['target_pid']];p['aliases']=[a for a in p['aliases']if a['surface']!='陶士衡']
  with self.assertRaises(AssertionError):guard_bundle(ROOT,self.case['target_pid'],people,self.records)
 def test_missing_new_reverse_rejected(self):
  people=copy.deepcopy(self.people);p=people[self.case['target_pid']];p['evidence']=[e for e in p['evidence']if e.get('mention_id')!=self.case['target_mid']]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,self.case['target_pid'],people,self.records)
 def test_missing_identity_catalog_rejected(self):
  records=[r for r in self.records if r.get('chapter_id')!=self.ch['id']or r.get('record_type')!='identity_decision_set']
  with self.assertRaises(AssertionError):guard_bundle(ROOT,self.case['target_pid'],self.people,records)
 def test_catalog_cannot_substitute_parent(self):
  old=json.loads((ROOT/self.case['parent_ref']).read_bytes())['chapter_template'];records=[old if r.get('id')==self.ch['id']else r for r in self.records]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,self.case['target_pid'],self.people,records)
 def test_ssxy_complete_capture_not_replaceable(self):
  cap=self.case['ssxy_capture'];bad=(ROOT/cap['path']).read_bytes().replace('陶士衡'.encode(),'陸士衡'.encode())
  with self.altered({cap['path']:bad}):self.assertTrue(errors(self.ch,ROOT))
 def test_immutable_parent_contract_not_rewritten(self):
  d=json.loads((ROOT/self.case['parent_ref']).read_bytes());d['chapter_template']=self.ch
  with self.altered({self.case['parent_ref']:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_names_uncle_death_age_titles_still_work(self):
  self.assertTrue(name_contract(ROOT));paras={p['id']:(self.ch['id'],p)for p in self.ch['paragraphs']};aa=json.loads((ROOT/'corpus/liangshu/041-wanggui-ws1512987-assertions.json').read_bytes())['assertions'];uncles=[a for a in aa if a['predicate']=='paternal_uncle'];self.assertTrue(uncles)
  for a in uncles:self.assertTrue(uncle_valid(a,paras,ROOT))
  life=json.loads((ROOT/'corpus/liangshu/041-wanggui-ws1512987-life-events.json').read_bytes())['events'][0];self.assertEqual(normalized_date_errors(life['normalized_date'],{self.ch['id']:self.ch},ROOT,bound_record=life,bound_role='life_event'),[]);age=self.ch['annotation']['age_assertions'][0];self.assertTrue(direct_source_age_valid(age));self.assertTrue(age_context_valid(age,{life['id']:life}));self.assertEqual(life['normalized_date']['year'],536)
  rank=json.loads((ROOT/'source-evidence/liang041-wanggui-ws1512987/inherited-rank-heading-contract.json').read_bytes())['holdings']
  for h in rank:self.assertTrue(inherited_rank_valid(h,self.ch,ROOT))
 def test_protected_name_contract_failure_cannot_be_hidden(self):
  p='source-evidence/liang041-wanggui-ws1512987/name-components-contract.json';d=json.loads((ROOT/p).read_bytes());d['record']['records'][0]['ming']='偽名'
  with self.altered({p:d}):self.assertTrue(errors(self.ch,ROOT))
 def test_coherent_source_owned_current_endpoint_rekey_without_capture_changes(self):
  old=self.case['target_pid'];new='zzt_4ao_001';self.assertNotIn(new,self.people)
  def project(x):
   if isinstance(x,str):return new if x==old else x
   if isinstance(x,list):return[project(v)for v in x]
   if isinstance(x,dict):return{new if k==old else k:project(v)for k,v in x.items()}
   return x
  reg=project(json.loads((ROOT/'registry/persons.json').read_bytes()));people={p['id']:p for p in reg['persons']};records=project(self.records)
  changes={'registry/persons.json':reg,self.case['chapter_path']:project(self.ch),self.case['decision_path']:project(self.case['decision_after']),self.case['source_seed']['path']:project(json.loads((ROOT/self.case['source_seed']['path']).read_bytes()))}
  parent=(ROOT/self.case['parent_ref']).read_bytes();raw=(ROOT/self.case['ssxy_capture']['path']).read_bytes();case=(ROOT/REF).read_bytes()
  with self.altered(changes):
   current,base,expanded=_state(ROOT,people=people);self.assertEqual(expanded['target_pid'],new);self.assertEqual(current['paragraphs'][6]['mentions'][0]['person_id'],new);self.assertTrue(owner_applies(new,people,records));guard_bundle(ROOT,new,people,records)
   # Missing new reverse still cannot suppress ownership after a legitimate role rekey.
   missing=copy.deepcopy(people);missing[new]['evidence']=[e for e in missing[new]['evidence']if e.get('mention_id')!=self.case['target_mid']];self.assertTrue(owner_applies(new,missing,records))
   with self.assertRaises(AssertionError):guard_bundle(ROOT,new,missing,records)
   self.assertEqual((ROOT/self.case['parent_ref']).read_bytes(),parent);self.assertEqual((ROOT/self.case['ssxy_capture']['path']).read_bytes(),raw);self.assertEqual((ROOT/REF).read_bytes(),case)
 def test_partial_rekey_cannot_change_only_upgraded_endpoint(self):
  self.bad_chapter(lambda c:c['paragraphs'][6]['mentions'][0].update(person_id='zzt_4ao_001'))
 def test_normal_current_taokan_and_wanggui_API(self):
  for pid in [self.case['target_pid'],'7r6_k52_qji_ABAAAAEAAAA']:
   out=bundle(pid,root=ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertEqual(out['canonical_person_id'],pid)
  out=bundle(self.case['target_pid'],root=ROOT,include_provisional=True,catalog=(self.people,self.records));self.assertTrue(any(e.get('mention_id')==self.case['target_mid']for p in out['persons']if p['id']==self.case['target_pid']for e in p['evidence']))
if __name__=='__main__':unittest.main(verbosity=2)
