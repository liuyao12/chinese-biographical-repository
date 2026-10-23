# coding:utf-8
"""Finite source-role/name/age/place proofs for a pinned complete Kanripo unit.
No identity lookup by spelling, family ID, or inferred birth-year arithmetic.
"""
from pathlib import Path
import json,hashlib,re
PROOF_PATH='source-evidence/sgz016-du-finite-facts/proofs.json'
PROOF_SHA='69fe68e21ec93089dec6b2b2a719cb10e0f39260cd71edee9484a026a9c50736'
def load(root):
 p=Path(root).resolve()/PROOF_PATH;assert p.resolve()==p
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==PROOF_SHA
 return json.loads(b)
def anchor(a,chapter):
 p=next(p for p in chapter['paragraphs']if p['id']==a['paragraph_id'])
 assert hashlib.sha256(p['text'].encode()).hexdigest()==a['paragraph_sha256']
 assert p['source_position']['source_layer']==a['source_layer']
 assert type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])and p['text'][a['start']:a['end']]==a['surface']
 return p
def number(s):
 ds='一二三四五六七八九'
 if s in ds:return ds.index(s)+1
 if '十'in s:
  a,b=s.split('十');return(ds.index(a)+1 if a else 1)*10+(ds.index(b)+1 if b else 0)
 raise ValueError('來源數詞不在有限十進位語法')
def check(r,roles,out,ch,root):
 try:from scripts.fixed_kanripo_fact_slots import expand
 except ImportError:from fixed_kanripo_fact_slots import expand
 assert r['finite_biography_proofs']==dict(path=PROOF_PATH,sha256=PROOF_SHA)
 raw=load(root);w=raw[0]['fixed_witness'];assert w==dict(chapter_id=ch['id'],revision_id=r['source_revision'],raw_sha256=r['raw_sha256'],witness_key=r['witness_key']);proofs=[expand(p,roles)for p in raw];by={v['id']:v for v in out};ss={s['slot']:by[expand(s['record'],roles)['id']]for s in r['slots']}
 assert len(proofs)==27 and len({p['slot']for p in proofs})==27
 seedproof,=[p for p in proofs if p['kind']=='name'and p['full_name']];seed=ss[seedproof['slot']];assert seed['surname']+seed['ming']==seedproof['anchor']['surface']
 for p in proofs:
  v=ss[p['slot']];a=p['anchor'];paragraph=anchor(a,ch)
  assert v['person_id']==p['subject']and v['human_reviewed']is False and all(v.get(k)==value for k,value in p['expected_semantics'].items())
  hit=next(m for u in ch['paragraphs']for m in u['mentions']if m['id']==p['subject_mention']);assert hit['kind']=='person'and hit['person_id']==v['person_id']
  if p['kind']=='name':
   assert v['person_mention_id']==hit['id']and v['paragraph_id']==paragraph['id']and v['quote']==paragraph['text']
   z=p['zi_anchor'];assert anchor(z,ch)['id']==paragraph['id']and v['zi']==z['surface']and paragraph['text'][z['start']-1:z['start']]=='字'
   assert v['ming']==a['surface'][-1]and v['surname']==seed['surname']and a['start']==hit['start']and a['end']==hit['end']
   if p['full_name']:assert v['surname']+v['ming']==a['surface']and 'surname_basis' not in v
   else:
    b=v['surname_basis'];assert b['kind']=='contextual_surname_from_fixed_kanripo_slots'and b['status']=='contextual_provisional'and b['seed_name_record_id']==seed['id']and b['assertion_ids']==p['surname_path']and 1<=len(p['surname_path'])<=4
    cur=seed['person_id'];seen={cur}
    for aid in p['surname_path']:
     e=by[aid];expected=p['expected_surname_edges'][p['surname_path'].index(aid)];assert all(e[k]==value for k,value in expected.items());assert e['predicate']in('father','brother','agnatic_cousin')and e['evidence'][0]['chapter_id']==ch['id']
     x,y=e['subject_person_id'],e['object_person_id'];assert cur in(x,y)and x!=y
     cur=y if cur==x else x;assert cur not in seen;seen.add(cur)
    assert cur==v['person_id']
  else:
   assert v['source_term']==(a['surface'].removeprefix('以').removesuffix('而卒') if p['kind']=='age'else a['surface'])and any(e['paragraph_id']==paragraph['id']and e['quote']==paragraph['text']for e in v['evidence'])
   if p['kind']=='age':
    n=re.search('[一二三四五六七八九十]+',a['surface']).group();assert v['source_number']==n and type(v['value'])is int and v['value']==number(n)==p['value']and v['birth_year']is None and v['counting']=='unspecified_source_age'and v['date_expression']is None and'normalized_date'not in v
   elif p['kind']=='place':
    assert v['place']==dict(source_name=p['source_name'],modern_identification=None,place_id=None)
    if p.get('context_anchor'):anchor(p['context_anchor'],ch)
   else:
    assert v['event_type']=='death'
    if 'omitted_era'in p:assert date_valid(v['normalized_date'],v,ch,root,already_checked=True)
    else:assert v['date_expression']is None and'normalized_date'not in v
 return True
def date_valid(d,v,ch,root,already_checked=False):
 try:
  try:from scripts.fixed_kanripo_fact_slots import grammar,expand,valid
  except ImportError:from fixed_kanripo_fact_slots import grammar,expand,valid
  r,roles=grammar(ch,root);p,=[expand(p,roles)for p in load(root)if 'omitted_era'in p]
  spec=p['omitted_era'];assert v['person_id']==p['subject']and v['fixed_source_fact_binding']['slot']==p['slot']and v['event_type']=='death'and v['date_expression']==spec['source_expression']
  a=p['anchor'];anchor(a,ch);ordered=ch['paragraphs'];positions={q['id']:i for i,q in enumerate(ordered)};expected=spec['complete_body_interval'];first,last=positions[expected[0]['id']],positions[expected[-1]['id']]
  body=[q for q in ordered[first:last+1]if q['source_position']['source_layer']=='received_body']
  assert [{k:q[k]for k in('id','text','source_position')}for q in body]==expected
  for key in('antecedent_anchor','event_anchor','following_reset_anchor'):anchor(spec[key],ch)
  event=spec['event_anchor'];following=spec['following_reset_anchor'];assert event['paragraph_id']==following['paragraph_id']and event['end']==following['start']and event['surface'].startswith(spec['source_expression'])
  row,=[q for q in spec['basis']['rows']if q['era_name']==spec['inferred_era']];year=row['first_year']+number(spec['source_number'])-1
  assert year==spec['preferred_normalized_year']and d['year']==d['era_year']==year and d['era']=='CE'and d['year_numbering']=='astronomical'and d['precision']=='year'and d['calendar']=='chinese_civil'and d['source_expression']==spec['source_expression']and d['human_reviewed']is False
  assert d['regnal_year_mapping']==dict(kind='fixed_kanripo_body_interval_regnal_year',era_name=spec['inferred_era'],regnal_year=spec['regnal_year'],start_ce_year=row['first_year'],end_ce_year=row['last_year'],source_number=spec['source_number'],reference_index=0)
  ref=d['references'][0];assert ref['columns']==dict(dynasty=row['dynasty'],era_name=row['era_name'],first_year=str(row['first_year']),last_year=str(row['last_year']))and ref['url']==spec['basis']['url']and ref['scope']=='modern_era_year_equivalence_only'and ref['quote']==row['era_name']
  assert d['original_quote']==body[-1]['text']and d['evidence']==v['evidence']and d['status']=='editorial_provisional'
  if not already_checked:assert valid(v,ch,root)
  return True
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,OSError):return False
