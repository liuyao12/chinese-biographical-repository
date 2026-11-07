"""Shared exact received-frame/marker view; no surname or kinship inference."""
import hashlib,json,re
from pathlib import Path
KIND='contextual_surname_from_observed_named_near_kin'

def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def read(root,rel):
 root=Path(root).resolve();p=Path(rel);assert not p.is_absolute()and'..'not in p.parts
 q=root/p;assert q.is_file()and not q.is_symlink()and q.resolve().is_relative_to(root)
 return q.read_bytes()

def at(value,pointer):
 for token in pointer.split('/')[1:]:
  token=token.replace('~1','/').replace('~0','~');value=value[int(token)]if type(value)is list else value[token]
 return value

def source_view(frames,chapters,assertions,root):
 rows=json.loads(read(root,'registry/persons.json'))['persons'];people={p['id']:p for p in rows};assert len(people)==len(rows)
 works={w['id']:w for w in json.loads(read(root,'registry/works.json'))['works']};bases=json.loads(read(root,'registry/work-provenance.json'))['text_bases'];ps={};cs={}
 for f in frames:
  assert set(f)=={'native_path','chapter_id','paragraph_id','paragraph_sha256','source_metadata','capture_path','capture_sha256','capture_text_pointer','capture_map_pointer','character_positions','capture_qualification'}
  assert Path(f['native_path']).parts[0]=='corpus'
  ch=json.loads(read(root,f['native_path']));assert ch['record_type']=='marked_chapter'and ch['id']==f['chapter_id']and same(ch,chapters[ch['id']])and same(ch['source'],f['source_metadata'])
  assert (Path(f['capture_path']).parts[0]=='source-evidence'
          or (Path(f['capture_path']).parts[0]=='sources'
              and f['capture_path']==ch['source'].get('raw_path')
              and f['capture_text_pointer']is None and f['capture_map_pointer']is None))
  work=works[ch['work_id']];book,=[b for b in work['books']if b['id']==ch['book_id']];assert ch['id']in book['chapter_ids']and bases[ch['source_id']]['work_id']==ch['work_id']and bases[ch['source_id']]['source_id']==ch['source_id']
  assert ch['source'].get('image_verified')is False
  p,=[p for p in ch['paragraphs']if p['id']==f['paragraph_id']];assert p['id']not in ps and hashlib.sha256(p['text'].encode()).hexdigest()==f['paragraph_sha256']
  raw=read(root,f['capture_path']);assert hashlib.sha256(raw).hexdigest()==f['capture_sha256']
  if f['capture_text_pointer'] is None:
   assert Path(f['capture_path']).suffix in('.wikitext','.txt')and not any(ch['source'].get(k)is False for k in('fixed_body_obtained','original_wikitext_obtained','raw_capture_obtained'))
   received=raw.decode();positions=f['character_positions'];assert f['capture_map_pointer']is None
   raw_keys=[k for k in('raw_sha256','raw_file_sha256')if k in ch['source']]
   assert raw_keys and all(ch['source'][k]==f['capture_sha256']for k in raw_keys)
   if 'raw_sha256'not in ch['source']:assert ch['source']['raw_path']==f['capture_path']
   assert f['capture_qualification']=={'kind':'existing_fixed_raw','revision_id':ch['source']['revision_id'],'image_verified':False}
  else:
   doc=json.loads(raw);received=at(doc,f['capture_text_pointer']);positions=at(doc,f['capture_map_pointer'])if f['capture_map_pointer']is not None else f['character_positions'];assert same(positions,f['character_positions'])
   qual=f['capture_qualification'];assert qual['kind']=='existing_received_observation'
   for pointer,expected in qual['captured_leaves'].items():assert same(at(doc,pointer),expected)
   for edition in (ch['source'].get(k)for k in('edition','actual_print_edition','printed_base_edition')):assert edition is None or type(edition)is str and any(term in edition for term in('未知','未核'))or any(pointer.rsplit('/',1)[-1]in('actual_print_edition','actual_print_edition_id')and same(value,edition)for pointer,value in qual['captured_leaves'].items())
   assert qual['no_image_verification']is True and ch['source'].get('image_verified')is False
   for pointer,expected in qual['captured_leaves'].items():
    key=pointer.rsplit('/',1)[-1]
    if key in('reported_revision','reported_revision_id'):assert same(ch['source'].get('revision_id'),expected)
    if key=='url':assert ch['source']['url']==expected
    if key in('fixed_permalink_body_read','original_wikitext_obtained','raw_capture_obtained','raw_wikitext_obtained','fixed_body_obtained')and key in ch['source']:assert same(ch['source'][key],expected)
    if key in('raw_wikitext_obtained','original_wikitext_obtained','raw_capture_obtained')and expected is False:assert not any(ch['source'].get(k)is True for k in('original_wikitext_obtained','raw_capture_obtained','raw_wikitext_obtained'))
    if key=='fixed_body_obtained'and expected is False:assert ch['source'].get('fixed_body_obtained')is not True and ch['source'].get('fixed_permalink_body_read')is not True
    if key in('actual_print_edition','actual_print_edition_id')and expected is None:
     edition=ch['source'].get('actual_print_edition',ch['source'].get('edition'));assert edition is None or type(edition)is str and any(term in edition for term in('未知','未核'))
  assert type(received)is str and type(positions)is list and all(type(i)is int for i in positions)and len(positions)==len(p['text'])and positions==sorted(set(positions))
  assert all(0<=i<len(received)for i in positions)and ''.join(received[i]for i in positions)==p['text']
  ps[p['id']]=(ch,p);cs[ch['id']]=ch
 def marker(par,mid):
  ch,p=ps[par];m,=[m for m in p['mentions']if m['id']==mid];assert m['kind']=='person'and type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface']
  es=[(pid,e)for pid,r in people.items()for e in r.get('evidence',[])if e.get('mention_id')==mid];assert len(es)==1 and es[0][0]==m['person_id'];e=es[0][1];expected=dict(work_id=ch['work_id'],book_id=ch['book_id'],chapter_id=ch['id'],source_id=ch['source_id'],paragraph_id=p['id'],mention_id=mid,quote=m['surface']);assert same({k:e[k]for k in expected},expected)
  aliases=[(pid,a)for pid,r in people.items()for a in r.get('aliases',[])if mid in a.get('mention_ids',[])];assert len(aliases)==1 and aliases[0][0]==m['person_id']and aliases[0][1]['surface']==m['surface']and aliases[0][1]['mention_ids'].count(mid)==1
  return ch,p,m
 def anchor(a):
  assert set(a)=={'paragraph_id','start','end','surface'};_,p=ps[a['paragraph_id']];assert type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface'];return p
 def existing_assertion(path,aid,*,with_document=False):
  assert Path(path).parts[0]=='corpus';doc=json.loads(read(root,path));row,=[a for a in doc['assertions']if a['id']==aid];caller,=[a for a in assertions if a['id']==aid];assert same(row,caller);return (caller,doc)if with_document else caller

 return ps,cs,people,marker,anchor,existing_assertion
