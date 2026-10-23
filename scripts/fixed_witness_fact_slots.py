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
 try:from scripts.fixed_wikisource_units import source_errors
 except ImportError:from fixed_wikisource_units import source_errors
 assert ch['annotation'].get('fixed_wikisource_unit_ref')and not source_errors(ch,root)
 assert ch['source']['revision_id']==r['source_revision']and ch['source']['raw_file_sha256']==r['raw_sha256']
 path=Path(ch['source']['raw_file']);assert not path.is_absolute()and'..'not in path.parts and path.parts[0]in('sources','source-evidence');raw=root/path;assert raw.resolve()==raw and raw.is_file()and hashlib.sha256(raw.read_bytes()).hexdigest()==r['raw_sha256']
 assert len(ch['paragraphs'])==len(r['paragraphs']);roles=[];allcoords=[]
 for j,(p,pattern)in enumerate(zip(ch['paragraphs'],r['paragraphs'])):
  assert p['text_layer']=='received_chapter'and p['source_position']['source_layer']=='received_biography'
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

def records(ch,root=ROOT):
 r,roles=grammar(ch,root);slots=r['slots'];assert len({s['slot']for s in slots})==len(slots)
 out=[expand(s['record'],roles)for s in slots];assert len({x['id']for x in out})==len(out);by_slot={s['slot']:v for s,v in zip(slots,out)};hs={v['id']:v for s,v in zip(slots,out)if s['category']=='holding'}
 for s,v in zip(slots,out):
  b=v['fixed_source_fact_binding'];assert b==dict(kind=KIND,key=r['key'],slot=s['slot'])
  for key in('normalized_date','normalized_date_range','birth_year'):
   assert key not in v
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
