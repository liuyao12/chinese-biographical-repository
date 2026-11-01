"""Six near Lu roles, source-bound family placement and exact current endpoint rekey.

Received Pei/Liu quotations stay distinct; opaque IDs and historical bytes never move.
"""
import copy,hashlib,json
from pathlib import Path
try:from scripts.liang_xiao_close_family import same,expand,typed_projection,raw,read
except ImportError:from liang_xiao_close_family import same,expand,typed_projection,raw,read
REF='source-evidence/lu-six-near-family/family-source-contract.json'
SHA='60b2d3866ce39058d13cb35f2a509693ceb545e9ff93b016dc0754da39608b69'
KIND='fixed_lu_six_near_family'

def active(root):return(Path(root)/REF).is_file()

def contract(root):
 b=raw(root,REF);assert hashlib.sha256(b).hexdigest()==SHA;c=json.loads(b)
 for path,key in [('ledger_path','ledger_sha256'),('retirement_receipt_path','retirement_receipt_sha256')]:assert hashlib.sha256(raw(root,c[path])).hexdigest()==c[key]
 units=read(root,c['ledger_path']);assert len(units)==3
 assert all(u['human_reviewed']is False and u['image_verified']is False for u in units)
 assert units[0]['raw_received']is False and units[1]['raw_received']is False and units[2]['original_wikitext_obtained']is False
 assert '逊祖纡，字叔盘' in units[0]['observed_text']and'父骏，字季才'in units[0]['observed_text']
 assert '次子抗襲爵'in units[1]['observed_text']
 assert '雲字士龍，吳大司馬抗之第五子，機同母之弟也'in units[2]['complete_item_text']
 assert '按蔡所論士十六人，無陸機兄弟'in units[2]['complete_item_text']
 assert '周俊命為主簿'in units[2]['complete_item_text']and'年十八'in units[2]['complete_item_text']
 return c

def _native_additions(root,prior,ownids,physical,source_dirs=None,records=None):
 # Locate only newly claimed registered chapters. Trusted existing chapter paths
 # provide work directories; no volume/filename or permanent person-ID rule.
 additions={pid:[]for pid in prior};works={w['id']:w for w in read(root,'registry/works.json')['works']};bases=read(root,'registry/work-provenance.json')['text_bases'];required={};seen=set()
 for pid,oldmids in prior.items():
  for e in physical[pid]['evidence']:
   if e.get('chapter_id')in ownids or e.get('mention_id')in oldmids:continue
   w=works[e['work_id']];book,=[b for b in w['books']if b['id']==e['book_id']];assert e['chapter_id']in book['chapter_ids']and bases[e['source_id']]['work_id']==e['work_id']
   required[e['chapter_id']]=e['work_id']
 # Caller rows can request a missing-source candidate, never supply authority.
 for ch in records or[]:
  if not isinstance(ch,dict)or ch.get('record_type')!='marked_chapter'or ch.get('id')in ownids:continue
  for p in ch.get('paragraphs',[]):
   for m in p.get('mentions',[]):
    pid=m.get('person_id')
    if isinstance(pid,str)and pid in prior and m.get('id')not in prior[pid]:required[ch['id']]=ch['work_id']
 if not required:return additions
 paths=[]
 for wid in set(required.values()):
  for directory in sorted((source_dirs or{}).get(wid,())):paths.extend(sorted((Path(root)/directory).glob('*.json')))
 # Fallback lookup supports a registered work's newly introduced directory.
 # Stop once required chapter IDs are located; normal native checks own global
 # chapter/raw fidelity and all other sources, not this additive reverse check.
 paths.extend(sorted((Path(root)/'corpus').glob('*/*.json')));visited=set();found=set()
 for path in paths:
  if path in visited:continue
  visited.add(path);ch=read(root,str(path.relative_to(root)))
  if not isinstance(ch,dict)or ch.get('record_type')!='marked_chapter'or ch.get('id')not in required:continue
  assert ch['work_id']==required[ch['id']];found.add(ch['id'])
  for p in ch['paragraphs']:
   for m in p['mentions']:
    pid=m.get('person_id')
    if not isinstance(pid,str)or pid not in prior or m['id']in prior[pid]:continue
    assert m['kind']in('person','pronoun')and m['id']not in seen;seen.add(m['id'])
    assert type(m['start'])is int and type(m['end'])is int and 0<=m['start']<m['end']<=len(p['text'])and p['text'][m['start']:m['end']]==m['surface']
    work=works[ch['work_id']];book,=[b for b in work['books']if b['id']==ch['book_id']];assert ch['id']in book['chapter_ids']and bases[ch['source_id']]['work_id']==ch['work_id']and bases[ch['source_id']]['source_id']==ch['source_id']
    e=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface']);additions[pid].append((e,m))
  if found==set(required):break
 assert found==set(required)
 return additions

def _external_growth_valid(actor,want,ownids,ownmids,additions,physical):
 actual=[e for e in actor['evidence']if e.get('chapter_id')not in ownids];oldmids={e['mention_id']for e in want['evidence']};newmids={e['mention_id']for e,m in additions}
 assert not oldmids&newmids and len(newmids)==len(additions)
 assert same([e for e in actual if e.get('mention_id')in oldmids],want['evidence'])
 assert len(actual)==len(want['evidence'])+len(additions)
 for e,m in additions:
  assert m['person_id']==actor['id']and e['mention_id']==m['id']and e['quote']==m['surface']
  assert same([x for x in actual if x.get('mention_id')==m['id']],[e])
  assert[(pid,x)for pid,p in physical.items()for x in p.get('evidence',[])if x.get('mention_id')==m['id']]==[(actor['id'],e)]
  aliases=[(pid,a)for pid,p in physical.items()for a in p.get('aliases',[])if m['id']in a.get('mention_ids',[])]
  if m['kind']=='person':assert len(aliases)==1 and aliases[0][0]==actor['id']and aliases[0][1]['surface']==m['surface']and aliases[0][1]['mention_ids'].count(m['id'])==1
  else:assert not aliases
 aliases=[]
 for a in actor['aliases']:
  mids=[mid for mid in a['mention_ids']if mid not in ownmids and mid not in newmids]
  if mids:aliases.append(dict(surface=a['surface'],mention_ids=mids))
 assert same(aliases,want['aliases'])

def proof(root,people=None,records=None):
 c=contract(root)
 physical={p['id']:p for p in read(root,'registry/persons.json')['persons']}
 if people is None:people=physical
 roles={}
 for role,s in c['role_seeds'].items():
  ch=read(root,s['path']);p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];m,=[m for m in p['mentions']if m['id']==s['marker']['id']]
  assert p['text']==s['text']and same({k:v for k,v in m.items()if k!='person_id'},s['marker']);pid=m['person_id'];assert pid in people;roles['$'+role]=pid
  assert[e for e in people[pid]['evidence']if e.get('mention_id')==m['id']]==[s['reverse']]
  assert any(a['surface']==m['surface']and m['id']in a['mention_ids']for a in people[pid]['aliases'])
 for role,s in c['new_role_mids'].items():
  ch=read(root,s['path']);p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];m,=[m for m in p['mentions']if m['id']==s['mid']];assert m['kind']=='person'and m['person_id']in people;roles['$'+role]=m['person_id']
 assert len(set(roles.values()))==6
 assert all(pid in people and same(people[pid],physical[pid])for pid in roles.values())
 try:from scripts.person_ids import valid_person_id,family_path_errors
 except ImportError:from person_ids import valid_person_id,family_path_errors
 assert len(roles['$yu'])==11 and valid_person_id(roles['$yu'])
 parents={'jun':'yu','xun':'jun','kang':'xun','ji':'kang','yun':'kang'}
 assert all(not family_path_errors(roles['$'+k],{'connection':'father','parent_person_id':roles['$'+p]})for k,p in parents.items())
 mapping={old:roles['$'+r]for old,r in c['historical_old_id_role_map'].items()};assert not set(mapping)&set(people)
 # Other current owners can coherently move their own endpoints; source MIDs bind them.
 source_dirs={}
 for a in c['archives']:
  if a['kind']=='registry'or not a['path'].endswith('.json'):continue
  before=read(root,a['before_capture'])
  if before.get('record_type')!='marked_chapter':continue
  now=read(root,a['path']);source_dirs.setdefault(now['work_id'],set()).add(str(Path(a['path']).parent));oldm={m['id']:m for p in before['paragraphs']for m in p['mentions']};newm={m['id']:m for p in now['paragraphs']for m in p['mentions']};assert oldm.keys()==newm.keys()
  for mid,om in oldm.items():
   nm=newm[mid];assert all(same(om.get(k),nm.get(k))for k in ('id','start','end','surface','kind','source_role'))
   if om.get('kind')in('person','pronoun'):
    old,new=om['person_id'],nm['person_id'];assert new in people
    if old in mapping:assert mapping[old]==new
    else:mapping[old]=new
 for rel,h in c['immutable_prior_capture_hashes'].items():
  if hashlib.sha256(raw(root,rel)).hexdigest()==h:continue
  try:from scripts.fixed_jin037_gaomi_nanyang import legacy_projection_valid
  except ImportError:from fixed_jin037_gaomi_nanyang import legacy_projection_valid
  assert legacy_projection_valid(root,rel,h)
 for a in c['archives']:
  b=raw(root,a['before_capture']);assert hashlib.sha256(b).hexdigest()==a['before_sha256']
  if a['kind']=='registry'or a['path']=='registry/works.json':continue
  if a['path'].endswith('.json'):assert same(read(root,a['path']),typed_projection(json.loads(b),mapping))
  else:
   text=b.decode()
   for old,new in mapping.items():text=text.replace('ref="'+old+'"','ref="'+new+'"')
   assert raw(root,a['path']).decode()==text
 pref=expand(c['preferred_reading_template'],roles);assert same(read(root,c['preferred_reading_path']),pref)
 sources={p:expand(t,roles)for p,t in c['source_templates'].items()};sidecars={p:expand(t,roles)for p,t in c['sidecar_templates'].items()};ns=expand(c['name_set_template'],roles)
 for rel,want in {**sources,**sidecars,c['name_path']:ns}.items():assert same(read(root,rel),want)
 units=read(root,c['ledger_path']);ownids={ch['id']for ch in sources.values()};midmap={m['id']:(ch,p,m)for ch in sources.values()for p in ch['paragraphs']for m in p['mentions']}
 for ch in sources.values():
  for p in ch['paragraphs']:
   q=p['received_unit_fragment'];u=units[q['unit_index']];whole=u.get('observed_text',u.get('complete_item_text'));assert p['text']==whole[q['start']:q['end']]
   end=0
   for m in p['mentions']:assert end<=m['start']<m['end']and p['text'][m['start']:m['end']]==m['surface'];end=m['end']
 # Existing actor unknown metadata and all earlier source reverse/aliases are conserved.
 base=read(root,next(a['before_capture']for a in c['archives']if a['kind']=='registry'));byold={p['id']:p for p in base['persons']}
 prior={roles['$'+role]:{e['mention_id']for e in byold[old]['evidence']}for old,role in c['historical_old_id_role_map'].items()}
 for role,t in c['new_people_templates'].items():prior[roles['$'+role]]={e['mention_id']for e in expand(t,roles)['evidence']}
 additions=_native_additions(root,prior,ownids,physical,source_dirs,records)
 for old,role in c['historical_old_id_role_map'].items():
  want=typed_projection(byold[old],mapping);actor=people[roles['$'+role]]
  assert same({k:v for k,v in actor.items()if k not in('aliases','evidence','family_path')},{k:v for k,v in want.items()if k not in('aliases','evidence','family_path')})
  _external_growth_valid(actor,want,ownids,midmap,additions[actor['id']],physical)
 for role,t in c['new_people_templates'].items():
  actor=people[roles['$'+role]];want=expand(t,roles)
  assert same({k:v for k,v in actor.items()if k not in('aliases','evidence')},{k:v for k,v in want.items()if k not in('aliases','evidence')})
  want=dict(want,evidence=[e for e in want['evidence']if e.get('chapter_id')not in ownids],aliases=[dict(surface=a['surface'],mention_ids=[mid for mid in a['mention_ids']if mid not in midmap])for a in want['aliases']if any(mid not in midmap for mid in a['mention_ids'])])
  _external_growth_valid(actor,want,ownids,midmap,additions[actor['id']],physical)
 for role,t in c['family_path_templates'].items():assert same(people[roles['$'+role]].get('family_path'),expand(t,roles))
 for pid,actor in people.items():
  assert not set(actor.get('id_aliases',[]))&set(c['historical_old_id_role_map'])
  want=[dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=p['id'],mention_id=m['id'],quote=m['surface'])for ch,p,m in midmap.values()if m['person_id']==pid]
  assert same([e for e in actor['evidence']if e.get('chapter_id')in ownids],want)
  als={}
  for ch,p,m in midmap.values():
   if m['person_id']==pid:als.setdefault(m['surface'],[]).append(m['id'])
  actual={a['surface']:[mid for mid in a['mention_ids']if mid in midmap]for a in actor['aliases']if any(mid in midmap for mid in a['mention_ids'])};assert same(actual,als)
 works={w['id']:w for w in read(root,'registry/works.json')['works']};progress=read(root,'corpus/progress.json')['books'];bases=read(root,'registry/work-provenance.json')['text_bases']
 for ch in sources.values():
  w=works[ch['work_id']];book,=[b for b in w['books']if b['id']==ch['book_id']];assert ch['id']in book['chapter_ids']and bases[ch['source_id']]['status']=='unknown'and bases[ch['source_id']]['edition_id']is None
  row,=[p for p in progress if p['chapter_id']==ch['id']];assert row['complete']is False and row['person_status']=='in_progress'
  assert same(book,c['own_book_rows'][ch['book_id']])and same(row,c['own_progress_rows'][ch['id']])and same(bases[ch['source_id']],c['own_text_base_rows'][ch['source_id']])
 if records is not None:
  for want in [*sources.values(),*sidecars.values(),ns,pref]:assert sum(same(x,want)for x in records)==1
 return c,roles,sources,sidecars,ns

def errors(root):
 if not active(root):return[]
 try:proof(root);return[]
 except(AssertionError,KeyError,ValueError,TypeError,OSError,IndexError,StopIteration):return['陸氏近六人來源層/明父與祖父推導/第五子與同母弟/真實全引用重鍵或反查不符']

def family_applies(a):return a.get('qualifiers',{}).get('source_clause_binding',{}).get('kind')==KIND

def family_valid(a,paragraphs,root):
 if not family_applies(a):return False
 try:
  _,_,sources,sidecars,_=proof(root);assert sum(same(a,x)for s in sidecars.values()for x in s['assertions'])==1
  e,=a['evidence'];_,p=paragraphs[e['paragraph_id']];assert same(p,next(p for ch in sources.values()for p in ch['paragraphs']if p['id']==e['paragraph_id']));return True
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False

def family_path_valid(root,pid,path):
 if not active(root):return False
 try:
  c,r,*_=proof(root);return any(r['$'+role]==pid and same(path,expand(t,r))for role,t in c['family_path_templates'].items())
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False

def validate_surname(name,names,chapters,assertions,root=None):
 assert root is not None
 _,_,sources,_,ns=proof(root);assert sum(same(name,n)for n in ns['records'])==1 and all(n in names for n in ns['records'])
 for ch in sources.values():assert same(chapters[ch['id']],ch)
 return None

def layer_valid(ch,p,root):
 try:
  _,_,sources,_,_=proof(root);return p['text_layer']=='witness_appended_liuxiaobiao_note'and any(same(ch,s)and p in s['paragraphs']for s in sources.values())
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return False

def guard_bundle(root,pid,people,records):
 if not active(root):return
 c=contract(root);owned=set()
 for s in [*c['role_seeds'].values(),*c['new_role_mids'].values()]:
  ch=read(root,s['path']);p,=[p for p in ch['paragraphs']if p['id']==s['paragraph_id']];mid=s.get('mid',s.get('marker',{}).get('id'));m,=[m for m in p['mentions']if m['id']==mid];owned.add(m['person_id'])
 if pid in owned:proof(root,people=people,records=records)


def preferred_reading_errors(reading,names,chapters,root):
 try:
  c,r,sources,_,ns=proof(root);pref=expand(c['preferred_reading_template'],r)
  assert sum(same(reading,x)for x in pref['readings'])==1
  assert all(n in names for n in ns['records'])
  for ch in sources.values():assert same(chapters[ch['id']],ch)
  assert reading['basis']['not_an_additional_received_witness']is True
  return []
 except(AssertionError,KeyError,ValueError,TypeError,OSError,StopIteration):return ['Source-bound Lu glyph display reading must retain its exact received record, anchors and declared conversion qualification']
