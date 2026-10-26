"""Death statements in the fixed WYD044 source; current IDs follow source anchors."""
import json
from pathlib import Path
CID='c-songshu-044-wyd1739-xiehui'

def record(root):
    try:
        from .wyd_song044_formal_roles import source_errors
    except ImportError:
        from wyd_song044_formal_roles import source_errors
    c=json.loads((Path(root)/'corpus/songshu/044-wyd1739.json').read_text())
    if source_errors(c,root):
        raise ValueError('死亡敘述須有完整固定原文及逐人雙向錨點')
    ps={p['id'].split(':')[-1]:p for p in c['paragraphs']}
    def event(p,m,term,note):
        return {'id':'le-song044-wyd-'+m['source_role_key'],'person_id':m['person_id'],
                'event_type':'death','status':'source_attested','date_expression':None,
                'source_term':term,'evidence':[{**{k:c[k]for k in('work_id','book_id','source_id')},
                'chapter_id':CID,'paragraph_id':p['id'],'quote':p['text'],'person_mention_id':m['id']}],
                'interpretation_note':note,'reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
    p=ps['p016'];lo=p['text'].index('於是與晦');hi=p['text'].index('並伏誅')
    listed=[m for m in p['mentions']if m['kind']=='person'and lo<=m['start']<hi]
    expected=['hui','xiedun','shiji','shiyou','dengzhi','kongyanxiu','zhouchao','feiyin','douyingqi','jiangqian','yanqiansi']
    if [m['source_role_key']for m in listed]!=expected:
        raise ValueError('伏誅名單須保留具體列名，不納入相鄰敘事人物')
    # The witness lists Dengzhi both among executions and among pardons.
    # Preserve that conflict separately; do not manufacture a certain death.
    if '庾登之殿道鸞何承天並皆原免'not in p['text']:
        raise ValueError('不得省略同段庾登之原免記載')
    events=[event(p,m,'並伏誅','本源處死列名；庾登之另有同段原免，未列確定死亡。紀年另行覆核，不借名單旁人的日期。')
            for m in listed if m['source_role_key']!='dengzhi']
    p=ps['p001'];m=next(m for m in p['mentions']if m.get('source_role_key')=='xuan-brother')
    if not p['text'][m['end']:].startswith('高祖鎮軍長史蚤卒'):
        raise ValueError('蚤卒須回指晦兄絢，不是晦本人')
    events.append(event(p,m,'蚤卒','絢為本句死亡主體；蚤卒不換成確切卒年或享年。'))
    p=ps['p017'];m=next(m for m in p['mentions']if m.get('source_role_key')=='shangxuanshi')
    if not p['text'].startswith('不敢許知玄石獨謀不立遂為晦領幢事旣平恨本心之不遂投水死'):
        raise ValueError('投水死須保商玄石前後主語，不轉給懷福或任官君主')
    events.append(event(p,m,'投水死','玄石為本段承接主體；不把其子懷福或受任君主當成死亡主體。'))
    # p003 explicitly moves from 元嘉二年 to 三年正月. The continuous
    # campaign ends in p016's executions; January is not the death month.
    date_p=ps['p003'];era_at=date_p['text'].index('元嘉二年');year_at=date_p['text'].index('三年正月',era_at)
    reference=json.loads((Path(root)/'corpus/songshu/053-yu-dengzhi-life-events.json').read_text())['events'][0]['normalized_date']['references'][0]
    if reference['columns']!={'dynasty':'宋','era_name':'元嘉','first_year':'424','last_year':'453'}:
        raise ValueError('元嘉年號對照須保留既收現代年號表原證')
    def anchor(p,start,term):
        return {'paragraph_id':p['id'],'start':start,'end':start+len(term),'surface':term}
    timeline=[p for p in c['paragraphs'] if 3<=int(p['id'].split(':p')[-1])<=16]
    if len(timeline)!=14:raise ValueError('同役敘事中間段不得省略')
    for item in events[:10]:
        death_e=item['evidence'][0];date_e={**{k:c[k]for k in('work_id','book_id','source_id')},'chapter_id':CID,'paragraph_id':date_p['id'],'quote':date_p['text']}
        item['date_expression']='三年'
        item['normalized_date']={
            'era':'CE','era_year':426,'year':424+3-1,'year_numbering':'astronomical',
            'precision':'year','calendar':'chinese_civil','source_expression':'三年',
            'status':'editorial_provisional','original_quote':death_e['quote'],
            'evidence':[date_e,death_e],'references':[reference],
            'regnal_year_mapping':{'kind':'fixed_wyd_execution_narrative_year','era_name':'元嘉',
                'source_number':'三','regnal_year':3,'start_ce_year':424,'end_ce_year':453,'reference_index':0},
            'event_evidence_binding':{'kind':'wyd_song044_execution_narrative_year','life_event_id':item['id'],
                'person_mention_id':death_e['person_mention_id'],'era_anchor':anchor(date_p,era_at,'元嘉二年'),
                'year_anchor':anchor(date_p,year_at,'三年正月'),
                'source_revision':c['source']['revision_id'],'raw_sha256':c['source']['raw_sha256'],
                'full_narrative':[{'paragraph_id':p['id'],'quote':p['text'],'source_position':p['source_position']}for p in timeline]},
            'rationale':'元嘉二年後明轉三年正月；本役敘事延至沙橋敗、檻送京師及本段伏誅，未改敘事年。引語追述永初等不改主線紀年。只換中國曆第三年為426，不將起兵正月當死亡月，不倒算生年。',
            'reviewer':'Codex（AI代理）','human_reviewed':False,'model':None}
    return {'format_version':'0.1','record_type':'person_life_event_assertion_set','chapter_id':CID,'events':events}

def valid(value,root):
    try:
        return isinstance(value,dict)and value==record(root)
    except (KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):
        return False


def date_valid(date,event,chapters,root):
    try:
        expected=next(e for e in record(root)['events']if e['id']==event['id'])
        current=json.loads((Path(root)/'corpus/songshu/044-wyd1739.json').read_text())
        return (chapters.get(CID)==current and event==expected
                and 'normalized_date'in expected and date==expected['normalized_date'])
    except (KeyError,ValueError,TypeError,OSError,StopIteration,AttributeError):
        return False
