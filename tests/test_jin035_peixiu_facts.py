"""Complete-source facts: maternal contrast, quote scope, age and calendar fences."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import fixed_witness_fact_slots as facts
ROOT=Path(__file__).resolve().parents[1]
CID='c-jinshu-035-peixiu';CP='corpus/jinshu/035-peixiu.json';KEY='jin035-peixiu-finite'
class PeixiuFacts(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/CP).read_text());self.r=copy.deepcopy(facts.recipes()[KEY]);self.pin=json.loads((ROOT/'scripts/fixed_attached_subsection_witnesses.json').read_text())['chapters'][CID]
 def transaction(self,c=None,r=None):
  c=copy.deepcopy(c or self.c);r=copy.deepcopy(r or self.r)
  with tempfile.TemporaryDirectory()as td:
   root=Path(td);rels=[self.pin['raw_file'],self.pin['projection_ref'],self.pin['embedded_document']['subject_resolution_seed']['chapter_path']]+[x['raw_file']for x in self.r['calendar_references']]
   for rel in rels:
    p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/rel).read_bytes())
   p=root/CP;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(c,ensure_ascii=False))
   p=root/'scripts/fixed_attached_subsection_witnesses.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps({'format_version':'0.1','chapters':{CID:self.pin}}))
   with patch.object(facts,'recipes',return_value={KEY:r}):return facts.records(c,root)
 def reject(self,c=None,r=None):
  with self.assertRaises((AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,OSError)):self.transaction(c,r)
 def slot(self,r,name):return next(s['record']for s in r['slots']if s['slot']==name)
 def test_all_records_and_bounded_mothers(self):
  vs=self.transaction();self.assertEqual(len(vs),97);mom=next(v for v in vs if v.get('fixed_source_fact_binding',{}).get('slot')=='kin-010');principal=next(v for v in vs if v.get('fixed_source_fact_binding',{}).get('slot')=='kin-011')
  self.assertNotEqual(mom['object_person_id'],principal['object_person_id']);self.assertFalse(mom['qualifiers']['maternal_interpretation']['source_explicit_birth']);self.assertEqual(principal['qualifiers']['role'],'principal_mother');self.assertIsNone(principal['qualifiers']['biological_mother']);self.assertFalse(any(v.get('predicate')=='spouse'for v in vs))
 def test_maternal_record_cannot_claim_explicit_birth(self):
  r=copy.deepcopy(self.r);self.slot(r,'kin-010')['qualifiers']['maternal_interpretation']['source_explicit_birth']=True;self.reject(r=r)
 def test_mother_role_swap_and_same_person_rejected(self):
  for collapse in (False,True):
   c=copy.deepcopy(self.c);p=c['paragraphs'][0];mother=[m for m in p['mentions']if m['surface']=='秀母'];principal=[m for m in p['mentions']if m['surface']in('嫡母宣氏','宣氏')];a=mother[0]['person_id'];b=principal[0]['person_id']
   for m in mother:m['person_id']=b
   if not collapse:
    for m in principal:m['person_id']=a
   # record endpoints remain bound to their named semantic roles; proof cannot swap birth interpretation.
   r=copy.deepcopy(self.r);proof=r['maternal_context_proofs'][0];proof['record_roles']['object']=[0,'xuan0'];self.reject(c,r)
 def test_contrast_or_denial_cannot_cochange_source(self):
  for old,new in [('嫡母','其母'),('秀母賤','非秀母賤')]:
   c=copy.deepcopy(self.c);c['paragraphs'][0]['text']=c['paragraphs'][0]['text'].replace(old,new,1);self.reject(c)
 def test_quote_scope_and_wrong_layer_rejected(self):
  vs=self.transaction();quoted=[v for v in vs if v.get('source_evidence_scope',{}).get('kind')=='received_embedded_work_preface'];self.assertEqual(len(quoted),2)
  for n in (0,7,8):
   c=copy.deepcopy(self.c);c['paragraphs'][n]['source_position']['source_layer']='received_quoted_document'if n==0 else'received_biography';self.reject(c)
 def test_open_age_and_death_age_are_not_birth(self):
  vs=self.transaction();age=next(v for v in vs if v.get('fixed_source_fact_binding',{}).get('slot')=='age-009');self.assertIsNone(age['value']);self.assertEqual(age['bounds'],{'lower':10,'lower_inclusive':False,'upper':None,'upper_inclusive':None});self.assertIsNone(age['birth_year'])
  deathage=next(v for v in vs if v.get('fixed_source_fact_binding',{}).get('slot')=='age-066');self.assertEqual(deathage['value'],48);self.assertEqual(deathage['age_context']['kind'],'at_death')
  r=copy.deepcopy(self.r);self.slot(r,'age-009')['birth_year']=250;self.reject(r=r)
 def test_exact_271_not_other_era_or_office_end(self):
  vs=self.transaction();death=next(v for v in vs if v.get('fixed_source_fact_binding',{}).get('slot')=='death-xiu');self.assertEqual(death['normalized_date']['year'],271)
  self.assertTrue(all(v['effective_period']['end']['status']=='unknown'for v in vs if 'effective_period'in v))
  for field,value in [('year',471),('year',270)]:
   r=copy.deepcopy(self.r);self.slot(r,'death-xiu')['normalized_date'][field]=value;self.reject(r=r)
 def test_era_phase_keeps_full_range(self):
  vs=self.transaction();ranges=[v['normalized_date_range']for v in vs if 'normalized_date_range'in v];self.assertEqual([(v['earliest']['year'],v['latest']['year'])for v in ranges],[(264,265),(275,280)])
  r=copy.deepcopy(self.r);self.slot(r,'detail-034')['normalized_date_range']['latest']['year']=264;self.reject(r=r)
 def test_actor_group_and_title_patient_cannot_exchange(self):
  c=copy.deepcopy(self.c);ms=[m for m in c['paragraphs'][2]['mentions']if m['kind']=='person'];x=next(m for m in ms if m['surface']=='秀');other=next(m for m in ms if m['surface']=='陳泰');x['person_id']=other['person_id'];self.reject(c)
 def test_complete_witness_not_truncated_or_missing_role(self):
  c=copy.deepcopy(self.c);c['paragraphs'].pop();self.reject(c)
  c=copy.deepcopy(self.c);c['paragraphs'][0]['mentions'].pop(0);self.reject(c)
 def test_principal_role_is_not_stepmother_or_unspecified(self):
  for pred,role in [('stepmother','principal_mother'),('maternal_role','mother_unspecified')]:
   r=copy.deepcopy(self.r);v=self.slot(r,'kin-011');v['predicate']=pred;v['qualifiers']['role']=role;self.reject(r=r)
 def test_principal_record_must_point_to_distinct_named_role(self):
  r=copy.deepcopy(self.r);self.slot(r,'kin-011')['object_person_id']=copy.deepcopy(self.slot(r,'kin-010')['object_person_id']);self.reject(r=r)
 def test_principal_contrast_cannot_lose_explicit_word_or_move_anchor(self):
  r=copy.deepcopy(self.r);r['maternal_context_proofs'][0]['principal_mother_contrast']['contrast_anchor']['start']+=1;self.reject(r=r)
  r=copy.deepcopy(self.r);r['maternal_context_proofs'][0]['principal_mother_contrast']['principal_roles']=['mother0','mother1'];self.reject(r=r)
if __name__=='__main__':unittest.main()
