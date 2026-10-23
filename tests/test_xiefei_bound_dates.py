import copy,json,tempfile,unittest,shutil
from pathlib import Path
from scripts.fixed_primary_biography_dates import valid,file
from scripts.validate_corpus import normalized_date_errors
R=Path(__file__).resolve().parents[1]
class BoundDateTests(unittest.TestCase):
 def setUp(self):
  load=lambda p:json.loads((R/p).read_text());self.ch=load('corpus/liangshu/015-xiefei.json');self.chs={self.ch['id']:self.ch};self.life=load('corpus/liangshu/015-xiefei-life-events.json')['events'];self.hs=load('corpus/liangshu/015-xiefei-titles.json')['holdings'];self.e=next(e for e in self.life if e['id'].endswith('-fei'));self.d=self.e['normalized_date']
 def cases(self):
  yield self.e,'life_event',self.d
  for h in self.hs:
   for a in h['attestations']:
    if'fixed_primary_binding'in a.get('normalized_date',{}):yield h,'attestation',a['normalized_date']
   d=h.get('effective_period',{}).get('start',{}).get('normalized_date',{})
   if 'fixed_primary_binding'in d:yield h,'start',d
  for q in self.ch['annotation']['title_proposals']:
   if'fixed_primary_binding'in q.get('normalized_date',{}):yield q,'appointment_notice',q['normalized_date']
 def test_every_actual_holding_proposal_death_positive(self):
  cases=list(self.cases());self.assertEqual(16,len(cases))
  for record,role,d in cases:
   with self.subTest(role=role,id=record['id']):self.assertTrue(valid(d,self.chs,R,record,role));self.assertEqual([],normalized_date_errors(d,self.chs,root=R,bound_record=record,bound_role=role))
 def test_coherent_wrong_record_recipient_at_central_dispatch(self):
  for record,role,d in self.cases():
   r=copy.deepcopy(record);p=next(p for p in self.ch['paragraphs']if p['id']==r['evidence'][0]['paragraph_id']);m=next(m for m in p['mentions']if m['surface']in('輿駕','高祖'));r['person_id']=m['person_id'];r['evidence'][0]['person_mention_id']=m['id']
   if role=='attestation':r['attestations'][0]['person_mention_id']=m['id']
   if role=='appointment_notice':r['person_mention_id']=m['id']
   with self.subTest(role=role,id=r['id']):self.assertTrue(normalized_date_errors(d,self.chs,root=R,bound_record=r,bound_role=role))
 def test_wrong_event_or_title_not_just_date_evidence(self):
  r=copy.deepcopy(self.e);r['event_type']='birth';self.assertFalse(valid(self.d,self.chs,R,r,'life_event'))
  for record,role,d in self.cases():
   if role=='attestation':
    r=copy.deepcopy(record);r['title']='國子博士';self.assertFalse(valid(d,self.chs,R,r,role));break
 def test_same_person_same_title_posthumous_slot_not_grant(self):
  record,role,d=next((r,role,d)for r,role,d in self.cases()if role=='attestation'and r['title']=='司徒'and d['year']==506)
  r=copy.deepcopy(record);t=self.ch['paragraphs'][7]['text'];lo=t.index('贈侍中、')+len('贈侍中、');a=r['attestations'][0];a['start']=lo;a['end']=lo+2;a['surface']='司徒'
  self.assertFalse(valid(d,self.chs,R,r,role))
 def test_no_bound_record_or_wrong_role_rejected(self):self.assertFalse(valid(self.d,self.chs,R));self.assertFalse(valid(self.d,self.chs,R,self.e,'attestation'))
 def test_raw_and_metadata_lexical_escape(self):
  for field in('raw_path','metadata_path'):
   for path in('../outside','sources/test','/tmp/outside'):
    d=copy.deepcopy(self.d);d['fixed_primary_binding'][field]=path;r=copy.deepcopy(self.e);r['normalized_date']=d
    with self.subTest(field=field,path=path):self.assertFalse(valid(d,self.chs,R,r,'life_event'))
 def test_final_and_intermediate_symlink_for_raw_and_metadata(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td)/'root';outside=Path(td)/'outside';root.mkdir();outside.mkdir();b=self.d['fixed_primary_binding']
   for field in('raw_path','metadata_path'):
    rel=Path(b[field]);f=root/rel;f.parent.mkdir(parents=True,exist_ok=True);target=outside/rel.name;shutil.copyfile(R/rel,target);f.symlink_to(target)
    with self.subTest(field=field,kind='final'):
     with self.assertRaises(ValueError):file(root,str(rel))
    f.unlink();shutil.copyfile(target,f)
   linked=root/'source-evidence'/'escaped';linked.symlink_to(outside,target_is_directory=True)
   for field in('raw_path','metadata_path'):
    rel=Path(b[field]);escaped='source-evidence/escaped/'+rel.name
    with self.subTest(field=field,kind='intermediate'):
     with self.assertRaises(ValueError):file(root,escaped)
 def test_actual_validator_symlink_archives_identical_bytes(self):
  with tempfile.TemporaryDirectory()as td:
   root=Path(td)/'root';outside=Path(td)/'outside';root.mkdir();outside.mkdir();b=self.d['fixed_primary_binding']
   for field in('raw_path','metadata_path'):
    rel=Path(b[field]);f=root/rel;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/rel,f);shutil.copyfile(R/rel,outside/rel.name)
   self.assertTrue(valid(self.d,self.chs,root,self.e,'life_event'))
   for field in('raw_path','metadata_path'):
    rel=Path(b[field]);f=root/rel;f.unlink();f.symlink_to(outside/rel.name)
    with self.subTest(field=field,kind='final-full-validator'):self.assertFalse(valid(self.d,self.chs,root,self.e,'life_event'))
    f.unlink();shutil.copyfile(R/rel,f)
   (root/'source-evidence'/'escaped').symlink_to(outside,target_is_directory=True)
   for field in('raw_path','metadata_path'):
    d=copy.deepcopy(self.d);d['fixed_primary_binding'][field]='source-evidence/escaped/'+Path(b[field]).name;r=copy.deepcopy(self.e);r['normalized_date']=d
    with self.subTest(field=field,kind='intermediate-full-validator'):self.assertFalse(valid(d,self.chs,root,r,'life_event'))
if __name__=='__main__':unittest.main()
