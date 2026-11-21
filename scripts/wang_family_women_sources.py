"""Project the fixed received text and its editorial notes for the Wang family witnesses."""
from pathlib import Path
from hashlib import sha256
import re

FOLDER = 'source-evidence/nanshi022-wang'
SOURCES = {
    'nanshi': (2288359, 'nan011-ws2288359.wikitext', '056a4790420554786f40b92b14255aeec0a0eb168722bfeda19ad5f78f6363d4'),
    'songshu': (2634831, 'song041-ws2634831.wikitext', '9bbc04376eabe39a2e58ca12fb45068b667ae57102a566f557d564efb9556d55'),
}
UNITS = {
    'c-nanshi-011-yuanqigui': ('nanshi', (35, 37), True),
    'c-songshu-041-yuanqigui': ('songshu', tuple(range(193,216,2)), True),
    'c-nanshi-011-panshufei': ('nanshi', (40,), True),
    'c-nanshi-011-shenrongji': ('nanshi', (52,), True),
    'c-nanshi-011-zangqiyuan': ('nanshi', (23,), False),
}
TOKENS = re.compile(r'<ref>.*?</ref>|\{\{YL\|([^{}|]*)\}\}|\[\[([^\[\]]+)\]\]|-\{([^{}|:;< >])\}-')


def projection(raw, unit):
    work, lines, complete = UNITS[unit]
    body = raw.splitlines(keepends=True)
    sections = []
    for number in lines:
        line = body[number-1].rstrip('\n')
        if not complete:
            line = line[:line.index('郡功曹。')+len('郡功曹。')]
        start = sum(map(len,body[:number-1]))
        kept, notes = [], []
        last = int(line.startswith(':'))
        for m in TOKENS.finditer(line):
            kept.extend(range(start+last,start+m.start()))
            last = m.end()
            if m[0].startswith('<ref>'):
                notes.append((start+m.start(),start+m.end(),m[0]))
                continue
            if m[1] is not None: a,b = m.start(1),m.end(1)
            elif m[2] is not None:
                a,b = m.start(2) + m[2].rfind('|')+1,m.end(2)
            else: a,b=m.start(3),m.end(3)
            kept.extend(range(start+a,start+b))
        kept.extend(range(start+last,start+len(line)))
        text=''.join(raw[i]for i in kept)
        if any(w in text for w in ('<ref','</ref','[[',']]','{{','}}','-{','}-')):
            raise ValueError('unknown markup')
        sections.append((number,text,start,start+len(line),kept,notes))
    return sections


def errors(ch,root):
    if ch['id'] not in UNITS:
        return []
    try:
        work, lines, full = UNITS[ch['id']]
        rev, name, sha = SOURCES[work]
        rel = FOLDER + '/' + name
        root = Path(root).resolve()
        f = root/rel
        if f.resolve() != f or sha256(f.read_bytes()).hexdigest() != sha:
            raise ValueError('file')
        s=ch['source']
        if (s['raw_path'],s['raw_file_sha256'],s['revision_id'],ch['work_id'])!=(rel,sha,rev,'w-'+work):
            raise ValueError('identity')
        raw=f.read_text()
        all_lines=raw.splitlines()
        if full and (not all_lines[lines[0]-2].startswith('===') or
                     not next(x for x in all_lines[lines[-1]:] if x).startswith('===')):
            raise ValueError('bounds')
        expected=projection(raw,ch['id'])
        pars=ch['paragraphs']
        if len(pars)!=len(expected):
            raise ValueError('coverage')
        notes=[]
        for p,(n,text,a,b,indices,reported) in zip(pars,expected):
            loc=p['source_position']
            if (p['text'],loc['first_line'],loc['last_line'],loc['raw_start'],loc['raw_end'],
                loc['raw_character_offsets'],loc['revision_id']) != (text,n,n,a,b,indices,rev):
                raise ValueError('projection')
            notes.extend((p['id'],i,j,s) for i,j,s in reported)
        got=[(z['paragraph_id'],z['raw_start'],z['raw_end'],z['raw_text'])
             for z in ch['annotation']['modern_collation_reports']]
        if got!=notes:
            raise ValueError('editorial notes')
    except (KeyError,ValueError,TypeError,IndexError,OSError,StopIteration):
        return ['王僧綽公主母家所在見證之原字、行段或校記不符']
    return []
# SOURCE-SPECIFIC KINSHIP FRAMES
FRAMES_PATH = 'source-evidence/wang-family-women/kinship-frames.json'
FRAMES_SHA = '766de5b0563fc84207f92f0d84fcb5e6a305c7e42821d346010feebebbe526ed'


def kin_valid(a,ch,root):
    import json
    try:
        root = Path(root).resolve()
        path = root/FRAMES_PATH
        if path.resolve() != path or sha256(path.read_bytes()).hexdigest() != FRAMES_SHA:
            return False
        frame=json.loads(path.read_text())[a['id']]
        if (errors(ch,root) or a['status'] != 'source_attested' or a['predicate'] != frame['predicate']
                or a['subject_person_id']==a['object_person_id'] or frame['source_id']!=ch['source_id']
                or frame['chapter_id']!=ch['id'] or a['qualifiers']['source_term']!=frame['word']
                or a['id']!='a-'+ch['id'][2:]+'-'+a['qualifiers']['wang_women_kin_frame']):
            return False
        e,=a['evidence']
        p,=(p for p in ch['paragraphs'] if p['source_position']['first_line']==frame['line'])
        if (any(e[k]!=ch[k] for k in ('work_id','book_id','source_id'))
                or e['chapter_id']!=ch['id'] or e['paragraph_id']!=p['id'] or e['quote']!=p['text']):
            return False
        for field,word,clause,pid in frame['endpoints']:
            if p['text'].count(clause)!=1 or clause.count(word)!=1:
                return False
            i=p['text'].index(clause)+clause.index(word)
            if field.endswith('_reference_id'):
                rows=[r for r in ch['annotation']['person_reference_occurrences']
                      if r['paragraph_id']==p['id'] and r['referent_role']=='third_person']
            else:
                rows=[m for m in p['mentions'] if m['kind']=='person']
            m,=(m for m in rows if m['start']==i and m['end']==i+len(word) and m['surface']==word)
            if m['person_id']!=pid or a[field.split('_')[0]+'_person_id']!=pid or e[field]!=m['id']:
                return False
        return True
    except (KeyError,ValueError,TypeError,OSError):
        return False
