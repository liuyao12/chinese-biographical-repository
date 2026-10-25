# coding: utf-8
"""Finite, complete fixed-witness role-bound person facts; trusted static data only."""
from pathlib import Path
import json,re,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
KIND='fixed_kanripo_person_fact_slots'
RECIPE_PATH=Path(__file__).with_name('fixed_kanripo_fact_slots.json')
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
 return a==b
def recipe_for(key,root=ROOT):
 legacy=json.loads(RECIPE_PATH.read_text())
 if key==legacy['key']:return legacy,False
 path=Path(root).resolve()/'scripts/fixed_kanripo_additional_fact_slots.json';assert path.resolve()==path and path.is_file()
 d=json.loads(path.read_text());assert d['format_version']=='0.1'and isinstance(d['recipes'],dict)and key in d['recipes']
 r=d['recipes'][key];assert r['key']==key and r['kind']==KIND
 return r,True
def grammar(ch,root=ROOT):
 try:from scripts.fixed_kanripo_projection import errors
 except ImportError:from fixed_kanripo_projection import errors
 r,additional=recipe_for(ch['annotation']['fixed_kanripo_fact_slots_ref']['key'],root);assert ch['annotation']['fixed_kanripo_fact_slots_ref']==dict(kind=KIND,key=r['key'])
 assert ch['annotation'].get('fixed_kanripo_projection_ref')and not errors(ch,root)
 projection=json.loads((Path(root)/ch['annotation']['fixed_kanripo_projection_ref']).read_text())
 raw_path=Path(projection['raw_file']if additional else ch['source']['raw_path']);assert not raw_path.is_absolute()and raw_path.parts[0]=='source-evidence'and'..'not in raw_path.parts
 raw_file=Path(root).resolve()/raw_path;assert raw_file.resolve()==raw_file and projection['raw_file']==str(raw_path)
 assert ch['source']['revision_id']==r['source_revision']and hashlib.sha256(raw_file.read_bytes()).hexdigest()==r['raw_sha256']
 if additional:
  pinpath=Path(root).resolve()/'scripts/fixed_kanripo_witness_pins.json';assert pinpath.resolve()==pinpath and pinpath.is_file();pins=json.loads(pinpath.read_text())
  assert pins['chapter_bindings'][ch['id']]==projection['witness_key']==r['witness_key']and pins['witnesses'][r['witness_key']]['raw_sha256']==r['raw_sha256']
  assert projection['raw_file_sha256']==ch['source']['response_sha256']==r['raw_sha256']
  assert len(r['paragraph_layers'])==len(ch['paragraphs'])and all(p['text_layer']==layer['text_layer']and p['source_position']['source_layer']==layer['source_layer']for p,layer in zip(ch['paragraphs'],r['paragraph_layers']))
 else:assert ch['source']['raw_file_sha256']==r['raw_sha256']
 assert len(ch['paragraphs'])==len(r['paragraphs']);roles=[]
 for p,pattern in zip(ch['paragraphs'],r['paragraphs']):
  mm=[m for m in p['mentions']if m['kind']=='person'];pos=0;used=[]
  for part in re.split(r'(<r[0-9]+>)',pattern):
   if re.fullmatch(r'<r[0-9]+>',part):
    i=int(part[2:-1]);m=mm[i];assert m['start']==pos and p['text'][pos:m['end']]==m['surface'];pos=m['end'];used.append(i)
   else:assert p['text'].startswith(part,pos);pos+=len(part)
  assert pos==len(p['text'])and used==list(range(len(mm)));roles.append(mm)
 if additional:
  for group in r['same_person_groups']:
   assert len(group)>=2 and len({roles[i][j]['person_id']for i,j in group})==1
 return r,roles
def expand(v,roles):
 if isinstance(v,dict):
  if set(v)in ({'$person'},{'$mention'}):
   key=next(iter(v));p,m=v[key];return roles[p][m]['person_id'if key=='$person'else'id']
  return {k:expand(x,roles)for k,x in v.items()}
 if isinstance(v,list):return [expand(x,roles)for x in v]
 return v
def records(ch,root=ROOT):
 r,roles=grammar(ch,root);out=[expand(s['record'],roles)for s in r['slots']];assert len({v['id']for v in out})==len(out)
 if 'finite_biography_proofs'in r:
  try:from scripts.fixed_kanripo_biographical_facts import check
  except ImportError:from fixed_kanripo_biographical_facts import check
  assert check(r,roles,out,ch,root)
 hs={v['id']:v for v in out if 'title'in v and'attestations'in v}
 for v in out:
  link=v.get('values',{}).get('linked_holding_id')
  if link:assert link in hs and hs[link]['person_id']==v['person_id']
 for v in out:
  d=v.get('effective_period',{}).get('start',{}).get('normalized_date',{})
  if d.get('regnal_year_mapping',{}).get('kind')=='fixed_kanripo_accession_ce_year':
   try:from scripts.fixed_kanripo_accession_dates import bound_valid
   except ImportError:from fixed_kanripo_accession_dates import bound_valid
   assert bound_valid(d,v,ch,root),'固定本紀即位紀年須綁同人官爵原句與年份，不借下年改元'
 return out
def valid(v,ch,root=ROOT):
 try:
  b=v['fixed_source_fact_binding'];assert b['kind']==KIND
  expected,=[a for a in records(ch,root)if a['id']==v['id']];return strict(v,expected)
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):return False
def errors(root,rows):
 chs={c['id']:c for c in rows if c.get('record_type')=='marked_chapter'};out=[];got={}
 for row in rows:
  for field in ('assertions','holdings','records','events'):
   for v in row.get(field,[]):
    if v.get('fixed_source_fact_binding',{}).get('kind')==KIND:got.setdefault(row.get('chapter_id'),[]).append(v)
 for cid,ch in chs.items():
  for field in ('age_assertions','title_proposals'):
   for v in ch.get('annotation',{}).get(field,[]):
    if v.get('fixed_source_fact_binding',{}).get('kind')==KIND:got.setdefault(cid,[]).append(v)
 active={cid for cid,ch in chs.items()if ch.get('annotation',{}).get('fixed_kanripo_fact_slots_ref',{}).get('kind')==KIND}
 for cid in set(got)-active:out.append('固定Kanripo人物事實缺完整來源範圍:'+str(cid))
 for cid in active:
  try:
   expected=records(chs[cid],root);actual=got.get(cid,[]);assert len(actual)==len(expected)and len({v['id']for v in actual})==len(actual)
   wd={v['id']:v for v in expected}
   assert all(strict(v,wd.get(v.get('id')))for v in actual)
  except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):out.append('固定Kanripo完整事實須逐原角色、原詞、層次及紀年；不得移人、漏項或重複')
 return out

def valid_from_paragraphs(v,paragraphs,root=ROOT):
 try:
  key=v['fixed_source_fact_binding'].get('key');r,_=recipe_for(key,root)if key is not None else(json.loads(RECIPE_PATH.read_text()),False);rel=Path(r['chapter_path']);assert not rel.is_absolute()and rel.parts[0]=='corpus'and'..'not in rel.parts;path=Path(root).resolve()/rel;assert path.resolve()==path;ch=json.loads(path.read_text())
  assert all(paragraphs[p['id']]==(ch['id'],p)for p in ch['paragraphs'])
  return valid(v,ch,root)
 except(AssertionError,KeyError,ValueError,TypeError,OSError):return False

def inherited_surface_valid(h,a,ch,holdings,relations,root):
 """Resolve an omitted rank only through a trusted source succession and father."""
 try:
  assert root is not None and valid(h,ch,root)
  recipe,roles=grammar(ch,root);expected={v['id']:v for v in records(ch,root)}
  link,=[x for x in recipe.get('succession_links',[])if x['holding_id']==h['id']]
  assert set(link)=={'holding_id','event_id','father_assertion_id','predecessor_holding_id'}
  binding=h['inherited_title_binding'];i=h['inheritance'];raw=expected[h['id']]['inherited_title_binding']['raw_surface'];assert isinstance(raw,str)and raw
  assert binding==dict(kind='fixed_kanripo_named_father_rank_succession',father_assertion_id=link['father_assertion_id'],predecessor_holding_id=link['predecessor_holding_id'],raw_surface=raw,succession_event_id=link['event_id'])
  parent=holdings[link['predecessor_holding_id']];father,=[v for v in relations if v['id']==link['father_assertion_id']]
  assert strict(parent,expected[parent['id']])and valid(parent,ch,root)and strict(father,expected[father['id']])and valid(father,ch,root)
  assert father['predicate']=='father'and father['subject_person_id']==h['person_id']and father['object_person_id']==parent['person_id']==i['predecessor_person_id']
  assert parent['kind']==h['kind']=='noble_rank'and not parent['mode'].startswith('posthumous')and parent['title']==h['title']==i['resolved_title']and h['mode']=='accession'
  # The event is read from its real native sidecar; a trusted recipe alone cannot hide a broken reciprocal link.
  rel=Path(recipe['chapter_path']);ep=Path(root).resolve()/rel.with_name(rel.stem+'-person-events.json');assert ep.resolve()==ep
  payload=json.loads(ep.read_bytes());assert payload['record_type']=='person_event_assertion_set'and payload['chapter_id']==ch['id']
  event,=[v for v in payload['events']if v['id']==link['event_id']]
  assert strict(event,expected[event['id']])and valid(event,ch,root)and event['person_id']==h['person_id']and event['title_holding_id']==h['id']
  eb=event['source_succession_binding'];assert eb==dict(kind=binding['kind'],predecessor_holding_id=parent['id'],father_assertion_id=father['id'],resolved_title=h['title'],interpretation_status='contextual_provisional',human_reviewed=False)
  assert event['date_expression']is None and'normalized_date'not in event and'normalized_date_range'not in event
  assert h['effective_period']==dict(start=dict(status='source_event',event_type='accession',date_expression=None,evidence=h['evidence']),end=dict(status='unknown',date_expression=None,evidence=[]))
  assert a==h['attestations'][0]and a['surface']==raw and a['date_expression']is None and a['person_mention_id']==event['evidence'][0]['person_mention_id']
  p,=[p for p in ch['paragraphs']if p['id']==a['paragraph_id']];assert p['text'][a['start']:a['end']]==raw
  ea=event['source_anchor'];assert event['source_term'].endswith(raw)and ea['paragraph_id']==a['paragraph_id']and ea['start']<=a['start']<a['end']<=ea['end']
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,OSError):return False

def noble_replacement_valid(h,holdings,paragraphs,mentions,chapters,root):
 """Only reviewed, complete-source rank changes close a specific former rank."""
 try:
  assert root is not None and isinstance(chapters,dict)
  ch=chapters[h['evidence'][0]['chapter_id']];assert valid(h,ch,root)
  recipe,roles=grammar(ch,root);expected={v['id']:v for v in records(ch,root)}
  link,=[x for x in recipe.get('noble_replacement_links',[])if x['successor_holding_id']==h['id']]
  previous=holdings[link['previous_holding_id']];b=h['transfer_basis'];assert strict(previous,expected[previous['id']])and valid(previous,ch,root)
  assert h['previous_holding_id']==b['previous_holding_id']==previous['id']and previous['id']!=h['id']
  assert h['kind']==previous['kind']=='noble_rank'and h['person_id']==previous['person_id']and not previous['mode'].startswith('posthumous')
  assert b['kind']=='fixed_source_noble_replacement'and b['previous_title_status']=='source_context'and b['status']=='contextual_provisional'and b['human_reviewed']is False
  status=link['interpretation_status'];assert b['interpretation_status']==status
  assert status in('explicit_source_transfer','contextual_source_rank_progression')
  term=link['source_term'];title=h['title'];assert isinstance(term,str)and isinstance(title,str)and title and term.endswith(title)
  prefix=term[:-len(title)];assert prefix in (('轉封','改封')if status=='explicit_source_transfer'else('進封',))
  assert h['mode']==('transfer'if status=='explicit_source_transfer'else'grant')and b['source_term']==link['source_term']==prefix+h['title']
  a=h['attestations'][0];p,=[p for p in ch['paragraphs']if p['id']==a['paragraph_id']];assert p['text'][a['start']-len(prefix):a['end']]==b['source_term']
  actor,=[m for m in p['mentions']if m['id']==b['actor_mention_id']];assert actor['person_id']==h['person_id']
  start=h['effective_period']['start'];end=previous['effective_period']['end'];assert start['status']=='source_event'and start['event_type']==h['mode']and end['status']=='source_event'and end['event_type']=='explicit_end'
  assert b['evidence']==h['evidence']==start['evidence']==end['evidence']and all(end.get(k)==start.get(k)for k in('date_expression','normalized_date','normalized_date_range'))
  # Follow only explicit trusted change edges; accidental cycles cannot close every title.
  nxt={x['previous_holding_id']:x['successor_holding_id']for x in recipe.get('noble_replacement_links',[])};assert len(nxt)==len(recipe.get('noble_replacement_links',[]));seen=set();cur=previous['id']
  while cur in nxt:assert cur not in seen;seen.add(cur);cur=nxt[cur]
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,OSError):return False

# Preserve the complete core-v1 implementation for unchanged, open-ended cases.
_core_v1_inherited_surface_valid = inherited_surface_valid

def _replacement_qualified_inherited_surface_valid(h,a,ch,holdings,relations,root):
 try:
  assert root is not None and valid(h,ch,root)
  recipe,roles=grammar(ch,root);expected={v['id']:v for v in records(ch,root)}
  link,=[x for x in recipe.get('succession_links',[])if x['holding_id']==h['id']]
  binding=h['inherited_title_binding'];i=h['inheritance'];raw=expected[h['id']]['inherited_title_binding']['raw_surface'];assert isinstance(raw,str)and raw
  assert binding==dict(kind='fixed_kanripo_named_father_rank_succession',father_assertion_id=link['father_assertion_id'],predecessor_holding_id=link['predecessor_holding_id'],raw_surface=raw,succession_event_id=link['event_id'])
  parent=holdings[link['predecessor_holding_id']];father,=[v for v in relations if v['id']==link['father_assertion_id']]
  assert strict(parent,expected[parent['id']])and valid(parent,ch,root)and strict(father,expected[father['id']])and valid(father,ch,root)
  assert father['predicate']=='father'and father['subject_person_id']==h['person_id']and father['object_person_id']==parent['person_id']==i['predecessor_person_id']
  assert parent['kind']==h['kind']=='noble_rank'and not parent['mode'].startswith('posthumous')and parent['title']==h['title']==i['resolved_title']and h['mode']=='accession'
  path=Path(root).resolve()/Path(recipe['chapter_path']).with_name(Path(recipe['chapter_path']).stem+'-person-events.json');assert path.resolve()==path
  payload=json.loads(path.read_bytes());assert payload['record_type']=='person_event_assertion_set'and payload['chapter_id']==ch['id'];event,=[v for v in payload['events']if v['id']==link['event_id']]
  assert strict(event,expected[event['id']])and valid(event,ch,root)and event['person_id']==h['person_id']and event['title_holding_id']==h['id']
  assert event['source_succession_binding']==dict(kind=binding['kind'],predecessor_holding_id=parent['id'],father_assertion_id=father['id'],resolved_title=h['title'],interpretation_status='contextual_provisional',human_reviewed=False)
  assert event['date_expression']is None and'normalized_date'not in event and'normalized_date_range'not in event
  assert h['effective_period']['start']==dict(status='source_event',event_type='accession',date_expression=None,evidence=h['evidence'])
  successors=[x for x in recipe.get('noble_replacement_links',[])if x['previous_holding_id']==h['id']];assert len(successors)==1
  next_h=holdings[successors[0]['successor_holding_id']];assert noble_replacement_valid(next_h,holdings,{}, {},{ch['id']:ch},root)
  assert a==h['attestations'][0]and a['surface']==raw and a['date_expression']is None and a['person_mention_id']==event['evidence'][0]['person_mention_id'];p,=[p for p in ch['paragraphs']if p['id']==a['paragraph_id']];assert p['text'][a['start']:a['end']]==raw
  ea=event['source_anchor'];assert event['source_term'].endswith(raw)and ea['paragraph_id']==a['paragraph_id']and ea['start']<=a['start']<a['end']<=ea['end']
  return True
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,StopIteration,OSError):return False

def inherited_surface_valid(h,a,ch,holdings,relations,root):
 try:
  assert isinstance(h,dict)and isinstance(ch,dict)and root is not None
  recipe,roles=grammar(ch,root);rel=Path(recipe['chapter_path']);assert not rel.is_absolute()and'..'not in rel.parts and rel.parts[0]=='corpus'
  if h.get('effective_period',{}).get('end',{}).get('status')=='unknown':return _core_v1_inherited_surface_valid(h,a,ch,holdings,relations,root)
  return _replacement_qualified_inherited_surface_valid(h,a,ch,holdings,relations,root)
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,OSError):return False
