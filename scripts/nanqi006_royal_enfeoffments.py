"""Six fixed royal enfeoffments: existing holdings and year date model, no runtime AI."""
from pathlib import Path
import json,hashlib
CID='c-nanqishu-006-jianwu1-nov'
BASE='source-evidence/nanqi006-six-prince-enfeoffments/'
KIND='fixed_nanqi006_royal_enfeoffment'
MAPPING='fixed_nanqi006_annal_year'
CAL_SHA='837f7c4e428f89ea46898ab2cd0b59d4ab6a1ec45d199c81a802ca8765968034'
YEAR_SHA='9f8aa367d30784c4ff0ab49a44b797043c0cb70bc5324b91c3cf7a3270110a14'
SLOTS=[(88, '寳義', 91, '晉安王'), (94, '寳𤣥', 97, '江夏王'), (100, '寳源', 103, '廬陵王'), (106, '寳寅', 109, '建安王'), (112, '寳融', 115, '随郡王'), (118, '寳攸', 121, '南平王')]
def identical(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return set(a)==set(b)and all(identical(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(identical(x,y)for x,y in zip(a,b))
 return a==b
def digest(b):return hashlib.sha256(b).hexdigest()
def anchor(p,start,end):return dict(paragraph_id=p['id'],start=start,end=end,surface=p['text'][start:end])
def basis(ch,root):
 assert isinstance(ch,dict)and ch['id']==CID
 try:from scripts.fixed_nanqi006_november import source_errors
 except ImportError:from fixed_nanqi006_november import source_errors
 assert not source_errors(ch,root)
 root=Path(root).resolve();cp=root/BASE/'calendar-row.json';yp=root/BASE/'year-context.json';assert cp.resolve()==cp and yp.resolve()==yp
 cb=cp.read_bytes();yb=yp.read_bytes();assert digest(cb)==CAL_SHA and digest(yb)==YEAR_SHA
 cal=json.loads(cb);year=json.loads(yb);raw=(root/'source-evidence/nanqi006-jianwu1-nov/KR2a0017_006.txt').read_bytes();t=raw.decode('utf-8')
 assert digest(raw)==year['raw_sha256']==ch['source']['response_sha256']and t[year['raw_start']:year['raw_end']]==year['quote']
 ya=year['year_anchor'];assert t[ya['raw_start']:ya['raw_end']]==ya['surface']=='建武元年'and year['quote'].startswith('建武元年冬十月')and t[year['raw_end']:].startswith('十一月癸酉')
 assert cal['row_id']=='av525'and cal['columns']=={'dynasty':'齊','era_name':'建武','first_year':'494','last_year':'498'}and cal['image_verified']is False
 assert "id='av525'"in cal['row_raw']and '>建武</td>'in cal['row_raw']and '>494</div>'in cal['row_raw']and '>498</div>'in cal['row_raw']
 p,=ch['paragraphs'];assert p['text'].startswith('十一月癸酉')and p['text'][83:88]=='庚辰立皇子'
 assert p['text'][88:124]=='寳義為晉安王寳𤣥為江夏王寳源為廬陵王寳寅為建安王寳融為随郡王寳攸為南平王'
 return p,cal,year

def expected(ch,root):
 p,cal,year=basis(ch,root);ce_year=int(cal['columns']['first_year'])+1-1;assert ce_year==494;ms={m['start']:m for m in p['mentions']};results=[];group='grant-nanqi006-jianwu1-nov-gengchen'
 for start,surface,ts,title in SLOTS:
  m=ms[start];assert m['kind']=='person'and m['surface']==surface and m['end']==start+len(surface)and p['text'][m['end']]=='為'and ts==m['end']+1 and p['text'][ts:ts+len(title)]==title
  hid='th-nanqi006-nov-m'+str(start).zfill(4);e=dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
  month=anchor(p,0,3);day=anchor(p,83,85);title_a=anchor(p,ts,ts+len(title));clause=anchor(p,83,124)
  parts=dict(calendar='chinese_civil',month=11,leap_month=None,day=None,sexagenary_day='庚辰',year_source_term='建武元年',month_source_term='十一月',day_source_term='庚辰',year_raw_anchor=year['year_anchor'],year_context_ref=BASE+'year-context.json',month_anchor=month,day_anchor=day,composed_display='建武元年十一月庚辰',composition_status='editorial_join_of_three_source_parts_not_continuous_literal_quote')
  date=dict(era='CE',era_year=ce_year,year=ce_year,year_numbering='astronomical',precision='year',calendar='chinese_civil',source_expression='庚辰',original_quote=p['text'],evidence=[e],references=[dict(url=cal['source_url']+'#av525',scope='modern_era_year_equivalence_only',quote='建武',columns=cal['columns'],fixed_excerpt_ref=BASE+'calendar-row.json'),dict(url=ch['source']['url'],scope='fixed_received_regnal_year_context',quote='建武元年',raw_anchor=year['year_anchor'],fixed_context_ref=BASE+'year-context.json')],status='editorial_provisional',reviewer='Codex（AI代理）',human_reviewed=False,rationale='同一固定本紀年首建武元年銜接完整十一月，庚辰為本組六皇子封爵日原干支。教育部齊建武起494，元年為中國曆年494；不轉公曆月日，不推農曆日序。',regnal_year_mapping=dict(kind=MAPPING,era_name='建武',source_number='元',regnal_year=1,start_ce_year=494,end_ce_year=498,reference_index=0),source_date_parts=parts)
  role=dict(kind=KIND,slot=m['id'],group_id=group,source_revision=ch['source']['revision_id'],paragraph_sha256=digest(p['text'].encode()),recipient_mention_id=m['id'],grant_clause_anchor=clause,title_anchor=title_a,absolute_birth_order_inferred=False)
  h=dict(id=hid,person_id=m['person_id'],title=title,kind='royal_rank',mode='grant',status='source_attested',reviewer='Codex（AI代理）',human_reviewed=False,model=None,evidence=[e],attestations=[dict(id=hid+':a001',paragraph_id=p['id'],start=ts,end=ts+len(title),surface=title,person_mention_id=m['id'],usage='narrative',date_expression='庚辰')],effective_period=dict(start=dict(status='source_event',event_type='grant',date_expression='庚辰',normalized_date=date,evidence=[e]),end=dict(status='unknown',date_expression=None,evidence=[])),source_career_role=role,interpretation_note='立皇子實授，各爵與本人逐字相接；六項同一庚辰日期組，不由列序推排行或全部兒子。任終未知，不以後文諸王被誅泛終止。')
  results.append(h)
 assert len({h['person_id']for h in results})==6
 return results

def valid(h,ch,root):
 if not isinstance(h,dict)or not isinstance(ch,dict):return False
 try:
  rows=expected(ch,root);matches=[x for x in rows if x['id']==h.get('id')];return len(matches)==1 and identical(h,matches[0])
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,StopIteration,AttributeError):return False

def normalized_valid(date,h,role,chapters,root):
 if not isinstance(date,dict)or not isinstance(h,dict)or not isinstance(chapters,dict)or role!='start':return False
 try:
  ch=chapters[h['evidence'][0]['chapter_id']]
  return identical(date,h['effective_period']['start']['normalized_date'])and valid(h,ch,root)
 except(AssertionError,KeyError,TypeError,ValueError,IndexError,OSError,StopIteration,AttributeError):return False
