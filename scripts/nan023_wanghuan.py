"""按固定原始碼位覆核 南史王奐與齊魏梁諸證。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-023-wanghuan', 'c-nanqishu-049-wanghuan-final-family', 'c-liangshu-027-wanghuan-daughter-and-yinrui', 'c-weishu-weishou-063-wangsu-father-and-brother', 'c-gujin-xingshi-shu-bianzheng-014-wangpuyao-and-wangyan', 'c-nanqishu-043-wangsiyuan-father-and-cousin', 'c-nanqishu-042-wangyan-father-and-grandfather', 'c-weishu-weishou-071-peishuye-father', 'c-nanqishu-003-wanghuan-execution-date')
F='source-evidence/nan023-wanghuan/frames.json'
FS='401459967537cffb7fdfcd73d9146d1c77217b410982cb3fabfc6e2d2b2205a8'
R='source-evidence/nan023-wanghuan/reading.json'
RS='5ec63d921c06c0a7208670e2d3aafdc9baeeaa873830088fb25d482821b24705'
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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史王奐與齊魏梁諸證 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史王奐與齊魏梁諸證 的親屬、職序或身後事與所據原句不合']

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

def pua_zhou_valid(ch, paragraph, mention, root):
    """維基轉錄只在王奐傳末原模板之內是具名提及。"""
    try:
        if ch['id']!='c-nanqishu-049-wanghuan-final-family' or errors(ch, root):
            return False
        if paragraph['id']!=ch['id']+':p003' or mention['id']!=paragraph['id']+':m0002':
            return False
        if mention not in paragraph['mentions'] or (mention['start'],mention['end'],mention['surface'],mention['person_id'])!=(2,3,'','q7m_r8k_2vn_AC'):
            return False
        u=frame(ch,root);raw=source(root,u['source_path'],u['raw_sha256'])
        i=paragraph['source_position']['raw_character_offsets'][2]
        return paragraph['text'][0:5]=='奐弟女爲' and raw[i-8:i+4]=='奐弟{{PUA|}}女'
    except (KeyError,IndexError,TypeError,ValueError,OSError):
        return False

def wei71_father_endpoints(a,ch,root,adjacent,endpoints):
    """同一原行先具傳主，後載父名；逐端核引句與兩原位。"""
    try:
        if a['id']!='a-nan023-wanghuan-pei-father' or not kin_valid(a,ch,root):
            return False
        first,second=ch['paragraphs'];u=frame(ch,root);raw=source(root,u['source_path'],u['raw_sha256'])
        p=first['source_position'];q=second['source_position']
        return (a['subject_person_id'],a['object_person_id'])==('2we_3ll_c5i_A','2we_3ll_c5i') and a['context']['paragraph_ids']==adjacent==[first['id'],second['id']] and endpoints==[{'2we_3ll_c5i_A'},{'2we_3ll_c5i'}] and p['first_line']==q['first_line']==3 and p['raw_end']<=q['raw_start'] and raw[p['raw_start']:p['raw_end']]==first['text']=='裴叔業，河東聞喜人也。' and raw[q['raw_start']:q['raw_end']]==second['text']=='父順宗'
    except (KeyError,IndexError,TypeError,ValueError,OSError):
        return False
