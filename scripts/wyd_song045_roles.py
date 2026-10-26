"""Finite WYD045 role layer. Source-only validation remains a separate strict gate."""
import copy,hashlib,json
from pathlib import Path
CID='c-songshu-045-wyd1739-liucui'
PATH='corpus/songshu/045-wyd1739-liucui.json'
CONTRACT='source-evidence/song045-wyd1739-liucui/ner-role-contract.json'
CONTRACT_SHA='05561e24521e8ccc76f43524d958769552660d559f7eeb3ee2a8b02562abfdf9'
KEY='fixed_ner_role_layer'
LAYER={'kind':'wuyingdian_song045_complete_selected_roles','status':'ai_provisional','human_reviewed':False,'coverage':'complete_selected_text_named_roles_first_pass_with_explicit_unresolved'}
def need(ok,message):
 if not ok:raise ValueError('宋045人物層：'+message)
def load_contract(root):
 root=Path(root).resolve();p=(root/CONTRACT).resolve();need(p.is_relative_to(root/'source-evidence'),'契約路徑越界');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==CONTRACT_SHA,'契約SHA');return json.loads(raw)
def reverse(person,ch,p,m):
 if not isinstance(person,dict)or not isinstance(person.get('aliases'),list)or not isinstance(person.get('evidence'),list):return False
 return any(a.get('surface')==m['surface']and isinstance(a.get('mention_ids'),list)and m['id']in a['mention_ids']for a in person.get('aliases',[])if isinstance(a,dict))and any(all(e.get(k)==v for k,v in {'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'mention_id':m['id'],'quote':m['surface']}.items())for e in person.get('evidence',[])if isinstance(e,dict))
def foreign_role(root,seed,people):
 root=Path(root).resolve();p=(root/seed['path']).resolve();need(p.is_relative_to(root/'corpus'),'seed越界');ch=json.loads(p.read_bytes());need(all(ch.get(k)==seed[k]for k in('chapter_id','source_id','work_id','book_id')if k!='chapter_id')and ch.get('id')==seed['chapter_id'],'seed來源維度');need(hashlib.sha256(json.dumps(ch['source'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==seed['source_sha256'],'seed來源SHA');ps=[p for p in ch['paragraphs']if p['id']==seed['paragraph_id']];need(len(ps)==1,'seed段唯一');p=ps[0];need(hashlib.sha256(p['text'].encode()).hexdigest()==seed['paragraph_sha256'],'seed全段SHA');ms=[m for m in p['mentions']if m['id']==seed['mention_id']];need(len(ms)==1,'seedMID唯一');m=ms[0];need(m.get('kind')=='person'and all(m.get(k)==seed[k]for k in('start','end','surface'))and p['text'][m['start']:m['end']]==m['surface'],'seed角色');pid=m.get('person_id');need(pid in people and reverse(people[pid],ch,p,m),'seed反向');return pid
def resolve_roles(ch,root,contract=None):
 need(isinstance(ch,dict),'章須物件');c=contract or load_contract(root);reg=json.loads((Path(root)/'registry/persons.json').read_bytes());people={p['id']:p for p in reg['persons']};need(len(people)==len(reg['persons']),'registry重複');out={r:foreign_role(root,s,people)for r,s in c['foreign_seeds'].items()}
 ps={p['id']:p for p in ch['paragraphs']}
 for spec in c['paragraphs']:
  p=ps[spec['id']];need(hashlib.sha256(p['text'].encode()).hexdigest()==spec['paragraph_sha256'],'本源全段SHA');actual={m['id']:m for m in p['mentions']};need(len(actual)==len(p['mentions']),'重複MID')
  for expected in spec['mentions']:
   role=expected.get('role_key')
   if role is None:continue
   m=actual.get(expected['id']);need(isinstance(m,dict)and m.get('kind')=='person','角色須人物');pid=m.get('person_id');need(pid in people and reverse(people[pid],ch,p,m),'本源反向缺失')
   if role in out:need(out[role]==pid,'本源/跨源角色或單端改號不一致')
   else:out[role]=pid
 need(len(out)==len(set(out.values())),'不同來源角色不可無判讀合併');return out

def source_only_projection(ch,root):
 need(isinstance(ch,dict),'章須物件');c=load_contract(root);need(ch.get('id')==CID,'章ID');a=ch.get('annotation');need(isinstance(a,dict)and isinstance(a.get(KEY),dict)and a.get(KEY)==LAYER and a[KEY].get('human_reviewed')is False,'人物層資格');base=copy.deepcopy(a);base.pop(KEY);expected_annotation={**c['base_annotation'],**c['ner_annotation_overrides']};need(base==expected_annotation,'其他annotation不可漂移');roles=resolve_roles(ch,root,c);need(len(ch['paragraphs'])==len(c['paragraphs']),'段數');out=copy.deepcopy(ch)
 for p,s in zip(ch['paragraphs'],c['paragraphs']):
  need(p['id']==s['id']and p.get('annotation_status')=='named_mentions_first_pass','段界或進度');expected=[]
  for e in s['mentions']:
   m=copy.deepcopy(e);r=m.pop('role_key',None)
   if r is not None:m['person_id']=roles[r]
   expected.append(m)
  need(p.get('mentions')==expected,'固定MID/字位/角色/未定漂移')
 out['annotation']=copy.deepcopy(c['base_annotation'])
 for p in out['paragraphs']:p['mentions']=[];p['annotation_status']='pending'
 return out
RELATION_KIND='fixed_wyd_song045_named_relation'
RELATION_SLOTS=(
 ('cui-grandfather','liucui','grandfather','hui','p001','祖恢','祖恢'),
 ('kuang-father','kuangzhi','father','liucui','p004','以粹子曠之為參軍','子曠之'),
 ('chen-father','chen','father','kuangzhi','p004','曠之卒子琛嗣','子琛'),
 ('huai-father','huaizhi','father','liucui','p004','粹庶長子懷之','庶長子懷之'),
 ('liang-brother','liang','brother','chen','p004','琛弟亮','弟亮'),
 ('sun-father','liusun','father','liuzhenzhi','p014','粹族弟損字子騫衞將軍毅從父弟也父鎮之字仲德','父鎮之'),
 ('sun-clan-younger','liusun','agnatic_cousin','liucui','p014','粹族弟損','族弟'),
 ('sun-congfudi','liusun','agnatic_cousin','liuyi','p014','損字子騫衞將軍毅從父弟也','從父弟'),
 ('cui-clan-younger','liucui','agnatic_cousin','liuyi','p002','衞將軍毅粹族兄也','族兄'),
 ('daozhu-brother','daozhu','brother','chengdaoyang','p008','道養弟道助','弟道助'))
def relation_records(ch,root):
 c=load_contract(root);roles=resolve_roles(ch,root,c);ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']};specs={p['id']:p for p in c['paragraphs']};out=[]
 def mark(p,role,within=None):
  candidates=[e for e in specs[p['id']]['mentions']if e.get('role_key')==role and (within is None or within[0]<=e['start']and e['end']<=within[1])]
  need(bool(candidates),'親屬人物角色缺少');e=candidates[0];m=next(m for m in p['mentions']if m['id']==e['id']);need(m.get('person_id')==roles[role],'親屬角色不符');return m
 for slot,sub,pred,obj,pkey,phrase,term in RELATION_SLOTS:
  p=ps[pkey];need(p['text'].count(phrase)==1,'親屬完整原詞唯一');start=p['text'].index(phrase);area=(start,start+len(phrase));sm=mark(p,sub,area if any(e.get('role_key')==sub and area[0]<=e['start']<area[1]for e in specs[p['id']]['mentions'])else None);om=mark(p,obj,area if any(e.get('role_key')==obj and area[0]<=e['start']<area[1]for e in specs[p['id']]['mentions'])else None)
  q={'source_term':term,'wyd_relation_binding':{'kind':RELATION_KIND,'slot':slot,'paragraph_sha256':hashlib.sha256(p['text'].encode()).hexdigest()}}
  if pred in('father','grandfather'):q['lineage']='paternal'
  if pred=='brother':q['relative_birth_order']={'older_person_id':roles[obj],'younger_person_id':roles[sub],'operator':'lt','scope':'siblings','older_ordinal':None,'younger_ordinal':None}
  if pred=='agnatic_cousin':
   q['kinship_structure']={'lineage':'paternal','generation_difference':0,'collateral':True,'distance':None,'common_ancestor_person_id':None,'subject_relative_age':'younger'}
   q['relative_birth_order']={'older_person_id':roles[obj],'younger_person_id':roles[sub],'operator':'lt','scope':'agnatic_cousins','older_ordinal':None,'younger_ordinal':None}
   if slot=='sun-congfudi':q['source_paternal_path_term']='從父弟';q['reported_kinship_path']=['father','brother','son'];q['path_interpretation']='AI詞義解讀，不建立具名中間父親或共祖。'
  if slot=='huai-father':q['source_birth_position']={'source_term':'庶長子','reported_ordinal':1,'source_qualifier':'庶','accepted_birth_order':None,'scope_interpretation':None,'absolute_ordinal':None,'qualification':'長原稱所報序數一與庶資格分存；適用範圍未定，不推全部子女或庶子內已接受排行，不排懷之與曠之。'}
  e={**{k:ch[k]for k in('work_id','book_id','source_id')},'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'relationship_anchor':{'paragraph_id':p['id'],'start':start,'end':area[1],'surface':phrase},'subject_person_mention_id':sm['id'],'object_person_mention_id':om['id']}
  out.append({'id':'a-song045-wyd-'+slot,'subject_person_id':roles[sub],'predicate':pred,'object_person_id':roles[obj],'status':'source_attested','qualifiers':q,'evidence':[e],'interpretation_note':'本源明文關係；不補生母、生日、共同父祖或絕對排行。從父弟/族弟保原詞與限定。','reviewer':'Codex（AI代理）','human_reviewed':False,'model':None})
 return out

def relation_applies(a):
 if not isinstance(a,dict):return False
 b=a.get('qualifiers',{}).get('wyd_relation_binding',{})
 return a.get('id')in {'a-song045-wyd-'+s[0]for s in RELATION_SLOTS}or isinstance(b,dict)and b.get('kind')==RELATION_KIND

def relation_valid(a,paragraphs,chapters,root):
 try:
  if not isinstance(a,dict)or a.get('human_reviewed')is not False or not isinstance(paragraphs,dict)or not isinstance(chapters,dict):return False
  if a.get('id')=='a-song045-wyd-huai-father':
   reported=a.get('qualifiers',{}).get('source_birth_position',{})
   if not isinstance(reported,dict)or type(reported.get('reported_ordinal'))is not int or reported.get('accepted_birth_order')is not None or reported.get('scope_interpretation')is not None:return False
  ch=chapters[CID];source_only_projection(ch,root);expected=next(x for x in relation_records(ch,root)if x['id']==a.get('id'));pid=expected['evidence'][0]['paragraph_id'];p=next(p for p in ch['paragraphs']if p['id']==pid)
  return a==expected and paragraphs.get(pid)==(CID,p)
 except(KeyError,ValueError,TypeError,StopIteration,OSError,AttributeError):return False
NAME_KIND='fixed_wyd_song045_family_name_components'
SURNAME_KIND='contextual_surname_from_wyd_song045_kinship'
NAME_ROLES=(('liucui','劉','粹','p001','劉粹','道沖',()),('hui','劉','恢','p001','恢',None,('cui-grandfather',)),('liudaoji','劉','道濟','p004','道濟',None,()),('kuangzhi','劉','曠之','p004','曠之',None,('kuang-father',)),('huaizhi','劉','懷之','p004','懷之',None,('huai-father',)),('chen','劉','琛','p004','琛',None,('kuang-father','chen-father')),('liang','劉','亮','p004','亮',None,('kuang-father','chen-father','liang-brother')),('liusun','劉','損','p014','損','子騫',('sun-clan-younger',)),('liuzhenzhi','劉','鎮之','p014','鎮之','仲德',('sun-clan-younger','sun-father')),('chengdaoyang','程','道養','p008','程道養',None,()),('daozhu','程','道助','p008','道助',None,('daozhu-brother',)))
def name_records(ch,root):
 c=load_contract(root);roles=resolve_roles(ch,root,c);ps={p['id'].split(':')[-1]:p for p in ch['paragraphs']};specs={p['id']:p for p in c['paragraphs']};out=[]
 for role,surname,ming,pkey,surface,zi,steps in NAME_ROLES:
  p=ps[pkey];e=next(e for e in specs[p['id']]['mentions']if e.get('role_key')==role and e['surface']==surface);m=next(m for m in p['mentions']if m['id']==e['id']);need(m['person_id']==roles[role],'姓名人物角色')
  n={'id':'name-song045-wyd-'+role,'person_id':roles[role],'surname':surname,'ming':ming,'additional_names':[],'chapter_id':CID,'paragraph_id':p['id'],'person_mention_id':m['id'],'quote':p['text'],'status':'contextual_provisional','human_reviewed':False,'model':None,'wyd_name_binding':{'kind':NAME_KIND,'role':role,'paragraph_sha256':hashlib.sha256(p['text'].encode()).hexdigest(),'name_form':'explicit_full_name'if role in('liucui','chengdaoyang')else 'contextual_surname_source_token_preserved'}}
  if zi:n['zi']=zi
  if role not in('liucui','chengdaoyang'):
   proof=['a-song045-wyd-'+s for s in steps]
   if role=='liudaoji':proof=['a-song044-wyd-liudaoji-liucui-brother']
   n['surname_basis']={'kind':SURNAME_KIND,'source_name_record_id':'name-song045-wyd-'+('chengdaoyang'if role=='daozhu'else 'liucui'),'relationship_assertion_ids':proof,'status':'contextual_provisional','human_reviewed':False,'rationale':'依本源傳首劉粹全名及明祖、父子、弟兄/族弟的逐角色近系判讀；鎮之沿損父稱上溯，原單稱不改。非ID、label、配偶或遠溯祖系推姓。'}
  out.append(n)
 return out

def name_applies(n):
 if not isinstance(n,dict):return False
 return n.get('id')in {'name-song045-wyd-'+x[0]for x in NAME_ROLES}or n.get('wyd_name_binding',{}).get('kind')==NAME_KIND or n.get('surname_basis',{}).get('kind')==SURNAME_KIND

def name_valid(n,names,chapters,assertions,root):
 try:
  if not isinstance(n,dict)or n.get('human_reviewed')is not False or not isinstance(names,list)or not isinstance(chapters,dict)or not isinstance(assertions,list):return False
  if 'surname_basis'in n and (not isinstance(n['surname_basis'],dict)or n['surname_basis'].get('human_reviewed')is not False):return False
  ch=chapters[CID];source_only_projection(ch,root);expected_records=name_records(ch,root);expected=next(x for x in expected_records if x['id']==n.get('id'));need(n==expected,'姓名欄位/角色/姓氏/原名/字/資格');seed=next(x for x in expected_records if x['id']==n.get('surname_basis',{}).get('source_name_record_id',n['id']));need(seed in names,'缺同源全名seed')
  actual={a['id']:a for a in assertions};expected_a={a['id']:a for a in relation_records(ch,root)}
  for aid in n.get('surname_basis',{}).get('relationship_assertion_ids',[]):
   if aid in expected_a:need(actual.get(aid)==expected_a[aid],'姓氏來源鏈缺失或端點錯誤')
   else:
    try:from scripts.wyd_song044_direct_brothers import records as brother_records
    except ImportError:from wyd_song044_direct_brothers import records as brother_records
    original=next(a for a in brother_records(root)if a['id']==aid);need(actual.get(aid)==original,'既有明弟來源鏈不符');roles=resolve_roles(ch,root);need(original['subject_person_id']==roles['liudaoji']and original['object_person_id']==roles['liucui'],'跨篇弟兄端點錯誤')
  return True
 except(KeyError,ValueError,TypeError,StopIteration,OSError,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root):
 if not name_valid(n,names,chapters,assertions,root):raise ValueError('宋045推姓須由完整原文角色與有源近系逐鏈，不依ID/label或任意相鄰人名')
