"""按固定原始碼位覆核 南史王藻與代作讓婚表。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-023-wangzao',)
F='source-evidence/nan023-wangzao/frames.json'
FS='a23bb63b91194b282511b01cf720bccd339535860dbdf16c10498c90f61d7ab6'
R='source-evidence/nan023-wangzao/reading.json'
RS='b817010fd77cd03278fc816a9cd0aaf89214cd4824e5ea6bce1d720f53cfb9ba'
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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史王藻與代作讓婚表 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史王藻與代作讓婚表 的親屬、職序或身後事與所據原句不合']

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

def kin_valid(a,ch,root):
    if ch.get('id') not in CIDS or errors(ch,root) or a not in frame(ch,root)['kin']:return False
    if a.get('qualifiers',{}).get('nan023_wangzao_reading') != 'preceding-yan':return True
    try:
        q=a['qualifiers'];n=q['antecedent'];old=json.loads((Path(root)/'corpus/nanshi/023-wangdan-gu-yan.json').read_text());parent=old['paragraphs'][-1];child=ch['paragraphs'][0];em=next(m for m in parent['mentions']if m['id']==n['mention_id']);cm=next(m for m in child['mentions']if m['id']==a['evidence'][0]['subject_person_mention_id'])
        raw=source(root,n['raw_path'],ch['source']['raw_file_sha256']).splitlines()
        return (old['id']==n['chapter_id'] and old['source']['revision_id']==n['revision']==ch['source']['revision_id'] and n['paragraph_id']==parent['id'] and n['quote']==parent['text']==raw[11] and child['text']==raw[13] and raw[12]=='' and n['first_line']==12 and n['child_first_line']==14 and em['surface']==parent['text'][em['start']:em['end']]=='偃' and em['person_id']==a['object_person_id'] and cm['person_id']==a['subject_person_id'] and cm['start']==2 and cm['surface']=='藻' and child['text'].startswith(q['source_term']) and q['birth_order']['ordinal']==1)
    except (KeyError,ValueError,TypeError,IndexError,StopIteration,OSError):return False
