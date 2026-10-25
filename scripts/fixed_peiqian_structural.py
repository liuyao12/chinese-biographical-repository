"""Proposed finite source-role bindings. No text rewriting or ancestor inference."""
from pathlib import Path
import json,hashlib
PROOF='source-evidence/sgz023-peiqian-phaseb/structural-source-proof.json'
SHA='a70a40f34a70f4c5fdf4f5722134513ccbc33e2df1ccc04cd8cb707e922a28db'
def context(ch,root):
 assert isinstance(ch,dict)and isinstance(root,(str,Path));assert isinstance(ch.get('source'),dict)and isinstance(ch.get('paragraphs'),list)and all(isinstance(u,dict)and isinstance(u.get('text'),str)and isinstance(u.get('mentions'),list)and all(isinstance(m,dict)for m in u['mentions'])for u in ch['paragraphs'])
 b=(Path(root)/PROOF).read_bytes();assert hashlib.sha256(b).hexdigest()==SHA;p=json.loads(b);assert all(ch[k]==v for k,v in p['source_dimensions'].items());url=ch['source'].get('permalink')or ch['source'].get('url');assert isinstance(url,str)and url.startswith('https://');assert all(isinstance(ch['source'][k],str)and ch['source'][k].startswith('https://')for k in ['permalink','url']if k in ch['source']);assert ch['source']['revision_id']==p['revision_id']and ch['source'].get('response_sha256')==p['raw_sha256'];assert hashlib.sha256((Path(root)/p['raw_path']).read_bytes()).hexdigest()==p['raw_sha256'];ps={u['id']:u for u in ch['paragraphs']}
 for pid,u in p['units'].items():
  q=ps[pid];assert q['text']==u['text']and q['text_layer']==u['text_layer']and hashlib.sha256(q['text'].encode()).hexdigest()==u['sha256']
 def role(key):
  r=p['roles'][key];q=ps[r['paragraph_id']];m=next(m for m in q['mentions']if m['id']==r['mention_id']);assert type(m.get('start'))is int and type(m.get('end'))is int and isinstance(m.get('person_id'),str)and m['person_id']and m['kind']=='person'and all(m[k]==r[k]for k in ['start','end','surface'])and q['text'][m['start']:m['end']]==m['surface'];return m
 return p,ps,role
def evidence(ch,u,m=None):
 e={k:ch[k]for k in ['work_id','book_id','source_id']};e.update(chapter_id=ch['id'],paragraph_id=u['id'],quote=u['text'])
 if m:e['person_mention_id']=m['id']
 return e
def father(a,child,parent,ch,ps):
 assert a['predicate']=='father'and a['subject_person_id']==child['person_id']and a['object_person_id']==parent['person_id']and a['status']=='source_attested'and a['qualifiers']['lineage']=='paternal'and a['qualifiers']['source_interpretation_status']=='explicit_source_wording';assert not any(a['qualifiers'].get(k)for k in ['adoptive','sworn','same_mother_only'])
 seen=set()
 for ev in a['evidence']:
  u=ps[ev['paragraph_id']];assert ev['quote']==u['text']and ev['source_id']==ch['source_id']and ev['chapter_id']==ch['id'];ms={m['id']:m for m in u['mentions']}
  for field,person in [('subject_person_mention_id',child),('object_person_mention_id',parent)]:
   if field in ev:
    m=ms[ev[field]];assert m['kind']=='person'and m['person_id']==person['person_id'];seen.add(field)
 assert seen=={'subject_person_mention_id','object_person_mention_id'}
def recruitment_valid(event,ch,root):
 try:
  if not (all(isinstance(v,dict)for v in [event,ch]))or not isinstance(root,(str,Path)):return False
  p,ps,role=context(ch,root);subject=role('xiu');patron=role('shuang');a=p['anchors']['recruitment'];u=ps[a['paragraph_id']];assert u['text'][a['start']:a['end']]==a['surface']=='曹爽辟'and a['start']==patron['start']and a['end']==patron['end']+1
  assert event['event_type']=='recruitment'and event['person_id']==subject['person_id']!=patron['person_id']and event['date_expression']is None and'normalized_date'not in event and event['source_term']=='曹爽辟'and event['source_anchor']==a and event['status']=='source_attested'and event['evidence']==[evidence(ch,u,subject)]
  assert event['source_recruitment_binding']==dict(kind='fixed_peiqian_recruitment',key=p['key'],subject_person_mention_id=subject['id'],patron_person_mention_id=patron['id'],patron_person_id=patron['person_id'],source_anchor=a,office_title=None,age_assertion_id=None,human_reviewed=False);return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError,IndexError):return False

def prefix_surface_valid(holding,attestation,ch,root):
 try:
  if not (all(isinstance(v,dict)for v in [holding,attestation,ch]))or not isinstance(root,(str,Path)):return False
  p,ps,role=context(ch,root);m=role('xiu');a=p['anchors'];u=ps[a['office_group']['paragraph_id']]
  assert holding['person_id']==m['person_id']and holding['kind']=='office'and holding['title']=='尚書令'and holding['mode']=='grant'and holding['evidence']==[evidence(ch,u,m)]
  assert holding['source_office_prefix_binding']==dict(kind='fixed_peiqian_office_prefix',key=p['key'],subject_person_mention_id=m['id'],group_anchor=a['office_group'],prefix_anchor=a['office_prefix'],noun_anchor=a['office_noun'],status='contextual_provisional',human_reviewed=False)
  assert a['office_prefix']['surface']+a['office_noun']['surface']==holding['title'];assert attestation['paragraph_id']==u['id']and all(attestation[k]==a['office_noun'][k]for k in ['start','end','surface'])and attestation['person_mention_id']==m['id']and attestation['usage']=='narrative';return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError,IndexError):return False

def bereavement_context_valid(binding,event,ch,ev,root,assertions):
 try:
  if not (all(isinstance(v,dict)for v in [binding,event,ch,ev])and isinstance(assertions,list))or not isinstance(root,(str,Path)):return False
  p,ps,role=context(ch,root);child=role('qian');parent=role('mao');a,=[a for a in assertions if a['id']==p['father_assertion_ids']['mao_qian']];father(a,child,parent,ch,ps);anchor=p['anchors']['father_bereavement'];u=ps[anchor['paragraph_id']]
  expected=dict(kind='fixed_named_parent_bereavement',key=p['key'],father_assertion_id=a['id'],child_person_mention_id=child['id'],father_person_mention_id=parent['id'],supporting_evidence=[evidence(ch,ps[p['roles']['mao']['paragraph_id']],parent)],source_anchor=anchor,human_reviewed=False)
  assert binding==expected and event['event_type']=='death'and event['person_id']==parent['person_id']!=child['person_id']and event['source_term']=='喪父去官'and event['date_expression']is None and'normalized_date'not in event and event['status']=='source_attested';assert ev==dict(evidence(ch,u),context=binding)and u['text'][anchor['start']:anchor['end']]==anchor['surface'];return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError,IndexError):return False
def wrongful_killing_valid(event,ch,root):
 try:
  if not (all(isinstance(v,dict)for v in [event,ch]))or not isinstance(root,(str,Path)):return False
  p,ps,role=context(ch,root);m=role('wei_harm');u=ps[p['roles']['wei_harm']['paragraph_id']];a=p['anchors']['wrongful_killing'];assert event['event_type']=='death'and event['person_id']==m['person_id']and event['source_term']==a['surface']=='被枉害'and event['source_anchor']==a and event['date_expression']is None and'normalized_date'not in event and event['status']=='source_attested'and event['evidence']==[evidence(ch,u,m)];assert event['source_death_interpretation']==dict(kind='fixed_peiqian_passive_wrongful_killing',key=p['key'],source_subject_mention_id=m['id'],contextual_meaning='killed_wrongfully',interpretation_status='contextual_provisional',human_reviewed=False);return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError,IndexError):return False
def office_departure_valid(event,ch,root):
 try:
  if not (all(isinstance(v,dict)for v in [event,ch]))or not isinstance(root,(str,Path)):return False
  p,ps,role=context(ch,root);b=event['source_office_departure_binding'];case=b['case'];assert case in ['qian_parental_mourning','xiu_former_staff_dismissal'];key='qian'if case=='qian_parental_mourning'else'xiu';m=role(key);u=ps[p['roles'][key]['paragraph_id']];term='去官'if key=='qian'else'爽誅以故吏免';at=u['text'].index(term);a=dict(paragraph_id=u['id'],start=at,end=at+len(term),surface=term);pat=next((x for x in u['mentions']if x['kind']=='person'and x['surface']=='爽'),None)if key=='xiu'else None
  assert event['person_id']==m['person_id']and event['event_type']=='office_departure'and event['source_term']==term and event['source_anchor']==a and event['date_expression']is None and'normalized_date'not in event and event['status']=='source_attested'and event['evidence']==[evidence(ch,u,m)]
  _,_,_,dep=departure_spec(ch,root,case)
  expected=dict(kind='fixed_peiqian_office_departure',key=p['key'],case=case,actor_person_mention_id=m['id'],departure_mode='left_office_for_parental_mourning'if key=='qian'else'dismissed_as_former_staff',departed_holding_id=dep['holding_id'],office_identification_status='contextual_provisional',prior_office_anchor=dep['prior_office_anchor'],following_office_anchor=dep['following_office_anchor'],cause_patron_person_id=pat['person_id']if pat else None,cause_patron_person_mention_id=pat['id']if pat else None,related_life_event_id='le-sgz023-peiqian-phaseb-mao-death'if key=='qian'else None,source_anchor=a,human_reviewed=False);assert b==expected and event['title_holding_id']==dep['holding_id']and event['office_title']==dep['title']
  if pat:assert pat['person_id']==role('shuang')['person_id']
  else:assert u['text'][at-2:at]=='喪父'
  return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError,IndexError):return False
def departure_spec(ch,root,case):
 p,ps,role=context(ch,root);assert case in ['qian_parental_mourning','xiu_former_staff_dismissal'];key='qian'if case=='qian_parental_mourning'else'xiu';m=role(key);u=ps[p['roles'][key]['paragraph_id']]
 values=('入為尚書令','尚書令','去官','拜光祿大夫','th-sgz023-peiqian-pqt-049')if key=='qian'else('年二十五遷黄門侍郎','黄門侍郎','爽誅以故吏免','遷衛國相','th-sgz023-peiqian-phaseb-013')
 prior,title,term,following,hid=values;t=u['text'];assert t.count(prior)==t.count(term)==t.count(following)==1;start=t.index(prior);at=t.index(term);after=t.index(following);assert start<at<after
 def a(s,n):return dict(paragraph_id=u['id'],start=n,end=n+len(s),surface=s)
 prior_a=a(title,start+len(prior)-len(title));term_a=a(term,at);following_a=a(following,after);clause=a(t[start:after+len(following)],start)
 return p,u,m,dict(holding_id=hid,title=title,prior_office_anchor=prior_a,departure_anchor=term_a,following_office_anchor=following_a,clause_anchor=clause)
def qualified_office_end_basis(ch,root,case,event_id):
 p,u,m,s=departure_spec(ch,root,case)
 return dict(kind='fixed_named_prior_office_departure',key=p['key'],case=case,departure_event_id=event_id,actor_person_mention_id=m['id'],prior_office_anchor=s['prior_office_anchor'],departure_anchor=s['departure_anchor'],following_office_anchor=s['following_office_anchor'],clause_anchor=s['clause_anchor'],source_term=s['departure_anchor']['surface'],evidence=[evidence(ch,u,m)],interpretation_status='contextual_provisional',rationale='完整同源官序中唯一緊接前職與明示去官／被免相接，下一新職另明言；只結束此職、不泛終其他官爵、不推CE年。',human_reviewed=False)
def office_end_valid(holding,ch,root):
 try:
  if not all(isinstance(v,dict)for v in [holding,ch])or not isinstance(root,(str,Path)):return False
  b=holding.get('end_basis');ev=holding.get('evidence')
  if not isinstance(b,dict)or b.get('case')not in ['qian_parental_mourning','xiu_former_staff_dismissal']or not isinstance(b.get('departure_event_id'),str)or not isinstance(ev,list)or not ev or not all(isinstance(e,dict)for e in ev):return False
  p,u,m,s=departure_spec(ch,root,b['case']);assert holding.get('id')==s['holding_id']and holding.get('title')==s['title']and holding.get('kind')=='office'and holding.get('person_id')==m['person_id'];assert b==qualified_office_end_basis(ch,root,b['case'],b['departure_event_id'])and ev==b['evidence']
  expected_slot='pqt-049'if b['case']=='qian_parental_mourning'else'phaseb-013';assert holding.get('fixed_source_fact_binding')==dict(kind='fixed_kanripo_person_fact_slots',key='sgz023-peiqian-family-qian-finite',slot=expected_slot)
  try:
   from scripts.fixed_kanripo_fact_slots import valid,grammar
  except ModuleNotFoundError as exc:
   if exc.name != 'scripts':raise
   from fixed_kanripo_fact_slots import valid,grammar
  assert valid(holding,ch,root)
  recipe,_=grammar(ch,root);ep=Path(root).resolve()/Path(recipe['chapter_path']).with_name(Path(recipe['chapter_path']).stem+'-person-events.json');assert ep.resolve()==ep;payload=json.loads(ep.read_bytes());assert isinstance(payload,dict)and payload['record_type']=='person_event_assertion_set'and payload['chapter_id']==ch['id']and isinstance(payload.get('events'),list)and all(isinstance(e,dict)for e in payload['events']);event,=[e for e in payload['events']if e.get('id')==b['departure_event_id']];assert valid(event,ch,root)and office_departure_valid(event,ch,root)and event['person_id']==holding['person_id']and event['title_holding_id']==holding['id']and event['office_title']==holding['title'];assert event['evidence']==b['evidence']
  assert holding['effective_period']['end']==dict(status='source_event',event_type='explicit_end',date_expression=None,evidence=b['evidence']);return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration,OSError,IndexError):return False
