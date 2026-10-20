"""原表明示死亡證據的驗證器；不從國除或繼位推死亡。"""
import re
try:
 from .table_evidence import table_cell, table_person_evidence_errors, table_regnal_range_errors
 from .date_ranges import year_range_errors
except ImportError:
 from table_evidence import table_cell, table_person_evidence_errors, table_regnal_range_errors
 from date_ranges import year_range_errors

def native_death_errors(record,event,tables,people):
 errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 check(record.get('record_type')=='table_person_life_event_assertion_set','原表生卒事件集型別不符')
 table=tables.get(record.get('table_id'))
 if not table:return errors+['原表不存在']
 check(record.get('chapter_id')==table['source']['chapter_id'],'原表篇章不符')
 check(event.get('person_id')in people and event.get('event_type')=='death','原表死亡人物或事件類型不符')
 check(event.get('status')=='source_attested'and event.get('source_representation')=='table_cells'and event.get('human_reviewed')is False and bool(event.get('reviewer'))and bool(event.get('interpretation_note')),'原表死亡缺來源判讀')
 evidence=event.get('evidence',[])
 if not isinstance(evidence,list)or len(evidence)!=1:return errors+['本原表死亡模型須一個完整原格']
 e=evidence[0];cell=table_cell(table,e.get('table_cell_id'))
 if not cell:return errors+['死亡原格不存在']
 check(e.get('table_id')==table['id']and e.get('quote')==cell['text'],'死亡證據須完整同表原格')
 m=next((m for m in cell.get('person_mentions',[])if m['id']==e.get('person_mention_id')),None)
 if not m:return errors+['死亡人物須逐人錨點']
 proof=dict(e,mention_id=e['person_mention_id'],quote=m['surface'],source_quote=e['quote'])
 errors.extend(table_person_evidence_errors(proof,tables,event.get('person_id')))
 term=event.get('source_term');date=event.get('date_expression')
 # 僅接受明示同一人物「名死」；未死、當死、死罪不符合此句式。
 check(isinstance(term,str)and term==m['surface']+'死'and cell['text'][m['start']:].startswith(term+'，'),'原表須明記錨點人物已死，不由無後國除推死亡')
 layout=event.get('date_layout')
 prefix_ok=isinstance(date,str)and cell['text'][:m['start']]==date+'，'
 if layout is not None:
  count=layout.get('cell_count_source_term')if isinstance(layout,dict)else None
  prefix_ok=(isinstance(layout,dict)and set(layout)=={'kind','cell_count_source_term','title_source_term'}
   and layout.get('kind')=='after_cell_count_and_title'and isinstance(count,str)
   and bool(re.fullmatch(r'[一二三四五六七八九十百]+。',count))and layout.get('title_source_term')=='侯'
   and isinstance(date,str)and cell['text'][:m['start']]==count+date+'，侯')
 check(isinstance(date,str)and bool(re.fullmatch(r'.+(元|[一二三四五六七八九十]+)年',date))and prefix_ok,'死亡原紀年須在同句前綴，不借後任紀年')
 window=event.get('normalized_date_range')
 check('normalized_date' not in event and isinstance(window,dict),'原表死亡須有明示換年範圍，不填假精確年')
 if isinstance(window,dict):
  errors.extend(year_range_errors(window,evidence,date))
  errors.extend(table_regnal_range_errors(window,date,tables))
 return errors
