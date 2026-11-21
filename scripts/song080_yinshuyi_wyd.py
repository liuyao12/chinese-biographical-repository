"""核對卷八十武英殿本母序與子鸞傳節錄。"""
from pathlib import Path
import hashlib,json
CID='c-songshu-080-yinshuyi-wyd'
FILES={'source-evidence/song080-yinshuyi-wyd/column-collation.json': '717a89af9a75eebcfbd6b02d961ddb3f13f09bc8b9f534d3f78193e00aec16dc', 'source-evidence/song080-yinshuyi-wyd/columns.txt': 'decae79aae97c5d073f20a297a85a6089ef8a3b6cd45b769eca114fba95e7023', 'corpus/songshu/080-yinshuyi-wyd.json': '7cb4889f71efc6a8b39fc9af0dca7bb659fcfc9b0bb6f0f2764981e496ac35e8', 'corpus/songshu/080-yinshuyi-wyd-assertions.json': 'a3905eadeb3484bafc863c284d47477e036045c26d9ba759f3363f65d705b007'}
RECORD='corpus/songshu/080-yinshuyi-wyd.json'
LEDGER='source-evidence/song080-yinshuyi-wyd/column-collation.json'
def digest(text):return hashlib.sha256(text.encode()).hexdigest()
def canonical(value):return digest(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def errors(ch,root):
    if ch.get('id')!=CID:return []
    try:
        root=Path(root).resolve()
        for path,sha in FILES.items():
            f=root/path
            if f.resolve()!=f or digest(f.read_text())!=sha:raise ValueError('原證指紋')
        if canonical(ch)!=FILES[RECORD]:raise ValueError('所讀原字')
        ledger=json.loads((root/LEDGER).read_bytes())
        cols={r['column']:r for r in ledger['columns']}
        for projection,text in [(p['source_position']['column_projection'],p['text']) for p in ch['paragraphs']]+[(x['printed_projection'],x['printed_quote']) for x in ledger['collations']]:
            if ''.join(cols[x['column']]['text'][x['start']:x['end']] for x in projection)!=text:raise ValueError('刊本原欄')
        raw=(root/'sources/songshu/songshu080-ws2261200.wikitext').read_text()
        if digest(raw)!='4900b71a1b578913596a47b7fc1f73a48e7fe0583d7c243ea19d5672fd66b76b':raise ValueError('數位卷八十版本')
        lines=raw.splitlines()
        for x in ledger['collations']:
            if lines[x['digital_line']-1][x['digital_start']:x['digital_end']]!=x['digital_quote']:raise ValueError('卷八十主文與校注界')
        return []
    except (OSError,ValueError,TypeError,KeyError,IndexError):return ['宋書卷八十武英殿本母序或子鸞傳原欄不符']
