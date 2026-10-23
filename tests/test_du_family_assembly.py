# coding:utf-8
from pathlib import Path
import json,copy,hashlib,unittest
from unittest.mock import patch
from scripts.person_bundle import load_catalog,bundle
from scripts.family_assemblies import load_assemblies
from scripts.received_kin_assembly import valid
from scripts.retired_person_ids import retired_person_ids,allocation_conflicts
ROOT=Path(__file__).resolve().parents[1];BASE='source-evidence/du-family-assembly';FID='family-jingzhao-du-ji-core'
def read(p):return json.loads(p.read_bytes())
def valuehash(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def pointer(v,p):
 for k in p.split('/')[1:]:v=v[int(k)]if isinstance(v,list)else v[k.replace('~1','/').replace('~0','~')]
 return v
class DuFamily(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cat=load_catalog(ROOT);cls.source,cls.assembled=load_assemblies(ROOT,cls.cat);cls.family=next(a for a in read(ROOT/'registry/family-assemblies.json')['assemblies']if a['id']==FID);cls.rows={m['person_id']:m for m in cls.family['members']};cls.claims={a['id']:a for r in cls.cat[1]if r.get('record_type')=='person_assertion_set'for a in r['assertions']};cls.chapters={r['id']:r for r in cls.cat[1]if r.get('record_type')=='marked_chapter'};cls.editorial=[m for m in cls.rows.values()if m.get('parent_connection')]
 def state(self):return copy.deepcopy(self.editorial[0]),copy.deepcopy(self.rows),copy.deepcopy(self.claims),copy.deepcopy(self.chapters)
 def check(self,m,rows,aa,chs):return valid(m,rows,aa,chs,ROOT)
 def test_eight_members_five_direct_two_editorial(self):
  self.assertEqual(len(self.rows),8);self.assertEqual(sum(m['source_assertion_id']is not None for m in self.rows.values()),5);self.assertEqual(len(self.editorial),2)
  for m in self.editorial:self.assertIsNone(m['source_assertion_id']);self.assertEqual(m['parent_connection']['interpretation_basis'],'fixed_complete_witness_shared_father');self.assertTrue(self.check(m,self.rows,self.claims,self.chapters))
 def test_direct_edges_are_source_fathers(self):
  for m in self.rows.values():
   if m['source_assertion_id']:
    a=self.claims[m['source_assertion_id']];self.assertEqual(a['predicate'],'father');self.assertEqual((a['subject_person_id'],a['object_person_id']),(m['person_id'],m['parent_person_id']))
 def test_editorial_fathers_not_synthesized_in_source(self):
  for m in self.editorial:self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==m['person_id']for a in self.claims.values()))
 def test_brother_source_and_unknown_orders_preserved(self):
  for m in self.editorial:
   a=self.claims[m['parent_connection']['sibling_assertion_id']];self.assertEqual(a['predicate'],'brother');self.assertNotIn('shared_father',a['qualifiers']);self.assertNotIn('shared_mother',a['qualifiers']);order=a['qualifiers']['relative_birth_order'];self.assertIsNone(order['older_ordinal']);self.assertIsNone(order['younger_ordinal'])
 def test_cousin_affinity_and_stepmother_not_members(self):
  sg=read(ROOT/'corpus/sanguozhi/016-duji-dushu-assertions.json')['assertions'];a=next(a for a in sg if a['id']=='a-sgz016-du-bin-older-agnatic-cousin-pre');self.assertNotIn(a['subject_person_id'],self.rows);self.assertIsNone(a['qualifiers']['kinship_structure']['common_ancestor_person_id']);self.assertIsNone(a['qualifiers']['kinship_structure']['distance']);s=next(a for a in sg if a['predicate']=='stepmother');self.assertNotIn(s['object_person_id'],self.rows)
  j=read(ROOT/'corpus/jinshu/034-duyu-assertions.json')['assertions'];spouse=next(a for a in j if a['predicate']=='spouse');self.assertNotIn(spouse['object_person_id'],self.rows)
 def test_same_mother_nonpaternal_and_explicit_different_father_rejected(self):
  for flag,value in [('same_mother_only',True),('lineage','maternal'),('shared_father',False)]:
   m,r,a,c=self.state();a[m['parent_connection']['sibling_assertion_id']]['qualifiers'][flag]=value
   with patch('scripts.fixed_kanripo_fact_slots.valid',return_value=True):self.assertFalse(self.check(m,r,a,c))
 def test_conflicting_father_from_other_source_rejected(self):
  m,r,a,c=self.state();other=next(a['object_person_id']for a in self.claims.values()if a['id']=='a-sgz016-du-pre-father-in-law-xuanwang');a['hypothetical-external-father']=dict(predicate='father',subject_person_id=m['person_id'],object_person_id=other,evidence=[dict(chapter_id='c-other-complete-source')])
  with patch('scripts.fixed_kanripo_fact_slots.valid',return_value=True):self.assertFalse(self.check(m,r,a,c))
 def test_reverse_brother_source_rejected(self):
  m,r,a,c=self.state();edge=a[m['parent_connection']['sibling_assertion_id']];edge['subject_person_id'],edge['object_person_id']=edge['object_person_id'],edge['subject_person_id'];self.assertFalse(self.check(m,r,a,c))
 def test_same_person_sibling_cycle_rejected(self):
  m,r,a,c=self.state();m['parent_connection']['sibling_person_id']=m['person_id']
  with patch('scripts.fixed_kanripo_fact_slots.valid',return_value=True):self.assertFalse(self.check(m,r,a,c))
 def test_wrong_witness_rejected(self):
  m,r,a,c=self.state();ch=next(iter(c[e['chapter_id']]for e in a[m['parent_connection']['sibling_assertion_id']]['evidence']));ch['source']['revision_id']='wrong';self.assertFalse(self.check(m,r,a,c))
 def test_wrong_fact_slot_rejected(self):
  m,r,a,c=self.state();a[m['parent_connection']['sibling_assertion_id']]['fixed_source_fact_binding']['slot']='wrong';self.assertFalse(self.check(m,r,a,c))
 def test_entire_projection_ref_cannot_disappear(self):
  m,r,a,c=self.state();cid=a[m['parent_connection']['sibling_assertion_id']]['evidence'][0]['chapter_id'];c[cid]['annotation'].pop('fixed_kanripo_projection_ref');self.assertFalse(self.check(m,r,a,c))
 def test_labels_and_coherent_family_ids_are_not_allowlisted(self):
  m,r,a,c=self.state();ids=list(r);mapping={pid:'zzz_yyy_xxx'+pid[len(self.family['root_person_id']):]for pid in ids}
  def rekey(v):
   if isinstance(v,dict):return{mapping.get(k,k):rekey(x)for k,x in v.items()}
   if isinstance(v,list):return[rekey(x)for x in v]
   return mapping.get(v,v)if isinstance(v,str)else v
  mm,rr,aa,cc=map(rekey,[m,r,a,c]);mm['label']='另一展示標籤';self.assertTrue(self.check(mm,rr,aa,cc))
 def test_stable_assertion_id_is_not_person_endpoint(self):
  data=read(ROOT/'corpus/jinshu/093-chupou-addresses.json');a=next(a for a in data['assertions']if a['id']=='pa-jinshu-093-chupou-51-source_locality_designation-a2u_2ji_h68');self.assertEqual(a['person_id'],self.claims['a-jin034-duyu-yi-father']['subject_person_id'])
 def test_retired_ids_not_queries_aliases_or_allocations(self):
  receipt=read(ROOT/(BASE+'/annotation-chain.json'));retired=retired_person_ids(ROOT)
  for old in receipt['retired_person_ids']:
   self.assertNotIn(old,self.cat[0]);self.assertIn(old,retired);self.assertTrue(allocation_conflicts(old,retired));self.assertTrue(allocation_conflicts(old+'_A',retired))
   with self.assertRaises(ValueError):bundle(old,ROOT,catalog=self.cat)
   for directory in('exports/persons','data/corpus/profiles'):self.assertFalse((ROOT/directory/(old+'.json')).exists())
 def test_historical_files_and_protected_capture_values_stay_exact(self):
  q=read(ROOT/(BASE+'/capture-qualification.json'))
  for spec in q['historical_files']:
   self.assertEqual(hashlib.sha256((ROOT/spec['path']).read_bytes()).hexdigest(),spec['sha256'])
   if spec.get('current_projection'):
    projection=read(ROOT/spec['current_projection']);self.assertEqual(projection['historical_sha256'],spec['sha256']);self.assertFalse(projection['person_aliases_created'])
    for cap in projection['protected_historical_capture_values']:
     v=pointer(projection,cap['projection_pointer']);self.assertEqual(valuehash(v),cap['json_value_sha256']);mutated=copy.deepcopy(v);mutated['negative_only']=True;self.assertNotEqual(valuehash(mutated),cap['json_value_sha256'])
if __name__=='__main__':unittest.main()
