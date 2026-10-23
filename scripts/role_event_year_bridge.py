"""Reviewed archived-event dates for position-bound biography roles, never ambient years."""
import hashlib,re,json
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1]
EXACT={('accession_office_series','rank1'):'king_accession',('accession_office_series','office1'):'king_accession',('accession_office_series','office2'):'imperial_accession',('accession_office_series','office3'):'imperial_accession',('testamentary_successor_office_series','rank'):'successor_accession',('campaign_office_series','office3'):'named_appointment',('testamentary_successor_office_series','office'):'named_appointment'}
RANGES={('accession_office_series','office4'),('accession_office_series','rank2')}
def project(raw):
 return ''.join(c for c in re.sub(r'<pb:[^>]*>','',raw)if not c.isspace()and c not in '()¶')
def span(t,a):
 return isinstance(a,dict)and set(a)=={'start','end','quote'}and type(a.get('start'))is int and type(a.get('end'))is int and 0<=a['start']<a['end']<=len(t)and t[a['start']:a['end']]==a.get('quote')
def reference(ref,root):
 assert ref['projection']=='kanripo_all_layers_drop_layout_wrappers_v1'
 p=PurePosixPath(ref['path']);assert not p.is_absolute()and '..'not in p.parts and str(p).startswith('source-evidence/')
 q=(root/str(p)).resolve();assert root.resolve()in q.parents
 b=q.read_bytes();assert hashlib.sha256(b).hexdigest()==ref['sha256']and re.fullmatch('[a-f0-9]{40}',ref['revision'])
 assert re.fullmatch(r'KR2a0012_\d{3}\.txt',ref['file'])and ref['url']=='https://raw.githubusercontent.com/kanripo/KR2a0012/'+ref['revision']+'/'+ref['file']
 t=project(b.decode());assert all(span(t,ref[k])for k in ['head','era','year','event'])
 assert ref['head']['start']<ref['event']['start']
 return t
def number(s):return {'元':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}[s]
def point(proof,root):
 t=reference(proof,root);m=proof['mapping'];a,b,n=m['first'],m['last'],number(m['source_number']);r=proof['calendar_reference']
 assert m['era_name']in('延康','黃初')and m['source_era_name']in(m['era_name'],'黄初')and(m['source_era_name']!='黄初'or m['era_name']=='黃初')
 assert r=={'url':'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=1','scope':'modern_era_year_equivalence_only','quote':m['era_name'],'columns':{'era_name':m['era_name'],'first_year':str(a),'last_year':str(b)}}
 assert (m['era_name'],a,b)in(('延康',220,220),('黃初',220,226))and a+n-1<=b
 era,yr,event=proof['era'],proof['year'],proof['event'];kind=proof['event_kind'];q=event['quote']
 if kind=='king_accession':
  assert m['era_name']=='延康'and n==1 and q=='太祖崩嗣位為丞相魏王'and yr['quote']=='改建安二十五年為延康元年'and event['end']<yr['start']
 elif kind=='imperial_accession':
  assert m['era_name']=='黃初'and n==1 and q=='乃為壇於繁陽庚午王升壇即阼百官陪位事訖降壇視燎成禮而反改延康為黃初大赦'and yr['quote']=='黃初元年'and event['end']<=yr['start']
 elif kind=='successor_accession':
  assert m['era_name']=='黃初'and n==7 and q=='七年夏五月帝病篤乃立為皇太子丁巳即皇帝位大赦'and yr['quote']=='七年夏五月'and yr['start']==event['start']and era['quote']=='黄初'
 elif kind in('named_appointment','holding_attested_before_appointment'):
  actor,title=proof['actor'],proof['title'];assert span(t,actor)and span(t,title)and event['start']<=actor['start']<actor['end']<=event['end']and event['start']<=title['start']<title['end']<=event['end']
  assert actor['quote']+'為'+title['quote']in q and title['start']==actor['end']+1 and era['start']<yr['start']<=event['start']
  assert yr['quote']in('六年春二月','七年夏五月')and n==number(yr['quote'][0])
  assert not re.search('[元一二三四五六七八九十]+年',t[yr['end']:event['start']])
  if kind=='holding_attested_before_appointment':assert q.startswith('其以尚書令潁鄉侯')and title['quote']=='鎮軍大將軍'
 else:raise AssertionError('unknown event syntax')
 assert m['source_era_name']in era['quote']and not any(e in t[era['end']:event['start']]for e in ('太和元年','青龍元年','景初元年'))
 return a+n-1
def valid(h,ch,root=None):
 try:
  root=Path(root or ROOT).resolve()
  try:
   from scripts.biographical_appointment_sequence import analyse,SLOTS
  except ImportError:
   from biographical_appointment_sequence import analyse,SLOTS
  b=h['source_role_year_bridge'];seq=h['source_role_sequence'];key=(seq['rule'],h['source_role_slot']);a=h['attestations'][0];p=next(p for p in ch['paragraphs']if p['id']==seq['paragraph_id']);ms={m['id']:m for m in p['mentions']}
  _,_,fields=analyse(seq,ch,h['person_id']);kind,mode,_,original_time=SLOTS[seq['rule']][h['source_role_slot']]
  assert h['title']==fields[h['source_role_slot']]['surface']and h['kind']==kind and h['mode']==mode and h['source_time_scope']['source_expression']==original_time
  assert b['kind']=='reviewed_archived_role_event'and b['status']=='contextual_provisional'and b['human_reviewed']is False and b['holding_id']==h['id']and b['person_id']==h['person_id']and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()
  assert b['source_revision']==ch['source'].get('source_commit',ch['source'].get('revision_id'))and b['rationale']
  assert h['effective_period']['end']=={'status':'unknown','date_expression':None,'evidence':[]}
  start=h['effective_period']['start'];assert start['status']=='source_event'and start['event_type']==h['mode']and start['date_expression']is None and start['evidence']==h['evidence']
  v=start.get('normalized_date',start.get('normalized_date_range'));assert isinstance(v,dict)and v['evidence']==h['evidence']and v['original_quote']==seq['scope_anchor']['surface']and v['human_reviewed']is False and v['status']=='editorial_provisional'and v['year_numbering']=='astronomical'and v['calendar']=='chinese_civil'
  assert all(v.get(k)is None for k in ['month','day','lunar_month','lunar_day','source_date_parts'])and v['rationale']and v['reviewer']
  head=ms[seq['biography_subject_mention_id']];assert head['person_id']==h['person_id']and head['start']==0 and h['status']=='source_attested'and h['human_reviewed']is False
  assert len(h['attestations'])==1 and ms[a['person_mention_id']]['person_id']==h['person_id']and a['surface']==fields[h['source_role_slot']]['surface']and a['start']==fields[h['source_role_slot']]['start']and a['end']==fields[h['source_role_slot']]['end']
  assert h['evidence']==[dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=ch['id'],source_id=ch['source_id'],paragraph_id=p['id'],quote=seq['scope_anchor']['surface'],person_mention_id=a['person_mention_id'])]
  refs=b['proofs'];assert refs and all(x['revision']==b['source_revision']for x in refs)
  if key in RANGES:
   assert 'normalized_date'not in start and v['basis']=='reviewed_role_event_year_range'and v['precision']=='year_range'and len(refs)==2 and refs[0]['event_kind']=='imperial_accession'and refs[1]['event_kind']=='holding_attested_before_appointment'
   lo,hi=point(refs[0],root),point(refs[1],root);assert v['earliest']=={'era':'CE','era_year':lo,'year':lo}and v['latest']=={'era':'CE','era_year':hi,'year':hi}and 'year'not in v
   assert refs[1]['actor']['quote']==head['surface']and h['title']in refs[1]['event']['quote']and lo<=hi
   assert v['references']==[r['calendar_reference']for r in refs]
   yr=None;status='external_event_year_range'
  else:
   assert key in EXACT and len(refs)==1 and refs[0]['event_kind']==EXACT[key]and 'normalized_date_range'not in start
   ref=refs[0];yr=point(ref,root);assert v['precision']=='year'and v['year']==v['era_year']==yr and v['era']=='CE'and v['regnal_year_mapping']['kind']=='reviewed_archived_role_event'
   if ref['event_kind']=='named_appointment':assert ref['actor']['quote']==head['surface']and ref['title']['quote']==h['title']
   assert v['source_expression']==h['source_time_scope']['source_expression']
   m=ref['mapping'];assert v['regnal_year_mapping']=={'kind':'reviewed_archived_role_event','era_name':m['era_name'],'source_era_name':m['source_era_name'],'source_number':m['source_number'],'regnal_year':number(m['source_number']),'start_ce_year':m['first'],'end_ce_year':m['last'],'reference_index':0}and v['references']==[ref['calendar_reference'],{'url':ref['url'],'quote':ref['event']['quote'],'scope':'received_parallel_event'},{'url':ref['url'],'quote':ref['year']['quote'],'scope':'received_regnal_year_attestation'}]
   assert v['basis']=={'kind':'parallel_event','source_event_quote':seq['scope_anchor']['surface'],'reference_url':ref['url'],'reference_event_quote':ref['event']['quote'],'reference_year_quote':ref['year']['quote']}
   status='external_event_year'
  # Bind the explicitly resolved issuer/successor, including bare帝's named antecedent.
  role='successor'if seq['rule']=='testamentary_successor_office_series'else'ruler';ruler=ms[seq['roles'][role]];ant=ms[b['local_ruler_antecedent_mention_id']]
  assert ant['person_id']==ruler['person_id']==b['ruler_person_id']and ant['surface']in('文帝','明帝')and ant['start']<=ruler['start']
  for ref in refs:
   assert ref['head']['quote'].startswith(ant['surface'][:-1]+'皇帝諱')and ref['head']['quote'].endswith('太子也')
  scope=h['source_time_scope'];assert scope['normalized_start_year']==yr and scope['normalized_end_year']is None and scope['status']==status
  return True
 except(KeyError,TypeError,ValueError,OSError,StopIteration,AssertionError,IndexError):return False
def normalized_valid(date,h,role,chapters,root):
 try:return role=='start'and isinstance(h,dict)and date==h.get('effective_period',{}).get('start',{}).get('normalized_date')and valid(h,chapters.get(h['evidence'][0]['chapter_id'],{}),root)
 except(KeyError,TypeError,IndexError):return False
def range_errors(v,evidence,expression,root=None):
 try:
  root=Path(root or ROOT);b=v['role_event_record'];path=PurePosixPath(b['path']);assert not path.is_absolute()and '..'not in path.parts and str(path).startswith('corpus/')
  h=next(h for h in json.loads((root/str(path)).read_text())['holdings']if h['id']==b['holding_id']);assert h['effective_period']['start'].get('normalized_date_range')==v and v['evidence']==evidence and expression is None
  cp=root/b['chapter_path'];assert root.resolve()in cp.resolve().parents;ch=json.loads(cp.read_text());assert valid(h,ch,root);return []
 except(KeyError,TypeError,ValueError,OSError,StopIteration,AssertionError):return ['跨篇官序範圍須有完整同人角色、兩界原證及固定來源，不能冒精確年']
