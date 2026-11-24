"""Project the fixed early Wu witnesses with traceable raw character offsets."""
try:
    from .sanguozhi063_layers import bounds
except ImportError:
    from sanguozhi063_layers import bounds

WRAPPERS = {'ProperNoun', 'WavyBookMark', 'red', 'quote', '!'}


def shown(raw, offset=0):
    characters = []
    positions = []
    cursor = 0
    while cursor < len(raw):
        if raw.startswith("'''", cursor):
            cursor += 3
            continue
        if raw.startswith('<!--', cursor):
            cursor = raw.index('-->', cursor + 4) + 3
            continue
        if raw.startswith('{{', cursor):
            stop = bounds(raw, cursor)
            kind, sep, value = raw[cursor + 2:stop - 2].partition('|')
            if kind == 'gap' and not sep:
                cursor = stop
                continue
            assert sep and (kind in WRAPPERS or kind == 'YL'), (kind, value)
            if kind == 'YL':
                value = value.split('|', 1)[0]
            text, where = shown(value, offset + cursor + 3 + len(kind))
            characters.extend(text)
            positions.extend(where)
            cursor = stop
            continue
        if raw.startswith('[[', cursor):
            stop = raw.index(']]', cursor + 2)
            pipe = raw.find('|', cursor + 2, stop)
            start = cursor + 2 if pipe == -1 else pipe + 1
            text, where = shown(raw[start:stop], offset + start)
            characters.extend(text)
            positions.extend(where)
            cursor = stop + 2
            continue
        if raw.startswith('-{', cursor):
            stop = raw.index('}-', cursor + 2)
            characters.extend(raw[cursor + 2:stop])
            positions.extend(range(offset + cursor + 2, offset + stop))
            cursor = stop + 2
            continue
        characters.append(raw[cursor])
        positions.append(offset + cursor)
        cursor += 1
    return ''.join(characters), positions


def project_line(line, offset=0):
    """Return received text and the raw intervals of separately retained notes."""
    if line.startswith('{{quote|'):
        end = -2 if line.count('{{') == line.count('}}') and line.endswith('}}') else None
        text, positions, notes = project_line(line[8:end], offset + 8)
        return text, positions, [(a + 8, b + 8, n) for a, b, n in notes]
    if line.endswith('}}') and line.count('}}') > line.count('{{'):
        return project_line(line[:-2], offset)
    cursor = 0
    start = 0
    passages = []
    positions = []
    notes = []

    def append(stop):
        text, where = shown(line[start:stop], offset + start)
        passages.append(text)
        positions.extend(where)

    while cursor < len(line):
        if not line.startswith('{{', cursor):
            cursor += 1
            continue
        stop = bounds(line, cursor)
        if line.startswith('{{*|', cursor):
            append(cursor)
            notes.append((cursor + 4, stop - 2, len(positions)))
            start = stop
        cursor = stop
    append(len(line))
    return ''.join(passages), positions, notes


def project_slice(line, start, end):
    """Read an interval in its original line, including around nested markup."""
    received, positions, notes = project_line(line)
    for left, right, _ in notes:
        if left <= start < end <= right:
            text, offsets = shown(line[left:right], left)
            break
    else:
        text, offsets = received, positions
    return ''.join(char for char, index in zip(text, offsets, strict=True) if start <= index < end)
