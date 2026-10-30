"""Exact locally captured web-rendered comparison, not original raw or an edition."""
from pathlib import Path
import json,hashlib
CID='c-jinshu-049-jikang-rendered-comparison'
SID='s-jinshu049-jikang-web-rendered-comparison'
CH='corpus/jinshu/049-jikang-rendered-comparison.json'
BASE='source-evidence/jin049-jikang-rendered-comparison/'
PINS={'web-rendered-extract.txt': '29c47ce1cafc7ab2c1318b007e5fd9a4f92bc4c6610cc85d604422533bdfa8eb', 'capture-projection.json': '6da5c78e7fe2e694d220154415ace98755dcae4bdfab8f0fc0099b2581ec02ca', 'acquisition-qualification.json': 'd3ef9eda66a485fd9e693cf2833b04fa32e43f65002971fa9ca3c693632dd60a', 'contract.json': '69c9f68dfcf87048f576f2d417649a346280ce13e4616fd7718eb1891a7827ba'}
def validate_base_source(ch,root):
 if not isinstance(ch,dict):raise ValueError('章不是物件')
 root=Path(root).resolve()
 def fixed(name):
  p=(root/(BASE+name)).resolve()
  if not p.is_relative_to(root/'source-evidence'):raise ValueError('捕獲來源路徑越界')
  b=p.read_bytes()
  if hashlib.sha256(b).hexdigest()!=PINS[name]:raise ValueError('捕獲證據SHA不符：'+name)
  return b
 c=json.loads(fixed('contract.json'));captured=fixed('web-rendered-extract.txt');projection=json.loads(fixed('capture-projection.json'));fixed('acquisition-qualification.json')
 if any(ch.get(k)!=v for k,v in c['chapter_dimensions'].items())or ch.get('source')!=c['source']or ch.get('annotation')!=c['required_annotation']:raise ValueError('比較擷取完整資格／來源維度不符')
 ps=ch.get('paragraphs')
 if not isinstance(ps,list)or ps!=c['paragraphs']or len(ps)!=17:raise ValueError('完整17段／pending／mentions空資格不符')
 lines=captured.decode().splitlines()
 if projection['capture_sha256']!=hashlib.sha256(captured).hexdigest():raise ValueError('擷取hash不符')
 if len(projection['units'])!=len(ps):raise ValueError('擷取投影截短')
 for p,u in zip(ps,projection['units']):
  pos=p['captured_source_position'];n=u['capture_file_line'];points=u['capture_character_offsets']
  if p['id']!=CID+':'+u['unit_key']or pos['unit_key']!=u['unit_key']or pos['capture_sha256']!=projection['capture_sha256']:raise ValueError('擷取單元綁定不符')
  if not(type(n)is int and 1<=n<=len(lines)and all(type(x)is int and 0<=x<len(lines[n-1])for x in points)and points==sorted(set(points))):raise ValueError('擷取座標無效')
  text=''.join(lines[n-1][i]for i in points)
  if text!=p['text']or text!=u['text']or hashlib.sha256(text.encode()).hexdigest()!=u['text_sha256']:raise ValueError('擷取文字不符')
 return True
def source_errors(ch,root,source_path=None):
 if not isinstance(ch,dict):return ['比較擷取章不是物件']
 a=ch.get('annotation');owned_path=source_path is not None and Path(source_path).resolve()==(Path(root)/CH).resolve()
 if not owned_path and ch.get('id')!=CID and ch.get('source_id')!=SID and not(isinstance(a,dict)and a.get('fixed_rendered_capture_contract')=='jin049_jikang_web_capture_v1'):return []
 try:validate_source(ch,root);return []
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError)as e:return ['晉049比較擷取：'+str(e)]
# Named NER successor to the exact same web-capture source contract.
PHASE_SHA='fc1359370b958954370b0cd7b6bff79982fa4736bbb91bca05a5cf9ef873abce'
def _phase(root):
 b=(Path(root)/(BASE+'ner-phase-contract.json')).read_bytes()
 if hashlib.sha256(b).hexdigest()!=PHASE_SHA:raise ValueError('NER phase pin不符')
 return json.loads(b)
def _expand(x,roles):
 if isinstance(x,str)and x.startswith('$'):return roles[x[1:]]
 if isinstance(x,list):return [_expand(a,roles)for a in x]
 if isinstance(x,dict):return{k:_expand(v,roles)for k,v in x.items()}
 return x
def _resolve_source_roles_prior(ch,root,phase):
 root=Path(root);people=json.loads((root/'registry/persons.json').read_bytes())['persons'];by={x['id']:x for x in people}
 roles={}
 for s in phase['existing_seeds']:
  d=json.loads((root/s['path']).read_bytes())
  if any(d.get(k)!=v for k,v in s['chapter_dimensions'].items())or d.get('source')!=s['source']:raise ValueError('seed完整metadata不符')
  p,=[p for p in d['paragraphs']if p['id']==s['paragraph_id']]
  if p['text']!=s['full_paragraph']or hashlib.sha256(p['text'].encode()).hexdigest()!=s['paragraph_sha256']:raise ValueError('seed完整段不符')
  m,=[m for m in p['mentions']if m['id']==s['mention_id']]
  if any(m.get(k)!=s[k]for k in ['start','end','surface','kind']):raise ValueError('seed MID角色不符')
  pid=m['person_id'];rec=by[pid]
  if not any(e.get('mention_id')==m['id']and e.get('chapter_id')==d['id']and e.get('paragraph_id')==p['id']for e in rec.get('evidence',[])):raise ValueError('seed反向證據缺失')
  roles[s['role_key']]=pid
 for r in phase['local_roles']:
  key=r['role_key'];t=next(m for p in phase['chapter_template']['paragraphs']for m in p['mentions']if m.get('role_key')==key)
  ms=[m for p in ch['paragraphs']for m in p['mentions']if m['id']==t['id']]
  m,=ms;pid=m['person_id'];rec=by[pid]
  if rec.get('label')!=r['label']:raise ValueError('局部角色label不符')
  roles[key]=pid
 return roles
def validate_ner(ch,root):
 import copy
 phase=_phase(root);base=json.loads((Path(root)/(BASE+'contract.json')).read_bytes());projection=copy.deepcopy(ch)
 projection['annotation']=base['required_annotation']
 for p in projection['paragraphs']:p['annotation_status']='pending';p['mentions']=[]
 validate_base_source(projection,root)
 roles=resolve_roles(ch,root,phase)
 if ch!=_expand(phase['chapter_template'],roles):raise ValueError('NER完整章／marker／scope不符')
 people=json.loads((Path(root)/'registry/persons.json').read_bytes())['persons'];by={p['id']:p for p in people}
 for p in ch['paragraphs']:
  for m in p['mentions']:
   if m['kind']!='person':continue
   r=by[m['person_id']]
   if not any(e.get('chapter_id')==CID and e.get('paragraph_id')==p['id']and e.get('mention_id')==m['id']for e in r.get('evidence',[])):raise ValueError('本源反向證據缺失')
   if not any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in r.get('aliases',[])):raise ValueError('本源alias端點缺失')
 for path,t in phase['sidecar_templates'].items():
  if json.loads((Path(root)/path).read_bytes())!=_expand(t,roles):raise ValueError('本源sidecar不符：'+path)
 return True
def validate_ner_phase_source(ch,root):
 a=ch.get('annotation')if isinstance(ch,dict)else None
 if isinstance(a,dict)and isinstance(a.get('additional_annotation_phase'),dict)and a['additional_annotation_phase'].get('kind')=='jin049_received_comparison_ner_v1':return validate_ner(ch,root)
 return validate_base_source(ch,root)
# Same source handler, named finite lifecycle/office/address cohort.
TYPED_SHA='0d57d11277f27e6285b05b520822dd80f79b89c474d2ad64fc654c744ca6b207'
def _typed(root):
 b=(Path(root)/(BASE+'typed-basics-contract.json')).read_bytes()
 if hashlib.sha256(b).hexdigest()!=TYPED_SHA:raise ValueError('typed cohort pin不符')
 return json.loads(b)
def validate_basics(ch,root):
 import copy
 t=_typed(root);phase=_phase(root)
 if hashlib.sha256((Path(root)/(BASE+'ner-phase-contract.json')).read_bytes()).hexdigest()!=t['base_ner_phase_sha256']:raise ValueError('typed前置NER不符')
 roles=resolve_roles(ch,root,phase);projection=copy.deepcopy(ch);projection['annotation']=_expand(t['previous_template']['annotation'],roles)
 validate_ner_phase_source(projection,root)
 if ch!=_expand(t['chapter_template'],roles):raise ValueError('typed完整來源／報齡／scope不符')
 for path,template in t['sidecar_templates'].items():
  if json.loads((Path(root)/path).read_bytes())!=_expand(template,roles):raise ValueError('typed原生sidecar不符：'+path)
 return True
def validate_source(ch,root):
 a=ch.get('annotation')if isinstance(ch,dict)else None
 if isinstance(a,dict)and isinstance(a.get('additional_typed_phase'),dict)and a['additional_typed_phase'].get('kind')=='jin049_received_basics_v1':return validate_basics(ch,root)
 return validate_ner_phase_source(ch,root)
# Current source-role judgments are not an immutable historical-recall exemption.
def current_role_judgments_valid(phase,roles,people):
 if not isinstance(phase,dict)or phase.get('role_judgments_schema')!=2 or not isinstance(roles,dict)or not isinstance(people,dict):raise ValueError('current role schema/type不符')
 judgments=phase.get('role_judgments')
 if not isinstance(judgments,dict)or not set(roles)<=set(judgments):raise ValueError('source role判讀缺漏')
 local={r['role_key']for r in phase['local_roles']}
 for key,j in judgments.items():
  if not isinstance(j,dict):raise ValueError('role judgment不是物件')
  chosen=roles.get(key)
  expected_kind=('current_source_local_role'if key in local else'current_seed_role')if chosen is not None else'unresolved_source_reference'
  if j.get('judgment_type')!=expected_kind or j.get('preferred_person_id')!=chosen:raise ValueError('current preferred未綁已驗source MID role')
  cs=j.get('registry_candidates')
  if not isinstance(cs,list):raise ValueError('current candidates不是列表')
  seen=set();selected=[]
  for item in cs:
   if not isinstance(item,dict):raise ValueError('candidate不是物件')
   pid=item.get('person_id')
   if not isinstance(pid,str)or pid not in people or pid in seen or item.get('label')!=people[pid].get('label'):raise ValueError('current candidate未為唯一現役registry記錄')
   seen.add(pid);is_chosen=pid==chosen
   kind='current_preferred_role'if is_chosen else'current_registry_search_recall'
   if item.get('candidate_type')!=kind:raise ValueError('candidate current/recall類型錯置')
   if is_chosen:
    if item.get('current_role_key')!=key:raise ValueError('candidate綁錯role')
    selected.append(pid)
   elif 'current_role_key'in item:raise ValueError('未選recall不可冒已驗role')
  if selected!=([chosen]if chosen is not None else[]):raise ValueError('current role候選缺首選／未決偷定')
 return True
def resolve_roles(ch,root,phase):
 roles=_resolve_source_roles_prior(ch,root,phase)
 people={p['id']:p for p in json.loads((Path(root)/'registry/persons.json').read_bytes())['persons']}
 current_role_judgments_valid(phase,roles,people)
 return roles
