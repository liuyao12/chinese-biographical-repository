"""Exact death-date and reported-age records for Songshu 51 paragraphs 14–17."""
import copy,hashlib,json
from pathlib import Path

CID='c-songshu-051-wyd1739-zongshi'
CH='corpus/songshu/051-wyd1739.json'
YJ='source-evidence/song045-wyd1739-liucui/life-moe-yuanjia-row.json'
YH='source-evidence/song051-wyd1739-zongshi/p014-p017-yuanhui-calendar-row.json'
KIND='fixed_wyd_song051_p014_p017_life_date'
H=lambda b:hashlib.sha256(b).hexdigest()

def records(root):
 root=Path(root);ch=json.loads((root/CH).read_bytes());ps={p['id'].rsplit(':',1)[-1]:p for p in ch['paragraphs']}
 yj=json.loads((root/YJ).read_bytes());yh=json.loads((root/YH).read_bytes())
 def mention(pno,surface,pid):
  p=ps[pno];return next(m for m in p['mentions']if m['surface']==surface and m.get('person_id')==pid)
 def evidence(p,m):return {'work_id':ch['work_id'],'book_id':ch['book_id'],'source_id':ch['source_id'],'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':m['id']}
 def date(p,m,event_term,year,era,source_expr,refs,kind):
  ev=[evidence(p,m)];mapping={'kind':KIND,'era_name':era,'year':year,'source_expression':source_expr,'context_kind':kind}
  return {'era':'CE','era_year':year,'year':year,'year_numbering':'astronomical','precision':'year','calendar':'chinese_civil','source_expression':source_expr,'original_quote':p['text'],'evidence':ev,'references':refs,'regnal_year_mapping':mapping,'status':'editorial_provisional','rationale':'本段只保存可追溯的上下文換算；不推月日、生年或精確卒日。','reviewer':'Codex（AI代理）','human_reviewed':False}
 def ref(row,quote):return {'title':'教育部《重編國語辭典修訂本》中國歷代年號表','url':row['url'],'quote':quote,'scope':'modern_era_year_equivalence_only','columns':copy.deepcopy(row['columns']),'fixed_row_reference':{'path':YJ if row is yj else YH,'sha256':H((root/(YJ if row is yj else YH)).read_bytes())},'image_verified':False}
 events=[]
 yiz=mention('p014','伯奴','3qs_nqa_ioa_AABD');p=ps['p014'];term='二十一年卒';refs=[ref(yj,'元嘉')]
 e={'id':'le-song051-p014-yizong-death','person_id':yiz['person_id'],'event_type':'death','status':'source_attested','date_expression':'二十一年','source_term':term,'evidence':[evidence(p,yiz)],'interpretation_note':'本傳在元嘉八年事件後明記二十一年卒；依元嘉年號元年424年換算至444年。未推月日。','reviewer':'Codex（AI代理）','human_reviewed':False}
 e['normalized_date']=date(p,yiz,term,444,'元嘉','二十一年',refs,'same_biography_omitted_era_year_after_yuanjia_eight');events.append(e)
 deathterm='與二子承俁並死';p=ps['p017'];
 for pid,surface,midpart in [('3qs_nqa_ioa_AABDB','秉','m0062'),('3qs_nqa_ioa_AABDBA','承','m0076'),('3qs_nqa_ioa_AABDBB','俁','m0077')]:
  m=next(m for m in p['mentions']if m['id'].endswith(':'+midpart)and m.get('person_id')==pid)
  ev=[evidence(p,m)];event={'id':'le-song051-p017-'+midpart+'-death','person_id':pid,'event_type':'death','status':'source_attested','date_expression':deathterm,'source_term':deathterm,'evidence':ev,'interpretation_note':'本段明載秉與二子承、俁並死；本篇按前段元徽四年後「順帝即位」的編年脈絡暫換算477年，屬上下文判讀，不是本句明載年號或年月日。','reviewer':'Codex（AI代理）','human_reviewed':False,
   'contextual_date_basis':{'kind':'song051_yuanhui_fourth_year_then_shundi_accession','chapter_id':CID,'paragraph_id':ps['p016']['id'],'quote':ps['p016']['text'],'era_year_anchor':'元徽元年','sequence_anchor':'四年遷中書令','accession_anchor':'順帝即位','human_reviewed':False}}
  refs=[{'title':'宋書卷五十一清乾隆四年武英殿本','url':ch['source']['url'],'quote':'順帝即位','scope':'received_parallel_event','image_verified':False}, {'title':'教育部《重編國語辭典修訂本》中國歷代年號表','url':yh['url'],'quote':'元徽','scope':'digital_editorial_regnal_year_equivalence_only','columns':copy.deepcopy(yh['columns']),'fixed_row_reference':{'path':YH,'sha256':H((root/YH).read_bytes())},'image_verified':False}]
  nd=date(p,m,deathterm,477,'元徽',deathterm,refs,'same_biography_contextual_shundi_accession_after_yuanhui_four');nd['basis']={'kind':'parallel_event','source_event_quote':deathterm,'reference_url':ch['source']['url'],'reference_event_quote':'順帝即位','reference_year_url':yh['url'],'reference_year_quote':'元徽'};event['normalized_date']=nd;events.append(event)
 return {'format_version':'0.1','record_type':'person_life_event_assertion_set','chapter_id':CID,'events':events}

def date_valid(d,event,chapters,root):
 try:
  expected={e['id']:e for e in records(root)['events']}[event['id']]
  return d==expected['normalized_date'] and event==expected
 except (KeyError,TypeError,ValueError,StopIteration,OSError):return False

def valid_record(record,root):
 try:return record==records(root)
 except (KeyError,TypeError,ValueError,StopIteration,OSError):return False
