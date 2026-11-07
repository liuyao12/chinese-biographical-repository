"""Literal received biography headings: presentation evidence, never a dated grant."""
from pathlib import Path
import json,hashlib

def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def valid(h,ch,people,root):
 try:
  root=Path(root).resolve();b=h['received_header_attestation']
  assert type(b)is dict and set(b)=={'kind','chapter_path','holding_path','paragraph_id','person_mention_id','paragraph_sha256','source_metadata','human_reviewed'}
  assert b['kind']=='received_biography_header'and b['human_reviewed']is False
  def read(rel):
   assert type(rel)is str
   p=(root/rel).resolve();assert p.is_relative_to(root)and len(Path(rel).parts)==3 and Path(rel).parts[0]=='corpus'and p.suffix=='.json'
   return json.loads(p.read_bytes())
  actual=read(b['chapter_path']);assert same(actual,ch)and actual['record_type']=='marked_chapter'
  doc=read(b['holding_path']);assert doc['record_type']=='title_holding_assertion_set'and doc['chapter_id']==ch['id']
  found=[x for x in doc['holdings']if x['id']==h['id']];assert len(found)==1 and same(found[0],h)
  works=json.loads((root/'registry/works.json').read_bytes())['works']
  w,=[w for w in works if w['id']==ch['work_id']];book,=[x for x in w['books']if x['id']==ch['book_id']]
  assert book['work_id']==w['id']and book['chapter_ids'].count(ch['id'])==1
  source=ch['source'];assert same(source,b['source_metadata'])and source.get('human_reviewed')is False and source.get('image_verified')is False
  assert source.get('provider')and source.get('url')and source.get('edition')and source.get('review_status')and source.get('text_scope')
  # This opt-in supports unverified digital text only; never upgrade an unknown print witness.
  # This explicit opt-in requires an affirmative unknown/uninspected qualification,
  # not merely two matching mutable descriptions or a null legacy print field.
  assert type(source.get('edition'))is str and '印本未知'in source['edition']and '書影未核'in source['edition']
  assert all(source.get(field)is None for field in('actual_print_edition','actual_print_edition_id','printed_base_edition','printed_base_edition_id','printed_edition','printed_edition_id','print_edition','print_edition_id'))
  assert source.get('image_checked',False)is False and source.get('fixed_body_obtained',False)is False and source.get('raw_capture_obtained',False)is False
  assert all(source.get(flag,False)is False for flag in('original_wikitext_obtained','raw_wikitext_obtained','fixed_permalink_body_read'))
  p,=[x for x in ch['paragraphs']if x['id']==b['paragraph_id']]
  assert hashlib.sha256(p['text'].encode()).hexdigest()==b['paragraph_sha256']
  m,=[x for x in p['mentions']if x['id']==b['person_mention_id']]
  assert m['kind']=='person'and type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface']
  assert m['start']==len(p['text'])-len(p['text'].lstrip())and m['person_id']==h['person_id']
  pid=m['person_id'];physical=json.loads((root/'registry/persons.json').read_bytes())['persons'];person,=[x for x in physical if x['id']==pid]
  reverse=[(x['id'],e)for x in physical for e in x.get('evidence',[])if e.get('mention_id')==m['id']]
  alias=[(x['id'],a)for x in physical for a in x.get('aliases',[])for mid in a.get('mention_ids',[])if mid==m['id']]
  assert len(reverse)==len(alias)==1 and reverse[0][0]==alias[0][0]==pid
  assert pid in people and same(person,people[pid])and any(e.get('mention_id')==m['id']and e.get('chapter_id')==ch['id']and e.get('paragraph_id')==p['id']and e.get('source_id')==ch['source_id']and e.get('work_id')==ch['work_id']and e.get('book_id')==ch['book_id']and e.get('quote')==m['surface']for e in person['evidence'])
  assert any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person['aliases'])
  assert h['kind']in('royal_rank','imperial_rank')and h['mode']=='attestation'and h['status']=='source_attested'and h['human_reviewed']is False
  assert 'received_title_analysis'not in h and 'source_career_role'not in h
  unknown={'status':'unknown','date_expression':None,'evidence':[]};assert same(h['effective_period'],{'start':unknown,'end':unknown})
  a,=h['attestations'];assert a['paragraph_id']==p['id']and a['person_mention_id']==m['id']and a['usage']in('retrospective','posthumous_usage')and a['date_expression']is None
  assert type(a['start'])is int and type(a['end'])is int and a['start']==m['start']and a['start']<a['end']<=m['end']and p['text'][a['start']:a['end']]==a['surface']==h['title']
  e,=h['evidence'];assert same(e,dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],person_mention_id=m['id'],quote=p['text']))
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,AttributeError,OSError):return False
