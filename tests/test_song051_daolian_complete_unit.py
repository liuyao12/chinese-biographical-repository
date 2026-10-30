from pathlib import Path
import os,unittest,copy,ast,json,sys,tempfile,importlib.util
ROOT=Path(os.environ.get('CBR_TEST_ROOT',Path(__file__).resolve().parents[1])).resolve()
sys.path[:0]=[str(ROOT)]
from scripts import wyd_song051_yixin as y
from scripts.person_bundle import validate_full_name,bundle,load_catalog
from scripts.name_childhood import validate_childhood_name
from scripts.validation_context import scope
class DaoLianNames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with scope(ROOT):cls.ch,cls.roles,cls.c,cls.docs=y.state(ROOT);cls.catalog=load_catalog(ROOT)
  cls.ns=cls.docs['corpus/songshu/051-wyd1739-daolian-name-components.json']['records'];cls.ps={p['id']:p for p in cls.ch['paragraphs']}
 def fname(self,n,ch=None,root=ROOT):
  cc=self.ch if ch is None else ch;return validate_full_name(n,self.ps[n['paragraph_id']],chapter=cc,root=root)
 def child(self,n):return validate_childhood_name(n,self.ps[n['paragraph_id']],chapter=self.ch,root=ROOT)
 def test_true_unsplit_names_and_actual_bundle(self):
  with scope(ROOT):
   for n in self.ns:
    if 'full_name'in n:
     self.fname(n);self.assertIsNone(n['surname']);self.assertIsNone(n['ming']);b=bundle(n['person_id'],root=ROOT,include_provisional=True,catalog=self.catalog);self.assertIn({**n,**{k:self.ch[k]for k in ['work_id','book_id','source_id']}},b['name_components'])
 def test_unsplit_missing_context_and_bad_owner_value_or_han_split(self):
  for n in [n for n in self.ns if 'full_name'in n]:
   with self.assertRaises(ValueError):validate_full_name(n,self.ps[n['paragraph_id']])
   for key,value in [('person_id',self.roles['dl_daolian']),('full_name','長沙王'),('surname','索'),('ming','度真'),('quote','刪引文')]:
    bad=copy.deepcopy(n);bad[key]=value
    with self.assertRaises(ValueError):self.fname(bad)
 def test_cross_paragraph_fragments_are_actual_adjacent_tail_head(self):
  spec=next(b for b in self.c['received_unsplit_name_bindings']if b['value']=='解斯蘭');a,b=spec['fragments'];i=next(i for i,p in enumerate(self.ch['paragraphs'])if p['id']==a['paragraph_id']);self.assertEqual(self.ch['paragraphs'][i+1]['id'],b['paragraph_id']);self.assertEqual(a['end'],len(self.ps[a['paragraph_id']]['text']));self.assertEqual(b['start'],0)
  self.assertEqual(a['surface']+b['surface'],'解斯蘭')
 def test_fragment_direction_and_owner_guards_inside_validated_context(self):
  from unittest.mock import patch
  n=next(n for n in self.ns if n.get('full_name')=='解斯蘭')
  for case in ['reverse','skip_paragraph','not_tail','not_head','wrong_owner']:
   c=copy.deepcopy(self.c);ch=copy.deepcopy(self.ch);b=next(b for b in c['received_unsplit_name_bindings']if b['record_id']==n['id']);a,z=b['fragments']
   if case=='reverse':b['fragments'].reverse()
   if case=='skip_paragraph':z['paragraph_id']=ch['paragraphs'][2]['id']
   if case=='not_tail':a['end']-=1
   if case=='not_head':z['start']+=1
   if case=='wrong_owner':next(m for p in ch['paragraphs']for m in p['mentions']if m['id']==z['mention_id'])['person_id']=self.roles['dl_daolian']
   with patch.object(y,'state',return_value=(ch,self.roles,c,self.docs)):
    self.assertFalse(y.unsplit_name_valid(n,self.ps[n['paragraph_id']],self.ch,ROOT),case)
 def test_true_xiaozhi_and_no_missing_or_injected_word(self):
  n=next(n for n in self.ns if n.get('xiaozhi')=='車士')
  with scope(ROOT):self.child(n)
  for key,value in [('person_id',self.roles['dl_daolian']),('xiaozhi','車兒'),('quote',n['quote'].replace('小字也','小字',1))]:
   bad=copy.deepcopy(n);bad[key]=value
   with self.assertRaises(ValueError):self.child(bad)
  for change in ['wrong_subject','reversed','moved','invented_zhe','without_ye']:
   bad=copy.deepcopy(n);b=bad['xiaozhi_basis']
   if change=='wrong_subject':b['subject_anchor']['person_mention_id']=b['value_anchor']['person_mention_id']
   if change=='reversed':b['value_anchor'],b['subject_anchor']=b['subject_anchor'],b['value_anchor']
   if change=='moved':b['value_anchor']['start']+=1
   if change=='invented_zhe':b['source_term']='車士者義真小字也'
   if change=='without_ye':b['source_term']='車士義真小字'
   with self.assertRaises(ValueError):self.child(bad)
 def test_no_false_biological_ordinal_or_ningmeng_person(self):
  d=next(d for d in self.c['additional_source_role_ledgers']if d['key']=='daolian')['source_reported_ordinal'];self.assertEqual(d['source_reported_numeric'],2);self.assertIsNone(d['preferred_biological_ordinal']);self.assertFalse(d['used_for_birth_order_sorting'])
  aa=self.docs['corpus/songshu/051-wyd1739-daolian-assertions.json']['assertions'];self.assertEqual(len(aa),2);self.assertTrue(all('birth_order'not in a['qualifiers']for a in aa));self.assertFalse(any(m['surface']=='寧孟'for p in self.ch['paragraphs']for m in p['mentions']))
 def test_tuobakai_keeps_printed_form_but_resolves_by_fixed_primary(self):
  m=next(m for p in self.ch['paragraphs']for m in p['mentions']if m['surface']=='托跋開');self.assertEqual(m['kind'],'person');self.assertEqual(m['person_id'],self.roles['dl_tuobakai'])
  d=next(d for d in self.docs['corpus/songshu/051-wyd1739-daolian-identities.json']['decisions']if d['id']=='d-song051-daolian-tuobakai');self.assertEqual(d['person_id'],m['person_id']);self.assertEqual(len(d['references']),3);self.assertTrue(all(r['printed_edition']is None and r['image_verified']is False for r in d['references']))
 def test_legacy_xz_statement_is_still_exact(self):
  pid='old-person';p={'id':'old-paragraph','text':'黙者爽小字也','mentions':[{'id':'v','start':0,'end':1,'surface':'黙','person_id':pid},{'id':'s','start':2,'end':3,'surface':'爽','person_id':pid}]}
  def a(m):return dict(paragraph_id=p['id'],start=m['start'],end=m['end'],surface=m['surface'],person_mention_id=m['id'])
  n={'person_id':pid,'paragraph_id':p['id'],'quote':p['text'],'xiaozhi':'黙','xiaozhi_basis':{'kind':'explicit_xiaozhi_statement','source_term':p['text'],'value_anchor':a(p['mentions'][0]),'subject_anchor':a(p['mentions'][1]),'marker_anchor':{'paragraph_id':p['id'],'start':3,'end':5,'surface':'小字'},'status':'source_attested','human_reviewed':False,'rationale':'legacy正例'}};validate_childhood_name(n,p)
  bad=copy.deepcopy(n);bad['xiaozhi_basis']['source_term']='黙爽小字也'
  with self.assertRaises(ValueError):validate_childhood_name(bad,p)
if __name__=='__main__':unittest.main()
