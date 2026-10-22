"""Validate source-attributed authorship syntax; no historical-name whitelist."""
import re

def source_author_errors(works, chapters):
 errors=[]
 for wid, work in works.items():
  for ev in work.get('source_author_attributions',[]):
   def require(ok,why):
    if not ok:raise ValueError(why)
   try:
    c=chapters.get(ev.get('chapter_id'));require(c is not None,'missing chapter')
    ps={p['id']:p for p in c['paragraphs']};p=ps.get(ev.get('paragraph_id'));require(p is not None,'missing paragraph')
    require(ev.get('work_id')==c['work_id'] and ev.get('book_id')==c['book_id'] and ev.get('source_id')==c['source_id'],'citation source work/book differs')
    require(ev.get('referenced_work_id')==wid and ev.get('quote')==p['text'],'referenced work/full quote differs')
    ms={m['id']:m for m in p['mentions']};a=ms.get(ev.get('author_mention_id'));w=ms.get(ev.get('work_mention_id'))
    require(a is not None and w is not None,'missing author/title anchor')
    require(a.get('kind')=='person' and a.get('person_id')==ev.get('author_person_id') and a['surface']==ev.get('author_surface'),'author anchor differs')
    require(w.get('kind')=='work' and w.get('work_id')==wid,'title anchor differs')
    text=p['text'];order=(w['end']<=a['start'] if ev.get('authorship_syntax',{}).get('kind')=='title_author_suo_zhu' else a['end']<=w['start']);require(text[a['start']:a['end']]==a['surface'] and text[w['start']:w['end']]==w['surface'] and order,'author/title span differs')
    syntax=ev.get('authorship_syntax',{});kind=syntax.get('kind');gap=text[a['end']:w['start']]
    people=[m for m in p['mentions'] if m.get('kind')=='person' and a['end']<=m['start'] and m['end']<=w['start']]
    if kind=='author_title_prefix':
     require(not people and gap in ('','著','所著','撰','所撰','作','所作','編','所編'),'not adjacent source author prefix')
     require(not syntax.get('object_person_mention_ids'),'unexpected prefix objects')
    elif kind=='compiled_named_work':
     require(not people and not syntax.get('object_person_mention_ids'),'other person in compilation clause')
     require(re.fullmatch(r'(?:嘗)?(?:抄撮|采輯|編纂|撰集|撰|著|作)[^曰云。；！？]{1,80}(?:名曰|號曰|題曰)',gap) is not None,'not explicit compilation/name clause')
    elif kind=='continued_subject_authored_work':
     ids=syntax.get('object_person_mention_ids',[]);require(ids==[m['id']for m in people],'unqualified person inside subject continuation')
     require(len(people)<=1,'multiple possible subjects')
     masked=gap
     for m in reversed(people):
      require(m['start']>a['end'] and text[m['start']-1]=='尚','object lacks marriage predicate')
      masked=masked[:m['start']-a['end']]+'@P@'+masked[m['end']-a['end']:]
     # Restrict source grammar to an explicit subject-led biographical predicate,
     # an optional marriage object, character description, then authorship.
     require(re.fullmatch(r'(?:長於|生於|居於)[^曰云。；！？@]{1,12}(?:又?尚@P@)?(?:少以[^曰云。；！？@]{1,12}知名)?(?:好[^曰云。；！？@]{1,12}言)?(?:作|著|撰)',masked) is not None,'not explicit continued-subject authorship clause')
    elif kind=='resumed_biographical_subject_named_works':
     head=ms.get(syntax.get('biographical_head_mention_id'));reporter=ms.get(syntax.get('reporting_work_mention_id'))
     require(head is not None and reporter is not None,'missing biography/reporting anchors')
     require(head.get('kind')=='person' and head.get('person_id')==a.get('person_id') and head['end']<a['start'],'head and resumed subject differ')
     require(reporter.get('kind')=='work' and reporter['start']==0 and head['start']==reporter['end']+1 and text[reporter['end']:head['start']]=='曰' and text[head['end']:head['end']+1]=='字','not reported biography opening')
     listed=[ms.get(i) for i in syntax.get('listed_work_mention_ids',[])]
     require(len(listed)>=2 and len(listed)<=4 and all(x and x.get('kind')=='work' for x in listed),'missing listed works')
     require(len({x['id'] for x in listed})==len(listed) and w['id'] in [x['id'] for x in listed],'duplicate/unbound listed title')
     require(all(x['end']==y['start'] for x,y in zip(listed,listed[1:])),'not contiguous named works')
     first=listed[0];g=text[a['end']:first['start']]
     require(a['end']<first['start'] and len(g)<=120 and re.fullmatch(r'[^曰云。；！？]{1,118}(?:作|著|撰)',g) is not None,'not resumed explicit authorship clause')
     require(not re.search(r'(?:不|未|無|欲|將|當|議|請|可|宜)(?:作|著|撰)$',g),'negative/intended authorship')
     require(not [m for m in p['mentions'] if m.get('kind')=='person' and a['end']<=m['start']<listed[-1]['end']],'intervening person')
     for x in [head,reporter]+listed:
      require(text[x['start']:x['end']]==x['surface'],'resumption/list anchor span differs')
     require(syntax.get('scope_quote')==text[a['start']:listed[-1]['end']] and not syntax.get('object_person_mention_ids'),'scope quote/objects differ')
    elif kind=='title_author_suo_zhu':
     require(w['start']==0 and w['end']==a['start'] and not syntax.get('object_person_mention_ids'),'not initial title/author adjacent clause')
     clause=syntax.get('authorship_clause',{});end=a['end']+2
     require(text[a['end']:end] in ('所著','所撰','所作') and clause=={'start':0,'end':end,'quote':text[:end]},'not explicit title-author-suo attribution')
     following=syntax.get('following_explanation',{});q=following.get('quote','')
     require(following=={'start':end,'end':end+len(q),'quote':text[end:end+len(q)]} and re.fullmatch(r'[^曰云。；！？非不未無乎耶]{1,8}者',q) is not None,'not anchored following explanatory definition')
    else:raise ValueError('unknown/missing source authorship syntax')
   except (KeyError,TypeError,ValueError) as exc:errors.append('source-author-prefix: '+str(ev.get('work_mention_id'))+': '+str(exc))
 return errors
