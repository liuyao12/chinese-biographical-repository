"""按固定原始碼位覆核 南史卷二十三王誕、嘏、偃。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-023-wangdan-gu-yan',)
F='source-evidence/nan023-digital/frames.json'
FS='58203cab4b2fd6928ba10ae240d5a067dd8746d4bfb30f46c98a68b71cd41001'
R='source-evidence/nan023-digital/reading.json'
RS='d56949344799f8b1366b79242b8a1c2b0f1a32a88235a4a024bd801b8d6f3f7c'
PROPOSALS={'tp-nan023-digital-fuguo': ('c-nanshi-023-wangdan-gu-yan:p003', 'a1961255aa28571b3e6f4dcd91fede4a21590e346d6c7a0329b380356ce3be32', '3f9144d81f949b8cb447630d1469b5e2a7141c51a988e8b4a1113de98a9a3422')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史卷二十三王誕、嘏、偃 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史卷二十三王誕、嘏、偃 的親屬、職序或身後事與所據原句不合']

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

def yan_award(h,ch,root):
    if ch.get('id')!='c-nanshi-023-wangdan-gu-yan' or errors(ch,root) or h not in frame(ch,root)['offices']:return False
    pp=ch['paragraphs'][-1];text=pp['text'];basis=h.get('posthumous_basis') or h.get('naming_basis') or {};a,=h['attestations'];e,=h['evidence'];mode=h['mode'];marker='贈' if mode=='posthumous_grant' else '諡';return text.endswith('位右光祿大夫，贈開府儀同三司，諡恭公。') and h['person_id']=='7r6_k52_qji_ABAACAAB' and (mode,h['title']) in [('posthumous_grant','開府儀同三司'),('posthumous_naming','恭公')] and e['quote']==text and basis.get('evidence')==h['evidence']==h['effective_period']['start']['evidence'] and text[a['start']-1:a['end']]==marker+h['title']
