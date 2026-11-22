"""按固定原始碼位覆核 魚復侯子響。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanqishu-040-zixiang', 'c-nanshi-044-zixiang-nan', 'c-nanqishu-003-zixiang-ann', 'c-zizhitongjian-137-zixiang-tj', 'c-hanshu-053-zixiang-han', 'c-houhanshu-042-zixiang-hou', 'c-houhanshu-010-zixiang-yin')
F='source-evidence/nanqi040-zixiang/frames.json'
FS='aef5623a0d14b0d3b0d9c265a6edd82c8c5d63ac38dd000d6a19d03166b49a47'
R='source-evidence/nanqi040-zixiang/reading.json'
RS='9743a790449db13deb925590d983a39810f781998554261aa53bf5f213743ef7'
PROPOSALS={}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['魚復侯子響 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['魚復侯子響 的親屬、職序或身後事與所據原句不合']

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

def funeral_award(holding, chapter, events, root):
    if chapter['id'] != 'c-nanqishu-040-zixiang' or errors(chapter, root):
        return False
    try:
        f = frame(chapter, root)
        b = holding['posthumous_basis']
        death = events[b['death_event_id']]
        d, g = chapter['paragraphs'][2], chapter['paragraphs'][4]
        a, = holding['attestations']
        e, = holding['evidence']
        m = next(m for m in g['mentions'] if m['id'] == a['person_mention_id'])
        dm = next(m for m in d['mentions'] if m['id'] == death['evidence'][0]['person_mention_id'])
        def exact(anchor, para):
            return (anchor['paragraph_id'] == para['id'] and
                    para['text'][anchor['start']:anchor['end']] == anchor['surface'])
        return (holding in f['offices'] and death in f['life']
                and m['person_id'] == dm['person_id'] == death['person_id'] == holding['person_id']
                and b['death_anchor'] == death['source_anchor']
                and exact(b['death_anchor'], d) and exact(b['grant_anchor'], g) and exact(a, g)
                and d['text'].index('長史劉寅') <= dm['start'] < d['text'].index('於琴臺下')
                and b['death_term'] == b['death_anchor']['surface'] == '殺'
                and b['grant_term'] == b['grant_anchor']['surface'] == '贈'
                and b['grant_anchor']['end'] <= m['start'] < a['start'] < g['text'].index('。寅字景蕤')
                and a['usage'] == 'posthumous_usage' and a['surface'] == holding['title']
                and b['source_term'] == e['quote'] == g['text']
                and b['evidence'] == [e] == holding['effective_period']['start']['evidence'])
    except (KeyError, ValueError, StopIteration, TypeError, IndexError):
        return False
