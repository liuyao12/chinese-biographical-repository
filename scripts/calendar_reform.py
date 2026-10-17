"""太初元年過渡年的來源限定換算；不放寬一般歲首跨年規則。"""
RECONSTRUCTION='https://github.com/ytliu0/ChineseCalendar/blob/719e02ff011ab122aad5fb29084e3f6ee8b65390/src/table.js'
HAN_RULE='https://github.com/kanripo/KR2a0007/blob/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_006.txt'

def transition_year_errors(value,evidence,expression):
 errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 check(expression=='太初元年'and value.get('basis')=='calendar_reform_transition_year','改曆範圍僅適用明記太初元年')
 check(value.get('year_numbering')=='astronomical'and value.get('precision')=='year_range'and value.get('status')=='editorial_provisional','改曆年範圍精度或狀態不符')
 check(value.get('earliest')==dict(era='BCE',era_year=105,year=-104)and value.get('latest')==dict(era='BCE',era_year=103,year=-102),'太初元年須保留前冬至後歲首的三個公元年範圍')
 check(value.get('evidence')==evidence and value.get('original_quote')in [e.get('quote')for e in evidence]and isinstance(expression,str)and any(expression in e.get('quote','')for e in evidence),'改曆換年須保相同原事件與原紀年')
 proof=value.get('calendar_reform');check(isinstance(proof,dict)and proof=={'kind':'taichu_first_year_15_months','astronomical_table_year':-103,'first_month_date':'-11-26','last_month_date':'13-12','western_calendar':'proleptic_julian','event_month':'unknown'},'改曆年須保存明示復原表與月序，不能補事件月份')
 refs=value.get('references',[])
 def has(scope,quote,url):return any(isinstance(r,dict)and r.get('scope')==scope and r.get('quote')==quote and r.get('url')==url and r.get('image_verified')is False for r in refs)if isinstance(refs,list)else False
 for scope,quote,url in [('received_calendar_rule','正歴㠯正月為嵗首',HAN_RULE+'#L606-L610'),('calendar_reconstruction_first_month','-11-26',RECONSTRUCTION+'#L538'),('calendar_reconstruction_last_month','13-12',RECONSTRUCTION+'#L540'),('calendar_reconstruction_previous_year_notation','month in the previous year',RECONSTRUCTION+'#L465'),('calendar_reconstruction_next_year_notation','January in the following Julian year',RECONSTRUCTION+'#L465')]:check(has(scope,quote,url),'改曆換年缺固定來源的歲首、首末月或前後年符號依據')
 check(bool(value.get('rationale'))and bool(value.get('reviewer'))and value.get('human_reviewed')is False,'改曆年缺判讀與覆核狀態')
 return errors

def transition_table_errors(value,tables):
 try:
  from .table_evidence import table_cell
 except ImportError:
  from table_evidence import table_cell
 table=tables.get('shiji-022');errors=[]
 if not table:return ['改曆換年缺原年表']
 for cid,quote,scope in [('shiji-022-t1-r103-c01','太初元年','received_regnal_year_attestation'),('shiji-022-t1-r103-c00','104','digital_editorial_regnal_year_equivalence_only')]:
  c=table_cell(table,cid)
  if not c or c['text'].rstrip('。')!=quote or not any(isinstance(r,dict)and r.get('table_id')==table['id']and r.get('table_cell_id')==cid and r.get('quote')==c['text']and r.get('url')==table['source']['revision_url']and r.get('scope')==scope for r in value.get('references',[])):errors.append('改曆範圍缺固定太初元年原欄與數位104對照；不得改作事件確年')
 return errors
