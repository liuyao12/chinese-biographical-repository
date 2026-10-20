# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.bound_serial_posthumous import valid
from scripts.primary_era_abbreviation import valid as era_valid
from scripts.validate_corpus import normalized_date_errors
ROOT=Path(__file__).resolve().parents[1];PREFIX='corpus/weishu-weishou/038-wanghuilong'
def read(n):return json.loads((ROOT/n).read_text())
class BoundSerialGifts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read(PREFIX+'.json');cls.pars={p['id']:(cls.c['id'],p)for p in cls.c['paragraphs']};cls.ms={m['id']:(cls.c['id'],p['id'],m)for p in cls.c['paragraphs']for m in p['mentions']};cls.es={e['id']:e for e in read(PREFIX+'-life-events.json')['events']};cls.hs=[h for h in read(PREFIX+'-titles.json')['holdings']if h['mode']=='posthumous_grant'];cls.fixture=read('tests/fixtures/bound-posthumous-primary-cases.json');cls.date=next(e['normalized_date']for e in cls.es.values()if e.get('normalized_date',{}).get('year')==440)
 def test_six_full_real_paragraphs(self):
  self.assertEqual(len(self.hs),6)
  for h in self.hs:self.assertTrue(valid(h,self.pars,self.ms,self.es),h['id'])
 def bad(self,edit,index=0):
  h=copy.deepcopy(self.hs[index]);edit(h);self.assertFalse(valid(h,self.pars,self.ms,self.es))
 def test_wrong_recipient(self):self.bad(lambda h:h.__setitem__('person_id','other-person'))
 def test_wrong_death_event(self):self.bad(lambda h:h['posthumous_basis'].__setitem__('death_event_id','missing'))
 def test_no_lifetime_grant(self):self.bad(lambda h:h.__setitem__('mode','grant'))
 def test_no_inferred_gift_year(self):self.bad(lambda h:h['effective_period']['start'].__setitem__('date_expression','真君元年'))
 def test_no_inferred_issuer(self):self.bad(lambda h:h['posthumous_basis']['issuer'].__setitem__('person_id','emperor'))
 def test_wrong_death_span(self):self.bad(lambda h:h['posthumous_basis']['death_anchor'].__setitem__('start',0))
 def test_title_partition_gap(self):self.bad(lambda h:h['posthumous_basis']['title_parts'][0].__setitem__('end',1))
 def test_cannot_invent_title_partition(self):self.bad(lambda h:h.__setitem__('title','軍'))
 def test_nearest_child_not_parent(self):
  h=next(h for h in self.hs if h['title']=='征北將軍');x=copy.deepcopy(h);ctx=x['posthumous_basis']['death_subject_context'];ctx['parent_mention_id']=ctx['child_mention_id'];self.assertFalse(valid(x,self.pars,self.ms,self.es))
 def test_wrong_sibling_victim_context(self):
  h=copy.deepcopy(next(h for h in self.hs if h['person_id']=='7ad_718_47c_AAA'));ctx=h['posthumous_basis']['death_subject_context'];ctx['subject_mention_id']=ctx['relative_mention_id'];self.assertFalse(valid(h,self.pars,self.ms,self.es))
 def test_wrong_will_speaker_or_petition_agent(self):
  for key in ['speaker_mention_id','petition_agent_mention_id']:
   h=copy.deepcopy(self.hs[0]);ctx=h['posthumous_basis']['intervening_context'];ctx[key]=ctx['addressee_mention_id'];self.assertFalse(valid(h,self.pars,self.ms,self.es))
 def test_all_fiftynine_existing_title_ids_retained(self):
  hs=read(PREFIX+'-titles.json')['holdings'];self.assertEqual(len(hs),65);self.assertTrue(set(self.fixture['baseline_title_ids'])<={h['id']for h in hs});self.assertEqual(len(self.fixture['baseline_title_ids']),59)
 def test_no_death_end_cutoff_no_birth_estimate(self):
  hs=read(PREFIX+'-titles.json')['holdings'];self.assertEqual(sum(h['effective_period']['end']['status']!='unknown'for h in hs),2);self.assertTrue(all(h['effective_period']['end']['status']=='unknown'for h in self.hs));self.assertTrue(all(a['birth_year']is None for a in self.c['annotation']['age_assertions']))
 def test_death_and_original_grants_440_but_gifts_undated(self):
  self.assertEqual(self.date['year'],440);hs=read(PREFIX+'-titles.json')['holdings'];dated=[h for h in hs if h['effective_period']['start'].get('date_expression')=='真君元年'];self.assertEqual(len(dated),3);self.assertTrue(all(h['effective_period']['start']['normalized_date']['year']==440 for h in dated));self.assertTrue(all(h['effective_period']['start']['date_expression']is None for h in self.hs))
 def test_middle_range_stays_range(self):
  hs=read(PREFIX+'-titles.json')['holdings'];ranges=[h['effective_period']['start']for h in hs if 'normalized_date_range'in h['effective_period']['start']];self.assertEqual(len(ranges),3);self.assertTrue(all('normalized_date'not in b for b in ranges))
 def test_cuihong_complete_parallel_clause(self):
  x=self.fixture['cuihong'];p=x['paragraph'];pars={p['id']:(x['chapter_id'],p)};ms={m['id']:(x['chapter_id'],p['id'],m)for m in p['mentions']};es={x['event']['id']:x['event']};self.assertTrue(valid(x['candidate'],pars,ms,es))
  bad=copy.deepcopy(x['candidate']);ctx=bad['posthumous_basis']['death_subject_context'];bad['posthumous_basis']['topic_person_mention_id']=ctx['envoy_mention_id'];self.assertFalse(valid(bad,pars,ms,es))
 def test_true_short_era_bridge(self):self.assertTrue(era_valid(self.date,{self.c['id']:self.c},ROOT));self.assertEqual(normalized_date_errors(self.date,{self.c['id']:self.c},root=ROOT),[])
 def test_wrong_primary_hash_revision_ruler_or_polity(self):
  for key in ['raw_sha256','source_commit']:
   d=copy.deepcopy(self.date);d['era_name_bridge']['primary_witness'][key]='wrong';self.assertFalse(era_valid(d,{self.c['id']:self.c},ROOT))
  d=copy.deepcopy(self.date);d['era_name_bridge']['ruler_person_id']='other';self.assertFalse(era_valid(d,{self.c['id']:self.c},ROOT))
  d=copy.deepcopy(self.date);d['references'][0]['columns']['dynasty']='曹魏';self.assertTrue(normalized_date_errors(d,{self.c['id']:self.c},root=ROOT))
 def test_arbitrary_prefix_not_equivalent(self):
  d=copy.deepcopy(self.date);d['era_name_bridge']['omitted_prefix']='任意';self.assertTrue(normalized_date_errors(d,{self.c['id']:self.c},root=ROOT))
 def test_wrong_origin_era_span_or_year(self):
  for key in ['year','era_year']:
   d=copy.deepcopy(self.date);d[key]=441;self.assertTrue(normalized_date_errors(d,{self.c['id']:self.c},root=ROOT))
  d=copy.deepcopy(self.date);d['era_name_bridge']['source_expression_anchor']['start']=0;self.assertTrue(normalized_date_errors(d,{self.c['id']:self.c},root=ROOT))
 def test_synthetic_other_death_not_biography_topic(self):
  # Every byte/hash/span is internally consistent; only the stated victim differs.
  def case(other):
   text='甲'+('乙'if other else'')+'卒贈司空';pos=text.index('卒');pid='synthetic:subject-negative';ms=[{'id':'synthetic:m0','start':0,'end':1,'surface':'甲','kind':'person','person_id':'synthetic:甲'}]
   if other:ms.append({'id':'synthetic:m1','start':1,'end':2,'surface':'乙','kind':'person','person_id':'synthetic:乙'})
   p={'id':pid,'text':text,'text_layer':'received_chapter','source_position':{'revision_id':'synthetic-negative-test'},'mentions':ms};e={'work_id':'synthetic','book_id':'synthetic','source_id':'synthetic','chapter_id':'synthetic','paragraph_id':pid,'quote':text,'person_mention_id':'synthetic:m0'}
   a=lambda start,end:{'paragraph_id':pid,'start':start,'end':end,'surface':text[start:end]};h=copy.deepcopy(self.hs[0]);h.update(person_id='synthetic:甲',title='司空',evidence=[e]);h['effective_period']['start']['evidence']=[e];h['attestations']=[dict(a(pos+2,len(text)),id='synthetic:attestation',person_mention_id='synthetic:m0',usage='posthumous_usage',date_expression=None)]
   h['posthumous_basis']={'kind':'bound_death_serial_gift','source_term':text,'death_event_id':'synthetic:event','death_anchor':a(pos,pos+1),'grant_anchor':a(pos+1,len(text)),'title_parts':[a(pos+2,len(text))],'topic_person_mention_id':'synthetic:m0','intervening_context':{'kind':'immediate'},'death_subject_context':{'kind':'explicit_restatement','person_mention_id':'synthetic:m0'},'issuer':{'person_id':None,'source_anchor':None},'source_revision':'synthetic-negative-test','paragraph_sha256':__import__('hashlib').sha256(text.encode()).hexdigest(),'evidence':[e]};event={'id':'synthetic:event','person_id':'synthetic:甲','event_type':'death','status':'source_attested','source_term':'卒','date_expression':None,'evidence':[e]}
   return valid(h,{pid:('synthetic',p)},{m['id']:('synthetic',pid,m)for m in ms},{event['id']:event})
  self.assertTrue(case(False));self.assertFalse(case(True))
 def test_envoy_cannot_become_dead_recipient_by_consistent_retagging(self):
  x=self.fixture['cuihong'];p=x['paragraph'];h=copy.deepcopy(x['candidate']);event=copy.deepcopy(x['event']);mid=h['posthumous_basis']['death_subject_context']['envoy_mention_id'];m=next(m for m in p['mentions']if m['id']==mid);h['person_id']=m['person_id'];event['person_id']=m['person_id'];h['posthumous_basis']['topic_person_mention_id']=mid
  for e in h['evidence']:e['person_mention_id']=mid
  for e in event['evidence']:e['person_mention_id']=mid
  for a in h['attestations']:a['person_mention_id']=mid
  self.assertFalse(valid(h,{p['id']:(x['chapter_id'],p)},{m['id']:(x['chapter_id'],p['id'],m)for m in p['mentions']},{event['id']:event}))
 def test_primary_raw_requires_explicit_fixture_root(self):
  import tempfile
  raw_path=self.date['era_name_bridge']['primary_witness']['raw_path']
  with tempfile.TemporaryDirectory()as temp:
   root=Path(temp);f=root/raw_path;f.parent.mkdir(parents=True);f.write_bytes((ROOT/raw_path).read_bytes());self.assertEqual(normalized_date_errors(self.date,{self.c['id']:self.c},root=root),[]);f.unlink();self.assertTrue(normalized_date_errors(self.date,{self.c['id']:self.c},root=root))
