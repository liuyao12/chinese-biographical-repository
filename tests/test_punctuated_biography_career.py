"""Invented persons/IDs, production career hook; no historical source/person whitelist."""
import unittest,copy,re,hashlib
from scripts.punctuated_biography_career import FRAMES,KIND,proposal_errors,sister_valid,death_valid
from scripts.received_career_roles import holding_valid

def fixture(rule='initial_local',slot=None,recipient=None,overrides=None):
 values=dict(office='縣令',office2='右衛率',office3='驍騎將軍',rank='清河男',date='太康八年',proposal1='景',proposal2='穆',rulepost='簡',postname='簡')
 if overrides:values.update(overrides)
 prefix='沈寧，字子安，廣陵人也。';pid='synthetic-paragraph';person='person-alpha';head=dict(id='head',start=0,end=2,surface='沈寧',kind='person',person_id=person);mentions=[head];text=prefix;roles={};fields={};start=len(text)
 who={'subject':('寧',person),'visitor':('何平','person-beta'),'ruler':('文皇','person-ruler'),'colleague':('許安','person-colleague'),'ancestor':('景皇','person-ancestor')}
 for token in re.split(r'(<[^>]+>|\{[^}]+\})',FRAMES[rule][0]):
  if not token:continue
  if token.startswith('<'):
   key=token[1:-1];base=key.split('_repeat')[0];surface,personid=who[base];m=dict(id='role-'+key,start=len(text),end=len(text)+len(surface),surface=surface,kind='person',person_id=personid);mentions.append(m);roles[key]=m['id'];text+=surface
  elif token.startswith('{'):
   key=token[1:-1];s=values[key];fields[key]=dict(paragraph_id=pid,start=len(text),end=len(text)+len(s),surface=s);text+=s
  else:text+=token
 p=dict(id=pid,text=text,text_layer='received_chapter',mentions=mentions);ch=dict(id='synthetic-chapter',work_id='synthetic-work',book_id='synthetic-book',source_id='synthetic-source',source=dict(revision_id=7),paragraphs=[p])
 if slot is None:slot,recipient,*_=FRAMES[rule][1][0]
 if recipient is None:recipient=next(x[1]for x in FRAMES[rule][1]if x[0]==slot)
 spec=next(s for s in FRAMES[rule][1]if s[0]==slot and s[1]==recipient);_,_,kind,mode,semantic,time=spec
 assert time is None,'date-range fixtures tested separately'
 m=head if recipient=='head'else next(m for m in mentions if m['id']==roles[recipient]);e=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=pid,quote=text,person_mention_id=m['id']);unknown=dict(status='unknown',date_expression=None,evidence=[])
 b=dict(kind=KIND,rule=rule,paragraph_id=pid,source_revision=7,paragraph_sha256=hashlib.sha256(text.encode()).hexdigest(),head_mention_id=head['id'],scope_anchor=dict(paragraph_id=pid,start=start,end=len(text),surface=text[start:]),roles=roles,fields=fields,human_reviewed=False,slot=slot,recipient_role=recipient)
 h=dict(id='holding',person_id=m['person_id'],title=fields[slot]['surface'],kind=kind,mode=mode,appointment_role=semantic,status='source_attested',human_reviewed=False,source_career_role=b,evidence=[e],attestations=[dict(id='occurrence',**fields[slot],person_mention_id=m['id'],usage='narrative',date_expression=None)],effective_period=dict(start=dict(status='source_event',event_type=mode,date_expression=None,evidence=[e]),end=unknown))
 if mode=='posthumous_naming':h['naming_basis']=dict(source_term=b['scope_anchor']['surface'],death_term='卒',evidence=h['evidence'])
 return ch,h
class PunctuatedCareer(unittest.TestCase):
 def test_initial(self):c,h=fixture();self.assertTrue(holding_valid(h,c))
 def bad(self,mutate):
  c,h=fixture();mutate(c,h);self.assertFalse(holding_valid(h,c))
 def test_prose_as_office(self):c,h=fixture(overrides=dict(office='少與'));self.assertFalse(holding_valid(h,c))
 def test_place_as_office(self):c,h=fixture(overrides=dict(office='太原陽曲'));self.assertFalse(holding_valid(h,c))
 def test_other_owner(self):self.bad(lambda c,h:h.update(person_id='person-beta'))
 def test_wrong_source(self):self.bad(lambda c,h:h['evidence'][0].update(source_id='other'))
 def test_short_quote(self):self.bad(lambda c,h:h['evidence'][0].update(quote='初為縣令'))
 def test_wrong_offset(self):self.bad(lambda c,h:h['attestations'][0].update(start=0))
 def test_wrong_scope(self):self.bad(lambda c,h:h['source_career_role']['scope_anchor'].update(start=0))
 def test_false_date(self):self.bad(lambda c,h:h['effective_period']['start'].update(date_expression='太康八年'))
 def test_death_as_tenure_end(self):self.bad(lambda c,h:h['effective_period']['end'].update(status='source_event',date_expression='太康八年'))
 def test_wrong_rule(self):self.bad(lambda c,h:h['source_career_role'].update(rule='paired_and_promoted'))
 def test_paired_each_person(self):
  for who in ['head','colleague']:
   c,h=fixture('paired_and_promoted','office',who,dict(office='中庶子'));self.assertTrue(holding_valid(h,c));h['person_id']='person-ruler';self.assertFalse(holding_valid(h,c))
 def test_foreign_collapsed_into_head(self):
  c,h=fixture('paired_and_promoted','office','colleague',dict(office='中庶子'))
  next(m for m in c['paragraphs'][0]['mentions']if m['id']=='role-colleague')['person_id']='person-alpha';h['person_id']='person-alpha';self.assertFalse(holding_valid(h,c))
 def test_rank_distinct(self):c,h=fixture('paired_and_promoted','rank','head',dict(office='中庶子'));self.assertTrue(holding_valid(h,c));h['kind']='office';self.assertFalse(holding_valid(h,c))
 def test_posthumous_only_actual_grant(self):
  c,h=fixture('posthumous_deliberation');self.assertTrue(holding_valid(h,c));h['title']='景';self.assertFalse(holding_valid(h,c))
 def test_posthumous_not_lifetime(self):
  c,h=fixture('posthumous_deliberation');h['mode']='grant';self.assertFalse(holding_valid(h,c))
 def test_posthumous_needs_death_basis(self):
  c,h=fixture('posthumous_deliberation');h.pop('naming_basis');self.assertFalse(holding_valid(h,c))
 def test_not_a_source_explicit_date(self):
  c,h=fixture();h['effective_period']['start']['normalized_date']=dict(year=287);self.assertFalse(holding_valid(h,c))
 def test_proposal_and_grant_distinct(self):
  c,h=fixture('posthumous_deliberation');b=h['source_career_role'];fs=b['fields'];q=dict(person_id=h['person_id'],person_mention_id=h['evidence'][0]['person_mention_id'],title=fs['proposal1']['surface'],role_anchor=fs['proposal1'],source_appointment_context={**b,'slot':'proposal1','recipient_role':'subject'},proposal_kind='posthumous_name_proposal',outcome='not_enacted',status='contextual_provisional',human_reviewed=False,effective_service_attested=False,actual_grant_title=fs['postname']['surface'],actual_grant_anchor=fs['postname'],date_expression=None,evidence=h['evidence'],reviewer='AI',interpretation_note='synthetic rejected proposal')
  self.assertEqual(proposal_errors(q,c,{h['person_id']}),[]);q['outcome']='not_reported';self.assertTrue(proposal_errors(q,c,{h['person_id']}))

def sister_fixture():
 t='寧有寡姊';pid='sibling-paragraph';ms=[dict(id='brother',kind='person',person_id='person-younger',start=0,end=1,surface='寧'),dict(id='sister',kind='person',person_id='person-older',start=2,end=4,surface='寡姊')];c=dict(id='sibling-chapter',work_id='work',book_id='book',source_id='source',source=dict(revision_id=7),paragraphs=[dict(id=pid,text=t,mentions=ms)])
 b=dict(kind='has_widowed_older_sister',paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),source_revision=7,human_reviewed=False,scope_anchor=dict(paragraph_id=pid,start=0,end=4,surface=t));e=dict(work_id='work',book_id='book',source_id='source',chapter_id=c['id'],paragraph_id=pid,quote=t,subject_person_mention_id='sister',object_person_mention_id='brother')
 a=dict(predicate='sister',subject_person_id='person-older',object_person_id='person-younger',qualifiers=dict(source_term='寡姊',relative_birth_order=dict(older_person_id='person-older',younger_person_id='person-younger',operator='lt',scope='siblings',older_ordinal=None,younger_ordinal=None),source_clause_binding=b),status='source_attested',human_reviewed=False,evidence=[e]);return c,a
class WidowedSister(unittest.TestCase):
 def test_positive(self):c,a=sister_fixture();self.assertTrue(sister_valid(a,c))
 def bad(self,fn):c,a=sister_fixture();fn(c,a);self.assertFalse(sister_valid(a,c))
 def test_reversed(self):self.bad(lambda c,a:a.update(subject_person_id='person-younger',object_person_id='person-older'))
 def test_wrong_elder(self):self.bad(lambda c,a:a['qualifiers']['relative_birth_order'].update(older_person_id='person-younger',younger_person_id='person-older'))
 def test_no_absolute_order(self):self.bad(lambda c,a:a['qualifiers']['relative_birth_order'].update(older_ordinal=1))
 def test_no_father(self):self.bad(lambda c,a:a['qualifiers'].update(shared_father=True))
 def test_wrong_source(self):self.bad(lambda c,a:a['evidence'][0].update(source_id='another'))
 def test_wrong_term(self):self.bad(lambda c,a:a['qualifiers'].update(source_term='妹'))

def death_fixture():
 t='及寧疾病，詔賜錢二十萬，日給酒米。太康八年卒';pid='death-paragraph';m=dict(id='subject',kind='person',person_id='person-alpha',start=1,end=2,surface='寧');c=dict(id='death-chapter',work_id='work',book_id='book',source_id='source',source=dict(revision_id=7),paragraphs=[dict(id=pid,text=t,mentions=[m])]);i=t.index('太康');death=dict(paragraph_id=pid,start=len(t)-1,end=len(t),surface='卒');date=dict(paragraph_id=pid,start=i,end=i+4,surface='太康八年');e=dict(work_id='work',book_id='book',source_id='source',chapter_id=c['id'],paragraph_id=pid,quote=t,person_mention_id='subject');b=dict(kind='punctuated_biography_death_report',rule='illness_gift_then_dated_death',source_revision=7,paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),human_reviewed=False,subject_mention_id='subject',clause_anchor=dict(paragraph_id=pid,start=0,end=len(t),surface=t),death_anchor=death,date_anchor=date)
 event=dict(person_id='person-alpha',event_type='death',status='source_attested',human_reviewed=False,source_death_context=b,source_anchor=death,source_term='卒',date_expression='太康八年',normalized_date=dict(source_expression='太康八年'),evidence=[e]);return c,event
class DeathSubject(unittest.TestCase):
 def test_positive(self):c,e=death_fixture();self.assertTrue(death_valid(e,c))
 def bad(self,fn):c,e=death_fixture();fn(c,e);self.assertFalse(death_valid(e,c))
 def test_wrong_person(self):self.bad(lambda c,e:e.update(person_id='other'))
 def test_wrong_date(self):self.bad(lambda c,e:e.update(date_expression='太康九年'))
 def test_wrong_source(self):self.bad(lambda c,e:e['evidence'][0].update(source_id='other'))
 def test_short_quote(self):self.bad(lambda c,e:e['evidence'][0].update(quote='卒'))
 def test_wrong_death_word(self):self.bad(lambda c,e:e.update(source_term='病'))

def dismissal_fixture():
 c,h=fixture();p=c['paragraphs'][0];p['text']+='：「遠矣。」遂送何平出界數百里，坐此免官。';t=p['text'];h['source_career_role']['paragraph_sha256']=hashlib.sha256(t.encode()).hexdigest();h['evidence'][0]['quote']=t
 start=t.index('遂送');j=t.index('何平',start);m=dict(id='later-visitor',start=j,end=j+2,surface='何平',kind='person',person_id='person-beta');p['mentions'].append(m);st=t.index('坐此免官',start);a=dict(paragraph_id=p['id'],start=st,end=st+4,surface='坐此免官');b=dict(kind=KIND,rule='excursion_dismissal',paragraph_id=p['id'],source_revision=7,paragraph_sha256=hashlib.sha256(t.encode()).hexdigest(),head_mention_id='head',scope_anchor=dict(paragraph_id=p['id'],start=start,end=len(t),surface=t[start:]),roles=dict(visitor=m['id']),fields=dict(departure=a),human_reviewed=False,slot='departure',recipient_role='head');e=copy.deepcopy(h['evidence'][0]);e['person_mention_id']='head';d=dict(person_id='person-alpha',kind='office_departure',source_term=a['surface'],source_anchor=a,paragraph_sha256=b['paragraph_sha256'],source_revision=7,date_expression=None,evidence=[e],status='source_attested',human_reviewed=False,source_career_role=b,values=dict(departure_code='dismissal_after_excursion',linked_holding_id=h['id'],date_unknown=True,all_other_offices_ended=False));return c,h,d
class DismissalBinding(unittest.TestCase):
 def run_case(self,fn=None):
  from scripts.received_career_roles import detail_valid
  c,h,d=dismissal_fixture()
  if fn:fn(c,h,d)
  return detail_valid(d,c,{h['id']:h})
 def test_quote_closed_resumption(self):self.assertTrue(self.run_case())
 def test_no_general_tenure_end(self):self.assertFalse(self.run_case(lambda c,h,d:d['values'].update(all_other_offices_ended=True)))
 def test_wrong_linked_office_owner(self):self.assertFalse(self.run_case(lambda c,h,d:h.update(person_id='person-beta')))
 def test_wrong_kind(self):self.assertFalse(self.run_case(lambda c,h,d:d.update(kind='death')))
 def test_no_invented_date(self):self.assertFalse(self.run_case(lambda c,h,d:d.update(date_expression='太康八年')))
 def test_other_person(self):self.assertFalse(self.run_case(lambda c,h,d:d.update(person_id='person-beta')))
