"""按固定原始碼位覆核 南齊書昭冑與昭穎。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanqishu-040-zhaozhou', 'c-nanshi-044-zhaozhou-heir', 'c-nanqishu-045-zhaozhou-baolan', 'c-zizhitongjian-144-zhaozhou-brothers')
F='source-evidence/nanqi040-zhaozhou/frames.json'
FS='fe4f105241a8c61f927f6542302e9cfdd0856173714b52dd4c7e8587d9763257'
R='source-evidence/nanqi040-zhaozhou/reading.json'
RS='edc7ee8041cfa1396606667a0fcbf91876cb0dd91027b795efcc9b3fe3f7ac16'
PROPOSALS={'tp-nanqi040-zhaozhou-youwei': ('c-nanqishu-040-zhaozhou:p001', '670b6026e3ddf9914f499812d017787e53f4dac6703c29f316af7d64f090171c', 'ed26b0efd365ab0619852f10eb7145938b41135c3ed9dbd29c5e7290212e4fd1')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南齊書昭冑與昭穎 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南齊書昭冑與昭穎 的親屬、職序或身後事與所據原句不合']

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

def funeral_award(holding,chapter,events,root):
    roles={'x3q_cqm_dup_A':('追贈昭冑散騎常侍、撫軍將軍',{'散騎常侍','撫軍將軍'}),
           'x3q_cqm_dup_B':('昭穎黃門郎',{'黃門郎'})}
    try:
        if chapter['id']!='c-nanqishu-040-zhaozhou' or errors(chapter,root) or holding not in frame(chapter,root)['offices']:
            return False
        b=holding['posthumous_basis'];death=events[b['death_event_id']];e,=holding['evidence'];a,=holding['attestations']
        p=next(p for p in chapter['paragraphs']if p['id']==e['paragraph_id']);d,g=b['death_anchor'],b['grant_anchor']
        phrase,titles=roles[holding['person_id']];where=p['text'].index(phrase)
        m=next(m for m in p['mentions']if m['id']==a['person_mention_id'])
        def exact(anchor):
            return p['id']==anchor['paragraph_id'] and p['text'][anchor['start']:anchor['end']]==anchor['surface']
        return (holding['person_id']==m['person_id']==death['person_id'] and death in frame(chapter,root)['life']
                and all(exact(anchor)for anchor in [d,g,a,death['source_anchor']])
                and d['start']<=death['source_anchor']['start']<death['source_anchor']['end']<=d['end']<g['start']
                and d['surface']==b['death_term']=='皆伏誅' and g['surface']==b['grant_term']=='追贈'
                and where<=m['start']<m['end']<=a['start']<a['end']<=where+len(phrase)
                and a['surface']==holding['title'] and holding['title'] in titles and a['usage']=='posthumous_usage'
                and e['quote']==b['source_term']==p['text'] and [e]==b['evidence']==holding['effective_period']['start']['evidence'])
    except (KeyError,ValueError,TypeError,StopIteration):
        return False
