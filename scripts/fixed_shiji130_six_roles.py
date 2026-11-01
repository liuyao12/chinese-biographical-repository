"""Finite received-source collective/chapter roles; current endpoints come from real MIDs."""
from pathlib import Path
import json,hashlib
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
CID='c-shiji-130-taishigong';CH='corpus/shiji/130.json';GROUP='corpus/shiji/130-reference-groups.json';REF='source-evidence/shiji130-six-source-roles/contract.json';SHA='a88df1d7ec3b9663cdeaf1c696b49b2f97c0b11c192d82beec7d91cac57ae493'
def need(ok,why):
 if not ok:raise ValueError('史記130六段來源角色：'+why)
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def file(root,rel):
 root=Path(root).resolve();p=root/rel;need(not Path(rel).is_absolute()and'..'not in Path(rel).parts and p.resolve()==p and p.is_relative_to(root),'路徑/symlink');return p
def read(root,rel):return json.loads(file(root,rel).read_bytes())
def expand(v,roles):
 if isinstance(v,str):return roles.get(v,v)
 if isinstance(v,list):return[expand(x,roles)for x in v]
 if isinstance(v,dict):return{k:expand(x,roles)for k,x in v.items()}
 return v
def reverse(actor,ch,p,m):
 e={k:ch[k]for k in ('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);rows=[v for v in actor.get('evidence',[])if v.get('mention_id')==m['id']]
 need(len(rows)==1 and all(rows[0].get(k)==e[k]for k in ('chapter_id','paragraph_id','mention_id','quote'))and all(rows[0][k]==v for k,v in e.items()if k in rows[0]),'實際四欄反查/現有來源維度')
 need(any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in actor.get('aliases',[])),'原個人alias/MID反查')
def anchor(ch,spec):
 ps=[p for p in ch['paragraphs']if p['id']==spec['paragraph_id']];need(len(ps)==1 and hashlib.sha256(ps[0]['text'].encode()).hexdigest()==spec['paragraph_sha256'],'固定完整段');p=ps[0];ms=[m for m in p['mentions']if m['id']==spec['marker']['id']];need(len(ms)==1,'MID缺/多');m=ms[0]
 need(same({k:v for k,v in m.items()if k!='person_id'},spec['marker'])and m['kind']=='person'and type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface'],'個人全錨/角色');return p,m
@memoized(0)
def accepted(root):
 raw=file(root,REF).read_bytes();need(hashlib.sha256(raw).hexdigest()==SHA,'契約SHA');c=json.loads(raw);need(hashlib.sha256(file(root,c['scope_reading_path']).read_bytes()).hexdigest()==c['scope_reading_proposal_sha256'],'已讀提案SHA');ch=read(root,CH);people={p['id']:p for p in read(root,'registry/persons.json')['persons']};roles={}
 for role,spec in c['role_seeds'].items():
  p,m=anchor(ch,spec);pid=m['person_id'];need(pid in people,'本篇角色缺現役個人');reverse(people[pid],ch,p,m);roles[role]=pid
 for spec in c['external_individual_refs']:
  ext=read(root,spec['path']);e=spec['native_dimensions'];need(all(ext.get(k)==e[k]for k in ('work_id','book_id','source_id'))and ext['id']==e['chapter_id']and same(ext['source'],spec['source_metadata']),'外篇來源維度/固定修訂資格');p,m=anchor(ext,spec);pid=m['person_id'];need(pid in people,'外篇角色缺現役個人');reverse(people[pid],ext,p,m);need(spec['role']not in roles or roles[spec['role']]==pid,'本篇/外篇同一已採角色一端偷換');roles[spec['role']]=pid
 expected=expand(c['effective_native_template'],roles);need(same(ch,expected),'全章投影、所有未碰錨/原文或有限修改不符')
 for rel,t in c['unchanged_sidecar_templates'].items():need(same(read(root,rel),expand(t,roles)),'既有identity/來源側車未授權更改 '+rel)
 groups=expand(c['group_template'],roles);need(same(read(root,GROUP),groups),'完整群體側車缺/多/篡改')
 mids={m['id']:m for p in ch['paragraphs']for m in p['mentions']};owned=set()
 for g in groups['groups']:
  need(g['reported_count']is None or(type(g['reported_count'])is int and g['reported_count']==2),'來源有明數詞才報count');need(len(g['members'])==len({m['person_id']for m in g['members']})==2,'每個完整合稱為二位不同成員')
  for mid in g['group_marker_ids']:
   m=mids[mid];need(m['kind']=='unresolved'and m['person_id']is None and m['source_person_group']==g,'群體不得成個人/代詞/alternative');owned.add(mid)
 for ref in ch['cross_chapter_references']:
  m=mids[ref['source']['mention_id']];need(m['kind']=='work'and m['work_id']=='w-shiji'and m['person_id']is None and same(m['chapter_reference'],ref),'篇題不得算個人或擴寫原錨');owned.add(m['id']);target=ref['target'];path='corpus/shiji/'+target['book_id'].removeprefix('b-shiji-')+'.json';tc=read(root,path);need(tc['id']==target['chapter_id']and tc['book_id']==target['book_id']and tc['work_id']==target['work_id']and any(p['id']==target['paragraph_id']for p in tc['paragraphs']),'實際目標章歸屬')
 for actor in people.values():
  need(not any(e.get('mention_id')in owned for e in actor.get('evidence',[]))and not any(owned.intersection(a.get('mention_ids',[]))for a in actor.get('aliases',[])),'群體/篇題不可加個人直接提及/alias')
 protected=mids[c['protected_mid']];need(protected['kind']=='unresolved'and protected['person_id']is None,'父子相續太史公不可歸一')
 return ch,groups,roles,c

def errors(ch,root):
 try:need(same(ch,accepted(root)[0]),'caller章不符');return []
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return ['史記130六段人物合稱/章目角色、原字錨、現役個人反查與既有帳本不符']
def active(root):return (Path(root)/CH).is_file()or(Path(root)/REF).exists()or(Path(root)/GROUP).exists()
def group_set_valid(doc,people,root):
 ch,expected,roles,c=accepted(root);need(same(doc,expected),'caller有限owner或側車不符')
 for spec in c['external_individual_refs']:
  pid=roles[spec['role']];need(pid in people,'caller缺個人');ext=read(root,spec['path']);p,m=anchor(ext,spec);need(m['person_id']==pid,'current端點');reverse(people[pid],ext,p,m)
 owned={mid for g in expected['groups']for mid in g['group_marker_ids']}|{r['source']['mention_id']for r in ch['cross_chapter_references']}
 for actor in people.values():need(not any(e.get('mention_id')in owned for e in actor.get('evidence',[]))and not any(owned.intersection(a.get('mention_ids',[]))for a in actor.get('aliases',[])),'caller把篇名/群稱造個人alias')
 return True

def guard_catalog(records,people,root):
 if not active(root):return
 ch,doc,roles,c=accepted(root);docs=[r for r in records if r.get('record_type')=='source_person_reference_group_set'and(r.get('owner')=='fixed_shiji130_six_roles'or r.get('chapter_id')==CID)];need(len(docs)==1,'caller缺/多/未知owner群體側車');group_set_valid(docs[0],people,root);need(sum(same(r,ch)for r in records)==1,'caller缺完整本章')
 for rel,template in c['unchanged_sidecar_templates'].items():
  expected=expand(template,roles)
  need(sum(same(r,expected)for r in records)==1,'caller缺既有來源/identity側車 '+rel)
