# coding:utf-8
"""Qualified external chronological placement; never a source-event date.
Trusted reviewed full frames are declarative data, not source-supplied regexes.
No global cache: validation runs once per immutable catalog load transaction.
"""
from pathlib import Path
import json,hashlib,copy,re
KIND='compiler_chronological_placement'
def _read(root,path):
 p=Path(path);assert not p.is_absolute() and '..' not in p.parts and p.parts[0] in ('corpus','scripts','source-evidence','sources','registry')
 q=Path(root).resolve()/p;assert q.resolve()==q and q.is_file();return q.read_bytes()
def _anchor(a,raw):
 assert type(a['start']) is int and type(a['end']) is int and 0<=a['start']<a['end']<=len(raw)
 assert raw[a['start']:a['end']]==a['quote']
def _expected(d,ch,root):
 b=d['external_chronology_proof'];assert set(b)=={'kind','key','path'} and b['kind']=='fixed_compiler_editorial_chronology'
 config=json.loads(_read(root,'scripts/fixed_compiler_chronology_pins.json'));assert config['format_version']=='0.1'
 pin=config['placements'][b['key']];assert ch['id']==pin['chapter_id']
 assert ch['source']['revision_id']==pin['source_revision'] and ch['source']['raw_file_sha256']==pin['raw_sha256']
 try:from scripts.fixed_wikisource_units import source_errors
 except ImportError:from fixed_wikisource_units import source_errors
 assert not source_errors(ch,root)
 p,=[p for p in ch['paragraphs'] if p['id']==pin['paragraph_id']]
 assert hashlib.sha256(p['text'].encode()).hexdigest()==pin['paragraph_sha256']
 m,=[m for m in p['mentions'] if m['id']==pin['owner_mention']['id']]
 assert m['kind']=='person' and m['person_id'] and all(m[k]==v for k,v in pin['owner_mention'].items())
 assert p['text'][m['start']:m['end']]==m['surface']
 ev,=[e for e in json.loads(_read(root,pin['life_event_path']))['events'] if e['id']==pin['life_event_id']]
 try:from scripts.fixed_witness_fact_slots import valid as fact_valid
 except ImportError:from fixed_witness_fact_slots import valid as fact_valid
 assert fact_valid(ev,ch,root) and ev['person_id']==m['person_id'] and ev['event_type']=='death'
 assert ev.get('date_expression') is None and 'normalized_date' not in ev and 'normalized_date_range' not in ev
 proof=json.loads(_read(root,b['path']));assert proof==pin['proof'] and proof['human_reviewed'] is False
 src=proof['source'];assert src['url'].startswith(('https://','http://')) and src['image_verified'] is False
 assert isinstance(src['work_id'],str) and re.fullmatch(r'w-[A-Za-z0-9_-]+',src['work_id'])
 work,=[w for w in json.loads(_read(root,'registry/works.json'))['works'] if w['id']==src['work_id']]
 assert work['title']==src['work_title']
 assert src['work_provenance_ref']=='registry/work-provenance.json#/works/'+src['work_id']
 provenance=json.loads(_read(root,'registry/work-provenance.json'))['works'][src['work_id']]
 assert provenance['work_id']==src['work_id'] and provenance['title']==src['work_title']
 rawbytes=_read(root,src['raw_file']);assert hashlib.sha256(rawbytes).hexdigest()==src['sha256'];raw=rawbytes.decode('utf8')
 unit=proof['unit'];assert unit['path']==src['raw_file'] and unit['sha256']==src['sha256'];_anchor(unit,raw)
 heading,event,note=proof['anchors'];assert [a['layer'] for a in (heading,event,note)]==['annal_year_heading','received_tongjian_annal_body','received_combined_edition_quote_of_kaoyi_not_independent_kaoyi_witness']
 for a in (heading,event,note):
  assert a['path']==src['raw_file'] and a['sha256']==src['sha256'];_anchor(a,raw)
 assert heading['end']<unit['start']<=event['start']<event['end']<=note['start']<note['end']<=unit['end']
 assert proof['layers']=={'event':event['layer'],'qualification':note['layer']} and proof['qualification'] and proof['reading_scope'] and proof['identity_bridge']
 cal=proof['calendar'];tab=_read(root,cal['raw_file']);assert hashlib.sha256(tab).hexdigest()==cal['sha256']
 row=re.search(r"<tr id=['\"]"+re.escape(cal['row_id'])+r"['\"]>.*?</tr>",tab.decode('utf8'),re.S);assert row and cal['dynasty'] in row[0] and cal['era_name'] in row[0]
 assert re.findall(r"<div style=['\"]width:8em;['\"]>([0-9]+)</div>",row[0])==[str(cal['first_year']),str(cal['last_year'])]
 try:from scripts.chinese_civil_years import numeral
 except ImportError:from chinese_civil_years import numeral
 number=numeral(cal['regnal_number']);assert number==cal['regnal_year'] and 1<=number<=cal['last_year']-cal['first_year']+1
 expected=copy.deepcopy(pin['record']);expected['person_id']=m['person_id'];assert expected['person_id']==ev['person_id']
 assert expected['source_anchor']==ev['source_anchor'] and expected['evidence']==ev['evidence'] and expected['source_term']==ev['source_term']
 pl=expected['placement'];assert pl['year']==cal['first_year']+number-1 and type(pl['year']) is int
 assert pl['source_expression']==heading['quote']==cal['era_name']+cal['regnal_number']+'年'
 assert pl==dict(calendar='chinese_civil',year=pl['year'],month=None,day=None,precision='year',source_expression=heading['quote'],evidence_kind='received_compiler_editorial_placement',selection_status='preferred_provisional',human_reviewed=False)
 assert expected['status']=='contextual_provisional' and expected['human_reviewed'] is False
 assert expected['timeline_use']==dict(eligible=True,required_qualification='compiler_editorial_placement_provisional',must_display_qualification=True,replace_source_event_date=False,birth_year_inference_permitted=False)
 assert expected['linked_life_event_id']==ev['id'] and expected['kind']==KIND
 assert 'normalized_date' not in expected and 'normalized_date_range' not in expected
 return expected

def valid(d,ch,root):
 try:
  try:from scripts.fixed_witness_fact_slots import strict
  except ImportError:from fixed_witness_fact_slots import strict
  return strict(d,_expected(d,ch,root))
 except (AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,AttributeError,OSError):return False

def errors(root,records):
 chapters={r['id']:r for r in records if r.get('record_type')=='marked_chapter'};out=[];seen=set()
 for row in records:
  if row.get('record_type')!='biographical_source_detail_set':continue
  for d in row.get('records',[]):
   if d.get('kind')!=KIND:continue
   pair=(d.get('person_id'),d.get('linked_life_event_id'))
   if pair in seen or row.get('chapter_id') not in chapters or not valid(d,chapters[row['chapter_id']],root):out.append('外部編年推繫／來源限定不符:'+str(d.get('id')))
   seen.add(pair)
 return out
