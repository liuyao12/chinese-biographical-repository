"""Explicit editorial analysis of a received territorial/posthumous/rank heading.
This validates typed source spans and current endpoints, not historical identity by NLU.
A dated grant applies to territorial rank only; the epithet remains undated.
"""
import hashlib
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return set(a)==set(b)and all(same(v,b[k])for k,v in a.items())
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b if type(a)in(str,int,float,bool,type(None))else False
def valid(holding,chapter,attestation=None):
 try:
  h=holding;b=h['received_title_analysis'];keys={'kind','paragraph_id','paragraph_sha256','person_mention_id','surface_anchor','territory_anchor','posthumous_anchor','rank_anchor','grant_anchor','normalized_title','grant_applies_to','posthumous_date','status','human_reviewed','reviewer','model','rationale'}
  assert isinstance(b,dict)and set(b)==keys
  assert b['kind']=='received_territorial_posthumous_rank_heading'and b['status']=='editorial_provisional'and b['human_reviewed']is False and isinstance(b['reviewer'],str)and bool(b['reviewer'])and b['model']is None and isinstance(b['rationale'],str)and bool(b['rationale'])
  assert h['kind']=='noble_rank'and h['mode']=='grant'and h['status']=='source_attested'
  assert b['grant_applies_to']=='territorial_rank_only'and b['posthumous_date']is None
  p=next(p for p in chapter['paragraphs']if p['id']==b['paragraph_id']);text=p['text'];assert hashlib.sha256(text.encode()).hexdigest()==b['paragraph_sha256']
  def anchor(k):
   x=b[k];assert isinstance(x,dict)and set(x)=={'start','end','surface'}and type(x['start'])is int and type(x['end'])is int and isinstance(x['surface'],str)and 0<=x['start']<x['end']<=len(text)and text[x['start']:x['end']]==x['surface'];return x
  s,t,e,r,g=[anchor(k)for k in('surface_anchor','territory_anchor','posthumous_anchor','rank_anchor','grant_anchor')]
  assert s['start']==t['start']and t['end']==e['start']and e['end']==r['start']and r['end']==s['end']and s['surface']==t['surface']+e['surface']+r['surface']
  assert r['surface']in('王','公','侯','伯','子','男')
  assert h['title']==b['normalized_title']==t['surface']+r['surface']
  m=next(m for m in p['mentions']if m['id']==b['person_mention_id']);assert m['kind']=='person'and m['person_id']==h['person_id']and m['start']==s['start']and m['end']>s['end']and m['surface'].startswith(s['surface'])
  start=h['effective_period']['start'];assert start['status']=='source_event'and start['event_type']=='grant'and isinstance(start['date_expression'],str)and start['date_expression']and g['surface']==start['date_expression']+'受封'and m['end']<=g['start']
  aa=h['attestations'];assert isinstance(aa,list)and len(aa)==1;a=aa[0]
  assert a['paragraph_id']==p['id']and a['person_mention_id']==m['id']and type(a['start'])is int and type(a['end'])is int and a['start']==s['start']and a['end']==s['end']and a['surface']==s['surface']and a['usage']=='retrospective'and a['date_expression']is None
  if attestation is not None:assert same(a,attestation)
  expected={'work_id':chapter['work_id'],'book_id':chapter['book_id'],'source_id':chapter['source_id'],'chapter_id':chapter['id'],'paragraph_id':p['id'],'quote':text,'person_mention_id':m['id']}
  assert same(h['evidence'],[expected])and same(start['evidence'],[expected])
  assert h['effective_period']['end']['status']=='unknown'and h['effective_period']['end']['date_expression']is None and same(h['effective_period']['end']['evidence'],[])
  return True
 except(AssertionError,KeyError,TypeError,ValueError,StopIteration):return False
