from pathlib import Path
import re,json,hashlib
KIND='fixed_wikisource_attached_biography_quotes'
def project(raw,title):
 assert isinstance(title,str)and title.endswith('傳')and len(title)>1
 heading='=='+title[:-1]+'=='
 assert raw.count(heading)==1
 a=raw.index(heading);nexthead=re.search(r'^==[^=\n]+==\s*$',raw[a+len(heading):],re.M);assert nexthead
 b=a+len(heading)+nexthead.start();ps=[];ex=[];section=title[:-1];quote=False
 for m in re.finditer(r'[^\n]*\n|[^\n]+$',raw[a:b]):
  line=m[0].rstrip('\n');st=a+m.start();trim=line.strip()
  if not trim:ex.append({'start':st,'end':a+m.end(),'kind':'layout_whitespace'});continue
  if re.fullmatch(r'(={2,4})[^=\n]+\1',trim):section=trim.strip('=');ex.append({'start':st,'end':a+m.end(),'kind':'editorial_heading'});continue
  if re.fullmatch(r'\{\{wikipedia\|[^{}]+\}\}',trim):ex.append({'start':st,'end':a+m.end(),'kind':'editorial_cross_project_link'});continue
  out=[];ix=[];i=0;qlayer=quote
  while i<len(line):
   if line[i].isspace()and not out:ex.append(dict(start=st+i,end=st+i+1,kind='paragraph_indentation'));i+=1
   elif line.startswith('{{quote|',i):ex.append(dict(start=st+i,end=st+i+8,kind='quote_template_markup'));i+=8;quote=True;qlayer=True
   elif line.startswith('}}',i)and quote:ex.append(dict(start=st+i,end=st+i+2,kind='quote_template_markup'));i+=2;quote=False
   elif line.startswith('{{YL|',i):
    z=line.index('}}',i);v=line[i+5:z];assert not any(c in v for c in '{}[]|');ex.extend([dict(start=st+i,end=st+i+5,kind='year_template_markup'),dict(start=st+z,end=st+z+2,kind='year_template_markup')]);out.extend(v);ix.extend(range(st+i+5,st+z));i=z+2
   elif line.startswith('[[',i):
    z=line.index(']]',i);inner=line[i+2:z];assert not any(c in inner for c in '{}[]');bar=inner.find('|');v=inner[bar+1:]if bar>=0 else inner;vs=i+2+bar+1 if bar>=0 else i+2
    ex.extend([dict(start=st+i,end=st+vs,kind='wiki_link_target_and_markup'),dict(start=st+z,end=st+z+2,kind='wiki_link_markup')]);out.extend(v);ix.extend(range(st+vs,st+z));i=z+2
   elif line.startswith('-{',i):
    z=line.index('}-',i);v=line[i+2:z];assert not any(c in v for c in '{}[]|');ex.extend([dict(start=st+i,end=st+i+2,kind='character_conversion_markup'),dict(start=st+z,end=st+z+2,kind='character_conversion_markup')]);out.extend(v);ix.extend(range(st+i+2,st+z));i=z+2
   else:
    assert not any(line.startswith(c,i)for c in ['{{','}}','[[',']]','<','>']);out.append(line[i]);ix.append(st+i);i+=1
  if m[0].endswith('\n'):ex.append(dict(start=st+len(line),end=a+m.end(),kind='layout_newline'))
  if out:ps.append(dict(text=''.join(out),section=section,quoted_block=qlayer,raw_start=st,raw_end=st+len(line),raw_character_offsets=ix,first_line=raw.count('\n',0,st)+1,last_line=raw.count('\n',0,st+len(line))+1))
 v=[i for p in ps for i in p['raw_character_offsets']];e=[i for x in ex for i in range(x['start'],x['end'])];assert len(set(v))==len(v)and len(set(e))==len(e)and not set(v)&set(e)and set(v)|set(e)==set(range(a,b));assert not quote
 return a,b,ps,ex

def errors(ch,root,b):
 try:
  root=Path(root).resolve();s=ch['source']
  def local(rel):
   p=Path(rel);assert not p.is_absolute()and p.parts[0]in('sources','source-evidence')and '..'not in p.parts
   q=root/p;assert q.resolve()==q and q.is_file();return q
  assert b['record_type']==KIND and b['chapter_id']==ch['id']and type(b['source_revision'])is int and b['source_revision']==s['revision_id']
  rb=local(b['raw_file']).read_bytes();raw=rb.decode();assert b['raw_file']==s['raw_file']==s['raw_path']and hashlib.sha256(rb).hexdigest()==b['raw_sha256']==s['wikitext_sha256']==s['raw_file_sha256']
  a,z,ps,excluded=project(raw,ch['title'])
  assert b['selection']==dict(start=a,end=z,opening_heading='=='+ch['title'][:-1]+'==',following_heading=raw[z:raw.index('\n',z)],raw=raw[a:z])and b['excluded']==excluded
  assert len(ps)==len(ch['paragraphs'])and len({p['id']for p in ch['paragraphs']})==len(ps)
  for p,w in zip(ch['paragraphs'],ps):
   assert p['text_layer']=='received_chapter'and p['text']==w['text']
   pos={k:w[k]for k in('raw_start','raw_end','raw_character_offsets','first_line','last_line')}
   pos.update(revision_id=b['source_revision'],projection_sha256=hashlib.sha256((json.dumps(w['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),source_layer='received_biography',editorial_subsection=w['section'],quotation_block_markup=w['quoted_block'])
   assert p['source_position']==pos
  return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['完整本傳/附敘之節界、引語模板/連結/字形標記可見字、原位或全raw分類不符']
