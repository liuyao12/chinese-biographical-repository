"""將卷57固定修訂的正文與裴注分開，保留每字的原始碼點。"""
import re


def shown(text, offset):
    positions = list(range(offset, offset + len(text)))
    patterns = ((r'\[\[(?:[^\[\]|]+\|)?([^\[\]|]+)\]\]', 1),
                (r'\{\{YL\|([^{}|]+)(?:\|[^{}|]+)?\}\}', 1))
    for pattern, group in patterns:
        for m in reversed(list(re.finditer(pattern, text))):
            first, last = m.span()
            low, high = m.span(group)
            text = text[:first] + text[low:high] + text[last:]
            positions[first:last] = positions[low:high]
    for pattern,group in ((r'-\{([^{}]+)\}-',1),(r"'''([^']+)'''",1)):
        for m in reversed(list(re.finditer(pattern,text))):
            a,z=m.span();i,j=m.span(group);text=text[:a]+text[i:j]+text[z:];positions[a:z]=positions[i:j]
    assert not any(tag in text for tag in ('{{', '}}', '[[', ']]', '<ref')), text
    return text, positions


def project_line(line, offset=0):
    start = len('{{quote|') if line.startswith('{{quote|') else 0
    if line[start:].startswith('　　'):
        start += 2
    end = len(line)
    if line.endswith('}}') and (line.count('}}') > line.count('{{') or line.startswith('{{quote|')):
        end -= 2
    cursor = start
    parts, positions, notes = [], [], []
    for m in re.finditer(r'\{\{\*\|((?:\{\{YL\|[^{}]+\}\}|[^{}])+)\}\}', line[start:end]):
        a, z = start + m.start(), start + m.end()
        text, indexes = shown(line[cursor:a], offset + cursor)
        parts.append(text)
        positions.extend(indexes)
        notes.append((a + 4, z - 2, len(positions)))
        cursor = z
    text, indexes = shown(line[cursor:end], offset + cursor)
    parts.append(text)
    positions.extend(indexes)
    return ''.join(parts), positions, notes
