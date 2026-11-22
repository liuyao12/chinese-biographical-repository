"""按固定原始碼位覆核 南齊書子良本傳。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanqishu-040-ziliang', 'c-nanqishu-040-ziliang-roster', 'c-nanqishu-004-ziliang-death', 'c-songshu-090-ziliang-shaoling', 'c-songshu-093-ziliang-zhu-wife', 'c-nanqishu-038-ziliang-guards')
F='source-evidence/nanqi040-ziliang/frames.json'
FS='212d8a271c5edfe6a4bc59cfcd82cf6bca585f44b8bf01df68f0465cd10dd031'
R='source-evidence/nanqi040-ziliang/reading.json'
RS='2953ba69ac26afa224d7396cbbe9fec6b8d04298bc143ed1b19ce465d47d4d58'
PROPOSALS={'tp-nanqi040-ziliang-guoziji': ('c-nanqishu-040-ziliang:p036', '914865fc41c01e000252d7765f0d88bced24b36e3279984c821e81d371b28d4a', 'ad19badd1dc5ff668dcd4a4f76122920190d48612635ff7dde64ca65028719d7')}

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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南齊書子良本傳 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南齊書子良本傳 的親屬、職序或身後事與所據原句不合']

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

def resumed_title(attestation, holding, chapter):
    try:
        supported={
            '聞喜縣公':(14,20,'子良陳之曰','封聞喜縣公，邑千五百戶。'),
            '司徒':(42,60,'子良又啓曰','五年，正位司徒，給班劔二十人'),
        }
        first,last,subject,resume=supported[holding['title']]
        if chapter['id']!='c-nanqishu-040-ziliang' or holding['person_id']!='x3q_cqm_dup':
            return False
        paragraphs=chapter['paragraphs']
        source=next(p for p in paragraphs if p['source_position']['first_line']==first)
        target=next(p for p in paragraphs if p['source_position']['first_line']==last)
        a,z=paragraphs.index(source),paragraphs.index(target)
        ctx=attestation['context'];m=next(m for m in source['mentions'] if m['id']==ctx['person_mention_id'])
        evidence,=holding['evidence']
        l,r=attestation['start'],attestation['end']
        return (ctx==dict(kind='qi040_memorial_resumption',paragraph_id=source['id'],person_mention_id=m['id'],quote=subject,
                          intervening_paragraph_ids=[p['id']for p in paragraphs[a+1:z]])
                and [p['source_position']['first_line'] for p in paragraphs[a:z+1]]==list(range(first,last+1,2))
                and source['text'].endswith(subject+'：') and source['text'][m['start']:m['end']]=='子良'
                and target['text'].startswith(resume) and target['text'][l:r]==holding['title']
                and attestation['person_mention_id']==m['id'] and m['person_id']==holding['person_id']
                and ctx==evidence['context'] and evidence['quote']==target['text']
                and attestation['paragraph_id']==evidence['paragraph_id']==target['id'])
    except (KeyError,IndexError,ValueError,StopIteration,TypeError):
        return False


def funeral_award(holding,chapter,events,root):
    try:
        if chapter['id']!='c-nanqishu-040-ziliang' or errors(chapter,root) or holding not in frame(chapter,root)['offices']:
            return False
        b=holding['posthumous_basis']; death=events[b['death_event_id']]
        e,=holding['evidence'];a,=holding['attestations'];p=next(p for p in chapter['paragraphs']if p['id']==e['paragraph_id'])
        death_loc,grant=b['death_anchor'],b['grant_anchor']
        def exact(anchor):
            return anchor['paragraph_id']==p['id'] and p['text'][anchor['start']:anchor['end']]==anchor['surface']
        return (death in frame(chapter,root)['life'] and holding['person_id']==death['person_id']=='x3q_cqm_dup'
                and death['source_anchor']['paragraph_id']==p['id'] and all(exact(v)for v in [a,death_loc,grant])
                and death_loc['start']<=death['source_anchor']['start']<death['source_anchor']['end']<=death_loc['end']<grant['start']
                and grant['surface']==b['grant_term']=='可追崇' and death_loc['surface']==b['death_term']=='尋薨'
                and grant['end']<=a['start']<a['end']<=p['text'].index('，綠綟綬')
                and a['surface']==holding['title'] and a['usage']=='posthumous_usage'
                and b['evidence']==[e]==holding['effective_period']['start']['evidence']
                and b['source_term']==p['text']==e['quote'])
    except (KeyError,ValueError,TypeError,StopIteration):
        return False
