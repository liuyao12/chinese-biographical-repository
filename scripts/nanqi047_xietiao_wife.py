"""核對王敬則女在南齊書、南史的同段稱謂及本卷文體分界。"""
import json
import hashlib
from pathlib import Path
F='source-evidence/nanqi047-xietiao-wife/frames.json'
L='source-evidence/nanqi047-xietiao-wife/whole-volume.json'
SHA={'source-evidence/nanqi047-xietiao-wife/frames.json': 'd35d6f0e8a58b5e75a3a9ada99a2b6ebc0b145cc40994a41d06cf9a400b3f91c', 'source-evidence/nanqi047-xietiao-wife/whole-volume.json': '2e7e9c21218aa9940e719c352d5f20bbb9f8aa5983c61126f1d078713be8a93f'}
IDS=['c-nanqishu-047-xietiao', 'c-nanshi-019-xietiao']

def read(root,path):
    r=Path(root).resolve()
    f=r/path
    if f!=f.resolve() or not f.is_relative_to(r):
        raise ValueError('path')
    text=f.read_text()
    if hashlib.sha256(text.encode()).hexdigest()!=SHA[path]:
        raise ValueError('hash')
    return json.loads(text)

def errors(ch,root):
    if ch['id'] not in IDS:return []
    try:
        rec=read(root,F)[ch['id']]
        p,=[p for p in ch['paragraphs'] if p['id']==rec['paragraph_id']]
        if not (ch['source']['revision_id']==rec['revision'] and hashlib.sha256(p['text'].encode()).hexdigest()==rec['paragraph_sha']):
            raise ValueError('原文')
        for row in rec['references']:
            if row not in ch['annotation']['person_reference_occurrences'] or row['quote']!=p['text'] or p['text'][row['start']:row['end']]!=row['surface']:
                raise ValueError('人稱')
        v=read(root,L)
        raw=(Path(root)/v['source']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=v['sha256']:raise ValueError('齊47底本')
        lines=raw.decode().splitlines()
        for row in v['line_boundaries']:
            text=lines[row['source_line']-1]
            if hashlib.sha256(text.encode()).hexdigest()!=row['raw_line_sha256'] or not text.startswith(row['opening']) or not text.endswith(row['closing']):raise ValueError('段界')
        return []
    except (OSError,ValueError,KeyError,TypeError,IndexError):
        return ['王敬則女父夫兩端、原人稱或卷界不合']

def valid(a,ch,root):
    return ch['id'] in IDS and not errors(ch,root) and a in read(root,F)[ch['id']]['assertions']
