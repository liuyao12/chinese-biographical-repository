"""A complete single received biography: explicit boundaries, whitespace and YL only."""
from pathlib import Path
import hashlib,json,re
KIND='fixed_wikisource_plain_biography_year_templates'
def project(raw,title):
 assert isinstance(title,str)and title.endswith('傳')and len(title)>1
 heading='=='+title[:-1]+'=='
 assert raw.count(heading)==1
 start=raw.index(heading)
 following=re.search(r'^==[^=\n]+==\s*$',raw[start+len(heading):],re.M)
 assert following
 end=start+len(heading)+following.start()
 paragraphs=[];positions=[]
 for m in re.finditer(r'[^\n]+',raw[start:end]):
  line=m[0];a=start+m.start();z=start+m.end()
  if line==heading:continue
  lo=len(line)-len(line.lstrip());hi=len(line.rstrip());i=lo;out=[];ix=[]
  while i<hi:
   if line.startswith('{{YL|',i):
    close=line.index('}}',i)+2;value=line[i+5:close-2]
    assert value and not any(x in value for x in '{}<>|')
    for k in range(i+5,close-2):out.append(line[k]);ix.append(a+k)
    i=close
   else:
    assert not any(line.startswith(x,i)for x in ['{{','}}','[[',']]','<ref','</ref'])
    out.append(line[i]);ix.append(a+i);i+=1
  if out:paragraphs.append(dict(text=''.join(out),raw_start=a,raw_end=z,raw_character_offsets=ix,first_line=raw.count('\n',0,a)+1,last_line=raw.count('\n',0,z)+1));positions.extend(ix)
 assert paragraphs
 return start,end,paragraphs

def errors(ch,root,b):
 try:
  root=Path(root).resolve();s=ch['source']
  def local(rel):
   p=Path(rel);assert not p.is_absolute()and p.parts[0]in('sources','source-evidence')and '..'not in p.parts
   q=root/p;assert q.resolve()==q and q.is_file();return q
  assert b['record_type']==KIND and b['chapter_id']==ch['id']and type(b['source_revision'])is int and b['source_revision']==s['revision_id']
  rawb=local(b['raw_file']).read_bytes();raw=rawb.decode('utf8');assert b['raw_file']==s['raw_file']==s['raw_path']and hashlib.sha256(rawb).hexdigest()==b['raw_sha256']==s['wikitext_sha256']==s['raw_file_sha256']
  start,end,expected=project(raw,ch['title']);selection=b['selection']
  assert selection==dict(start=start,end=end,opening_heading='=='+ch['title'][:-1]+'==',following_heading=raw[end:raw.index('\n',end)],raw=raw[start:end])
  assert len(expected)==len(ch['paragraphs'])and len({p['id']for p in ch['paragraphs']})==len(expected)
  for p,want in zip(ch['paragraphs'],expected):
   assert p['text_layer']=='received_chapter'and p['text']==want['text']
   loc=p['source_position'];assert loc==dict(**{k:v for k,v in want.items()if k!='text'},revision_id=b['source_revision'],projection_sha256=hashlib.sha256((json.dumps(want['raw_character_offsets'],ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),source_layer='received_biography')
  return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return ['固定完整單傳、緊鄰節界或原行可見投影不符；不得改字重hash或共移位置掩缺文']
