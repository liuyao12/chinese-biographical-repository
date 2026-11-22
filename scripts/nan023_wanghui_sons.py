"""按固定原始碼位覆核 南史王繢、安陸王妃、王約雋克。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-023-wanghui-yue-jun-ke', 'c-nanqishu-049-wanghui-daughter-and-court-wedding', 'c-nanqishu-032-zhangdai-family')
F='source-evidence/nan023-wanghui_sons/frames.json'
FS='d1bb7d5abd1b1441284e1e93592f5a45c5556bb844bc641a10f33fe4af72344e'
R='source-evidence/nan023-wanghui_sons/reading.json'
RS='8cc09c855a2cc99245972d74c935af029164f30033461071d26c279536f4aa16'
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
        if ch['id']=='c-nanqishu-032-zhangdai-family' and len(ps)>1:
            ext=json.loads(source(root,'source-evidence/nanqi032-biographies/issued-zhangdai-extension.json','cb3c69cf1157ba3379d43640e45aed409f5b36dd9c7493bf6702dee4a002d1f2'))
            old=ext['old_first_paragraph']
            if hd(ch)!=ext['full_sha256'] or ps[0]!=old or hd([old['source_position']])!=u['positions_sha256'] or hd([old['mentions']])!=u['mentions_sha256'] or h(old['text'])!=u['body_sha256'] or hd(ext['old_annotation'])!=u['annotation_sha256']:raise ValueError('張岱傳首與全傳')
            for p in ps:
                loc=p['source_position']; offset=loc['raw_character_offsets']; n=loc['first_line']; base=sum(map(len,ls[:n-1]))
                if loc['last_line']!=n or not offset or offset!=sorted(set(offset)) or not base<=min(offset)<=max(offset)<base+len(ls[n-1]) or ''.join(raw[v]for v in offset)!=p['text']:raise ValueError('張岱全傳原字')
            return []
        if hd([p['source_position']for p in ps])!=u['positions_sha256']:raise ValueError('段落選取')
        for i,p in enumerate(ps,1):
            pos=p['source_position'];ix=pos['raw_character_offsets'];n=pos['first_line'];base=sum(map(len,ls[:n-1]));
            if p['id']!=u['paragraph_ids'][i-1] or n!=pos['last_line'] or pos['raw_start']!=base+pos['line_start'] or pos['raw_end']!=base+pos['line_end'] or hd(ix)!=pos['projection_sha256'] or ix!=sorted(set(ix)) or ''.join(raw[v]for v in ix)!=p['text']:raise ValueError('原字')
        if h('\n\n'.join(p['text']for p in ps))!=u['body_sha256'] or ch['text_sha256']!=u['body_sha256'] or hd(ch['annotation'])!=u['annotation_sha256'] or hd([p['mentions']for p in ps])!=u['mentions_sha256']:raise ValueError('姓名、引語及官次')
        for v in json.loads(source(root,R,RS))['comparisons']:
            l=source(root,v['fixed_path'],v['sha256']).splitlines()[v['source_line']-1]
            if l[v['start']:v['end']]!=v['quote']:raise ValueError('旁證')
        return []
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史王繢、安陸王妃、王約雋克 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if ch['id']=='c-nanqishu-032-zhangdai-family' and len(ch['paragraphs'])>1:
            ext=json.loads(source(root,'source-evidence/nanqi032-biographies/issued-zhangdai-extension.json','cb3c69cf1157ba3379d43640e45aed409f5b36dd9c7493bf6702dee4a002d1f2'))
            if hd(d[key]) not in ext['side_records'][key]:raise ValueError('張岱父祖及合併後各側檔')
            return []
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史王繢、安陸王妃、王約雋克 的親屬、職序或身後事與所據原句不合']

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
