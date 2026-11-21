"""按固定原始碼位覆核 王曇生兩傳。"""
from pathlib import Path
import json
import hashlib

CIDS=('c-nanshi-024-wangtansheng',)
F='source-evidence/song093-wangtansheng/frames.json'
FS='b109d67ce705d2470b2d455de82201fb0136ac1bc948db6ab5b60e2c487a45ed'
R='source-evidence/song093-wangtansheng/reading.json'
RS='a32418c233dd8098e4b91735a59d33c6acc72f8bcdbe9de5421c31bc79661353'
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
    except (KeyError,ValueError,IndexError,OSError,TypeError):return ['王曇生兩傳 固定段落或原字不符']


S_PID='c-songshu-093-recluses:line068'
S_PATH='source-evidence/nan023-wanghuan/ws1962755.wikitext'
S_HASH='006115bbb0fa72042b9926f19b6ffbc952b7955b7f3a9fdf9c6fb3be71cb98aa'
S_RAW='-{曇}-生好文義，以謙和見稱。歴顯位，吏部尚書，太常卿。大明末，爲呉興太守。太宗初，四方同逆，戰敗奔會稽，歸降被宥，終-{於}-中散大夫。'
S_TEXT_HASH='6a721c25ec2686b96c803cac0863381cd5fb6950cb75723f1fd8f9a93ac13bf3'
S_MIDS=[('c-songshu-093-recluses:line068:m0000', '7r6_k52_qji_ABDACABA'), ('c-songshu-093-recluses:line068:m0035', 'cti_o52_4nz')]
S_READ_HASH='e05ae2aaa7c00ed0dd13527245ee92d5e5256e599aacdb04a748008e77595005'
S_TITLES='8aef0cc04fe1ad5b8f2f546bfc1dd13e5c64eb6484934a57bd87b8c2953b8c9d'

def song_errors(ch,root):
    if ch.get('id') != 'c-songshu-093-recluses':
        return []
    try:
        p, = [p for p in ch['paragraphs'] if p['id'] == S_PID]
        unit = [a for a in ch['annotation']['narrative_readings'] if a['source_anchor']['paragraph_id'] == S_PID]
        text = source(root,S_PATH,S_HASH).splitlines()[67]
        if text != S_RAW or h(p['text']) != S_TEXT_HASH or p['annotation_status'] != 'reviewed':
            raise ValueError('曇生原段')
        if S_MIDS != [(m['id'],m['person_id']) for m in p['mentions']] or hd(unit) != S_READ_HASH:
            raise ValueError('曇生字位及家世')
        return []
    except (KeyError,TypeError,OSError,ValueError):
        return ['宋書原篇曇生附敘第六十八行的原證不符']

def title_errors(row,chapter,root):
    key=chapter.get('id')
    if key=='c-songshu-093-recluses':
        data=[h for h in row['holdings'] if h['person_id']=='7r6_k52_qji_ABDACABA' and any(a['paragraph_id']==S_PID for a in h['attestations'])]
        return [] if hd(data)==S_TITLES else ['宋書曇生四職的字位或有效時段不符']
    if key in CIDS:
        return [] if row['holdings']==frame(chapter,root)['offices'] else ['南史曇生四職原證不符']
    return []
