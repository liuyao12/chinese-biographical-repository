"""按固定原始碼位覆核 宋書卷五十二謝景仁、恂與稚。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-songshu-052-xiejingren', 'c-jinshu-010-xieyu-death')
F='source-evidence/song052-xiejingren/frames.json'
FS='f09dc4022ec38bcc8cdb9f44fc4971aa53a6f9388bff466c5be76fed72434492'
R='source-evidence/song052-xiejingren/reading.json'
RS='91cd90d481de341600a25a7e62740f6cbda374a7eaec66d01d29d6c2818da5fc'
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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['宋書卷五十二謝景仁、恂與稚 固定段落或原字不符']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['宋書卷五十二謝景仁、恂與稚 的親屬、職序或身後事與所據原句不合']

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

def gift_valid(h0,ch,events,root):
    if ch['id']!='c-songshu-052-xiejingren' or errors(ch,root) or h0 not in frame(ch,root)['offices']:return False
    b=h0.get('posthumous_basis',{});ev=events.get(b.get('death_event_id'),{});q=b.get('source_term','');a,=h0['attestations'];return ev.get('person_id')==h0.get('person_id')=='684_eaa_511' and b.get('evidence')==h0['evidence']==ev.get('evidence')==h0['effective_period']['start']['evidence'] and ev.get('source_term')==b.get('death_term')=='卒' and '十二年，卒，時年四十七。追贈金紫光祿大夫，加散騎常侍' in q and q[a['start']:a['end']]==h0['title'] and b['grant_term'] in ('追贈金紫光祿大夫','加散騎常侍') and b['grant_term'].endswith(h0['title'])

def age_valid(a,ch,root):
    if ch.get('id')!='c-songshu-052-xiejingren' or errors(ch,root):return False
    p=ch['paragraphs'][1];q,chose=a.get('source_repeated_age',{}),a.get('source_anchor',{});txt=p['text'];return a in ch['annotation'].get('age_assertions',[]) and a.get('id')=='age-song052-xiejingren-thirty2' and a.get('value')==30 and a.get('source_term')==a.get('source_number')=='三十' and q.get('speaker_id')=='u9s_w6j_8mc_AAF' and txt[chose['start']:chose['end']]=='三十' and txt[q['quotation_anchor']['start']:q['quotation_anchor']['end']]=='謝景仁三十方作著作佐郎' and txt[q['narration_anchor']['start']:q['narration_anchor']['end']]=='年三十' and a['person_id']=='684_eaa_511' and any(m['id']==a['evidence'][0].get('person_mention_id') and m['person_id']==a['person_id'] and m['start']==q['quotation_anchor']['start']for m in p['mentions'])
