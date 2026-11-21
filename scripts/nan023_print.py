"""按固定原始碼位覆核 南史卷二十三武英殿王誕、嘏、偃。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-023-wangdan-gu-yan-wyd',)
F='source-evidence/nan023-wangdan-wyd/frames.json'
FS='0353bc2d745d7cfdac33fbf4f350ef1693ef53d5ff2cbe0c4405b964c01dcbc5'
R='source-evidence/nan023-wangdan-wyd/reading.json'
RS='7c31839dc25779c844829b22a131faf5dd5869bee9366f9b1aa31bf032f19f9d'
PROPOSALS={'tp-nan023-print-fuguo': ('c-nanshi-023-wangdan-gu-yan-wyd:p003', '0ea919c18896fbf236faf18eed8e77ca40f6d9f475c0320c05fe35c48d460d6b', 'eef7ac82253ce5a75e1c71e12653b9b72b7c70a5b427c6f6929f0b68c638c7d8')}

def h(x):return hashlib.sha256(x.encode()).hexdigest()
def hd(v):return h(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def source(root,relative,digest):
    root=Path(root).resolve();p=root/relative
    if p!=p.resolve() or not p.is_relative_to(root):raise ValueError('來源路徑')
    s=p.read_text()
    if h(s)!=digest:raise ValueError('校本指紋')
    return s

def frame(ch,root):return json.loads(source(root,F,FS))

def errors(ch,root):
    if ch['id'] not in CIDS:return []
    try:
        f=frame(ch,root);r=json.loads(source(root,R,RS));s=ch['source'];ps=ch['paragraphs'];raw=source(root,r['raw_path'],s['raw_file_sha256'])
        if f['chapter_id']!=ch['id'] or ch['source_id']!='s-nanshi-023-wangdan-gu-yan-wyd1739' or hd(s)!=f['source_sha256'] or not s['image_verified'] or s['revision_id']!='cbr-ai-transcription-sha256:'+h(raw):raise ValueError('殿本來源')
        cols=r['columns'];parts=raw.splitlines();flat='';seen=[]
        if len(cols)!=len(parts) or [p['id']for p in ps]!=r['paragraph_ids']:raise ValueError('行款')
        for line,col in zip(parts,cols):
            k,t=line.split('	');loc=col['location'];start=len(flat);flat+=t
            if (k,t,start,len(flat))!=(col['column'],col['text'],col['start_codepoint'],col['end_codepoint']):raise ValueError('原欄原字')
            if loc!={'pdf_page':int(k[:-3]),'half':{'L':'左','R':'右'}[k[-3]],'column_from_right':int(k[-2:])}:raise ValueError('書影位置')
        for p in ps:
            pos=p['source_position'];a,b=pos['start_codepoint'],pos['end_codepoint']
            if a!=(seen[-1]if seen else 0) or b<=a or pos['revision_id']!=s['revision_id'] or pos['source_layer']!='received_biography' or flat[a:b]!=p['text']:raise ValueError('段界')
            seen.append(b);frag=[]
            for col in cols:
                start=col['start_codepoint'];l=max(a,start);u=min(b,col['end_codepoint'])
                if l<u:frag.append(dict(column=col['column'],**col['location'],start=l-start,end=u-start,text=flat[l:u]))
            if frag!=pos['column_projection']:raise ValueError('分欄段界')
        if seen[-1]!=len(flat) or h('\n\n'.join(p['text']for p in ps))!=ch['text_sha256'] or ch['text_sha256']!=f['body_sha256'] or hd(ch['annotation'])!=f['annotation_sha256'] or hd([p['mentions']for p in ps])!=f['mentions_sha256']:raise ValueError('姓名或事情')
        opening=r['print_only_opening']
        if ps[0]['id']!=opening['paragraph_id'] or ps[0]['text']!=opening['text'] or not ps[1]['text'].startswith(opening['digital_join']):raise ValueError('殿本傳首及續接')
        return []
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['南史卷二十三武英殿王誕、嘏、偃 的書影欄序、原字或人物指代有誤']

def kin_valid(a,ch,root):return ch['id']in CIDS and not errors(ch,root) and a in frame(ch,root)['kin']
def death_valid(event,e,ch,root):return ch['id']in CIDS and not errors(ch,root) and event in frame(ch,root)['life'] and event['evidence']==[e]
def side_errors(d,ch,root,key):
    if ch['id']not in CIDS:return []
    try:
        k={'assertions':'kin','holdings':'offices','events':'life','records':'names'}[key]
        if d[key]!=frame(ch,root)[k]:raise ValueError('原證')
        return []
    except (KeyError,TypeError,OSError,ValueError):return ['南史卷二十三武英殿王誕、嘏、偃 的親屬、職序或身後事與所據原句不合']

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

def yan_award(h,ch,root):
    if ch.get('id')!='c-nanshi-023-wangdan-gu-yan-wyd' or errors(ch,root) or h not in frame(ch,root)['offices']:return False
    pp=ch['paragraphs'][-1];text=pp['text'];basis=h.get('posthumous_basis') or h.get('naming_basis') or {};a,=h['attestations'];e,=h['evidence'];mode=h['mode'];marker='贈' if mode=='posthumous_grant' else '諡';return text.endswith('位右光祿大夫贈開府儀同三司諡恭公') and h['person_id']=='7r6_k52_qji_ABAACAAB' and (mode,h['title']) in [('posthumous_grant','開府儀同三司'),('posthumous_naming','恭公')] and e['quote']==text and basis.get('evidence')==h['evidence']==h['effective_period']['start']['evidence'] and text[a['start']-1:a['end']]==marker+h['title']
