# coding:utf-8
import unittest,json,copy,subprocess,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import fixed_witness_fact_slots as f
class DuYuKinshipTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/jinshu/034-duyu.json').read_text());cls.a=json.loads((ROOT/'corpus/jinshu/034-duyu-assertions.json').read_text())['assertions'];cls.by={x['id'].split('a-jin034-duyu-')[1]:x for x in cls.a}
 def test_all_seven_source_slots(self):
  self.assertEqual(len(self.a),7);self.assertTrue(all(f.valid(a,self.c,ROOT)for a in self.a));self.assertFalse(f.errors(ROOT,[self.c]+[json.loads(p.read_text())for p in (ROOT/'corpus/jinshu').glob('034-duyu-*.json')]))
 def test_father_ancestor_separate_and_no_fake_middle(self):
  self.assertEqual(self.by['pre-grandfather']['predicate'],'grandfather');self.assertEqual(self.by['pre-father']['predicate'],'father');self.assertFalse(any(x['subject_person_id']==self.by['pre-father']['object_person_id']for x in self.a))
 def test_sister_female_subject_younger(self):
  a=self.by['princess-younger-sister'];self.assertEqual(a['subject_person_id'],self.by['pre-spouse']['object_person_id']);self.assertEqual(a['predicate'],'sister');self.assertEqual(a['qualifiers']['relative_age'],'younger');self.assertEqual(a['qualifiers']['relative_birth_order']['younger_person_id'],a['subject_person_id'])
 def test_no_mother_order_or_adoption(self):
  self.assertFalse(any(x['predicate']in ('mother','adoptive_father')for x in self.a));self.assertFalse(any('relative_birth_order'in x['qualifiers']for x in self.a if x['predicate']=='father'))
 def test_dan_context_binds_preceding_duyu_not_sunhao(self):
  a=self.by['dan-father'];self.assertEqual(a['object_person_id'],self.by['pre-father']['subject_person_id']);self.assertEqual(a['context']['kind'],'adjacent_paragraphs');self.assertEqual([e['paragraph_id']for e in a['evidence']],a['context']['paragraph_ids']);self.assertTrue(a['evidence'][1]['quote'].startswith('孫皓既平'))
 def test_consistent_swapped_roles_rejected(self):
  for a in self.a:
   b=copy.deepcopy(a);b['subject_person_id'],b['object_person_id']=b['object_person_id'],b['subject_person_id']
   for e in b['evidence']:
    s=e.pop('subject_person_mention_id',None);o=e.pop('object_person_mention_id',None)
    if s:e['object_person_mention_id']=s
    if o:e['subject_person_mention_id']=o
   self.assertFalse(f.valid(b,self.c,ROOT))
 def test_wrong_relationship_mother_rank_recipient_rejected(self):
  for key,field,value in [('pre-grandfather','predicate','father'),('dan-father','predicate','mother'),('xi-father','predicate','adoptive_father')]:
   a=copy.deepcopy(self.by[key]);a[field]=value;self.assertFalse(f.valid(a,self.c,ROOT))
  a=copy.deepcopy(self.by['princess-younger-sister']);a['qualifiers']['relative_age']='older';self.assertFalse(f.valid(a,self.c,ROOT))
 def test_layer_list_rejected_if_wrong_or_unknown(self):
  original=f.recipes();r=copy.deepcopy(original);r['jin034-duyu-kinship']['paragraph_layers'][3]='received_biography'
  with patch.object(f,'recipes',lambda:r):self.assertFalse(f.valid(self.a[0],self.c,ROOT))
  r['jin034-duyu-kinship']['paragraph_layers'][3]='website_editorial'
  with patch.object(f,'recipes',lambda:r):self.assertFalse(f.valid(self.a[0],self.c,ROOT))
 def test_legacy_recipe_without_layers_keeps_old_biography_rule(self):
  r=copy.deepcopy(f.recipes());r['jin034-duyu-kinship'].pop('paragraph_layers')
  with patch.object(f,'recipes',lambda:r):self.assertFalse(f.valid(self.a[0],self.c,ROOT))
 def test_missing_and_duplicate_slot_rejected(self):
  self.assertTrue(f.errors(ROOT,[self.c,{'chapter_id':self.c['id'],'assertions':self.a[:-1]}]));self.assertTrue(f.errors(ROOT,[self.c,{'chapter_id':self.c['id'],'assertions':self.a+[self.a[0]]}]))
 def test_real_cli_consistent_sister_swap_rejected_without_writes(self):
  code="""import runpy,json
from pathlib import Path
from unittest.mock import patch
p=Path('corpus/jinshu/034-duyu-assertions.json').resolve();d=json.loads(p.read_text());a=next(x for x in d['assertions']if x['predicate']=='sister');a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
for e in a['evidence']:e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
old=Path.read_text
def read(q,*a,**kw):return json.dumps(d,ensure_ascii=False)if q.resolve()==p else old(q,*a,**kw)
with patch.object(Path,'read_text',read):runpy.run_path('scripts/validate_corpus.py',run_name='__main__')
"""
  p=subprocess.run([sys.executable,'-c',code],cwd=ROOT,capture_output=True,text=True);self.assertEqual(p.returncode,1,p.stdout+p.stderr);self.assertNotIn('Traceback',p.stdout+p.stderr)
