"""按固定原始碼位覆核 王彧身世、王智嗣後與宋明帝詔答。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-023-wangyu-jingwen', 'c-songshu-072-jinping-xiuyou-father', 'c-songshu-094-dai-family-and-chao-xu', 'c-nanqishu-030-jiaodu-at-wangjingwens-death', 'c-songshu-008-wangjingwen-death-annal')
F='source-evidence/nan023-wangyu/frames.json'
FS='2c421a4e9a55d3b1221fbf54fd09432385a80bd0cc73d62f4c57b973eb771077'
R='source-evidence/nan023-wangyu/reading.json'
RS='1665964d655e58da8808672f3f2f035e8b250ffc01210dad93085d0d24b10770'
PROPOSALS={'tp-nan023-wangyu-huangmen': ('c-nanshi-023-wangyu-jingwen:p003', 'bc40156ab3763305a6098c2e5015deb4d0b596a60e9a442b7f72522ac36d6840', '0a453c03621b75b2b6d7137fb747f44332c4d89f42623994630ce8ddac52de80')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['王彧身世、王智嗣後與宋明帝詔答 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['王彧身世、王智嗣後與宋明帝詔答 的親屬、職序或身後事與所據原句不合']

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

def gift_valid(hld,ch,events,root):
    try:
        if ch['id']!='c-nanshi-023-wangyu-jingwen' or errors(ch,root):return False
        f=frame(ch,root);b=hld['posthumous_basis'];e,=hld['evidence'];a,=hld['attestations'];d=events[b['death_event_id']];p=ch['paragraphs'][-1];m,=[m for m in p['mentions']if m['id']==a['person_mention_id']]
        return (hld in f['offices'] and d in f['life'] and d['event_type']=='death' and d['person_id']==hld['person_id']==m['person_id']=='1tc_q18_x7v'
                and m['surface']=='景文' and e['paragraph_id']==a['paragraph_id']==p['id'] and b['evidence']==d['evidence']==hld['effective_period']['start']['evidence']==[e]
                and e['quote']==b['source_term']==p['text'] and p['text'][d['source_anchor']['start']:d['source_anchor']['end']]==b['death_term']=='賜景文死'
                and p['text'][a['start']-2:a['end']]==b['grant_term']=='追贈開府儀同三司' and hld['title']==a['surface']=='開府儀同三司' and p['text'].endswith('時年六十。追贈開府儀同三司，諡曰懿。長子絢。'))
    except (KeyError,IndexError,TypeError,ValueError,OSError):return False
