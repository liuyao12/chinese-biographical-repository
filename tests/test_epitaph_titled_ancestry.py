from tests.portable_fixture_copy import fixture_copy2
import unittest,copy,json,tempfile,shutil
from pathlib import Path
from scripts.person_bundle import load_catalog
from scripts.epitaph_titled_ancestry import valid,BASIS
R=Path(__file__).resolve().parents[1]
class TitledEpitaphAncestry(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.people,rs=load_catalog(R);cls.chapters={r['id']:r for r in rs if r.get('record_type')=='marked_chapter'};cls.assertions={a['id']:a for r in rs if r.get('record_type')=='person_assertion_set'for a in r['assertions']};cls.family=next(f for f in json.loads((R/'registry/family-assemblies.json').read_text())['assemblies']if any(m.get('parent_connection',{}).get('interpretation_basis')==BASIS for m in f['members']));cls.rows={m['person_id']:m for m in cls.family['members']};cls.member=next(m for m in cls.rows.values()if m.get('parent_connection',{}).get('interpretation_basis')==BASIS)
 def check(self,m=None,rows=None,aa=None,cc=None,root=R):return valid(m or self.member,rows or self.rows,aa or self.assertions,cc or self.chapters,root)
 def test_real_complete_witness_and_two_distances(self):self.assertTrue(self.check());self.assertFalse(self.check(root=None));self.assertEqual(len(self.family['members']),28)
 def test_no_added_source_father_for_anonymous_parent(self):
  self.assertIsNone(self.member['source_assertion_id']);self.assertFalse(any(a['predicate']=='father'and a['subject_person_id']==self.member['person_id']for a in self.assertions.values()))
 def test_wrong_parent_or_grandparent_not_id_whitelist(self):
  for k in ('parent_person_id','chain_subject_person_id'):
   m=copy.deepcopy(self.member)
   if k=='chain_subject_person_id':m['parent_connection'][k]=self.family['root_person_id']
   else:m[k]=self.family['root_person_id']
   self.assertFalse(self.check(m=m))
 def test_order_and_source_claim_ids(self):
  m=copy.deepcopy(self.member);b=m['parent_connection'];b['nearer_ancestor_assertion_id'],b['farther_ancestor_assertion_id']=b['farther_ancestor_assertion_id'],b['nearer_ancestor_assertion_id'];self.assertFalse(self.check(m=m))
 def test_primitive_source_father_cannot_be_fabricated(self):
  aa=copy.deepcopy(self.assertions);a=copy.deepcopy(aa[self.member['parent_connection']['nearer_ancestor_assertion_id']]);a['id']='synthetic-conflicting-father';a['subject_person_id']=self.member['person_id'];a['object_person_id']=self.family['root_person_id'];aa[a['id']]=a;self.assertFalse(self.check(aa=aa))
 def test_role_spans_and_surfaces_bound(self):
  cid=self.assertions[self.member['parent_connection']['nearer_ancestor_assertion_id']]['evidence'][0]['chapter_id']
  for mode in ('offset','outer_quote','maternal'):
   cc=copy.deepcopy(self.chapters);c=cc[cid];p=c['paragraphs'][0]
   if mode=='offset':next(m for m in p['mentions']if m['id']==c['annotation']['epitaph_fact_binding']['roles']['father'])['start']+=1
   elif mode=='outer_quote':p['text']='「'+p['text']+'」'
   else:p['text']=p['text'].replace('之孫','之外孫',1)
   self.assertFalse(self.check(cc=cc))
 def test_identity_qualification_is_read_not_just_ref_label(self):
  with tempfile.TemporaryDirectory()as t:
   base=Path(t)
   for rel in ['source-evidence/yangshu-epitaph-zju','source-evidence/yangshu-family-placement']:
    shutil.copytree(R/rel,base/rel, copy_function=fixture_copy2)
   q=base/'corpus/weishu-weishou/058-yangbo-yangkan.json';q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((R/'corpus/weishu-weishou/058-yangbo-yangkan.json').read_bytes())
   self.assertTrue(self.check(root=base));rel=self.member['parent_connection']['ancestor_identity_reference']['path'];q=base/rel;old=q.read_bytes();d=json.loads(old);g=next(x for x in d['decisions']if x['key']=='grandfather')
   for key,value in [('status','source_attested'),('qualification',''),('person_id',self.member['person_id'])]:
    dd=copy.deepcopy(d);next(x for x in dd['decisions']if x['key']=='grandfather')[key]=value;q.write_text(json.dumps(dd,ensure_ascii=False));self.assertFalse(self.check(root=base))
   q.write_bytes(old)
 def test_actual_transcription_and_hash_cannot_drift(self):
  with tempfile.TemporaryDirectory()as t:
   base=Path(t)
   for rel in ['source-evidence/yangshu-epitaph-zju','source-evidence/yangshu-family-placement']:shutil.copytree(R/rel,base/rel, copy_function=fixture_copy2)
   q=base/'source-evidence/yangshu-epitaph-zju/transcription.json';d=json.loads(q.read_text());d['text']=d['text']+'錯';q.write_text(json.dumps(d,ensure_ascii=False));self.assertFalse(self.check(root=base))
 def test_reference_scope_and_exact_quotes(self):
  for k,v in [('quote','孫'),('source_id','synthetic-other'),('scope','')]:
   m=copy.deepcopy(self.member);m['parent_connection']['references'][0][k]=v;self.assertFalse(self.check(m=m))
 def test_same_title_does_not_resolve_anonymous_father(self):
  child=self.rows[self.member['parent_connection']['chain_subject_person_id']];self.assertEqual(child['parent_person_id'],self.member['person_id']);self.assertEqual(child['source_assertion_id'],self.member['parent_connection']['nearer_ancestor_assertion_id']);self.assertNotEqual(self.member['parent_person_id'],child['parent_person_id'])
