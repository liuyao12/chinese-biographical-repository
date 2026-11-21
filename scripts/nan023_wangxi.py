"""按固定原始碼位覆核 南史王錫與王僉。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-023-wangxi-qian', 'c-nanqishu-032-zhangyong-brother-of-dai', 'c-nanshi-031-zhanggui-father-zhangyong', 'c-liangshu-033-zhangshuai-forebears')
F='source-evidence/nan023-wangxi/frames.json'
FS='16622e214760051c43a74b51dbe4182a85308584a8a02c0effc8e49ee7a1c828'
R='source-evidence/nan023-wangxi/reading.json'
RS='50362cf2ea928177eef6786b1169c6b11798267f722501d9a93c5220b5b1cde6'
PROPOSALS={'tp-nan023-wangxi-xi': ('c-nanshi-023-wangxi-qian:p003', 'a366e4f569020a4eb967c26292a1ad8c75ef84307b4fc67dd54d57ae588a3106', '2b84912c8383fbbbfe59d5a2cb0ffbdbbcfebe49cd31bbf5ccb8af3ccfb7f086'), 'tp-nan023-wangxi-qian': ('c-nanshi-023-wangxi-qian:p004', '7b8ea20b5a0a4eea7922c96ee9ba5c901dd5dc269af876fcee69d6da97bf03cb', '8405ece01345cc4b3fff014cfb0f3a8cca3e424c2cf332ef7d86661ae8c7fd6d')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史王錫與王僉 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史王錫與王僉 的親屬、職序或身後事與所據原句不合']

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


def biography_death_gift(holding,ch,events,root):
    """王錫與僉同篇，兩次贈侍中的死者須由各自傳首、卒錄及交接句指認。"""
    try:
        if ch['id']!='c-nanshi-023-wangxi-qian' or errors(ch,root):return False
        u=frame(ch,root)
        if holding not in u['offices'] or holding['mode']!='posthumous_grant' or holding['title']!='侍中':return False
        b=holding['posthumous_basis'];e,=holding['evidence'];a,=holding['attestations']
        if b['kind']!='nan23_named_biography_death_gift' or holding['effective_period']['start']['evidence']!=b['evidence'] or b['evidence']!=[e]:return False
        d=events[b['death_event_id']]
        if d not in u['life'] or d['event_type']!='death' or d['person_id']!=holding['person_id'] or d['evidence']!=[e]:return False
        p,=[p for p in ch['paragraphs']if p['id']==e['paragraph_id']];q,=[p for p in ch['paragraphs']if p['id']==b['topic_paragraph_id']]
        topic,=[m for m in q['mentions']if m['id']==b['topic_mention_id']];recipient,=[m for m in p['mentions']if m['id']==b['recipient_person_mention_id']]
        source=p['text'];dc=d['source_anchor'];g=source.index(b['grant_term'])
        return (q['text'].startswith(b['topic_opening']) and topic['start']==b['topic_opening'].index(topic['surface']+'字') and topic['person_id']==recipient['person_id']==holding['person_id']
                and e['person_mention_id']==recipient['id']==a['person_mention_id'] and b['source_term']==source==e['quote']
                and source.endswith(b['closing_clause']) and dc['surface']==b['death_term']=='卒' and dc['paragraph_id']==p['id']
                and source[dc['start']:dc['end']]=='卒' and dc['end']<=g and b['grant_term']=='贈侍中'
                and a['paragraph_id']==p['id'] and a['start']==g+1 and a['end']==g+3 and source[a['start']:a['end']]=='侍中')
    except (KeyError,ValueError,IndexError,TypeError,OSError):return False
