"""Complete fixed unknown-print WS2376966 Pei Qian unit, with bounded accepted roles.
The original received narrative and Pei notes are distinct; no historical dates inferred.
"""
import copy,hashlib,json
from pathlib import Path
CID='c-sanguozhi-023-peiqian-ws2376966'
SID='s-sanguozhi-023-peiqian-ws2376966'
REF='source-evidence/sgz023-peiqian-ws2376966/contract.json'
CONTRACT_SHA='536b61bd304c09cdf0fa5f333a8577fb6c14f71673a25da3716691140ccf68dd'
RAW_SHA='6aba2ec0a43e037d6c2bcbc3b546c517d2d92dbf736a95ed7c53c39ad0f97bb2'
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def digest(x):return hashlib.sha256(x).hexdigest()
def need(ok,message):
 if not ok:raise ValueError('固定裴潛完整單元：'+message)
def local(root,rel):
 p=Path(rel);need(not p.is_absolute()and'..'not in p.parts and p.parts[0]in('sources','source-evidence','corpus','registry'),'路徑')
 q=Path(root).resolve()/p;need(q.resolve()==q and q.is_file(),'實檔');return q
def load(root):
 b=local(root,REF).read_bytes();need(digest(b)==CONTRACT_SHA,'契約SHA');return json.loads(b)
def read(root,rel):return json.loads(local(root,rel).read_bytes())
def reverse(person,ch,p,m):
 return any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[]))and [e for e in person.get('evidence',[])if e.get('mention_id')==m['id']]==[{**{k:ch[k]for k in('work_id','book_id','source_id')},'chapter_id':ch['id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':m['surface']}]
def resolve_roles(root,c,people):
 roles={}
 for role,s in c['foreign_role_seeds'].items():
  ch=read(root,s['path']);need({k:ch[k]for k in s['dimensions']}==s['dimensions']and digest(encoded(ch['source']))==s['source_sha256'],'外篇來源維度')
  p=next(p for p in ch['paragraphs']if p['id']==s['paragraph_id']);need(digest(p['text'].encode())==s['paragraph_text_sha256'],'外篇完整原段')
  m=next(m for m in p['mentions']if m['id']==s['marker']['id']);need({k:v for k,v in m.items()if k!='person_id'}==s['marker'],'外篇錨形')
  pid=m['person_id'];need(pid in people and reverse(people[pid],ch,p,m),'外篇雙向');roles['$'+role]=pid
 need(len(roles.values())==len(set(roles.values())),'不同來源角色無判讀合併');return roles
def expand(x,roles):
 if isinstance(x,str):return roles.get(x,x)
 if isinstance(x,list):return[expand(v,roles)for v in x]
 if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
 return x
def project(raw):
 lines=raw.splitlines(keepends=True);assert lines[65].strip()=='==裴潛==' and lines[76].strip()=='==【評】=='
 out=[];dropped=[];offset=sum(map(len,lines[:66]))
 def plain(a,z,layer,line):
  points=[];i=a
  def flush():
   if points:
    out.append({'layer':layer,'line':line,'raw_positions':list(points),'text':''.join(raw[k]for k in points)});points.clear()
  while i<z:
   if raw.startswith('[[',i):
    end=raw.index(']]',i)+2;assert end<=z;value=raw[i+2:end-2];a0=i+2+(value.rindex('|')+1 if '|' in value else 0);assert '[['not in value and '{{'not in value
    dropped.append({'start':i,'end':end,'kind':'wikilink_wrapper','display_start':a0,'display_end':end-2});points.extend(range(a0,end-2));i=end
   elif raw.startswith('{{YL|',i):
    end=raw.index('}}',i)+2;assert end<=z;value=raw[i+5:end-2];first=value.split('|')[0];assert first and '{{'not in value
    dropped.append({'start':i,'end':end,'kind':'digital_year_link_wrapper','display_start':i+5,'display_end':i+5+len(first)});points.extend(range(i+5,i+5+len(first)));i=end
   elif raw.startswith('<br>',i):flush();dropped.append({'start':i,'end':i+4,'kind':'digital_paragraph_break'});i+=4
   else:
    assert not raw.startswith(('{{','}}','<ref','</ref','<br','[['),i)
    if raw[i]not in '\r\n':points.append(i)
    i+=1
  flush()
 for n in range(67,76):
  line=lines[n-1];a=offset;z=a+len(line);cursor=a
  while '{{*|' in raw[cursor:z]:
   k=raw.index('{{*|',cursor,z);plain(cursor,k,'received_chapter',n)
   i=k+4;depth=1
   while depth:
    if raw.startswith('{{',i):depth+=1;i+=2
    elif raw.startswith('}}',i):depth-=1;i+=2
    else:i+=1
    assert i<=z
   plain(k+4,i-2,'witness_appended_pei_songzhi_note',n);dropped.append({'start':k,'end':i,'kind':'pei_note_wrapper','content_start':k+4,'content_end':i-2});cursor=i
  plain(cursor,z,'received_chapter',n);offset=z
 return out,dropped

def _base_validate(ch,root,people_override=None,sidecars_override=None):
 c=load(root);people=people_override if people_override is not None else {p['id']:p for p in read(root,'registry/persons.json')['persons']};roles=resolve_roles(root,c,people)
 need(ch==expand(c['chapter_template'],roles),'來源／層次／MID／角色／未決資格')
 rawb=local(root,c['raw_file']).read_bytes();need(digest(rawb)==c['raw_sha256']==RAW_SHA,'固定原文SHA');units,wrappers=project(rawb.decode())
 projb=local(root,c['projection_path']).read_bytes();need(digest(projb)==c['projection_sha256'],'投影SHA');projection=json.loads(projb)
 need(projection['raw_sha256']==RAW_SHA and projection['digital_wrappers']==wrappers and len(units)==len(ch['paragraphs'])==len(projection['units']),'完整單元／包裝')
 seen=[]
 for i,(p,u,s)in enumerate(zip(ch['paragraphs'],units,projection['units']),1):
  need({k:s[k]for k in u}==u and p['text']==u['text']and p['text_layer']==u['layer'],'逐字／原層次')
  need(p['source_position']['first_line']==u['line']and p['source_position']['last_line']==u['line']and s['key']==f'p{i:03d}','原行位置')
  seen.extend(u['raw_positions'])
  for m in p['mentions']:
   need(p['text'][m['start']:m['end']]==m['surface'],'錨字位')
   if m['kind']=='person':need(m['person_id']in people and reverse(people[m['person_id']],ch,p,m),'本篇雙向')
 need(seen==sorted(set(seen)),'原字位置重複／錯序')
 need(ch['text_sha256']==digest('\n\n'.join(p['text']for p in ch['paragraphs']).encode()),'正文SHA')
 for path,t in c['sidecar_templates'].items():need((sidecars_override[path]if sidecars_override is not None and path in sidecars_override else read(root,path))==expand(t,roles),'近系來源斷言／方向／未知欄位')
 works=read(root,'registry/works.json')['works'];book=next(b for w in works if w['id']=='w-sanguozhi'for b in w['books']if b['id']=='b-sanguozhi-023');need(book['chapter_ids'].count(CID)==1,'卷篇登記')
 if ch['annotation'].get('two_hui_identity_adopted'):
  try:from scripts.two_hui_identity import validate as validate_hui
  except ImportError:from two_hui_identity import validate as validate_hui
  validate_hui(root,ch)
 return roles
def validate(ch,root):
 if (Path(root)/'source-evidence/sgz023-peiqian-ws2376966/four-biographies-ner-contract.json').exists():
  try:from scripts.fixed_sgz023_four_biographies import proof
  except ImportError:from fixed_sgz023_four_biographies import proof
  state=proof(root);need(ch==state['chapter'],'完整具名NER caller章')
  # Identity joining is checked on the true current caller and real current files.
  if ch['annotation'].get('two_hui_identity_adopted'):
   try:from scripts.two_hui_identity import validate as validate_hui
   except ImportError:from two_hui_identity import validate as validate_hui
   validate_hui(root,ch)
  return _base_validate(state['parent_chapter'],root,state['parent_people'],state['parent_sidecars'])
 return _base_validate(ch,root)
def errors(ch,root):
 if ch.get('id')!=CID and ch.get('source_id')!=SID and 'fixed_sgz023_peiqian_ref'not in ch.get('annotation',{}):return []
 try:validate(ch,root);return []
 except(AssertionError,ValueError,KeyError,TypeError,OSError,StopIteration,IndexError):return ['固定裴潛完整單元：原文、數位見證資格、層次、近系角色或雙向來源不符']
