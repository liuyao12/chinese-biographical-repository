"""Finite Zhou041 二陸 continuation: source collective, never aliases or direct occurrences."""
import copy,json,hashlib
from pathlib import Path
CID='c-zhoushu-041-wangbao-ws2432538'
MID='c-zhoushu-041-wangbao-ws2432538:p006:m0036'
REF='source-evidence/zhou041-wangbao-ws2432538/erlu-collective-contract.json'
SHA='917d46b524c6cc635af9ba91fc69ea8343200980c5c53c630b6508c403248e5b'
CH='corpus/zhoushu/041-wangbao-ws2432538.json'
GROUP='corpus/zhoushu/041-wangbao-ws2432538-reference-groups.json'
NOTE='二陸為陸機、陸雲完整二人合稱；群體錨保持未決人物/null PID，具體成員另存來源群體側車。'
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def need(ok,why):
 if not ok:raise ValueError('周041二陸群稱：'+why)
def read(root,rel):
 root=Path(root).resolve();p=root/rel;need(p.resolve()==p and p.is_relative_to(root),'路徑/symlink');return json.loads(p.read_bytes())
def expand(x,roles):
 if isinstance(x,str):return roles.get(x,x)
 if isinstance(x,list):return[expand(v,roles)for v in x]
 if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
 return x
def active(root,ch=None):
 p=Path(root)/CH
 if ch is None:
  if not p.is_file():return False
  ch=read(root,CH)
 return REF==ch.get('annotation',{}).get('fixed_zhou041_erlu_ref') or (Path(root)/REF).exists() or (Path(root)/GROUP).exists()
def contract(root):
 b=(Path(root)/REF).read_bytes();need(hashlib.sha256(b).hexdigest()==SHA,'契約SHA');c=json.loads(b);rb=(Path(root)/c['review_path']).read_bytes();need(hashlib.sha256(rb).hexdigest()==c['review_sha256'],'實讀資格SHA')
 fb=(Path(root)/c['fixed_primary_reading_path']).read_bytes();need(hashlib.sha256(fb).hexdigest()==c['fixed_primary_reading_sha256'],'既存固定capture閱讀SHA');f=json.loads(fb);raw=(Path(root)/f['raw_path']).read_bytes();meta=(Path(root)/f['existing_capture_metadata_path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==f['raw_sha256']and hashlib.sha256(meta).hexdigest()==f['existing_capture_metadata_sha256'],'既存固定raw/資格SHA');need(raw.decode()[f['start']:f['end']]==f['exact_quote']and hashlib.sha256(f['exact_quote'].encode()).hexdigest()==f['quote_sha256'],'實讀完整陸雲開篇')
 return c

def source_projection(ch,root,roles,c):
 if not active(root,ch):return ch
 contract(root);out=copy.deepcopy(ch);need(out['annotation'].pop('fixed_zhou041_erlu_ref',None)==REF,'active標記缺漏')
 original=expand(c['chapter_template'],roles);old=next(m for p in original['paragraphs']for m in p['mentions']if m['id']==MID);want=copy.deepcopy(old);want.pop('candidate_person_ids');want.update(interpretation_note=NOTE,source_reference_group_id='g-zhou041-erlu')
 rows=[(p,i,m)for p in out['paragraphs']for i,m in enumerate(p['mentions'])if m['id']==MID];need(len(rows)==1,'MID重複/缺漏');p,i,m=rows[0];need(same(m,want) and p['text'][m['start']:m['end']]=='二陸','群體全錨不得改成個人/代詞/候選');p['mentions'][i]=old
 cases=out['annotation']['unresolved_identity_cases'];need(not any(v['id']=='d-zhou041-erlu'for v in cases),'不再存二選一identity case');oldcases=original['annotation']['unresolved_identity_cases'];index=next(i for i,v in enumerate(oldcases)if v['id']=='d-zhou041-erlu');cases.insert(index,copy.deepcopy(oldcases[index]));return out

def validate_state(root,ch,people,roles,c):
 if not active(root,ch):return
 cap=contract(root);want=expand(cap['groups_template'],roles);need(same(read(root,GROUP),want),'完整群體側車缺/多/改')
 group=want['groups'][0];need(type(group['reported_count'])is int and group['reported_count']==len(group['members'])==len({m['person_id']for m in group['members']})==2,'完整二人計數')
 for member,spec in zip(group['members'],cap['member_source_anchors']):
  pid=member['person_id'];e=member['evidence'];source=read(root,spec['path']);need(all(source.get(k)==v for k,v in spec['source_dimensions'].items()),'外篇來源維度');ps=[p for p in source['paragraphs']if p['id']==spec['paragraph_id']];need(len(ps)==1 and hashlib.sha256(ps[0]['text'].encode()).hexdigest()==spec['paragraph_text_sha256'],'外篇完整段');ms=[m for m in ps[0]['mentions']if m['id']==spec['marker']['id']];need(len(ms)==1 and {k:v for k,v in ms[0].items()if k!='person_id'}==spec['marker']and ms[0]['person_id']==pid and ms[0]['kind']=='person'and ps[0]['text'][ms[0]['start']:ms[0]['end']]==ms[0]['surface'],'外篇真個人全錨');need(e==dict(work_id=source['work_id'],book_id=source['book_id'],source_id=source['source_id'],chapter_id=source['id'],paragraph_id=ps[0]['id'],mention_id=ms[0]['id'],quote=ms[0]['surface']),'來源反查七欄');need(pid in people,'成員缺現役人物');actor=people[pid];need(any(a['surface']==ms[0]['surface']and ms[0]['id']in a['mention_ids']for a in actor.get('aliases',[])),'真個人alias反查');need(sum(all(v==ev.get(k)for k,v in e.items())for ev in actor.get('evidence',[]))==1,'成員外篇七欄反查')
  need(not any(ev.get('mention_id')==MID for ev in actor.get('evidence',[])),'群稱不得直接個人提及');need(not any(MID in a.get('mention_ids',[])for a in actor.get('aliases',[])),'群稱不得個人別名')
 return want

def group_set_valid(d,people,root):
 try:from scripts.fixed_zhou041_wangbao import proof
 except ImportError:from fixed_zhou041_wangbao import proof
 ch,c,roles=proof(root,people=people);need(active(root,ch),'owner未啟用');need(same(d,validate_state(root,ch,people,roles,c)),'caller群體側車篡改');return True

def guard_catalog(records,people,root):
 if not active(root):return
 docs=[d for d in records if d.get('record_type')=='source_person_reference_group_set'and(d.get('owner')=='fixed_zhou041_erlu'or d.get('chapter_id')==CID)];need(len(docs)==1,'caller缺/多/錯owner本源群體側車');group_set_valid(docs[0],people,root)
