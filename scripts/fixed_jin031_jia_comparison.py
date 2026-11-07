"""Finite WS2479706 Jia unit: source projection and explicit core names, not a generic wiki parser."""
from pathlib import Path
import json,hashlib
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
CID='c-jinshu-031-jia-comparison';SID='s-jinshu031-jia-ws2479706-comparison';CH='corpus/jinshu/031-jia-comparison.json';EP='source-evidence/jin031-jia-comparison/source-proof.json';NS='corpus/jinshu/031-jia-comparison-names.json';AD='corpus/jinshu/031-jia-comparison-addresses.json'
PROOF_SHA='80fe719994b05dd0ecacf27916ef482a5cc80a4d6544790b230b364f0a54fc36'
NAME_KIND='contextual_surname_from_fixed_jin031_received_family'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,msg):
 if not v:raise ValueError('晉031：'+msg)
def path(root,rel):
 root=Path(root).resolve();p=Path(rel);need(not p.is_absolute()and'..'not in p.parts,'相對路徑');q=root/p;need(q.resolve()==q and q.is_file(),'來源路徑邊界');return q
def read(root,rel):return json.loads(path(root,rel).read_bytes())
def expand(x,roles):
 if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
 if isinstance(x,list):return[expand(v,roles)for v in x]
 return roles[x[1:]]if isinstance(x,str)and x.startswith('$')else x

def fixed(root):
 b=path(root,EP).read_bytes();need(H(b)==PROOF_SHA,'固定完整契約漂移');return json.loads(b)
def roles(root,proof,people):
 out={}
 for s in proof['seeds']:
  c=read(root,s['native_path']);need(c['id']==s['chapter_id']and all(c[k]==s[k]for k in('work_id','book_id','source_id'))and c['source'].get('revision_id')==s['revision_id'],'既有同人來源維度');p,=[p for p in c['paragraphs']if p['id']==s['paragraph']['id']];need({k:v for k,v in p.items()if k!='mentions'}==s['paragraph']and H(p['text'].encode())==s['paragraph_sha256'],'既有完整同人段');m,=[m for m in p['mentions']if m['id']==s['mention_id']];need({k:m[k]for k in('id','start','end','surface','kind')}==s['mention']and m['kind']=='person'and p['text'][m['start']:m['end']]==m['surface'],'既有MID/固定字位角色');person=people[m['person_id']];evidence=dict(work_id=c['work_id'],book_id=c['book_id'],source_id=c['source_id'],chapter_id=c['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(any(all(e.get(k)==v for k,v in evidence.items())for e in person['evidence'])and any(m['id']in a.get('mention_ids',[])and a['surface']==m['surface']for a in person['aliases']),'既有完整七欄反向引用');need(s['role']not in out or out[s['role']]==m['person_id'],'同role多seed不得不一致');out[s['role']]=m['person_id']
 need(out['queen']!=out['father'],'父女不可同人');return out

@memoized(0)
def source_context(root):
 b=fixed(root);people={p['id']:p for p in read(root,'registry/persons.json')['persons']};r=roles(root,b,people);return b,r,{pid:people[pid]for pid in r.values()}

def prepared(ch,root):
 if ch.get('annotation',{}).get('fixed_jin031_full_ner_ref'):
  try:from scripts.fixed_jin031_jia_full_ner import prepared as full_ner_prepared
  except ImportError:from fixed_jin031_jia_full_ner import prepared as full_ner_prepared
  return full_ner_prepared(ch,root)
 b,r,people=source_context(root);expected=expand(b['chapter_template'],r);need(ch==read(root,CH)==expected,'完整actual章/未知增量或角色漂移');raw=path(root,b['raw_path']).read_bytes();need(H(raw)==b['raw_sha256'],'固定raw漂移');t=raw.decode();need(t.count(b['opening_heading'])==t.count(b['following_heading'])==1 and t.index(b['opening_heading'])==b['selection_start']and t.index(b['following_heading'])==b['selection_end'],'完整單元節界')
 for p in ch['paragraphs']:
  loc=p['source_position'];ix=loc['raw_character_offsets'];need(p['text']==''.join(t[i]for i in ix)and H((json.dumps(ix,ensure_ascii=False,indent=2)+'\n').encode())==loc['projection_sha256'],'原行可見投影');need(p['text_layer']=='received_chapter'and loc['revision_id']==2479706,'來源層/修訂')
  for m in p['mentions']:
   need(p['text'][m['start']:m['end']]==m['surface']and m['kind']=='person','本源人物字位');person=people[m['person_id']];evidence=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);need(any(all(e.get(k)==v for k,v in evidence.items())for e in person['evidence'])and any(m['id']in a.get('mention_ids',[])and a['surface']==m['surface']for a in person['aliases']),'本源缺完整七欄reverse')
 for n in ch['annotation']['modern_collation_reports']:need(t[n['raw_start']:n['raw_end']]==n['raw_text']and n['image_verified']is False and n['human_reviewed']is False,'Wiki ref位置/資格')
 for rel,key in[(NS,'names_template'),(AD,'addresses_template')]:need(read(root,rel)==expand(b[key],r),'核心姓名/原籍側車漂移')
 for k,collection in [('father_assertion','assertions'),('father_name','records')]:
  q=b[k];want=expand(q['record'],r);need([x for x in read(root,q['native_path'])[collection]if x['id']==want['id']]==[want],'既有父女/父全名證照漂移')
 return r,b

def source_errors(ch,root):
 try:prepared(ch,root);return[]
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AttributeError):return['晉031完整單元、兩Wiki注、來源資格/同人/核心姓名原籍不符']

def xiaoming_valid(n,p):
 try:
  b=n['xiaoming_basis'];need(b['kind']=='fixed_jin031_opening_ming_origin_xiaoming'and b['source_revision']==2479706 and b['human_reviewed']is False and b['status']=='source_attested','小名資格');need(p['id']==CID+':p001'and n['paragraph_id']==p['id']and n['chapter_id']==CID and n['quote']==p['text']and H(p['text'].encode())==b['paragraph_sha256']and p['text'].startswith('惠賈皇后諱南風，平陽人也，小名時。父充，別有傳。'),'完整本段/諱籍貫小名詞序')
  ms={m['id']:m for m in p['mentions']};subject=ms[b['subject_mention_id']];ming=ms[b['ming_mention_id']];value=ms[b['value_mention_id']]
  need(all(m['kind']=='person'and m['person_id']==n['person_id']and p['text'][m['start']:m['end']]==m['surface']for m in [subject,ming,value]),'小名跨人');need([(m['start'],m['end'],m['surface'])for m in[subject,ming,value]]==[(0,4,'惠賈皇后'),(5,7,'南風'),(15,16,'時')]and n['person_mention_id']==ming['id']and n['ming']=='南風'and n['xiaoming']=='時'and b['source_term']=='小名時'and not n.get('zi'),'小名不是普通時字/未載字');return True
 except(ValueError,KeyError,TypeError,IndexError,AttributeError):return False

def validate_surname(n,names,chapters,assertions,root):
 ch=chapters[CID];r,b=prepared(ch,root);want=expand(b['names_template'],r)['records'][1];need(n==want,'復姓完整記錄');fn=expand(b['father_name']['record'],r);fa=expand(b['father_assertion']['record'],r);need([x for x in names if x.get('id')==fn['id']]==[fn]and any(x==fa for x in assertions),'復姓proof closure缺父全名或明父證')

def guard_bundle(root,pid,people,records):
 try:from scripts.fixed_jin031_jia_full_ner import active as full_ner_active,guard_bundle as full_ner_guard
 except ImportError:from fixed_jin031_jia_full_ner import active as full_ner_active,guard_bundle as full_ner_guard
 if full_ner_active(root):return full_ner_guard(root,pid,people,records)
 own=Path(root)/CH
 has=any(e.get('chapter_id')==CID for e in people.get(pid,{}).get('evidence',[]))
 if not own.exists():need(not has,'已新增來源reverse卻撤章');return
 b,r,actual_people=source_context(root)
 if pid in r.values()or has:
  need(people.get(pid)==actual_people.get(pid),'傳入相關人物不是完整current registry');ch=read(root,CH);prepared(ch,root);need([x for x in records if x.get('id')==CID]==[ch],'傳入catalog缺完整031章');need([x for x in records if x.get('record_type')=='person_name_component_set'and x.get('chapter_id')==CID]==[read(root,NS)],'傳入catalog缺031姓名');need([x for x in records if x.get('record_type')=='person_address_assertion_set'and x.get('chapter_id')==CID]==[read(root,AD)],'傳入catalog缺031原籍')
