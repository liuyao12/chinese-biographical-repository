import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.wyd_song044_direct_brothers import records,valid,applies,CID
ROOT=Path(__file__).resolve().parents[1]
class DirectBrotherTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_bytes());cls.cs={CID:cls.ch};cls.ps={p['id']:(CID,p)for p in cls.ch['paragraphs']};cls.rows=records(ROOT)
 def test_both_actual_records_are_source_bound(self):
  self.assertEqual(len(self.rows),2)
  for a in self.rows:self.assertTrue(valid(a,self.ps,self.cs,ROOT));self.assertTrue(applies(a));self.assertEqual(a['predicate'],'brother');self.assertEqual(a['qualifiers']['relative_birth_order']['younger_person_id'],a['subject_person_id'])
 def test_wrong_person_direction_or_order_reject(self):
  for source in self.rows:
   for field,value in [('subject_person_id','wrong'),('object_person_id','wrong')]:
    a=copy.deepcopy(source);a[field]=value;self.assertFalse(valid(a,self.ps,self.cs,ROOT))
   a=copy.deepcopy(source);a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(valid(a,self.ps,self.cs,ROOT))
   a=copy.deepcopy(source);o=a['qualifiers']['relative_birth_order'];o['older_person_id'],o['younger_person_id']=o['younger_person_id'],o['older_person_id'];self.assertFalse(valid(a,self.ps,self.cs,ROOT))
 def test_no_absolute_order_shared_parent_or_wedding(self):
  for source in self.rows:
   for key,value in [('shared_father',True),('shared_mother',True),('spouse','wrong')]:
    a=copy.deepcopy(source);a['qualifiers'][key]=value;self.assertFalse(valid(a,self.ps,self.cs,ROOT))
   a=copy.deepcopy(source);a['qualifiers']['relative_birth_order']['younger_ordinal']=2;self.assertFalse(valid(a,self.ps,self.cs,ROOT))
 def test_cross_paragraph_and_anchor_shift_reject(self):
  for key in ['paragraph_id','subject_person_mention_id','object_person_mention_id']:
   a=copy.deepcopy(self.rows[0]);a['evidence'][0][key]=self.rows[1]['evidence'][0][key];self.assertFalse(valid(a,self.ps,self.cs,ROOT))
  a=copy.deepcopy(self.rows[0]);a['evidence'][0]['relationship_anchor']['start']+=1;self.assertFalse(valid(a,self.ps,self.cs,ROOT))
 def test_single_endpoint_source_rekey_and_wrong_kind_reject(self):
  for edit in ['pid','kind']:
   c=copy.deepcopy(self.ch);p=next(p for p in c['paragraphs']if p['id'].endswith('p003'));m=next(m for m in p['mentions']if m['id'].endswith('m0325'));m['person_id']='ab1_cd2_ef3'if edit=='pid'else m['person_id'];m['kind']='unresolved'if edit=='kind'else m['kind'];self.assertFalse(valid(self.rows[0],{p['id']:(CID,p)for p in c['paragraphs']},{CID:c},ROOT))
 def test_changed_complete_text_plus_shift_reject(self):
  c=copy.deepcopy(self.ch);p=next(p for p in c['paragraphs']if p['id'].endswith('p003'));p['text']='字'+p['text']
  for m in p['mentions']:m['start']+=1;m['end']+=1
  self.assertFalse(valid(self.rows[0],{p['id']:(CID,p)for p in c['paragraphs']},{CID:c},ROOT))
 def test_source_metadata_and_missing_binding_reject(self):
  c=copy.deepcopy(self.ch);c['source']['revision']='wrong';self.assertFalse(valid(self.rows[0],self.ps,{CID:c},ROOT))
  a=copy.deepcopy(self.rows[0]);del a['qualifiers']['source_clause_binding'];self.assertTrue(applies(a));self.assertFalse(valid(a,self.ps,self.cs,ROOT))
 def test_consistent_current_reference_rekey_not_historical_capture_rewrite(self):
  ids={v for a in self.rows for v in [a['subject_person_id'],a['object_person_id']]};mp={v:n for v,n in zip(sorted(ids),['ab1_cd2_ef3','ab1_cd2_ef4','ab1_cd2_ef5','ab1_cd2_ef6'])}
  def remap(v):
   if isinstance(v,str):return mp.get(v,v)
   if isinstance(v,list):return[remap(x)for x in v]
   if isinstance(v,dict):return{k:remap(x)for k,x in v.items()}
   return v
  original_b=Path.read_bytes;original_t=Path.read_text
  def rb(p):
   raw=original_b(p)
   try:rel=p.relative_to(ROOT)
   except ValueError:return raw
   if p.suffix=='.json'and rel.parts[0]in('corpus','registry'):return json.dumps(remap(json.loads(raw)),ensure_ascii=False).encode()
   return raw
  def rt(p,*args,**kwargs):
   try:rel=p.relative_to(ROOT)
   except ValueError:return original_t(p,*args,**kwargs)
   return rb(p).decode(kwargs.get('encoding')or'utf-8')if p.suffix=='.json'and rel.parts[0]in('corpus','registry')else original_t(p,*args,**kwargs)
  with patch.object(Path,'read_bytes',rb),patch.object(Path,'read_text',rt):
   c=remap(self.ch);rows=records(ROOT,c)
   for a in rows:self.assertTrue(valid(a,{p['id']:(CID,p)for p in c['paragraphs']},{CID:c},ROOT))
 def test_malformed_inputs_fail_closed(self):
  for bad in [None,[],{},'bad']:
   self.assertFalse(valid(bad,self.ps,self.cs,ROOT));self.assertFalse(valid(self.rows[0],bad,self.cs,ROOT));self.assertFalse(valid(self.rows[0],self.ps,bad,ROOT))
if __name__=='__main__':unittest.main()
