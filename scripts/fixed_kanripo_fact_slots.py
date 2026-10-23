# coding: utf-8
"""Finite, complete fixed-witness role-bound person facts; trusted static data only."""
from pathlib import Path
import json,re,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
KIND='fixed_kanripo_person_fact_slots'
RECIPE_PATH=Path(__file__).with_name('fixed_kanripo_fact_slots.json')
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
 return a==b
def grammar(ch,root=ROOT):
 try:from scripts.fixed_kanripo_projection import errors
 except ImportError:from fixed_kanripo_projection import errors
 r=json.loads(RECIPE_PATH.read_text());assert ch['annotation']['fixed_kanripo_fact_slots_ref']==dict(kind=KIND,key=r['key'])
 assert ch['annotation'].get('fixed_kanripo_projection_ref')and not errors(ch,root)
 raw_path=Path(ch['source']['raw_path']);assert not raw_path.is_absolute()and raw_path.parts[0]=='source-evidence'and'..'not in raw_path.parts
 raw_file=Path(root).resolve()/raw_path;assert raw_file.resolve()==raw_file
 projection=json.loads((Path(root)/ch['annotation']['fixed_kanripo_projection_ref']).read_text());assert projection['raw_file']==str(raw_path)
 assert ch['source']['revision_id']==r['source_revision']and ch['source']['raw_file_sha256']==r['raw_sha256']and hashlib.sha256((Path(root)/ch['source']['raw_path']).read_bytes()).hexdigest()==r['raw_sha256']
 assert len(ch['paragraphs'])==len(r['paragraphs']);roles=[]
 for p,pattern in zip(ch['paragraphs'],r['paragraphs']):
  mm=[m for m in p['mentions']if m['kind']=='person'];pos=0;used=[]
  for part in re.split(r'(<r[0-9]+>)',pattern):
   if re.fullmatch(r'<r[0-9]+>',part):
    i=int(part[2:-1]);m=mm[i];assert m['start']==pos and p['text'][pos:m['end']]==m['surface'];pos=m['end'];used.append(i)
   else:assert p['text'].startswith(part,pos);pos+=len(part)
  assert pos==len(p['text'])and used==list(range(len(mm)));roles.append(mm)
 return r,roles
def expand(v,roles):
 if isinstance(v,dict):
  if set(v)in ({'$person'},{'$mention'}):
   key=next(iter(v));p,m=v[key];return roles[p][m]['person_id'if key=='$person'else'id']
  return {k:expand(x,roles)for k,x in v.items()}
 if isinstance(v,list):return [expand(x,roles)for x in v]
 return v
def records(ch,root=ROOT):
 r,roles=grammar(ch,root);out=[expand(s['record'],roles)for s in r['slots']];assert len({v['id']for v in out})==len(out)
 hs={v['id']:v for v in out if 'title'in v and'attestations'in v}
 for v in out:
  link=v.get('values',{}).get('linked_holding_id')
  if link:assert link in hs and hs[link]['person_id']==v['person_id']
 for v in out:
  d=v.get('effective_period',{}).get('start',{}).get('normalized_date',{})
  if d.get('regnal_year_mapping',{}).get('kind')=='fixed_kanripo_accession_ce_year':
   try:from scripts.fixed_kanripo_accession_dates import bound_valid
   except ImportError:from fixed_kanripo_accession_dates import bound_valid
   assert bound_valid(d,v,ch,root),'固定本紀即位紀年須綁同人官爵原句與年份，不借下年改元'
 return out
def valid(v,ch,root=ROOT):
 try:
  b=v['fixed_source_fact_binding'];assert b['kind']==KIND
  expected,=[a for a in records(ch,root)if a['id']==v['id']];return strict(v,expected)
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):return False
def errors(root,rows):
 chs={c['id']:c for c in rows if c.get('record_type')=='marked_chapter'};out=[];got={}
 for row in rows:
  for field in ('assertions','holdings','records','events'):
   for v in row.get(field,[]):
    if v.get('fixed_source_fact_binding',{}).get('kind')==KIND:got.setdefault(row.get('chapter_id'),[]).append(v)
 for cid,ch in chs.items():
  for field in ('age_assertions','title_proposals'):
   for v in ch.get('annotation',{}).get(field,[]):
    if v.get('fixed_source_fact_binding',{}).get('kind')==KIND:got.setdefault(cid,[]).append(v)
 active={cid for cid,ch in chs.items()if ch.get('annotation',{}).get('fixed_kanripo_fact_slots_ref',{}).get('kind')==KIND}
 for cid in set(got)-active:out.append('固定Kanripo人物事實缺完整來源範圍:'+str(cid))
 for cid in active:
  try:
   expected=records(chs[cid],root);actual=got.get(cid,[]);assert len(actual)==len(expected)and len({v['id']for v in actual})==len(actual)
   wd={v['id']:v for v in expected}
   assert all(strict(v,wd.get(v.get('id')))for v in actual)
  except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):out.append('固定Kanripo完整事實須逐原角色、原詞、層次及紀年；不得移人、漏項或重複')
 return out

def valid_from_paragraphs(v,paragraphs,root=ROOT):
 try:
  r=json.loads(RECIPE_PATH.read_text());ch=json.loads((Path(root)/r['chapter_path']).read_text())
  assert all(paragraphs[p['id']]==(ch['id'],p)for p in ch['paragraphs'])
  return valid(v,ch,root)
 except(AssertionError,KeyError,ValueError,TypeError,OSError):return False
