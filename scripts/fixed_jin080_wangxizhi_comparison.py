"""Fixed unknown-edition comparison source roles. Original text never supplies an edition claim."""
from pathlib import Path
import json,hashlib
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
try:from scripts.witness_projection import repository_positions
except ImportError:from witness_projection import repository_positions
CID='c-jinshu-080-wangxizhi-comparison';SID='s-jinshu080-ws2603570-comparison'
EP='source-evidence/jin080-wangxizhi-comparison/'
RULE='fixed_comparison_jin080_received_roles'
NAME_KIND='contextual_surname_from_fixed_jin080_received_family'
PINS={'ner-template.json': 'ba1814a10e9afc3e6ab40a242ef0a2733969b38cf17f8e46e8c74a87fbf2a4a9', 'ner-roles.json': 'cb64f19859b606f16335316db2a97b99ffeb32df3618240c046809a20de40fa3', 'ner-dispositions.json': '6653904897cf89bdc98cd267a804d47cedccc54059bdb9caf9f4770c61d13678', 'ner-facts-template.json': 'd352f3d1bce70b4d7012826b1d24fa13e39ff0c8e493d2bf125746abdf14ec17', 'ner-names-template.json': '8e4e86ff285bf619cc05af0528bdc0636788e8f6fab36bc0d75210f8211b4126', 'ner-identities-template.json': 'c985f32a82b7b29406871e0c735a73a8939e1b9489ad8d477e83785f8d9832d2', 'ner-external-reading.json': '12b7d96d9fd6c99922d037bf0aa3f1176c2286761fdd69d7604d3f82f4a7c2d8', 'ner-identity-background.json': '23f6754fe1de31a5f82a8419a6909eba8a17aea142f5a216bf568b713cfaa732', 'ner-stage-qualification.json': '84b318f038c38bce36c964e720f50b5f6400ad4a1eff2f0168e5ab3cedd7eebb', 'projection.json': 'c5063863832b96c0bc35f552eb3f5f35744873b40a8a93b5c2e7902ca707c873', 'raw.wikitext': '4f3f42dd7d8ab0ca3c45e6524e4977db40332e845080367088be0419a3a0e8a0', 'extraction-exclusions.json': '4bd220806c33a5441b872fa0f2ad5bbe802262fa3697e96457134d2dca20bb6e', 'contract.json': '52673cac21caade1b41bd68238fc7463ef14b5d2c0515f6969445e52b50b7fd1'}
def need(x,msg):
 if not x:raise ValueError('晉080比較本：'+msg)
def same(a,b):
 return json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':'))==json.dumps(b,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def rootpath(root,rel):
 root=Path(root).resolve();p=Path(rel);need(not p.is_absolute()and '..'not in p.parts and p.parts[0]in('corpus','registry','source-evidence'),'不安全路徑');q=root/p;need(q.resolve()==q and q.is_file(),'來源越界/缺檔');return q
def fixed(root,name):
 b=rootpath(root,EP+name).read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],'固定來源/角色配方SHA不符：'+name);return b

def expand(value,roles):
 if isinstance(value,dict):return {k:expand(v,roles)for k,v in value.items()}
 if isinstance(value,list):return [expand(v,roles)for v in value]
 if isinstance(value,str)and value.startswith('$'):return roles[value[1:]]
 return value

@memoized(0)
def resolve(root,ch):
 root=Path(root).resolve();spec=json.loads(fixed(root,'ner-roles.json'));registry=json.loads(rootpath(root,'registry/persons.json').read_bytes())['persons'];people={x['id']:x for x in registry};need(len(people)==len(registry),'人物登記重複')
 own={m['id']:(p,m)for p in ch['paragraphs']for m in p['mentions']};need(len(own)==sum(len(p['mentions'])for p in ch['paragraphs']),'提及重複')
 roles={};reverse={}
 for person in registry:
  for alias in person.get('aliases',[]):
   for mid in alias.get('mention_ids',[]):reverse.setdefault((mid,alias.get('surface')),set()).add(person['id'])
 for role,s in spec['existing_seeds'].items():
  c=json.loads(rootpath(root,s['native_path']).read_bytes());ps=[p for p in c['paragraphs']if p['id']==s['paragraph_id']];need(len(ps)==1,'外源段不唯一');p=ps[0]
  need(all(c[k]==s[k]for k in('work_id','book_id','source_id'))and c['id']==s['chapter_id']and same(c['source'].get('revision_id'),s['source_revision']),'外源見證維度不符')
  need(p['text']==s['complete_paragraph']and hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_sha256'],'外源完整段不符')
  ms=[m for m in p['mentions']if m['id']==s['mention_id']];need(len(ms)==1,'外源MID不唯一');m=ms[0]
  need(m.get('kind')=='person'and same({k:m[k]for k in('start','end','surface')},{k:s[k]for k in('start','end','surface')})and p['text'][m['start']:m['end']]==m['surface'],'外源字位角色不符');roles[role]=m['person_id']
  person=people.get(m['person_id'],{});need(any(e.get('mention_id')==m['id']and e.get('chapter_id')==c['id']and e.get('paragraph_id')==p['id']for e in person.get('evidence',[]))and any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[])),'外源角色缺反向證據')
 for role,mid in spec['new_role_first_mids'].items():
  need(mid in own,'新角色缺首MID');p,m=own[mid];need(m.get('kind')=='person'and p['text'][m['start']:m['end']]==m['surface'],'新角色字位不符');roles[role]=m['person_id']
 for role,other in spec['role_aliases'].items():roles[role]=roles[other]
 need(roles['kuang']!=roles['kuang405'],'父墓前誓已亡父不得接後世桓振部下同名者')
 for mid,role in spec['role_by_mid'].items():
  need(mid in own,'漏固定MID');p,m=own[mid];need(m.get('person_id')==roles[role]and m.get('kind')=='person','單端改號或角色轉移')
  r=people.get(roles[role],{});need(any(e.get('mention_id')==mid and e.get('chapter_id')==CID and e.get('paragraph_id')==p['id']and e.get('source_id')==SID and e.get('quote')==m['surface']for e in r.get('evidence',[])),'缺本源反向evidence')
  owners=reverse.get((mid,m['surface']),set());need(owners=={roles[role]},'反向alias不唯一/錯端')
 return roles

def validate_source(ch,root):
 need(isinstance(ch,dict),'章不是物件');root=Path(root).resolve();t=json.loads(fixed(root,'ner-template.json'));roles=resolve(root,ch);expected=expand(t,roles)
 need(same({k:ch.get(k)for k in expected['chapter_dimensions']},expected['chapter_dimensions'])and same(ch.get('source'),expected['source'])and same(ch.get('annotation'),expected['annotation']),'章來源/比較資格不符')
 need(same(ch.get('paragraphs'),expected['paragraphs'])and len(ch['paragraphs'])==47,'完整47段/字位/角色不符')
 raw=fixed(root,'raw.wikitext');fixed(root,'extraction-exclusions.json');fixed(root,'projection.json');fixed(root,'ner-dispositions.json');fixed(root,'ner-external-reading.json');fixed(root,'ner-identity-background.json');fixed(root,'ner-stage-qualification.json');fixed(root,'contract.json')
 for p in ch['paragraphs']:
  _,sha=repository_positions(root,p,raw.decode().splitlines());need(sha==hashlib.sha256(raw).hexdigest(),'投影見證不符')
 for name,rel in [('ner-facts-template.json','corpus/jinshu/080-wangxizhi-comparison-assertions.json'),('ner-names-template.json','corpus/jinshu/080-wangxizhi-comparison-names.json'),('ner-identities-template.json','corpus/jinshu/080-wangxizhi-comparison-identities.json')]:
  actual=json.loads(rootpath(root,rel).read_bytes());need(same(actual,expand(json.loads(fixed(root,name)),roles)),'親屬/姓名全部有限槽與角色不符')
 return roles

def source_errors(ch,root):
 if not isinstance(ch,dict):return ['晉080比較本章不是物件']
 a=ch.get('annotation')
 if ch.get('id')!=CID and ch.get('source_id')!=SID and not(isinstance(a,dict)and a.get('fixed_comparison_contract')=='jin080_wangxizhi_ws2603570'):return []
 try:validate_source(ch,root);return []
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError)as e:return ['晉080比較本：'+str(e)]

def family_valid(a,paragraphs=None,root=None):
 try:
  root=Path(root).resolve()if root is not None else Path(__file__).resolve().parents[1]
  if not isinstance(a,dict):return False
  b=a.get('qualifiers',{}).get('source_clause_binding',{})
  if b.get('kind')!='biography_family_clause'or b.get('rule')!=RULE:return False
  ch=json.loads(rootpath(root,'corpus/jinshu/080-wangxizhi-comparison.json').read_bytes());roles=validate_source(ch,root);rows=expand(json.loads(fixed(root,'ner-facts-template.json')),roles)['assertions'];matches=[x for x in rows if x['id']==a.get('id')]
  if not same(matches,[a]):return False
  if paragraphs is not None:
   own={p['id']:p for p in ch['paragraphs']}
   for e in a['evidence']:
    actual=paragraphs[e['paragraph_id']];p=actual[1] if isinstance(actual,tuple)else actual
    if not same(p,own[e['paragraph_id']]):return False
  return True
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root=None):
 root=Path(root).resolve()if root is not None else Path(__file__).resolve().parents[1]
 try:
  need(isinstance(n,dict)and n.get('surname_basis',{}).get('kind')==NAME_KIND,'復姓類型不符');ch=chapters[CID];roles=validate_source(ch,root);rows=expand(json.loads(fixed(root,'ner-names-template.json')),roles)['records'];matches=[x for x in rows if x['id']==n['id']];need(same(matches,[n]),'復姓來源/完整角色槽不符')
  seed=n['surname_basis']['source_name_record_id'];need(same([x for x in names if isinstance(x,dict)and x.get('id')==seed],[x for x in rows if x['id']==seed]),'全名seed缺/錯');aa={x['id']:x for x in assertions}
  expected=expand(json.loads(fixed(root,'ner-facts-template.json')),roles)['assertions']
  for aid in n['surname_basis']['source_assertion_ids']:
   e=[x for x in expected if x['id']==aid];need(len(e)==1 and same(aa.get(aid),e[0])and family_valid(e[0],root=root),'復姓親屬proof缺/錯')
  se,=[x for x in rows if x['id']==seed];need(se.get('surname')==n['surname']and se.get('ming')and not se.get('surname_basis'),'seed須原全名不得循環推姓');current=se['person_id']
  for step in n['surname_basis']['steps']:
   a=aa[step['assertion_id']];need(step['from_person_id']==current,'復姓步驟不連續');dest=step['to_person_id'];direction=step['traversal']
   if direction=='father_to_child':need(a['predicate']=='father'and(a['object_person_id'],a['subject_person_id'])==(current,dest),'父子復姓方向不符')
   elif direction=='child_to_father':need(a['predicate']=='father'and(a['subject_person_id'],a['object_person_id'])==(current,dest),'子父復姓方向不符')
   elif direction=='paternal_uncle_to_nephew':need(a['predicate']=='paternal_uncle'and(a['object_person_id'],a['subject_person_id'])==(current,dest)and a['qualifiers'].get('parent_person_id')is None,'叔侄復姓不得補父')
   else:raise ValueError('不支援無源復姓路徑')
   current=dest
  need(current==n['person_id'],'復姓路徑未達本人')
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError)as e:raise ValueError('晉080復姓須有原全名、完整源角色及有限親屬proof，不得依ID/label：'+str(e))

def clan_valid(n,p,relations):
 try:
  root=Path(__file__).resolve().parents[1];ch=json.loads(rootpath(root,'corpus/jinshu/080-wangxizhi-comparison.json').read_bytes());roles=validate_source(ch,root);rows=expand(json.loads(fixed(root,'ner-names-template.json')),roles)['records'];matches=[x for x in rows if x['id']==n.get('id')]
  if not same(matches,[n])or n.get('ming')is not None or n.get('surname')not in('王','郗')or not isinstance(n.get('clan_style'),dict):return False
  expected=next(x for x in ch['paragraphs']if x['id']==n['paragraph_id'])
  if not same(p,expected):return False
  aid=n['clan_style_basis']['father_assertion_id'];a,=[x for x in relations if x.get('id')==aid]
  return a['predicate']=='father'and a['subject_person_id']==n['person_id']and family_valid(a,root=root)and n['clan_style']['value']==n['surname']+'氏'
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError,StopIteration):return False

def guard_bundle(root,person_id,people,records):
 root=Path(root).resolve();rel='corpus/jinshu/080-wangxizhi-comparison.json';path=root/rel
 matches=[r for r in records if isinstance(r,dict)and r.get('record_type')=='marked_chapter'and r.get('id')==CID]
 if not path.exists():
  need(not matches,'catalog殘留已缺來源');return
 ch=json.loads(rootpath(root,rel).read_bytes())
 def participants_of(c):
  need(isinstance(c,dict)and isinstance(c.get('paragraphs'),list),'catalog/source章型別不符');result=set()
  for p in c['paragraphs']:
   need(isinstance(p,dict)and isinstance(p.get('mentions'),list),'catalog/source段型別不符')
   for m in p['mentions']:
    need(isinstance(m,dict),'catalog/source提及型別不符')
    if m.get('kind')=='person':result.add(m.get('person_id'))
  return result
 participants=participants_of(ch)
 for c in matches:participants.update(participants_of(c))
 if person_id not in participants:return
 need(len(matches)==1 and same(matches[0],ch),'catalog/source依賴漂移');roles=validate_source(ch,root);actual={p['id']:p for p in json.loads(rootpath(root,'registry/persons.json').read_bytes())['persons']}
 for pid in set(roles.values()):need(pid in people and same(people[pid],actual[pid]),'catalog/registry依賴漂移')
