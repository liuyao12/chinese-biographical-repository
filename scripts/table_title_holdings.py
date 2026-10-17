# coding: utf-8
"""固定原表的首封爵模型；不偽造正文段落或拼成原句。"""
import re
try:
 from .table_evidence import table_cell
except ImportError:
 from table_evidence import table_cell

def table_title_errors(h, tables, person_ids):
 if h.get('table_title_basis',{}).get('kind') == 'inline_title_attestation':
  return inline_title_errors(h, tables, person_ids)
 errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 check(isinstance(h.get('id'),str) and bool(h['id']) and h.get('source_representation')=='table_cells','稱號須有穩定ID與表格來源種類')
 b=h.get('table_title_basis',{});t=tables.get(b.get('table_id'))
 if not t:return ['表格原生稱號來源不存在']
 s=t['source'];person=h.get('person_id');event=b.get('event',{});name=b.get('noble_name',{});merit=b.get('merit',{});cell=table_cell(t,event.get('table_cell_id'));nc=table_cell(t,name.get('table_cell_id'));mc=table_cell(t,merit.get('table_cell_id'))
 check(person in person_ids and h.get('kind')=='noble_rank' and h.get('mode')=='grant' and h.get('status')=='source_attested','本模型只記有來源的已登記人物首封侯爵')
 if not cell or not nc or not mc:return errors+['首封缺事件、封國或功臣事由原格']
 rowid=cell['id'].rpartition('-c')[0];row=next(r for f in t['fragments']for r in f['rows']if r['id']==rowid);fragment=next(f for f in t['fragments']if row in f['rows'])
 check(all(c['id'].rpartition('-c')[0]==rowid for c in [nc,mc])and nc['column']==0 and mc['column']==1,'封國、功臣事由及事件須在同列原格')
 check(event.get('quote')==cell['text']and name.get('quote')==nc['text']and merit.get('quote')==mc['text'],'表格原生稱號須保留各原格全文')
 check(h.get('title')==nc['text'].rstrip('。')+'侯','稱號只能由同列封國與侯字組成')
 mention=next((m for m in cell['person_mentions']if m['id']==event.get('person_mention_id')),None)
 if not mention:return errors+['授侯持有人須有原格逐人錨點']
 check(mention['person_id']==person and mention['surface']==event.get('surface')and cell['text'][mention['start']:mention['end']]==mention['surface'],'授侯人物或字元錨點不符')
 check('元年'in cell['text'][mention['end']:]and '侯'in cell['text'][:mention['start']]and bool(re.search(r'侯(?:，[一二三四五六七八九十百千萬億]+戶)?$',mc['text'].rstrip('。'))),'首封須有功臣事由及同人侯元年，不能以父死當父封')
 check(all(not c['text'].strip()for c in row['cells']if 2<=c['column']<cell['column']),'已有前期爵位記錄不得當首封')
 e=h.get('evidence',[])
 check(len(e)==3 and {x.get('source_role')for x in e}=={'fief_name','merit','grant_event'},'稱號須分列封國、事由與授侯原格')
 for c in [nc,mc,cell]:
  check(any(x.get('kind')=='table_cell'and x.get('table_id')==t['id']and x.get('table_cell_id')==c['id']and x.get('quote')==c['text']and all(x.get(k)==s.get(v)for k,v in [('work_id','work_id'),('book_id','book_id'),('chapter_id','chapter_id'),('source_id','id'),('source_revision','revision')])for x in e),'稱號證據缺固定修訂或相符原格')
 ats=h.get('attestations',[]);check(len(ats)==1,'首封須有一組表格稱號用稱')
 if len(ats)==1:
  a=ats[0];parts=a.get('source_parts',[]);check(a.get('kind')=='table_title'and a.get('person_mention_id')==mention['id']and a.get('table_cell_id')==cell['id']and a.get('table_id')==t['id']and a.get('usage')=='narrative','表格稱號用稱錨點不符')
  check(len(parts)==2,'封國及侯字須分列原格位置')
  if len(parts)==2:
   for part,c in zip(parts,[nc,cell]):
    start,end=part.get('start'),part.get('end');check(part.get('table_cell_id')==c['id']and type(start)is int and type(end)is int and 0<=start<end<=len(c['text'])and c['text'][start:end]==part.get('surface'),'稱號組件原格或字元位置不符')
   check(''.join(p.get('surface','')for p in parts)==h.get('title')and parts[1].get('surface')=='侯'and parts[1].get('end',10**6)<=mention['start'],'稱號拼合不能納入職稱、姓名或別人的侯字')
   check(not any(m['person_id']!=person and parts[1].get('end',10**6)<=m['start']<mention['start']for m in cell['person_mentions']),'侯字與持有人之間出現別人')
 period=h.get('effective_period',{});start=period.get('start',{});end=period.get('end',{});check(end==dict(status='unknown',date_expression=None,evidence=[]),'首封不能暗補死亡或其他爵位的終期')
 check(start.get('status')=='source_event'and start.get('event_type')=='grant'and start.get('evidence')==e,'首封起點須有相同表格證據')
 date=b.get('date_parts',[]);expression=start.get('date_expression');check(start.get('date_expression_kind')=='table_columns_composed'and len(date)==2,'欄表紀年須明記分欄拼合')
 if len(date)!=2:return errors
 column=next((c for c in fragment['columns']if c['id']==date[0].get('table_column_id')),None);part=date[1];term=part.get('text','');a,z=part.get('start'),part.get('end')
 check(column is not None and fragment['columns'][cell['column']].get('id')==date[0].get('table_column_id')and date[0].get('text')==column.get('text'),'紀年原欄題必須是本格所在欄')
 check(part.get('table_cell_id')==cell['id']and type(a)is int and type(z)is int and 0<=a<z<=len(cell['text'])and cell['text'][a:z]==term,'表格日期原詞位置不符')
 check(isinstance(expression,str)and expression==date[0].get('text','')+term,'拼合日期不得冒作連續原句或更改日期')
 m=re.fullmatch(r'(元|[一二三四五六七八九十]+)年(?:(正|[一二三四五六七八九十]+|閏)月(?:[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])?)?',term)
 if not m:return errors+['首封日期須保留原年字；有月日時須保留月份及干支原詞']
 mapping=b.get('year_mapping',{});yt=tables.get(mapping.get('table_id'))
 if not yt:return errors+['首封缺原年列對照表']
 ys=yt['source'];check(all(mapping.get(k)==ys.get(v)for k,v in [('work_id','work_id'),('book_id','book_id'),('chapter_id','chapter_id'),('source_id','id'),('source_revision','revision')]),'紀年對照來源或固定修訂不符')
 yr=table_cell(yt,mapping.get('regnal_year_cell_id'));dy=table_cell(yt,mapping.get('digital_year_cell_id'));epoch=table_cell(yt,mapping.get('era_anchor_cell_id'))
 if not yr or not dy or not epoch:return errors+['首封紀年缺原年字、數位對照或年號起點']
 check(yr['column']==1 and dy['column']==0 and epoch['column']==1 and yr['id'].rpartition('-c')[0]==dy['id'].rpartition('-c')[0],'原年字與數位年份須同列')
 check(column is not None and epoch['text'].rstrip('。').endswith(column['text']+'元年')and(yr['text'].rstrip('。')==m[1]or yr['text'].rstrip('。')==column['text']+m[1]+'年'),'首封原年字、欄題與年號起點不符')
 rows=[r for f in yt['fragments']for r in f['rows']];ai=next((i for i,r in enumerate(rows)if any(c['id']==epoch['id']for c in r['cells'])),None);yi=next((i for i,r in enumerate(rows)if any(c['id']==yr['id']for c in r['cells'])),None)
 check(ai is not None and yi is not None and ai<=yi and not any(c['column']==1 and '元年'in c['text']for r in rows[ai+1:yi+1]for c in r['cells']),'紀年不得跨過另一年號')
 year=rows[yi]['year']if yi is not None else{};bce=year.get('value');check(type(bce)is int and bce>104 and year.get('era')=='BCE'and year.get('status')=='digital_editorial_equivalence'and year.get('source_cell_id')==dy['id']and year.get('source_quote')==dy['text']and dy['text']==str(bce)and year.get('astronomical_year')==1-bce,'本試點僅處理太初前確定年號的固定數位對照')
 if type(bce)is not int:return errors
 scalar=start.get('normalized_date');window=start.get('normalized_date_range');value=scalar or window or{};check(not(scalar and window),'同一授爵起點不可同填單年與跨年')
 check(value.get('original_quote')==cell['text']and value.get('evidence')==e and value.get('year_numbering')=='astronomical'and value.get('status')=='editorial_provisional','數字紀年須保留事件原格及相同來源證據')
 refs=value.get('references',[]);check(any(r.get('scope')=='received_calendar_rule'and '建亥'in r.get('quote','')for r in refs),'缺十月歲首原文依據')
 for c,table,scope in [(cell,t,'received_table_title_event'),(nc,t,'received_table_fief_name'),(mc,t,'received_table_merit'),(yr,yt,'received_regnal_year_attestation'),(epoch,yt,'received_regnal_year_attestation'),(dy,yt,'digital_editorial_regnal_year_equivalence_only')]:
  check(any(r.get('table_id')==table['id']and r.get('table_cell_id')==c['id']and r.get('quote')==c['text']and r.get('url')==table['source']['revision_url']and r.get('scope')==scope for r in refs),'首封日期缺相符原格及紀年參照')
 check(column is not None and any(r.get('table_id')==t['id']and r.get('table_column_id')==column['id']and r.get('quote')==column['text']and r.get('url')==s['revision_url']for r in refs),'首封日期缺原年號欄題參照')
 if m[2]in ['正','一','二','三','四','五','六','七','八','九']:
  check(isinstance(scalar,dict)and scalar.get('era')=='BCE'and scalar.get('era_year')==bce and scalar.get('year')==1-bce and scalar.get('precision')=='year','太初前三至七月等正月至九月須在數位所列西元年，不能粗加一年')
 elif m[2] in ('閏',None):
  check(isinstance(window,dict)and window.get('earliest')==dict(era='BCE',era_year=bce+1,year=-bce)and window.get('latest')==dict(era='BCE',era_year=bce,year=1-bce)and window.get('precision')=='year_range','未明月份或閏幾月須保跨年範圍，不任選單一年')
 else:errors.append('十月至十二月須另處理，不套本試點單年規則')
 return errors


def inline_title_errors(h, tables, person_ids):
 """同格姓名前的明示王侯稱號只證明用稱，不自動構成授爵。"""
 errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 b=h.get('table_title_basis',{});t=tables.get(b.get('table_id'))
 if not t:return ['用稱表格不存在']
 source=t['source'];event=b.get('event',{});cell=table_cell(t,event.get('table_cell_id'))
 check(isinstance(h.get('id'),str) and bool(h['id']) and h.get('person_id') in person_ids
       and h.get('source_representation')=='table_cells' and h.get('mode')=='attestation'
       and h.get('status')=='source_attested','表格用稱須有已登記人物且不得當授爵')
 check(h.get('kind') in ('royal_rank','noble_rank') and isinstance(h.get('title'),str)
       and bool(h.get('title')) and h['title'].endswith('王' if h.get('kind')=='royal_rank' else '侯'),'王侯用稱種類與原詞不符')
 if not cell or event.get('quote')!=cell['text']:return errors+['用稱須保留原格全文']
 mention=next((m for m in cell['person_mentions']if m['id']==event.get('person_mention_id')),None)
 if not mention:return errors+['用稱人物須有逐人錨點']
 check(mention['person_id']==h.get('person_id') and event.get('surface')==mention['surface']
       and type(mention.get('start')) is int and type(mention.get('end')) is int
       and 0<=mention['start']<mention['end']<=len(cell['text'])
       and cell['text'][mention['start']:mention['end']]==mention['surface'],'用稱人物與字元位置不符')
 evidence=h.get('evidence',[])
 check(len(evidence)==1,'同格用稱須有一筆原格證據')
 if len(evidence)==1:
  e=evidence[0]
  check(e.get('kind')=='table_cell' and 'paragraph_id' not in e and e.get('table_id')==t['id']
        and e.get('table_cell_id')==cell['id'] and e.get('quote')==cell['text']
        and e.get('person_mention_id')==mention['id']
        and all(e.get(k)==source.get(v) for k,v in [('work_id','work_id'),('book_id','book_id'),('chapter_id','chapter_id'),('source_id','id'),('source_revision','revision')]),'用稱證據原格、人物或固定版本不符')
 ats=h.get('attestations',[]);check(len(ats)==1,'同格用稱須有一組稱號錨點')
 if len(ats)==1:
  a=ats[0];parts=a.get('source_parts',[])
  check(isinstance(a.get('id'),str) and bool(a['id']) and a.get('kind')=='table_title'
        and a.get('table_id')==t['id'] and a.get('table_cell_id')==cell['id']
        and a.get('person_mention_id')==mention['id'] and a.get('usage')=='narrative'
        and len(parts)==1,'同格用稱錨點不符')
  if len(parts)==1:
   part=parts[0];start,end=part.get('start'),part.get('end')
   valid=(part.get('table_cell_id')==cell['id'] and type(start)is int and type(end)is int
          and 0<=start<end<=mention['start'] and cell['text'][start:end]==part.get('surface')==h.get('title'))
   check(valid,'用稱原詞須精確位於同人姓名之前')
   if valid:
    # Only a consecutive sequence of rank terms can intervene; never cross a
    # verb, punctuation, or a different named person to claim their title.
    gap=cell['text'][end:mention['start']]
    check(not gap or re.fullmatch(r'[^，。；：、！？王侯]{1,8}[王侯](?:[^，。；：、！？王侯]{1,8}[王侯])*',gap) is not None,'稱號與姓名之間不得跨敘事或其他句子')
    check(not any(m['person_id']!=h['person_id'] and start<=m['start']<mention['start'] for m in cell['person_mentions']),'稱號與姓名之間不得出現另一人')
  check(a.get('date_expression') is None and 'normalized_date' not in a and 'normalized_date_range' not in a,'本用稱模型不以原表數位對照年冒充精確用稱年份')
 period=h.get('effective_period',{})
 check(set(period)=={'start','end'} and all(period.get(key)==dict(status='unknown',date_expression=None,evidence=[]) for key in ('start','end')),'用稱不能推定授封、死亡或廢黜起訖')
 return errors
