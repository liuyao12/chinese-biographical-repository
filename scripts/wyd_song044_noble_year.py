"""One rendered collective-award year bridge, never a native 043 transcription."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
PATH='source-evidence/song044-wyd1739-xiehui/wuchang-year-comparison'
PINS={'calendar-row-reference.json': '738adca4b3961a7b46817708f67747e9b60541f7864f85c589abdf84a4e84e6a', 'primary-units.json': '844d465000f46fa980d90918f1c8648144381cb3ae2fa29356fb1b9c92596f5f', 'context.json': '2a963af6518c3385a7889bef7df9b2a2f5c00c45c040f113081ae7af2d969b54', 'finding.json': '6928a90bff2f3a954291471c0c1945533957a20262323ff2b31f79af1bd459e5', 'access-scope.json': '6a06229805d9aba49746be4ebf382de29cd2de6a2aac7b8bb615133b08db480b'}

def date_record(ch,root=ROOT):
 try:from .wyd_song044_nobles import _build
 except ImportError:from wyd_song044_nobles import _build
 h,_=_build(ch) # full native source metadata and local head/award roles
 payload={}
 for name,sha in PINS.items():
  raw=(Path(root)/PATH/name).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('比較原證或取得資格漂移')
  payload[name]=json.loads(raw)
 units=payload['primary-units.json'];edict,fu=units[:2]
 for u in units:
  if hashlib.sha256(u['text'].encode()).hexdigest()!=u['text_sha256']:raise ValueError('比較單元全文指紋不符')
 if(edict['role']!='complete_award_edict_paragraph'or fu['role']!='complete_explicit_year_award_paragraph'
    or edict['work_id']!='w-songshu'or fu['work_id']!='w-songshu'or edict['volume']!='043'or fu['volume']!='043'
    or '高祖踐阼'not in edict['text']or '上初即位'not in edict['text']
    or '中書令、領太子詹事傅亮，侍中、中領軍謝晦'not in edict['text']
    or '亮可建城縣公，晦可武昌縣公，食邑各二千戶'not in edict['text']
    or not fu['text'].startswith('永初元年，遷太子詹事，中書令如故。以佐命功，封建城縣公，食邑二千戶。')):
  raise ValueError('不是同次佐命群授與傅亮本傳同爵明年')
 p=next(p for p in ch['paragraphs']if p['id'].endswith(':p002'))
 m,=[m for m in p['mentions']if m['id']==p['id']+':m0371']
 if(m['kind']!='person'or m['surface']!='傅亮'or(m['start'],m['end'])!=(371,373)
    or p['text'][371:373]!='傅亮'or m['person_id']==h['person_id']):raise ValueError('同詔對讀人物不得互換')
 def span(text,term):
  if text.count(term)!=1:raise ValueError('比較原詞不唯一')
  i=text.index(term);return dict(start=i,end=i+len(term),surface=term)
 refs=[dict(kind='rendered_primary_reading_reference',url=u['permalink'],quote=u['text'],text_sha256=u['text_sha256'],
   work_id=u['work_id'],volume=u['volume'],section=u['section'],role=u['role'],
   acquisition='rendered_reading_only_footer_revision_observed_fixed_permalink_fetch_cache_miss',
   raw_obtained=False,image_verified=False,text_base_edition=None)for u in units[:2]]
 cal=payload['calendar-row-reference.json'];row=''.join(x['text']for x in cal['read_lines'])
 if("id='av510'"not in row or '>宋</div>'not in row or '>永初</td>'not in row or '>420</div>'not in row or '>422</div>'not in row):raise ValueError('宋永初年表列不符')
 refs.append(dict(scope='modern_era_year_equivalence_only',url=cal['source_url'],quote='永初',
  columns=dict(dynasty='宋',era_name='永初',first_year='420',last_year='422'),
  response_sha256=cal['sha256'],row_excerpt=cal['read_lines'],image_verified=False))
 b=dict(kind='rendered_same_collective_award_explicit_peer_year',record_id=h['id'],person_id=h['person_id'],
  subject_mention_id=h['source_career_role']['subject_mention_id'],head_mention_id=h['source_career_role']['head_mention_id'],
  peer_person_id=m['person_id'],peer_mention_id=m['id'],peer_source_span=dict(start=371,end=373,surface='傅亮'),
  title='武昌縣公',households=2000,peer_title='建城縣公',peer_households=2000,
  edict_subject=span(edict['text'],'侍中、中領軍謝晦'),edict_peer=span(edict['text'],'中書令、領太子詹事傅亮'),
  edict_award=span(edict['text'],'亮可建城縣公，晦可武昌縣公，食邑各二千戶'),
  peer_explicit_year=span(fu['text'],'永初元年'),peer_award=span(fu['text'],'以佐命功，封建城縣公，食邑二千戶'),
  evidence_files=[dict(path=PATH+'/'+n,sha256=s)for n,s in PINS.items()],
  acquisition_scope=payload['access-scope.json'],narrative_context=payload['context.json'],
  interpretation='同次群授詔列兩人同功同食邑，傅亮本傳明永初元年；這是AI跨來源首選，不是044明載年，亦非任意同僚日期外推。',
  source_base_remains='s-songshu-044-wyd1739-xiehui',human_reviewed=False)
 return dict(era='CE',year=420,era_year=420,year_numbering='astronomical',precision='year',calendar='chinese_civil',
  source_expression='永初元年',original_quote=fu['text'],status='editorial_provisional',
  expression_scope='external_rendered_peer_biography_not_literal_in_wyd044',
  regnal_year_mapping=dict(kind='rendered_collective_award_year',era_name='永初',source_number='元',regnal_year=1,start_ce_year=420,end_ce_year=422,reference_index=2),
  rendered_collective_award_year_binding=b,evidence=h['evidence'],references=refs,
  rationale='卷043完整同詔、傅亮同爵同食邑的永初元年明文與受禪初上下文相合，官方年號列宋永初420–422故首選中國曆420。比較頁底本未知，固定頁直取cache miss，未取raw／圖像；不挪六月庚午中領軍日，不推月日或426終期。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)

def valid(date,record,role,chapters,root=ROOT):
 try:
  if not all(isinstance(x,dict)for x in(date,record,chapters))or role!='start':return False
  try:from .wyd_song044_nobles import CID,_build
  except ImportError:from wyd_song044_nobles import CID,_build
  ch=chapters[CID];expected=date_record(ch,root);base=_build(ch)[0]
  candidate=json.loads(json.dumps(record));start=candidate['effective_period']['start']
  if start.pop('normalized_date',None)!=expected or start.get('date_expression')!='永初元年':return False
  start['date_expression']=None
  return date==expected and candidate==base
 except (KeyError,TypeError,ValueError,AttributeError,OSError,StopIteration):return False
