"""投影固定修訂2085149的正文、裴注和注中列名的引書，原文碼點按原位保留。"""
import re

# Only markup actually present in the eight Zhang and Gu headings.
DISPLAY = (
    (r'<ref>[^<>]*</ref>', None),
    (r'-\{([^{}|:;<>\s])\}-', 1),
    (r'\[\[(?:[^\[\]|]+\|)?([^\[\]|]+)\]\]', 1),
    (r'\{\{YL\|([^{}|]+)(?:\|[^{}|]+)?\}\}', 1),
)

def shown(line, base=0):
    positions = list(range(base, base + len(line)))
    for pattern, group in DISPLAY:
        for match in reversed(list(re.finditer(pattern, line))):
            a, z = match.span()
            b, e = match.span(group) if group else (a, a)
            line = line[:a] + line[b:e] + line[z:]
            positions[a:z] = positions[b:e]
    assert not any(t in line for t in ('{{','}}','[[',']]','<ref','-{','}-')), line
    return line, positions


def project_line(line, base=0):
    start = 2 if line.startswith('　　') else 0
    end = len(line)
    if line.startswith('{{quote|'):
        assert line.endswith('}}')
        start, end = len('{{quote|'), end - 2
    parts, positions, notes = [], [], []
    cursor = start
    while cursor < end:
        a = line.find('{{*|', cursor, end)
        if a < 0:
            a = end
        segment, indexes = shown(line[cursor:a], base + cursor)
        parts.append(segment)
        positions.extend(indexes)
        if a == end:
            break
        z = line.index('}}', a + 4, end)
        assert '{{' not in line[a + 4:z], line
        notes.append((a + 4, z, len(positions)))
        cursor = z + 2
    return ''.join(parts), positions, notes
