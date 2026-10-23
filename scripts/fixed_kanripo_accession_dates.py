# coding: utf-8
"""A fixed annal accession dates only its source-bound local appointment, never ends."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
KIND='fixed_kanripo_accession_ce_year'
PROOF_PATH='source-evidence/sgz025-xinpi-accession-dates/primary-proofs.json'
PROOF_SHA='3c5eeb72d6cec9c9d274b57ab5126dce7033789e337c3c6d6bbf5029ab7e9b1c'
def proofs(root):
 root=Path(root).resolve();p=root/PROOF_PATH;assert p.resolve()==p;b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==PROOF_SHA
 d=json.loads(b);assert d['record_type']=='fixed_accession_annal_proofs'and d['human_reviewed']is False and d['image_verified']is False
 return d['proofs']
def bound_valid(date,h,ch,root=ROOT):
 try:
  root=Path(root or ROOT).resolve();b=date['source_accession_year_binding'];ref=proofs(root)[b['reference_key']]
  assert b['kind']==KIND and b['human_reviewed']is False and b['holding_id']==h['id']and b['person_id']==h['person_id']and b['source_revision']==ch['source']['revision_id']==ref['revision']
  assert h['fixed_source_fact_binding']['kind']=='fixed_kanripo_person_fact_slots'and h['kind']in('office','noble_rank')and h['mode']in('grant','transfer')
  start=h['effective_period']['start'];assert start['normalized_date']==date and start['status']=='source_event'and start['event_type']==h['mode']and h['effective_period']['end']==dict(status='unknown',date_expression=None,evidence=[])
  ev,=h['evidence'];assert date['evidence']==h['evidence']==start['evidence']and all(ev[k]==ch[k]for k in ('work_id','book_id','source_id'))and ev['chapter_id']==ch['id']
  p=next(p for p in ch['paragraphs']if p['id']==ev['paragraph_id']);ms={m['id']:m for m in p['mentions']};person=ms[ev['person_mention_id']];ruler=ms[b['ruler_mention_id']]
  assert person['kind']==ruler['kind']=='person'and person['person_id']==h['person_id']and ruler['person_id']==b['ruler_person_id']and ruler['surface'].endswith('帝')
  assert ev['quote']==date['original_quote']==p['text']and date['source_expression']==start['date_expression']
  anchor=b['source_event_anchor'];assert set(anchor)=={'paragraph_id','start','end','surface'}and anchor['paragraph_id']==p['id']and type(anchor['start'])is int and type(anchor['end'])is int and p['text'][anchor['start']:anchor['end']]==anchor['surface']and anchor['start']==ruler['start']
  suffix={'imperial_accession':'踐阼','successor_accession':'即位'}[ref['event_kind']];assert date['source_expression']==ruler['surface']+suffix and anchor['surface'].startswith(date['source_expression'])
  a,=h['attestations'];assert a['paragraph_id']==p['id']and a['person_mention_id']==person['id']and anchor['start']<=a['start']<a['end']<=anchor['end']and p['text'][a['start']:a['end']]==a['surface']==h['title']
  assert ref['head']['quote'].startswith(ruler['surface'][:-1]+'皇帝諱')and ref['head']['quote'].endswith('太子也')
  raw=Path(ref['path']);assert not raw.is_absolute()and'..'not in raw.parts and raw.parts[0]=='source-evidence';dest=root/raw;assert dest.resolve()==dest
  try:from scripts.role_event_year_bridge import point,number
  except ImportError:from role_event_year_bridge import point,number
  year=point(ref,root);m=ref['mapping'];assert type(date['year'])is int and date['era']== 'CE'and date['year']==date['era_year']==year and date['precision']=='year'and date['calendar']=='chinese_civil'and date['year_numbering']=='astronomical'and date['status']=='editorial_provisional'and date['human_reviewed']is False
  assert type(date['era_year'])is int and all(type(date['regnal_year_mapping'].get(k))is int for k in('regnal_year','start_ce_year','end_ce_year','reference_index'))
  assert date['regnal_year_mapping']==dict(kind=KIND,era_name=m['era_name'],source_era_name=m['source_era_name'],source_number=m['source_number'],regnal_year=number(m['source_number']),start_ce_year=m['first'],end_ce_year=m['last'],reference_index=0)
  assert date['references']==[ref['calendar_reference'],dict(url=ref['url'],quote=ref['event']['quote'],scope='received_parallel_event'),dict(url=ref['url'],quote=ref['year']['quote'],scope='received_regnal_year_attestation')]
  assert date['basis']==dict(kind='parallel_event',source_event_quote=anchor['surface'],reference_url=ref['url'],reference_event_quote=ref['event']['quote'],reference_year_quote=ref['year']['quote'])
  assert not any(k in date for k in('month','day','lunar_month','lunar_day','source_month_number'))
  return True
 except(AssertionError,KeyError,TypeError,ValueError,OSError,StopIteration,IndexError):return False
def normalized_valid(date,h,role,chapters,root=ROOT):
 try:
  assert role=='start'and isinstance(h,dict)and date==h['effective_period']['start'].get('normalized_date')
  ch=chapters[h['evidence'][0]['chapter_id']]
  try:from scripts.fixed_kanripo_fact_slots import valid
  except ImportError:from fixed_kanripo_fact_slots import valid
  return valid(h,ch,root)and bound_valid(date,h,ch,root)
 except(AssertionError,KeyError,TypeError,ValueError,IndexError):return False
