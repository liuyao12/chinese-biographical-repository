"""Finite reviewed event bridges for complete fixed-witness source fact slots.
No NLU, person-ID whitelist, ambient-year inheritance, or inference of tenure ends.
The trusted recipe selects semantic event equivalences; this module binds their
actual recipient, original spans, whole annual unit, independent witness pins,
and reviewed official era columns. It never discovers additional equivalences.
"""
from pathlib import Path,PurePosixPath
import json,hashlib,re
KIND='fixed_witness_parallel_primary_ce_year'
PINS=Path(__file__).with_name('fixed_witness_parallel_date_witnesses.json')
def file(root,path):
 p=PurePosixPath(path);assert not p.is_absolute()and'..'not in p.parts and p.parts[0]=='source-evidence';q=Path(root)/path;assert q.resolve()==q and not q.is_symlink();return q.read_bytes()
def anchor(text,a):
 assert isinstance(a,dict)and set(a)=={'start','end','quote'}and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(text)and text[a['start']:a['end']]==a['quote'];return a['quote']
def columns(root,reference):
 pin=json.loads(PINS.read_text())['era_column_sources'][reference['witness_key']];raw=file(root,reference['path']);assert hashlib.sha256(raw).hexdigest()==reference['sha256']==pin['sha256']and reference['path']==pin['path'];data=json.loads(raw)
 assert data['kind']=='reviewed_official_era_columns'and data['human_reviewed']is False
 return {x['id']:x for x in data['rows']}
def value_at(record,path):
 for key in path:record=record[key]
 return record
def prove(date,record,proof,recipe,ch,root):
 assert proof['kind']=='fixed_archived_parallel_year'and proof['slot']==record['fixed_source_fact_binding']['slot'];row=columns(root,recipe['parallel_calendar_reference'])[proof['calendar_row_id']];n=proof['regnal_year'];assert type(n)is int and 1<=n<=row['last_year']-row['first_year']+1
 b=proof['primary'];pin=json.loads(PINS.read_text())['primary_witnesses'][b['witness_key']];raw=file(root,b['raw_path']);meta=json.loads(file(root,b['metadata_path']));assert pin['raw_sha256']==hashlib.sha256(raw).hexdigest()==meta['raw_sha256']and pin['revision_id']==meta['revision_id']and meta['url']==pin['url']and b['raw_path']==pin['raw_path']and meta['image_verified']is False
 text=raw.decode();unit=b['complete_unit'];q=anchor(text,unit);head=anchor(text,b['year_anchor']);event=anchor(text,b['event_anchor']);assert unit['start']<=b['year_anchor']['start']<b['year_anchor']['end']<=unit['end']and unit['start']<=b['event_anchor']['start']<b['event_anchor']['end']<=unit['end'];assert text[unit['start']-1:unit['start']]in ('','\n')
 nxt=b['next_unit_boundary'];assert text[unit['end']:].startswith(nxt)and(unit['end']==len(text)or text[unit['end']-1]=='\n')
 start=b['unit_start_boundary'];assert q.startswith(start)and(start.startswith('==')or start.startswith('{{YL|'))
 first_line_end=text.index('\n',unit['start'])
 candidates=list(re.finditer(r'(?m)^(?:==[^=\n]+==|\{\{YL\|[^}\n]+年(?:\|[^}\n]*)?\}\}|[二三四五六七八九十]+年(?:春|夏|秋|冬)[^\n]{0,12})',text[first_line_end+1:]))
 stops=[first_line_end+1+x.start()for x in candidates if first_line_end+1+x.start()!=b['year_anchor']['start']]
 assert stops and stops[0]==unit['end'],'Complete primary annual boundary was skipped'

 num=proof['source_number'];assert row['era_name']+num+'年'in head;assert head.replace('{{YL|','').strip('{}=').startswith(row['era_name']+num+'年')
 try:from scripts.chinese_civil_years import numeral
 except ImportError:from chinese_civil_years import numeral
 assert numeral(num)==n
 # Full annual headers cannot be skipped between the selected year and event.
 if b['year_anchor']['end']<=b['event_anchor']['start']:
  middle=text[b['year_anchor']['end']:b['event_anchor']['start']];assert not re.search(r'(?m)^(?:==[^=\n]+年==|\{\{YL\|[^}\n]+年(?:\||\}\})|[二三四五六七八九十]+年(?:春|夏|秋|冬))',middle)
 else:assert proof['event_relation']=='ruler_accession'and n==1
 p=next(p for p in ch['paragraphs']if p['id']==proof['received_event_anchor']['paragraph_id']);ra={k:proof['received_event_anchor'][k]for k in('start','end','quote')};received=anchor(p['text'],ra);assert date['evidence']==record['evidence']and date['original_quote']==p['text']and received in p['text']and all(e['quote']==p['text']and e['paragraph_id']==p['id']for e in record['evidence'])
 ms={m['id']:m for pp in ch['paragraphs']for m in pp['mentions']};recipient=ms[proof['source_person_mention_id']];assert recipient.get('person_id')==record['person_id']and any(e.get('person_mention_id')==recipient['id']for e in record['evidence'])
 relation=proof['event_relation']
 if relation in('same_named_appointment','same_named_shared_appointment_clause','same_named_death'):
  named=ms[proof['biography_full_name_mention_id']];actor=anchor(text,b['actor_anchor']);assert actor==named['surface']and named['person_id']==record['person_id']and named['start']==0
  assert b['event_anchor']['start']<=b['actor_anchor']['start']<b['actor_anchor']['end']<=b['event_anchor']['end']and '<ref'not in event and '{{*|'not in event
  if relation=='same_named_death':assert record.get('event_type')=='death'and text[b['actor_anchor']['end']:b['event_anchor']['end']]in('卒','卒。','薨','薨。')and record['source_term'].endswith(('卒','薨'))
  else:
   title=anchor(text,b['title_anchor']);assert (title==record['title']if relation=='same_named_appointment'else title+'、'+record['title']in received)and b['actor_anchor']['end']<=b['title_anchor']['start']and text[b['actor_anchor']['end']:b['title_anchor']['start']]in('','為','爲')and record['mode']in('grant','transfer','demotion')and title in received
 elif relation=='ruler_accession':
  ruler=ms[proof['ruler_mention_id']];assert ruler['person_id']!=recipient['person_id']and ruler['surface']in received;rh=anchor(text,b['ruler_head_anchor']);title=rh.split('諱')[0];assert ruler['surface']in(title,title.replace('皇帝','帝'));assert (ruler['surface']+'受禪'in received or ruler['surface']+'立'in received)
  assert ('受禪'in received and'受禪'in event)or('立'in received and'即皇帝位'in event);assert record.get('kind')in('office','noble_rank','honorific')and record['mode']=='grant'
 elif relation=='five_grade_nobility_institution':assert received=='五等建'and'奏復五等爵'in event and record.get('kind')=='noble_rank'and record['mode']=='grant'
 else:raise AssertionError('Unreviewed event relation')
 mapping=dict(kind=KIND,reference_index=0,start_ce_year=row['first_year'],end_ce_year=row['last_year'],regnal_year=n,source_number=num,era_name=row['era_name']);assert date['regnal_year_mapping']==mapping and type(date['year'])is int and date['year']==date['era_year']==row['first_year']+n-1 and date['era']=='CE'and date['precision']=='year'and date['calendar']=='chinese_civil'and date['human_reviewed']is False
 assert date['references'][0]['url']==row['url']and date['references'][0]['columns']==dict(dynasty=row['dynasty'],era_name=row['era_name'],first_year=str(row['first_year']),last_year=str(row['last_year']))
 assert date['basis']==dict(kind='parallel_event',source_event_quote=received,reference_url=pin['url'],reference_event_quote=event,reference_year_quote=head)
 assert date['references'][1]==dict(url=pin['url'],scope='received_parallel_event',quote=event)and date['references'][2]==dict(url=pin['url'],scope='received_regnal_year_attestation',quote=head)
 assert value_at(record,proof['record_path'])==date
 return True

def normalized_valid(date,record,role,chapters,root):
 try:
  try:from scripts.fixed_witness_fact_slots import grammar,expand,strict
  except ImportError:from fixed_witness_fact_slots import grammar,expand,strict
  assert isinstance(record,dict)and record['fixed_source_fact_binding']['kind']=='fixed_witness_person_fact_slots';ch=chapters[record['evidence'][0]['chapter_id']];r,roles=grammar(ch,root);slot=record['fixed_source_fact_binding']['slot'];definition,=[s for s in r['slots']if s['slot']==slot];expected=expand(definition['record'],roles);assert strict(expected,record)
  matches=[p for p in r.get('date_proofs',[])if p.get('kind')=='fixed_archived_parallel_year'and p['slot']==slot and p['bound_role']==role and value_at(record,p['record_path'])==date];assert len(matches)==1;return prove(date,record,matches[0],r,ch,root)
 except(AssertionError,KeyError,ValueError,TypeError,IndexError,StopIteration,OSError,UnicodeError,RuntimeError):return False
