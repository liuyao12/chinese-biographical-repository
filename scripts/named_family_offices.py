"""Explicit listed-child grants and named siblings' office/duty frames.
Neither a list position nor a family ID establishes absolute birth order.
"""
import hashlib

def a(p,x):
 assert set(x)=={'paragraph_id','start','end','surface'}and x['paragraph_id']==p['id']and type(x['start'])is int and type(x['end'])is int and 0<=x['start']<x['end']<=len(p['text'])and p['text'][x['start']:x['end']]==x['surface'];return x

def parts(record,chapters,key):
 e,=record['evidence'];ch=chapters[e['chapter_id']];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);b=record[key];assert e['quote']==p['text']and e['source_id']==ch['source_id']and e['work_id']==ch['work_id']and e['book_id']==ch['book_id']and b['source_revision']==ch['source']['revision_id']and b['paragraph_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()and b['human_reviewed']is False and record['human_reviewed']is False
 ms={m['id']:m for m in p['mentions']if m['kind']=='person'};scope=a(p,b['scope_anchor']);roles={k:ms[v]for k,v in b['roles'].items()};fields={k:a(p,v)for k,v in b['fields'].items()}
 for m in roles.values():assert p['text'][m['start']:m['end']]==m['surface']and scope['start']<=m['start']<m['end']<=scope['end']
 return ch,p,b,scope,roles,fields

def valid(h,chapters):
 try:
  ch,p,b,s,r,f=parts(h,chapters,'source_family_office_frame');unknown={'status':'unknown','date_expression':None,'evidence':[]};assert h['status']=='source_attested'and h['kind']in('office','noble_rank')and h['mode']=='grant'and h['effective_period']=={'start':{'status':'source_event','event_type':'grant','date_expression':None,'evidence':h['evidence']},'end':unknown}
  aa,=h['attestations'];m=r[b['recipient_role']];title=f[b['title_field']];assert h['person_id']==m['person_id']and aa=={'id':h['id']+':a','paragraph_id':p['id'],'start':title['start'],'end':title['end'],'surface':title['surface'],'person_mention_id':m['id'],'usage':'narrative','date_expression':None}and h['title']==title['surface']and h['evidence'][0]['person_mention_id']==m['id']
  if b['kind']=='named_sons_collective_enfeoffment':
   assert set(r)=={'father','child1','child2','child3','child4','child5'}and set(f)=={'count','rank'}and f['count']['surface']=='五'and b['recipient_role']in{'child1','child2','child3','child4','child5'}and b['title_field']=='rank'and h['kind']=='noble_rank'and h['title']=='列侯'
   prior=b['preceding_named_death'];da=a(p,prior['source_anchor']);dm=next(x for x in p['mentions']if x['id']==prior['person_mention_id']);assert prior['event_type']=='death'and prior['relation']=='after'and dm['person_id']==r['father']['person_id']and da['surface']==dm['surface']+'薨'and da['start']==dm['start']and da['end']<s['start']
   children=[r['child'+str(i)]for i in range(1,6)];assert s['surface']=='其悉封'+r['father']['surface']+f['count']['surface']+'子'+''.join(x['surface']for x in children)+'皆為'+f['rank']['surface']and len({x['person_id']for x in children})==5 and r['father']['person_id']not in{x['person_id']for x in children}
   cursor=s['start']+3;assert r['father']['start']==cursor;cursor=r['father']['end'];assert f['count']['start']==cursor;cursor=f['count']['end']+1
   for child in children:assert child['start']==cursor;cursor=child['end']
   assert f['rank']['start']==cursor+2 and f['rank']['end']==s['end']
  elif b['kind']=='named_younger_brother_office_series':
   assert set(r)=={'elder','younger1','younger2','younger3'}and set(f)=={'office1','office2','office3','duty'}and b['recipient_role']in{'younger1','younger2','younger3'}and b['title_field']=='office'+b['recipient_role'][-1]and h['kind']=='office'
   assert sibling_frame(s,r,f)
  else:return False
  assert b['absolute_birth_order_inferred']is False and all(m['id']in{x['id']for x in r.values()}for m in p['mentions']if m['kind']=='person'and s['start']<=m['start']<s['end'])
  return True
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False

def sibling_frame(s,r,f):
 chain=[r['elder'],'弟',r['younger1'],'為',f['office1'],r['younger2'],f['office2'],r['younger3'],f['office3'],f['duty']];cursor=s['start']
 for v in chain:
  if isinstance(v,str):cursor+=len(v)
  else:
   if v['start']!=cursor:return False
   cursor=v['end']
 return cursor==s['end']and s['surface']==''.join(v if isinstance(v,str)else v['surface']for v in chain)and len({x['person_id']for x in r.values()})==4

def duty_valid(d,chapters,holdings):
 try:
  _,p,b,s,r,f=parts(d,chapters,'source_family_duty_frame');assert b['kind']=='named_younger_brother_office_series'and sibling_frame(s,r,f)and d['kind']=='official_duty'and d['status']=='source_attested'and d['date_expression']is None and d['person_id']==r['younger3']['person_id']and d['source_term']==f['duty']['surface']=='侍講'and d['source_anchor']==f['duty']and d['evidence'][0]['person_mention_id']==r['younger3']['id']
  v=d['values'];h=holdings[v['office_title_holding_id']];return v=={'duty_code':'lecture_attendance','source_term':'侍講','independent_substantive_office':False,'office_title_holding_id':h['id']}and h['person_id']==d['person_id']and h['title']==f['office3']['surface']and valid(h,chapters)
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False

def sibling_order_valid(assertion,paragraphs):
 try:
  q=assertion['qualifiers'];b=q['source_clause_binding'];e,=assertion['evidence'];_,p=paragraphs[e['paragraph_id']];ms={m['id']:m for m in p['mentions']};older=ms[b['older_mention_id']];younger=ms[b['younger_mention_id']];term=a(p,b['source_anchor']);assert b['kind']=='named_older_di_younger'and term['surface']==older['surface']+'弟'+younger['surface']and older['start']==term['start']and younger['end']==term['end']and older['end']+1==younger['start']and q['source_term']==term['surface']
  assert assertion['predicate']=='brother'and assertion['subject_person_id']==younger['person_id']and assertion['object_person_id']==older['person_id']and e['quote']==p['text']
  return q['relative_birth_order']=={'older_person_id':older['person_id'],'younger_person_id':younger['person_id'],'operator':'lt','older_ordinal':None,'younger_ordinal':None,'scope':'siblings'}
 except(KeyError,TypeError,ValueError,AssertionError,StopIteration):return False
