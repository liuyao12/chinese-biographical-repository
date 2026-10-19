# coding: utf-8
import copy,json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.person_bundle import load_catalog
from scripts.family_assemblies import load_assemblies
from scripts.uncle_parentage import parent_through_paternal_uncle_valid
class UncleChildListExtensionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cat=load_catalog(ROOT);_,cls.rows=load_assemblies(ROOT,cat);cls.assertions={a['id']:a for r in cat[1] if r.get('record_type')=='person_assertion_set' for a in r['assertions']};cls.chapters={r['id']:r for r in cat[1] if r.get('record_type')=='marked_chapter'}
  cls.own='aa6_83c_juy_C';cls.child='aa6_83c_juy_CD';cls.an='aa6_83c_juy_B';cls.parent='aa6_83c_juy';cls.nfid='a-jinshu079-expansion-009';cls.nuid='a-jinshu079-xie-005';cls.ufid='a-jinshu079-xie-001'
  cls.pids=['c-jinshu-079-xielang-family:exp-xieyi-p001','c-jinshu-079-xielang-family:exp-xieyi-p002','c-jinshu-079-xielang-family:p002'];cls.cid='c-jinshu-079-xielang-family'
 def setUp(self):
  self.rr=copy.deepcopy(self.rows);self.aa={k:copy.deepcopy(v) for k,v in self.assertions.items()};self.cc={self.cid:copy.deepcopy(self.chapters[self.cid])}
  # A candidate object only: no registry ID or stored assembly is edited.
  self.m=copy.deepcopy(self.rr[self.own]);self.m.update(parent_person_id=self.parent,source_assertion_id=None,connection='father')
  refs=[]
  for aid in [self.nfid,self.nuid,self.ufid]:
   for e in self.aa[aid]['evidence']:refs.append({**e,'assertion_id':aid,'url':self.cc[self.cid]['source']['url'],'scope':'完整既有原生證據；奕父裒是可撤回推論。'})
  self.m['parent_connection']={'type':'parent_through_paternal_uncle','nephew_person_id':self.child,'uncle_person_id':self.an,'nephew_father_assertion_id':self.nfid,'nephew_uncle_assertion_id':self.nuid,'uncle_father_assertion_id':self.ufid,'status':'contextual_provisional','human_reviewed':False,'rationale':'完整父傳及三子名單、玄傳首叔父安、安父裒，引用四筆全不刪。','references':refs};self.rr[self.own]=self.m
 def ok(self):return parent_through_paternal_uncle_valid(self.m,self.rr,self.aa,self.cc)
 def paragraph(self,i):return next(p for p in self.cc[self.cid]['paragraphs'] if p['id']==self.pids[i])
 def sync_quote(self,i):
  p=self.paragraph(i)
  for a in self.aa.values():
   for e in a.get('evidence',[]):
    if e.get('paragraph_id')==p['id']:e['quote']=p['text']
  for ref in self.m['parent_connection']['references']:
   if ref['paragraph_id']==p['id']:ref['quote']=p['text']
 def test_complete_four_refs_accepts_without_forged_source_father(self):
  self.assertTrue(self.ok());self.assertEqual(len(self.m['parent_connection']['references']),4);self.assertIsNone(self.m['source_assertion_id']);self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']==self.own for a in self.aa.values()))
 def test_old_three_ref_same_paragraph_branch_still_accepts(self):
  member=self.rows['aa6_83c_juy_A'];self.assertTrue(parent_through_paternal_uncle_valid(member,self.rows,self.assertions,self.chapters));self.assertEqual(len(member['parent_connection']['references']),3)
 def test_old_three_ref_branch_rejects_extra_reference(self):
  rows=copy.deepcopy(self.rows);member=rows['aa6_83c_juy_A'];member['parent_connection']['references'].append(copy.deepcopy(member['parent_connection']['references'][0]));self.assertFalse(parent_through_paternal_uncle_valid(member,rows,self.assertions,self.chapters))
 def test_wrong_uncle(self):
  self.m['parent_connection']['uncle_person_id']=self.parent;self.assertFalse(self.ok())
 def test_wrong_father_assertion(self):
  self.m['parent_connection']['uncle_father_assertion_id']=self.nfid;self.assertFalse(self.ok())
 def test_wrong_nephew_father(self):
  self.aa[self.nfid]['object_person_id']=self.an;self.assertFalse(self.ok())
 def test_maternal_uncle_does_not_supply_paternal_edge(self):
  self.aa[self.nuid]['predicate']='maternal_uncle';self.assertFalse(self.ok())
 def test_cycle(self):
  self.m['parent_connection']['nephew_person_id']=self.own;self.assertFalse(self.ok())
 def test_explicit_conflicting_father(self):
  self.aa['conflict']={'id':'conflict','predicate':'father','subject_person_id':self.own,'object_person_id':'other-father'};self.assertFalse(self.ok())
 def test_source_not_attested(self):
  self.aa[self.nfid]['status']='contextual_provisional';self.assertFalse(self.ok())
 def test_drop_parent_reference_does_not_fake_three_refs(self):
  self.m['parent_connection']['references'].pop(0);self.assertFalse(self.ok())
 def test_duplicate_ref_does_not_replace_list_ref(self):
  self.m['parent_connection']['references'][1]=copy.deepcopy(self.m['parent_connection']['references'][0]);self.assertFalse(self.ok())
 def test_partial_quote_not_full_body(self):
  self.m['parent_connection']['references'][0]['quote']='奕字無奕';self.assertFalse(self.ok())
 def test_unknown_assertion_id(self):
  self.m['parent_connection']['references'][0]['assertion_id']='not-validated';self.assertFalse(self.ok())
 def test_wrong_child_anchor_position(self):
  p=self.paragraph(1);m=next(m for m in p['mentions'] if m.get('person_id')==self.child);m['start']+=1;self.assertFalse(self.ok())
 def test_wrong_child_count(self):
  p=self.paragraph(1);p['text']=p['text'].replace('三子','四子',1);self.aa[self.nfid]['qualifiers']['source_term']='四子';self.sync_quote(1);self.assertFalse(self.ok())
 def test_duplicate_child_identity(self):
  p=self.paragraph(1);p['mentions'][0]['person_id']=self.child;self.assertFalse(self.ok())
 def test_wrong_parent_topic(self):
  p=self.paragraph(0);p['mentions'][0]['person_id']=self.an;self.assertFalse(self.ok())
 def test_cross_biography_opening(self):
  p=self.paragraph(2);p['text']='朗'+p['text'][1:];p['mentions'][0]['surface']='朗';self.sync_quote(2);self.assertFalse(self.ok())
 def test_intervening_received_body_is_not_skipped(self):
  chapter=self.cc[self.cid];p=copy.deepcopy(self.paragraph(1));p['id']='inserted-body';p['text']='另人傳文。';p['mentions']=[];at=chapter['paragraphs'].index(self.paragraph(2));chapter['paragraphs'].insert(at,p);self.assertFalse(self.ok())
 def test_wrong_fixed_revision(self):
  self.paragraph(2)['source_position']['revision_id']=1;self.assertFalse(self.ok())
 def test_cross_chapter(self):
  self.aa[self.nuid]['evidence'][0]['chapter_id']='other-chapter';self.assertFalse(self.ok())
 def test_wrong_source_id(self):
  self.aa[self.nfid]['evidence'][1]['source_id']='other-source';self.assertFalse(self.ok())
 def test_missing_layout_receipt_does_not_skip_raw_lines(self):
  norm=self.cc[self.cid]['source']['normalization'];norm['omitted_digital_paratext']=[x for x in norm['omitted_digital_paratext'] if x['source_lines']!=[79,80]];self.assertFalse(self.ok())
 def test_layout_heading_with_received_body_is_rejected(self):
  import hashlib
  record=next(x for x in self.cc[self.cid]['source']['normalization']['omitted_digital_paratext'] if x['source_lines']==[79,80]);record['raw_quote']='===奕子 玄===\n正文不可跳過';record['raw_quote_sha256']=hashlib.sha256(record['raw_quote'].encode()).hexdigest();self.assertFalse(self.ok())
 def test_wrong_layout_hash(self):
  record=next(x for x in self.cc[self.cid]['source']['normalization']['omitted_digital_paratext'] if x['source_lines']==[79,80]);record['raw_quote_sha256']='0'*64;self.assertFalse(self.ok())
 def test_commentary_is_not_received_parent_biography(self):
  self.paragraph(0)['text_layer']='witness_appended_bangu_note';self.assertFalse(self.ok())
 def test_list_context_must_be_explicit_existing_adjacent_assertion(self):
  self.aa[self.nfid]['context']['kind']='arbitrary_distant_passages';self.assertFalse(self.ok())
 def test_list_order_is_not_sibling_ordinal(self):
  self.assertTrue(self.ok());self.assertNotIn('ordinal',str(self.m));self.assertNotIn('relative_birth_order',str(self.m))
 def test_wan_and_shi_use_existing_sibling_inference_model(self):
  from scripts.family_assemblies import brother_connects
  father=self.aa[self.ufid]
  for pid in ['aa6_83c_juy_D','aa6_83c_juy_E']:
   brother=next(a for a in self.aa.values() if a['predicate']=='brother' and a['subject_person_id']==pid and a['object_person_id']==self.an)
   self.assertTrue(brother_connects(brother,[pid],[self.an]));self.assertEqual(father['object_person_id'],self.parent)
 def test_wan_and_shi_reject_explicit_different_father(self):
  from scripts.family_assemblies import brother_connects
  for pid in ['aa6_83c_juy_D','aa6_83c_juy_E']:
   brother=copy.deepcopy(next(a for a in self.aa.values() if a['predicate']=='brother' and a['subject_person_id']==pid and a['object_person_id']==self.an));brother['qualifiers']['shared_father']=False
   self.assertFalse(brother_connects(brother,[pid],[self.an]))
 def test_uncle_source_word_is_not_replaced_by_generic_kin(self):
  p=self.paragraph(2);p['text']=p['text'].replace('叔父安','伯父安');self.sync_quote(2);self.assertFalse(self.ok())
 def test_father_lineage_not_maternal(self):
  self.aa[self.ufid]['qualifiers']['lineage']='maternal';self.assertFalse(self.ok())
 def test_in_memory_canonical_id_change_preserves_proof(self):
  mapping={self.own:'aa6_83c_juy_C'}
  for pid in self.rr:
   if pid.startswith(self.own+'_'):mapping[pid]='aa6_83c_juy_C'+pid[len(self.own)+1:]
  def remap(value):
   if isinstance(value,str):return mapping.get(value,value)
   if isinstance(value,list):return [remap(v) for v in value]
   if isinstance(value,dict):return {mapping.get(k,k):remap(v) for k,v in value.items()}
   return value
  self.assertTrue(parent_through_paternal_uncle_valid(remap(self.m),remap(self.rr),remap(self.aa),remap(self.cc)))
 def test_transitive_parent_cycle(self):
  self.rr[self.parent]['parent_person_id']=self.child;self.assertFalse(self.ok())
 def test_precise_whole_paragraph_quote_ranges(self):
  for ref in self.m['parent_connection']['references']:ref.update(quote_start=0,quote_end=len(ref['quote']))
  self.assertTrue(self.ok());self.m['parent_connection']['references'][0]['quote_start']=1;self.assertFalse(self.ok())
if __name__=='__main__':unittest.main(verbosity=2)
