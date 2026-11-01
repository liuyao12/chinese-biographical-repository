import copy,hashlib,json,sys,unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.lu_near_paternal_family import proof,contract,read,raw,typed_projection,guard_bundle,REF
from scripts.person_bundle import load_catalog,bundle
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts

class LuNearPaternalFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c,cls.roles,cls.sources,cls.sides,cls.names=proof(ROOT)
  cls.people,cls.records=load_catalog(ROOT)
 def overlay(self,changes):
  ob,ot=Path.read_bytes,Path.read_text
  def get(p):
   if not p.is_relative_to(ROOT):return None
   v=changes.get(str(p.relative_to(ROOT)))
   return v if v is None or isinstance(v,bytes)else(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
  stack=ExitStack();stack.enter_context(patch.object(Path,'read_bytes',lambda p:get(p)if get(p)is not None else ob(p)));stack.enter_context(patch.object(Path,'read_text',lambda p,*a,**k:get(p).decode()if get(p)is not None else ot(p,*a,**k)));return stack
 def test_current_six_and_retirement(self):
  self.assertEqual(set(self.people),{p['id']for p in read(ROOT,'registry/persons.json')['persons']});self.assertTrue(set(self.roles.values())<=set(self.people))
  for old in self.c['historical_old_id_role_map']:
   self.assertNotIn(old,self.people);self.assertIn(old,retired_person_ids(ROOT));self.assertTrue(allocation_conflicts(old,retired_person_ids(ROOT)))
  self.assertEqual(len({pid.split('_')[0]for pid in self.roles.values()}),1)
 def test_full_received_critique_and_qualification(self):
  units=read(ROOT,self.c['ledger_path']);self.assertIn('無陸機兄弟',units[2]['complete_item_text'])
  for ch in self.sources.values():self.assertIsNone(ch['source']['edition']);self.assertIs(ch['source']['human_reviewed'],False);self.assertIs(ch['source']['original_wikitext_obtained'],False)
  self.assertTrue(any(p['text_layer']=='witness_appended_liuxiaobiao_note'for ch in self.sources.values()for p in ch['paragraphs']))
 def test_fifth_and_same_mother_are_scoped(self):
  assertions=[a for d in self.sides.values()for a in d['assertions']];a=next(a for a in assertions if a['id']=='a-lu-near-yun-father-kang');o=a['qualifiers']['source_reported_ordinal'];self.assertEqual(o['value'],5);self.assertIs(o['preferred_all_sibling_order_selected'],False)
  b=next(a for a in assertions if a['id']=='a-lu-near-yun-younger-shared-mother-ji');self.assertIs(b['qualifiers']['shared_mother'],True);self.assertIsNone(b['qualifiers']['mother_person_id']);self.assertIsNone(b['qualifiers']['relative_birth_order']['older_ordinal'])
  for path,d in self.sides.items():
   wrong=copy.deepcopy(d)
   for a in wrong['assertions']:
    if 'source_reported_ordinal'in a['qualifiers']:a['qualifiers']['source_reported_ordinal']['value']=4
    if 'shared_mother'in a['qualifiers']:a['qualifiers']['shared_mother']=False
   if wrong!=d:
    with self.overlay({path:wrong}),self.assertRaises(AssertionError):proof(ROOT)
 def test_wrong_single_endpoint_or_glyph_refused(self):
  for path,ch in self.sources.items():
   wrong=copy.deepcopy(ch);m=next(m for p in wrong['paragraphs']for m in p['mentions']);m['person_id']=self.roles['$ji']if m['person_id']!=self.roles['$ji']else self.roles['$xun']
   with self.overlay({path:wrong}),self.assertRaises(AssertionError):proof(ROOT)
  wrong=copy.deepcopy(self.names);wrong['records'][0]['surname']='羊'
  with self.overlay({self.c['name_path']:wrong}),self.assertRaises(AssertionError):proof(ROOT)
 def test_caller_reverse_or_names_omission_refused(self):
  for role in self.roles:
   pid=self.roles[role];people=copy.deepcopy(self.people);people[pid]['evidence']=[]
   with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,people,self.records)
  pid=self.roles['$yu'];records=[d for d in self.records if d!=self.names]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,self.people,records)
 def test_coherent_whole_family_rekey_keeps_opaque_and_captures(self):
  root=self.roles['$yu'];new='z97_k3x_h2p';self.assertNotIn(new,self.people);mapping={pid:new+pid[len(root):]for pid in self.roles.values()}
  rels={a['path']for a in self.c['archives']}|set(self.sources)|set(self.sides)|{self.c['name_path'],self.c['preferred_reading_path']};changes={}
  for rel in rels:
   if rel.endswith('.json'):changes[rel]=typed_projection(read(ROOT,rel),mapping)
   else:
    b=raw(ROOT,rel).decode()
    for old,pid in mapping.items():b=b.replace('ref="'+old+'"','ref="'+pid+'"')
    changes[rel]=b.encode()
  people={mapping.get(k,k):typed_projection(v,mapping)for k,v in self.people.items()};records=[typed_projection(x,mapping)for x in self.records]
  capture_before={p:hashlib.sha256(raw(ROOT,p)).hexdigest()for p in self.c['immutable_prior_capture_hashes']}
  with self.overlay(changes):
   proof(ROOT,people=people,records=records)
   for pid in mapping.values():guard_bundle(ROOT,pid,people,records)
   self.assertEqual(capture_before,{p:hashlib.sha256(raw(ROOT,p)).hexdigest()for p in capture_before})
   for rel,ch in self.sources.items():self.assertEqual([m['id']for p in read(ROOT,rel)['paragraphs']for m in p['mentions']],[m['id']for p in ch['paragraphs']for m in p['mentions']])
   missing=copy.deepcopy(people);missing[mapping[self.roles['$yun']]]['evidence']=[]
   with self.assertRaises(AssertionError):guard_bundle(ROOT,mapping[self.roles['$yun']],missing,records)
 def test_declared_glyph_reading_cannot_be_recast_as_received(self):
  from scripts.lu_near_paternal_family import preferred_reading_errors
  names=[n for d in self.records if d.get('record_type')=='person_name_component_set'for n in d['records']]
  chapters={d['id']:d for d in self.records if d.get('record_type')=='marked_chapter'}
  pref=read(ROOT,self.c['preferred_reading_path'])
  for r in pref['readings']:
   self.assertEqual(preferred_reading_errors(r,names,chapters,ROOT),[])
   bad=copy.deepcopy(r);bad['basis']['not_an_additional_received_witness']=False
   self.assertTrue(preferred_reading_errors(bad,names,chapters,ROOT))
   for mutate in ('wrong-record','wrong-conversion'):
    bad=copy.deepcopy(r)
    if mutate=='wrong-record':bad['records'][0]['record']['id']='name-lu-near-not-this-owner'
    else:bad['preferred_value']='X';bad['basis']['display_value']='X'
    self.assertTrue(preferred_reading_errors(bad,names,chapters,ROOT))
  sgpath=next(p for p,c in self.sources.items()if c['work_id']=='w-sanguozhi')
  sg=copy.deepcopy(self.sources[sgpath]);sg['paragraphs'][1]['text']=sg['paragraphs'][1]['text'].replace('\u7ea1','\u7d06')
  with self.overlay({sgpath:sg}),self.assertRaises(AssertionError):proof(ROOT)
  pid=self.roles['$yu'];records=[d for d in self.records if d!=pref]
  with self.assertRaises(AssertionError):guard_bundle(ROOT,pid,self.people,records)
 def test_pei_work_collection_grows_without_weakening_old_rows_or_authors(self):
  from scripts.fixed_sgz023_works import state,work_with_additive_books_valid,author_valid
  c,ch,old,roles,works=state(ROOT)
  actual=read(ROOT,'registry/works.json')['works'];work=next(w for w in actual if w['id']=='w-sanguozhi')
  baseline=copy.deepcopy(work);baseline['books']=[b for b in baseline['books']if b['id']!='b-sanguozhi-058']
  self.assertTrue(work_with_additive_books_valid(work,baseline,ROOT))
  for kind in ('old-retitle','old-remove','old-reorder','new-wrong-work','new-unknown-chapter','duplicate-book'):
   bad=copy.deepcopy(work)
   if kind=='old-retitle':bad['books'][0]['title']='bad'
   elif kind=='old-remove':bad['books'].pop(0)
   elif kind=='old-reorder':bad['books'][0],bad['books'][1]=bad['books'][1],bad['books'][0]
   elif kind=='new-wrong-work':bad['books'][-1]['work_id']='w-jinshu'
   elif kind=='new-unknown-chapter':bad['books'][-1]['chapter_ids']=['c-no-such-chapter']
   else:bad['books'].append(copy.deepcopy(bad['books'][-1]))
   self.assertFalse(work_with_additive_books_valid(bad,baseline,ROOT),kind)
  typed_baseline=copy.deepcopy(baseline);typed_work=copy.deepcopy(work)
  typed_baseline['books'][0]['number']=1;typed_work['books'][0]['number']=1
  self.assertTrue(work_with_additive_books_valid(typed_work,typed_baseline,ROOT))
  typed_work['books'][0]['number']=True
  self.assertFalse(work_with_additive_books_valid(typed_work,typed_baseline,ROOT),'old book integer1 must not equal boolTrue')
  found=[]
  for w in works.values():
   for e in w.get('source_author_attributions',[]):
    if e['work_mention_id'].endswith((':m0330',':m0333',':m0619')):
     self.assertTrue(author_valid(e,w,ch,ROOT));found.append(e['work_mention_id'])
  self.assertEqual(len(found),3)
 def test_normal_six_api(self):
  for role,pid in self.roles.items():
   with self.subTest(role=role):
    b=bundle(pid,root=ROOT,catalog=(self.people,self.records));self.assertEqual(b['canonical_person_id'],pid)

if __name__=='__main__':unittest.main()
