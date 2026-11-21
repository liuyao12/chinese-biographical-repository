"""覆核《南史》武英殿本王韶之傳的原欄與具人原證。"""
from pathlib import Path
import json
import hashlib

CID='c-nanshi-024-wangshaozhi-wyd'
RAW='source-evidence/nanshi024-wangshaozhi-wyd/columns.txt'
LEDGER='source-evidence/nanshi024-wangshaozhi-wyd/reading.json'
FRAMES='source-evidence/nanshi024-wangshaozhi-wyd/frames.json'
HASHES={'source-evidence/nanshi024-wangshaozhi-wyd/columns.txt': 'af3de450fdc0e9b276536e944f5eb2441b4e43d32c08efdad27bd6452c20a868', 'source-evidence/nanshi024-wangshaozhi-wyd/reading.json': '767562ca49ff23a2f31e176c1d7329fcc9c13b80329eeda7d7c0c53b7cfe9727', 'source-evidence/nanshi024-wangshaozhi-wyd/frames.json': 'ec5cfcb82522c989aabf043ab2306e7ed585b18305bf0aa1e10579de084485b8'}

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
        if len(lines)!=24 or len({x[0] for x in lines})!=24 or any(len(w)!=(7 if k=='43L06' else 21) for k,w in lines):
            raise ValueError('24欄，末欄7字')
        if len(ch['paragraphs'])!=5 or len(ledger['paragraph_spans'])!=5 or ch['source_id']!=proof['source_id'] or data_hash(ch['source'])!=proof['source_sha256']:
            raise ValueError('篇首與校本')
        text=''.join(w for _,w in lines)
        for i,(k,w) in enumerate(lines):
            row=ledger['columns'][i]
            if (row['column'],row['text'],row['start_codepoint'],row['end_codepoint'])!=(k,w,i*21,i*21+len(w)):
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
        if pos!=490 or ch['text_sha256']!=proof['body_sha256'] or digest('\n\n'.join(p['text'] for p in ch['paragraphs']))!=proof['body_sha256']:
            raise ValueError('傳文與王悅之傳界')
        if data_hash(ch['annotation'])!=proof['annotation_sha256'] or data_hash([p['mentions'] for p in ch['paragraphs']])!=proof['mentions_sha256']:
            raise ValueError('人名、親稱與諸說')
        return []
    except (ValueError,KeyError,TypeError,IndexError,OSError) as problem:
        return ['南史武英殿本王韶之傳原欄不符：'+str(problem)]

def side_errors(d,ch,root,key):
    if ch['id']!=CID:
        return []
    try:
        if d[key]!=frame(root)[key]:
            raise ValueError('原證')
        return []
    except (ValueError,KeyError,TypeError,OSError):
        return ['殿本王韶之親屬、官職或生卒的原欄與人物不符']

def kin_valid(a,ch,root):
    return ch['id']==CID and not errors(ch,root) and a in frame(root)['assertions']

def death_valid(e,q,ch,root):
    return ch['id']==CID and not errors(ch,root) and e in frame(root)['events'] and e['evidence']==[q]
