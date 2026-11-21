"""按固定原始碼位覆核 王僧孺家世、仕歷及書牘。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-liangshu-033-wangsengru', 'c-nanqishu-042-wangdeyuan-names', 'c-sanguozhi-013-wangsu-posthumous-rank')
F='source-evidence/liang033-wangsengru/frames.json'
FS='b50f82de2e6dce5afe9858023b72c69a9707b8a9a89db61df2bff758e468e8b1'
R='source-evidence/liang033-wangsengru/reading.json'
RS='f5b129d6b1d544f1b22856da8d4557be0c582c1c1453c3773860e679ea86927b'
PROPOSALS={'tp-liang033-wangsengru-palace': ('c-liangshu-033-wangsengru:p003', '972c9fe630f955d8a799e962a761707307fff61548dc9682834b404e95315c81', 'a2e60024272fd38832c4c83e16bd5c48c979ed6477ef5238b6e53b81db0fb4ea')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['王僧孺家世、仕歷及書牘 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['王僧孺家世、仕歷及書牘 的親屬、職序或身後事與所據原句不合']

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

def resumed_subject(context, evidence, subject, chapter):
    """The letter ends immediately before the resumption, and the following paragraph names its subject."""
    try:
        if chapter['id']!='c-liangshu-033-wangsengru' or subject!='59d_72d_924_AAA':
            return False
        pre,letter,career,following=[chapter['paragraphs'][i] for i in (5,10,11,12)]
        if not (pre['text'].startswith('僧孺坐免官') and pre['text'].endswith('乃致書於炯，以見其意。曰：')
                and letter['text'].endswith('去矣何生，高樹芳烈。裁書代面，筆淚俱下。')
                and career['text']=='久之，起爲安西安成王參軍，累遷鎮右始興王中記室，北中郎南康王諮議參軍，入直西省，知撰譜事。普通三年，卒，時年五十八。'
                and following['text'].startswith('僧孺好墳籍，聚書至萬餘卷')):
            return False
        member,=[m for m in following['mentions'] if m['start']==0 and m['end']==2 and m['surface']=='僧孺' and m['person_id']==subject]
        return (context==dict(kind='liang033_sengru_resumed_biography',paragraph_id=following['id'],person_mention_id=member['id'],quote='僧孺好墳籍')
                and evidence['context']==context and evidence['paragraph_id']==career['id']
                and evidence['chapter_id']==chapter['id'] and evidence['source_id']==chapter['source_id']
                and evidence['person_mention_id']==member['id'] and evidence['quote']==career['text'])
    except (KeyError,ValueError,IndexError,TypeError):
        return False


def resumed_title(attestation, holding, chapter):
    try:
        evidence,=holding['evidence']
        if not resumed_subject(attestation['context'],evidence,holding['person_id'],chapter):
            return False
        p=chapter['paragraphs'][11]
        return (attestation['person_mention_id']==evidence['person_mention_id'] and attestation['paragraph_id']==p['id']
                and p['text'][attestation['start']:attestation['end']]==attestation['surface']==holding['title']
                and holding['title'] in ('安西安成王參軍','鎮右始興王中記室','北中郎南康王諮議參軍'))
    except (KeyError,ValueError,IndexError,TypeError):
        return False
