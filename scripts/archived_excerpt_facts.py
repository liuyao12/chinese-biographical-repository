# coding:utf-8
"""Only previously archived quoted excerpts; never a complete external raw witness.
Trusted role recipe is maintained independently of candidate chapter edits.
"""
from pathlib import Path
import json,hashlib,re,copy
KIND='fixed_archived_excerpt_fact';REF='archived_excerpt_fact_slots_ref'
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
 return a==b

def config(root):
 p=Path(root).resolve()/'scripts/archived_excerpt_fact_recipes.json';assert p.resolve()==p and p.is_file()
 d=json.loads(p.read_bytes());assert d['format_version']=='0.1'and isinstance(d['recipes'],dict);return d['recipes']
def project(text):
 t=text.strip()
 if t.startswith('{{quote|'):t=t[8:].lstrip()
 if t.endswith('}}')and not re.search(r'\{\{YL\|[^{}]*\}\}$',t):t=t[:-2]
 t=re.sub(r'\{\{YL\|([^{}|]+)\}\}',r'\1',t)
 t=re.sub(r'\[\[([^\[\]]+)\]\]',lambda m:m[1].split('|')[-1],t)
 assert not any(x in t for x in('{{','}}','[[',']]','<ref','</ref'))
 return t

def grammar(ch,root):
 root=Path(root).resolve();recipes=config(root);r,=[r for r in recipes.values()if r['chapter_id']==ch['id']]
 assert ch['annotation'][REF]==dict(kind=KIND,key=r['key'])
 # This contract is never an alternative to a complete-raw chapter's driver.
 assert not any(ch['annotation'].get(k)for k in('fixed_wikisource_unit_ref','fixed_kanripo_projection_ref'))
 rel=Path(r['source_file']);assert not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]=='source-evidence';p=root/rel;assert p.resolve()==p and p.is_file();raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==r['source_sha256'];s=json.loads(raw)
 assert all(ch[k]==s[k]for k in('id',)if k in s)
 assert ch['id']==s['chapter_id']and all(ch[k]==s[k]for k in('work_id','book_id','source_id'))
 assert ch['source']['revision_id']==s['revision_id']and ch['source']['permalink']==s['permalink']and ch['source']['wikitext_sha256']==s['wikitext_sha256']
 excerpts=ch['source']['normalization']['excerpts'];assert strict(excerpts,s['excerpts'])and len(excerpts)==len(ch['paragraphs'])==len(s['paragraphs'])
 em={e['proposed_paragraph_id']:e for e in excerpts};assert len(em)==len(excerpts)
 marks={}
 for p,w in zip(ch['paragraphs'],s['paragraphs']):
  assert all(strict(p[k],w[k])for k in('id','text','source_position','text_layer'));assert p['text_layer']=='received_chapter'
  e=em[p['id']];assert hashlib.sha256(e['raw_quote'].encode()).hexdigest()==e['raw_quote_sha256']and hashlib.sha256(p['text'].encode()).hexdigest()==e['selected_text_sha256'];assert project(e['raw_quote'])==p['text']
  assert type(e['source_lines'][0])is int and len(e['source_lines'])==2 and e['source_lines'][0]<=e['source_lines'][1]
  ms=[m for m in p['mentions']if m['kind']=='person'];assert len(ms)==len(w['mentions'])
  for m,fixed in zip(ms,w['mentions']):
   assert all(m[k]==fixed[k]for k in('id','start','end','surface'))and p['text'][m['start']:m['end']]==m['surface'];assert m['id']not in marks;marks[m['id']]=m
 groups=r['same_person_groups'];assert sorted(x for g in groups for x in g)==sorted(marks)
 identities=[]
 for g in groups:
  ids={marks[mid]['person_id']for mid in g};assert len(ids)==1;identities.extend(ids)
 assert len(identities)==len(set(identities))
 return r,marks

def expand(v,marks):
 if isinstance(v,dict):
  if set(v)=={'$person'}:return marks[v['$person']]['person_id']
  return{k:expand(x,marks)for k,x in v.items()}
 if isinstance(v,list):return[expand(x,marks)for x in v]
 return v

def records(ch,root):
 r,marks=grammar(ch,root);out=[expand(s['record'],marks)for s in r['slots']];assert len({v['id']for v in out})==len(out)
 for s,v in zip(r['slots'],out):assert v['archived_excerpt_fact_binding']==dict(kind=KIND,key=r['key'],slot=s['slot'])
 return out

def valid(v,ch,root):
 try:return strict(v,next(x for x in records(ch,root)if x['id']==v['id']))
 except(AssertionError,KeyError,IndexError,TypeError,ValueError,OSError,StopIteration,AttributeError):return False

def validate_names(ch,root,all_rows):
 r,marks=grammar(ch,root);expected=records(ch,root);by={v['id']:v for v in expected};relations={a['id']:a for row in all_rows for a in row.get('assertions',[])};ps={p['id']:p for p in ch['paragraphs']}
 for aid,template in r['relation_proofs'].items():assert strict(relations[aid],expand(template,marks))
 for migration in r.get('legacy_migrations',[]):
  old=expand(migration['legacy_record'],marks);target=by[migration['native_record_id']]
  assert migration['old_stable_id']is None and 'id'not in old
  for key,value in old.items():
   if key=='status':assert target['migrated_source_qualification']['prior_status']==value
   else:assert strict(target[key],value)
  assert not any(strict(n,old)for row in all_rows for n in row.get('records',[]))
 for slot,v in zip(r['slots'],expected):
  if slot['category']!='name':continue
  p=ps[v['paragraph_id']];m=marks[slot['name_mid']];assert v['person_id']==m['person_id']and v['person_mention_id']==m['id']and v['quote']==p['text']
  if slot['name_mode']=='full_name':assert m['surface']==v['surname']+v['ming']and 'surname_basis'not in v
  else:assert slot['name_mode']=='ming_only'and m['surface']==v['ming']
  a=slot['zi_anchor']
  if a is None:assert 'zi'not in v
  else:assert p['text'][a['start']:a['end']]==a['surface']==v['zi']and p['text'][m['end']:a['start']]in('字','，字')and v['zi']!=v['ming']
  if 'surname_basis'not in v:continue
  b=v['surname_basis'];assert b['kind']=='contextual_surname_from_archived_excerpt_paths'and b['status']=='contextual_provisional'and b['human_reviewed']is False and v['status']=='contextual_provisional'
  seed=b['source_name_record_id']
  if seed.startswith('source-full-name:'):
   n=r['external_name_seeds'][seed.split(':',1)[1]];sm=marks[n['person_mid']];assert sm['surface']==n['surname']+n['ming']==n['full_name'];current=sm['person_id'];surname=n['surname']
  else:n=by[seed];assert not n.get('surname_basis')and next(s for s in r['slots']if s['record']['id']==seed)['name_mode']=='full_name';current=n['person_id'];surname=n['surname']
  assert surname==v['surname'];steps=b['steps'];assert len(steps)<=3;seen={current};used=set()
  for step in steps:
   aid=step['assertion_id'];assert aid not in used;used.add(aid);a=relations[aid];q=a['qualifiers'];assert a['status']=='source_attested'and all(e['chapter_id']==ch['id']for e in a['evidence'])
   assert a['predicate']in('father','ancestor','brother','agnatic_cousin','kinship_unspecified')and not any(q.get(k)for k in('adoptive','sworn','shared_mother'))
   if a['predicate']=='ancestor':assert q['lineage']=='paternal'and type(q['generation_distance'])is int and q['generation_distance']>0
   if a['predicate']=='kinship_unspecified':assert q['kinship_basis']=='archived_excerpt_collateral_appellation'and q['lineage']=='paternal'
   if a['predicate']=='agnatic_cousin':assert q['kinship_structure']['lineage']=='paternal'and q['kinship_structure']['generation_difference']==0
   sub,obj=a['subject_person_id'],a['object_person_id'];direction=step['traversal']
   if direction=='subject_to_object':assert current==sub;current=obj
   else:assert direction=='object_to_subject'and current==obj;current=sub
   assert current not in seen;seen.add(current)
  assert current==v['person_id']

def errors(root,rows):
 if not (Path(root)/'scripts/archived_excerpt_fact_recipes.json').exists():
  active=any(c.get('annotation',{}).get(REF)for c in rows)or any(v.get('archived_excerpt_fact_binding')for row in rows for field in('assertions','records')for v in row.get(field,[]))
  return ['既存節錄事實缺受信配方']if active else []
 try:
  cfg=config(root);chs={c['id']:c for c in rows if c.get('record_type')=='marked_chapter'};active={r['chapter_id']for r in cfg.values()};got={}
  for row in rows:
   for field in('assertions','records'):
    for v in row.get(field,[]):
     if v.get('archived_excerpt_fact_binding',{}).get('kind')==KIND:got.setdefault(row.get('chapter_id',v.get('chapter_id')),[]).append(v)
  assert set(got)<=active
  for cid in active:
   expected=records(chs[cid],root);actual=got.get(cid,[]);assert len(actual)==len(expected)and len({x['id']for x in actual})==len(actual);by={x['id']:x for x in expected};assert all(strict(x,by.get(x['id']))for x in actual);validate_names(chs[cid],root,rows)
  return []
 except(AssertionError,KeyError,IndexError,TypeError,ValueError,OSError,StopIteration,AttributeError):return ['既存節錄型事實須固定全選錄、原角色及姓名路徑；不是完整外部raw驗證']
