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
    text=p['text'];require(text[a['start']:a['end']]==a['surface'] and text[w['start']:w['end']]==w['surface'] and a['end']<=w['start'],'author/title span differs')
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
    else:raise ValueError('unknown/missing source authorship syntax')
   except (KeyError,TypeError,ValueError) as exc:errors.append('source-author-prefix: '+str(ev.get('work_mention_id'))+': '+str(exc))
 return errors
