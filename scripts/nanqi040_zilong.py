"""按固定原始碼位覆核 隨郡王子隆。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanqishu-040-zilong', 'c-nanqishu-040-zilong-mother', 'c-nanshi-044-zilong-nan', 'c-nanqishu-005-zilong-an', 'c-nanshi-032-zilong-xu')
F='source-evidence/nanqi040-zilong/frames.json'
FS='f901394a53c219f61e6e26053a65fbc324b605de153d23b4ec1d1aff0edc77cb'
R='source-evidence/nanqi040-zilong/reading.json'
RS='377e0281fd96d762033da5e1931a8a8314055dae2eadd91dcfaa993df124007c'
PROPOSALS={'tp-nanqi040-zilong-jiangzhou': ('c-nanqishu-040-zilong:p001', '13d8f2b4abd0a8cdb5b7b2897fd40a97b561d9b1f276e4e9d980326b1a6006a1', '5670901af3e49be534ba14c4cfc35d43883f79335f6e84cff311abea1a363ce0'), 'tp-nanqi040-zilong-zhongshu': ('c-nanqishu-040-zilong:p001', '13d8f2b4abd0a8cdb5b7b2897fd40a97b561d9b1f276e4e9d980326b1a6006a1', 'dfd9aaa17f4e38e1828ee5542ccf05deb40c689a3c7a5402466d918d186d11e7')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['隨郡王子隆 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['隨郡王子隆 的親屬、職序或身後事與所據原句不合']

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

single_paragraph_proposal_valid = proposal_valid

def proposal_valid(q, ch):
    if q.get('id') != 'tp-nanqi040-zilong-zhongshu':
        return single_paragraph_proposal_valid(q, ch)
    try:
        p, n = ch['paragraphs'][:2]
        pid, digest, record = PROPOSALS[q['id']]
        m, = [m for m in p['mentions'] if m['id'] == q['person_mention_id']]
        e, = q['evidence']
        f, = q['non_assumption_evidence']
        return (ch['id'] == 'c-nanqishu-040-zilong' and
                [p['source_position']['first_line'], n['source_position']['first_line']] == [134, 136] and
                hd(q) == record and h(p['text']) == digest and p['id'] == pid and
                p['text'].endswith('遷長兼中書令。') and '未及拜，仍遷中護軍' in n['text'] and
                m['person_id'] == q['person_id'] == '4tg_ud8_zdy' and
                e['paragraph_id'] == p['id'] and f['paragraph_id'] == n['id'] and
                e['quote'] == p['text'] and f['quote'] == n['text'] and
                all(a['paragraph_id'] == para['id'] and para['text'][a['start']:a['end']] == a['surface']
                    for a,para in [(q['role_anchor'],p),(q['appointment_anchor'],p),(q['non_assumption_anchor'],n)]))
    except (KeyError, TypeError, ValueError, IndexError):
        return False
