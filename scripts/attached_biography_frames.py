# -*- coding: utf-8 -*-
"""Finite complete received paragraph grammars, with typed slots and all person roles.
Templates are reviewed source syntax; records cannot supply executable patterns.
No person, family, chapter or mention-ID allowlist is used.
"""
from pathlib import Path
import json,re,hashlib
KIND='attached_received_biography_frame'
RECIPES=json.loads(Path(__file__).with_name('attached_biography_frames.json').read_text())
OFFICES=('令','主簿','功曹','掾','從事','郎中','中郎','國相','吏部郎','長史','軍司馬','鴻臚','都尉','刺史','將軍','侍中','尚書','議郎','卿','傅','常侍','僕射','左丞','大夫','司徒','校尉','左率','吏部郎','舍人','庶子','黃門郎','督護','內史','郎將','侍郎','太守','佐史')
def anchor(p,x):return isinstance(x,dict)and set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(p['text'])and p['text'][x['start']:x['end']]==x['surface']
def paragraph_frame(b,ch):
 assert (b['kind']==KIND or b['kind']=='biography_family_clause'and b.get('rule')==KIND)and b['human_reviewed']is False and b['source_revision']==ch['source']['revision_id']
 by={p['id']:p for p in ch['paragraphs']};assert len(by)==len(ch['paragraphs']);p=by[b['paragraph_id']];t=p['text'];assert p['text_layer']=='received_chapter'and hashlib.sha256(t.encode()).hexdigest()==b['paragraph_sha256']
 recipe=RECIPES[b['frame']];ms={m['id']:m for m in p['mentions']};rs={k:ms[mid]for k,mid in b['roles'].items()};fs=b['fields'];usedr=set();usedf=set();cursor=0
 for part in re.split(r'(<r[0-9]+>|\{career_[0-9]+\})',recipe['template']):
  if not part:continue
  if part.startswith('<r'):
   k=part[1:-1];v=rs[k];assert v['kind']=='person'and v['start']==cursor and t[v['start']:v['end']]==v['surface'];usedr.add(k)
  elif part.startswith('{career_'):
   k=part[1:-1];v=fs[k];assert anchor(p,v)and v['start']==cursor;usedf.add(k)
  else:assert t.startswith(part,cursor);cursor+=len(part);continue
  cursor=v['end']
 assert cursor==len(t)and set(rs)==usedr and{m['id']for m in rs.values()}=={m['id']for m in p['mentions']if m['kind']=='person'}
 for k,inside in recipe['inside_role_fields'].items():
  v=fs[k];role=rs[inside['role']];assert anchor(p,v)and v['start']==role['start']+inside['prefix']and v['end']==role['end']-inside['suffix'];usedf.add(k)
 assert set(fs)==usedf
 for group in recipe['same_person_groups']:assert len({rs[k]['person_id']for k in group})==1
 for a0,b0 in recipe['distinct_role_groups']:assert rs[a0]['person_id']!=rs[b0]['person_id']
 return p,rs,fs,recipe

def analyse(record,ch,key='source_career_role'):
 b=record[key];p,rs,fs,recipe=paragraph_frame(b,ch);t=p['text']
 slot=recipe['slots'][b['slot']];assert b['recipient_role']==slot['recipient_role'];m=rs[slot['recipient_role']];a=fs[slot['field']]
 assert record['person_id']==m['person_id']
 ev,=record['evidence'];assert ev==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=t,person_mention_id=m['id'])
 return p,m,a,slot,b

def nominal(title,kind,role):
 if not isinstance(title,str)or not 1<=len(title)<=24 or any(w in title for w in ('曰','云','詔','不','未','欲','請','少與','高簡','。','；','：','「','」')):return False
 if kind=='office':return any(title.endswith(x)for x in OFFICES)
 if kind in('noble_rank','royal_rank'):return len(title)>1 and title.endswith(('公','侯','伯','子','男','王'))
 if kind=='honorific':return role in('posthumous_name','posthumous_rank')and(title=='儀同三司'or len(title)==1)
 return kind=='unclassified'and((role=='recommendation_qualification'and title in('孝廉','秀才'))or(role=='command_scope'and re.fullmatch(r'都督[^曰云非不未]+諸軍事',title))or(role=='credential_authority'and title=='假節'))

def holding_valid(h,ch,root=None):
 try:
  if 'inherited_title_binding'in h:return inherited_holding_valid(h,ch)
  p,m,a,s,b=analyse(h,ch);assert s['state']=='holding'and nominal(h['title'],s['kind'],s['appointment_role'])
  if 'source_pin'in RECIPES[b['frame']]:assert pinned_attestation_source_valid(h,ch,root)
  assert h['title']==a['surface']and h['kind']==s['kind']and h['mode']==s['mode']and h['appointment_role']==s['appointment_role']and h['status']=='source_attested'and h['human_reviewed']is False
  phase=s['date_expression'];ev=h['evidence'];unknown=dict(status='unknown',date_expression=None,evidence=[]);att,=h['attestations']
  assert att['paragraph_id']==p['id']and att['start']==a['start']and att['end']==a['end']and att['surface']==a['surface']and att['person_mention_id']==m['id']and att['usage']=='narrative'
  start=h['effective_period']['start'];assert h['effective_period']['end']==unknown
  if s['mode']=='attestation':assert start==unknown and att['date_expression']==phase;date=att
  else:
   assert {k:v for k,v in start.items()if k not in('normalized_date','normalized_date_range')}==dict(status='source_event',event_type=s['mode'],date_expression=phase,evidence=ev)and att['date_expression']is None
   date=start
  if phase:
   assert phase in p['text']
   if phase.endswith(('初','中','末')):
    try:from scripts.date_ranges import year_range_errors
    except ImportError:from date_ranges import year_range_errors
    assert 'normalized_date_range'in date and not year_range_errors(date['normalized_date_range'],ev,phase)and 'normalized_date'not in date
   else:
    try:from scripts.validate_corpus import normalized_date_errors
    except ImportError:from validate_corpus import normalized_date_errors
    assert date['normalized_date']['source_expression']==phase and date['normalized_date']['evidence']==ev and not normalized_date_errors(date['normalized_date'],{ch['id']:ch})
   era=s['civil_era'];value=date.get('normalized_date_range',date.get('normalized_date'));mapping=value.get('era_span_mapping',value.get('regnal_year_mapping'))
   assert mapping['era_name']==era['era_name']and mapping['start_ce_year']==era['first']and mapping['end_ce_year']==era['last']and value['references'][mapping['reference_index']]['columns']['dynasty']==era['dynasty']

  else:assert not any(k in date for k in('normalized_date','normalized_date_range'))
  if s['mode']=='posthumous_grant':assert h['posthumous_basis']['evidence']==ev and h['posthumous_basis']['source_term']==p['text']
  else:assert 'posthumous_basis'not in h
  if s['mode']=='posthumous_naming':assert h['naming_basis']==dict(source_term=p['text'],death_term='薨',evidence=ev)
  else:assert 'naming_basis'not in h
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

def proposal_errors(q,ch,pids):
 try:
  p,m,a,s,b=analyse(q,ch,'source_appointment_context');assert s['state']=='unassumed'and nominal(q['title'],s['kind'],s['appointment_role'])and q['title']==a['surface']and q['role_anchor']==a
  assert q['person_id']==m['person_id']in pids and q['person_mention_id']==m['id']and q['proposal_kind']=='unassumed_appointment'and q['outcome']=='not_assumed'and q['effective_service_attested']is False and q['status']=='contextual_provisional'and q['human_reviewed']is False
  assert q['date_expression']is None and not any(k in q for k in('normalized_date','normalized_date_range'))and q['interpretation_note']and q['reviewer']
  na=q['non_assumption_anchor'];assert anchor(p,na)and na['surface']in('不就','不行')and a['end']<=na['start']and q['non_assumption_kind']=='did_not_take_up'
  return []
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return ['未就/未行須完整附傳語境、原角色與明授官名，不能當已任或擴至後任']

def kin_qualifiers(slot,rs,b):
 q=dict(source_term=slot['source_term'],source_clause_binding=b);s=rs[slot['subject_role']];o=rs[slot['object_role']];pred=slot['predicate']
 if pred=='father':
  q['lineage']='paternal'
  if 'ordinal'in slot:q['birth_order']=dict(parent_person_id=o['person_id'],scope='sons_of_parent',ordinal=slot['ordinal'],position='unspecified',source_term=slot['source_term'],interpretation_status='source_attested')
 elif pred=='maternal_role':q.update(role='mother_unspecified',biological_mother=None,father_person_id=None)
 elif pred=='agnatic_cousin':
  q['kinship_structure']=dict(lineage='paternal',generation_difference=0,collateral=True,distance=None,common_ancestor_person_id=None,subject_relative_age=slot['relative_age'])
  older,younger=(o,s)if slot['relative_age']=='younger'else(s,o)
  q['relative_birth_order']=dict(older_person_id=older['person_id'],younger_person_id=younger['person_id'],operator='lt',scope='agnatic_cousins',older_ordinal=None,younger_ordinal=None)
 elif pred=='brother':
  age=slot.get('subject_relative_age','older');assert age in('older','younger')
  older,younger=(s,o)if age=='older'else(o,s)
  q['relative_birth_order']=dict(older_person_id=older['person_id'],younger_person_id=younger['person_id'],operator='lt',scope='siblings',older_ordinal=None,younger_ordinal=None)
 elif pred=='maternal_aunt':q.update(maternal_path='mother_sister',generation_difference=-1,mother_person_id=None)
 elif pred=='great_grandfather':q.update(lineage='paternal',generation_distance=3,intermediate_person_ids=[None,None])
 elif pred=='ritual_successor_of':q.update(succession_kind='named_ji_hou',legal_adoption_status='not_stated',parentage_inference='not_inferred')
 elif pred=='kinship_unspecified':q.update(kinship_basis='explicit_zhongbiao_relationship',lineage='unspecified',generation_difference=None,exact_distance=None,common_ancestor_person_id=None)
 return q

def kinship_valid(a,paragraphs,chapters=None):
 try:
  b=a['qualifiers']['source_clause_binding'];e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']]
  ch=(chapters or {}).get(cid)
  if ch is None:ch=dict(id=cid,work_id=e['work_id'],book_id=e['book_id'],source_id=e['source_id'],source=dict(revision_id=p['source_position']['revision_id']),paragraphs=[p])
  pp,rs,fs,recipe=paragraph_frame(b,ch);slot=recipe['kinship_slots'][b['slot']];s=rs[slot['subject_role']];o=rs[slot['object_role']]
  assert a['predicate']==slot['predicate']and a['subject_person_id']==s['person_id']!=o['person_id']==a['object_person_id']and a['status']=='source_attested'and a['human_reviewed']is False
  assert e==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],subject_person_mention_id=s['id'],object_person_mention_id=o['id'])
  assert a['qualifiers']==kin_qualifiers(slot,rs,b)and slot['source_term']in p['text']
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

def typed_slot(record,ch,key,category):
 b=record[key];p,rs,fs,recipe=paragraph_frame(b,ch);s=recipe[category+'_slots'][b['slot']];m=rs[s['recipient_role']];assert record['person_id']==m['person_id']and record['human_reviewed']is False and record['status']=='source_attested'
 ev,=record['evidence'];assert ev==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
 return p,m,s,b

def expected_anchor(p,term,phrase=None):
 phrase=phrase or term;assert p['text'].count(phrase)==1 and term in phrase;start=p['text'].index(phrase)+phrase.index(term);return dict(paragraph_id=p['id'],start=start,end=start+len(term),surface=term)

def check_exact_date(value,expression,evidence,ch,era):
 try:from scripts.validate_corpus import normalized_date_errors
 except ImportError:from validate_corpus import normalized_date_errors
 assert value['source_expression']==expression and value['evidence']==evidence and not normalized_date_errors(value,{ch['id']:ch})
 m=value['regnal_year_mapping'];assert m['era_name']==era['era_name']and(m['start_ce_year'],m['end_ce_year'])==(era['first'],era['last'])and value['references'][m['reference_index']]['columns']['dynasty']==era['dynasty']

def life_valid(v,ch):
 try:
  p,m,s,b=typed_slot(v,ch,'source_death_context','life');assert v['event_type']==s['event_type']=='death'and v['source_term']==s['source_term']and v['source_anchor']==expected_anchor(p,s['source_term'],s['source_phrase'])
  assert v['date_expression']==s['date_expression']and not any(k in v for k in('birth_year','death_place','burial_place','normalized_date_range'))
  if s['date_expression']:check_exact_date(v['normalized_date'],s['date_expression'],v['evidence'],ch,s['civil_era'])
  else:assert 'normalized_date'not in v
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

def age_valid(v,ch):
 try:
  p,m,s,b=typed_slot(v,ch,'attached_biography_age_frame','ages');term=s['source_term'];assert term in p['text']and v['source_term']==term and v['source_number']==s['source_number']and v['value']==s['value']and v['source_anchor']==expected_anchor(p,term)
  assert v['birth_year']is None and v['counting']=='unspecified_source_age'and v['unit']=='source_age_years'
  want=dict(kind=s['age_context'])
  if s['age_context']=='at_death':want['life_event_id']=s.get('life_event_id','le-jin043-shantao-'+s['life_slot'])
  assert v['age_context']==want
  try:from scripts.chinese_civil_years import numeral
  except ImportError:from chinese_civil_years import numeral
  kind=s['age_kind']
  if kind=='exact':assert numeral(v['source_number'])==v['value']and v['reporting_status']=='direct_report'and not any(k in v for k in('bounds','approximation','source_age_idiom'))
  elif kind in('lower_bound','idiom_lower_bound'):
   assert v['value']is None and v['bounds']==dict(lower=s['lower'],lower_inclusive=False,upper=None,upper_inclusive=None)and v['reporting_status']=='direct_report'and 'approximation'not in v
   if kind=='lower_bound':assert numeral(v['source_number'])==s['lower']and'source_age_idiom'not in v
   else:
    i=v['source_age_idiom'];assert i['source_term']=='耳順'and i['numeric_equivalent']==60==s['lower']and i['reference']==dict(title='教育部《重編國語辭典修訂本》耳順',url='https://dict.revised.moe.edu.tw/dictView.jsp?ID=148459&la=0&powerMode=0',quote='六十而耳順',scope='modern_lexical_equivalence_not_source_age_counting')
  elif kind=='approaching':assert numeral(v['source_number'])==s['target']and v['value']is None and v['approximation']==dict(kind='approaching_age',target=s['target'])and v['reporting_status']=='approximate_report'and not any(k in v for k in('bounds','source_age_idiom'))
  else:return False
  life=RECIPES[b['frame']].get('life_slots',{}).get(s.get('life_slot'))
  if life and life['date_expression']:
   assert v['date_expression']==life['date_expression'];check_exact_date(v['normalized_date'],life['date_expression'],v['evidence'],ch,life['civil_era'])
  else:assert v['date_expression']is None and not any(k in v for k in('normalized_date','normalized_date_range'))
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

def address_valid(v,ch):
 try:
  p,m,s,b=typed_slot(v,ch,'source_address_binding','addresses');assert v['relation']==s['relation']and v['source_term']==s['source_term']and v['place']==dict(source_name=s['place'],place_id=None,modern_identification=None)and v['source_anchor']==expected_anchor(p,s['source_term'])and v['date_expression']is None and not any(k in v for k in('normalized_date','normalized_date_range'))
  if s['relation']=='service_location':assert v.get('qualifiers')==dict(source_position='鎮')
  elif s['relation']=='source_locality_designation':assert v.get('qualifiers')==dict(designation_kind='geographical_person_reference',origin_or_residence=None)
  else:assert 'qualifiers'not in v
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

def name_valid(n,ch):
 try:
  b=n['component_source_binding'];p,rs,fs,recipe=paragraph_frame(b,ch);s=recipe['names_slots'][b['slot']];m=rs[s['recipient_role']];mode=s['name_mode']
  assert n['person_id']==m['person_id']and n['person_mention_id']==m['id']and n['chapter_id']==ch['id']and n['paragraph_id']==p['id']and n['quote']==p['text']and n['status']=='editorial_provisional'and n['human_reviewed']is False and n['additional_names']==[]and'surname_basis'not in n
  if mode in('full_head','full_named_reference'):
   assert len(m['surface'])==2 and n['surname']==m['surface'][:1]and n['ming']==m['surface'][1:]
   if mode=='full_head':assert m['start']==0 and p['text'][m['end']:].startswith('，字')
  elif mode=='given':assert n['surname']is None and n['ming']==m['surface']
  elif mode=='shi':assert m['surface'].endswith('氏')and n['surname']==m['surface'][:-1]and n['ming']is None
  else:return False
  if 'style_role'in s:
   z=rs[s['style_role']];assert z['person_id']==m['person_id']and p['text'][m['end']:z['start']]in('字','，字')and n['zi']==z['surface']
  else:assert 'zi'not in n
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False


def detail_valid(d,ch,holdings,root=None):
 try:
  p,m,s,b=typed_slot(d,ch,'source_career_role','details');v=d['values']
  assert d['kind']==s['kind']and d['source_term']==s['source_term']and d['source_anchor']==expected_anchor(p,s['source_term'])and v==s['values']
  assert d['source_revision']==ch['source']['revision_id']and d['paragraph_sha256']==b['paragraph_sha256']and d['date_expression']is None and not any(k in d for k in('normalized_date','normalized_date_range'))
  linked=[]
  if v.get('linked_holding_id'):linked.append(v['linked_holding_id'])
  linked+=v.get('linked_holding_ids',[])
  for hid in linked:
   h=holdings[hid];assert h['person_id']==m['person_id']and holding_valid(h,ch)
  if d['kind']=='death_in_office':
   assert root is not None
   es=[e for f in (Path(root)/'corpus').glob('*/*-life-events.json')for e in json.loads(f.read_text()).get('events',[])if e['id']==v['linked_life_event_id']]
   e,=es;assert e['person_id']==m['person_id']and life_valid(e,ch)and e['source_term']=='卒'and e['source_anchor']['start']==d['source_anchor']['start']and e['source_anchor']['paragraph_id']==p['id']
  try:from scripts.chinese_civil_years import numeral
  except ImportError:from chinese_civil_years import numeral
  if d['kind']=='reported_son_count':assert numeral(v['source_number'])==v['value']==v['enumerated_named_sons']
  if 'reported_troops'in v:assert v['source_number'].endswith('百')and numeral(v['source_number'][:-1])*100==v['reported_troops']
  if 'lower_exclusive_years'in v:assert numeral(v['source_number'])==v['lower_exclusive_years']
  if v.get('unit')=='旬':assert numeral(v['source_number'])==v['value']
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False


def inherited_holding_valid(h,ch):
 try:
  b=h['source_career_role'];p,rs,fs,r=paragraph_frame(b,ch);s=r['inherited_rank_slots'][b['slot']];m=rs[s['recipient_role']];father=rs[s['father_role']];ev,=h['evidence'];a,=h['attestations'];t=p['text'];term=s['source_term'];start=t.index(term)+1
  assert t.count(term)==1 and father['start']==start and t[father['start']:father['end']+1]==s['raw_title']
  assert ev==dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],quote=t,person_mention_id=m['id'])
  assert h['person_id']==m['person_id']!=father['person_id']and h['kind']=='noble_rank'and h['mode']=='accession'and h['appointment_role']=='inherited_rank'and h['status']=='source_attested'and h['human_reviewed']is False and nominal(h['title'],'noble_rank','inherited_rank')
  assert a==dict(id=h['id']+':a001',paragraph_id=p['id'],start=start,end=start+len(s['raw_title']),surface=s['raw_title'],person_mention_id=m['id'],usage='narrative',date_expression=None)
  assert h['effective_period']==dict(start=dict(status='source_event',event_type='accession',date_expression=None,evidence=h['evidence']),end=dict(status='unknown',date_expression=None,evidence=[]))
  i=h['inheritance'];assert i['predecessor_person_id']==father['person_id']and i['resolved_title']==h['title']and i['source_term']==term and i['evidence']==h['evidence']and i['status']=='contextual_provisional'and i['human_reviewed']is False and i.get('predecessor_relation','father')=='father'
  x=h['inherited_title_binding'];assert set(x)=={'kind','father_assertion_id','predecessor_holding_id','raw_surface'}and x['kind']=='explicit_father_rank_in_complete_biography'and x['raw_surface']==s['raw_title']and x['predecessor_holding_id']==i['predecessor_holding_id']
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False

def inherited_surface_valid(h,a,ch,holdings,relations,paragraphs,chapters):
 try:
  assert inherited_holding_valid(h,ch)and a==h['attestations'][0];x=h['inherited_title_binding'];f,=[v for v in relations if v['id']==x['father_assertion_id']];parent=holdings[x['predecessor_holding_id']]
  assert f['predicate']=='father'and f['subject_person_id']==h['person_id']and f['object_person_id']==parent['person_id']==h['inheritance']['predecessor_person_id']and kinship_valid(f,paragraphs,chapters)
  assert parent['kind']=='noble_rank'and parent['title']==h['title']and parent['mode']!='accession'and holding_valid(parent,chapters[parent['evidence'][0]['chapter_id']])and any(e['paragraph_id']==a['paragraph_id']for e in f['evidence'])
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError):return False


def pinned_attestation_source_valid(h,ch,root):
 """Trusted complete role recipe plus exact original Kanripo position map.
 Only an explicitly pinned, undated noble source-use may be a heading choice.
 """
 try:
  assert root is not None
  p,m,a,slot,b=analyse(h,ch);r=RECIPES[b['frame']];pin=r['source_pin']
  assert set(pin)=={'kind','revision_id','raw_path','raw_sha256','paragraph_id','text_layer','source_layer','first_line','last_line','raw_position_map_sha256'}
  assert pin['kind']=='kanripo_received_position_map'and h['kind']=='noble_rank'and h['mode']=='attestation'and h['appointment_role']=='source_attested_use'
  unknown=dict(status='unknown',date_expression=None,evidence=[]);assert h['effective_period']==dict(start=unknown,end=unknown)and slot['date_expression']is None
  assert pin['revision_id']==ch['source']['revision_id']==ch['source']['source_commit']and pin['raw_path']==ch['source']['raw_path']and pin['raw_sha256']==ch['source']['raw_file_sha256']
  assert pin['paragraph_id']==p['id']and pin['text_layer']==p['text_layer']=='received_chapter'and pin['source_layer']==p['source_position']['source_layer']=='received_biography'
  assert p['source_position']['revision_id']==pin['revision_id']and p['source_position']['first_line']==pin['first_line']and p['source_position']['last_line']==pin['last_line']
  root=Path(root).resolve();rel=Path(pin['raw_path']);assert not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]in('sources','source-evidence')
  current=root
  for part in rel.parts:
   current=current/part;assert not current.is_symlink()
  assert current.resolve()==current and current.is_file();raw=current.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin['raw_sha256'];lines=raw.decode('utf8').splitlines(keepends=True)
  coords=p['source_position']['raw_character_positions'];assert len(coords)==len(p['text'])and hashlib.sha256(json.dumps(coords,sort_keys=True,separators=(',',':')).encode()).hexdigest()==pin['raw_position_map_sha256']
  assert all(isinstance(x,dict)and set(x)=={'line','column'}and type(x['line'])is int and type(x['column'])is int and pin['first_line']<=x['line']<=pin['last_line']and x['column']>=0 for x in coords)
  pairs=[(x['line'],x['column'])for x in coords];assert pairs==sorted(set(pairs))and pairs[0][0]==pin['first_line']and pairs[-1][0]==pin['last_line']
  assert ''.join(lines[x['line']-1][x['column']]for x in coords)==p['text']
  return True
 except(KeyError,ValueError,TypeError,AssertionError,StopIteration,IndexError,AttributeError,OSError,UnicodeError):return False
