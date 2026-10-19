"""固定紀年語境到具體事件的無NLU接線；不替無日期事件補年。"""
import json
from pathlib import Path

def date_shape_valid(d):
 c=d.get('calendar_context');a=c.get('event_anchor') if isinstance(c,dict)else None
 return (isinstance(c,dict) and set(c)=={'context_id','event_anchor'} and isinstance(c['context_id'],str)
  and isinstance(a,dict) and set(a)=={'paragraph_id','start','end','surface'} and type(a['start'])is int and type(a['end'])is int
  and a['start']<a['end'] and isinstance(a['surface'],str) and bool(a['surface'])
  and d.get('calendar')=='chinese_civil' and d.get('era')=='CE' and d.get('year')==d.get('era_year')
  and type(d.get('year'))is int and d['year']>0 and 'regnal_year_mapping'not in d and d.get('source_expression')
  and d.get('year_numbering')=='astronomical' and d.get('precision')=='year')

def binding_errors(d,owner,slot,contexts,paragraphs):
 if 'calendar_context'not in d:return []
 if not date_shape_valid(d):return ['紀年語境接線結構不符']
 c=contexts.get(d['calendar_context']['context_id']);a=d['calendar_context']['event_anchor']
 if not c:return ['紀年語境不存在']
 es=[]
 def ck(ok,msg):
  if not ok:es.append(msg)
 ck(d['year']==c['normalized_date']['year'] and d['source_expression']==c['original_expression'],'接線年份／原詞不符')
 ck(a['paragraph_id']==c['anchor']['paragraph_id'] and c['scope']['start']<=a['start']<a['end']<=c['scope']['end'] and c['full_paragraph'][a['start']:a['end']]==a['surface'],'事件錨點越過日期scope或原字不符')
 ck(d['original_quote']==c['full_paragraph'] and d['evidence']==owner['evidence'],'接線完整原句／事件證據不符')
 ck(all(e['paragraph_id']==a['paragraph_id'] and e['quote']==c['full_paragraph'] for e in d['evidence']),'接線來源段不符')
 if slot in ('attestation','start','end'):
  hits=[x for x in owner['attestations'] if all(x.get(k)==a[k]for k in a)]
  ck(bool(hits),'稱號接線必須對應本持有記錄的逐字attestation')
  if slot in ('start','end'):ck(owner['effective_period'][slot]['status']=='source_event' and owner['effective_period'][slot].get('date_expression')==c['original_expression'],'未知邊界不得接線補年')
 else:
  p=paragraphs.get(a['paragraph_id'],{})
  mids={e.get('person_mention_id')for e in owner['evidence']}
  hits=[m for m in p.get('mentions',[])if m['id']in mids and all(m.get(k)==a[k]for k in ['start','end','surface']) and m.get('person_id')==owner['person_id']]
  ck(bool(hits) and owner['event_type']=='death' and owner.get('date_expression')==c['original_expression'],'死亡接線須對應同人同事件錨點')
  ck(owner.get('source_term') in c['scope']['quote'],'死亡原詞越過日期scope')
 return es

def validate(root):
 root=Path(root);contexts={};paragraphs={};records=[]
 for f in (root/'corpus').rglob('*.json'):
  x=json.loads(f.read_text());records.append(x)
  for p in x.get('paragraphs',[]):paragraphs[p['id']]=p
  if x.get('record_type')=='calendar_context_assertion_set':contexts.update({c['id']:c for c in x['records']})
 es=[]
 for x in records:
  for h in x.get('holdings',[]):
   for a in h['attestations']:
    if isinstance(a.get('normalized_date'),dict):es.extend(binding_errors(a['normalized_date'],h,'attestation',contexts,paragraphs))
   for slot,b in h['effective_period'].items():
    if isinstance(b.get('normalized_date'),dict):es.extend(binding_errors(b['normalized_date'],h,slot,contexts,paragraphs))
  for e in x.get('events',[]):
   if isinstance(e.get('normalized_date'),dict):es.extend(binding_errors(e['normalized_date'],e,'event',contexts,paragraphs))
 return es

def export_calendar_contexts(root):
    """獨立紀年API亦保留無人物主體的大赦；絕不創建生卒事件。"""
    try:
        from . import calendar_contexts
    except ImportError:
        import calendar_contexts
    es=calendar_contexts.validate(root)+validate(root)
    if es:raise ValueError('；'.join(es))
    root=Path(root);records=[]
    for f in sorted((root/'corpus/calendar-contexts').glob('*.json')):
        records.extend(json.loads(f.read_text())['records'])
    dest=root/'exports/calendar-contexts.json';dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps({'record_type':'calendar_context_api','schema_version':1,'runtime_ai_required':False,'records':records},ensure_ascii=False,indent=2)+'\n')
    return dest
