"""按固定原始碼位覆核 梁書卷二十一王暕與薦文。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-liangshu-021-wangjian-sons-context', 'c-nanqishu-050-xiaobaoyuan-wangjian', 'c-houhanshu-082-lihe-wangjian', 'c-houhanshu-063-ligu-wangjian', 'c-liangshu-003-wangjian-death')
F='source-evidence/liang021-wangjiansihui/frames.json'
FS='f7b4311884db3009b0cc96a2e9b2463937a09d177d21ef8bd8e4adbbb031eb09'
R='source-evidence/liang021-wangjiansihui/reading.json'
RS='bd6c569f0820428ca19920b59aa40fe1093fbc794ef0b533d0a0b52a65e51db0'
PROPOSALS={'tp-liang021-wangjiansihui-yuanwai': ('c-liangshu-021-wangjian-sons-context:p002', '29769b5a021f356ec6ff47ccc8f5d91eda2d042312cefebd6ef55146f6c25fab', '2a1bdda6051107e8e05e92aaa21bb5cb5418f7e36701c54ebf0c4e75f721eae8')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['梁書卷二十一王暕與薦文 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['梁書卷二十一王暕與薦文 的親屬、職序或身後事與所據原句不合']

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

def gift_valid(h0,ch,events,root):
    if ch['id']!='c-liangshu-021-wangjian-sons-context' or errors(ch,root) or h0 not in frame(ch,root)['offices']:return False
    b=h0.get('posthumous_basis',{});ev=events.get(b.get('death_event_id'),{});pp=next(p for p in ch['paragraphs']if p['id'].endswith(':p001'));a,=h0['attestations'];ee,=h0['evidence']
    if not (ev.get('person_id')==h0['person_id']=='7r6_k52_qji_ABAAAAEAAB' and ev.get('source_term')==b.get('death_term')=='暴疾卒'
            and ev.get('evidence')==b.get('evidence')==h0['evidence']==h0['effective_period']['start']['evidence']
            and pp['text']==ee['quote']==b['source_term'] and pp['text'][a['start']:a['end']]==h0['title']):return False
    t=pp['text'];g='贈侍中、中書令、中軍將軍';return b['grant_term']==g and t.count(g)==1 and t.index('暴疾卒')<t.index(g)<a['start']<t.index(g)+len(g)
