"""按固定原始碼位覆核 南史王晏。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-024-wangyan', 'c-nanqishu-035-hedong-xuan-yan', 'c-nanqishu-006-wangyan-jianwu-four')
F='source-evidence/nanshi024-wangyan/frames.json'
FS='7d038e884465aff2c4ba474afe5842f1ee58d82c5aeb1b46150fe1ffe9c3b88e'
R='source-evidence/nanshi024-wangyan/reading.json'
RS='fdf55191d8b4781b1afce0a33e7dcbc2ae52bf3d1e3aea724f48829621d4c749'
PROPOSALS={'tp-nanshi024-wangyan-jiangzhou': ('c-nanshi-024-wangyan:p004', '4f715debd3fa6e540bafba7d99b86b9e1057c88cea65f6c4ec5649beb9d7869b', 'fe7e3c33f0a2907bbca151b162fab5cbaee8c7d20df1256609b45aaade88fe9e')}

def h(x):return hashlib.sha256(x.encode()).hexdigest()
def hd(v):return h(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def source(root,relative,digest):
    root=Path(root).resolve();p=root/relative
    if p!=p.resolve() or not p.is_relative_to(root):raise ValueError('來源路徑')
    s=p.read_text()
    if h(s)!=digest:raise ValueError('校本指紋')
    return s

def frame(ch,root):return json.loads(source(root,F,FS))[ch['id']]

def errors(ch,root):
    if ch['id']not in CIDS:return []
    try:
        u=frame(ch,root);s=ch['source'];ps=ch['paragraphs'];raw=source(root,u['source_path'],u['raw_sha256']);ls=raw.splitlines(keepends=True)
        if (ch['source_id'],s['raw_path'],s['raw_file_sha256'],s['revision_id'],s['image_verified'])!=(u['source_id'],u['source_path'],u['raw_sha256'],u['revision_id'],False):raise ValueError('底本')
        if hd([p['source_position']for p in ps])!=u['positions_sha256']:raise ValueError('段落選取')
        for i,p in enumerate(ps,1):
            pos=p['source_position'];ix=pos['raw_character_offsets'];n=pos['first_line'];base=sum(map(len,ls[:n-1]));
            if p['id']!=u['paragraph_ids'][i-1] or n!=pos['last_line'] or pos['raw_start']!=base+pos['line_start'] or pos['raw_end']!=base+pos['line_end'] or hd(ix)!=pos['projection_sha256'] or ix!=sorted(set(ix)) or ''.join(raw[v]for v in ix)!=p['text']:raise ValueError('原字')
        if h('\n\n'.join(p['text']for p in ps))!=u['body_sha256'] or ch['text_sha256']!=u['body_sha256'] or hd(ch['annotation'])!=u['annotation_sha256'] or hd([p['mentions']for p in ps])!=u['mentions_sha256']:raise ValueError('姓名、引語及官次')
        for v in json.loads(source(root,R,RS))['comparisons']:
            l=source(root,v['fixed_path'],v['sha256']).splitlines()[v['source_line']-1]
            if l[v['start']:v['end']]!=v['quote']:raise ValueError('旁證')
        return []
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史王晏 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史王晏 的親屬、職序或身後事與所據原句不合']

def proposal_valid(q,ch):
    try:
        pid,body,record=PROPOSALS[q['id']];p,=[p for p in ch['paragraphs']if p['id']==pid]
        if ch['id']not in CIDS or h(p['text'])!=body or hd(q)!=record:return False
        for f in ('appointment_anchor','role_anchor','non_assumption_anchor'):
            a=q[f]
            if a['paragraph_id']!=pid or p['text'][a['start']:a['end']]!=a['surface']:return False
        e,=q['evidence'];m,=[m for m in p['mentions']if m['id']==q['person_mention_id']]
        return m['person_id']==q['person_id'] and m['kind']=='person' and e['quote']==p['text'] and q['title']==q['role_anchor']['surface'] and q['outcome']=='not_assumed'
    except (KeyError,TypeError,IndexError,ValueError):return False

def ruler_holding(row,chapter,root):
    if chapter.get('id')!='c-nanshi-024-wangyan' or errors(chapter,root):return False
    try:
        att,=row['attestations'];para=next(p for p in chapter['paragraphs'] if p['id']==att['paragraph_id']);ref,=[r for r in chapter['annotation']['person_reference_occurrences']if r['id']==att['person_reference_id']];return row in frame(chapter,root)['offices'] and row['title']==att['surface']=='長史' and row['person_id']==ref['person_id']=='kix_r92_2ed' and ref['surface']=='齊武帝' and para['text'][ref['start']:att['end']]=='齊武帝爲長史' and att['person_mention_id'] is None
    except (KeyError,ValueError,TypeError,StopIteration):return False


def annal_date_valid(date,event,role,chapters,root):
    try:
        ch=chapters['c-nanqishu-006-wangyan-jianwu-four'];p,=ch['paragraphs'];b=date['annal_locator'];src=source(root,ch['source']['raw_path'],ch['source']['raw_file_sha256']).splitlines();assert role=='life_event'and not errors(ch,root) and event in frame(ch,root)['life']and event['id']=='le-nanshi024-wangyan-yan-annal'and event['person_id']=='i08_s4b_5bb'and event['normalized_date']==date and date['original_quote']==p['text']=='丙辰，尚書令王晏伏誅。'and b['month']==1 and b['ganzhi']=='丙辰' and b['year']==4 and b['era']=='建武';return all(src[a['line']-1][a['start']:a['end']]==a['quote']for a in b['anchors'])and date['year']==date['era_year']==497 and date['references'][0]['columns']=={'dynasty':'齊','era_name':'建武','first_year':'494','last_year':'498'}
    except (AssertionError,KeyError,TypeError,IndexError,ValueError,OSError):return False
