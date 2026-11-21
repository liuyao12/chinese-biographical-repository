"""按固定原始碼位覆核 南京象山九號墓三方誌文。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-epitaph-wangjianzhi-full', 'c-epitaph-liumeizi-stone-full', 'c-epitaph-liumeizi-brick-full')
F='source-evidence/xiangshan-m9-epitaphs/frames.json'
FS='19a908836c0f60c128bd5e50260b2d942b85162330e20bcd629fe96dd5baa395'
R='source-evidence/xiangshan-m9-epitaphs/reading.json'
RS='47ef7771ccd6d3b7b9e0c4ad989b4952cd87e064eb44642cb621f1aa913a0eea'
PROPOSALS={'tp-xiangshan-m9-xicao': ('c-epitaph-wangjianzhi-full:p001', 'b24f19246f104609b1362cc62ee8d5bf0acae3d3af4b0f5af9fd296cb2ffd507', 'd60ed0b7a3b2daefb97931643d9110f90aee187aeaae4bd2b806f046d510bfa7'), 'tp-xiangshan-m9-biejia': ('c-epitaph-wangjianzhi-full:p001', 'b24f19246f104609b1362cc62ee8d5bf0acae3d3af4b0f5af9fd296cb2ffd507', 'b4f74343af534927c86e71e1c1539792af11cc5424c131949b3052f217fbb228')}

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
        if (ch['source_id'],s['raw_path'],s['raw_file_sha256'],s['revision_id'],s['image_verified'])!=(u['source_id'],u['source_path'],u['raw_sha256'],None,True):raise ValueError('實物及轉寫見證')
        plate=json.loads(source(root,'source-evidence/xiangshan-m9-epitaphs/columns-and-editions.json','b5f7c5e9622ab2801931e6101c1e3a7c7fd9c23f6718ac85161a68ae448c397a'))['witnesses']
        witness,=[w for w in plate.values() if w['columns_file']==u['source_path']]
        if hd(s)!=u['source_metadata_sha256']:raise ValueError('來源書目及圖版識別')
        if [l.rstrip('\n') for l in ls]!=[w['text'] for w in witness['columns']]:raise ValueError('圖版欄次')
        if hd([p['source_position']for p in ps])!=u['positions_sha256']:raise ValueError('欄位選取')
        for i,p in enumerate(ps,1):
            pos=p['source_position'];ix=pos['raw_character_offsets']
            if p['id']!=u['paragraph_ids'][i-1] or pos['first_line']!=1 or pos['last_line']!=len(ls) or hd(ix)!=pos['projection_sha256'] or ix!=sorted(set(ix)) or ''.join(raw[v]for v in ix)!=p['text']:raise ValueError('原字')
        if h('\n\n'.join(p['text']for p in ps))!=u['body_sha256'] or ch['text_sha256']!=u['body_sha256'] or hd(ch['annotation'])!=u['annotation_sha256'] or hd([p['mentions']for p in ps])!=u['mentions_sha256']:raise ValueError('姓名、引語及官次')
        for v in json.loads(source(root,R,RS))['comparisons']:
            l=source(root,v['fixed_path'],v['sha256']).splitlines()[v['source_line']-1]
            if l[v['start']:v['end']]!=v['quote']:raise ValueError('旁證')
        return []
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南京象山九號墓三方誌文 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        expected=frame(ch,root)[k]
        if key=='events' and 'record_type'in d:
            burial=d['record_type']=='person_event_assertion_set'
            expected=[r for r in expected if (r['event_type']=='burial')==burial]
        if d[key]!=expected:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南京象山九號墓三方誌文 的親屬、職序或身後事與所據原句不合']

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
def inscribed_year_valid(date,event,role,chapters,root):
    """同一古誌的年號、日期、朔與日干支，均須繫同一事件。"""
    try:
        if role!='life_event' or date!=event['normalized_date']:
            return False
        ch=chapters[event['evidence'][0]['chapter_id']]
        if event not in frame(ch,root)['life'] or errors(ch,root):
            return False
        p,=ch['paragraphs']
        parts=event['inscribed_date_components']
        def present(anchor,term):
            return (anchor['paragraph_id']==p['id'] and anchor['surface']==term
                    and p['text'][anchor['start']:anchor['end']]==term)
        year=parts['regnal_year']
        if date['year']!=date['era_year'] or not present(year['anchor'],year['era_name']+('六' if year['year']==6 else '二')+'年'):
            return False
        if (year['era_name'],year['year'],date['year']) not in [('泰和',6,371),('咸安',2,372)]:
            return False
        if not present(parts['month_anchor'],parts['month_anchor']['surface']) or not present(parts['day_anchor'],parts['day_anchor']['surface']):
            return False
        first,last=parts['first_day_sexagenary'],parts['day_sexagenary']
        if first is not None:
            if not present(parts['first_day_anchor'],first+'朔') or not present(parts['day_sexagenary_anchor'],last):
                return False
            cycle=['甲乙丙丁戊己庚辛壬癸'[i%10]+'子丑寅卯辰巳午未申酉戌亥'[i%12] for i in range(60)]
            if (cycle.index(last)-cycle.index(first))%60!=parts['day']-1:return False
        return date['evidence']==event['evidence'] and date['original_quote']==p['text'] and date['source_expression']==event['date_expression']
    except (TypeError,KeyError,IndexError,ValueError,OSError):return False
def plate_source_errors(chapter,root,works,books):
    try:
        src=chapter['source']
        if (chapter['id'] not in CIDS or works[chapter['work_id']]['work_type']!='single_epitaph'
                or books[chapter['book_id']]['unit_kind']!='editorial_single_text_container'
                or books[chapter['book_id']]['number'] is not None
                or src['transcription_witness']['original_object_accessed'] is not False):
            raise ValueError('原物與圖版')
        return errors(chapter,root)
    except (KeyError,TypeError,ValueError):
        return ['象山M9墓誌卷界或原物核讀狀態不符']
