"""Finite complete Yixin unit; explicit additions project to the unchanged 49-anchor phase."""
from pathlib import Path
import json,copy,hashlib
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
CH='corpus/songshu/051-wyd1739.json';CID='c-songshu-051-wyd1739-zongshi';REF='source-evidence/song051-wyd1739-zongshi/yixin-complete-unit-contract.json';PHASE='song051_yixin_complete_unit_phase2';CONTRACT_SHA='8e3ed53fa092ee1376dcc14ba8e0f5a6243a364d63466fa1c2d49eb58f93ee7b'
def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return all(type(k)is str for k in a)and all(type(k)is str for k in b)and set(a)==set(b)and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 if a is None or type(a)in(str,int,bool):return a==b
 if type(a)is float:
  try:return json.dumps(a,allow_nan=False)==json.dumps(b,allow_nan=False)
  except ValueError:return False
 return False
def need(ok,msg):
 if not ok:raise ValueError('武英殿宋051義欣完整單元：'+msg)
def load(root,rel):
 root=Path(root).resolve();p=(root/rel).resolve();need(p.is_relative_to(root),'檔案越界');return json.loads(p.read_bytes())
def contract(root):
 root=Path(root).resolve();p=(root/REF).resolve();need(p.is_relative_to(root/'source-evidence'),'契約路徑');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==CONTRACT_SHA,'契約SHA');return json.loads(raw)
def materialize(v,roles):
 if type(v)is dict:
  if set(v)=={'$role'}:return roles[v['$role']]
  return{k:materialize(x,roles)for k,x in v.items()}
 if type(v)is list:return[materialize(x,roles)for x in v]
 return v
def has_phase(ch):return type(ch)is dict and type(ch.get('annotation'))is dict and 'additional_annotation_phase'in ch['annotation']
def phase_chapter(c,roles):
 ch=materialize(c['base_source_template'],roles);ch['annotation']['additional_annotation_phase']={'kind':PHASE,'contract_path':REF,'coverage':c['coverage'],'human_reviewed':False,'model':None}
 for row in c['markers']:
  p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m=materialize(row['marker'],roles);need(not any(x['id']==m['id']for x in p['mentions']),'新增MID碰撞');p['mentions'].append(m);p['mentions'].sort(key=lambda x:x['start']);p['annotation_status']='in_progress'
 for row in c.get('referenced_work_markers',[])+c.get('unresolved_source_markers',[])+c.get('non_person_markers',[]):
  p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m=materialize(row['marker'],roles);need(not any(x['id']==m['id']for x in p['mentions']),'書題MID碰撞');p['mentions'].append(m);p['mentions'].sort(key=lambda x:x['start']);p['annotation_status']='in_progress'
 if c.get('age_order_conflicts'):ch['annotation']['source_age_order_decision_refs']=[{'id':d['id'],'source_contract_path':REF,'affected_relation_ids':d['affected_relation_ids']}for d in c['age_order_conflicts']]
 return ch
def collect(ch,c):
 roles={}
 for row in c['base_role_mentions']+c['markers']:
  mid=row.get('mention_id')or row['marker']['id'];p=next(p for p in ch['paragraphs']if p['id']==row['paragraph_id']);m,=[m for m in p['mentions']if m['id']==mid];role=row['role_key'];pid=m.get('person_id');need(type(pid)is str and pid,'角色PID');need(role not in roles or roles[role]==pid,'角色跨錨不同號');roles[role]=pid
 return roles
def resolve_seeds(root,c):
 rows=load(root,'registry/persons.json')['persons'];people={p['id']:p for p in rows};need(len(people)==len(rows),'種子registry重複ID');roles={}
 for s in c['existing_seeds']:
  ch=load(root,s['path']);need(all(ch.get(k)==s[k]for k in('work_id','book_id','source_id','chapter_id')if k!='chapter_id')and ch['id']==s['chapter_id'],'種子維度');need(hashlib.sha256(json.dumps(ch['source'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==s['source_metadata_sha256'],'種子來源資格')
  metadata=ch['source'];rp=metadata.get('raw_path')or metadata.get('raw_file')or s.get('source_raw_witness_path');hs=metadata.get('raw_file_sha256')or metadata.get('raw_sha256')
  if rp is not None or hs is not None:
   need(type(rp)is str and rp and type(hs)is str and len(hs)==64,'種子raw資格');f=(Path(root)/rp).resolve();need(f.is_relative_to(Path(root).resolve()),'種子raw越界');need(hashlib.sha256(f.read_bytes()).hexdigest()==hs,'種子rawSHA')
  p=next(p for p in ch['paragraphs']if p['id']==s['paragraph_id']);need(p['text']==s['full_paragraph']['text']and hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_text_sha256'],'種子完整段');m,=[m for m in p['mentions']if m['id']==s['mention_id']];need(m['kind']=='person'and m['surface']==s['surface']and p['text'][m['start']:m['end']]==s['surface'],'種子MID原字');pid=m['person_id'];person=people.get(pid);need(person is not None,'種子未登記');need(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'種子反向alias');need(any(e['mention_id']==m['id']and e['paragraph_id']==p['id']and e['quote']==m['surface']for e in person['evidence']),'種子反向evidence');roles[s['role_key']]=pid
 return roles
@memoized(0)
def state(root,ch=None):
 root=Path(root).resolve();actual=load(root,CH);need(ch is None or same(ch,actual),'所給current完整章不符');c=contract(root);roles=collect(actual,c);need(same(actual,phase_chapter(c,roles)),'完整原文/舊新錨/資格/位置或新增metadata差異');seeds=resolve_seeds(root,c);need(all(roles[k]==v for k,v in seeds.items()),'既有人物跨源角色錯接');need(roles['yixin']==roles['old_yixin']and roles['wendi']==roles['old_taizu'],'既有角色被另造');need(len({roles[r]for r in c['new_names']})==len(c['new_names']),'本源不同個體不得同號');need(not({roles[r]for r in c['new_names']}&(set(seeds.values())|{v for k,v in roles.items()if k.startswith('old_')})),'新角色與既有人物錯合')
 rows=load(root,'registry/persons.json')['persons'];people={p['id']:p for p in rows};need(len(people)==len(rows),'current registry重複ID')
 for row in c['markers']:
  p=next(p for p in actual['paragraphs']if p['id']==row['paragraph_id']);m=next(m for m in p['mentions']if m['id']==row['marker']['id']);person=people.get(m['person_id']);need(person is not None,'新增角色未登記');need(m['kind']=='pronoun' or any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'新增alias缺反向');e={k:actual[k]for k in('work_id','book_id','source_id')};e.update(chapter_id=CID,paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(e in person['evidence'],'新增evidence缺反向')
 docs={rel:materialize(v,roles)for rel,v in c['expected_documents'].items()}
 for rel,expected in docs.items():need(same(load(root,rel),expected),'新人物/姓名/親屬sidecar不符：'+rel)
 family=next(f for f in load(root,'registry/family-assemblies.json')['assemblies']if f['id']=='family-song041-qiao');rows={r['person_id']:r for r in family['members']};need(len(rows)==len(family['members']),'家系重複')
 for expected in materialize(c['expected_family_members'],roles):need(same(rows.get(expected['person_id']),expected),'新近系明父/推定父行不符')
 # Names rely on already checked source-based Liu components, not labels or structural IDs.
 old_names=load(root,'corpus/songshu/051-wyd1739-name-components.json')['records']
 for role in ['yixin','yizong']:
  n,=[n for n in old_names if n['id']=='name-song051-phase1-restored-'+role];need(n['person_id']==roles['old_'+role]and n['surname']=='劉'and n['surname_basis']['kind']=='contextual_surname_from_wyd_song051_named_path','劉姓既有源證種子不符')
 validate_added_context(root,roles,c,docs)
 validate_annotation_corrections(root,actual,roles,c,docs)
 validate_appellation_fragment_groups(actual,roles,c)
 return actual,roles,c,docs

def project_previous_phase(root,ch):
 need(type(ch)is dict,'投影須提供完整current章，不以None或缺章回填')
 actual,roles,c,docs=state(root,ch);return materialize(c['base_source_template'],roles)
def previous_frames(root,paragraphs,chapters):
 actual,roles,c,docs=state(root);given=chapters.get(CID);need(same(given,actual),'親屬所給完整current章不符');projected=materialize(c['base_source_template'],roles);pp=copy.copy(paragraphs);cc=copy.copy(chapters);cc[CID]=projected
 for p in actual['paragraphs']:
  if p['id']in paragraphs:need(type(paragraphs[p['id']])is tuple and len(paragraphs[p['id']])==2 and paragraphs[p['id']][0]==CID and same(paragraphs[p['id']][1],p),'親屬所給current原段不符');pp[p['id']]=(CID,next(x for x in projected['paragraphs']if x['id']==p['id']))
 return pp,cc

def family_valid(a,paragraphs,chapters,root):
 try:
  try:from scripts import fixed_wuyingdian_song051_family_phase as core
  except ImportError:import fixed_wuyingdian_song051_family_phase as core
  core.context(root);ch,roles,c,docs=state(root);need(any(same(a,x)for d in docs.values()for x in d.get('assertions',[])),'非本源明親屬');need(same(chapters.get(CID),ch),'親屬章不同')
  for e in a['evidence']:
   p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);frame=paragraphs.get(p['id']);need(type(frame)is tuple and len(frame)==2 and frame[0]==CID and same(frame[1],p),'親屬段不同')
  return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

def _component_json(value):
 # Reuse the scope key's exact JSON shape rule; unknown fields participate.
 try:from scripts.validation_context import _json_tree
 except ImportError:from validation_context import _json_tree
 need(_json_tree(value),'姓名比較只准完整JSON值')
 return json.dumps(value,ensure_ascii=False,sort_keys=True,allow_nan=False,separators=(',',':'))

@memoized(0)
def _proven_component_index(root):
 # A compact consequence of both complete proofs, never a replacement witness.
 try:from scripts import fixed_wuyingdian_song051_family_phase as core
 except ImportError:import fixed_wuyingdian_song051_family_phase as core
 core.context(root)
 actual,roles,c,docs=state(root,load(root,CH))
 return {'chapter':_component_json(actual),
         'records':[_component_json(x)for d in docs.values()for x in d.get('records',[])]}

def component_valid(n,ch,root):
 try:
  need(type(ch)is dict,'姓名須提供完整current章')
  index=_proven_component_index(root)
  return _component_json(ch)==index['chapter']and _component_json(n)in index['records']
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root):
 need(type(chapters)is dict and type(names)is list and type(assertions)is list,'姓名catalog須完整章map及JSON lists')
 actual,roles,c,docs=state(root);need(component_valid(n,chapters.get(CID),root),'姓名完整源證');expected=next(x for d in docs.values()for x in d.get('records',[])if x['id']==n['id']);need('surname_basis'in expected,'非復原姓氏行');need(sum(same(x,n)for x in names)==1,'姓名catalog缺漏/重複');source=load(root,'corpus/songshu/051-wyd1739-name-components.json')['records']
 if 'source_name_record_path'in n['surname_basis']:
  path=n['surname_basis']['source_name_record_path'];need(path in docs and docs[path].get('record_type')=='person_name_component_set','推姓新種子只允本fixed contract逐字姓名文件');source=docs[path]['records']
 seed=next(x for x in source if x['id']==n['surname_basis']['source_name_record_id']);need(sum(same(x,seed)for x in names)==1,'缺原劉姓證據');aa=[a for d in docs.values()for a in d.get('assertions',[])]
 for aid in n['surname_basis']['source_assertion_ids']:
  a=next(a for a in aa if a['id']==aid);need(sum(same(x,a)for x in assertions)==1,'姓氏路徑親屬catalog不全/重複')
 return True

def guard_bundle(root,pid,people,records):
 candidate=people.get(pid)
 registered=isinstance(candidate,dict)and any(e.get('chapter_id')==CID for e in candidate.get('evidence',[]))
 source_records=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID]
 source_relevant=any(m.get('person_id')==pid for source in source_records for p in source.get('paragraphs',[])for m in p.get('mentions',[]))
 if not registered and not source_relevant:return
 ch=load(root,CH)
 if not has_phase(ch):return
 actual,roles,c,docs=state(root);registered={p['id']:p for p in load(root,'registry/persons.json')['persons']};need(same(people.get(pid),registered.get(pid)),'bundle現行人物不符')
 for rel,expected in docs.items():need(sum(same(r,expected)for r in records)==1,'bundle新完整人物/親屬/名字資料缺漏或重複')

# Appended to the existing finite051 module, not a second per-unit dispatcher.
def validate_added_context(root,roles,c,docs):
 for witness in c.get('comparative_reference_witnesses',[]):
  for f in witness['files']:
   p=(Path(root)/f['path']).resolve();need(p.is_relative_to(Path(root).resolve()/'source-evidence'),'比較源路徑');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==f['sha256'],'比較源原bytes')
  raw=(Path(root)/witness['files'][0]['path']).read_bytes();a,b=witness['complete_unit_line_range'];unit=b''.join(raw.splitlines(keepends=True)[a-1:b]);need(hashlib.sha256(unit).hexdigest()==witness['complete_unit_raw_sha256'],'比較完整單元範圍')
  ordinal=witness['reported_son_ordinal'];anchor=ordinal['reference_anchor'];line=raw.decode().splitlines()[anchor['raw_line_1based']-1];need(line[anchor['start']:anchor['end']]==anchor['surface']and line[anchor['ordinal_start']:anchor['ordinal_end']]==anchor['ordinal_surface']=='二'and type(ordinal['value'])is int and ordinal['value']==2,'比較源第二男原字/數值');need(ordinal['adopted_as_preferred_birth_order']is False and ordinal['preferred_ordinal']is None,'比較所報二不可暗作首選/總子數')
 for f in c.get('comparison_reference_files',[]):
  p=(Path(root)/f['path']).resolve();need(p.is_relative_to(Path(root).resolve()/'source-evidence')and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],'比較錄文/版本metadata SHA')
 for group in c.get('expected_additional_family_groups',[]):
  family=next(f for f in load(root,'registry/family-assemblies.json')['assemblies']if f['id']==group['assembly_id']);rows={r['person_id']:r for r in family['members']};need(len(rows)==len(family['members']),'附加家系重號')
  for expected in materialize(group['members'],roles):need(same(rows.get(expected['person_id']),expected),'附加明女家系行不符')
 for spec in c.get('external_literal_name_records',[]):
  seed=next(s for s in c['existing_seeds']if s['role_key']==spec['seed_role']);n=next(n for d in docs.values()for n in d.get('records',[])if n['id']==spec['record_id']);need(n['person_id']==roles[spec['seed_role']]and n['surname']+n['ming']==seed['surface']and n['person_mention_id']==seed['mention_id']and n['chapter_id']==seed['chapter_id']and n['paragraph_id']==seed['paragraph_id']and n['quote']==seed['full_paragraph']['text'],'外源逐字全名須與已驗MID一致，不借label')
 if c.get('excluded_identity_seeds'):
  excluded=resolve_seeds(root,{'existing_seeds':c['excluded_identity_seeds']})
  for s in c['excluded_identity_seeds']:need(roles[s['excluded_target_role']]!=excluded[s['role_key']],'反候選原完整來源人物不可截名誤接')
 for s in c.get('supporting_identity_seeds',[]):
  supporting=resolve_seeds(root,{'existing_seeds':[s]});need(roles[s['role_key']]==supporting[s['role_key']],'平行身份正證角色不符')
 validated_yiqing_context(root,load(root,CH),roles,c,docs)
 validated_age_order_decisions(roles,c,docs)

def validated_age_order_decisions(roles,c,docs):
 cases=materialize(c.get('age_order_conflicts',[]),roles);assertions={a['id']:a for d in docs.values()for a in d.get('assertions',[])};seen=set()
 for case in cases:
  need(case['kind']=='source_bound_agnatic_age_order_cycle'and case['status']=='unresolved'and case['preferred_interpretation']is None and case['human_reviewed']is False,'父系年序分歧資格');edges=case['cycle_edges'];need(type(edges)is list and len(edges)==7 and len(case['person_ids'])==7 and len(set(case['person_ids']))==7,'七人七邊環');affected=case['affected_relation_ids'];need(len(affected)==2 and len(set(affected))==2 and not seen.intersection(affected),'只兩跨支年序不施加');seen.update(affected);direct=[];collateral=[]
  for edge in edges:
   a=assertions[edge['assertion_id']];need(edge['operator']=='lt'and edge['older_person_id']!=edge['younger_person_id'],'年序邊方向');q=a['qualifiers']
   if a['predicate']=='brother':
    r=q['relative_birth_order'];need(r['older_person_id']==edge['older_person_id']and r['younger_person_id']==edge['younger_person_id']and r['operator']=='lt'and r['scope']=='siblings','明兄弟原年序不得改');direct.append(a['id'])
   elif a['predicate']=='agnatic_cousin':
    k=q['kinship_structure'];need(k['lineage']=='paternal'and type(k['generation_difference'])is int and k['generation_difference']==0 and k['subject_relative_age']=='younger'and a['object_person_id']==edge['older_person_id']and a['subject_person_id']==edge['younger_person_id'],'從弟須保原父系同代/年幼原報');collateral.append(a['id'])
   else:need(False,'非此源父系年序類型')
  need(len(direct)==5 and set(collateral)==set(affected)and direct==case['preserved_direct_brother_assertion_ids'],'不壓直接兄弟或別的源約束');need({e['older_person_id']for e in edges}=={e['younger_person_id']for e in edges}==set(case['person_ids']),'環端點不閉合');need(all(edges[i]['younger_person_id']==edges[(i+1)%7]['older_person_id']for i in range(7)),'原方向未成同一七邊環');need([claim['assertion_id']for claim in case['source_claims']]==affected,'兩原從弟源ID')
  for claim in case['source_claims']:
   a=assertions[claim['assertion_id']];need(claim['source_subject_person_id']==a['subject_person_id']and claim['source_object_person_id']==a['object_person_id']and claim['source_subject_relative_age']=='younger'and same(claim['evidence'],a['evidence']),'兩原從弟端點/原證不符')
 return cases

def source_age_order_decisions(root,person_ids,people,records):
 # Ordinary unrelated/synthetic catalogs do not trigger any filesystem read.
 if not any(any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[]))for pid in person_ids):return []
 actual,roles,c,docs=state(root)
 if not c.get('age_order_conflicts'):return []
 need(sum(same(r,actual)for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID)==1,'年序取捨須有唯一完整current正文，不信刪改的傳入metadata')
 return[copy.deepcopy(d)for d in validated_age_order_decisions(roles,c,docs)if person_ids.intersection(d['person_ids'])]

def preferred_source_age_relation(assertion,decisions):
 result=copy.deepcopy(assertion);d=next((d for d in decisions if assertion['id']in d['affected_relation_ids']),None)
 if d is not None:
  need(result['predicate']=='agnatic_cousin'and d['status']=='unresolved','只限有驗兩從弟年序');result['qualifiers'].pop('relative_birth_order',None);result['qualifiers']['kinship_structure']['subject_relative_age']='unknown';result['relative_age_decision_ref']={'id':d['id'],'status':'unresolved','source_contract_path':REF,'affected_relation_ids':copy.deepcopy(d['affected_relation_ids'])}
 return result


def unsplit_name_valid(n,paragraph,chapter,root):
 try:
  need(type(n)is dict and type(paragraph)is dict and type(chapter)is dict and root is not None,'未分姓名完整參數')
  actual,roles,c,docs=state(root,chapter);need(component_valid(n,chapter,root),'未分姓名完整row')
  b,=[b for b in c.get('received_unsplit_name_bindings',[])if b['record_id']==n['id']]
  need(n.get('surname')is None and n.get('ming')is None and n.get('full_name')==b['value'] and n['full_name_basis']['source_term']==b['value'],'未分姓名原值/不得暗拆漢姓')
  parts=b['fragments'];need(type(parts)is list and 1<=len(parts)<=2,'完整原稱片數');joined='';indices=[]
  for a in parts:
   index=next(i for i,p in enumerate(actual['paragraphs'])if p['id']==a['paragraph_id']);p=actual['paragraphs'][index];m,=[m for m in p['mentions']if m['id']==a['mention_id']]
   need(m.get('kind')=='person'and m.get('person_id')==n['person_id']==roles[b['role_key']]and all(m[k]==a[k]for k in('start','end','surface'))and p['text'][a['start']:a['end']]==a['surface'],'未分姓名人物/原片錯接');joined+=a['surface'];indices.append(index)
  need(joined==b['value'] and n['paragraph_id']==parts[0]['paragraph_id'] and same(paragraph,actual['paragraphs'][indices[0]]),'完整原稱/主段')
  if len(parts)==2:need(indices[1]==indices[0]+1 and parts[0]['end']==len(actual['paragraphs'][indices[0]]['text'])and parts[1]['start']==0,'跨段姓名必相鄰末首連續')
  return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

def childhood_apposition_valid(n,paragraph,chapter,root):
 try:
  need(type(n)is dict and type(paragraph)is dict and type(chapter)is dict and root is not None,'小字完整參數');actual,roles,c,docs=state(root,chapter);need(component_valid(n,chapter,root),'小字完整row')
  b=n['xiaozhi_basis'];need(n['quote']==paragraph['text']and n['paragraph_id']==paragraph['id'],'小字完整原段');aa=[b[k]for k in('value_anchor','subject_anchor','marker_anchor')]
  for i,a in enumerate(aa):
   need(a['paragraph_id']==paragraph['id']and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(paragraph['text'])and paragraph['text'][a['start']:a['end']]==a['surface'],'小字錨位置')
   if i<2:
    m,=[m for m in paragraph['mentions']if m['id']==a['person_mention_id']];need(m.get('kind')=='person'and m['person_id']==n['person_id']and all(m[k]==a[k]for k in('start','end','surface')),'小字同人雙錨')
  v,s,m=aa;need(v['person_mention_id']!=s['person_mention_id']and v['surface']==n['xiaozhi']and v['end']==s['start']and s['end']==m['start']and m['surface']=='小字','小字雙錨順序')
  term=n['xiaozhi']+s['surface']+'小字也';need(b['source_term']==term and paragraph['text'][v['start']:m['end']+1]==term,'小字精確值主語小字也');return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

# This text is appended to the existing finite051 module, not loaded as a new handler.
def validated_yiqing_context(root,actual,roles,c,docs):
 ps={p['id']:p for p in actual['paragraphs']};ordered=[p['id']for p in actual['paragraphs']]
 records={n['id']:n for d in docs.values()for n in d.get('records',[])}
 for b in materialize(c.get('courtesy_fragment_groups',[]),roles):
  n=records[b['record_id']];need(n['person_id']==roles[b['role']]and n['zi']==b['value'],'跨頁字owner/value')
  fs=b['fragments'];need(type(fs)is list and len(fs)==2,'只兩相鄰字片')
  for f in fs:
   p=ps[f['paragraph_id']];m=next(m for m in p['mentions']if m['id']==f['id']);expected={k:v for k,v in f.items()if k!='paragraph_id'};need(same(m,expected)and m['person_id']==roles[b['role']]and m['kind']=='person','跨頁字錨/owner');need(type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface'],'跨頁字位置')
  first,last=fs;need(ordered.index(last['paragraph_id'])==ordered.index(first['paragraph_id'])+1 and first['end']==len(ps[first['paragraph_id']]['text'])and last['start']==0,'跨頁字須真正相鄰尾首');need(first['surface']+last['surface']==b['value'],'跨頁字順序')
  z=b['zi_marker'];owner=b['owner_anchor'];p=ps[first['paragraph_id']];need(z['paragraph_id']==first['paragraph_id']==owner['paragraph_id']and z['start']==first['start']-1 and z['end']==first['start']and z['surface']==p['text'][z['start']:z['end']]=='字','跨頁字標誌');m=next(m for m in p['mentions']if m['id']==owner['id']);need(m['person_id']==roles[b['role']]and m['end']==z['start']and same(m,{k:v for k,v in owner.items()if k!='paragraph_id'}),'跨頁字具名主語');need(any(ref.get('quote')=='字'+b['value']for ref in n.get('references',[])),'跨頁字連讀引用')
 for b in c.get('reference_supported_name_components',[]):
  n=records[b['record_id']];literal=records[b['literal_record_id']];need(n['person_id']==literal['person_id']==roles[b['role']]and literal['ming']is None,'外證復原須留本源省稱');need(n['surname']==b['surname']and n['ming']==b['ming']and n.get('zi')==b['zi']and n['component_source_binding']['name_form']=='reference_restored_full_name','外證姓名分件')
  raw=(Path(root)/b['reference_unit_path']).read_bytes();meta_raw=(Path(root)/b['metadata_path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==b['reference_unit_sha256']and hashlib.sha256(meta_raw).hexdigest()==b['metadata_sha256'],'外證全單元/資格SHA');meta=json.loads(meta_raw);source=meta['source'];need(type(source['revision_id'])is int and source['revision_id']==b['revision_id']and type(source['url'])is str and source['url']and source['raw_sha256'],'外證固定修訂資格');need(meta['edition']is None and meta['image_verified']is False and meta['human_reviewed']is False,'外證印本及AI資格不得升格');text=raw.decode();a=b['reference_head_anchor'];need(type(a['start'])is int and type(a['end'])is int and text[a['start']:a['end']]==a['surface']==n['surname']+n['ming'],'外證傳首逐字姓名');q=b['reference_head_projection'];need(a['start']==q['start']+len('{{ProperNoun|')and a['end']==a['start']+len(n['surname']+n['ming'])and text[q['start']:q['end']]==q['raw_text']and q['raw_text'].startswith('{{ProperNoun|'+a['surface']+'}}，字')and q['raw_text'].replace('{{ProperNoun|','').replace('}}','')==q['display_text']and n['references'][0]['quote']==q['display_text']and '，字'+n['zi']+'，'in q['display_text'],'外證傳首正文而非編輯heading/精確標記去除');p=ps[n['paragraph_id']];m=next(m for m in p['mentions']if m['id']==n['person_mention_id']);need(m['person_id']==roles[b['role']]and m['surface'].startswith(n['surname'])and n['quote']==p['text'],'外證本源owner/姓氏錨');need(b['qualification']=='reference_restored_not_main_literal','外證不冒原文明全名')
 for row in c.get('unresolved_source_markers',[]):
  p=ps[row['paragraph_id']];m=row['marker'];need(m in p['mentions']and m['kind']=='unresolved'and m['person_id']is None and m['status']=='unresolved'and p['text'][m['start']:m['end']]==m['surface']and m['reason'],'未裁定引古稱謂須明留原字/理由，不暗選人物')
 works={w['id']:w for w in load(root,'registry/works.json')['works']}
 for row in c.get('referenced_work_markers',[]):
  p=ps[row['paragraph_id']];m=row['marker'];need(m in p['mentions']and m['kind']=='work'and p['text'][m['start']:m['end']]==m['surface'],'書題原錨');w=works[m['work_id']];need(w.get('citation_title',w['title'])==m['surface'],'書題正式題');need(any(e.get('chapter_id')==CID and e.get('paragraph_id')==p['id']and e.get('mention_id')==m['id']and e.get('quote')==p['text']for e in w.get('reference_attestations',[])),'書題反向引用')
 for b in materialize(c.get('source_work_author_bindings',[]),roles):
  p=ps[b['paragraph_id']];w=works[b['work_id']];need(b['attribution']in w.get('source_author_attributions',[]),'書作者反向依據');a=next(m for m in p['mentions']if m['id']==b['author_mention_id']);m=b['work_marker'];need(a['person_id']==roles[b['author_role']]and a['surface']==b['author_surface']and m in p['mentions']and p['text']==b['full_paragraph'],'書作者完整來源/角色');pred=b['predicate'];need(p['text'][pred['start']:pred['end']]==pred['surface']and pred['end']==m['start'],'書作者撰為原詞')
  if b['case']in ['xuzhou-xianxian','dianxu']:
   aside=b['interpolated_comparison'];subject=b['subject_clause'];resumed=b['resumed_clause'];need(a['start']==subject['start']and subject['end']==aside['start']and aside['end']==resumed['start']and resumed['end']==m['start'],'撰書主語/插敘/回接位置');need(all(p['text'][x['start']:x['end']]==x['text']for x in [aside,subject,resumed]),'插敘完整字串');need(aside['text']=='先是王弘為江州亦有此制'and subject['text'].startswith('義慶留心撫物')and resumed['text'].startswith('在州八年為西土所安'),'插敘王弘不得接成作者')
  if b['case']=='xuzhou-xianxian':need(pred['surface']=='撰','先賢傳明撰')
  elif b['case']=='dianxu':
   q=b['imitation_clause'];need(p['text'][q['start']:q['end']]==q['text']=='又擬班固典引為'and pred['surface']=='為','典敘模仿主語與為');need(q['model_author_role']!=b['author_role'],'典引作者非典敘作者')
  elif b['case']=='heqing-song':need(pred['surface']=='為'and a['end']==pred['start']and p['text'][m['end']:m['end']+7]=='其序甚工其辭曰','照為頌直接原句')
  elif b['case']=='dianyin':need(pred['surface']==''and a['end']==m['start']and p['text'][a['start']-2:a['start']]=='又擬','班固典引嵌入模仿句')
  else:need(False,'未列書作者case')

def work_author_valid(ev,work,chapter,root):
 try:
  need(root is not None and type(chapter)is dict,'書作者須真完整來源與root');actual,roles,c,docs=state(root,chapter);w=next(w for w in load(root,'registry/works.json')['works']if w['id']==work['id']);need(same(work,w),'書作者current作品不同');bindings=materialize(c.get('source_work_author_bindings',[]),roles);need(any(same(ev,b['attribution'])and b['work_id']==work['id']for b in bindings),'書作者非本契約明列');return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

def preferred_name_reading_errors(reading,names,chapters,root):
 try:
  need(root is not None and type(names)is list and type(chapters)is dict,'同章姓名選讀須有真root/catalog');actual,roles,c,docs=state(root);need(same(chapters.get(CID),actual),'同章姓名選讀完整current章不同')
  cases=c.get('source_name_display_preferences',[]);case=next(b for b in cases if b['reading_id']==reading['id']);expected=next(r for r in docs[case['document_path']]['readings']if r['id']==case['reading_id']);need(same(reading,expected)and reading['person_id']==roles[case['role']],'同章姓名選讀不是契約列明值')
  need(reading['field']=='ming'and reading['preferred_value']=='曄'and reading['source_values']==['曄','燁']and reading['coverage']=='listed_records_only'and reading['status']=='editorial_provisional'and reading['human_reviewed']is False,'同章姓名選讀資格')
  def locator(n):return{k:n.get(k)for k in ['id','person_id','chapter_id','paragraph_id','surname','ming','quote']}
  actual_records=[locator(n)for n in names if n.get('person_id')==reading['person_id']and n.get('ming')in reading['source_values']];listed=[ref['record']for ref in reading['records']];need(len(actual_records)==len(listed)and all(sum(same(n,x)for x in actual_records)==1 for n in listed),'同章姓名選讀不可漏列/重複原record');paragraphs={p['id']:p for p in actual['paragraphs']};ordered=[p['id']for p in actual['paragraphs']];indices=[]
  for ref in reading['records']:
   n=ref['record'];p=paragraphs[n['paragraph_id']];m=next(m for m in p['mentions']if m['id']==ref['anchor']['id']);need(same(m,ref['anchor'])and m['person_id']==reading['person_id']and n['chapter_id']==CID and ref['source_id']==actual['source_id']and n['quote']==p['text']and n['ming']in m['surface'],'同章姓名選讀完整段/雙端/原字');indices.append(ordered.index(p['id']))
  need(max(indices)-min(indices)==1 and len(set(indices))==2,'限同傳真正相鄰兩段');need(reading['basis']['kind']=='source_bound_wyd_song051_adjacent_name_variant','同章姓名選讀新kind資格');return []
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return ['武英殿宋051同章相鄰姓名顯示選讀須核完整current源及列明原字records，不得改字或代替身份判斷']

def source_name_fragments(root,person_ids,people,records):
 # Never read the finite source for unrelated or synthetic people.
 if not any(any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[]))for pid in person_ids):return []
 actual,roles,c,docs=state(root);registered={p['id']:p for p in load(root,'registry/persons.json')['persons']};need(all(same(people.get(pid),registered.get(pid))for pid in person_ids),'姓名片段current人物不符');need(sum(same(r,actual)for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID)==1,'姓名片段須唯一完整current正文')
 result=[]
 for b in materialize(c.get('courtesy_fragment_groups',[]),roles):
  pid=roles[b['role']]
  if pid not in person_ids:continue
  n=next(n for d in docs.values()for n in d.get('records',[])if n['id']==b['record_id']);need(n['person_id']==pid and n.get('zi')==b['value'],'姓名片段完整字號record')
  result.append({'kind':'source_bound_name_fragment_group','person_id':pid,'source_id':actual['source_id'],'chapter_id':CID,'mention_ids':[f['id']for f in b['fragments']],'fragments':b['fragments'],'complete_component':{'record_id':b['record_id'],'field':'zi','value':b['value']},'status':'contextual_provisional','human_reviewed':False,'source_mentions_and_registry_aliases_retained':True})
 return result

# fixed-c51-annotation-corrections: ordinary office component and cited courtesy-name actor.
def validate_annotation_corrections(root,actual,roles,c,docs):
 ps={p['id']:p for p in actual['paragraphs']};people=load(root,'registry/persons.json')['persons']
 for row in c.get('non_person_markers',[]):
  p=ps[row['paragraph_id']];m=row['marker'];b=row['source_binding'];need(p['text']==b['full_paragraph']and m in p['mentions'],'非人物須完整原段及固定錨');need(m['kind']=='non_person'and m['person_id']is None and m['status']=='contextual_provisional'and m['lexical_role']=='office_title_component'and m['human_reviewed']is False,'非人物處置型別');need(m['source_context_binding']=={'kind':'received_wyd_complete_unit_office_component','contract_path':REF},'非人物可信入口');need(p['text'][m['start']:m['end']]==m['surface']and m['end']==m['start']+len(m['surface']),'非人物原字位置')
  o=b['office_anchor'];v=b['appointment_verb'];s=b['recipient_anchor'];need(p['text'][o['start']:o['end']]==o['surface']and o['start']==m['start']and o['surface'].startswith(m['surface']),'整官名及首字');need(p['text'][v['start']:v['end']]==v['surface']=='為'and v['end']==o['start'],'授職語法');owner=next(x for x in p['mentions']if x['id']==s['mention_id']);need(owner['kind']=='person'and owner['person_id']==roles[b['recipient_role']]and owner['start']==s['start']and owner['end']==s['end']==v['start']and owner['surface']==s['surface'],'授職主體/角色/錨');need(m['basis_quote']in p['text']and m['basis_quote']==b['basis_quote']and m['interpretation_note']==b['interpretation_note'],'非人物原語境/判讀')
  need(not any(m['id']in a.get('mention_ids',[])for person in people for a in person.get('aliases',[]))and not any(e.get('mention_id')==m['id']for person in people for e in person.get('evidence',[])),'非人物不得保人物反向邊')
  need(not any(m['id']in d.get('identification_basis',{}).get('target_mention_ids',[])for doc in docs.values()for d in doc.get('decisions',[])),'非人物不得保同指target')
 for b in c.get('annotation_identity_comparisons',[]):
  p=ps[b['paragraph_id']];m=next(m for m in p['mentions']if m['id']==b['mention_id']);need(m['kind']=='person'and m['person_id']==roles[b['role_key']]and m['surface']==b['local_appellation']and p['text']==b['full_paragraph'],'引詩具體稱謂與current角色')
  raw=(Path(root)/b['raw_path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==b['raw_sha256'],'外部primary固定raw');text=raw.decode();u=b['unit'];need(text[u['start']:u['end']]==u['text']and hashlib.sha256(u['text'].encode()).hexdigest()==u['sha256'],'外部完整傳首及原位');need(u['text'].startswith('\u3000\u3000'+b['reference_full_name']+'，字'+b['courtesy_name']+'，'),'外部明文名/字');seed=next(s for s in c['existing_seeds']if s['role_key']==b['role_key']);need(seed['surface']==b['reference_full_name'],'canonical來源全名與外證明名');need(b['reference_qualification']['revision_id']==2605147 and b['reference_qualification']['edition']is None and b['reference_qualification']['image_verified']is False and b['reference_qualification']['human_reviewed']is False,'外部資格不得升格/冒武英殿')

def non_person_component_valid(mention,text,chapter,root):
 try:
  need(type(mention)is dict and type(chapter)is dict and type(text)is str and root is not None,'非人物須真完整章/root/原段');actual,roles,c,docs=state(root,chapter)
  return any(same(mention,row['marker'])and text==next(p['text']for p in actual['paragraphs']if p['id']==row['paragraph_id'])for row in c.get('non_person_markers',[]))
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False


def validate_appellation_fragment_groups(actual,roles,c):
 groups=c.get('appellation_fragment_groups',[]);need(type(groups)is list,'稱號片段群須list')
 ps={p['id']:p for p in actual['paragraphs']};ordered=[p['id']for p in actual['paragraphs']]
 for b in materialize(groups,roles):
  need(b.get('kind')=='source_bound_appellation_fragment_group'and b.get('appellation_kind')=='title','只限有源稱號片段，非姓名/holding');pid=roles[b['role']];fs=b['fragments'];need(type(fs)is list and len(fs)==2,'只兩相鄰稱號片段');a=b['complete_source_anchor'];ap=ps[a['paragraph_id']];am=next(m for m in ap['mentions']if m['id']==a['id']);need(same(am,{k:v for k,v in a.items()if k!='paragraph_id'})and am['kind']=='person'and am['person_id']==pid and am['surface']==b['value']and ap['text_layer']=='received_chapter','同源完整稱號/角色錨')
  for f in fs:
   p=ps[f['paragraph_id']];m=next(m for m in p['mentions']if m['id']==f['id']);need(same(m,{k:v for k,v in f.items()if k!='paragraph_id'})and m['kind']=='person'and m['person_id']==pid and p['text_layer']=='received_chapter','稱號片段完整原錨/同人/正文');need(type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface'],'稱號片段原字位置')
  first,last=fs;fp=ps[first['paragraph_id']];lp=ps[last['paragraph_id']];need(ordered.index(last['paragraph_id'])==ordered.index(first['paragraph_id'])+1 and first['end']==len(fp['text'])and last['start']==0,'稱號片段真相鄰尾首');need(fp['source_position']['last_line']+1==lp['source_position']['first_line'],'稱號片段真相鄰原列');need(first['surface']+last['surface']==b['value']and b['canonical_mention_id']==first['id'],'稱號連讀值及第一原錨');need(len({f['id']for f in fs})==2,'稱號片段錨不可重複')

def source_appellation_fragments(root,person_ids,people,records):
 # No source read for unrelated callers; accepted result always comes from the native full-frame guard.
 if not any(any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[]))for pid in person_ids):return []
 actual,roles,c,docs=state(root);registered={p['id']:p for p in load(root,'registry/persons.json')['persons']};need(all(same(people.get(pid),registered.get(pid))for pid in person_ids),'稱號片段current人物不符');need(sum(same(r,actual)for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==CID)==1,'稱號片段須唯一完整current正文');ps={p['id']:p for p in actual['paragraphs']};result=[]
 for b in materialize(c.get('appellation_fragment_groups',[]),roles):
  pid=roles[b['role']]
  if pid not in person_ids:continue
  result.append({'id':b['id'],'kind':'source_bound_appellation_fragment_group','person_id':pid,'source_id':actual['source_id'],'chapter_id':CID,'canonical_mention_id':b['canonical_mention_id'],'mention_ids':[f['id']for f in b['fragments']],'fragments':b['fragments'],'complete_appellation':{'kind':'title','value':b['value']},'complete_source_anchor':b['complete_source_anchor'],'source_quotes':[{'paragraph_id':f['paragraph_id'],'quote':ps[f['paragraph_id']]['text']}for f in b['fragments']],'status':'contextual_provisional','human_reviewed':False,'source_mentions_and_registry_aliases_retained':True,'qualification':b['qualification']})
 return result
