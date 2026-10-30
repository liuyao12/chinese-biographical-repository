"""Finite, AI-reviewed complete Yang Hu biography NER; no runtime text inference."""
from pathlib import Path
import json,hashlib
try:
 from scripts.validation_context import memoized
except ImportError:
 from validation_context import memoized
CID='c-jinshu-034-yanghu-comparison'
SID='s-jinshu-034-yanghu-ws2567662-rendered-comparison'
CH='corpus/jinshu/034-yanghu-comparison.json'
BASE='source-evidence/jin034-yanghu-comparison/'
EP=BASE+'ner-phase.json'
PROOF_SHA='169916d6f41b4fc8d4c9c0007e199e5869ae7df6658b398c504e48d98ec637d6'
H=lambda b:hashlib.sha256(b).hexdigest()
def same(a,b):return json.dumps(a,ensure_ascii=False,sort_keys=True,allow_nan=False)==json.dumps(b,ensure_ascii=False,sort_keys=True,allow_nan=False)
def need(ok,why):
 if not ok:raise ValueError('晉034完整NER：'+why)
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
 b=path(root,EP).read_bytes();need(H(b)==PROOF_SHA,'proof SHA');v=json.loads(b);need(H(path(root,v['source_parent_path']).read_bytes())==v['source_parent_sha256'],'來源前置契約');
 for rel,h in v['source_input_pins'].items():need(H(path(root,rel).read_bytes())==h,'source input pin '+rel)
 try:from scripts.fixed_jin034_core_kinship import effective
 except ImportError:from fixed_jin034_core_kinship import effective
 out=effective(v,root)
 try:from scripts.fixed_jin034_minimal_life import effective as minimal_life_effective
 except ImportError:from fixed_jin034_minimal_life import effective as minimal_life_effective
 return minimal_life_effective(out,root)
@memoized(0)
def source_index(root):
 p=Path(root)/CH
 if not p.is_file():return {'active':False,'person_ids':[]}
 ch=read(root,CH);active='fixed_jin034_full_ner_ref'in ch.get('annotation',{});ids={m['person_id']for p in ch['paragraphs']for m in p['mentions']if m.get('kind')=='person'and m.get('person_id')}
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
 r={};own=read(root,CH)
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
 b,r,people=source_context(root);ch=read(root,CH);need(same(ch,expand(b['chapter_template'],r)),'完整41段/全錨/層/modern note/資格')
 for p in ch['paragraphs']:
  for m in p['mentions']:
   need(type(m['start'])is int and type(m['end'])is int and p['text'][m['start']:m['end']]==m['surface'],'字位')
   if m['kind']=='person':reverse(people[m['person_id']],ch,p,m)
   elif m['kind']=='unresolved':need(m['person_id']is None and m['status']=='unresolved','合稱不得造人')
   else:need(m['kind']=='work'and m['person_id']is None,'作品不得造人')
 for key,tkey in [('names_path','names_template'),('identities_path','identities_template'),('groups_path','groups_template')]:need(same(read(root,b[key]),expand(b[tkey],r)),'側車完整template '+key)
 # Full literal 楊肇 in p011 is not a 羊-family ellipsis. Independent of the proof template.
 zrows=[n for n in read(root,b['names_path'])['records']if n.get('person_id')==r['yang_zhao']]
 need(len(zrows)==1,'楊肇只能保一個本源literal姓名')
 z=zrows[0];zp,=[p for p in ch['paragraphs']if p['id']==CID+':p011'];zm,=[m for m in zp['mentions']if m['id']==CID+':p011:m0043']
 need(zm['surface']=='楊肇'and zm['start']==43 and zm['end']==45 and zm['person_id']==r['yang_zhao']and zp['text'].count('楊肇')==3,'楊肇完整原文角色')
 need(z.get('surname')=='楊'and z.get('ming')=='肇'and 'surname_basis'not in z and z.get('source_anchor')=={'start':43,'end':45,'surface':'楊肇'}and z.get('person_mention_id')==zm['id']and z.get('quote')==zp['text'],'楊肇原文明姓不得借羊氏復姓')
 for n in ch['annotation'].get('non_person_exclusions',[]):
  p,=[p for p in ch['paragraphs']if p['id']==n['paragraph_id']]
  need(type(n['start'])is int and type(n['end'])is int and p['text'][n['start']:n['end']]==n['surface']and n['classification']=='non_person','non-person literal range')
  need(not any(max(m['start'],n['start'])<min(m['end'],n['end'])for m in p['mentions']),'non-person exclusion cannot retain a person/unresolved underline')
 # Validate original fixed rendered witness after removing only this owned phase.
 old=read(root,b['source_parent_path']);projection=json.loads(json.dumps(ch));projection['annotation']=old['annotation']
 for p,op in zip(projection['paragraphs'],old['paragraphs']):p['mentions']=op['mentions'];p['annotation_status']=op['annotation_status']
 need(same(projection,old),'原41段source-only前置全文/層/資格')
 need(H(path(root,old['source']['capture_ref']).read_bytes())==old['source']['capture_sha256'],'固定呈現文字capture SHA')
 projection_doc=read(root,BASE+'projection.json');need([x['text']for x in projection_doc['paragraphs']]==[x['text']for x in old['paragraphs']]and projection_doc['open_heading_line']==130 and projection_doc['closing_heading_line']==201,'原頁完整起訖/projection')
 works={w['id']:w for w in read(root,'registry/works.json')['works']}
 for wid,w in expand(b['work_registry_fields'],r).items():need(same(works.get(wid),w),'作品/作者/範圍metadata')
 try:from scripts.fixed_jin034_core_kinship import documents
 except ImportError:from fixed_jin034_core_kinship import documents
 documents(root,r,ch)
 try:from scripts.fixed_jin034_minimal_life import documents as minimal_life_documents
 except ImportError:from fixed_jin034_minimal_life import documents as minimal_life_documents
 minimal_life_documents(root,r,ch)
 return b,r,people,ch
def validate_source(ch,root):
 b,r,people,actual=accepted_state(root);need(same(ch,actual),'caller章不完整');return True
def name_record_valid(n,root,all_names=None):
 try:
  b,r,people,ch=accepted_state(root);expected=expand(b['names_template'],r)['records']
  if all_names is not None:
   got=[n for n in all_names if n.get('chapter_id')==CID or str(n.get('person_mention_id','')).startswith(CID+':')];need(same(sorted(got,key=lambda n:n['id']),sorted(expected,key=lambda n:n['id'])),'全catalog姓名缺/多/重複')
  return any(same(n,x)for x in expected)
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False
def validate_surname(n,names,chapters,assertions,root=None):
 try:
  b,r,people,ch=accepted_state(root);need(chapters.get(CID)==ch,'推姓caller完整章');expected=expand(b['names_template'],r)['records'];need(any(same(n,x)for x in expected) and n.get('surname_basis',{}).get('kind')=='contextual_surname_from_fixed_jin034_received_family','推姓有限槽');need(all(x in names for x in expected),'推姓完整同源姓名proof closure');return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return False
def guard_bundle(root,pid,people,records):
 has=any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[]))
 if pid not in source_index(root)['person_ids']and not has:return
 b,r,actual,ch=accepted_state(root);need(same(people.get(pid),actual.get(pid)),'caller個人metadata');need(same([x for x in records if x.get('id')==CID],[ch]),'caller缺完整本章')
 for key,typ in [('names_path','person_name_component_set'),('identities_path','person_identity_decision_set'),('groups_path','source_person_reference_group_set')]:need(same([x for x in records if x.get('record_type')==typ and x.get('chapter_id')==CID],[read(root,b[key])]),'caller缺本源側車 '+typ)
 # bounded-minimal-life-caller: unrelated-person early return above stays unchanged.
 try:from scripts.fixed_jin034_minimal_life import guard_bundle as minimal_life_guard
 except ImportError:from fixed_jin034_minimal_life import guard_bundle as minimal_life_guard
 minimal_life_guard(root,pid,people,records,r,actual,ch)
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


def source_errors(ch,root,source_path=None):
 owned=source_path is not None and Path(source_path).resolve()==(Path(root)/CH).resolve()
 if not owned and ch.get('id')!=CID and ch.get('source_id')!=SID and 'fixed_jin034_full_ner_ref'not in ch.get('annotation',{}):return []
 try:validate_source(ch,root);return []
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError,UnicodeError)as exc:return ['晉034完整NER：'+str(exc)]
