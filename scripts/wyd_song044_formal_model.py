"""Private formal source-role compiler. Allocation proposals are not identity proofs."""
from pathlib import Path
import json,copy,hashlib,importlib.util
CID='c-songshu-044-wyd1739-xiehui'
CH='corpus/songshu/044-wyd1739.json'
try:
 from scripts.validation_context import memoized
except ImportError:
 from validation_context import memoized

def need(ok,message):
 if not ok:raise ValueError('宋044正式角色：'+message)
def load_known_model():
 p=Path(__file__).resolve().parent/'wyd_song044_role_seed.py';s=importlib.util.spec_from_file_location('song044_known_dependency',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
@memoized(0)
def resolve_existing(root,contract):return load_known_model().resolve(root,contract)
@memoized(0)
def local_current(root,contract):
 """Current native MID and reverse endpoint, never a draft ownership key or old PID."""
 root=Path(root);ch=json.loads((root/CH).read_bytes());people={p['id']:p for p in json.loads((root/'registry/persons.json').read_bytes())['persons']};out={}
 for key,row in contract['local_roles'].items():
  mids={e['mention_id']for e in row['source_evidence']};hits=[(p,m)for p in ch['paragraphs']for m in p['mentions']if m['id']in mids and m.get('kind')=='person']
  if not hits:continue
  need(len(hits)==len(mids),'部分來源個體已採，拒混合端點');ids={m['person_id']for _,m in hits};need(len(ids)==1,'同角色多號');pid=next(iter(ids));need(pid in people,'本源PID未登記')
  person=people[pid]
  for p,m in hits:
   expected=next(e for e in row['source_evidence']if e['mention_id']==m['id']);need(all(m[k]==expected[k]for k in ['start','end','surface'])and p['text']==expected['quote'],'本源角色字位/全文')
   need(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'本源alias方向')
   need(any(e.get('chapter_id')==CID and e.get('paragraph_id')==p['id']and e.get('mention_id')==m['id']for e in person['evidence']),'本源evidence方向')
  out[key]=pid
 return out

def compile_chapter(root,contract,proposals):
 root=Path(root);known=resolve_existing(root,contract);current=local_current(root,contract);people=json.loads((root/'registry/persons.json').read_bytes());used={p['id']for p in people['persons']}
 import sys
 sys.path.insert(0,str(root/'scripts'))
 from retired_person_ids import retired_person_ids,allocation_conflicts
 from person_ids import valid_person_id
 retired=retired_person_ids(root);roles=dict(known)
 for key in contract['local_roles']:
  if key in current:roles[key]=current[key];continue
  relative={'shixiu':('hui',1),'shiji':('xuan-brother',1),'xiedun':('chong',1),'shao':('chong',2),'shiyou':('chong',2),'huaifu':('shangxuanshi',1)}
  pid=proposals[key]
  if key in relative:
   parent,distance=relative[key];need(parent in roles,'近系角色須先解析父祖');ancestor=roles[parent]
   pid=ancestor+('_'if len(ancestor)==11 else'')+'*'*(distance-1)+pid[-1]
  need(valid_person_id(pid)and pid not in used and not allocation_conflicts(pid,retired),'新號碰現役/退休保留或格式錯誤');need(pid not in roles.values(),'新角色重號');roles[key]=pid;used.add(pid)
 base=json.loads((root/CH).read_bytes());result=copy.deepcopy(base);m=load_known_model()
 for p,s in zip(result['paragraphs'],contract['paragraphs']):
  need(p['id']==s['id'],'完整22段次');p['mentions']=m.materialize(s['mentions'],roles);p['annotation_status']=s['annotation_status']
 need(len(result['paragraphs'])==len(contract['paragraphs'])==22,'完整22段數');result['annotation']=copy.deepcopy(contract['required_annotation'])
 return result,roles,current

def compile_registry(root,chapter,roles,current,contract):
 root=Path(root);before=json.loads((root/'registry/persons.json').read_bytes());after=copy.deepcopy(before);people={p['id']:p for p in after['persons']}
 for key,row in contract['local_roles'].items():
  pid=roles[key]
  if pid in people:continue
  person={'id':pid,'label':row['literal_label'],'status':'active','historicity':'historical_tradition','aliases':[],'evidence':[],'identity_note':row['qualification']+' 來源內明確個體先登記；本號不斷言與其他來源必異人，不補姓/父母/出生年。','review':'source_local_candidate'}
  after['persons'].append(person);people[pid]=person
 return load_known_model().registry(after,chapter)
