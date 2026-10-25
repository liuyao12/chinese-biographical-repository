# -*- coding: utf-8 -*-
"""Complete adjacent biography with attached headings, YL and displayed wiki links.
Every raw code point is either visible or assigned one explicit markup/layout reason.
"""
from pathlib import Path
import hashlib,json,re
KIND='fixed_wikisource_biography_subsections_links'
def project(raw,title,opening_heading=None,following_heading=None):
 if opening_heading is None:
  assert isinstance(title,str)and title.endswith('傳')and len(title)>1
  heading='=='+title[:-1]+'=='
 else:
  assert isinstance(opening_heading,str)and re.fullmatch(r'===[^=\n]+===',opening_heading)
  heading=opening_heading
 assert raw.count(heading)==1
 start=raw.index(heading)
 if following_heading is None:
  following=re.search(r'^==[^=\n]+==\s*$',raw[start+len(heading):],re.M);assert following
 else:
  assert opening_heading is not None and re.fullmatch(r'(={2,3})[^=\n]+\1',following_heading)
  following=re.search(r'^(={2,3})[^=\n]+\1[ \t]*$',raw[start+len(heading):],re.M);assert following
  assert following.group(0).strip()==following_heading
 end=start+len(heading)+following.start();ps=[];classes=[]
 for m in re.finditer(r'[^\n]*\n|[^\n]+$',raw[start:end]):
  line=m[0].rstrip('\n');a=start+m.start();z=a+len(line);trim=line.strip()
  if not trim:classes.append(dict(start=a,end=start+m.end(),kind='layout_whitespace'));continue
  if re.fullmatch(r'(={2,3})[^=\n]+\1',trim):classes.append(dict(start=a,end=start+m.end(),kind='editorial_heading',text=line));continue
  assert not trim.startswith('=')
  out=[];ix=[];i=0
  while i<len(line):
   if line[i].isspace()and(i==0 or all(c.isspace()for c in line[:i])):classes.append(dict(start=a+i,end=a+i+1,kind='paragraph_indentation'));i+=1;continue
   if line.startswith('{{YL|',i):
    c=line.index('}}',i);v=line[i+5:c];assert v and not any(x in v for x in '{}[]<>|')
    classes.extend([dict(start=a+i,end=a+i+5,kind='year_template_markup'),dict(start=a+c,end=a+c+2,kind='year_template_markup')]);out.extend(v);ix.extend(range(a+i+5,a+c));i=c+2
   elif line.startswith('[[',i):
    c=line.index(']]',i);bar=line.index('|',i,c);target=line[i+2:bar];display=line[bar+1:c];assert target and display and not any(x in target+display for x in '{}[]<>|')
    classes.extend([dict(start=a+i,end=a+bar+1,kind='wiki_link_target_and_markup'),dict(start=a+c,end=a+c+2,kind='wiki_link_markup')]);out.extend(display);ix.extend(range(a+bar+1,a+c));i=c+2
   else:
    assert not any(line.startswith(x,i)for x in ('{{','}}','[[',']]','<','>'))
    out.append(line[i]);ix.append(a+i);i+=1
  if m[0].endswith('\n'):classes.append(dict(start=z,end=z+1,kind='layout_newline'))
  if out:ps.append(dict(text=''.join(out),raw_start=a,raw_end=z,raw_character_offsets=ix,first_line=raw.count('\n',0,a)+1,last_line=raw.count('\n',0,z)+1))
 assert ps
 visible=[i for p in ps for i in p['raw_character_offsets']];excluded=[i for c in classes for i in range(c['start'],c['end'])]
 assert len(set(visible))==len(visible)and len(set(excluded))==len(excluded)and not set(visible)&set(excluded)and set(visible)|set(excluded)==set(range(start,end))
 return start,end,ps,classes

def errors(ch,root,b):
 try:
  root=Path(root).resolve();s=ch['source']
  def local(rel):
   p=Path(rel);assert not p.is_absolute()and p.parts[0]in('sources','source-evidence')and '..'not in p.parts
   q=root/p;assert q.resolve()==q and q.is_file();return q
  assert b['record_type']==KIND and b['chapter_id']==ch['id']and type(b['source_revision'])is int and b['source_revision']==s['revision_id']
  rawb=local(b['raw_file']).read_bytes();raw=rawb.decode('utf8');assert b['raw_file']==s['raw_file']==s['raw_path']and hashlib.sha256(rawb).hexdigest()==b['raw_sha256']==s['wikitext_sha256']==s['raw_file_sha256']
  start,end,ps,excluded=project(raw,ch['title'])
  assert b['selection']==dict(start=start,end=end,opening_heading='=='+ch['title'][:-1]+'==',following_heading=raw[end:raw.index('\n',end)],raw=raw[start:end])and b['excluded']==excluded
  assert len(ps)==len(ch['paragraphs'])and len({p['id']for p in ch['paragraphs']})==len(ps)
  for p,w in zip(ch['paragraphs'],ps):
   assert p['text_layer']=='received_chapter'and p['text']==w['text']
   layer='received_commentary'if w['text'].startswith('史臣曰：')else'received_biography'
   assert p['source_position']==dict(**{k:v for k,v in w.items()if k!='text'},revision_id=b['source_revision'],projection_sha256=hashlib.sha256((json.dumps(w['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),source_layer=layer)
  return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['完整本傳及附傳節界、連結/模板可見字、原行位置或全raw排除分類不符']
