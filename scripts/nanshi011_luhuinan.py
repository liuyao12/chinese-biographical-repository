"""按固定原始碼位覆核 南史宋書路惠男與路氏親屬。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-011-luhuinan', 'c-songshu-041-luhuinan', 'c-songshu-008-luhuinan-death-context', 'c-songshu-007-lu-empress-accession-context')
F='source-evidence/nanshi011-luhuinan/frames.json'
FS='170e75cdaaeb08b94a5963dde1ad09c4bf3934db8e70c70beafdb972b2b42d9e'
R='source-evidence/nanshi011-luhuinan/reading.json'
RS='bc1772a27be27214b1ee822b77dbf7d761d63429c2b0ec11796ae87836d61924'
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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史宋書路惠男與路氏親屬 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史宋書路惠男與路氏親屬 的親屬、職序或身後事與所據原句不合']

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

def age_recipient(age, evidence, chapter, root):
    if chapter.get('id') != 'c-songshu-041-luhuinan' or errors(chapter,root):
        return False
    reports=chapter['annotation'].get('age_assertions', [])
    if age not in reports or age.get('evidence') != [evidence]:
        return False
    p=chapter['paragraphs'][5]
    token=next((r for r in chapter['annotation']['person_reference_occurrences'] if r['id']==evidence.get('person_reference_id')), None)
    return (token is not None and token['person_id']==age['person_id']=='bfe_7hz_jcb'
            and evidence['chapter_id']==chapter['id'] and evidence['paragraph_id']==token['paragraph_id']==p['id']
            and p['text'][token['start']:token['end']]==token['surface']=='崇憲太后'
            and evidence['quote']==p['text'] and '尋崩，時年五十五。' in p['text']
            and age['age_context']['life_event_id']=='le-nanshi011-luhuinan-s-death'
            and age['value']==55 and age['source_term']=='時年五十五')
