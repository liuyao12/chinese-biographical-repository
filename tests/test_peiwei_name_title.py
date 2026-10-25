from pathlib import Path
import unittest,json,copy,tempfile,shutil
R=Path(__file__).resolve().parents[1]
class PeiweiNameTitleTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch={}
  for p in ['corpus/jinshu/035-peiwei.json','corpus/jinshu/043-leguang.json']:
   c=json.loads((R/p).read_bytes());cls.ch[c['id']]=c
  cls.names=[]
  for p in ['035-peiwei-name-components.json','043-leguang-name-components.json','040-jiachong-family-name-components.json']:
   q=R/'corpus/jinshu'/p
   if q.exists():cls.names.extend(json.loads(q.read_bytes())['records'])
  cls.by={n['id']:n for n in cls.names};cls.assertions=json.loads((R/'corpus/jinshu/035-peiwei-assertions.json').read_bytes())['assertions'];cls.nr=json.loads((R/'corpus/jinshu/035-peiwei-name-components.json').read_bytes());cls.hs=json.loads((R/'corpus/jinshu/035-peiwei-titles.json').read_bytes());cls.pref=json.loads((R/'corpus/jinshu/035-peiwei-profile-title.json').read_bytes())
 def validate(self,n,names=None,chapters=None,assertions=None,root=R):
  from scripts.surname_from_father import validate
  return validate(n,self.names if names is None else names,self.ch if chapters is None else chapters,self.assertions if assertions is None else assertions,root)
 def test_three_source_bound_surnames_no_name_duplication(self):
  for key,ming in [('wei','頠'),('song','嵩'),('gai','該')]:
   n=self.by['nc-jin035-peiwei-name-'+key];self.assertEqual((n['surname'],n['ming']),('裴',ming));self.validate(n);self.assertEqual(n['status'],'contextual_provisional')
  self.assertEqual(self.by['nc-jin035-peiwei-name-wei']['zi'],'逸民');self.assertIsNone(self.by['nc-jin035-peiwei-name-kai']['surname']);self.assertEqual(self.by['nc-jin043-leguang-name-peiwei']['surname'],'裴');self.assertNotIn('surname_basis',self.by['nc-jin043-leguang-name-peiwei'])
 def test_valid_legacy_name_without_id_does_not_hide_unique_native_seed(self):
  n=self.by['nc-jin035-peiwei-name-wei'];legacy=dict(person_id=n['person_id'],surname='裴',ming='頠',quote='legacy name display row')
  self.assertNotIn('id',legacy);names=self.names+[legacy]
  for key in ['wei','song','gai']:self.validate(self.by['nc-jin035-peiwei-name-'+key],names=names)
  contrary=dict(legacy,surname='裘')
  with self.assertRaises(ValueError):self.validate(n,names=self.names+[contrary])
  duplicate=copy.deepcopy(self.by['nc-jin043-leguang-name-peiwei'])
  with self.assertRaises(ValueError):self.validate(n,names=self.names+[legacy,duplicate])
 def test_profile_title_filename_is_excluded_from_actual_holding_glob(self):
  path=R/'corpus/jinshu/035-peiwei-profile-title.json';self.assertTrue(path.is_file());self.assertNotIn(path,list((R/'corpus').glob('*/*-titles.json')));self.assertFalse((R/'corpus/jinshu/035-peiwei-profile-titles.json').exists())
  with tempfile.TemporaryDirectory()as d:
   bad=Path(d)/'corpus/jinshu/035-peiwei-profile-titles.json';bad.parent.mkdir(parents=True);bad.write_text(json.dumps(self.pref))
   selected=list((Path(d)/'corpus').glob('*/*-titles.json'));self.assertEqual(selected,[bad]);self.assertNotEqual(json.loads(bad.read_text())['record_type'],'title_holding_assertion_set');self.assertNotIn('holdings',json.loads(bad.read_text()))
 def test_other_literal_name_variants_remain_and_no_ming_arbitration(self):
  for n in self.names:
   if n['id']=='nc-jin040-jiachong-089':self.assertEqual((n['surname'],n['ming']),('裴','顗'));self.assertNotIn('surname_basis',n)
  self.assertEqual(len([n for n in self.names if n['id']=='nc-jin043-leguang-name-peiwei']),1)
 def test_wrong_seed_person_kind_literal_and_book_fields_rejected(self):
  n=self.by['nc-jin035-peiwei-name-wei']
  for field,value in [('person_id','wrong-current-person'),('surname','裘'),('ming','顗')]:
   bad=copy.deepcopy(n);bad[field]=value
   with self.assertRaises(ValueError):self.validate(bad)
  for field,value in [('kind','work'),('surface','裴顗'),('person_id','wrong-current-person')]:
   ch=copy.deepcopy(self.ch);m=next(m for m in ch['c-jinshu-043-leguang']['paragraphs'][4]['mentions']if m['id']=='c-jinshu-043-leguang:p005:m0028');m[field]=value
   with self.assertRaises(ValueError):self.validate(n,chapters=ch)
  for key,value in [('raw_file_sha256','0'*64),('source_revision',1),('work_id','w-hanshu')]:
   bad=copy.deepcopy(n);bad['surname_basis']['seed_frame'][key]=value
   with self.assertRaises(ValueError):self.validate(bad)
  bad=copy.deepcopy(n);bad['surname_basis']['source_units'][1]['source_title']='《漢書》卷四十三'
  with self.assertRaises(ValueError):self.validate(bad)
  names=copy.deepcopy(self.names);contrary=copy.deepcopy(n);contrary['id']='synthetic-contrary-literal';contrary['surname']='裘';contrary.pop('surname_basis');names.append(contrary)
  with self.assertRaises(ValueError):self.validate(n,names=names)
 def test_parent_mother_adopter_or_reversed_edge_never_transfer_surname(self):
  n=self.by['nc-jin035-peiwei-name-gai']
  for predicate in ['mother','adoptive_father','spouse']:
   bad=copy.deepcopy(n);rows=copy.deepcopy(self.assertions);a=next(a for a in rows if a['id']==bad['surname_basis']['steps'][0]['assertion_id']);a['predicate']=predicate;bad['surname_basis']['steps'][0]['assertion_snapshot']=copy.deepcopy(a)
   with self.assertRaises(ValueError):self.validate(bad,assertions=rows)
  for which in ['reverse','wrongfather']:
   bad=copy.deepcopy(n);rows=copy.deepcopy(self.assertions);a=next(a for a in rows if a['id']==bad['surname_basis']['steps'][0]['assertion_id'])
   if which=='reverse':a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id']
   else:a['object_person_id']=self.by['nc-jin035-peiwei-name-kai']['person_id']
   bad['surname_basis']['steps'][0]['assertion_snapshot']=copy.deepcopy(a)
   with self.assertRaises(ValueError):self.validate(bad,assertions=rows)
 def test_missing_surname_is_not_arbitrary_label_or_id_inference(self):
  n=copy.deepcopy(self.by['nc-jin035-peiwei-name-song']);n['surname_basis']['steps']=[]
  with self.assertRaises(ValueError):self.validate(n)
  n=copy.deepcopy(self.by['nc-jin035-peiwei-name-song']);n['surname_basis']['seed_name_record_id']='registry-label'
  with self.assertRaises(ValueError):self.validate(n)
 def test_true_existing_resolver_selects_only_timeless_grant_headings(self):
  from scripts.profile_title_preferences import resolve
  people={m['person_id']:{'id':m['person_id'],'id_aliases':[]}for c in self.ch.values()for p in c['paragraphs']for m in p['mentions']if m['kind']=='person'};records=list(self.ch.values())+[self.hs,self.pref];choices=resolve(records,people,R)
  for key,title in [('wei','尚書左僕射'),('gai','武昌侯')]:
   pid=self.by['nc-jin035-peiwei-name-'+key]['person_id'];self.assertEqual(choices[pid]['title'],title);self.assertEqual(choices[pid]['mode'],'grant');d=next(d for d in self.pref['decisions']if d['person_id']==pid);self.assertEqual(d['temporal_claim'],'none');self.assertEqual(d['scope'],'timeless_profile_heading');self.assertNotIn('year',d)
  for h in self.hs['holdings']:
   if h['id']in{d['holding_id']for d in self.pref['decisions']}:self.assertEqual(h['effective_period']['end']['status'],'unknown');self.assertIsNone(h['effective_period']['start']['date_expression'])
 def test_heading_wrong_person_free_title_or_date_rejected(self):
  from scripts.profile_title_preferences import resolve
  people={m['person_id']:{'id':m['person_id'],'id_aliases':[]}for c in self.ch.values()for p in c['paragraphs']for m in p['mentions']if m['kind']=='person'}
  for change in [('person_id',self.by['nc-jin035-peiwei-name-gai']['person_id']),('title','最高官'),('year',300),('temporal_claim','at_death')]:
   pref=copy.deepcopy(self.pref);pref['decisions'][0][change[0]]=change[1]
   with self.assertRaises(ValueError):resolve(list(self.ch.values())+[self.hs,pref],people,R)
 def temporary_source_root(self,ch):
  tmp=tempfile.TemporaryDirectory();root=Path(tmp.name)
  for c in ch.values():
   path='corpus/jinshu/'+('035-peiwei.json'if c['id']=='c-jinshu-035-peiwei'else'043-leguang.json');q=root/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(c,ensure_ascii=False));raw=c['source']['raw_file'];q=root/raw;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/raw,q);ref=c['annotation']['fixed_wikisource_unit_ref'];q=root/ref;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/ref,q)
  # The existing embedded-document validator also resolves its author against
  # this native parent-unit seed. Carry only the fixed dependency, coherently
  # rekeying its person mentions for the positive identity migration test.
  oldmain=self.ch['c-jinshu-035-peiwei']['paragraphs'][0]['mentions'][0]['person_id'];newmain=ch['c-jinshu-035-peiwei']['paragraphs'][0]['mentions'][0]['person_id']
  support='corpus/jinshu/035-pei-family.json';source=json.loads((R/support).read_bytes())
  for p in source['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')==oldmain:m['person_id']=newmain
  q=root/support;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(source,ensure_ascii=False))
  pins='scripts/fixed_attached_subsection_witnesses.json';q=root/pins;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/pins,q)
  calendar='sources/calendar-context/moe-era-table-page2.html';q=root/calendar;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/calendar,q)
  return tmp,root
 def test_cross_source_raw_byte_corruption_and_coherent_text_changes_rejected(self):
  ch=copy.deepcopy(self.ch);tmp,root=self.temporary_source_root(ch)
  try:
   raw=root/ch['c-jinshu-043-leguang']['source']['raw_file'];raw.write_bytes(raw.read_bytes()+b' ')
   with self.assertRaises(ValueError):self.validate(self.by['nc-jin035-peiwei-name-wei'],root=root)
  finally:tmp.cleanup()
  ch=copy.deepcopy(self.ch);p=ch['c-jinshu-043-leguang']['paragraphs'][4];p['text']=p['text'].replace('裴頠','裘頠');n=copy.deepcopy(self.by['nc-jin035-peiwei-name-wei']);n['surname_basis']['seed_frame']['quote']=p['text'];n['surname_basis']['seed_frame']['paragraph_sha256']=__import__('hashlib').sha256(p['text'].encode()).hexdigest();tmp,root=self.temporary_source_root(ch)
  try:
   with self.assertRaises(ValueError):self.validate(n,chapters=ch,root=root)
  finally:tmp.cleanup()
 def test_consistent_source_pid_rekey_valid_without_id_whitelist(self):
  ids={self.by['nc-jin035-peiwei-name-'+k]['person_id']:('q9z_x8y_w7v'+['','_A','_B'][i]) for i,k in enumerate(['wei','song','gai'])}
  def rewrite(v):
   if isinstance(v,dict):return{k:rewrite(x)for k,x in v.items()}
   if isinstance(v,list):return[rewrite(x)for x in v]
   return ids.get(v,v)if isinstance(v,str)else v
  names=rewrite(self.names);ch=rewrite(self.ch);rows=rewrite(self.assertions);tmp,root=self.temporary_source_root(ch)
  try:
   for key in ['wei','song','gai']:self.validate(next(n for n in names if n['id']=='nc-jin035-peiwei-name-'+key),names=names,chapters=ch,assertions=rows,root=root)
  finally:tmp.cleanup()
if __name__=='__main__':unittest.main()
