"""Finite Song051 first-family phase. No person-ID allowlist or text inference."""
from pathlib import Path
import json,copy,hashlib
CID='c-songshu-051-wyd1739-zongshi'
CH='corpus/songshu/051-wyd1739.json'
REF='source-evidence/song051-wyd1739-zongshi/formal-role-contract.json'
CONTRACT_SHA='7fed0f55ceb458db3ad9607fff69396d87e1a3864560020533a35d066eac6ce6'
FACTS='corpus/songshu/051-wyd1739-assertions.json'
NAMES='corpus/songshu/051-wyd1739-name-components.json'
KIND='fixed_wyd_song051_direct_family_phase1'
sha=lambda b:hashlib.sha256(b).hexdigest()
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return all(type(k)is str for k in a)and all(type(k)is str for k in b)and set(a)==set(b)and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 if a is None or type(a)in(str,int,bool):return a==b
 if type(a)is float:
  try:return json.dumps(a,allow_nan=False)==json.dumps(b,allow_nan=False)
  except ValueError:return False
 return False
def need(ok,message):
 if not ok:raise ValueError('武英殿宋051有限親族：'+message)
def read_contract(root):
 root=Path(root).resolve();p=(root/REF).resolve();need(p.is_relative_to(root/'source-evidence'),'契約路徑');raw=p.read_bytes();need(sha(raw)==CONTRACT_SHA,'契約SHA');return json.loads(raw)
def materialize(value,roles):
 if isinstance(value,dict):
  if set(value)=={'$role'}:return roles[value['$role']]
  return{k:materialize(v,roles)for k,v in value.items()}
 if isinstance(value,list):return[materialize(v,roles)for v in value]
 return value
def resolve_existing(root,c):
 # Reuse the established pure source-MID resolver; its CID is not used by resolve.
 try:from scripts.wyd_song044_role_seed import resolve
 except ImportError:from wyd_song044_role_seed import resolve
 bindings={}
 for s in c['existing_seeds']:
  chapter=json.loads((Path(root)/s['path']).read_bytes());metadata=chapter['source'];need(sha(json.dumps(metadata,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==s['source_metadata_sha256'],'種子完整來源')
  raw_path=metadata.get('raw_path') or metadata.get('raw_file')
  raw_hash=metadata.get('raw_file_sha256') or metadata.get('raw_sha256')
  if raw_path is not None or raw_hash is not None:
   need(isinstance(raw_path,str)and bool(raw_path)and isinstance(raw_hash,str)and len(raw_hash)==64,'種子原檔定位或SHA不完整')
   rp=(Path(root)/raw_path).resolve();need(rp.is_relative_to(Path(root).resolve()),'種子原檔越界');need(sha(rp.read_bytes())==raw_hash,'種子原檔SHA漂移')
  p,=[p for p in chapter['paragraphs']if p['id']==s['paragraph_id']]
  seed={'path':s['path'],'work_id':s['dimensions']['work_id'],'book_id':s['dimensions']['book_id'],'source_id':s['dimensions']['source_id'],'chapter_id':s['dimensions']['id'],'source_revision':metadata['revision_id'],'source_metadata_sha256':s['source_metadata_sha256'],'source_identity_fields':{k:metadata[k]for k in ['provider','url','revision_id']},'paragraph_id':p['id'],'paragraph_text':p['text'],'paragraph_sha256':s['text_sha256'],'marker':s['marker']}
  bindings.setdefault(s['role_key'],{'seeds':[]})['seeds'].append(seed)
 return resolve(root,{'bindings':bindings})
def phase_chapter(c,roles):
 ch=copy.deepcopy(c['source_before']);ch['annotation']=copy.deepcopy(c['phase_annotation'])
 for p in ch['paragraphs']:
  p['mentions']=[materialize(row['marker'],roles)for row in c['markers']if row['paragraph_id']==p['id']]
  if p['mentions']:p['annotation_status']='in_progress'
 return ch
def collect_roles(ch,c):
 roles={}
 for row in c['markers']:
  p,=[p for p in ch['paragraphs']if p['id']==row['paragraph_id']];m,=[m for m in p['mentions']if m['id']==row['marker']['id']]
  k=row['role'];pid=m['person_id'];need(k not in roles or roles[k]==pid,'同角色不同號');roles[k]=pid
 need(len(roles)==16 and len(set(roles.values()))==16,'本批角色須各自確指不同個體');return roles
def evidence(ch,para,subject,object_,roles):
 p=next(p for p in ch['paragraphs']if p['id'].endswith(':'+para))
 def marker(role):return next(m for m in p['mentions']if m.get('source_role_key')==role)
 s=marker(subject);o=marker(object_)
 return dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text'],subject_person_mention_id=s['id'],object_person_mention_id=o['id'])
def assertions(ch,roles):
 result=[]
 def fact(key,predicate,child,parent,para,term,extra=None):
  q={'source_term':term,'source_clause_binding':{'kind':KIND,'case':key,'raw_sha256':ch['source']['raw_sha256']}}
  if predicate=='father':q.update(lineage='paternal',source_child_term='子',source_child_sex='male')
  if extra:q.update(extra)
  result.append({'id':'a-song051-phase1-'+key,'subject_person_id':roles[child],'predicate':predicate,'object_person_id':roles[parent],'status':'source_attested','qualifiers':q,'human_reviewed':False,'model':None,'evidence':[evidence(ch,para,child,parent,roles)]})
 for child in ['yixin','yiqing','yirong','yizong','yibin','yiqi']:fact(child+'-father','father',child,'daolian','p008','道憐六子義欣義慶義融義宗義賓義綦')
 fact('zong-father','father','zong_yibin_son','yibin','p018','子惠侯綜嗣')
 fact('xian-father','father','xian_zong_son','zong_yibin_son','p018','綜嗣卒子憲嗣')
 fact('changxin-father','father','changxin_yiqi_son','yiqi','p019','子長猷嗣')
 fact('gui-brother','brother','gui_zong_brother','zong_yibin_son','p018','綜弟珪',{'shared_father':None,'subject_relative_age':'younger','lineage':'paternal','interpretation_note':'原詞明弟；同父用於家族組裝為可撤回的近系推導，不冒本源逐字明父。'})
 fact('yiqing-adoptive-father','adoptive_father','yiqing','daogui','p012','義慶出繼臨川烈武王道規',{'adoption_basis':'fixed_wyd_song051_named_chuji','modern_legal_status':'not_inferred','biological_father_assertion_id':'a-song051-phase1-yiqing-father','interpretation_note':'本源明出繼；道規無子以長沙景王第二子義慶為嗣另有同卷文字支持；不覆生父。'})
 return{'format_version':'0.2','record_type':'person_assertion_set','chapter_id':CID,'assertions':result}
def literal_names(ch,roles,c):
 rows=[]
 for role,ming in c['new_roles'].items():
  p,m=next((p,m)for p in ch['paragraphs']for m in p['mentions']if m.get('source_role_key')==role and m['surface']==ming)
  rows.append({'id':'name-song051-phase1-'+role,'person_id':roles[role],'surname':None,'ming':ming,'additional_names':[],'chapter_id':CID,'paragraph_id':p['id'],'person_mention_id':m['id'],'quote':p['text'],'status':'editorial_provisional','human_reviewed':False,'model':None,'component_source_binding':{'kind':'fixed_wyd_song051_literal_ming','role':role,'name_form':'ming_only_literal','raw_sha256':ch['source']['raw_sha256'],'paragraph_sha256':sha(p['text'].encode())},'note':'本源明名，姓氏未在本筆補入；不從ID、label或父系圖自動填姓。'})
 for role,spec in c['clan_roles'].items():
  p,m=next((p,m)for p in ch['paragraphs']for m in p['mentions']if m.get('source_role_key')==role and m['surface']==spec['source_term'])
  rows.append({'id':'name-song051-phase1-literal-clan-'+role,'person_id':roles[role],'surname':spec['surname'],'ming':None,'additional_names':[],'chapter_id':CID,'paragraph_id':p['id'],'person_mention_id':m['id'],'quote':p['text'],'status':'editorial_provisional','human_reviewed':False,'model':None,'component_source_binding':{'kind':'fixed_wyd_song051_literal_clan','role':role,'name_form':'literal_clan_only','raw_sha256':ch['source']['raw_sha256'],'paragraph_sha256':sha(p['text'].encode())},'clan_style':{'kind':'received_clan_appellation','value':spec['source_term'],'source_term':spec['source_term'],'assertion_ids':[],'status':'source_attested','rationale':'本源逐字氏稱，姓明名未載；不從夫姓/ID填姓，不補丈夫、生母或養母。','human_reviewed':False}})
 return{'format_version':'0.2','record_type':'person_name_component_set','chapter_id':CID,'records':rows}
INTRO_CH='corpus/songshu/005-wyd1739-wendi-opening.json'
INTRO_FACTS='corpus/songshu/005-wyd1739-wendi-opening-assertions.json'
def intro_chapter(c,roles):
 spec=c['song005_opening_bridge'];ch=copy.deepcopy(spec['source_before']);ch['annotation']['formal_phase']=spec['phase'];ch['annotation']['coverage']='完整所選246字傳首的姓名、稱謂與代詞第一輪14錨；不稱卷005全卷NER完成。'
 for p in ch['paragraphs']:
  p['mentions']=[materialize(r['marker'],roles)for r in spec['markers']if r['paragraph_id']==p['id']]
  if p['mentions']:p['annotation_status']='in_progress'
 return ch

def intro_facts(c,roles):
 ch=intro_chapter(c,roles);p=ch['paragraphs'][0];sm=next(m for m in p['mentions']if m['surface']=='義隆');om=next(m for m in p['mentions']if m['surface']=='武帝')
 a={'id':'a-song005-opening-phase1-wendi-father','subject_person_id':roles['taizu'],'predicate':'father','object_person_id':roles['gaozu'],'status':'source_attested','qualifiers':{'source_term':'武帝第三子也','lineage':'paternal','source_child_term':'子','source_child_sex':'male','source_clause_binding':{'kind':'fixed_wyd_song005_opening_father_phase1','raw_sha256':ch['source']['raw_sha256']},'reported_son_ordinal':{'value':3,'source_term':'第三子','scope':'sons_of_named_father','source_range':{'paragraph_id':p['id'],'start':14,'end':17,'surface':'第三子'}},'interpretation_note':'本源明武帝第三子；父角色另由既收劉裕全文名種子核定，不將武帝原字改高祖、不由ID推排行。'},'human_reviewed':False,'model':None,'evidence':[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'quote':p['text'],'subject_person_mention_id':sm['id'],'object_person_mention_id':om['id']}]}
 return {'format_version':'0.2','record_type':'person_assertion_set','chapter_id':ch['id'],'assertions':[a]}

def family_projection_valid(root,ch,roles):
 doc=json.loads((Path(root)/'registry/family-assemblies.json').read_bytes());f,=[f for f in doc['assemblies']if f['id']=='family-song041-qiao'];rows={r['person_id']:r for r in f['members']};need(len(rows)==len(f['members']),'家系成員重複')
 expected=[(r,'daolian','a-song051-phase1-'+r+'-father')for r in ['yixin','yiqing','yirong','yizong','yibin','yiqi']]+[('zong_yibin_son','yibin','a-song051-phase1-zong-father'),('xian_zong_son','zong_yibin_son','a-song051-phase1-xian-father'),('changxin_yiqi_son','yiqi','a-song051-phase1-changxin-father'),('taizu','gaozu','a-song005-opening-phase1-wendi-father')]
 for child,parent,aid in expected:
  row=rows.get(roles[child],{});need(row.get('parent_person_id')==roles[parent]and row.get('source_assertion_id')==aid and not row.get('parent_connection'),'本源明父家系缺失/被母嗣系替換')
 row=rows.get(roles['gui_zong_brother'],{});p18=next(p for p in ch['paragraphs']if p['id'].endswith(':p018'));connection={'type':'shared_father_through_sibling','sibling_person_id':roles['zong_yibin_son'],'sibling_assertion_id':'a-song051-phase1-gui-brother','sibling_father_assertion_id':'a-song051-phase1-zong-father','status':'contextual_provisional','rationale':'本源綜弟珪，綜又明為義賓子；首選按同父近系組裝。不是本源逐字父句，不造其他父，不由爵位承襲或名單次序推定。','references':[{'title':'《宋書・宗室》','url':ch['source']['url'],'quote':p18['text'],'scope':'綜明父與綜弟珪同完整段；只採有資格同父推定，不補生母或絕對排行。'}]}
 need(row.get('parent_person_id')==roles['yibin']and row.get('source_assertion_id')is None and same(row.get('parent_connection'),connection),'珪須保明弟＋綜明父的有限推定家系，不能冒逐字父句')
 for parent,aid,rel in [('yiqing','a-song075-sengda-004','corpus/songshu/075-wangsengda-assertions.json'),('taizu','a-song071-sengchuo-003','corpus/songshu/071-wangsengchuo-assertions.json')]:
  d=json.loads((Path(root)/rel).read_bytes());hits=[a for a in d.get('assertions',[])if a.get('id')==aid]
  a,=hits;need(a.get('predicate')=='father'and a.get('object_person_id')==roles[parent],'既有女支父證改變');row=rows.get(a['subject_person_id'],{});need(row.get('parent_person_id')==roles[parent]and row.get('source_assertion_id')==aid,'既有女支未保全於同父系')
 return True

try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized

@memoized(0)
def _phase1_context(root,ch=None,check_sidecars=True):
 root=Path(root);c=read_contract(root);actual=json.loads((root/CH).read_bytes());ch=actual if ch is None else ch;need(same(ch,actual),'呼叫章與現行章不符')
 roles=collect_roles(ch,c);need(same(ch,phase_chapter(c,roles)),'完整原文/位置/資格或49錨不符')
 expected=resolve_existing(root,c);need(all(roles[k]==v for k,v in expected.items()if k in roles),'跨篇現役角色不同號');roles.update(expected);need(len(set(roles.values()))==len(roles),'祖父與後代角色不得混號')
 temple_contract=copy.deepcopy(c);temple_contract['existing_seeds']=[c['temple_identity_seed']];need(resolve_existing(root,temple_contract).get('temple_identity_candidate')==roles['taizu'],'太祖與義隆同指未閉合')
 intro=json.loads((root/INTRO_CH).read_bytes());need(same(intro,intro_chapter(c,roles)),'005完整轉錄/位置/有限14錨漂移')
 try:from scripts.fixed_wuyingdian_song005_opening import validate_source as validate_intro
 except ImportError:from fixed_wuyingdian_song005_opening import validate_source as validate_intro
 validate_intro(c['song005_opening_bridge']['source_before'],root)
 people={p['id']:p for p in json.loads((root/'registry/persons.json').read_bytes())['persons']}
 for p in ch['paragraphs']+intro['paragraphs']:
  owner=ch if p['id'].startswith(CID+':')else intro
  for m in p['mentions']:
   person=people.get(m['person_id']);need(bool(person),'人物未登記')
   need(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'缺反向alias')
   e=dict(work_id=owner['work_id'],book_id=owner['book_id'],source_id=owner['source_id'],chapter_id=owner['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(e in person['evidence'],'缺反向evidence')
 # The original pending validator is unchanged; normalize only after exact formal proof.
 try:from scripts.fixed_wuyingdian_song051 import validate_source
 except ImportError:from fixed_wuyingdian_song051 import validate_source
 validate_source(c['source_before'],root)
 family_projection_valid(root,ch,roles)
 facts=assertions(ch,roles);ns=names(ch,roles,c,root)
 if check_sidecars:
  need(same(json.loads((root/INTRO_FACTS).read_bytes()),intro_facts(c,roles)),'005明父表漂移')
  need(same(json.loads((root/INTRO_IDENTITIES).read_bytes()),intro_identities(c,roles,root)),'005傳首五角色身份證據漂移')
  need(same(json.loads((root/FACTS).read_bytes()),facts),'本批親屬表或主語方向不符')
  need(same(json.loads((root/NAMES).read_bytes()),ns),'本批姓名表不符')
  for rel,doc in full_seed_docs(root,c,roles).items():need(same(json.loads((root/rel).read_bytes()),doc),'外部全名種子表不符')
  need(same(json.loads((root/IDENTITIES).read_bytes()),identities(ch,roles,c,root)),'本批身份或兩個2的來源讀法不符')
 return ch,roles,c,facts,ns

def source_errors(ch,root):
 try:from scripts.fixed_wuyingdian_song051 import source_errors as pending_errors
 except ImportError:from fixed_wuyingdian_song051 import source_errors as pending_errors
 if not isinstance(ch,dict)or not isinstance(ch.get('annotation'),dict)or ch['annotation'].get('formal_phase')!='song051_direct_family_phase1':return pending_errors(ch,root)
 try:context(root,ch);return []
 except (ValueError,KeyError,TypeError,OSError,UnicodeError,StopIteration,AttributeError)as e:return['武英殿宋051有限親族：'+str(e)]
def source_errors005(ch,root):
 try:from scripts.fixed_wuyingdian_song005_opening import source_errors as pending_errors
 except ImportError:from fixed_wuyingdian_song005_opening import source_errors as pending_errors
 if not isinstance(ch,dict)or not isinstance(ch.get('annotation'),dict)or ch['annotation'].get('formal_phase')!='song005_opening_emperor_identity_bridge_phase1':return pending_errors(ch,root)
 try:
  current,roles,c,facts,ns=context(root);need(same(ch,intro_chapter(c,roles)),'005呼叫章與現行不符');return []
 except (ValueError,KeyError,TypeError,OSError,UnicodeError,StopIteration,AttributeError)as e:return ['武英殿宋005有限身份橋：'+str(e)]

def _phase1_applies(a):
 if not isinstance(a,dict):return False
 q=a.get('qualifiers');b=q.get('source_clause_binding')if isinstance(q,dict)else None
 return str(a.get('id','')).startswith(('a-song051-phase1-','a-song005-opening-phase1-'))or isinstance(b,dict)and b.get('kind')==KIND
def _phase1_family_valid(a,paragraphs,chapters,root):
 try:
  ch,roles,c,facts,ns=context(root);need(any(same(a,x)for x in facts['assertions']+intro_facts(c,roles)['assertions']),'非本批逐字親屬')
  for e in a['evidence']:
   owner=ch if e['chapter_id']==CID else intro_chapter(c,roles);p=next(p for p in owner['paragraphs']if p['id']==e['paragraph_id']);frame=paragraphs.get(p['id']);need(type(frame)is tuple and len(frame)==2 and frame[0]==owner['id']and same(frame[1],p)and same(chapters.get(owner['id']),owner),'親屬所給章段與現行不符')
  return True
 except (ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False
def _phase1_component_valid(n,ch,root):
 try:
  current,roles,c,facts,ns=context(root)
  if n.get('component_source_binding',{}).get('kind')=='fixed_wyd_song051_external_fullname_seed':
   for seed in c['literal_full_name_seeds']:
    if n.get('id')==seed['name_record_id']:
     foreign=json.loads((Path(root)/seed['path']).read_bytes());return same(ch,foreign)and any(same(n,x)for x in full_seed_docs(root,c,roles)[seed['component_path']]['records'])
   return False
  return same(ch,current)and any(same(n,x)for x in ns['records'])
 except (ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

SEED_NAMES='corpus/jinshu/099-huanxuan-song051-seed-name-components.json'
IDENTITIES='corpus/songshu/051-wyd1739-identities.json'
SURNAME_KIND='contextual_surname_from_wyd_song051_named_path'
def external_parents(root,c,roles):
 doc=json.loads((Path(root)/c['external_parent_assertions']['path']).read_bytes());result=[]
 for template in c['external_parent_assertions']['templates']:
  expected=materialize(template,roles);hits=[a for a in doc['assertions']if a['id']==expected['id']];need(same(hits,[expected]),'041父稱原句/方向/資格漂移');result.append(expected)
 return result

def full_seed_docs(root,c,roles):
 docs={}
 for seed in c['literal_full_name_seeds']:
  ch=json.loads((Path(root)/seed['path']).read_bytes());p=next(p for p in ch['paragraphs']if p['id']==seed['paragraph_id']);m=next(m for m in p['mentions']if m['id']==seed['marker']['id']);need(m['surface']==seed['surname']+seed['ming'],'全名原錨不符')
  n={'id':seed['name_record_id'],'person_id':roles[seed['role_key']],'surname':seed['surname'],'ming':seed['ming'],'additional_names':[],'chapter_id':ch['id'],'paragraph_id':p['id'],'person_mention_id':m['id'],'quote':p['text'],'status':'editorial_provisional','human_reviewed':False,'model':None,'component_source_binding':{'kind':'fixed_wyd_song051_external_fullname_seed','seed_mention_id':m['id'],'source_metadata_sha256':seed['source_metadata_sha256'],'paragraph_sha256':seed['text_sha256']},'note':'既存收到見證逐字全名，作本批同指氏姓外證；不冒武英殿宋051原來含省略的姓或名。'}
  docs.setdefault(seed['component_path'],{'format_version':'0.2','record_type':'person_name_component_set','chapter_id':ch['id'],'records':[]})['records'].append(n)
 return docs

def full_seed_name(root,c,roles):
 return full_seed_docs(root,c,roles)[SEED_NAMES]

def restored_names(root,ch,roles,c,facts):
 aa={a['id']:a for a in facts['assertions']+external_parents(root,c,roles)};result=[]
 for role,path in c['surname_paths'].items():
  ming=c['role_ming'][role]
  p,m=next((p,m)for p in ch['paragraphs']for m in p['mentions']if m.get('source_role_key')==role and (m['surface']==ming or role in ('gaozu','taizu')))
  seed=next(s for s in c['literal_full_name_seeds']if s['role_key']==c['surname_seed_role'][role])
  steps=[]
  for spec in path:
   a=aa[spec['assertion_id']];step={k:v for k,v in spec.items()if k not in ('from_role','to_role')};step.update(from_person_id=roles[spec['from_role']],to_person_id=roles[spec['to_role']],evidence=copy.deepcopy(a['evidence']),assertion_record=copy.deepcopy(a))
   if 'supporting_father_assertion_id'in spec:step['supporting_father_evidence']=copy.deepcopy(aa[spec['supporting_father_assertion_id']]['evidence'])
   steps.append(step)
  n={'id':'name-song051-phase1-restored-'+role,'person_id':roles[role],'surname':'劉','ming':ming,'additional_names':[],'chapter_id':CID,'paragraph_id':p['id'],'person_mention_id':m['id'],'quote':p['text'],'status':'contextual_provisional','human_reviewed':False,'model':None,'component_source_binding':{'kind':'fixed_wyd_song051_contextual_name','role':role,'name_form':'context_restored_surname','raw_sha256':ch['source']['raw_sha256'],'paragraph_sha256':sha(p['text'].encode())},'surname_basis':{'kind':SURNAME_KIND,'status':'contextual_provisional','source_name_record_id':seed['name_record_id'],'steps':steps,'rationale':'晉099逐字劉道規全名，041既有婚生父稱雙證及WYD051具名近系鏈。保各原證資格；珪同父為明弟及綜明父的近系推導。非由familyID、名單順序、label或妻母推姓。','human_reviewed':False,'model':None}}
  result.append(n)
 return result

def names(ch,roles,c,root=None):
 doc=literal_names(ch,roles,c)
 if root is not None:doc['records'].extend(restored_names(root,ch,roles,c,assertions(ch,roles)))
 return doc

def ordinal_readings(ch,roles,role):
 specs={'yizong':('p003','次子義宗','次子','義宗'),'yiqing':('p028','第二子義慶','第二子','義慶')}
 if role not in specs:return []
 para,phrase,term,ming=specs[role];p=next(p for p in ch['paragraphs']if p['id'].endswith(':'+para));start=p['text'].index(phrase);m=next(m for m in p['mentions']if m['person_id']==roles[role]and m['start']==start+len(term));parent=next(m for m in p['mentions']if m['person_id']==roles['daolian'])
 return[{'id':'ord-song051-phase1-'+role,'kind':'source_reported_son_ordinal_reading','person_id':roles[role],'parent_person_id':roles['daolian'],'source_term':term,'reported_ordinal':2,'accepted_birth_order':None,'scope_interpretation':None,'status':'unresolved_scope','source_range':{'paragraph_id':p['id'],'start':start,'end':start+len(phrase),'surface':phrase,'target_mention_id':m['id'],'parent_mention_id':parent['id']},'rationale':'來源原詞所報2保留；次子與第二子是否同一生序範圍未定，宗法/存世/出繼等解釋尚待核，不能由六子列表定序或作兩人同一已解生序。','human_reviewed':False,'model':None}]

def succession_reading(ch,roles):
 p=next(p for p in ch['paragraphs']if p['id'].endswith(':p028'));specs=[('raised_by','初太祖少為道規所養',{'subject_person_id':roles['taizu'],'caretaker_person_id':roles['daogui']}),('ordered_succession','高祖命紹焉',{'ordering_person_id':roles['gaozu'],'prospective_heir_person_id':roles['taizu'],'prospective_predecessor_person_id':roles['daogui']}),('ritual_objection','咸以禮無二繼',{'collective_speakers':True,'principle':'no_double_succession'}),('returned_to_original_line','太祖還本',{'subject_person_id':roles['taizu'],'withdrawn_prospective_predecessor_person_id':roles['daogui']}),('heir_confirmed','而定義慶',{'heir_person_id':roles['yiqing'],'predecessor_person_id':roles['daogui']})];events=[]
 for i,(kind,quote,actors) in enumerate(specs,1):
  start=p['text'].index(quote);events.append({'sequence':i,'event_type':kind,**actors,'source_range':{'paragraph_id':p['id'],'start':start,'end':start+len(quote),'surface':quote},'date_expression':None,'current_parent_edge_created':False,'interpretation_status':'contextual_provisional','human_reviewed':False,'model':None})
 return {'kind':'source_reported_historical_succession_sequence','events':events,'present_adoptive_father_asserted_for_subject':False,'rationale':'受養、命紹及後還本分存歷史經過；義隆不存永久嗣父道規。後定義慶另有明出繼來源，生父道憐仍保留；年份、母親與法律身分不補。','human_reviewed':False,'model':None}

def identities(ch,roles,c,root):
 out=[]
 for role in sorted({r['role']for r in c['markers']}):
  hits=[(p,m)for p in ch['paragraphs']for m in p['mentions']if m['source_role_key']==role];surfaces=list(dict.fromkeys(m['surface']for p,m in hits));p,m=hits[0]
  d={'id':'d-song051-phase1-'+role,'person_id':roles[role],'surfaces':surfaces,'scope':'cross_chapter'if role not in c['source_local_registration_roles']else'same_chapter','chapter_ids':[CID],'status':'contextual_provisional','confidence_level':'high','identification_basis':{'kind':'source_context','target_mention_ids':[m['id']for p,m in hits]},'evidence':[dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text'])],'rationale':'有限親族段落的具名人物辨識；既有角色由固定外部MID及雙向來源回查，新源局部角色不斷言與全庫已證異人。未明母/婚配/出生年不補。','human_reviewed':False,'model':None}
  if role in c.get('role_rationales',{}):
   d['rationale']=c['role_rationales'][role]
   if role=='tan_taifei':d['confidence_level']='medium'
  if role=='taizu':
   d['historical_succession_reading']=succession_reading(ch,roles);d['rationale']+=' '+d['historical_succession_reading']['rationale']
   intro=intro_chapter(c,roles);ip=intro['paragraphs'][0];d['chapter_ids'].append(intro['id']);d['evidence'].append({'work_id':intro['work_id'],'book_id':intro['book_id'],'source_id':intro['source_id'],'chapter_id':intro['id'],'paragraph_id':ip['id'],'quote':ip['text']});d['rationale']+=' 武英殿卷005完整傳首明太祖文皇帝諱義隆、武帝第三子；本處太祖與既收劉義隆全文名角色取同指首選，全部當前引用統一，不保兩個同人副本。原武帝、小字車兒與京城不改字；不補本單元未載母親或正式字。'

  for seed in c['existing_seeds']+([dict(c['temple_identity_seed'],role_key='taizu')]if role=='taizu'else []):
   if seed['role_key']!=role:continue
   foreign=json.loads((Path(root)/seed['path']).read_bytes());fp=next(p for p in foreign['paragraphs']if p['id']==seed['paragraph_id'])
   if foreign['id']not in d['chapter_ids']:d['chapter_ids'].append(foreign['id'])
   item={'work_id':foreign['work_id'],'book_id':foreign['book_id'],'source_id':foreign['source_id'],'chapter_id':foreign['id'],'paragraph_id':fp['id'],'quote':fp['text']}
   if item not in d['evidence']:d['evidence'].append(item)
  d['scope']='cross_chapter'if len(d['chapter_ids'])>=2 else'same_chapter'
  reports=ordinal_readings(ch,roles,role)
  if reports:
   d['source_ordinal_readings']=reports;d['rationale']+=' '+reports[0]['rationale'];r=reports[0];p=next(p for p in ch['paragraphs']if p['id']==r['source_range']['paragraph_id']);d['evidence'].append(dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text']));d['references']=[{'title':'《宋書・宗室》','url':ch['source']['url'],'quote':p['text'],'scope':'兩處來源所報2分存，不採入已解生序','access_scope_display':'已核讀所列武英殿本段落；AI轉錄，未經人工校勘。','human_reviewed':False,'image_verified':False,'model':None}]
  out.append(d)
 return{'format_version':'0.2','record_type':'person_identity_decision_set','chapter_id':CID,'decisions':out}

def _phase1_validate_surname(n,all_names,chapters,all_assertions,root):
 try:
  ch,roles,c,facts,ns=context(root);expected,=[x for x in ns['records']if x['id']==n['id']];need(same(n,expected)and n.get('surname_basis',{}).get('kind')==SURNAME_KIND,'限本源已列氏姓讀法')
  seed_spec=next(s for s in c['literal_full_name_seeds']if s['name_record_id']==n['surname_basis']['source_name_record_id']);seed=next(x for x in full_seed_docs(root,c,roles)[seed_spec['component_path']]['records']if x['id']==seed_spec['name_record_id']);need(same([x for x in all_names if x.get('id')==seed['id']],[seed]),'全名種子不存在/重複/改讀');need(same(chapters.get(CID),ch),'姓名章不符')
  foreign=json.loads((Path(root)/seed_spec['path']).read_bytes());need(same(chapters.get(foreign['id']),foreign),'外部全名章不符')
  expected_facts={a['id']:a for a in facts['assertions']+external_parents(root,c,roles)};b=n['surname_basis'];current=seed['person_id'];generation=0;seen={current}
  for step in b['steps']:
   hits=[a for a in all_assertions if a.get('id')==step['assertion_id']];need(same(hits,[expected_facts[step['assertion_id']]]),'路徑原證重複/方向/資格改變');a=hits[0];q=a['qualifiers']
   need(not q.get('adoptive')and not q.get('same_mother_only')and not q.get('sworn')and q.get('shared_father')is not False and q.get('lineage')not in('maternal','non_paternal'),'不得混母嗣系')
   need(step['from_person_id']==current and step['generation_before']==generation and step['evidence']==a['evidence'],'來源步與世代不符');target=step['to_person_id']
   if step['traversal']=='child_to_father':need(a['predicate']=='father'and(a['subject_person_id'],a['object_person_id'])==(current,target)and step['generation_after']==generation-1,'反向父步不符')
   elif step['traversal']=='father_to_child':need(a['predicate']=='father'and(a['object_person_id'],a['subject_person_id'])==(current,target)and step['generation_after']==generation+1,'正向父步不符')
   else:
    need(step['traversal']=='same_father_sibling'and a['id']=='a-song051-phase1-gui-brother'and a['predicate']=='brother'and(a['object_person_id'],a['subject_person_id'])==(current,target)and step['generation_after']==generation,'限珪與綜本源明弟步')
    support=expected_facts[step['supporting_father_assertion_id']];need([x for x in all_assertions if x.get('id')==support['id']]==[support]and support['subject_person_id']==current and step['supporting_father_evidence']==support['evidence'],'明弟推定須另有綜明父')
   need(target not in seen,'不得循環');current=target;seen.add(target);generation=step['generation_after']
  need(current==n['person_id']and n['surname']==seed['surname'],'氏姓路徑終點不符')
 except (ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):raise ValueError('宋051氏姓須有晉099逐字全名、041雙父證及本源有限父系路徑，不借ID/母嗣系或省略推定步')

INTRO_IDENTITIES='corpus/songshu/005-wyd1739-wendi-opening-identities.json'
def intro_identities(c,roles,root):
 ch=intro_chapter(c,roles);out=[]
 for role in sorted({r['role']for r in c['song005_opening_bridge']['markers']}):
  hits=[(p,m)for p in ch['paragraphs']for m in p['mentions']if m['source_role_key']==role];paragraphs=[]
  for p,m in hits:
   if p not in paragraphs:paragraphs.append(p)
  evidence=[{'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':ch['id'],'paragraph_id':p['id'],'quote':p['text']}for p in paragraphs];chapter_ids=[ch['id']]
  seeds=[s for s in c['existing_seeds']if s['role_key']==role]
  if role=='taizu':seeds.append(c['temple_identity_seed'])
  for seed in seeds:
   foreign=json.loads((Path(root)/seed['path']).read_bytes());p=next(p for p in foreign['paragraphs']if p['id']==seed['paragraph_id']);item={'work_id':foreign['work_id'],'book_id':foreign['book_id'],'source_id':foreign['source_id'],'chapter_id':foreign['id'],'paragraph_id':p['id'],'quote':p['text']}
   if item not in evidence:evidence.append(item)
   if foreign['id']not in chapter_ids:chapter_ids.append(foreign['id'])
  reasons={'taizu':'本傳首明太祖文皇帝諱義隆、小字車兒、武帝第三子；上均承傳主，不因鄰近安帝、盧循、劉粹而轉指。與既收具名劉義隆及宋044太祖取有據同指。','gaozu':'本傳首武帝明為義隆父，下文高祖使劉粹輔上、伐羌及還彭城皆劉裕；原武帝不改寫高祖，原京城不自動改建康。','jinandi':'本源晉安帝義熙三年，與既收晉安帝隆安及司馬德宗/徳宗統治時段相符；不因全名精確零召回另建人。','luxun':'本源盧循之難，與既收劉裕南摧盧循的同時代軍事脈絡相符；只辨名，不聲稱與義隆同地在場或親屬。','liucui':'本源高祖使諮議參軍劉粹輔義隆鎮京城，與既收宋044同朝軍政的劉粹取同指；不混弟劉道濟，無關母系不補。'}
  out.append({'id':'d-song005-opening-phase1-'+role,'person_id':roles[role],'surfaces':list(dict.fromkeys(m['surface']for p,m in hits)),'scope':'cross_chapter'if len(chapter_ids)>1 else'same_chapter','chapter_ids':chapter_ids,'status':'contextual_provisional','confidence_level':'high','identification_basis':{'kind':'source_context','target_mention_ids':[m['id']for p,m in hits]},'evidence':evidence,'rationale':reasons[role],'human_reviewed':False,'model':None})
 return {'format_version':'0.2','record_type':'person_identity_decision_set','chapter_id':ch['id'],'decisions':out}

def _phase1_guard_bundle(root,person_id,people,records):
 root=Path(root);candidate=people.get(person_id)
 registered_relevant=isinstance(candidate,dict)and any(e.get('chapter_id')in(CID,'c-songshu-005-wyd1739-wendi-opening')for e in candidate.get('evidence',[]))
 source_records=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')in(CID,'c-songshu-005-wyd1739-wendi-opening')]
 source_relevant=any(m.get('person_id')==person_id for source in source_records for p in source.get('paragraphs',[])for m in p.get('mentions',[]))
 if not registered_relevant and not source_relevant:return
 registered=json.loads((root/'registry/persons.json').read_bytes())['persons'];hit=next((p for p in registered if p['id']==person_id),None)
 ch,roles,c,facts,ns=context(root)
 need(same(people.get(person_id),hit),'bundle人物catalog與current不符')
 for rel in [CH,INTRO_CH,FACTS,INTRO_FACTS,NAMES,IDENTITIES,INTRO_IDENTITIES]+list(full_seed_docs(root,c,roles)):
  expected=json.loads((root/rel).read_bytes());need(sum(same(r,expected)for r in records)==1,'bundle缺完整本源/姓名/親屬/身份資料或重複')


# song051-yixin-complete-unit-phase2
def _phase2_context(root,ch=None,check_sidecars=True):
 root=Path(root);c=read_contract(root);actual=json.loads((root/CH).read_bytes());ch=actual if ch is None else ch;need(same(ch,actual),'呼叫章與現行章不符')
 try:from scripts.wyd_song051_yixin import project_previous_phase
 except ImportError:from wyd_song051_yixin import project_previous_phase
 ch=project_previous_phase(root,ch)
 roles=collect_roles(ch,c);need(same(ch,phase_chapter(c,roles)),'完整原文/位置/資格或49錨不符')
 expected=resolve_existing(root,c);need(all(roles[k]==v for k,v in expected.items()if k in roles),'跨篇現役角色不同號');roles.update(expected);need(len(set(roles.values()))==len(roles),'祖父與後代角色不得混號')
 temple_contract=copy.deepcopy(c);temple_contract['existing_seeds']=[c['temple_identity_seed']];need(resolve_existing(root,temple_contract).get('temple_identity_candidate')==roles['taizu'],'太祖與義隆同指未閉合')
 intro=json.loads((root/INTRO_CH).read_bytes());need(same(intro,intro_chapter(c,roles)),'005完整轉錄/位置/有限14錨漂移')
 try:from scripts.fixed_wuyingdian_song005_opening import validate_source as validate_intro
 except ImportError:from fixed_wuyingdian_song005_opening import validate_source as validate_intro
 validate_intro(c['song005_opening_bridge']['source_before'],root)
 people={p['id']:p for p in json.loads((root/'registry/persons.json').read_bytes())['persons']}
 for p in ch['paragraphs']+intro['paragraphs']:
  owner=ch if p['id'].startswith(CID+':')else intro
  for m in p['mentions']:
   person=people.get(m['person_id']);need(bool(person),'人物未登記')
   need(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'缺反向alias')
   e=dict(work_id=owner['work_id'],book_id=owner['book_id'],source_id=owner['source_id'],chapter_id=owner['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(e in person['evidence'],'缺反向evidence')
 # The original pending validator is unchanged; normalize only after exact formal proof.
 try:from scripts.fixed_wuyingdian_song051 import validate_source
 except ImportError:from fixed_wuyingdian_song051 import validate_source
 validate_source(c['source_before'],root)
 family_projection_valid(root,ch,roles)
 facts=assertions(ch,roles);ns=names(ch,roles,c,root)
 if check_sidecars:
  need(same(json.loads((root/INTRO_FACTS).read_bytes()),intro_facts(c,roles)),'005明父表漂移')
  need(same(json.loads((root/INTRO_IDENTITIES).read_bytes()),intro_identities(c,roles,root)),'005傳首五角色身份證據漂移')
  need(same(json.loads((root/FACTS).read_bytes()),facts),'本批親屬表或主語方向不符')
  need(same(json.loads((root/NAMES).read_bytes()),ns),'本批姓名表不符')
  for rel,doc in full_seed_docs(root,c,roles).items():need(same(json.loads((root/rel).read_bytes()),doc),'外部全名種子表不符')
  need(same(json.loads((root/IDENTITIES).read_bytes()),identities(ch,roles,c,root)),'本批身份或兩個2的來源讀法不符')
 return ch,roles,c,facts,ns


def _yixin_module():
 try:from scripts import wyd_song051_yixin as y
 except ImportError:import wyd_song051_yixin as y
 return y
@memoized(0)
def context(root,ch=None,check_sidecars=True):
 read_contract(root)
 actual=json.loads((Path(root)/CH).read_bytes())
 if _yixin_module().has_phase(actual):return _phase2_context(root,ch,check_sidecars)
 return _phase1_context(root,ch,check_sidecars)
def applies(a):
 return (isinstance(a,dict)and str(a.get('id','')).startswith('a-song051-yixin-'))or _phase1_applies(a)
def family_valid(a,paragraphs,chapters,root):
 if isinstance(a,dict)and str(a.get('id','')).startswith('a-song051-yixin-'):return _yixin_module().family_valid(a,paragraphs,chapters,root)
 try:
  actual=json.loads((Path(root)/CH).read_bytes())
  if _yixin_module().has_phase(actual)and CID in chapters:paragraphs,chapters=_yixin_module().previous_frames(root,paragraphs,chapters)
  return _phase1_family_valid(a,paragraphs,chapters,root)
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False
def component_valid(n,ch,root):
 if not isinstance(n,dict):return False
 if isinstance(n.get('component_source_binding'),dict)and n['component_source_binding'].get('kind')=='fixed_wyd_song051_yixin_name_component':return _yixin_module().component_valid(n,ch,root)
 try:
  if isinstance(ch,dict)and ch.get('id')==CID and _yixin_module().has_phase(json.loads((Path(root)/CH).read_bytes())):ch=_yixin_module().project_previous_phase(root,ch)
  return _phase1_component_valid(n,ch,root)
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False
def validate_surname(n,all_names,chapters,all_assertions,root):
 try:
  actual=json.loads((Path(root)/CH).read_bytes())
  if _yixin_module().has_phase(actual):
   projected=_yixin_module().project_previous_phase(root,chapters.get(CID));chapters=copy.copy(chapters);chapters[CID]=projected
  return _phase1_validate_surname(n,all_names,chapters,all_assertions,root)
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):raise ValueError('宋051氏姓須有晉099逐字全名、041雙父證及本源有限父系路徑，不借ID/母嗣系或省略推定步')
def guard_bundle(root,person_id,people,records):
 _phase1_guard_bundle(root,person_id,people,records)
 _yixin_module().guard_bundle(root,person_id,people,records)
