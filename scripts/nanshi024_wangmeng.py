"""按固定原始碼位覆核 南史王猛、陳書王勇及其家人。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-024-wangmeng', 'c-chenshu-014-wangyong', 'c-chenshu-014-fangqing-family-context', 'c-chenshu-014-zhengwanqing-father-context', 'c-chenshu-028-wangmeng-commanders-context', 'c-chenshu-006-wangmeng-houzhu-context', 'c-chenshu-009-wumingche-family-context', 'c-nanshi-077-kongfan-family-context', 'c-suishu-047-weiguang-family-context', 'c-suishu-047-weiguang-siku-heading-context', 'c-suishu-001-yangjian-family-context', 'c-suishu-048-yangsu-family-context')
F='source-evidence/nanshi024-wangmeng/frames.json'
FS='803e9407463a99a8238c2a6f92c307c2c77a3b884b7bbe23801659b097551134'
R='source-evidence/nanshi024-wangmeng/reading.json'
RS='259a6532ca43a0e97b4f62131c3145217a34abb50c9eb304cc42c6728d054a8e'
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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史王猛、陳書王勇及其家人 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史王猛、陳書王勇及其家人 的親屬、職序或身後事與所據原句不合']

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
    if chapter['id'] not in ('c-nanshi-024-wangmeng','c-chenshu-014-wangyong') or errors(chapter,root):
        return False
    try:
        if holding not in frame(chapter, root)['offices']:
            return False
        field = {'posthumous_grant':'posthumous_basis',
                 'posthumous_naming':'naming_basis',
                 'posthumous_enfeoffment':'enfeoffment_basis'}[holding['mode']]
        basis = holding[field]
        death = events[basis['death_event_id']]
        if death != next(e for e in frame(chapter, root)['life'] if e['id'] == basis['death_event_id']):
            return False
        evidence, = holding['evidence']
        paragraph = next(p for p in chapter['paragraphs'] if p['id']==evidence['paragraph_id'])
        att, = holding['attestations']
        def exact(anchor):
            return (anchor['paragraph_id']==paragraph['id'] and 0<=anchor['start']<anchor['end']<=len(paragraph['text'])
                    and paragraph['text'][anchor['start']:anchor['end']]==anchor['surface'])
        da, ga = basis['death_anchor'], basis['grant_anchor']
        return (holding['person_id']==death['person_id']=='72e_1a7_3ac_AAAA' and death['event_type']=='death'
                and death['source_anchor']['paragraph_id']==paragraph['id']
                and exact(da) and exact(ga) and exact(att)
                and da['start']<=death['source_anchor']['start']<death['source_anchor']['end']<=da['end']<=ga['start']
                and ga['start']<=att['start']<att['end']<=ga['end']
                and basis['evidence']==[evidence]==holding['effective_period']['start']['evidence']
                and evidence['quote']==paragraph['text']==basis['source_term']
                and att['surface']==holding['title'] and att['usage']=='posthumous_usage'
                and att['person_mention_id']==basis['recipient_person_mention_id'])
    except (KeyError, IndexError, StopIteration, TypeError, ValueError):
        return False
