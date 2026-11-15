"""One finite father biography death/relative home/approximate age; no inferred birth."""
from pathlib import Path
import json,hashlib,importlib.util,sys,copy
CID='c-songshu-045-wyd1739-liucui';SOURCE='corpus/songshu/045-wyd1739-liucui.json';LE='le-song045-wyd-zhenzhi';AGE='age-song045-wyd-zhenzhi-death';ADDR='addr-song045-wyd-zhenzhi-death-home';ROW='source-evidence/song045-wyd1739-liucui/life-moe-yuanjia-row.json';ROW_SHA='fc8a17ad4e6050f84622b4dd3360c3e37eecfc4fdac0be4608d9281dc121847c'
J=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'));H=lambda b:hashlib.sha256(b).hexdigest()
def anchor(p,term):
 if p['text'].count(term)!=1:raise ValueError('鎮之原詞不唯一')
 s=p['text'].index(term);return dict(paragraph_id=p['id'],start=s,end=s+len(term),surface=term)
def subject(ch):
 assert isinstance(ch,dict)and(ch['id'],ch['work_id'],ch['book_id'],ch['source_id'])==(CID,'w-songshu','b-songshu-045','s-songshu-045-wyd1739-liucui')
 ps={p['id']:p for p in ch['paragraphs']};p14,p15=ps[CID+':p014'],ps[CID+':p015'];identity=anchor(p14,'父鎮之字仲德以毅貴歷顯位閑居京口未');name=anchor(p15,'鎮之門');clause=anchor(p15,'元嘉二年年九十餘卒於家');assert p14['text'][identity['start']:]==identity['surface'];assert p15['text'][:clause['end']]=='嘗應召常謂毅汝必破我家毅甚憚之每還京未嘗敢以羽儀人從入鎮之門左光祿大夫徵不就元嘉二年年九十餘卒於家'
 a=next(m for m in p14['mentions']if m['start']==identity['start']+1 and m['surface']=='鎮之');b=next(m for m in p15['mentions']if m['start']==name['start']and m['surface']=='鎮之');assert a['kind']==b['kind']=='person'and a['person_id']==b['person_id']
 scope=dict(kind='received_named_father_biography_into_next_page_side',identity_anchor=identity,father_person_mention_id=a['id'],resumed_person_mention_id=b['id'],death_clause_anchor=clause,paragraph_ids=[p14['id'],p15['id']],full_paragraphs=[dict(paragraph_id=p['id'],quote=p['text'],source_position=p['source_position'])for p in[p14,p15]],human_reviewed=False)
 return p15,b,scope

def evidence(ch,p,m):return dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=CID,paragraph_id=p['id'],quote=p['text'],person_mention_id=m['id'])
def age_record(ch):
 p,m,scope=subject(ch);return dict(id=AGE,person_id=m['person_id'],value=None,source_number='九十',source_term='年九十餘',unit='source_age_years',counting='unspecified_source_age',birth_year=None,bounds=dict(lower=90,lower_inclusive=False,upper=None,upper_inclusive=None),reporting_status='direct_report',source_qualification=None,status='source_attested',date_expression=None,evidence=[evidence(ch,p,m)],age_context=dict(kind='at_death',life_event_id=LE),source_zhenzhi_subject_scope=scope,interpretation_note='九十餘只存開放下界九十，上界未載；不是精確九十或九十一，不由425倒生年，不推定原文明示計歲法。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)

def context(root):
 root=Path(root).resolve();old=list(sys.path)
 try:
  sys.path[:0]=[str(root),str(root/'scripts')];s=importlib.util.spec_from_file_location('zhenzhi_existing_life',root/'scripts/wyd_song045_lifecycle.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);ch,c,roles=m.context(root);p,person,scope=subject(ch);assert person['person_id']==roles['liuzhenzhi'];return ch,p,person,scope
 finally:sys.path[:]=old

def records(root):
 root=Path(root).resolve();ch,p,m,scope=context(root);path=(root/ROW).resolve();assert path.is_relative_to(root/'source-evidence');raw=path.read_bytes();assert H(raw)==ROW_SHA;row=json.loads(raw);assert row['columns']==dict(dynasty='宋',era_name='元嘉',first_year='424',last_year='453');e=evidence(ch,p,m)
 date=dict(era='CE',era_year=425,year=425,year_numbering='astronomical',precision='year',calendar='chinese_civil',source_expression='元嘉二年',original_quote=p['text'],evidence=[e],references=[dict(title='教育部《重編國語辭典修訂本》中國歷代年號表',url=row['url'],quote='元嘉',scope='modern_era_year_equivalence_only',columns=copy.deepcopy(row['columns']),fixed_row_reference=dict(path=ROW,sha256=ROW_SHA),image_verified=False)],regnal_year_mapping=dict(kind='ce_regnal_era_span',era_name='元嘉',source_number='二',regnal_year=2,start_ce_year=424,end_ce_year=453,reference_index=0),status='editorial_provisional',rationale='本源同句明元嘉二年，固定宋元嘉424–453對照為中國曆425；年精度，未知月日，不倒出生年。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
 event=dict(id=LE,person_id=m['person_id'],event_type='death',source_term='卒於家',date_expression='元嘉二年',status='source_attested',normalized_date=date,evidence=[e],source_zhenzhi_subject_scope=scope,interpretation_note='承明父鎮之兩頁側完整敘事；元嘉二年卒於家。家為原相對地稱，未指具體地名，不把前文閑居京口自動當卒地。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
 address=dict(id=ADDR,person_id=m['person_id'],relation='death_place',place=dict(source_name='家',place_id=None,modern_identification=None),source_term='卒於家',date_expression='元嘉二年',normalized_date=copy.deepcopy(date),status='source_attested',evidence=[e],source_zhenzhi_subject_scope=copy.deepcopy(scope),interpretation_note='只保卒於家原相對地稱，沒有精確地名或現代行政區；不由閑居京口補卒地京口。',reviewer='Codex（AI代理）',human_reviewed=False,model=None)
 return event,age_record(ch),address

def death_applies(e):return isinstance(e,dict)and(e.get('id')==LE or isinstance(e.get('source_zhenzhi_subject_scope'),dict)and e.get('event_type')=='death')
def address_applies(a):return isinstance(a,dict)and a.get('id')==ADDR

def death_valid(e,root):
 if not isinstance(e,dict):return False
 try:return J(e)==J(records(root)[0])
 except(KeyError,TypeError,ValueError,AssertionError,OSError,AttributeError,StopIteration):return False

def address_valid(a,ch,root):
 if not isinstance(a,dict):return False
 try:
  actual,_,_,_=context(root);return J(ch)==J(actual)and J(a)==J(records(root)[2])
 except(KeyError,TypeError,ValueError,AssertionError,OSError,AttributeError,StopIteration):return False
