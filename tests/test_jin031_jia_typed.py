import copy,hashlib,json,shutil,tempfile,unittest
from pathlib import Path
from scripts import fixed_jin031_jia_typed as t
from scripts import fixed_jin031_jia_full_ner as ner
from scripts.age_approximations import age_approximation_errors
SOURCE=Path(__file__).resolve().parents[1]
class Typed031(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(prefix='jin031-typed-');cls.addClassCleanup(cls.tmp.cleanup);cls.root=Path(cls.tmp.name)
  cls.paths=t.fixture_paths(SOURCE);cls.before={p:hashlib.sha256((SOURCE/p).read_bytes()).hexdigest()for p in cls.paths}
  for rel in cls.paths:
   src=SOURCE/rel;dst=cls.root/rel;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(src,dst);assert src.stat().st_ino!=dst.stat().st_ino
  cls.ch=t.core.read(cls.root,t.core.CH);cls.roles,cls.base=ner.prepared(cls.ch,cls.root);cls.p={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.b=t.proof(cls.root)
 @classmethod
 def tearDownClass(cls):assert all(hashlib.sha256((SOURCE/p).read_bytes()).hexdigest()==h for p,h in cls.before.items())
 def test_baseline_full_source_and_typed_counts(self):
  self.assertEqual(ner.prepared(self.ch,self.root)[0],self.roles)
  self.assertEqual(sum(len(p['text'])for p in self.ch['paragraphs']),1628);self.assertEqual(sum(m['kind'] in ('person','pronoun')for p in self.ch['paragraphs']for m in p['mentions']),205 if self.ch['annotation'].get('fixed_jin031_remaining_titles_ref')else 204)
  self.assertEqual(len(self.ch['annotation']['age_assertions']),3);self.assertEqual(len(self.ch['annotation']['age_difference_assertions']),2)
  for a in t.core.read(self.root,'corpus/jinshu/031-jia-comparison-assertions.json')['assertions']:self.assertTrue(t.family_valid(a,self.p,self.root))
 def test_appearance_age_common_checks_and_scope(self):
  a=self.ch['annotation']['age_assertions'][2];p=self.ch['paragraphs'][4]
  self.assertEqual(age_approximation_errors(a,p,root=self.root,chapter=self.ch),[])
  self.assertTrue(age_approximation_errors(a,p))
  for field,value in [('value',35),('birth_year',265),('bounds',{'lower':35,'upper':36}),('human_reviewed',True),('reporting_status','qualified_report'),('age_context',{'kind':'at_death','life_event_id':'fake'})]:
   bad=copy.deepcopy(a);bad[field]=value;self.assertTrue(age_approximation_errors(bad,p,root=self.root,chapter=self.ch))
  for field in ['subject_person_mention_id','speaker_person_mention_id']:
   bad=copy.deepcopy(a);bad['subject_scope'][field]=p['mentions'][0]['id'];self.assertTrue(age_approximation_errors(bad,p,root=self.root,chapter=self.ch))
 def test_age_difference_direction_not_thirteen(self):
  rows=self.ch['annotation']['age_difference_assertions'];self.assertEqual([x['value']for x in rows],[1,2])
  for row in rows:
   self.assertTrue(t.difference_valid(row,self.ch,self.root));bad=copy.deepcopy(row);bad['person_id'],bad['reference_person_id']=bad['reference_person_id'],bad['person_id'];self.assertFalse(t.difference_valid(bad,self.ch,self.root))
 def test_raised_grandchild_not_blood_denial_or_mother(self):
  a=next(a for a in t.core.read(self.root,'corpus/jinshu/031-jia-comparison-assertions.json')['assertions']if a['id'].endswith('jami-raised-grandchild'))
  q=a['qualifiers'];self.assertEqual((q['generation_distance'],q['direction']),(2,'grandchild_to_grandparent'));self.assertIn('not_denial',q['biological_qualification_scope'])
  for field,value in [('generation_distance',1),('direction','grandparent_to_grandchild'),('relationship_class','biological_grandchild'),('legal_adoption_status','legal_adoption')]:
   bad=copy.deepcopy(a);bad['qualifiers'][field]=value;self.assertFalse(t.family_valid(bad,self.p,self.root))
 def test_holding_duration_and_unknown_boundaries(self):
  hs=t.core.read(self.root,'corpus/jinshu/031-jia-comparison-titles.json')['holdings'];h=next(h for h in hs if h['id']=='th-jin031-empress');d=h['reported_duration'];self.assertEqual((d['value'],d['unit'],d['counting']),(11,'title_year','unspecified_source_years'));self.assertTrue(d['evidence'][0]['person_mention_id'].endswith('p007:m0229'))
  bad=copy.deepcopy(h);bad['reported_duration']['value']=12;self.assertFalse(t.holding_valid(bad,self.ch,self.root))
  fi=next(h for h in hs if h['id']=='th-jin031-taizifei');self.assertEqual(fi['effective_period']['start']['normalized_date']['year'],272);self.assertIsNone(fi['source_calendar_components']['calendar_day'])
  for field,value in [('chinese_year',273),('month',3),('sexagenary_day','甲子'),('calendar_day',17)]:
   bad=copy.deepcopy(fi);bad['source_calendar_components'][field]=value;self.assertFalse(t.holding_valid(bad,self.ch,self.root))
  bad=copy.deepcopy(fi);bad['effective_period']['start']['normalized_date']['year']=273;self.assertFalse(t.holding_valid(bad,self.ch,self.root))
 def test_wrong_one_endpoint_and_reverse_rejected(self):
  a=t.core.read(self.root,'corpus/jinshu/031-jia-comparison-assertions.json')['assertions'][0];bad=copy.deepcopy(a);bad['object_person_id']=a['subject_person_id'];self.assertFalse(t.family_valid(bad,self.p,self.root))
  path=self.root/'registry/persons.json';old=path.read_bytes()
  try:
   people=json.loads(old);person=next(p for p in people['persons']if p['id']==self.roles['weizu']);person['evidence']=[e for e in person['evidence']if e.get('chapter_id')!=t.core.CID];path.write_text(json.dumps(people));self.assertFalse(t.family_valid(a,self.p,self.root))
  finally:path.write_bytes(old)
 def test_full_legal_uid_relocation(self):
  old=self.roles['weizu'];new='z7q_0aa_9tt';self.assertNotIn(new,{p['id']for p in t.core.read(self.root,'registry/persons.json')['persons']});back={}
  def replace(x):
   if isinstance(x,dict):return{k:replace(v)for k,v in x.items()}
   if isinstance(x,list):return[replace(v)for v in x]
   return new if x==old else x
  try:
   for rel in self.paths:
    if not rel.endswith('.json')or rel in {t.EP,ner.EP,t.core.EP}:continue
    path=self.root/rel;raw=path.read_bytes();value=json.loads(raw);after=replace(value)
    if value!=after:back[rel]=raw;path.write_text(json.dumps(after,ensure_ascii=False))
   ch=t.core.read(self.root,t.core.CH);roles,_=ner.prepared(ch,self.root);self.assertEqual(roles['weizu'],new)
   ps={p['id']:(ch['id'],p)for p in ch['paragraphs']}
   for a in t.core.read(self.root,'corpus/jinshu/031-jia-comparison-assertions.json')['assertions']:self.assertTrue(t.family_valid(a,ps,self.root))
  finally:
   for rel,raw in back.items():(self.root/rel).write_bytes(raw)
  self.assertEqual(ner.prepared(self.ch,self.root)[0],self.roles)
if __name__=='__main__':unittest.main(verbosity=2)
