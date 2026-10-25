import copy,json,unittest
from pathlib import Path
from scripts.fixed_kanripo_fact_slots import valid,records
ROOT=Path(__file__).resolve().parents[1]
class FamilyBNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/sanguozhi/023-peiqian.json').read_text());cls.ns=json.loads((ROOT/'corpus/sanguozhi/023-peiqian-familyb-name-components.json').read_text())['records'];cls.proof=json.loads((ROOT/'source-evidence/sgz023-peiqian-familyb-names/proofs.json').read_text())['records']
 def test_eight_native_names_in_current_finite_recipe(self):
  self.assertEqual(len(self.ns),8);self.assertEqual({n['ming']for n in self.ns},set('苞純盾郃廓瓚憲遐'));self.assertTrue(all(valid(n,self.ch,ROOT)for n in self.ns))
  expected=[r for r in records(self.ch,ROOT)if r['fixed_source_fact_binding']['slot'].startswith(('pqt-','phaseb-name-'))];self.assertEqual(len(expected),76);self.assertEqual(sum(r['fixed_source_fact_binding']['slot'].startswith('pqt-')for r in expected),68);self.assertEqual(sum(r['fixed_source_fact_binding']['slot'].startswith('phaseb-name-')for r in expected),8);actual=[]
  for path in (ROOT/'corpus/sanguozhi').glob('*.json'):
   row=json.loads(path.read_text())
   if row.get('chapter_id')!=self.ch['id']:continue
   for field in ('assertions','holdings','records','events'):
    actual.extend(r for r in row.get(field,[])if r.get('fixed_source_fact_binding',{}).get('key')==self.ch['annotation']['fixed_kanripo_fact_slots_ref']['key']and r.get('fixed_source_fact_binding',{}).get('slot','').startswith(('pqt-','phaseb-name-')))
  self.assertEqual(len(actual),76);self.assertEqual(len({r['id']for r in actual}),76);self.assertEqual({r['id']:r for r in actual},{r['id']:r for r in expected});self.assertTrue(all(valid(r,self.ch,ROOT)for r in actual))
  unknown=copy.deepcopy(self.ns[0]);unknown['fixed_source_fact_binding']['slot']='phaseb-name-not-reviewed';self.assertFalse(valid(unknown,self.ch,ROOT));unknown['id']='nc-sgz023-not-reviewed';self.assertFalse(valid(unknown,self.ch,ROOT))
 def test_all_components_are_exact_source_roles_not_labels(self):
  ps={p['id']:p for p in self.ch['paragraphs']}
  for n,q in zip(self.ns,self.proof):
   p=ps[q['paragraph_id']];m=next(m for m in p['mentions']if m['id']==q['source_mid']);self.assertEqual(n['person_id'],m['person_id']);self.assertEqual(n['person_mention_id'],m['id']);self.assertEqual(n['quote'],p['text']);self.assertEqual(m['surface'],q['source_name_anchor']['surface']);self.assertEqual(p['text'][q['ming_anchor']['start']:q['ming_anchor']['end']],n['ming'])
   if q['name_form']=='explicit_full_name':self.assertEqual(m['surface'],n['surname']+n['ming']);self.assertEqual(p['text'][q['surname_anchor']['start']:q['surname_anchor']['end']],n['surname'])
   else:self.assertEqual(q['name_form'],'ming_only');self.assertIsNone(n['surname']);self.assertEqual(m['surface'],n['ming'])
 def test_he_full_name_uses_m0047(self):
  n=next(n for n in self.ns if n['ming']=='郃');self.assertEqual((n['surname'],n['ming']),('裴','郃'));self.assertEqual(n['person_mention_id'],'c-sanguozhi-023-peiqian:p013:m0047');p=next(p for p in self.ch['paragraphs']if p['id']=='c-sanguozhi-023-peiqian:p013');m=next(m for m in p['mentions']if m['id']==n['person_mention_id']);self.assertEqual((m['start'],m['end'],m['surface']),(47,49,'裴郃'));self.assertNotIn('surname_basis',n)
 def test_no_blanket_surname_or_alias_replacement(self):
  for n in self.ns:
   bad=copy.deepcopy(n)
   if n['ming']=='郃':bad['ming']='邵'
   else:bad['surname']='裴'
   self.assertFalse(valid(bad,self.ch,ROOT))
 def test_co_moved_wrong_name_mid_still_rejected(self):
  n=copy.deepcopy(next(n for n in self.ns if n['ming']=='郃'));mid='c-sanguozhi-023-peiqian:p013:m0021';n['person_mention_id']=mid;n['evidence'][0]['person_mention_id']=mid;self.assertFalse(valid(n,self.ch,ROOT))
 def test_wrong_person_and_role_kind_rejected(self):
  n=copy.deepcopy(self.ns[0]);n['person_id']=self.ns[1]['person_id'];self.assertFalse(valid(n,self.ch,ROOT));ch=copy.deepcopy(self.ch);next(m for m in next(p for p in ch['paragraphs']if p['id']=='c-sanguozhi-023-peiqian:p013')['mentions']if m['id'].endswith(':m0047'))['kind']='unresolved';self.assertFalse(valid(self.ns[3],ch,ROOT))
 def test_coherent_current_rekey_follows_mid_without_surname_guess(self):
  ch=copy.deepcopy(self.ch);original=next(n['person_id']for n in self.ns if n['ming']=='郃');new='q8x_v4n_9t2'
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')==original:m['person_id']=new
  got=next(n for n in records(ch,ROOT)if n['id'].endswith('phaseb-name-he'));self.assertEqual(got['person_id'],new);self.assertEqual((got['surname'],got['ming']),('裴','郃'));self.assertEqual(got['person_mention_id'],'c-sanguozhi-023-peiqian:p013:m0047')
if __name__=='__main__':unittest.main()
