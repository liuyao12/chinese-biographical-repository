"""Finite, AI-reviewed complete Wei biography NER; no runtime text inference."""
from pathlib import Path
import json,hashlib
try:
 from scripts import fixed_jin036_wei_comparison as core
 from scripts.validation_context import memoized
except ImportError:
 import fixed_jin036_wei_comparison as core
 from validation_context import memoized
EP=core.BASE+'ner-phase.json'
PROOF_SHA='0d7731ac625ab7842aa898c9023bf7f9b547dcd0d2991912a05b22daedcf222a'
H=lambda b:hashlib.sha256(b).hexdigest()
def same(a,b):return json.dumps(a,ensure_ascii=False,sort_keys=True,allow_nan=False)==json.dumps(b,ensure_ascii=False,sort_keys=True,allow_nan=False)
def need(ok,why):
 if not ok:raise ValueError('晉036完整NER：'+why)
def path(root,rel):
 root=Path(root).resolve();p=root/rel;need(p.resolve()==p and p.is_relative_to(root),'來源路徑越界/symlink');return p
def read(root,rel):return json.loads(path(root,rel).read_bytes())
def expand(v,r):
 if isinstance(v,str)and v.startswith('$role:'):return r[v[6:]]
 if isinstance(v,list):return [expand(x,r)for x in v]
 if isinstance(v,dict):return {k:expand(x,r)for k,x in v.items()}
 return v
@memoized(0)
def fixed(root):
 b=path(root,EP).read_bytes();need(H(b)==PROOF_SHA,'proof SHA');v=json.loads(b);need(H(path(root,core.BASE+'contract.json').read_bytes())==v['source_only_contract_sha256'],'來源前置契約');return _close_kin_effective(v,root)
@memoized(0)
def source_index(root):
 p=Path(root)/core.CH
 if not p.is_file():return {'active':False,'person_ids':[]}
 ch=read(root,core.CH);active='fixed_jin036_full_ner_ref'in ch.get('annotation',{});ids={m['person_id']for p in ch['paragraphs']for m in p['mentions']if m.get('kind')=='person'and m.get('person_id')}
 return {'active':active,'person_ids':sorted(ids)}
def reverse(person,ch,p,m,expected=None):
 e={k:ch[k]for k in ('work_id','book_id','source_id')};e.update(chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])
 rows=[x for x in person.get('evidence',[])if x.get('mention_id')==m['id']]
 if expected is None:need(len(rows)==1 and all(rows[0].get(k)==v for k,v in e.items()),'七欄reverse')
 else:
  need(len(rows)==1 and same(rows[0],expected),'既有seed reverse metadata')
  need(all(rows[0].get(k)==v for k,v in e.items()if k in rows[0]),'既有seed reverse維度')
 need(any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[])),'alias/MID')
def roles(root,b,people):
 r={};own=read(root,core.CH)
 for s in b['external_roles']:
  ch=read(root,s['native_path']);need(all(ch[k]==s[k]for k in ('work_id','book_id','source_id'))and ch['id']==s['chapter_id']and ch['source'].get('revision_id')==s['revision_id'],'外篇來源維度')
  p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];need({k:v for k,v in p.items()if k!='mentions'}==s['paragraph']and H(p['text'].encode())==s['paragraph_sha256'],'外篇完整段')
  m,=[m for m in p['mentions']if m['id']==s['mention_id']];need(same({k:m[k]for k in ('id','start','end','surface','kind')},s['mention'])and m['kind']=='person'and p['text'][m['start']:m['end']]==m['surface'],'外篇seed全錨')
  reverse(people[m['person_id']],ch,p,m,s['existing_reverse']);need(s['role']not in r or r[s['role']]==m['person_id'],'同role衝突');r[s['role']]=m['person_id']
 for s in b['local_roles']:
  p,=[p for p in own['paragraphs']if p['id']==s['paragraph_id']];need(H(p['text'].encode())==s['paragraph_sha256'],'本源整段')
  m,=[m for m in p['mentions']if m['id']==s['mention_id']];need(same({k:m[k]for k in ('id','start','end','surface','kind')},s['mention'])and m['kind']=='person'and p['text'][m['start']:m['end']]==m['surface'],'本源角色首錨')
  reverse(people[m['person_id']],own,p,m);r[s['role']]=m['person_id']
 need(len(set(r.values()))==len(r),'本源已核明確角色不得單端合併')
 return r
@memoized(0)
def source_context(root):
 b=fixed(root);people={p['id']:p for p in read(root,'registry/persons.json')['persons']};r=roles(root,b,people)
 return b,r,{pid:people[pid]for pid in r.values()}
@memoized(0)
def accepted_state(root):
 b,r,people=source_context(root);ch=read(root,core.CH);need(same(ch,expand(b['chapter_template'],r)),'完整21段/全錨/層/modern note/資格')
 for p in ch['paragraphs']:
  for m in p['mentions']:
   need(type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface'],'字位')
   if m['kind']=='person':reverse(people[m['person_id']],ch,p,m)
   elif m['kind']=='unresolved':need(m['person_id']is None and m['status']=='unresolved','合稱不得造人')
   else:need(m['kind']=='work'and m['person_id']is None,'作品不得造人')
 for key,tkey in [('names_path','names_template'),('identities_path','identities_template'),('groups_path','groups_template')]:need(same(read(root,b[key]),expand(b[tkey],r)),'側車完整template '+key)
 for n in ch['annotation'].get('non_person_exclusions',[]):
  p,=[p for p in ch['paragraphs']if p['id']==n['paragraph_id']]
  need(type(n['start'])is int and type(n['end'])is int and p['text'][n['start']:n['end']]==n['surface']and n['classification']=='non_person','non-person literal range')
  need(not any(max(m['start'],n['start'])<min(m['end'],n['end'])for m in p['mentions']),'non-person exclusion cannot retain a person/unresolved underline')
 # Validate original fixed rendered witness after removing only this owned phase.
 old=read(root,core.BASE+'contract.json')['chapter_template'];projection=json.loads(json.dumps(ch));projection['annotation']=old['annotation']
 for p,op in zip(projection['paragraphs'],old['paragraphs']):p['mentions']=op['mentions'];p['annotation_status']=op['annotation_status']
 projection.pop('cross_chapter_references',None)
 core._source_only_validate_source(projection,root)
 _close_kin_documents(root,r,ch)
 return b,r,people,ch
def validate_source(ch,root):
 b,r,people,actual=accepted_state(root);need(same(ch,actual),'caller章不完整');return True
def name_record_valid(n,root,all_names=None):
 try:
  b,r,people,ch=accepted_state(root);expected=expand(b['names_template'],r)['records']
  if all_names is not None:
   got=[n for n in all_names if n.get('chapter_id')==core.CID or str(n.get('person_mention_id','')).startswith(core.CID+':')];need(same(sorted(got,key=lambda n:n['id']),sorted(expected,key=lambda n:n['id'])),'全catalog姓名缺/多/重複')
  return any(same(n,x)for x in expected)
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False
def validate_surname(n,names,chapters,assertions,root=None):
 try:
  b,r,people,ch=accepted_state(root);need(chapters.get(core.CID)==ch,'推姓caller完整章');expected=expand(b['names_template'],r)['records'];need(any(same(n,x)for x in expected) and n.get('surname_basis',{}).get('kind')=='contextual_surname_from_fixed_jin036_received_family','推姓有限槽');need(all(x in names for x in expected),'推姓完整同源姓名proof closure');return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False
def guard_bundle(root,pid,people,records):
 has=any(e.get('chapter_id')==core.CID for e in people.get(pid,{}).get('evidence',[]))
 if pid not in source_index(root)['person_ids']and not has:return
 b,r,actual,ch=accepted_state(root);need(same(people.get(pid),actual.get(pid)),'caller個人metadata');need(same([x for x in records if x.get('id')==core.CID],[ch]),'caller缺完整本章')
 for key,typ in [('names_path','person_name_component_set'),('identities_path','person_identity_decision_set'),('groups_path','source_person_reference_group_set')]:need(same([x for x in records if x.get('record_type')==typ and x.get('chapter_id')==core.CID],[read(root,b[key])]),'caller缺本源側車 '+typ)
def group_set_valid(d,people,root):
 b,r,actual,ch=accepted_state(root);need(same(d,expand(b['groups_template'],r)),'未知/額外/篡改group/readings')
 for g in d['groups']:
  mids={m['id']:m for p in ch['paragraphs']for m in p['mentions']}
  need(all(mid in mids and mids[mid]['kind']=='unresolved'and mids[mid]['person_id']is None for mid in g['group_marker_ids']),'群體錨不得個人化')
  need(g['reported_count']is None or type(g['reported_count'])is int,'reported_count不得bool')
  for member in g['members']:
   pid=member['person_id'];e=member['evidence'];p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']];m,=[m for m in p['mentions']if m['id']==e['mention_id']];need(m['kind']=='person'and m['person_id']==pid,'member全端點');need(same(people.get(pid),actual[pid]),'member metadata');reverse(people[pid],ch,p,m)
 for x in d['unresolved_readings']:
  need(all(pid in people for pid in x['candidate_person_ids']),'候選缺現役人物')
  kind=x.get('interpretation_kind')
  if kind in ('collective_resolution','partial_collective_resolution'):
   need(x['preferred_person_id']is None and x['status']=='editorial_provisional'and bool(x['resolved_member_refs']),'合稱解讀資格')
   for member in x['resolved_member_refs']:
    pid=member['person_id'];e=member['evidence'];p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']];m,=[m for m in p['mentions']if m['id']==e['mention_id']];need(m['kind']=='person'and m['person_id']==pid,'合稱個人真錨');need(same(people.get(pid),actual[pid]),'合稱個人metadata');reverse(people[pid],ch,p,m)
   for q in x['source_ranges']:
    p,=[p for p in ch['paragraphs']if p['id']==q['paragraph_id']];need(p['text'][q['start']:q['end']]==q['surface']and H(p['text'].encode())==q['paragraph_text_sha256'],'合稱來源完整段/範圍')
  elif kind=='external_name_reading':need(x['preferred_person_id']==x['subject_person_id']and x['subject_person_id']in actual and same(people.get(x['subject_person_id']),actual[x['subject_person_id']])and x['status']=='editorial_provisional','參校姓名資格')
  else:need(x['preferred_person_id']is None if x['status']=='unresolved'else x['preferred_person_id']in x['candidate_person_ids'],'候選首選/未決資格')
 return True

def work_author_valid(ev,work,ch,root):
 try:
  b,r,people,actual=accepted_state(root);need(same(ch,actual),'著作caller完整章');w=expand(b['work_registry_fields'],r).get(work['id']);need(w is not None and same(work,w)and any(same(ev,x)for x in w.get('source_author_attributions',[])),'完整source-bound作者契約');return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False

# --- fixed-jin036-close-kin finite continuation; original NER proof remains immutable ---
CLOSE_KIN_EP=core.BASE+'close-kin-phase.json'
CLOSE_KIN_SHA='ae3b8d645cd19a79e83451d83ab420770debc9cfc33196835d8c1c2f1eac3ebc'
CLOSE_KIN_RULE='fixed_jin036_complete_unit_close_kin'
def close_kin_proof(root):
 raw=path(root,CLOSE_KIN_EP).read_bytes();need(H(raw)==CLOSE_KIN_SHA,'close-kin proof SHA');return json.loads(raw)
def _close_kin_effective(parent,root):
 if not(Path(root)/CLOSE_KIN_EP).is_file():return parent
 import copy
 b=close_kin_proof(root);need(H(path(root,EP).read_bytes())==b['parent_ner_sha256'],'close-kin exact NER predecessor')
 out=copy.deepcopy(parent)
 for k,v in b['annotation_additions'].items():need(k not in out['chapter_template']['annotation'],'close-kin annotation collision');out['chapter_template']['annotation'][k]=v
 return out
def _close_kin_documents(root,r,ch):
 if not(Path(root)/CLOSE_KIN_EP).is_file():return None
 b=close_kin_proof(root);need(ch['annotation'].get('fixed_jin036_close_kin_ref')==CLOSE_KIN_EP,'close-kin active annotation')
 for rel,template in b['expected_documents'].items():
  d=read(root,rel);need(same(d,expand(template,r)),'close-kin sidecar missing/extra/one-end drift '+rel)
  if d.get('record_type')=='source_family_count_report_set':
   groups=read(root,fixed(root)['groups_path'])['groups']
   for count in d['reports']:
    if count['reference_group_id'] is not None:
     g,=[g for g in groups if g['id']==count['reference_group_id']]
     need(g['reported_count']==count['reported_count']and {m['person_id']for m in g['members']}==set(count['known_member_person_ids']),'close-kin source group membership/count mismatch')
  items=d.get('assertions',d.get('reports',[]))
  for rec in items:
   for e in rec['evidence']:
    p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']]
    need(e['quote']==p['text']and e['chapter_id']==ch['id']and all(e[k]==ch[k]for k in('work_id','book_id','source_id')),'close-kin complete source quote/dimensions')
    ms={m['id']:m for m in p['mentions']}
    for field,endpoint in [('subject_person_mention_id','subject_person_id'),('object_person_mention_id','object_person_id'),('reference_person_mention_id','reference_person_id')]:
     if field in e:
      m=ms[e[field]];need(m['kind']=='person'and m['person_id']==rec[endpoint]and p['text'][m['start']:m['end']]==m['surface'],'close-kin role/MID endpoint')
    if 'count_anchor'in e:
     a=e['count_anchor'];need(type(a['start'])is int and type(a['end'])is int and p['text'][a['start']:a['end']]==a['surface'],'close-kin count exact source range')
 return b
def close_kin_state(root):
 b,r,people,ch=accepted_state(root);t=_close_kin_documents(root,r,ch);need(t is not None,'close-kin phase missing');return t,r,people,ch
def close_kin_applies(a):return a.get('qualifiers',{}).get('source_clause_binding',{}).get('rule')==CLOSE_KIN_RULE
def close_kin_valid(a,paragraphs,root):
 try:
  b,r,people,ch=close_kin_state(root);expected=expand(b['expected_documents']['corpus/jinshu/036-wei-comparison-assertions.json'],r)['assertions'];need(any(same(a,x)for x in expected),'close-kin exact assertion slot')
  for e in a['evidence']:
   p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']];hit=paragraphs.get(p['id']);need(hit is not None and hit[0]==ch['id']and same(hit[1],p),'close-kin caller paragraph/mention full tuple')
  return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False
def _close_kin_caller_catalog(records,people,root,b,r,actual,ch):
 need(isinstance(people,dict)and isinstance(records,list),'close-kin caller catalog types')
 for pid,person in actual.items():need(same(people.get(pid),person),'close-kin caller role/PID/reverse/metadata '+pid)
 need(same([d for d in records if d.get('record_type')=='marked_chapter'and d.get('id')==core.CID],[ch]),'close-kin caller full chapter')
 parent=fixed(root)
 for key in('names_path','identities_path','groups_path'):
  expected=read(root,parent[key]);got=[d for d in records if d.get('record_type')==expected['record_type']and d.get('chapter_id')==core.CID];need(same(got,[expected]),'close-kin caller NER sidecar '+key)
 for rel,template in b['expected_documents'].items():
  expected=expand(template,r);got=[d for d in records if d.get('record_type')==expected['record_type']and d.get('chapter_id')==core.CID];need(same(got,[expected]),'close-kin caller complete sidecar '+rel)
def close_kin_counts(records,people,root,ids):
 # This owner accepts its own reports in a full multi-owner catalog. Foreign
 # reports remain validated by the finite dispatcher; unknown/mislabelled owners
 # must not disappear merely because they belong to another chapter.
 all_docs=[d for d in records if d.get('record_type')=='source_family_count_report_set']
 allowed={'fixed_jin036_wei_ner':core.CID,'fixed_jin034_yanghu_ner':'c-jinshu-034-yanghu-comparison'}
 need(all(d.get('owner')in allowed and d.get('chapter_id')==allowed[d['owner']]for d in all_docs),'unknown family-count owner')
 docs=[d for d in all_docs if d['owner']=='fixed_jin036_wei_ner']
 if not(Path(root)/CLOSE_KIN_EP).is_file():need(not docs,'orphan family-count sidecar');return []
 b,r,actual,ch=close_kin_state(root);_close_kin_caller_catalog(records,people,root,b,r,actual,ch)
 key='corpus/jinshu/036-wei-comparison-family-counts.json';expected=expand(b['expected_documents'][key],r)
 need(all(d.get('owner')=='fixed_jin036_wei_ner'and d.get('chapter_id')==core.CID for d in docs),'unknown family-count owner')
 # Return only published typed reports; internal witness templates/authoring rows stay private.
 return [d for d in expected['reports']if d['reference_person_id']in ids]
def close_kin_guard_bundle(root,pid,people,records):
 if not(Path(root)/CLOSE_KIN_EP).is_file():return
 b,r,actual,ch=close_kin_state(root)
 if pid not in r.values():return
 _close_kin_caller_catalog(records,people,root,b,r,actual,ch)
# --- end fixed-jin036-close-kin ---
