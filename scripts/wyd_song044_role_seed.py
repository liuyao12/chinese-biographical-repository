"""Source-MID role resolution; no immutable person-ID whitelist or new IDs."""
import json,hashlib,copy
from pathlib import Path
CID='c-songshu-044-wyd1739-xiehui'
REF='source-evidence/song044-wyd1739-xiehui/known-role-contract.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def need(ok,why):
 if not ok:raise ValueError('宋044既有角色：'+why)
def resolve(root,contract):
 root=Path(root).resolve();reg=json.loads((root/'registry/persons.json').read_bytes());people={p['id']:p for p in reg['persons']};roles={}
 for key,binding in contract['bindings'].items():
  values=[]
  for s in binding['seeds']:
   rel=Path(s['path']);need(not rel.is_absolute()and '..'not in rel.parts and rel.parts[0]=='corpus','種子路徑')
   c=json.loads((root/rel).read_bytes());need(all(c[k]==s[k]for k in ['work_id','book_id','source_id'])and c['id']==s['chapter_id']and c['source']['revision_id']==s['source_revision'],'種子來源維度')
   need(digest(json.dumps(c['source'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==s['source_metadata_sha256']and all(c['source'].get(k)==v for k,v in s['source_identity_fields'].items())and bool(c['source'].get('provider'))and bool(c['source'].get('url'))and type(c['source'].get('revision_id'))in (int,str)and bool(c['source']['revision_id']),'種子完整來源元資料')
   p,=[p for p in c['paragraphs']if p['id']==s['paragraph_id']];need(p['text']==s['paragraph_text']and digest(p['text'].encode())==s['paragraph_sha256'],'種子全文')
   expected=s['marker'];m,=[m for m in p['mentions']if m['id']==expected['id']];need(m.get('kind')=='person'and all(m[k]==expected[k]for k in ['start','end','surface'])and p['text'][m['start']:m['end']]==m['surface'],'種子MID/字位')
   pid=m['person_id'];need(pid in people,'種子未登記');person=people[pid]
   need(any(a['surface']==m['surface']and m['id']in a.get('mention_ids',[])for a in person['aliases']),'種子反向alias')
   need(any(e.get('chapter_id')==c['id']and e.get('paragraph_id')==p['id']and e.get('mention_id')==m['id']for e in person['evidence']),'種子反向evidence')
   values.append(pid)
  need(values and len(set(values))==1,'同角色平行種子不同號');roles[key]=values[0]
 return roles

def materialize(value,roles):
 if isinstance(value,dict):
  if set(value)=={'$role'}:return roles[value['$role']]
  return {k:materialize(v,roles)for k,v in value.items()}
 if isinstance(value,list):return [materialize(v,roles)for v in value]
 return value

def chapter(root,current,contract):
 roles=resolve(root,contract);result=copy.deepcopy(current)
 need(current.get('id')==CID,'未知篇')
 for p,s in zip(result['paragraphs'],contract['paragraphs']):
  need(p['id']==s['id'],'段次')
  p['mentions']=materialize(s['mentions'],roles);p['annotation_status']=s['annotation_status']
 result['annotation']=copy.deepcopy(contract['required_annotation'])
 return result,roles

def registry(reg,chapter):
 result=copy.deepcopy(reg);people={p['id']:p for p in result['persons']}
 for p in chapter['paragraphs']:
  for m in p['mentions']:
   if m['kind']!='person':continue
   person=people[m['person_id']];hits=[a for a in person['aliases']if a['surface']==m['surface']]
   need(len(hits)<=1,'alias重複')
   if not hits:person['aliases'].append({'surface':m['surface'],'mention_ids':[]});hits=[person['aliases'][-1]]
   if m['id']not in hits[0]['mention_ids']:hits[0]['mention_ids'].append(m['id'])
   e={'work_id':chapter['work_id'],'book_id':chapter['book_id'],'source_id':chapter['source_id'],'chapter_id':chapter['id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':m['surface']}
   existing=[x for x in person['evidence']if x.get('mention_id')==m['id']]
   need(not existing or existing==[e],'新來源evidence衝突')
   if not existing:person['evidence'].append(e)
 return result
