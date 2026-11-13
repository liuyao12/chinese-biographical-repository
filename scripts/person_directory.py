"""Small sourced directory metadata from already published profiles; no rebundling."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAME_FIELDS=('id','person_id','surname','ming','full_name','zi','hao','xiaozhi','xiaoming','former_ming','additional_names','title','chapter_id','paragraph_id','person_mention_id','source_id','work_id','book_id')
POSTHUMOUS={'posthumous_grant','posthumous_enfeoffment','posthumous_name','posthumous_only','posthumous_attestation'}

def text(v):return v.strip()if isinstance(v,str)and v.strip()else None

def source_ref(value):
 e=value.get('evidence',[])
 return [{k:r[k]for k in ('source_id','chapter_id','paragraph_id','person_mention_id')if k in r}for r in e if isinstance(r,dict)and r.get('paragraph_id')]

def compact_names(p):
 preferences=p.get('preferred_name_component_readings',[])
 locator_fields={k for r in preferences if isinstance(r,dict)for v in r.get('records',[])if isinstance(v,dict)for k in v.get('record',{})}
 fields=set(NAME_FIELDS)|locator_fields;own=set(p.get('person_ids',[]))|{p['id']};rows=[]
 for n in p.get('name_components',[]):
  if not isinstance(n,dict)or n.get('person_id')not in own:continue
  row={k:n[k]for k in sorted(fields) if k in n}
  if isinstance(n.get('clan_style'),dict)and text(n['clan_style'].get('value')):row['clan_style']={'value':n['clan_style']['value']}
  rows.append(row)
 return rows,preferences

def period_assignments(p):
 own=set(p.get('person_ids',[]))|{p['id']};groups={}
 def collect(d,record,slot):
  if not isinstance(d,dict):return
  # Only explicit, finite normalized dates. No lifespan-range interpolation.
  if not isinstance(d.get('era_year'),int)or isinstance(d.get('era_year'),bool)or d['era_year']<=0:return
  refs=d.get('references',[]);mapping=d.get('regnal_year_mapping',{})
  ix=mapping.get('reference_index')if isinstance(mapping,dict)else None
  if ix is not None:
   if type(ix)is not int or not 0<=ix<len(refs):return
   refs=[refs[ix]]
  for local_index,ref in enumerate(refs):
   columns=ref.get('columns',{})if isinstance(ref,dict)else{}
   dynasty=text(columns.get('canonical_dynasty'))or text(columns.get('dynasty'))
   if not dynasty:continue
   g=groups.setdefault(dynasty,dict(value=dynasty,qualification='dated_activity',record_ids=set(),source_refs=[],era_names=set(),record_refs=[]))
   if text(record.get('id')):g['record_ids'].add(record['id'])
   binding={k:v for k,v in dict(id=record.get('id'),slot=slot,era=d.get('era'),era_year=d.get('era_year'),year=d.get('year'),year_numbering=d.get('year_numbering'),era_name=columns.get('era_name'),reference_index=ix if ix is not None else local_index).items()if v is not None}
   if binding not in g['record_refs']:g['record_refs'].append(binding)
   era=text(columns.get('era_name'))
   if era:g['era_names'].add(era)
   for e in source_ref(record):
    if e not in g['source_refs']:g['source_refs'].append(e)
 def known_event(event):
  return isinstance(event,dict)and event.get('person_id')in own
 # An unresolved competing-date decision cannot silently choose a candidate.
 decisions=p.get('life_event_date_decisions',[])
 contested={eid:[dec for dec in decisions if isinstance(dec,dict)and eid in dec.get('candidate_event_ids',[])]for dec in decisions if isinstance(dec,dict)for eid in dec.get('candidate_event_ids',[])}
 for e in p.get('life_events',[]):
  ds=contested.get(e.get('id'),[])
  chosen=all(dec.get('status')in ('editorial_provisional','editorial_preferred','contextual_provisional')and bool(own.intersection(dec.get('person_ids',[])))and dec.get('event_type')==e.get('event_type')and dec.get('preferred_event_id')==e.get('id')for dec in ds)
  if known_event(e)and e.get('event_type')in ('birth','death')and chosen:collect(e.get('normalized_date'),e,'life_event')
 for h in p.get('titles',[]):
  if not known_event(h)or h.get('mode')in POSTHUMOUS:continue
  if h.get('assumed')is False or h.get('appointment_basis',{}).get('assumed')is False or h.get('service_status')in ('not_assumed','not_taken_up','unreported'):continue
  if any(a.get('person_id')in own and a.get('title')==h.get('title')and a.get('outcome')in ('not_assumed','not_reported')for a in p.get('title_proposals',[])if isinstance(a,dict)):continue
  if h.get('attestations')and all(a.get('usage')in ('posthumous_usage','posthumous_only')for a in h['attestations']):continue
  if h.get('status')in ('unresolved','disputed','not_assumed')or h.get('posthumous_only')is True:continue
  period=h.get('effective_period',{})
  for side in ('start','end'):
   bound=period.get(side,{})
   if isinstance(bound,dict)and bound.get('status')not in ('unknown','unresolved','not_reported'):collect(bound.get('normalized_date'),h,side)
  for a in h.get('attestations',[]):
   if isinstance(a,dict)and a.get('usage')not in ('posthumous_usage','posthumous_only'):collect(a.get('normalized_date'),h,'attestation')
 return [{**g,'record_ids':sorted(g['record_ids']),'era_names':sorted(g['era_names']),'source_refs':sorted(g['source_refs'],key=lambda v:json.dumps(v,sort_keys=True))}for _,g in sorted(groups.items())]

def metadata(p):
 own=set(p.get('person_ids',[]))|{p['id']};names,prefs=compact_names(p);places=[]
 for a in p.get('addresses',[]):
  if a.get('person_id')not in own or a.get('relation')not in ('biographical_origin','native_place'):continue
  value=text(a.get('place',{}).get('source_name'))
  if value:places.append(dict(value=value,record_id=a.get('id'),source_refs=source_ref(a),relation=a['relation']))
 return dict(name_components=names,preferred_name_component_readings=prefs,jiguan=places,period_assignments=period_assignments(p) )

def outputs(root=ROOT):
 root=Path(root);directory=root/'data/corpus/profiles';index=directory/'index.json'
 if not index.is_file():return {}
 canonical={p['id']for p in json.loads((root/'registry/persons.json').read_text())['persons']};rows={}
 for entry in sorted(json.loads(index.read_text())['profiles'],key=lambda v:v['id']):
  pid=entry['id']
  if pid not in canonical:continue
  path=directory/(pid+'.json')
  if not path.is_file():raise ValueError('人物目錄缺少已登記profile：'+pid)
  p=json.loads(path.read_text())
  if p.get('id')!=pid or p.get('canonical_person_id',pid)!=pid:raise ValueError('人物目錄canonical profile不符：'+pid)
  rows[pid]=metadata(p)
 result=dict(schema_version=1,coverage=dict(canonical_registry_count=len(canonical),indexed_profile_count=len(rows),complete=len(rows)==len(canonical)),qualification=dict(dynasty='朝代沿本人已錄生卒/生前職務紀年對照原標籤；同名標籤未進行政權同一判定，非效忠、國籍或一生唯一歸屬，未載不猜。',surname='既有typed姓名共識；不從label拆姓。',jiguan='僅biographical_origin/native_place；不將出生、居住、祖籍或葬地混入。'),persons=rows)
 return {root/'data/corpus/person-directory.json':(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n').encode()}

def run(root=ROOT,check=False):
 result=outputs(root)
 for path,data in result.items():
  if check:
   if not path.is_file()or path.read_bytes()!=data:raise ValueError('人物目錄metadata不同步：'+str(path))
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 print('人物目錄metadata'+('檢查'if check else'生成')+'：'+str(len(result))+'檔')
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();run(check=args.check)
