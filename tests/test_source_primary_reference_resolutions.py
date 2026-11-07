# coding: utf-8
"""Real captured source and ordinary catalog; editorial consistency, not history by schema."""
import copy,hashlib,json,sys,unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import source_primary_reference_resolutions as refs
from scripts.fixed_zhou041_wangbao import proof,errors,guard_bundle,CH
from scripts.person_bundle import load_catalog,bundle
from scripts.render_corpus import render
class PrimaryReferenceBinding(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch,cls.contract,cls.roles=proof(ROOT);cls.state=refs.resolve(ROOT,CH);cls.case=cls.state['resolved'][0];cls.entry=cls.case['entry'];cls.ref=cls.state['ref'];cls.pid=cls.case['pid'];cls.reg=refs.read(ROOT,'registry/persons.json');cls.identities=refs.read(ROOT,cls.state['document']['decision_path']);cls.catalog=load_catalog(ROOT)
 def overlay(self,changes):
  ob,ot=Path.read_bytes,Path.read_text
  def value(p):
   if not p.is_relative_to(ROOT)or str(p.relative_to(ROOT))not in changes:return None
   v=changes[str(p.relative_to(ROOT))];return v if isinstance(v,bytes)else v.encode()if isinstance(v,str)else(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
  s=ExitStack();s.enter_context(patch.object(Path,'read_bytes',lambda p:value(p)if value(p)is not None else ob(p)));s.enter_context(patch.object(Path,'read_text',lambda p,*a,**k:value(p).decode()if value(p)is not None else ot(p,*a,**k)));return s
 def reject(self,changes):
  with self.overlay(changes):self.assertTrue(errors(changes.get(CH,self.ch),ROOT))
 def prior(self):
  ch=copy.deepcopy(self.ch);mid=self.entry['target']['mention_id'];old=next(m for p in self.contract['chapter_template']['paragraphs']for m in p['mentions']if m['id']==mid)
  for p in ch['paragraphs']:
   for i,m in enumerate(p['mentions']):
    if m['id']==mid:p['mentions'][i]=copy.deepcopy(old)
  a=ch['annotation'];a.pop(refs.ANNOTATION_REF);oldlist=self.contract['chapter_template']['annotation']['unresolved_source_reference_readings'];ix=next(i for i,v in enumerate(oldlist)if v['id']==self.entry['id']);a['unresolved_source_reference_readings'].insert(ix,copy.deepcopy(oldlist[ix]))
  for f in self.state['document']['progress_formatters']:
   at,key=refs._pointer(ch,f['pointer']);at[key]=refs._format(f['template'],refs.counts(ch))
  return ch
 def test_actual_unit_existing_candidate_and_literal_reverse(self):
  actor=self.catalog[0][self.pid];self.assertEqual(actor['label'],'尹喜（老韓列傳候選）');self.assertEqual(actor['historicity'],'historical_tradition');self.assertIn(self.entry['canonical_anchor']['reverse'],actor['evidence']);self.assertEqual(len(self.entry['canonical_anchor']['reverse']),4)
  self.assertEqual(self.case['reverse']['quote'],'關令');self.assertEqual(len(self.case['reverse']),7);self.assertFalse(self.entry['interpretation']['automated_historical_identity_proof']);self.assertFalse(self.entry['primary']['fixed_permalink_body_read']);self.assertIsNone(self.entry['primary']['actual_print_edition'])
 def test_only_explicit_identity_leaves_and_counter_slots_get_view(self):
  old=self.prior();self.assertTrue(refs.same(refs.semantic_view(old,self.state,prior=True),refs.semantic_view(self.ch,self.state)));self.assertEqual(refs.xml_view(render(old),self.state,prior=True),refs.xml_view(render(self.ch),self.state))
  unknown=copy.deepcopy(self.ch);unknown['annotation']['unknown_metadata_to_preserve']={'x':False};self.assertNotEqual(refs.semantic_view(unknown,self.state),refs.semantic_view(self.ch,self.state))
  old['annotation']['unknown_metadata_to_preserve']={'x':False};current=copy.deepcopy(self.ch);current['annotation']['unknown_metadata_to_preserve']={'x':False};self.assertTrue(refs.same(refs.semantic_view(old,self.state,prior=True),refs.semantic_view(current,self.state)));current['annotation']['unknown_metadata_to_preserve']['x']=0;self.assertFalse(refs.same(refs.semantic_view(old,self.state,prior=True),refs.semantic_view(current,self.state)))
 def test_wrong_single_target_and_seed_endpoints_rejected(self):
  ch=copy.deepcopy(self.ch);next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==self.entry['target']['mention_id'])['person_id']=self.roles['$liukun'];self.reject({CH:ch})
  path=self.entry['canonical_anchor']['path'];seed=refs.read(ROOT,path);next(m for p in seed['paragraphs']for m in p['mentions']if m['id']==self.entry['canonical_anchor']['marker']['id'])['person_id']=self.roles['$liukun'];self.reject({path:seed})
 def test_missing_reverse_or_literal_alias_and_fabricated_name_refused(self):
  mid=self.entry['target']['mention_id']
  for kind in ('reverse','missing-alias','fabricated-full-name'):
   reg=copy.deepcopy(self.reg);actor=next(p for p in reg['persons']if p['id']==self.pid)
   if kind=='reverse':actor['evidence']=[e for e in actor['evidence']if e.get('mention_id')!=mid]
   else:
    for a in actor['aliases']:
     if mid in a['mention_ids']:
      if kind=='fabricated-full-name':a['surface']='尹喜'
      else:a['mention_ids'].remove(mid)
   self.reject({'registry/persons.json':reg})
 def test_wrong_owner_unknown_kind_and_false_source_qualifications_refused(self):
  for key,val in [('owner','foreign'),('kind','unrecognized_role_kind'),('fixed_permalink_body_read',True),('image_verified',True),('actual_print_edition','武英殿'),('citation_layer_kind','modern_collation_report'),('automated_historical_identity_proof',True),('reported_revision',True)]:
   doc=copy.deepcopy(self.state['document'])
   if key=='owner':doc['owner']['chapter_id']=val
   elif key=='kind':doc['entries'][0]['kind']=val
   elif key=='automated_historical_identity_proof':doc['entries'][0]['interpretation'][key]=val
   else:doc['entries'][0]['primary'][key]=val
   self.reject({self.ref:doc})
 def test_full_observed_tool_paragraph_not_truncated_quote(self):
  doc=copy.deepcopy(self.state['document']);p=doc['entries'][0]['primary'];p['complete_unit']=p['complete_unit'][:-1];p['normalized_unit_sha256']=refs.sha(p['complete_unit'].encode());self.reject({self.ref:doc})
 def test_unexplained_other_mid_unknown_metadata_and_modern_notes_refused(self):
  for key in ('other-mid','unknown','modern','source','offset-bool'):
   ch=copy.deepcopy(self.ch)
   if key=='other-mid':ch['paragraphs'][0]['mentions'][0]['person_id']=self.pid
   elif key=='unknown':ch['annotation']['new_unknown_metadata']={'do_not_ignore':True}
   elif key=='modern':ch['annotation']['modern_collation_reports'][0]['text']+='改'
   elif key=='source':ch['source']['printed_base_edition']='武英殿'
   else:next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==self.entry['target']['mention_id'])['start']=True
   self.reject({CH:ch})
 def test_current_decision_and_progress_cannot_drift(self):
  decisions=copy.deepcopy(self.identities);next(d for d in decisions['decisions']if d['id']==self.entry['id'])['person_id']=self.roles['$liukun'];self.reject({self.state['document']['decision_path']:decisions})
  for key in ('coverage','old-limit'):
   ch=copy.deepcopy(self.ch)
   if key=='coverage':
    c=refs.counts(ch);c['person']+=1;f=next(v for v in self.state['document']['progress_formatters']if v['pointer']=='/annotation/coverage');ch['annotation']['coverage']=refs._format(f['template'],c)
   else:ch['annotation']['limitations'][0]='已全部證實'
   self.reject({CH:ch})
  doc=copy.deepcopy(self.state['document']);doc['progress_formatters'][0]['pointer']='/source/edition';self.reject({self.ref:doc})
 def test_caller_single_endpoint_foreign_query_and_missing_sidecar_refused(self):
  people=copy.deepcopy(self.catalog[0]);records=copy.deepcopy(list(self.catalog[1]));owned={m.get('person_id')for p in self.ch['paragraphs']for m in p['mentions']};foreign=next(pid for pid in people if pid not in owned and not any(e.get('chapter_id')==self.ch['id']for e in people[pid]['evidence']));self.assertNotIn(foreign,owned);ch=next(r for r in records if r.get('id')==self.ch['id']);next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==self.entry['target']['mention_id'])['person_id']=foreign
  with self.assertRaises((AssertionError,ValueError)):guard_bundle(ROOT,foreign,people,records)
  records=[r for r in self.catalog[1]if not(r.get('record_type')=='identity_decision_set'and r.get('chapter_id')==self.ch['id'])]
  with self.assertRaises((AssertionError,ValueError)):guard_bundle(ROOT,self.pid,self.catalog[0],records)
 def test_complete_reference_rekey_ordinary_api_without_PID_whitelist(self):
  new='j97_r4k_b1n';self.assertNotIn(new,self.catalog[0]);mid=self.entry['target']['mention_id'];values={}
  def project(x):
   if isinstance(x,str):return new if x==self.pid else x
   if isinstance(x,list):return[project(v)for v in x]
   if isinstance(x,dict):return{k:project(v)for k,v in x.items()}
   return x
  for path in (ROOT/'corpus').glob('*/*.json'):
   text=path.read_text()
   if '"'+self.pid+'"'in text:
    d=project(json.loads(text));values[str(path.relative_to(ROOT))]=d
    if d.get('record_type')=='marked_chapter':values[str(path.with_suffix('.xml').relative_to(ROOT))]=render(d)
  values['registry/persons.json']=project(self.reg)
  path=ROOT/'data/corpus/profile-names.json'
  if '"'+self.pid+'"'in path.read_text():values[str(path.relative_to(ROOT))]=project(json.loads(path.read_text()))
  captures=[self.entry['primary']['observation_path'],self.entry['primary']['fixed_attempt_path']];before={p:refs.sha(refs.raw(ROOT,p))for p in captures}
  with self.overlay(values):
   ch,c,roles=proof(ROOT);self.assertEqual(roles['$guanling'],new);cat=load_catalog(ROOT);self.assertNotIn(self.pid,cat[0]);b=bundle(new,root=ROOT,catalog=cat);self.assertEqual(b['canonical_person_id'],new);self.assertTrue(any(m['id']==mid and m['person_id']==new for m in b['mentions']));self.assertEqual(before,{p:refs.sha(refs.raw(ROOT,p))for p in captures})
   self.assertEqual([m['id']for p in ch['paragraphs']for m in p['mentions']],[m['id']for p in self.ch['paragraphs']for m in p['mentions']])
if __name__=='__main__':unittest.main()
