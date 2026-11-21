"""覆核《南齊書》武英殿本王融傳的原欄與具人原證。"""
from pathlib import Path
import json
import hashlib

CID='c-nanqishu-047-wangrong-wyd'
RAW='source-evidence/nanqi047-wangrong-wyd/columns.txt'
LEDGER='source-evidence/nanqi047-wangrong-wyd/reading.json'
FRAMES='source-evidence/nanqi047-wangrong-wyd/frames.json'
HASHES={'source-evidence/nanqi047-wangrong-wyd/columns.txt': 'b3e13ccecc0f8c15729050515a6de4188790d8f8462c2804f0031b37022b7043', 'source-evidence/nanqi047-wangrong-wyd/reading.json': 'df27e40da54fd4fab2bb86d5222f91f08081d78416a8d2943d3ef4825c33a0b6', 'source-evidence/nanqi047-wangrong-wyd/frames.json': '95182ae49aab10e3c82d2f1b3de7a2919f756ccd734067d199d20a780537f9d9'}

def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()

def data_hash(v):
    return digest(json.dumps(v, ensure_ascii=False, indent=2)+'\n')

def fixed(root, relative):
    root=Path(root).resolve()
    p=root/relative
    if p!=p.resolve() or not p.is_relative_to(root):
        raise ValueError('來源路徑')
    text=p.read_text()
    if digest(text)!=HASHES[relative]:
        raise ValueError('原錄指紋')
    return text

def frame(root):
    return json.loads(fixed(root,FRAMES))

def errors(ch,root):
    if ch['id']!=CID:
        return []
    try:
        proof=frame(root)
        ledger=json.loads(fixed(root,LEDGER))
        lines=[line.split() for line in fixed(root,RAW).splitlines()]
        if len(lines)!=159 or len({x[0] for x in lines})!=159 or any(len(w)!=21 for _,w in lines):
            raise ValueError('159欄，每欄21字')
        if len(ch['paragraphs'])!=23 or len(ledger['paragraph_spans'])!=23 or ch['source_id']!=proof['source_id'] or data_hash(ch['source'])!=proof['source_sha256']:
            raise ValueError('篇首與校本')
        text=''.join(w for _,w in lines)
        for i,(k,w) in enumerate(lines):
            row=ledger['columns'][i]
            if (row['column'],row['text'],row['start_codepoint'],row['end_codepoint'])!=(k,w,i*21,(i+1)*21):
                raise ValueError('原欄')
        pos=0
        for p,s in zip(ch['paragraphs'],ledger['paragraph_spans']):
            lo,hi=s['start_codepoint'],s['end_codepoint']
            if p['id']!=s['paragraph_id'] or lo!=pos or not lo<hi<=len(text) or p['text']!=text[lo:hi]:
                raise ValueError('逐段唯一起訖')
            parts=[]
            for row in ledger['columns']:
                a,b=row['start_codepoint'],row['end_codepoint']
                if a<hi and b>lo:
                    start=max(a,lo)-a
                    end=min(b,hi)-a
                    cell={k:row[k] for k in ('column','pdf_page','half','leaf','column_from_right')}
                    parts.append(dict(cell,start=start,end=end,text=row['text'][start:end]))
            if p['source_position']!={'revision_id':ch['source']['revision_id'],'source_layer':'received_biography','column_projection':parts}:
                raise ValueError('逐欄回投')
            pos=hi
        if pos!=3339 or ch['text_sha256']!=proof['body_sha256'] or digest('\n\n'.join(p['text'] for p in ch['paragraphs']))!=proof['body_sha256']:
            raise ValueError('傳文與謝朓傳界')
        if data_hash(ch['annotation'])!=proof['annotation_sha256'] or data_hash([p['mentions'] for p in ch['paragraphs']])!=proof['mentions_sha256']:
            raise ValueError('人名、親稱與諸說')
        return []
    except (ValueError,KeyError,TypeError,IndexError,OSError) as problem:
        return ['南齊書武英殿本王融傳原欄不符：'+str(problem)]

def side_errors(d,ch,root,key):
    if ch['id']!=CID:
        return []
    try:
        if d[key]!=frame(root)[key]:
            raise ValueError('原證')
        return []
    except (ValueError,KeyError,TypeError,OSError):
        return ['殿本王融親屬、官職或生卒的原欄與人物不符']

def kin_valid(a,ch,root):
    return ch['id']==CID and not errors(ch,root) and a in frame(root)['assertions']

def death_valid(e,q,ch,root):
    return ch['id']==CID and not errors(ch,root) and e in frame(root)['events'] and e['evidence']==[q]
