"""Validate the printed Chen shu 7 collation without requiring privately cached page images."""
import hashlib
import json
from pathlib import Path

CHAPTER = 'c-chenshu-007-wuying-consorts'
MANIFEST = {'corpus/chenshu/007-wuying-consorts.json': '6d0eeb941d20342abaaebda598a3be56231b06ff456510a57bcddc297bce39b2', 'corpus/chenshu/007-wuying-consorts-assertions.json': '3badeee154fe347c03f020aed65f9f4fb3b10b34277568ce60bcbe53455b8243', 'corpus/chenshu/007-wuying-consorts-life-events.json': '2fd07f04fbda2cab410c7e43b825907dfa523dcbcc3810507c8f38816ff0cac1', 'corpus/chenshu/007-wuying-consorts.xml': '99f89205c6e8f90286bec57f4c76d48818f484bc62e9b7cb7790741b62faff68', 'source-evidence/chen007-wuying-consorts/columns.txt': 'af8dccf903767b99c9a789debedbd5e19b346e21cea98059d5bc194c76e387d9', 'source-evidence/chen007-wuying-consorts/column-collation.json': 'b3f880e4e66ec1f3c239ace1193a0ed63cb5db1f80b358e7c7e6dc0b0c9028d8'}
NATIVE = 'corpus/chenshu/007-wuying-consorts.json'
LEDGER = 'source-evidence/chen007-wuying-consorts/column-collation.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inspect_projection(parts, columns):
    text = []
    for part in parts:
        col = columns[part['column']]
        for key in ('pdf_page','half','column_from_right','leaf','url'):
            if col[key] != part[key]:
                raise ValueError('頁欄')
        start, end = part['start'], part['end']
        if not 0 <= start < end <= len(col['text']) or col['text'][start:end] != part['text']:
            raise ValueError('欄內字位')
        text.append(part['text'])
    return ''.join(text)

def ledger_errors(chapter, ledger, root):
    root = Path(root)
    cols = {row['column']:row for row in ledger['columns']}
    if len(cols) != len(ledger['columns']):
        raise ValueError('欄號重複')
    pars = {p['id']:p for p in chapter['paragraphs']}
    rows = ledger['collations']
    if [r['paragraph_id'] for r in rows] != list(pars):
        raise ValueError('篇內次序')
    ok_files = {}
    def checked_file(path, digest):
        if path not in ok_files:
            fp = root / path
            if fp.resolve()!=fp or sha(fp.read_bytes())!=digest:
                raise ValueError('固定讀本')
            ok_files[path] = (digest, fp.read_text().splitlines())
        cached, lines = ok_files[path]
        if cached != digest:
            raise ValueError('同檔指紋')
        return lines
    for row in rows:
        p = pars[row['paragraph_id']]
        if p['source_position']['source_layer'] != row['source_layer']:
            raise ValueError('正文與考證')
        projection = p['source_position']['column_projection']
        if projection != row['printed_projection'] or inspect_projection(projection,cols) != p['text'] or row['printed_quote'] != p['text']:
            raise ValueError('原字或起訖')
        if 'digital' in row:
            digital = row['digital']
            lines = checked_file(digital['path'],digital['sha256'])
            if lines[digital['line']-1][digital['start']:digital['end']] != digital['quote']:
                raise ValueError('數位原字位')
        for source in row.get('comparison_sources',[]):
            checked_file(source['path'],source['sha256'])
    return []

def errors(chapter,root):
    if chapter.get('id') != CHAPTER:
        return []
    try:
        root=Path(root).resolve()
        data=(json.dumps(chapter,ensure_ascii=False,indent=2)+'\n').encode()
        if sha(data)!=MANIFEST[NATIVE]:
            raise ValueError('篇章')
        for path,digest in MANIFEST.items():
            fp=root/path
            if fp.resolve()!=fp or sha(fp.read_bytes())!=digest:
                raise ValueError('篇檔')
        return ledger_errors(chapter,json.loads((root/LEDGER).read_bytes()),root)
    except (KeyError,OSError,ValueError,IndexError,TypeError):
        return ['陳書卷七武英殿本卷題、六傳及考證的書影投影或數位對讀未合。']

def fixed_assertion(record, chapter, root, collection):
    if chapter.get('id') != CHAPTER:
        return False
    try:
        path = NATIVE[:-5] + ('-assertions.json' if collection == 'assertions' else '-life-events.json')
        raw=(Path(root)/path).read_bytes()
        if sha(raw)!=MANIFEST[path] or sha((json.dumps(chapter,ensure_ascii=False,indent=2)+'\n').encode())!=MANIFEST[NATIVE]:
            return False
        if not any(x == record for x in json.loads(raw)[collection]):
            return False
        pars={p['id']:p for p in chapter['paragraphs']}
        for evidence in record['evidence']:
            p=pars[evidence['paragraph_id']]
            if p['text']!=evidence['quote'] or evidence['source_id']!=chapter['source_id']:
                return False
            endpoints={m['id']:m for m in p['mentions']}
            endpoints.update({r['id']:r for r in chapter['annotation']['person_reference_occurrences'] if r['paragraph_id']==p['id']})
            if collection=='assertions':
                people=[(u+'_person',record[u+'_person_id'])for u in ['subject','object']]
                a=evidence['relationship_anchor']
                if p['text'][a['start']:a['end']]!=record['qualifiers']['source_term'] or a['surface']!=record['qualifiers']['source_term']:
                    return False
            else:
                people=[('person',record['person_id'])]
                a=record['source_anchor']; date=record['date_expression']
                if p['text'][a['start']:a['end']]!=record['source_term'] or (date and date not in p['text']):
                    return False
            for key,person in people:
                anchors=[evidence[key+t] for t in ('_mention_id','_reference_id') if key+t in evidence]
                if len(anchors)!=1 or endpoints[anchors[0]]['person_id']!=person:
                    return False
        return True
    except (KeyError,OSError,ValueError,IndexError,TypeError):
        return False
