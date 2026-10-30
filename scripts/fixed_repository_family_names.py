"""Finite family-name reading backed by complete repository witness and literal near kin.
No label/structural-ID inference; no new relationship, birth year or glyph correction.
"""
from pathlib import Path
import json,hashlib
PROOF='source-evidence/jin043-wangrong-family-names/name-proof.json'
PROOF_SHA='813d37604d7ed24ad380b8f3db5c88d0cd9864b2b521590f272b2ef1468657e5'
KIND='contextual_surname_from_fixed_repository_biography_family'
CLAN_KIND='fixed_repository_biography_head_daughter'
OLD='c-jinshu-043-wangrong'
NEW='c-jinshu-043-wyd1739-wangrong'
FILES=('corpus/jinshu/043-wangrong-family-names.json','corpus/jinshu/035-wangsui-literal-names.json')
TRIGGERS=frozenset(('c-jinshu-043-wangrong:p001:m0000','c-jinshu-043-wangrong:p001:m0015','c-jinshu-043-wangrong:p001:m0023','c-jinshu-043-wangrong:p014:m0030','c-jinshu-043-wangrong:p011:m0172','c-jinshu-035-peikai-family:p011:m0022'))

def need(ok,message):
 if not ok:raise ValueError('王戎近系姓名：'+message)
def read(root,path):
 rel=Path(path);need(not rel.is_absolute()and'..'not in rel.parts,'來源路徑');p=(root/rel).resolve();need(p.is_relative_to(root),'來源越界');return json.loads(p.read_bytes())
def projection(c):
 return {'header':{k:c[k]for k in('format_version','record_type','id','work_id','book_id','source_id','title','source')},'paragraphs':[dict(id=p['id'],text=p['text'],text_layer=p['text_layer'],source_position=p['source_position'],mentions=[{k:m.get(k)for k in('id','start','end','surface','kind')}for m in p['mentions']])for p in c['paragraphs']]}
def expand(x,roles):
 if isinstance(x,str)and x.startswith('$'):need(x in roles,'未知角色');return roles[x]
 if isinstance(x,dict):return{k:expand(v,roles)for k,v in x.items()}
 if isinstance(x,list):return[expand(v,roles)for v in x]
 return x

def installed(root):
 root=Path(root).resolve();old=root/'corpus/jinshu/043-wangrong.json'
 return (root/PROOF).exists()or any((root/p).exists()for p in FILES)or(old.is_file()and bool(read(root,'corpus/jinshu/043-wangrong.json').get('annotation',{}).get('family_name_phase_ref')))

def state(root,people=None,records=None):
 root=Path(root).resolve();raw=(root/PROOF).read_bytes();need(hashlib.sha256(raw).hexdigest()==PROOF_SHA,'完整有限契約SHA');proof=json.loads(raw);chapters={}
 for unit in proof['source_units']:
  c=read(root,unit['path']);need(projection(c)==unit['projection'],'完整來源單元／字位漂移');chapters[c['id']]=c
  need(hashlib.sha256((root/unit['raw_path']).read_bytes()).hexdigest()==unit['raw_sha256'],'原始見證SHA')
 if people is None:people={p['id']:p for p in read(root,'registry/persons.json')['persons']}
 roles={}
 for key,spec in proof['roles'].items():
  c=chapters[spec['chapter_id']];p,=[p for p in c['paragraphs']if p['id']==spec['paragraph_id']];m,=[m for m in p['mentions']if m['id']==spec['marker']['id']];need(all(m.get(k)==v for k,v in spec['marker'].items())and m['kind']=='person','來源角色');pid=m.get('person_id');need(pid in people and people[pid].get('status')!='retired','現役來源人物')
  n=people[pid];need([e for e in n.get('evidence',[])if e.get('mention_id')==m['id']]==[spec['reverse_evidence']],'人物反查');need(any(a.get('surface')==m['surface']and m['id']in a.get('mention_ids',[])for a in n.get('aliases',[])),'原稱反查');roles['$'+key]=pid
 from scripts.fixed_repository_witness import validate_source
 wyd=read(root,proof['witness_path']);witness_roles=validate_source(wyd,root,people,records)
 for key,wkey in proof['witness_roles'].items():need(roles['$'+key]==witness_roles[wkey],'兩見證同角色不同端點')
 chapters[wyd['id']]=wyd
 assertions=read(root,proof['assertions_path'])['assertions'];by={a['id']:a for a in assertions};paras={p['id']:(c['id'],p)for c in chapters.values()for p in c['paragraphs']}
 from scripts.biography_family_clause import valid as family_valid
 for key,template in proof['relations'].items():
  expected=expand(template,roles);actual=by.get(expected['id']);need(actual==expected,'原父／祖／女斷言漂移');need(family_valid(actual,paras,assertions,chapters,root),'原近親句法不符')
 expectedfiles={path:expand(value,roles)for path,value in proof['name_files'].items()}
 for path,value in expectedfiles.items():need(read(root,path)==value,'完整姓名側檔不符')
 old=chapters[OLD];need(old['annotation'].get('family_name_phase_ref')=={'kind':'fixed_repository_biography_family_names','path':PROOF,'sha256':PROOF_SHA},'姓名階段引用不符')
 ages={a['id']:a for a in old['annotation'].get('age_assertions',[])}
 for aid,template in proof['ages'].items():need(ages.get(aid)==expand(template,roles),'生前／卒時報齡資料不符')
 if records is not None:
  for c in chapters.values():need(sum(r==c for r in records)==1,'catalog缺完整來源單元')
  for value in expectedfiles.values():need(sum(r==value for r in records)==1,'catalog缺完整姓名側檔')
 return proof,roles,chapters,by,expectedfiles

def validate_installed(root,people,records):
 if installed(root):state(root,people,records)

def guard_bundle(root,person_id,people,records):
 # A sparse caller cannot activate proof authority by inventing ownership tags.
 if not installed(root):return
 relevant=any(e.get('mention_id')in TRIGGERS for e in people.get(person_id,{}).get('evidence',[]))
 if not relevant:
  # Follow the finite proof's actual source-role seeds, including 035王綏.
  # The 043萬 and 035綏 endpoints must still agree in state(); no permanent PID list.
  proof_raw=(Path(root).resolve()/PROOF).read_bytes()
  need(hashlib.sha256(proof_raw).hexdigest()==PROOF_SHA,'完整有限契約SHA')
  proof=json.loads(proof_raw)
  for unit in proof['source_units']:
   c=read(Path(root).resolve(),unit['path'])
   if any(m.get('person_id')==person_id and m['id']in TRIGGERS for p in c['paragraphs']for m in p['mentions']):
    relevant=True;break
 if relevant:state(root,people,records)

def validate_surname(name,names,chapters,assertions,root):
 proof,roles,cs,aa,files=state(root);case=proof['name_cases']['grandfather'];expected=expand(case['record'],roles);need(name==expected,'祖父姓名非本來源行')
 need(all(chapters.get(cid)==c for cid,c in cs.items()),'姓名catalog缺完整原文')
 seed=expand(proof['seed_name'],roles);need(sum(n==seed for n in names)==1,'全名種子不符');relation=expand(proof['relations']['grandfather'],roles);need(sum(a==relation for a in assertions)==1,'祖父斷言被省略／倒置')
 need(relation['predicate']=='grandfather'and relation['subject_person_id']==roles['$head']and relation['object_person_id']==roles['$grandfather']and relation['qualifiers']['lineage']=='paternal','不是父系祖父')
 need(name['surname']==seed['surname']and name['ming']=='雄','祖父姓名組件不符')

def clan_valid(name,paragraph,relations,root=None):
 try:
  root=Path(root if root is not None else Path(__file__).resolve().parents[1]).resolve();proof,roles,cs,aa,files=state(root);case=proof['name_cases']['daughter'];need(name==expand(case['record'],roles),'未名女氏稱行不符')
  p,=[p for p in cs[OLD]['paragraphs']if p['id']==name['paragraph_id']];need(paragraph==p,'未名女原段不完整');relation=expand(proof['relations']['daughter'],roles);need(sum(a==relation for a in relations)==1,'女之父斷言缺失／倒置')
  need(name['ming']is None and'full_name'not in name and name['surname']=='王'and name['clan_style']['value']=='王氏','未名女不得補名或用夫姓')
  need(relation['predicate']=='father'and relation['subject_person_id']==roles['$daughter']and relation['object_person_id']==roles['$head']and relation['qualifiers']['source_clause_binding']['rule']=='close_family_head_daughter_marriage','非原父親及婚姻敘事')
  return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,StopIteration,AssertionError):return False
