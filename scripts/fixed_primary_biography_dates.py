"""Archived parallel regnal events. No network, inferred birthday or rewritten text."""
import json,hashlib,re
from pathlib import Path,PurePosixPath

def valid(d,chapters,root,bound_record=None,bound_role=None):
 try:
  m=d['regnal_year_mapping'];b=d['fixed_primary_binding'];e,=d['evidence'];ch=chapters[e['chapter_id']];p=next(p for p in ch['paragraphs']if p['id']==e['paragraph_id']);person=next(x for x in p['mentions']if x['id']==b['source_person_mention_id']);t=p['text'];rawpath=Path(b['raw_path']);metapath=Path(b['metadata_path'])
  if not record_bound(d,bound_record,bound_role,person,p):return False
  raw=file(root,str(rawpath));meta=json.loads(file(root,str(metapath)).decode('utf-8'));text=raw.decode();a=b['event_anchor'];h=b['year_heading_anchor'];n=m['regnal_year'];num={1:'元',2:'二',5:'五'}.get(n)
  if(hashlib.sha256(raw).hexdigest()!=meta['raw_sha256']or meta['revision_id']!=2401748 or not meta['url'].endswith('oldid=2401748')or e['quote']!=t or d['original_quote']!=t or person['id']!=e['person_mention_id']or not person.get('person_id')or meta.get('image_verified')is not False):return False
  if text[a['raw_start']:a['raw_end']]!=a['quote']or text[h['year_heading_start']:h['year_heading_end']]!=h['year_heading']or h['year_heading']!='==天監'+str(num)+'年=='or h['year_heading_end']>a['raw_start']or '==天監'in text[h['year_heading_end']:a['raw_start']]:return False
  if m!={'kind':'fixed_primary_parallel_ce_regnal_span','era_name':'天監','start_ce_year':502,'end_ce_year':519,'regnal_year':n,'source_number':num,'reference_index':0}or d['year']!=501+n or d['era_year']!=501+n:return False
  ref=d['references'][0]
  if ref.get('scope')!='modern_era_year_equivalence_only'or ref.get('quote')!='天監'or ref.get('columns')!={'dynasty':'梁','era_name':'天監','first_year':'502','last_year':'519'}:return False
  basis=d['basis']
  if basis['reference_url']!=meta['url']or basis['reference_event_quote']!=a['quote']or basis['reference_year_quote']!=h['year_heading']:return False
  key=b['reading_key'];s=person['surface'];q=a['quote']
  # Main-name source anchors bind the parallel event recipient. Titles alone never identify a person.
  head=ch['paragraphs'][0]['mentions'][0]
  if key=='feisummons':
   return n==1 and person['person_id']in {x['person_id']for x in p['mentions']if x['surface']in ('朏','胤')}and t.startswith('高祖踐阼，徵朏爲侍中、左光祿大夫、開府儀同三司，胤散騎常侍、特進、右光祿大夫，又並不屈。')and '徵謝朏爲左光祿大夫、開府儀同三司，何胤爲右光祿大夫。'in q
  if person['person_id']!=head['person_id']:return False
  if key=='year2appointment':return n==2 and '明年六月，朏輕舟出，詣闕自陳。旣至，詔以爲侍中、司徒、尚書令。'in t and '六月'in q and '以新除左光祿大夫謝朏爲司徒、尚書令。'in q
  if key not in ('year5appointment','death5')or n!=5:return False
  qualification=d['received_chronology_qualification']
  if qualification.get('received_expression')!='後五年'or qualification.get('silently_emended')is not False or qualification.get('preferred_year')!=506 or qualification.get('alternative_year_not_asserted')is not True:return False
  aux=b['corroborating_appointment_anchor']
  if text[aux['raw_start']:aux['raw_end']]!=aux['quote']or aux['year_heading']!='==天監五年=='or '以前司徒謝朏爲中書監、司徒、衛將軍'not in aux['quote']:return False
  if text[aux['year_heading_start']:aux['year_heading_end']]!=aux['year_heading']or not aux['year_heading_end']<=aux['raw_start']or '==天監'in text[aux['year_heading_end']:aux['raw_start']]or aux['revision_id']!=meta['revision_id']or aux['raw_sha256']!=meta['raw_sha256']:return False
  if '後五年，改授中書監、司徒、衛將軍，並固讓不受。遣謁者敦授，乃拜受焉。是冬薨於府，時年六十六。'not in t:return False
  return ('以前司徒謝朏爲中書監、司徒、衛將軍'in q)if key=='year5appointment'else('十二月癸卯，司徒謝朏薨。'in q)
 except(KeyError,TypeError,ValueError,StopIteration,OSError,UnicodeError,RuntimeError):return False


def file(root,path):
 """Both archive and metadata must remain real files in source-evidence.
 Same narrow lexical/resolved-path policy as archived_parallel_death.file.
 """
 p=PurePosixPath(path)if isinstance(path,str)else None
 if root is None or not p or p.is_absolute()or '..'in p.parts or not p.parts or p.parts[0]!='source-evidence':raise ValueError('source evidence path')
 f=Path(root)/path
 if f.is_symlink()or f.resolve()!=Path(root).resolve()/path:raise ValueError('source evidence symlink escape')
 return f.read_bytes()

def record_bound(d,record,role,person,p):
 if not isinstance(record,dict)or record.get('status')!=('contextual_provisional'if role=='appointment_notice'else'source_attested')or record.get('person_id')!=person.get('person_id')or record.get('evidence')!=d.get('evidence'):return False
 key=d['fixed_primary_binding']['reading_key']
 if key=='death5':
  return role=='life_event' and record.get('event_type')=='death'and record.get('source_term')=='薨於府'and record.get('normalized_date')==d
 if key in ('year2appointment','year5appointment'):
  titles=('侍中','司徒','尚書令')if key=='year2appointment'else('中書監','司徒','衛將軍')
  prefix,suffix=('詔以爲','。')if key=='year2appointment'else('改授','，並固讓不受')
  lo=p['text'].index(prefix)+len(prefix);hi=p['text'].index(suffix,lo)
  return (role=='attestation'or(role=='start'and key=='year5appointment'and record.get('effective_period',{}).get('start',{}).get('normalized_date')==d and record['effective_period']['start'].get('status')=='source_event'))and record.get('kind')=='office'and record.get('title')in titles and any(a.get('normalized_date')==d and a.get('person_mention_id')==person['id']and a.get('paragraph_id')==p['id']and a.get('surface')==record['title']and type(a.get('start'))is int and type(a.get('end'))is int and lo<=a['start']<a['end']<=hi and p['text'][a['start']:a['end']]==record['title']for a in record.get('attestations',[]))
 if key=='feisummons':
  if role!='appointment_notice'or record.get('proposal_kind')!='unassumed_appointment'or record.get('normalized_date')!=d:return False
  titles={'朏':('侍中','左光祿大夫','開府儀同三司'),'胤':('散騎常侍','特進','右光祿大夫')}
  a=record.get('role_anchor',{})
  return record.get('title')in titles.get(person['surface'],())and record.get('person_mention_id')==person['id']and a.get('paragraph_id')==p['id']and a.get('surface')==record['title']and type(a.get('start'))is int and type(a.get('end'))is int and person['end']<=a['start']<a['end']<=p['text'].index('又並不屈。')and p['text'][a['start']:a['end']]==record['title']
 return False
