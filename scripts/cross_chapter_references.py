"""Validate explicit source-bound cross references and imported target ownership."""
import json,hashlib,re
from pathlib import Path
def errors(chapters,root):
 if not isinstance(chapters,dict):return ['互見章目索引必須為字典']
 if not any(isinstance(c,dict)and 'cross_chapter_references'in c for c in chapters.values()):return []
 try:
  directory=json.loads((Path(root)/'data/corpus/chapter-directory.json').read_text());books={}
  assert isinstance(directory,dict)and isinstance(directory.get('works'),list)
  for w in directory['works']:
   for b in w['books']:books.setdefault((w['work_id'],b['book_id']),[]).append(b)
 except (OSError,ValueError,TypeError,KeyError,AssertionError,AttributeError):return ['互見目標須有已登記卷目']
 out=[];seen=set()
 for cid,ch in chapters.items():
  if not isinstance(ch,dict):continue
  refs=ch.get('cross_chapter_references',[])
  if not isinstance(refs,list):out.append('互見記錄須為列表：'+str(cid));continue
  for ref in refs:
   try:
    assert isinstance(ref,dict)and ref['kind']=='explicit_cross_chapter_reference'and isinstance(ref['id'],str)and ref['id']and ref['id']not in seen;seen.add(ref['id'])
    s=ref['source'];t=ref['target'];assert isinstance(s,dict)and isinstance(t,dict)
    p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']]
    assert all(s[k]==ch[k]for k in('work_id','book_id','source_id'))and s['chapter_id']==ch['id']==cid and s['revision_id']==ch['source']['revision_id']and s['paragraph_text']==p['text']and s['paragraph_text_sha256']==hashlib.sha256(p['text'].encode()).hexdigest()
    assert type(s['start'])is int and type(s['end'])is int and 0<=s['start']<s['end']<=len(p['text'])and p['text'][s['start']:s['end']]==s['surface']
    assert re.fullmatch('w-[a-z0-9-]+',t['work_id'])and re.fullmatch('b-[a-z0-9-]+',t['book_id'])and len(books.get((t['work_id'],t['book_id']),[]))==1
    if t['text_status']=='imported':
     assert isinstance(t['chapter_id'],str)and re.fullmatch('c-[a-z0-9-]+',t['chapter_id'])and isinstance(t['paragraph_id'],str)and t['paragraph_id'].startswith(t['chapter_id']+':')and re.fullmatch('[a-zA-Z0-9:_-]+',t['paragraph_id'])
     target=chapters[t['chapter_id']];assert target['work_id']==t['work_id']and target['book_id']==t['book_id'];tp,=[p for p in target['paragraphs']if p['id']==t['paragraph_id']]
    else:assert t['text_status']=='not_imported'and t.get('chapter_id')is None and t.get('paragraph_id')is None
   except (AssertionError,KeyError,ValueError,TypeError,IndexError,AttributeError):out.append('互見須綁固定原段與原字位，已收目標須屬同作品卷篇及確有段落：'+str(ref.get('id')if isinstance(ref,dict)else cid))
 return out
