import re,json,hashlib
from pathlib import Path

def project(raw,title):
 assert isinstance(title,str)and title.endswith('傳')and len(title)>1
 heading='=='+title[:-1]+'=='
 assert raw.count(heading)==1
 a=raw.index(heading);after=re.search(r'^==[^=\n]+==\s*$',raw[a+len(heading):],re.M);assert after
 following_start=a+len(heading)+after.start();following=raw[following_start:raw.index('\n',following_start)]
 start=a;end=following_start;out=[];heads=[]
 for m in re.finditer(r'[^\n]+',raw[start:end]):
  t=m[0];a=start+m.start();z=start+m.end()
  if t.startswith('='):heads.append(dict(raw_start=a,raw_end=z,raw_text=t));continue
  if t=='{{wikipedia|'+title[:-1]+'}}':continue
  lo=len(t)-len(t.lstrip());hi=len(t.rstrip());i=lo;pos=[]
  while i<hi:
   if t.startswith('-{',i):
    j=t.index('}-',i+2);value=t[i+2:j];assert value and not any(x in value for x in '{}|;:');pos.extend(range(a+i+2,a+j));i=j+2
   elif t.startswith('{{YL|',i):
    j=t.index('}}',i+5);value=t[i+5:j];assert value and not any(x in value for x in '{}|<>');pos.extend(range(a+i+5,a+j));i=j+2
   elif t.startswith('[[',i):
    j=t.index(']]',i+2);value=t[i+2:j];assert value and not any(x in value for x in '|{}<>');pos.extend(range(a+i+2,a+j));i=j+2
   elif t.startswith("'''",i):i+=3
   else:
    assert not any(t.startswith(x,i)for x in ['{{','}}','[[',']]','<ref','</ref','<{','}>','-{','}-']),t[i:i+30]
    pos.append(a+i);i+=1
  text=''.join(raw[x]for x in pos)
  out.append(dict(projection_unit_number=len(out)+1,text=text,text_layer='received_chapter',mentions=[],source_position=dict(raw_start=a,raw_end=z,raw_character_offsets=pos,first_line=raw.count('\n',0,a)+1,last_line=raw.count('\n',0,z)+1,projection_sha256=hashlib.sha256((json.dumps(pos,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),source_layer='received_biography')))
 return out,dict(start=start,end=end,opening_heading=heading,following_heading=following,raw=raw[start:end],headings=heads)

KIND='fixed_wikisource_family_subsections'
def errors(ch,root,b):
 try:
  root=Path(root).resolve();s=ch['source']
  def local(rel):
   p=Path(rel);assert not p.is_absolute()and p.parts[0]in('sources','source-evidence')and '..'not in p.parts
   q=root/p;assert q.resolve()==q and q.is_file();return q
  assert b['record_type']==KIND and b['chapter_id']==ch['id']and type(b['source_revision'])is int and b['source_revision']==s['revision_id']
  data=local(b['raw_file']).read_bytes();raw=data.decode('utf8');assert b['raw_file']==s['raw_file']==s['raw_path']and hashlib.sha256(data).hexdigest()==b['raw_sha256']==s['raw_file_sha256']==s['wikitext_sha256']
  expected,selection=project(raw,ch['title']);assert b['selection']==selection and len(expected)==len(ch['paragraphs'])and len({p['id']for p in ch['paragraphs']})==len(expected)
  for p,w in zip(ch['paragraphs'],expected):
   assert p['text']==w['text']and p['text_layer']=='received_chapter'
   loc=w['source_position'];loc['revision_id']=b['source_revision'];assert p['source_position']==loc
   assert not any(k in p for k in ('annotator','attached_note_to_paragraph_id'))
  assert ch['annotation']['preserved_source_headings']==selection['headings']
  return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['固定本傳附傳完整節界或原字投影不符；不得改字、漏附傳或將標題當正文']
