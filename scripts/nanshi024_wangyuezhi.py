"""按固定原始碼位覆核 南史王悅之與宋書良吏王悅。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-024-wangyuezhi', 'c-songshu-092-wangyue')
F='source-evidence/nanshi024-wangyuezhi/frames.json'
FS='7f071e75a0af9bc13b4d669b159894e3ae81f2ac735741847b4c05923956b617'
R='source-evidence/nanshi024-wangyuezhi/reading.json'
RS='c09efd7ea89e3e9b107587edb01b1b62bcac8186ad2b59f034403216634cff6c'
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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史王悅之與宋書良吏王悅 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史王悅之與宋書良吏王悅 的親屬、職序或身後事與所據原句不合']

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

def song_death_era_scope(date, chapter):
    """卷九十二第七十九行於父親故事收束後重提王悅，自泰始中承至五年卒官。"""
    try:
        scope = date['narrative_era_scope']
        paragraph, = chapter['paragraphs']
        text = paragraph['text']
        if (chapter['id'] != 'c-songshu-092-wangyue'
                or chapter['source_id'] != 's-songshu-092-wangyue-ws2195614'
                or chapter['source']['revision_id'] != 2195614
                or scope['revision_id'] != 2195614
                or scope['source_id'] != chapter['source_id']
                or scope['paragraph_id'] != paragraph['id']
                or scope['raw_sha256'] != chapter['source']['raw_file_sha256']
                or scope['raw_sha256'] != '88da739ec68f6114fdca1344b9d5b1e8e49b9cbd0cc7d07506aed3b2a5c4ec8e'
                or scope['paragraph_sha256'] != h(text)
                or h(text) != '2d45417328f0d8901e2da294c79c4ee265977f4be76febb2b09298b4ca17e0e3'
                or paragraph['source_position']['first_line'] != 79
                or scope['human_reviewed'] is not False):
            return False
        binding = scope['event_binding']
        mentions = {m['id']:m for m in paragraph['mentions']}
        refs = {r['id']:r for r in chapter['annotation']['person_reference_occurrences']}
        ruler = refs[scope['polity_reference_id']]
        subject = mentions[scope['unit_subject_mention_id']]
        person = '326_faf_cd3_*AA'
        if (ruler['surface'], ruler['start'], ruler['person_id']) != ('太宗', 0, 'cti_o52_4nz'):
            return False
        if (binding['record_id'] != 'le-nanshi024-wangyuezhi-song-death'
                or binding['subject_mention_id'] != subject['id']
                or binding['subject_paragraph_id'] != paragraph['id']
                or binding['human_reviewed'] is not False or binding['event_type'] != 'death'
                or subject['person_id'] != person or scope['unit_subject_person_id'] != person
                or binding['person_id'] != person):
            return False
        def exact(anchor, word):
            start = text.index(word)
            return anchor == dict(paragraph_id=paragraph['id'],start=start,end=start+len(word),surface=word)
        era, year, death = scope['era_anchor'], scope['event_date_anchor'], binding['source_term_anchor']
        quote, = date['evidence']
        ref, = date['references']
        return (subject['end'] == era['start'] and text[subject['start']:subject['end']] == '悅'
                and exact(era, '泰始中') and exact(year, '五年') and exact(death, '卒官')
                and text[year['start']:death['end']] == '五年，卒官'
                and era['end'] < year['start'] and quote['quote'] == text == date['original_quote']
                and quote['chapter_id'] == chapter['id'] and quote['paragraph_id'] == paragraph['id']
                and quote['source_id'] == chapter['source_id'] and mentions[quote['person_mention_id']]['person_id'] == person
                and ref['columns'] == dict(dynasty='宋',era_name='泰始',first_year='465',last_year='471')
                and date['relative_year_reference']['era_expression'] == era['surface']
                and date['source_expression'] == year['surface'])
    except (AttributeError, IndexError, KeyError, TypeError, ValueError):
        return False
