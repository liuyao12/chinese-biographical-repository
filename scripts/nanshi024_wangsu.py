"""按固定原始碼位覆核 南史宋書王素及其母。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-songshu-093-wangsu', 'c-nanshi-024-wangsu', 'c-songshu-093-zhubainian-ancestry')
F='source-evidence/nanshi024-wangsu/frames.json'
FS='3b9a3db98047a8b7ab4f7f96c4ae4f9ed4c2df17aa3d70b700639042e6ce78e5'
R='source-evidence/nanshi024-wangsu/reading.json'
RS='7a868266cc2aec3f8bf72231a777e634772d80b3b523daa79526aef991f49768'
PROPOSALS={'tp-nanshi024-wangsu-cangcao': ('c-songshu-093-wangsu:p002', 'b7b11cea01158e277c732c555021ef7f6e288c8502e25dbde72dd69f1770126c', 'f16649466e3b19b1922ebe09e4b6cc5625d95b3d2fded2cc897aa57a149592c6'), 'tp-nanshi024-wangsu-zhongsheren': ('c-songshu-093-wangsu:p002', 'b7b11cea01158e277c732c555021ef7f6e288c8502e25dbde72dd69f1770126c', '7c6977130c7ec44752107fc6368f243e31df60a87d34116dab7c155d318da946')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史宋書王素及其母 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史宋書王素及其母 的親屬、職序或身後事與所據原句不合']

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
def four_ancestor_pair(member,rows,assertions,chapters,root):
    """同一傳首的四個具名世次。逐核並不仕主語，不以遠祖彬取代翹之。"""
    try:
        connection=member['parent_connection']
        ch=chapters['c-nanshi-024-wangsu']
        paragraph,=ch['paragraphs']
        anchored=frame(ch,root)['kin']
        keys=['a-nanshi024-wangsu-ancestor-'+str(n) for n in (4,3,2,1)]
        records=[assertions[key] for key in keys]
        if any(record not in anchored for record in records) or errors(ch,root):
            return False
        head=records[0]['subject_person_id']
        if any(record['subject_person_id']!=head for record in records):
            return False
        parents=[r['object_person_id'] for r in records]
        if len({head,*parents})!=5 or connection['chain_subject_person_id']!=head or head not in rows[head]['source_person_ids']:
            return False
        if connection['nearer_ancestor_assertion_id']!=keys[1] or connection['farther_ancestor_assertion_id']!=keys[0]:
            return False
        if parents[1]!=member['representative_source_person_id'] or parents[0]!=rows[member['parent_person_id']]['representative_source_person_id']:
            return False
        if any(a.get('predicate')=='father' and a.get('subject_person_id')in member['source_person_ids'] and a.get('object_person_id')not in rows[member['parent_person_id']]['source_person_ids'] for a in assertions.values()):
            return False
        refs=connection['references']
        return (connection['interpretation_basis']=='nanshi024_wangsu_four_ancestors'
                and len(refs)==2 and {x['assertion_id']for x in refs}==set(keys[:2])
                and all(x['paragraph_id']==paragraph['id'] and x['chapter_id']==ch['id']
                        and x['quote']==paragraph['text'] and x['source_id']==ch['source_id']
                        and x['url']==ch['source']['permalink'] and x.get('scope') for x in refs))
    except (TypeError,KeyError,ValueError,OSError):
        return False
