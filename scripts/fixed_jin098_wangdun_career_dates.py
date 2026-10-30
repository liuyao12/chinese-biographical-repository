"""Finite source-year bridge; pure compilation is not an actual-root API proof."""
import copy,hashlib,json
from pathlib import Path
KIND='fixed_jin098_career_outer_year_chain'
PROOF='source-evidence/jin098-wangdun-career/date-bridge-proof.json'
PROOF_SHA='9e42aa257e46360f164af595f2de2259fe3d5b7d47a10f017c682e869396f20a'
CID='c-jinshu-098-wangdun-comparison'
TARGETS=tuple('tp-jin098-career-p018-'+str(n)for n in range(34,38))+('bd-jin098-career-p018-38',)
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError(m)
def expand(v,roles):
 if isinstance(v,str)and v.startswith('$'):return roles[v[1:]]
 if isinstance(v,list):return[expand(x,roles)for x in v]
 if isinstance(v,dict):return{k:expand(x,roles)for k,x in v.items()}
 return v
def check(proof,ch,capture):
 need(proof['record_type']=='fixed_jin098_career_date_bridge'and proof['human_reviewed']is False,'日期資格')
 need(ch['id']==proof['chapter_id']==CID and ch['source_id']==proof['source_id']and ch['source']==proof['source'],'日期來源維度')
 ps={p['id']:p for p in ch['paragraphs']};need(len(ps)==len(ch['paragraphs']),'段ID重複')
 c=proof['outer_chain'];need(c['year']==322 and type(c['year'])is int and c['source_expression']=='永昌元年'and tuple(c['phase1_targets'])==TARGETS,'外年目標')
 ids=[CID+':p%03d'%n for n in range(11,19)];need([u['paragraph_id']for u in c['complete_chain']]==ids,'完整相鄰敘事鏈')
 need([p['id']for p in ch['paragraphs']][10:19]==ids+[CID+':p019'],'原自然段次序')
 for u in c['complete_chain']:
  p=ps[u['paragraph_id']];need(p['text']==u['text']and H(p['text'].encode())==u['sha256']and p['text_layer']==u['layer']=='received_chapter','外層完整兩表/原段')
 need(all(ps[CID+':p019'][k]==proof['boundary'][k]for k in ('id','text','text_layer','source_position'))and c['outer_end_boundary']==CID+':p019','太甯新年終界')
 a=c['date_anchor'];need(a=={'paragraph_id':CID+':p011','start':281,'end':285,'surface':'永昌元年'}and ps[a['paragraph_id']]['text'][a['start']:a['end']]==a['surface'],'原年詞')
 need(len(proof['range_rows'])==2,'兩初範圍')
 for row,rid,era,period,lo,hi in [(proof['range_rows'][0],'av489','永嘉','西晉',307,313),(proof['range_rows'][1],'av491','建武','東晉',317,317)]:
  d=row['date'];need(d['source_expression']==era+'初'and d['source_stage']=='初'and d['basis']=='within_named_era'and d['precision']=='year_range'and d['human_reviewed']is False,'初精度')
  need(d['earliest']=={'era':'CE','era_year':lo,'year':lo}and d['latest']=={'era':'CE','era_year':hi,'year':hi}and not any(k in d for k in('year','era_year','month','day')),'全朝外界不是確年或任期')
  m=d['era_span_mapping'];need(m=={'kind':'ce_regnal_era_span','polity_source_name':'晉','era_name':era,'source_era_name':era,'start_ce_year':lo,'end_ce_year':hi,'reference_index':0},'年號範圍對照')
  cols=d['references'][0]['columns'];need(cols=={'dynasty':'晉','period':period,'era_name':era,'first_year':str(lo),'last_year':str(hi)},'正確西東晉')
  cal=row['official_row'];need(cal['row_id']==rid,'非另一建武');check_row(cal,capture)
 check_row(c['official_row'],capture);need(c['official_row']['row_id']=='av493'and '>永昌</td>'in c['official_row']['exact_row_html'],'永昌為bare td')
 return ps

def check_row(cal,capture):
 need(H(capture)==cal['existing_capture_sha256']and cal['existing_capture_path']=='sources/calendar-context/moe-era-table-page2.html'and cal['exact_row_html'].encode()in capture and H(cal['exact_row_html'].encode())==cal['row_sha256'],'官方完整capture/確切row/hash')

def compile_template(proof,ch,capture):
 ps=check(proof,ch,capture);t=copy.deepcopy(proof['base_template'])
 for x in proof['range_rows']:
  r,=[r for r in t['title_record']['holdings']if r['id']==x['id']];d=copy.deepcopy(x['date'])
  need(r['evidence']==d['evidence']and r['evidence'][0]['quote']==ps[r['source_career_role']['paragraph_id']]['text'],'範圍事件全文')
  need(r['effective_period']['start']['date_expression']==d['source_expression']and 'normalized_date_range'not in r['effective_period']['start'],'範圍事件原詞')
  r['effective_period']['start']['normalized_date_range']=d
 rows=t['annotation']['title_proposals']+t['detail_record']['records']
 for rid in TARGETS:
  r,=[r for r in rows if r['id']==rid];b=r.get('source_career_role',r.get('source_appointment_context'))
  need(b['paragraph_id']==CID+':p018'and r['person_id']=='$dun'and r['date_expression']is None and 'normalized_date'not in r,'本段本人未有紀年')
  if rid.startswith('tp-'):need(r['outcome']=='not_assumed'and r['effective_service_attested']is False,'不把未受作實持')
  else:need(r['values']['authority']=='self_assumed'and r['values']['court_appointment_attested']is False,'自督不作朝廷授命')
  date_e=copy.deepcopy(r['evidence'][0]);date_e.update(paragraph_id=CID+':p011',quote=ps[CID+':p011']['text']);date_e.pop('person_mention_id',None)
  d={'era':'CE','era_year':322,'year':322,'year_numbering':'astronomical','precision':'year','calendar':'chinese_civil','status':'editorial_provisional','source_expression':'永昌元年','original_quote':ps[CID+':p011']['text'],'evidence':[date_e]+copy.deepcopy(r['evidence']),'references':[{'url':'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2','quote':'永昌','scope':'modern_era_year_equivalence_only','columns':{'dynasty':'晉','period':'東晉','era_name':'永昌','first_year':'322','last_year':'323'}}],'rationale':'p011末外層年詞經完整兩表至p018同役，p019另年為終界；只記此事件年，非持職期間。','reviewer':'Codex（AI代理）','human_reviewed':False,'regnal_year_mapping':{'kind':'ce_regnal_era_span','source_era_name':'永昌','era_name':'永昌','source_number':'元','regnal_year':1,'start_ce_year':322,'end_ce_year':323,'reference_index':0},'event_evidence_binding':{'kind':KIND,'record_id':rid,'person_id':'$dun','date_anchor':copy.deepcopy(proof['outer_chain']['date_anchor']),'target_anchor':copy.deepcopy(b['role_anchor']),'calendar_row_id':'av493','complete_chain_paragraph_ids':[u['paragraph_id']for u in proof['outer_chain']['complete_chain']],'source_acquisition_scope':'existing_fixed_official_calendar_capture; comparison-only biographical witness, not WYD'}}
  r.update(date_expression='永昌元年',normalized_date=d)
 return t

def prepared(root,ch,roles):
 try:from scripts import fixed_jin098_wangdun_comparison as core
 except ImportError:import fixed_jin098_wangdun_comparison as core
 raw=core.path(root,PROOF).read_bytes();need(H(raw)==PROOF_SHA,'日期固定契約漂移');p=json.loads(raw)
 need(core.path(root,'corpus/jinshu/098-wangdun-comparison.json').read_bytes()and ch==json.loads(core.path(root,'corpus/jinshu/098-wangdun-comparison.json').read_bytes()),'actual root')
 capture=core.path(root,p['outer_chain']['official_row']['existing_capture_path']).read_bytes()
 return expand(compile_template(p,ch,capture),roles)

def date_valid(date,record,role,chapters,root):
 try:
  try:from scripts import fixed_jin098_wangdun_career as owner
  except ImportError:import fixed_jin098_wangdun_career as owner
  ch=owner.read(root,owner.CH);_,t=owner.prepared(ch,root)
  need(chapters.get(CID)==ch,'actual catalog chapter')
  rows=t['annotation']['title_proposals']if role in('title_proposal','appointment_notice')else t['detail_record']['records']if role=='source_detail'else[]
  r,=[r for r in rows if r['id']==record.get('id')and r['id']in TARGETS]
  need(record==r and date==r['normalized_date'],'事件/主體/日期完整綁定');return True
 except(ValueError,KeyError,TypeError,OSError,IndexError,AttributeError,StopIteration):return False
