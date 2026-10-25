# coding:utf-8
"""Trusted complete-witness role recipes; source text is data, never executable.
Recipes contain reviewed semantic records, not an NLU recognizer. IDs are resolved
from current source-person anchors, so a coherent rekey does not alter semantics.
"""
from pathlib import Path
import json,re,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
KIND='fixed_witness_person_fact_slots'
REF='fixed_witness_fact_slots_ref'
RECIPES=Path(__file__).with_name('fixed_witness_fact_slots.json')
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
 return a==b

def recipes():
 data=json.loads(RECIPES.read_text());assert data['format_version']=='0.1'and isinstance(data['recipes'],dict)
 return data['recipes']

def grammar(ch,root):
 assert root is not None
 root=Path(root).resolve();binding=ch['annotation'][REF];assert set(binding)=={'kind','key'}and binding['kind']==KIND
 r=recipes()[binding['key']];assert r['key']==binding['key']and r['source_kind']=='fixed_wikisource_complete_biography'
 assert not any(key in layer for layer in(ch,ch['source'],binding,r)for key in('annotator','attached_note_to_paragraph_id'))
 assert all(layer.get('text_layer','received_chapter')=='received_chapter'and layer.get('source_layer','received_biography')=='received_biography'for layer in(ch,ch['source'],binding,r))
 try:from scripts.fixed_wikisource_units import source_errors
 except ImportError:from fixed_wikisource_units import source_errors
 assert ch['annotation'].get('fixed_wikisource_unit_ref')and not source_errors(ch,root)
 assert ch['source']['revision_id']==r['source_revision']and ch['source']['raw_file_sha256']==r['raw_sha256']
 path=Path(ch['source']['raw_file']);assert not path.is_absolute()and'..'not in path.parts and path.parts[0]in('sources','source-evidence');raw=root/path;assert raw.resolve()==raw and raw.is_file()and hashlib.sha256(raw.read_bytes()).hexdigest()==r['raw_sha256']
 assert len(ch['paragraphs'])==len(r['paragraphs']);roles=[];allcoords=[]
 for j,(p,pattern)in enumerate(zip(ch['paragraphs'],r['paragraphs'])):
  layers=r.get('paragraph_layers')
  if layers is not None:
   assert isinstance(layers,list)and len(layers)==len(ch['paragraphs'])and set(layers)<={'received_biography','received_quoted_document','received_criticism'}
   assert layers[0]=='received_biography'and ch['source']['text_scope']=='partial_chapter'
  expected_layer=layers[j]if layers is not None else'received_biography'
  assert p['text_layer']=='received_chapter'and p['source_position']['source_layer']==expected_layer
  assert not any(k in container for container in(p,p['source_position'])for k in('annotator','attached_note_to_paragraph_id'))
  ms=[m for m in p['mentions']if m['kind']=='person'];cursor=0;used=[]
  for part in re.split(r'(<r[0-9]+>)',pattern):
   if re.fullmatch(r'<r[0-9]+>',part):
    i=int(part[2:-1]);m=ms[i];assert type(m['start'])is int and type(m['end'])is int and m['start']==cursor and p['text'][m['start']:m['end']]==m['surface'];cursor=m['end'];used.append(i)
   else:assert p['text'].startswith(part,cursor);cursor+=len(part)
  assert cursor==len(p['text'])and used==list(range(len(ms)));roles.append(ms);allcoords.extend((j,i)for i in range(len(ms)))
 groups=r['same_person_groups'];seen=[];pids=[]
 for group in groups:
  assert group and all(isinstance(x,list)and len(x)==2 and all(type(n)is int for n in x)for x in group)
  ids={roles[j][i]['person_id']for j,i in group};assert len(ids)==1;pids.extend(ids);seen.extend(tuple(x)for x in group)
 assert len(pids)==len(set(pids))and sorted(seen)==sorted(allcoords)
 return r,roles

def expand(v,roles):
 if isinstance(v,dict):
  if set(v)in ({'$person'},{'$mention'}):
   k=next(iter(v));coord=v[k];assert isinstance(coord,list)and len(coord)==2 and all(type(i)is int and i>=0 for i in coord);p,m=coord;return roles[p][m]['person_id'if k=='$person'else'id']
  return{k:expand(x,roles)for k,x in v.items()}
 if isinstance(v,list):return[expand(x,roles)for x in v]
 return v

def _calendar_rows(r,root):
 rows={}
 for ref in r.get('calendar_references',[]):
  path=Path(ref['raw_file']);assert not path.is_absolute()and path.parts[0]=='sources'and'..'not in path.parts
  q=Path(root).resolve()/path;assert q.resolve()==q and q.is_file();raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==ref['sha256'];text=raw.decode('utf8')
  for row in ref['rows']:
   match=re.search(r"<tr id=['\"]"+re.escape(row['row_id'])+r"['\"]>.*?</tr>",text,re.S);assert match
   value=match[0];assert row['dynasty']in value and row['era_name']in value
   nums=re.findall(r"<div style=['\"]width:8em;['\"]>([0-9]+)</div>",value);assert nums==[str(row['first_year']),str(row['last_year'])]
   assert row['row_id']not in rows;rows[row['row_id']]=row
 return rows

def _dates(r,ch,slots,root):
 rows=_calendar_rows(r,root);proofs=r.get('date_proofs',[]);allowed={}
 for proof in proofs:
  if proof.get('kind') == 'fixed_archived_parallel_year':
   try:from scripts.fixed_witness_parallel_dates import prove,value_at
   except ImportError:from fixed_witness_parallel_dates import prove,value_at
   slot=proof['slot'];path=proof['record_path'];v=slots[slot];date=value_at(v,path)
   assert prove(date,v,proof,r,ch,root)
   allowed.setdefault(slot,[]).append(tuple(path));continue
  if proof.get('kind')=='fixed_calendar_era_phase_range':
   try:from scripts.date_ranges import year_range_errors
   except ImportError:from date_ranges import year_range_errors
   slot=proof['slot'];path=proof['record_path'];v=slots[slot];date=v
   for key in path:date=date[key]
   p=ch['paragraphs'][proof['paragraph_index']];a=proof['date_anchor'];assert type(a['start'])is int and type(a['end'])is int and p['text'][a['start']:a['end']]==a['surface']
   row=rows[proof['calendar_row_id']];mapping=date['era_span_mapping'];source_name=mapping.get('source_era_name',mapping['era_name']);phase=proof['source_phase']
   assert phase in ('初','中','末') and a['surface']==source_name+phase==date['source_expression']
   assert not year_range_errors(date,v['evidence'],a['surface'],root)
   assert mapping['era_name']==row['era_name'] and mapping['polity_source_name']==row['dynasty'] and mapping['start_ce_year']==row['first_year'] and mapping['end_ce_year']==row['last_year']
   assert date['original_quote']==p['text'] and date['source_stage']==phase
   allowed.setdefault(slot,[]).append(tuple(path));continue
  slot=proof['slot'];path=proof['record_path'];v=slots[slot];date=v
  for key in path:date=date[key]
  p=ch['paragraphs'][proof['paragraph_index']];a=proof['date_anchor'];assert type(a['start'])is int and type(a['end'])is int and p['text'][a['start']:a['end']]==a['surface']
  row=rows[proof['calendar_row_id']];mapping=date['regnal_year_mapping'];number=proof['source_number']
  try:from scripts.chinese_civil_years import numeral
  except ImportError:from chinese_civil_years import numeral
  n=numeral(number);assert type(n)is int and 1<=n<=row['last_year']-row['first_year']+1
  assert a['surface']==row['era_name']+number+'年'==date['source_expression']and mapping==dict(kind='ce_regnal_era_span',reference_index=0,start_ce_year=row['first_year'],end_ce_year=row['last_year'],regnal_year=n,source_number=number,era_name=row['era_name'])
  assert date['year']==date['era_year']==row['first_year']+n-1 and date['era']=='CE'and date['calendar']=='chinese_civil'and date['precision']=='year'
  assert date['evidence']==v['evidence']and date['original_quote']==p['text']and all(e['paragraph_id']==p['id']and e['quote']==p['text']for e in date['evidence'])
  columns=date['references'][0]['columns'];assert columns==dict(dynasty=row['dynasty'],era_name=row['era_name'],first_year=str(row['first_year']),last_year=str(row['last_year']))
  allowed.setdefault(slot,[]).append(tuple(path))
 def walk(x,path=()):
  out=[]
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ('normalized_date','normalized_date_range'):out.append(path+(k,))
    else:out.extend(walk(v,path+(k,)))
  elif isinstance(x,list):
   for i,v in enumerate(x):out.extend(walk(v,path+(i,)))
  return out
 for slot,v in slots.items():assert sorted(walk(v))==sorted(allowed.get(slot,[]))

def _maternal_context(r,slots,root):
 """Only reviewed recipe proofs qualify maternal preference; never parse a mother word."""
 proofs=r.get('maternal_context_proofs',[]);assert len({p['slot']for p in proofs})==len(proofs)
 required={k for k,v in slots.items()if 'supporting_source_references'in v.get('qualifiers',{}).get('maternal_interpretation',{})}
 assert required=={p['slot']for p in proofs}
 for proof in proofs:
  keys={'slot','kind','witnesses','record_roles','same_identity_groups','distinct_identity_groups'}
  assert set(proof)in(keys,keys|{'principal_mother_contrast'})and proof['kind']=='fixed_complete_witness_maternal_context'
  v=slots[proof['slot']];mi=v['qualifiers']['maternal_interpretation'];assert v['predicate']=='mother'and mi['status']=='contextual_preferred'and mi['source_explicit_birth']is False
  try:from scripts.fixed_wikisource_units import source_errors
  except ImportError:from fixed_wikisource_units import source_errors
  roles=[];refs=[];root=Path(root).resolve()
  for w in proof['witnesses']:
   assert set(w)=={'chapter_path','chapter_id','source_revision','raw_sha256','paragraph_id','paragraph_sha256','role_bindings'}
   path=Path(w['chapter_path']);assert not path.is_absolute()and'..'not in path.parts and path.parts[0]=='corpus';q=root/path;assert q.resolve()==q
   c=json.loads(q.read_bytes());assert c['id']==w['chapter_id']and c['source']['revision_id']==w['source_revision']and c['source']['raw_file_sha256']==w['raw_sha256']and c['annotation'].get('fixed_wikisource_unit_ref')and not source_errors(c,root)
   p,=[p for p in c['paragraphs']if p['id']==w['paragraph_id']];assert p['text_layer']=='received_chapter'and hashlib.sha256(p['text'].encode()).hexdigest()==w['paragraph_sha256']
   ms={m['id']:m for m in p['mentions']};rr={}
   for role,b in w['role_bindings'].items():
    assert set(b)=={'id','start','end','surface'};m=ms[b['id']];assert m['kind']=='person'and all(m[k]==b[k]for k in b)and p['text'][m['start']:m['end']]==m['surface'];rr[role]=m['person_id']
   roles.append(rr);refs.append(dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=c['id'],paragraph_id=p['id'],quote=p['text'],role_mentions={k:b['id']for k,b in w['role_bindings'].items()}))
  assert mi['supporting_source_references']==refs
  for field,coord in proof['record_roles'].items():assert field in('subject','object')and v[field+'_person_id']==roles[coord[0]][coord[1]]
  for group in proof['same_identity_groups']:assert len(group)>=2 and len({roles[j][k]for j,k in group})==1
  for group in proof['distinct_identity_groups']:assert len(group)>=2 and len({roles[j][k]for j,k in group})==len(group)
  if 'principal_mother_contrast'in proof:
   x=proof['principal_mother_contrast'];assert set(x)=={'principal_slot','witness_index','child_role','mother_roles','principal_roles','contrast_anchor'}
   i=x['witness_index'];assert type(i)is int and 0<=i<len(roles)
   rr=roles[i];wb=proof['witnesses'][i]['role_bindings'];quote=refs[i]['quote'];pr=slots[x['principal_slot']];pq=pr['qualifiers']
   assert mi['basis']=='same_complete_paragraph_mother_and_principal_mother_contrast'
   assert pr['predicate']=='maternal_role'and pq['role']=='principal_mother'and pq['biological_mother']is None and pq['father_person_id']is None
   assert rr[x['child_role']]==v['subject_person_id']==pr['subject_person_id']
   mm=x['mother_roles'];pm=x['principal_roles'];assert isinstance(mm,list)and isinstance(pm,list)and len(mm)>=2 and len(pm)>=2 and len(set(mm+pm))==len(mm+pm)
   assert {rr[k]for k in mm}=={v['object_person_id']} and {rr[k]for k in pm}=={pr['object_person_id']}and len({v['subject_person_id'],v['object_person_id'],pr['object_person_id']})==3
   assert wb[mm[0]]['surface'].endswith('母')and all(wb[k]['surface']==wb[mm[0]]['surface']for k in mm)
   assert wb[pm[0]]['surface'].startswith('嫡母')and wb[pm[0]]['surface'][2:].endswith('氏')and all(wb[k]['surface']==wb[pm[0]]['surface'][2:]for k in pm[1:])
   assert pq['source_term']==wb[pm[0]]['surface']and wb[mm[0]]['surface']in v['qualifiers']['source_term']
   a=x['contrast_anchor'];assert set(a)=={'start','end','surface'}and type(a['start'])is int and type(a['end'])is int and quote[a['start']:a['end']]==a['surface']
   assert a['start']<=wb[mm[0]]['start']<wb[mm[0]]['end']<=wb[pm[0]]['start']<wb[pm[0]]['end']<=a['end']


def records(ch,root=ROOT):
 r,roles=grammar(ch,root);slots=r['slots'];assert len({s['slot']for s in slots})==len(slots)
 out=[expand(s['record'],roles)for s in slots];assert len({x['id']for x in out})==len(out);by_slot={s['slot']:v for s,v in zip(slots,out)};hs={v['id']:v for s,v in zip(slots,out)if s['category']=='holding'}
 for s,v in zip(slots,out):
  b=v['fixed_source_fact_binding'];assert b==dict(kind=KIND,key=r['key'],slot=s['slot'])
  if 'birth_year'in v:assert v['birth_year']is None
  if not r.get('date_proofs'):assert 'normalized_date'not in v and'normalized_date_range'not in v
  for link in [v.get('values',{}).get('linked_holding_id'),v.get('values',{}).get('prior_holding_id'),v.get('title_formation',{}).get('previous_holding_id'),v.get('assumption_basis',{}).get('previous_holding_id')]:
   if link:assert link in hs and hs[link]['person_id']==v['person_id']
  for link in v.get('values',{}).get('related_holding_ids',[]):assert link in hs and hs[link]['person_id']==v['person_id']
  if 'source_anchor'in v:
   a=v['source_anchor'];p=next(p for p in ch['paragraphs']if p['id']==a['paragraph_id']);assert type(a['start'])is int and type(a['end'])is int and p['text'][a['start']:a['end']]==a['surface']==v['source_term']
 try:from scripts.biographical_appointment_sequence import integer
 except ImportError:from biographical_appointment_sequence import integer
 for proof in r['numeric_proofs']:
  p=ch['paragraphs'][proof['paragraph_index']];a,z=proof['start'],proof['end'];term=proof['source_number'];assert type(a)is int and type(z)is int and 0<=a<z<=len(p['text'])and p['text'][a:z]==term
  v=by_slot[proof['slot']]
  for key in proof['record_path']:v=v[key]
  assert type(v)is int and integer(term)==v
 _dates(r,ch,by_slot,root)
 _maternal_context(r,by_slot,root)
 for s,v in zip(slots,out):
  basis=v.get('surname_basis',{})
  if basis.get('kind')=='contextual_surname_from_fixed_witness_slots':
   seed=by_slot[basis['seed_name_slot']];a=by_slot[basis['source_assertion_slot']]
   assert v['surname']==seed['surname']and a['predicate']=='father'and a['subject_person_id']==seed['person_id']and a['object_person_id']==v['person_id']and a['status']=='source_attested'
 return out

def valid(v,ch,root=ROOT):
 try:
  b=v['fixed_source_fact_binding'];assert b['kind']==KIND
  expected,=[x for x in records(ch,root)if x['id']==v['id']]
  return strict(v,expected)
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):return False

def errors(root,rows):
 chs={c['id']:c for c in rows if c.get('record_type')=='marked_chapter'};got={};out=[]
 for row in rows:
  for field in('assertions','holdings','events','records'):
   for v in row.get(field,[]):
    if v.get('fixed_source_fact_binding',{}).get('kind')==KIND:got.setdefault(row.get('chapter_id',v.get('chapter_id')),[]).append(v)
 for cid,ch in chs.items():
  for field in('age_assertions','title_proposals'):
   for v in ch.get('annotation',{}).get(field,[]):
    if v.get('fixed_source_fact_binding',{}).get('kind')==KIND:got.setdefault(cid,[]).append(v)
 active={cid for cid,ch in chs.items()if ch.get('annotation',{}).get(REF,{}).get('kind')==KIND}
 for cid in set(got)-active:out.append('固定見證事實缺完整來源範圍:'+str(cid))
 for cid in active:
  try:
   expected=records(chs[cid],root);actual=got.get(cid,[]);assert len(actual)==len(expected)and len({v['id']for v in actual})==len(actual);by={v['id']:v for v in expected};assert all(strict(v,by.get(v.get('id')))for v in actual)
  except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):out.append('固定完整見證事實須逐原角色、原詞與全部來源槽，不能移人、漏項、重複或補日期:'+str(cid))
 return out
