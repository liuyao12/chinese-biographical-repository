import unittest,json,copy
from pathlib import Path
from scripts.fixed_biography_names import component_valid,validate_surname
from scripts.name_childhood import validate_childhood_name
ROOT=Path(__file__).resolve().parents[1]
class YanghuNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/jinshu/034-yanghu.json').read_bytes());cls.ns=json.loads((ROOT/'corpus/jinshu/034-yanghu-name-components.json').read_bytes())['records'];cls.aa=[]
  for path in(ROOT/'corpus').rglob('*.json'):cls.aa.extend(json.loads(path.read_bytes()).get('assertions',[]))
 def n(self,key):return copy.deepcopy(next(n for n in self.ns if n['id']=='nc-jin034-yanghu-'+key))
 def valid(self,n,aa=None):return validate_surname(n,self.ns,{self.c['id']:self.c},self.aa if aa is None else aa,ROOT)
 def test_all_seventeen_and_literal_courtesy(self):
  self.assertEqual(len(self.ns),17)
  for n in self.ns:
   self.assertTrue(component_valid(n,self.c,ROOT,self.aa))
   if n.get('surname_basis'):self.assertIsNone(self.valid(n))
  self.assertEqual(self.n('hu')['zi'],'叔子');self.assertEqual(self.n('liang')['zi'],'長玄')
 def test_mother_only_and_remote_ming_have_no_surname(self):
  for key in ('cheng','faxing'):self.assertIsNone(self.n(key)['surname']);self.assertNotIn('surname_basis',self.n(key))
 def test_exact_parent_and_uncle_direction_not_assembly(self):
  for key in('dao','xu','dan','tao','pian'):
   n=self.n(key);n['surname_basis']['steps'][0]['traversal']='object_to_subject';self.assertRaises(ValueError,self.valid,n)
 def test_missing_edge_cycle_wrong_endpoint_generation(self):
  for mutate in('missing','cycle','endpoint','generation'):
   n=self.n('pian');ss=n['surname_basis']['steps']
   if mutate=='missing':ss.pop(0)
   elif mutate=='cycle':ss.append(copy.deepcopy(ss[0]))
   elif mutate=='endpoint':ss[-1]['to_person_id']=ss[0]['from_person_id']
   else:ss[-1]['generation_after']+=1
   self.assertRaises(ValueError,self.valid,n)
 def test_cannot_forge_source_father_or_mother_route(self):
  for pred in('mother','adoptive_father','ritual_successor_of','spouse'):
   n=self.n('dao');aa=copy.deepcopy(self.aa);a=next(a for a in aa if a['id']==n['surname_basis']['steps'][0]['assertion_id']);a['predicate']=pred;self.assertRaises(ValueError,self.valid,n,aa)
 def test_same_mother_no_paternal_surname(self):
  n=self.n('cheng');n['surname']='羊';n['status']='contextual_provisional';n['surname_basis']=copy.deepcopy(self.n('fa')['surname_basis']);s=n['surname_basis']['steps'][0];a=next(a for a in self.aa if a['id']=='a-jin034-yanghu-same-mother-brother-cheng');s.update(assertion_id=a['id'],to_person_id=n['person_id']);self.assertRaises(ValueError,self.valid,n)
 def test_source_explicit_wrong_surname_and_missing_seed(self):
  for key,value in(('status','source_attested'),('surname','蔡')):
   n=self.n('dao');n[key]=value;self.assertRaises(ValueError,self.valid,n)
  n=self.n('dao');n['surname_basis']['seed_name_record_id']='missing';self.assertRaises(ValueError,self.valid,n)
 def test_source_slot_changed_kinship_is_rejected(self):
  n=self.n('dao');aa=copy.deepcopy(self.aa);a=next(a for a in aa if a['id']==n['surname_basis']['steps'][0]['assertion_id']);a['evidence'][0]['quote']='父道';self.assertRaises(ValueError,self.valid,n,aa)
 def test_wrong_chapter_or_non_source_slot_is_not_trusted(self):
  for mutate in ('chapter','kind','status'):
   n=self.n('dao');aa=copy.deepcopy(self.aa);a=next(a for a in aa if a['id']==n['surname_basis']['steps'][0]['assertion_id'])
   if mutate=='chapter':a['evidence'][0]['chapter_id']='other-complete-biography'
   elif mutate=='kind':a['fixed_source_fact_binding']['kind']='assembly_preferred_parent'
   else:a['status']='editorial_provisional'
   self.assertRaises(ValueError,self.valid,n,aa)
 def test_full_quote_offset_and_same_person_zi(self):
  for mode in('quote','mid','zi'):
   n=self.n('hu')
   if mode=='quote':n['quote']=n['quote'][:10]
   elif mode=='mid':n['person_mention_id']='missing'
   else:n['zi']='長玄'
   self.assertFalse(component_valid(n,self.c,ROOT,self.aa))
 def test_wife_clan_prefix_does_not_become_given_or_title(self):
  n=self.n('wife');self.assertEqual(n['surname'],'夏侯');self.assertIsNone(n['ming']);self.assertNotIn('title',n);self.assertNotIn('mother',n)
  for field,value in(('ming','氏'),('surname','夫人夏侯')):
   bad=copy.deepcopy(n);bad[field]=value;self.assertFalse(component_valid(bad,self.c,ROOT,self.aa))
  n['fixed_biography_name_binding']['title_prefix']='皇后';self.assertFalse(component_valid(n,self.c,ROOT,self.aa))
 def test_xiaozhi_not_song_or_zi(self):
  n=self.n('wangjun');p=next(p for p in self.c['paragraphs']if p['id']==n['paragraph_id']);self.assertIsNone(validate_childhood_name(n,p));self.assertNotIn('zi',n)
  for mutate in('song','person','position','truncated'):
   bad=copy.deepcopy(n)
   if mutate=='song':bad['xiaozhi_basis']['value_anchor']['person_mention_id']=p['mentions'][1]['id']
   elif mutate=='person':bad['person_id']='unrelated'
   elif mutate=='position':bad['xiaozhi_basis']['marker_anchor']['start']+=1
   else:bad['quote']='濬又小字阿童'
   self.assertRaises(ValueError,validate_childhood_name,bad,p)
class SyntheticSubjectXiaozhi(unittest.TestCase):
 def fixture(self):
  p=dict(id='s:p',text='甲又小字小乙，童謠小乙。',mentions=[dict(id='s:m1',kind='person',person_id='arbitrary',surface='甲',start=0,end=1),dict(id='s:m2',kind='person',person_id='arbitrary',surface='小乙',start=4,end=6)])
  def a(s,e,mid=None):
   d=dict(paragraph_id=p['id'],start=s,end=e,surface=p['text'][s:e])
   if mid:d['person_mention_id']=mid
   return d
  n=dict(person_id='arbitrary',paragraph_id=p['id'],quote=p['text'],xiaozhi='小乙',xiaozhi_basis=dict(kind='explicit_subject_xiaozhi',source_term='甲又小字小乙',subject_anchor=a(0,1,'s:m1'),value_anchor=a(4,6,'s:m2'),marker_anchor=a(2,4),status='source_attested',human_reviewed=False,rationale='Synthetic arbitrary source.'));return n,p
 def test_arbitrary_source_positive(self):self.assertIsNone(validate_childhood_name(*self.fixture()))
 def test_zi_xiaoming_negative_and_other_person(self):
  for word in('字','小名','非字'):
   n,p=self.fixture();p['text']=p['text'].replace('小字',word);n['quote']=p['text'];self.assertRaises(ValueError,validate_childhood_name,n,p)
  n,p=self.fixture();p['mentions'][1]['person_id']='other';self.assertRaises(ValueError,validate_childhood_name,n,p)
 def test_negation_or_changed_marker_rejected(self):
  for text in('甲非小字小乙，童謠小乙。','甲又小字小乙非也。'):
   n,p=self.fixture()
   p['text']=text;n['quote']=text;self.assertRaises(ValueError,validate_childhood_name,n,p)
if __name__=='__main__':unittest.main()
