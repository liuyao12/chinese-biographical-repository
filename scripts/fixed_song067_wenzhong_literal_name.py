"""One actual literal full name in existing author self-commentary, not a surname parser."""
from pathlib import Path
import json,hashlib
try:from scripts.validation_context import memoized
except ImportError:from validation_context import memoized
CASE='source-evidence/song067-wenzhong-literal-name-case.json';CASE_SHA='53747977d8a764ae3a8ed3b3b1bc08afdb6728752453d80c89139611321af803';NP='corpus/songshu/067-wenzhong-literal-name-components.json';KIND='received_song067_selfcommentary_literal_full_name'
def need(ok,msg):
 if not ok:raise ValueError('宋067完整原名：'+msg)
def same(a,b):return json.dumps(a,ensure_ascii=False,sort_keys=True)==json.dumps(b,ensure_ascii=False,sort_keys=True)
def material(x,pid):
 if isinstance(x,dict):return{k:material(v,pid)for k,v in x.items()}
 if isinstance(x,list):return[material(v,pid)for v in x]
 return pid if x=='$person'else x
@memoized(0)
def state(root):
 root=Path(root);raw=(root/CASE).read_bytes();need(hashlib.sha256(raw).hexdigest()==CASE_SHA,'完整caseSHA');case=json.loads(raw);c=json.loads((root/'corpus/songshu/067-xielingyun.json').read_text());need(all(c.get(k)==v for k,v in case['chapter_header'].items()),'章來源維度');need(same({k:v for k,v in c['source'].items()if k!='normalization'},case['source_header']),'固定見證資格');p=next(p for p in c['paragraphs']if p['id']==case['paragraph_id']);need(p['text']==case['paragraph_text'],'完整賦原字');own=next(m for m in p['mentions']if m['id']==case['source_marker']['id']);need(all(own.get(k)==v for k,v in case['source_marker'].items()),'本名真錨/字位/kind');pid=own['person_id'];need(own['surface']=='文種'and p['text'][own['start']:own['end']]=='文種','完整literal非借字');layer=case['self_commentary'];need(p['text'][layer['start']:layer['end']]==layer['quote']and layer['start']<=own['start']<own['end']<=layer['end'],'自注層界')
 source=(root/case['raw_path']).read_bytes();need(hashlib.sha256(source).hexdigest()==case['raw_sha256'],'固定rawSHA');proj=json.loads((root/'source-evidence/song067-lingyun-projection.json').read_text());need(any(x['paragraph_id']==p['id']and x['kind']=='author_self_commentary'and x['start']==layer['start']and x['end']==layer['end']and x['quote']==layer['quote']for x in proj['text_layers']['layers']),'實際自注層');lines=source.decode().splitlines();out=''
 for run in next(x for x in proj['projection']['paragraphs']if x['paragraph_id']==p['id'])['runs']:
  need(run['paragraph_start']==len(out),'投影起點');out+=lines[run['raw_line']-1][run['raw_start']:run['raw_end']];need(run['paragraph_end']==len(out),'投影終點')
 need(out==p['text'],'完整raw投影');s=case['parallel_seed'];sc=json.loads((root/s['chapter_path']).read_text());need(all(sc.get(k)==v for k,v in s['chapter_header'].items())and same(sc['source'],s['source']),'實際平行source維度/資格');sp=next(p for p in sc['paragraphs']if p['id']==s['paragraph_id']);sm=next(m for m in sp['mentions']if m['id']==s['mention_id']);need(sc['id']==s['chapter_id']and sp['text']==s['quote']and sm['kind']=='person'and sm['surface']==s['surface']and sm['person_id']==pid,'范蠡遺大夫種書的現役同人真MID');people={p['id']:p for p in json.loads((root/'registry/persons.json').read_text())['persons']};person=people[pid]
 for ch,para,m,complete in((c,p,own,True),(sc,sp,sm,False)):
  need(any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in person['aliases']),'人物原稱反查');base={'chapter_id':ch['id'],'paragraph_id':para['id'],'mention_id':m['id'],'quote':m['surface']};full={k:ch[k]for k in('work_id','book_id','source_id')}|base
  rows=[e for e in person['evidence']if e['mention_id']==m['id']];need(len(rows)==1 and(same(rows[0],full)or(not complete and same(rows[0],base))),'本名七欄/已知seed legacy或完整reverse')
 expected=material(case['name_template'],pid);doc=json.loads((root/NP).read_text());need(same(doc,{'format_version':'0.2','record_type':'person_name_component_set','chapter_id':c['id'],'records':[expected]}),'完整唯一姓名側車');return c,p,expected

def valid(n,paragraph,chapter,root):
 try:
  actual,p,expected=state(root);need(same(n,expected),'唯一完整原名row');need(isinstance(paragraph,dict)and same(paragraph,p),'caller完整原段');need(isinstance(chapter,dict)and chapter['id']==actual['id']and same(chapter,actual),'caller完整章');return True
 except(ValueError,KeyError,TypeError,OSError,StopIteration,IndexError):return False
