"""Finite three literal life/origin slots and one reviewed undated death pair. No PID whitelist."""
from pathlib import Path
import copy,hashlib,json
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
try:from scripts import fixed_jin098_wangdun_comparison as core
except ImportError:import fixed_jin098_wangdun_comparison as core
EP='source-evidence/jin098-wangdun-life/'
CH='corpus/jinshu/098-wangdun-comparison.json'
LIFE='corpus/jinshu/098-wangdun-comparison-life-events.json'
ADDR='corpus/jinshu/098-wangdun-comparison-addresses.json'
GROUP='corpus/jinshu/098-wangdun-comparison-life-event-groups.json'
OLDLIFE='corpus/jinshu/076-wangbin-life-events.json'
KIND='fixed_jin076_jin098_same_death'
PINS={'source-evidence/jin098-wangdun-life/source-proof.json': '5369b2389c47a91cb9df9f43d0c02a1f5df65c2e9ce9a9ca9c3ed0528c1777bd', 'source-evidence/jin098-wangdun-life/three-basics-template.json': 'bcfaf15752ae8c912b27e9f83c054cf51a378f9a4b973ab91e9fac79cd2b9bc9'}

def fixed(root,name):
 rel=EP+name;b=core.path(root,rel).read_bytes();core.need(hashlib.sha256(b).hexdigest()==PINS[rel],'生命/同事件完整契約漂移');return json.loads(b)
def read(root,rel):return json.loads(core.path(root,rel).read_bytes())
@memoized(1)
def prepared(ch,root):
 core.need(isinstance(ch,dict)and isinstance(ch.get('annotation'),dict),'生命來源入口型別不符');root=Path(root).resolve();core.need(core.same(ch,read(root,CH)),'生命來源章與實際root不符');roles=core.resolve(root,ch);t=core.expand(fixed(root,'three-basics-template.json'),roles);proof=fixed(root,'source-proof.json')
 annotation=ch['annotation'];wanted=t['life_annotation'];core.need(all(k in annotation and core.same(annotation[k],v)for k,v in wanted.items()),'生命階段/來源59報齡必須全槽相同')
 for rel,key in[(LIFE,'new_life_record'),(ADDR,'new_address_record'),(GROUP,'group_record')]:core.need(core.same(read(root,rel),t[key]),'生命/籍貫/同死亡分組完整資料不符')
 # This source's two new record families are closed: a second current sidecar is not an extra witness.
 for suffix,canonical in [('*-life-events.json',LIFE),('*-addresses.json',ADDR)]:
  for candidate in (root/'corpus').glob('*/'+suffix):
   rel=str(candidate.relative_to(root))
   if rel==canonical:continue
   record=json.loads(candidate.read_bytes());rows=record.get('events',record.get('assertions',[]))
   belongs=record.get('chapter_id')==core.CID or any(e.get('chapter_id')==core.CID for row in rows if isinstance(row,dict)for e in row.get('evidence',[])if isinstance(e,dict))
   core.need(not belongs,'098生命/籍貫不可另藏未驗影子記錄')
 old=read(root,OLDLIFE);matches=[e for e in old['events']if e['id']==t['prior_life_record']['id']];core.need(core.same(matches,[t['prior_life_record']]),'076原death record須原欄位保全，只許一致person重鍵')
 people={p['id']:p for p in read(root,'registry/persons.json')['persons']};seen={}
 for s in proof['proofs']:
  c=read(root,s['native_path']);core.need(all(c.get(k)==s[k]for k in('work_id','book_id','source_id'))and c['id']==s['chapter_id']and core.same(c['source'],s['source_descriptor']),'生命見證維度/取得/版源資格漂移');ps=[p for p in c['paragraphs']if p['id']==s['paragraph_id']];core.need(len(ps)==1,'生命段不唯一');p=ps[0];core.need(p['text']==s['complete_quote']and hashlib.sha256(p['text'].encode()).hexdigest()==s['paragraph_sha256']and core.same(p['source_position'],s['source_position'])and p['text_layer']=='received_chapter','生命完整原段/真層/位置不符');ms=[m for m in p['mentions']if m['id']==s['person_mention_id']];core.need(len(ms)==1,'生命MID不唯一');m=ms[0];core.need(core.same({k:m[k]for k in('start','end','surface','kind')},s['mention'])and m['person_id']==roles[s['role']],'生命角色/MID字位不符');person=people[roles[s['role']]];core.need(any(e.get('mention_id')==m['id']and e.get('chapter_id')==c['id']and e.get('paragraph_id')==p['id']for e in person.get('evidence',[]))and any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in person.get('aliases',[])),'生命角色缺registry反向');seen[p['id']]=p
 direct=t['source076_existing_direct_marker'];p=seen[direct['id'].rsplit(':',1)[0]];core.need(core.same([m for m in p['mentions']if m['id']==direct['id']],[direct]),'076既有直接敦錨須保留，非新增同名或換人')
 for key in['source076_death_clause','source098_death_clause']:
  a=proof[key];p=seen[a['paragraph_id']];core.need(type(a['start'])is int and type(a['end'])is int and p['text'][a['start']:a['end']]==a['surface'],'真卒原詞字位不符')
 core.need(proof['source076_death_clause']['surface']=='敦死'and proof['source098_death_clause']['surface']=='俄而敦死，時年五十九。','不能借假死詔/傳聞或別人報齡');raw=proof['source098_raw'];core.need(hashlib.sha256(core.path(root,raw['path']).read_bytes()).hexdigest()==raw['sha256']==core.RAW_SHA,'098原raw漂移')
 return roles,t

def stripped_chapter(ch,root):
 _,t=prepared(ch,root);view=copy.deepcopy(ch)
 for k in t['life_annotation']:view['annotation'].pop(k)
 return view

def group_valid(g,events,chapters,people,root):
 try:
  root=Path(root).resolve();ch=read(root,CH);core.need(ch.get('annotation',{}).get('life_stage')=='fixed_jin098_three_basics_and_same_death','同死亡不可漏098生命階段/59報齡');roles=core.validate_ner(ch,root);t=core.expand(fixed(root,'three-basics-template.json'),roles);expected,=t['group_record']['groups'];core.need(core.same(g,expected),'同死亡分組不是本源受驗完整pair');core.need(roles['dun']in people,'同死亡人不在current registry');actual_person,=[p for p in read(root,'registry/persons.json')['persons']if p['id']==roles['dun']];core.need(core.same(people[roles['dun']],actual_person),'傳入同死亡人物的反向來源/完整metadata不是current registry')
  for event in[t['prior_life_record'],t['new_life_record']['events'][0]]:core.need(core.same(events.get(event['id']),event),'同死亡原event端點/種類/未知年/資格不符')
  for e in expected['evidence']:
   c=chapters[e['chapter_id']];actual=read(root,'corpus/jinshu/076-wangbin.json'if e['chapter_id']=='c-jinshu-076-wangbin'else CH);core.need(core.same(c,actual),'傳入同死亡章/單端MID與current root不符')
  return True
 except(ValueError,KeyError,TypeError,OSError,UnicodeError,IndexError,AttributeError,StopIteration):return False

def catalog_basics_valid(records,root):
 chapters=[r for r in records if r.get('record_type')=='marked_chapter'and r.get('id')==core.CID]
 addresses=[r for r in records if r.get('record_type')=='person_address_assertion_set'and r.get('chapter_id')==core.CID]
 core.need(core.same(chapters,[read(root,CH)])and core.same(addresses,[read(root,ADDR)]),'傳入catalog098生命章/籍貫與current原生資料不符')

def stage_present(root):
 q=Path(root).resolve()/CH
 if not q.exists():return False
 c=read(root,CH)
 return isinstance(c,dict)and isinstance(c.get('annotation'),dict)and c['annotation'].get('life_stage')=='fixed_jin098_three_basics_and_same_death'

def stage_subject_ids(root):
 if not stage_present(root):return set(),None
 c=read(root,CH);ps=c.get('paragraphs');core.need(isinstance(ps,list)and all(isinstance(p,dict)and isinstance(p.get('mentions'),list)and all(isinstance(m,dict)for m in p['mentions'])for p in ps),'生命stage段/MID入口型別錯誤');by={m.get('id'):m for p in ps for m in p['mentions']}
 mids=[core.CID+':p034:m0095',core.CID+':p017:m0005'];core.need(all(mid in by for mid in mids),'生命stage必要MID缺失');ms=[by[mid]for mid in mids]
 core.need(all(m.get('kind')=='person'and isinstance(m.get('person_id'),str)for m in ms),'生命stage主體MID缺失')
 return {m['person_id']for m in ms},ms[0]['person_id']
