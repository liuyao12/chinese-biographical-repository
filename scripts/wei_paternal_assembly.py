# -*- coding: utf-8 -*-
"""Two finite source-bound editorial projections, never new received parent assertions."""
from pathlib import Path
import json,hashlib,copy
try:
 from scripts.validation_context import memoized
 from scripts.person_ids import family_path_errors
 from scripts.fixed_jin036_wei_ner import close_kin_state
except ImportError:
 from validation_context import memoized
 from person_ids import family_path_errors
 from fixed_jin036_wei_ner import close_kin_state
EP='source-evidence/wei-paternal-assembly/proof.json'
SHA='8502fbd86a5d6a01ed371e23e0fb4492dc884f633a6c908a4a4849dac7c94288'
def need(ok,why):
 if not ok:raise ValueError('衛氏有限父系投影：'+why)
def same(a,b):return json.dumps(a,ensure_ascii=False,sort_keys=True,allow_nan=False)==json.dumps(b,ensure_ascii=False,sort_keys=True,allow_nan=False)
def read(root,rel):
 root=Path(root).resolve();path=root/rel;need(path.resolve()==path and path.is_relative_to(root),'path/symlink');return json.loads(path.read_bytes())
def expand(v,roles,positions):
 if isinstance(v,str):
  if v.startswith('$source:'):return roles[v[8:]]
  if v.startswith('$position:'):return positions[v[10:]]
 if isinstance(v,list):return[expand(x,roles,positions)for x in v]
 if isinstance(v,dict):return{k:expand(x,roles,positions)for k,x in v.items()}
 return v
@memoized(0)
def context(root):
 need(root is not None,'root required');root=Path(root).resolve();proof_path=root/EP;need(proof_path.resolve()==proof_path,'proof symlink');raw=proof_path.read_bytes();need(hashlib.sha256(raw).hexdigest()==SHA,'proof SHA');b=json.loads(raw)
 _,roles,_,ch=close_kin_state(root);roles=dict(roles);song=read(root,b['song_path']);need(same(song['source'],b['song_source']),'宋060 received metadata/edition qualifications')
 p,=[p for p in song['paragraphs']if p['id']==b['song_paragraph_shape']['id']];shape=copy.deepcopy(p)
 for m in shape['mentions']:m.pop('person_id',None)
 need(same(shape,b['song_paragraph_shape']),'宋060 full paragraph/markers/layer/positions')
 ms={m['id']:m for m in p['mentions']};people={p['id']:p for p in read(root,'registry/persons.json')['persons']}
 for role,mid in b['song_role_mids'].items():
  if mid is None:continue
  m=ms[mid];need(m['kind']=='person'and p['text'][m['start']:m['end']]==m['surface'],'表內實錨')
  if role in roles:need(roles[role]==m['person_id'],'兩源具名角色不符')
  else:roles[role]=m['person_id']
  person=people[m['person_id']];reverse=[e for e in person.get('evidence',[])if e.get('mention_id')==mid]
  need(same(reverse,expand(b['song_reverse_templates'][role],roles,{}))and reverse[0].get('source_id')==song['source_id']and reverse[0].get('paragraph_id')==p['id']and reverse[0].get('quote')==m['surface'],'表內完整反向來源/原資格')
  need(any(a.get('surface')==m['surface']and mid in a.get('mention_ids',[])for a in person.get('aliases',[])),'表內alias/MID')
 pei=read(root,b['pei_path']);need(same(pei['source'],b['pei_source']),'035來源版本資格')
 pp,=[p for p in pei['paragraphs']if p['id']==b['pei_paragraph_shape']['id']];pshape=copy.deepcopy(pp)
 for m in pshape['mentions']:m.pop('person_id',None)
 need(same(pshape,b['pei_paragraph_shape']),'035完整原段/原錨/位置')
 pms={m['id']:m for m in pp['mentions']}
 for role,mid in b['pei_role_mids'].items():
  m=pms[mid];need(m['kind']=='person'and pp['text'][m['start']:m['end']]==m['surface'],'035人物實錨')
  if role in roles:need(roles[role]==m['person_id'],'035跨源角色錯人')
  else:roles[role]=m['person_id']
  person=people[m['person_id']];reverse=[e for e in person.get('evidence',[])if e.get('mention_id')==mid]
  need(same(reverse,expand(b['pei_reverse_templates'][role],roles,{}))and len(reverse)==1,'035反向來源資格')
  need(any(a.get('surface')==m['surface']and mid in a.get('mention_ids',[])for a in person.get('aliases',[])),'035alias/MID')
 need(len({roles[k]for k in b['relative_position_suffixes']})==len(b['relative_position_suffixes']),'十三來源角色不得暗合')
 positions={k:roles['gao']+suffix for k,suffix in b['relative_position_suffixes'].items()};wanted={}
 for rel in('corpus/jinshu/036-wei-comparison-assertions.json','corpus/songshu/060-assertions.json','corpus/jinshu/035-pei-family-assertions.json'):
  for a in read(root,rel)['assertions']:
   if a['id']in b['expected_assertions']:wanted[a['id']]=a
 need(same(wanted,expand(b['expected_assertions'],roles,positions)),'原始來源斷言缺失/改數/單端/資格')
 # A later explicit father must be reviewed before keeping either inferential edge.
 for path in(root/'corpus').glob('*/*-assertions.json'):
  for a in json.loads(path.read_bytes()).get('assertions',[]):
   need(not(a.get('predicate')=='father'and a.get('subject_person_id')in(roles['ji'],roles['chong'])),'已有新明父，不能沿用未知父投影')
 expected=expand(b['assembly_template'],roles,positions);expected_rows={m['person_id']:m for m in expected['members']}
 return b,roles,positions,{roles[k]:people[roles[k]]for k in list(b['relative_position_suffixes'])+['wei_son_wife','wei_son_wife_father']},ch,song,pei,wanted,expected_rows

def caller_context(member,rows,assertions,chapters,root,people):
 b,r,pos,actual,ch,song,pei,wanted,expected=context(root);need(isinstance(people,dict)and isinstance(rows,dict)and isinstance(assertions,dict)and isinstance(chapters,dict),'完整caller catalog')
 need(all(same(people.get(pid),person)for pid,person in actual.items()),'caller current role/reverse/metadata')
 need(same(chapters.get(ch['id']),ch)and same(chapters.get(song['id']),song)and same(chapters.get(pei['id']),pei),'caller兩篇完整章/實錨')
 need(all(same(assertions.get(aid),a)for aid,a in wanted.items()),'caller來源斷言缺失/偷換')
 need(not any(a.get('predicate')=='father'and a.get('subject_person_id')in(r['ji'],r['chong'])for a in assertions.values()),'caller偽加明父')
 need(same(rows,expected),'caller完整12節點/欄位/層次/衝突')
 need(member.get('person_id')in expected and same(member,expected[member['person_id']]),'member/caller row mismatch')
 return r,pos,wanted

def known_child_parent_ancestor_valid(member,rows,assertions,chapters,root,*,people=None):
 try:
  r,pos,a=caller_context(member,rows,assertions,chapters,root,people);need(member['person_id']==pos['ji'],'只處理本源覬槽')
  far=a['a-jin036-kin-001'];near=a['a-jin036-kin-002'];need(far['predicate']=='ancestor'and type(far['qualifiers']['generation_distance'])is int and far['qualifiers']['generation_distance']==4 and near['predicate']=='father','高祖4/父1原說')
  need(far['subject_person_id']==near['subject_person_id']==r['guan']and far['object_person_id']==r['gao']and near['object_person_id']==r['ji'],'祖/子/父方向')
  need(far['evidence']==near['evidence'] or {(e['paragraph_id'],e['quote'])for e in far['evidence']}=={(e['paragraph_id'],e['quote'])for e in near['evidence']},'同段全文')
  need(member['parent_person_id']is None and member['source_assertion_id']is None and member['ancestor_person_id']==pos['gao']and member['generation_distance']==3 and member['intermediate_person_ids']==[None,None],'只投影缺兩代祖連，不造父')
  need(family_path_errors(member['person_id'],member)==[],'結構ID/gap數')
  return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False

def high_great_pair_parent_valid(member,rows,assertions,chapters,root,*,people=None):
 try:
  r,pos,a=caller_context(member,rows,assertions,chapters,root,people);need(member['person_id']==pos['chong']and member['parent_person_id']==pos['zhao']and member['source_assertion_id']is None,'只處理崇→璪編輯父邊')
  far=a['a-songshu060-family-009'];near=a['a-songshu060-family-010'];raw=a['a-jin036-kin-024']
  need(far['predicate']=='ancestor'and far['qualifiers']['generation_distance']==4 and near['predicate']=='great_grandfather'and far['subject_person_id']==near['subject_person_id']==r['yu']and far['object_person_id']==r['zhao']and near['object_person_id']==r['chong'],'同表高祖/曾祖與主客')
  need({(e['chapter_id'],e['paragraph_id'],e['quote'])for e in far['evidence']}=={(e['chapter_id'],e['paragraph_id'],e['quote'])for e in near['evidence']},'同一自表全文，非跨源拼數')
  need(raw['subject_person_id']==r['chong']and raw['object_person_id']==r['guan']and raw['qualifiers']['generation_distance']==4,'原036玄孫4不可消失')
  need(member['generation_distance_readings']['preferred_for_this_assembly']['generation_distance']==3 and member['generation_distance_readings']['retained_source_claims'][0]['generation_distance']==4,'偏好3與原4明確分存')
  need(family_path_errors(member['person_id'],{'connection':'father','parent_person_id':member['parent_person_id']})==[],'結構ID父子距1')
  return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,AttributeError):return False
