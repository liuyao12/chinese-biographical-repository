import copy,json,unittest
from pathlib import Path
from scripts.fixed_kanripo_fact_slots import records,valid
from scripts.surname_from_father import validate as surname_valid
ROOT=Path(__file__).resolve().parents[1]
class ContextualPeiSurnames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/sanguozhi/023-peiqian.json').read_text());cls.all=records(cls.ch,ROOT);cls.names=[r for r in cls.all if r.get('fixed_source_fact_binding',{}).get('slot','').startswith('phaseb-surname-')];cls.seed=next(r for r in cls.names if 'surname_basis'not in r);cls.aa={a['id']:a for a in cls.all if a.get('predicate')=='father'};cls.literal=json.loads((ROOT/'corpus/sanguozhi/023-peiqian-familyb-name-components.json').read_text())['records']
 def walk(self,n,aa=None,seed=None):
  aa=aa or self.aa;seed=seed or self.seed;b=n['surname_basis'];self.assertEqual(b['kind'],'contextual_surname_from_fixed_kanripo_slots');self.assertEqual(n['status'],'contextual_provisional');self.assertIs(b['human_reviewed'],False);self.assertEqual(b['seed_name_record_id'],seed['id']);self.assertEqual(b['seed_person_id'],seed['person_id']);self.assertEqual(b['source_full_quote'],seed['quote']);self.assertNotIn('surname_basis',seed);self.assertEqual(seed['surname'],'裴');self.assertEqual(seed['ming'],'楷')
  cur=seed['person_id'];g=0;seen={cur};self.assertTrue(1<=len(b['steps'])<=3);self.assertEqual(b['assertion_ids'],[s['assertion_id']for s in b['steps']])
  for s in b['steps']:
   a=aa[s['assertion_id']];self.assertEqual(a['predicate'],'father');self.assertEqual(a['status'],'source_attested');self.assertEqual(a['qualifiers'].get('lineage'),'paternal');self.assertFalse(any(a['qualifiers'].get(k)for k in ('adoptive','same_mother_only','sworn')));self.assertEqual(s['evidence'],a['evidence']);self.assertEqual(s['from_person_id'],cur);self.assertEqual(s['generation_before'],g)
   if s['traversal']=='child_to_father':self.assertEqual((cur,s['to_person_id']),(a['subject_person_id'],a['object_person_id']));g-=1
   else:self.assertEqual(s['traversal'],'father_to_child');self.assertEqual((cur,s['to_person_id']),(a['object_person_id'],a['subject_person_id']));g+=1
   self.assertEqual(s['generation_after'],g);cur=s['to_person_id'];self.assertNotIn(cur,seen);seen.add(cur)
  self.assertEqual(cur,n['person_id'])
 def test_all84_complete_native_slots_and_unknown_reject(self):
  self.assertEqual(len(self.all),84);self.assertEqual(len(self.names),8);self.assertEqual(sum('surname_basis'in n for n in self.names),7);actual=[]
  for f in (ROOT/'corpus/sanguozhi').glob('*.json'):
   r=json.loads(f.read_text())
   if r.get('chapter_id')!=self.ch['id']:continue
   for field in ('assertions','holdings','records','events'):actual.extend(a for a in r.get(field,[])if a.get('fixed_source_fact_binding',{}).get('key')==self.ch['annotation']['fixed_kanripo_fact_slots_ref']['key'])
  self.assertEqual(len(actual),84);self.assertEqual({r['id']:r for r in actual},{r['id']:r for r in self.all});bad=copy.deepcopy(self.names[1]);bad['fixed_source_fact_binding']['slot']='not-reviewed';self.assertFalse(valid(bad,self.ch,ROOT))
 def test_explicit_seed_is_pei_kai_not_cai_or_label(self):
  p=next(p for p in self.ch['paragraphs']if p['id']==self.seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==self.seed['person_mention_id']);self.assertEqual(m['surface'],'裴楷');self.assertEqual(m['surface'],self.seed['surname']+self.seed['ming']);self.assertEqual(m['person_id'],self.seed['person_id']);self.assertEqual(self.seed['status'],'source_attested');self.assertNotEqual(self.seed['ming'],'凱')
 def test_seven_positive_paths_and_existing_surname_contract(self):
  for n in self.names:
   self.assertTrue(valid(n,self.ch,ROOT))
   if 'surname_basis'in n:self.walk(n);surname_valid(n,self.names,{self.ch['id']:self.ch},list(self.aa.values()),root=ROOT)
 def test_source_single_name_rows_remain_distinct_and_unchanged(self):
  raw={n['id']:n for n in self.literal};self.assertEqual(len(raw),8)
  for n in self.names:
   if 'surname_basis'not in n:continue
   source=raw[n['surname_basis']['source_token_name_record_id']];self.assertIsNone(source['surname']);self.assertEqual(source['ming'],n['ming']);self.assertEqual(source['person_id'],n['person_id']);self.assertEqual(source['person_mention_id'],n['person_mention_id']);self.assertEqual(source['quote'],n['quote']);self.assertNotIn('surname_basis',source)
 def test_wrong_maternal_adoptive_or_affine_path_rejected(self):
  n=next(n for n in self.names if 'surname_basis'in n)
  for pred in ['mother','adoptive_father','spouse','brother']:
   aa=copy.deepcopy(self.aa);aa[n['surname_basis']['assertion_ids'][0]]['predicate']=pred
   with self.assertRaises(AssertionError):self.walk(n,aa=aa)
  bad=copy.deepcopy(n);bad['surname_basis']['steps'][0]['traversal']='spouse_to_person';self.assertFalse(valid(bad,self.ch,ROOT))
 def test_wrong_seed_unknown_father_and_as_explicit_rejected(self):
  n=next(n for n in self.names if 'surname_basis'in n);bad=copy.deepcopy(n);bad['surname_basis']['seed_name_record_id']=self.literal[3]['id'];self.assertFalse(valid(bad,self.ch,ROOT));bad=copy.deepcopy(n);bad['status']='source_attested';self.assertFalse(valid(bad,self.ch,ROOT));aa=copy.deepcopy(self.aa);aa.pop(n['surname_basis']['assertion_ids'][0])
  with self.assertRaises(KeyError):self.walk(n,aa=aa)
 def test_bao_requires_three_explicit_edges_without_mao_hui(self):
  n=next(n for n in self.names if n['ming']=='苞');self.assertEqual(len(n['surname_basis']['steps']),3);self.assertEqual(n['surname_basis']['assertion_ids'],['a-sgz023-peiqian-pqt-010','a-sgz023-peiqian-pqt-008','a-sgz023-peiqian-pqt-012']);self.assertNotIn('a-sgz023-peiqian-pqt-004',n['surname_basis']['assertion_ids'])
 def test_missing_or_reversed_edge_rejected(self):
  n=next(n for n in self.names if 'surname_basis'in n);bad=copy.deepcopy(n);s=bad['surname_basis']['steps'][0];s['from_person_id'],s['to_person_id']=s['to_person_id'],s['from_person_id'];self.assertFalse(valid(bad,self.ch,ROOT))
  with self.assertRaises(AssertionError):self.walk(bad)
 def test_coherent_source_rekey_updates_seed_and_steps(self):
  ch=copy.deepcopy(self.ch);old=self.seed['person_id'];new='q8x_v4n_9t2'
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')==old:m['person_id']=new
  allnew=records(ch,ROOT);seed=next(n for n in allnew if n.get('id')==self.seed['id']);aa={a['id']:a for a in allnew if a.get('predicate')=='father'}
  for n in allnew:
   if n.get('surname_basis',{}).get('seed_name_record_id')==seed['id']:self.walk(n,aa=aa,seed=seed);self.assertEqual(n['surname'],'裴')
if __name__=='__main__':unittest.main()
