"""由完整固定行投影篇中附敘，以保全截在 wiki 顯示文字內的起訖。"""
from functools import lru_cache
from pathlib import Path
try: from .sanguozhi063_layers import project_line,shown
except ImportError: from sanguozhi063_layers import project_line,shown

@lru_cache(maxsize=1)
def source_lines():
    f=Path(__file__).resolve().parents[1]/'source-evidence/sanguozhi063-wu-liu-zhao/sanguozhi063-ws2188657.wikitext'
    return f.read_text().splitlines()

def slice_text(fragment):
    return slice_volume_text(fragment, source_lines(), '卷63')


def slice_volume_text(fragment, lines, volume):
    matches=set()
    for line in lines:
        offset=line.find(fragment)
        while offset>=0:
            last=offset+len(fragment)
            main,positions,notes=project_line(line)
            selected=''.join(c for c,i in zip(main,positions) if offset<=i<last)
            if not selected:
                for a,z,_ in notes:
                    if a<=offset<last<=z:
                        text,places=shown(line[a:z],a)
                        selected=''.join(c for c,i in zip(text,places) if offset<=i<last)
                        break
            if selected:matches.add(selected)
            offset=line.find(fragment,offset+1)
    if len(matches)!=1:raise ValueError((volume+'附敘與固定行不能唯一互讀',fragment[:20]))
    return matches.pop()
