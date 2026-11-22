"""《南史》混合篇內王弘之原有三段的逐項覆核。"""
from pathlib import Path
import hashlib,json
CID='c-nanshi-024-wang-family'
FRAME='source-evidence/nanshi024-wanghongzhi/frames.json'
PRINTED='source-evidence/nanshi024-wanghongzhi/print-collation.json'
HASHES={'source-evidence/nanshi024-wanghongzhi/frames.json': '8f7af0eadd23c3b411aeeea60a2cb532f99ee27797de5d14fa0b881bcca30b34', 'source-evidence/nanshi024-wanghongzhi/print-collation.json': '26ff2026a35d0eea6674155a37a58f6b863f71a869201953295cefc7b6841b3f', 'sources/nanshi/nanshi024-ws1765279.wikitext': '8fd9281c1d58e066b75c0b6cce86fff07d6e11c8ad6426459f8e0f2139a29499'}
PROPOSALS={'tp-nanshi024-wanghongzhi-shuzi': ('d37396fddd4f41ae5854ffe13a0eeabe3af17c2892b2604ef37724948a52afe5', '57b6db63b33e6516f0e121929ecd1641a468d84a42346bddf61d1c8e9317213e'), 'tp-nanshi024-wanghongzhi-tongzhi': ('d37396fddd4f41ae5854ffe13a0eeabe3af17c2892b2604ef37724948a52afe5', 'dffc226b06cdbfcd97a1a35199fde41c72a40d51764ec0c1d6910739286ae763')}

def h(s):return hashlib.sha256(s.encode()).hexdigest()
def hd(v):return h(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def get(root,path):
    r=Path(root).resolve();p=r/path
    if p!=p.resolve()or not p.is_relative_to(r):raise ValueError('原證路徑')
    s=p.read_text()
    if h(s)!=HASHES[path]:raise ValueError('原證指紋')
    return s

def frame(root):return json.loads(get(root,FRAME))

def errors(ch,root):
    if ch['id']!=CID:return []
    try:
        fixed=frame(root);collation=json.loads(get(root,PRINTED));ls=get(root,fixed['raw_path']).splitlines();A=ch['annotation'];ps={p['id']:p for p in ch['paragraphs']};ids=[p['id']for p in fixed['paragraphs']]
        if len(collation['columns'])!=6 or ch['source_id']!=fixed['old_source_id'] or ch['source']['revision_id']!=1765279:raise ValueError('版本')
        for proof in fixed['paragraphs']:
            p=ps[proof['id']];i=proof['line']
            if p['source_position']['first_line']!=i or p['source_position']['last_line']!=i or p['text']!=ls[i-1] or proof['text_sha256']!=h(p['text']) or proof['mentions_sha256']!=hd(p['mentions']) or p['annotation_status']!='reviewed':raise ValueError('原文或舊標')
        if A['biography_source_reviews']['王弘之']!=fixed['source_review']:raise ValueError('覆核範圍')
        if [v for v in A['person_reference_occurrences'] if v['paragraph_id'] in ids]!=fixed['references']:raise ValueError('稱謂')
        if [v for v in A['narrative_readings'] if v['source_anchor']['paragraph_id']in ids]!=fixed['readings']:raise ValueError('事跡')
        if [v for v in A['title_proposals'] if v['id']in PROPOSALS]!=fixed['proposals']:raise ValueError('未到任')
        return []
    except (KeyError,ValueError,TypeError,OSError):return ['南史王弘之傳原77、79、81行的字位或覆核範圍不符']

def kin_valid(row,ch,root):return ch['id']==CID and not errors(ch,root) and row in frame(root)['kin']

def side_errors(row,ch,root,key):
    if ch['id']!=CID:return []
    try:
        fields={'assertions':'kin','holdings':'offices','events':'life'};wanted=frame(root)[fields[key]];chosen={v['id']for v in wanted}
        if [v for v in row[key]if v['id']in chosen]!=wanted:raise ValueError('原證')
        return []
    except (KeyError,ValueError,TypeError,OSError):return ['南史王弘之原有卒條及新讀親屬官職須保留同段原證']

def proposal_valid(q,ch):
    try:
        p=next(p for p in ch['paragraphs']if p['id']==q['role_anchor']['paragraph_id'])
        if ch['id']!=CID or PROPOSALS[q['id']]!=(h(p['text']),hd(q)):return False
        return all(a['paragraph_id']==p['id']and p['text'][a['start']:a['end']]==a['surface']for a in (q['role_anchor'],q['appointment_anchor'],q['non_assumption_anchor']))
    except (KeyError,ValueError,TypeError,StopIteration):return False
