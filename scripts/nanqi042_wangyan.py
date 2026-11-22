"""按固定原始碼位覆核 南齊書王晏。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanqishu-042-wangyan', 'c-songshu-072-linhe-zichan', 'c-shiji-030-yanyi-fanchun', 'c-sanguozhi-012-cuiyan-qiuxu')
F='source-evidence/nanqi042-wangyan/frames.json'
FS='d526235161676c3428bc69a6e41ef2440f454b977b9945be5af6cd13c0b64db6'
R='source-evidence/nanqi042-wangyan/reading.json'
RS='b47598d9c7cb7ee0e867d7173c8ea02b8bc9038fefa1067539667906bfb6a0d2'
PROPOSALS={'tp-nanqi042-wangyan-m3-179': ('c-nanqishu-042-wangyan:p003', '601ef4a2d1597691fffc07a7b481f5606819c757a51c75c465eccecf86df83e7', '989efbb6c189103d277a127604e8e5b32e702b03868a8dbf8b573c9df457d846'), 'tp-nanqi042-wangyan-m4-56': ('c-nanqishu-042-wangyan:p004', '935b6eef2c0e7139b785e7239bd9581fc647181e832e3b956c16853759e2a4a6', '8e5b8c3c29a6efa516629dd3d338a457101f004e51046027cfd11fd92a5b47d8'), 'tp-nanqi042-wangyan-m4-62': ('c-nanqishu-042-wangyan:p004', '935b6eef2c0e7139b785e7239bd9581fc647181e832e3b956c16853759e2a4a6', '285c28b0d00dbaad3bfa2adffb2a65de0a51ab5f2d2991fd0f53356a70a79e34'), 'tp-nanqi042-wangyan-m4-80': ('c-nanqishu-042-wangyan:p004', '935b6eef2c0e7139b785e7239bd9581fc647181e832e3b956c16853759e2a4a6', '73895823ff1672fb0e7c762896e2592959a35b2609de7a9406316008c9aa4d1d'), 'tp-nanqi042-wangyan-m4-85': ('c-nanqishu-042-wangyan:p004', '935b6eef2c0e7139b785e7239bd9581fc647181e832e3b956c16853759e2a4a6', '7fc255f4f1f72a6676b8096cba216a9a7e48bf5a18c0b98e3cd70bef705c2cc8'), 'tp-nanqi042-wangyan-m4-91': ('c-nanqishu-042-wangyan:p004', '935b6eef2c0e7139b785e7239bd9581fc647181e832e3b956c16853759e2a4a6', '62584cbfd3396d7ed52c8b33f71b61ff0a1f0c44d045b39d90ae29bcd2e464c7'), 'tp-nanqi042-wangyan-m4-199': ('c-nanqishu-042-wangyan:p004', '935b6eef2c0e7139b785e7239bd9581fc647181e832e3b956c16853759e2a4a6', 'faec99d2bd67ea854b8e8838926f9e4fab5e750c7a934d74948fcb6a8493db0a'), 'tp-nanqi042-wangyan-s1-18': ('c-songshu-072-linhe-zichan:p001', 'd49eafa683e55e59b988b12b1a3b991fb108f956c81b2920c52a4a75f7415474', '418075021bcc1809e09ed42e7e8b27b42cb647d0d0567853fd9f5af6b4e838cc')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南齊書王晏 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南齊書王晏 的親屬、職序或身後事與所據原句不合']

def proposal_valid(q,ch):
    try:
        pid,body,record=PROPOSALS[q['id']];p,=[p for p in ch['paragraphs']if p['id']==pid]
        if ch['id']not in CIDS or h(p['text'])!=body or hd(q)!=record:return False
        for f in ('appointment_anchor','role_anchor','non_assumption_anchor'):
            a=q[f]
            if a['paragraph_id']!=pid or p['text'][a['start']:a['end']]!=a['surface']:return False
        e,=q['evidence'];m,=[m for x in ch['paragraphs'] for m in x['mentions']if m['id']==q['person_mention_id']]
        return m['person_id']==q['person_id'] and m['kind']=='person' and e['quote']==p['text'] and q['title']==q['role_anchor']['surface'] and q['outcome']=='not_assumed'
    except (KeyError,TypeError,IndexError,ValueError):return False
