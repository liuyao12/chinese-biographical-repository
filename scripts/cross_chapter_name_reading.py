"""Validate explicit, listed-record-only multi-source display readings; no identity merge."""
def locator(n):return{k:n.get(k)for k in('id','person_id','chapter_id','paragraph_id','surname','ming','quote')}
KIND='cross_chapter_same_person_source_variant'
def reading_errors(r,names,chapters):
 try:
  assert isinstance(r,dict)and set(r)=={'id','person_id','field','preferred_value','source_values','records','status','human_reviewed','rationale','coverage','basis'}
  assert r['field']=='ming'and r['status']=='editorial_provisional'and r['human_reviewed']is False and r['coverage']=='listed_records_only'and isinstance(r['rationale'],str)and r['rationale'].strip()and isinstance(r['id'],str)and r['id']and isinstance(r['person_id'],str)and r['person_id']
  b=r['basis'];assert set(b)=={'kind','status','human_reviewed','rationale'}and b['kind']==KIND and b['status']=='contextual_provisional'and b['human_reviewed']is False and isinstance(b['rationale'],str)and b['rationale'].strip()
  values=r['source_values'];assert isinstance(values,list)and len(values)==2 and len(set(values))==2 and all(isinstance(v,str)and 1<=len(v)<=16 for v in values)and r['preferred_value']in values
  refs=r['records'];assert isinstance(refs,list)and len(refs)>=2
  seen=[];source_chapters=set()
  for ref in refs:
   assert isinstance(ref,dict)and set(ref)=={'record','anchor','source_id'}
   n=ref['record'];assert isinstance(n,dict)and set(n)=={'id','person_id','chapter_id','paragraph_id','surname','ming','quote'}
   hit=[x for x in names if isinstance(x,dict)and locator(x)==n];assert len(hit)==1 and n['person_id']==r['person_id']and n['ming']in values
   c=chapters[n['chapter_id']];ps=[p for p in c['paragraphs']if p['id']==n['paragraph_id']];assert len(ps)==1;p=ps[0]
   a=ref['anchor'];ms=[m for m in p['mentions']if m['id']==a.get('id')];assert len(ms)==1;m=ms[0]
   assert ref['source_id']==c['source_id']and n['quote']==p['text']and m==a and m['kind']=='person'and m['person_id']==r['person_id']and p['text'][m['start']:m['end']]==m['surface']and n['ming']in m['surface']
   assert n not in seen;seen.append(n);source_chapters.add(c['id'])
  assert len(source_chapters)>=2 and {n['ming']for n in seen}==set(values)
  actual=[locator(n)for n in names if isinstance(n,dict)and n.get('person_id')==r['person_id']and n.get('ming')in values]
  assert len(actual)==len(seen)and all(n in seen for n in actual)
  return []
 except(KeyError,TypeError,ValueError,AssertionError,AttributeError):return ['跨篇姓名選讀須綁每個現役同人record唯一locator、完整段與真MID；不得補原字、漏列來源或代替同人決議']
