"""吳書七後四題正文。保留跨行引文及兩條「另」版面校語的原位置。"""
import re
try:
    from .sanguozhi052_layers import shown
except ImportError:
    from sanguozhi052_layers import shown

def project_extended(line, base=0, in_quote=False):
    start, end = 0, len(line)
    if line.startswith('{{quote|'):
        assert not in_quote
        in_quote = True
        start = len('{{quote|')
    if line.startswith('　　',start):
        start+=2
    if in_quote and line.endswith('}}'):
        end-=2
        in_quote=False
    notes, alternatives, chars, indexes = [], [], [], []
    cursor = start
    while cursor<end:
        m=re.search(r'\{\{(?:\*|另)\|',line[cursor:end])
        a=cursor+m.start()if m else end
        text,pos=shown(line[cursor:a],base+cursor)
        chars.append(text);indexes.extend(pos)
        if not m:break
        z=line.index('}}',a+4,end)
        assert '{{' not in line[a+4:z]
        if line.startswith('{{*|',a):
            notes.append((a+4,z,len(indexes)))
        else:
            s,other=line[a+4:z].split('|')
            assert (s,other)in (('斬','擒斬'),('比','皆比肩'))
            alternatives.append(dict(start=len(indexes),end=len(indexes)+len(s),initial_reading=s,alternate_reading=other,raw_start=base+a,raw_end=base+z+2,raw_quote=line[a:z+2],source_layer='數位轉錄的「另」模板'))
            chars.append(s);indexes.extend(range(base+a+4,base+a+4+len(s)))
        cursor=z+2
    return ''.join(chars),indexes,notes,alternatives,in_quote

def passage(lines):
    result=[];inside=False
    for line in lines:
        if not line.strip():continue
        text,_,_,_,inside=project_extended(line,0,inside);result.append(text)
    assert not inside
    return result
