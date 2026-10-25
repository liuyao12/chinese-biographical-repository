import copy,json,unittest
from pathlib import Path
try:
 from scripts.name_childhood import validate_childhood_name
 from scripts.person_bundle import validate_courtesy_name
except ImportError:
 from name_childhood import validate_childhood_name
 from person_bundle import validate_courtesy_name
ROOT=Path(__file__).resolve().parents[1]
class ShishuoNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/shishuoxinyu/yanyu-071.json').read_text());cls.ps={p['id']:p for p in cls.c['paragraphs']};cls.rows=json.loads((ROOT/'corpus/shishuoxinyu/yanyu-071-name-components.json').read_text())['records'];cls.child=next(n for n in cls.rows if n['id']=='nc-shishuo071-lang-xiaozhi');cls.p=cls.ps[cls.child['paragraph_id']]
 def test_seven_actual_source_name_rows(self):
  self.assertEqual(len([n for n in self.rows if n['id'].startswith('nc-shishuo071-')]),7)
  for n in self.rows:
   if n['id'].startswith('nc-shishuo071-'):
    self.assertEqual(n['quote'],self.ps[n['paragraph_id']]['text']);validate_courtesy_name(n);validate_childhood_name(n,self.ps[n['paragraph_id']])
  daoyun=[n for n in self.rows if n['id'].startswith('nc-shishuo071-daoyun-')]
  self.assertEqual([(n['surname'],n['ming'],n['title'])for n in daoyun],[('謝',None,None),(None,'道蘊',None)])
 def test_real_comma_childhood(self):
  self.assertIsNone(validate_childhood_name(self.child,self.p));self.assertEqual(self.child['xiaozhi'],'胡兒');self.assertNotIn('xiaoming',self.child)
 def test_bad_comma_actor_value_marker_or_kind(self):
  for edit in('actor','value','comma','oldkind','xiaoming','marker','sameanchor'):
   n=copy.deepcopy(self.child);b=n['xiaozhi_basis']
   if edit=='actor':n['person_id']='synthetic_other'
   elif edit=='value':n['xiaozhi']='長度'
   elif edit=='comma':b['separator_anchor']['surface']=','
   elif edit=='oldkind':b['kind']='explicit_xiaozhi_apposition';b.pop('separator_anchor')
   elif edit=='xiaoming':n['xiaoming']='胡兒'
   elif edit=='marker':b['marker_anchor']['start']+=1
   else:b['subject_anchor']=copy.deepcopy(b['value_anchor'])
   with self.assertRaises(ValueError,msg=edit):validate_childhood_name(n,self.p)
 def test_missing_final_ye_and_wrong_mention_kind(self):
  for edit in('ye','kind'):
   p=copy.deepcopy(self.p);n=copy.deepcopy(self.child)
   if edit=='ye':
    i=n['xiaozhi_basis']['marker_anchor']['end'];p['text']=p['text'][:i]+p['text'][i+1:];n['quote']=p['text']
   else:next(m for m in p['mentions']if m['id']==n['xiaozhi_basis']['subject_anchor']['person_mention_id'])['kind']='work'
   with self.assertRaises(ValueError):validate_childhood_name(n,p)
 def test_legitimate_source_mid_rekey(self):
  p=copy.deepcopy(self.p);n=copy.deepcopy(self.child);old=n['person_id'];n['person_id']='synthetic_current'
  for m in p['mentions']:
   if m.get('person_id')==old:m['person_id']=n['person_id']
  self.assertIsNone(validate_childhood_name(n,p))
 def test_old_statement_and_adjacent_apposition(self):
  for kind,text,sep in [('explicit_xiaozhi_statement','阿雲者乙小字也','者'),('explicit_xiaozhi_apposition','阿雲乙小字也','')]:
   cid='synthetic-chapter';p=dict(id=cid+':p1',text=text,mentions=[]);a=dict(paragraph_id=p['id'],start=0,end=2,surface='阿雲',person_mention_id='value');start=2+len(sep);s=dict(paragraph_id=p['id'],start=start,end=start+1,surface='乙',person_mention_id='subject');k=dict(paragraph_id=p['id'],start=start+1,end=start+3,surface='小字')
   p['mentions']=[dict(id=a['person_mention_id'],start=a['start'],end=a['end'],surface=a['surface'],person_id='synthetic_person'),dict(id=s['person_mention_id'],start=s['start'],end=s['end'],surface=s['surface'],person_id='synthetic_person')]
   if kind=='explicit_xiaozhi_apposition':
    for m in p['mentions']:m['kind']='person'
   n=dict(person_id='synthetic_person',chapter_id=cid,paragraph_id=p['id'],quote=text,xiaozhi='阿雲',xiaozhi_basis=dict(kind=kind,source_term=text,value_anchor=a,subject_anchor=s,marker_anchor=k,status='source_attested',human_reviewed=False,rationale='synthetic grammar regression'))
   self.assertIsNone(validate_childhood_name(n,p))
 def test_old_subject_youxiaozhi(self):
  p=dict(id='synthetic:p',text='乙又小字阿雲',mentions=[dict(id='subject',kind='person',person_id='p',start=0,end=1,surface='乙'),dict(id='value',kind='person',person_id='p',start=4,end=6,surface='阿雲')])
  a=dict(paragraph_id=p['id'],start=4,end=6,surface='阿雲',person_mention_id='value');subject=dict(paragraph_id=p['id'],start=0,end=1,surface='乙',person_mention_id='subject');k=dict(paragraph_id=p['id'],start=2,end=4,surface='小字')
  n=dict(person_id='p',paragraph_id=p['id'],quote=p['text'],xiaozhi='阿雲',xiaozhi_basis=dict(kind='explicit_subject_xiaozhi',source_term=p['text'],value_anchor=a,subject_anchor=subject,marker_anchor=k,status='source_attested',human_reviewed=False,rationale='legacy synthetic regression'))
  self.assertIsNone(validate_childhood_name(n,p))
 def test_explicit_parent_scoped_orders_only(self):
  aa=json.loads((ROOT/'corpus/shishuoxinyu/yanyu-071-assertions.json').read_text())['assertions'];by={a['id']:a for a in aa}
  for aid,num,term in [('a-shishuo071-lang-father',1,'長子'),('a-shishuo071-ningzhi-father',2,'第二子')]:
   a=by[aid];o=a['qualifiers']['birth_order'];self.assertEqual(o['ordinal'],num);self.assertEqual(o['parent_person_id'],a['object_person_id']);self.assertEqual(o['scope'],'sons_of_parent');self.assertIn(term,a['evidence'][0]['quote'])
  for a in aa:
   if a['predicate']=='brother':self.assertNotIn('birth_order',a['qualifiers'])
if __name__=='__main__':unittest.main()
