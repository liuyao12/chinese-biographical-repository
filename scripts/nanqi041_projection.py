"""Reconstruct fixed Nanqishu text while retaining explicitly encoded rare glyphs."""
import re

try:
    from .sanguozhi063_layers import bounds
except ImportError:
    from sanguozhi063_layers import bounds


def decode_line(line, offset=0):
    text = []
    spans = []
    annotations = []
    cursor = int(line.startswith(':　　'))
    while cursor < len(line):
        if line.startswith('<ref>', cursor):
            end = line.index('</ref>', cursor + 5)
            annotations.append(dict(kind='數位校注', raw_start=offset + cursor,
                                    raw_end=offset + end + 6, source=line[cursor + 5:end]))
            cursor = end + 6
            continue
        if line.startswith('{{', cursor):
            end = bounds(line, cursor)
            token = line[cursor + 2:end - 2]
            name, separator, content = token.partition('|')
            if not separator:
                raise ValueError(f'未識模板 {token}')
            if name == '*':
                annotations.append(dict(kind='注音及小字', raw_start=offset + cursor,
                                        raw_end=offset + end, source=content))
            elif name == '?':
                annotations.append(dict(kind='存疑構形', raw_start=offset + cursor,
                                        raw_end=offset + end, source=content))
                start = cursor + 3 + len(name)
                text.append(content)
                spans.extend([offset + p, offset + p + 1] for p in range(start, start + len(content)))
            elif name == '!':
                nested = bounds(content, 0) if content.startswith('{{') else 0
                mark, separator, description = content[nested:].partition('|')
                glyph = content[:nested] if nested else mark
                start = cursor + 3 + len(name)
                if nested:
                    if mark or not separator or not glyph.startswith('{{Unihan|'):
                        raise ValueError(token)
                    code = glyph.removeprefix('{{Unihan|').removesuffix('}}')
                    if not re.fullmatch('[0-9A-F]{4,6}', code):
                        raise ValueError(token)
                    text.append(chr(int(code, 16)))
                    spans.append([offset + start, offset + start + nested])
                else:
                    if len(glyph) != 1 or not separator:
                        raise ValueError(token)
                    text.append(glyph)
                    spans.append([offset + start, offset + start + 1])
                annotations.append(dict(kind='字形標記', raw_start=offset + cursor,
                                        raw_end=offset + end, source=description))
            elif name == 'YL':
                start = cursor + 3 + len(name)
                value = content.split('|', 1)[0]
                text.append(value)
                spans.extend([offset + p, offset + p + 1] for p in range(start, start + len(value)))
            else:
                raise ValueError(f'未識模板 {name}')
            cursor = end
            continue
        if line.startswith('[[', cursor):
            end = line.index(']]', cursor + 2)
            start = line.rfind('|', cursor + 2, end)
            start = start + 1 if start != -1 else cursor + 2
            text.append(line[start:end])
            spans.extend([offset + p, offset + p + 1] for p in range(start, end))
            cursor = end + 2
            continue
        text.append(line[cursor])
        spans.append([offset + cursor, offset + cursor + 1])
        if 0xE000 <= ord(line[cursor]) <= 0xF8FF:
            annotations.append(dict(kind='數位本私用區字元', raw_start=offset + cursor,
                                    raw_end=offset + cursor + 1, source=hex(ord(line[cursor]))))
        cursor += 1
    reading = ''.join(text)
    assert len(reading) == len(spans)
    return reading, spans, annotations


def verify_positions(chapter, raw):
    """Check direct, expanded, and unresolved source characters against the pinned witness."""
    positions = [0]
    lines = raw.splitlines(keepends=True)
    for line in lines:
        positions.append(positions[-1] + len(line))
    prior = 0
    for paragraph in chapter['paragraphs']:
        source = paragraph['source_position']
        n = source['first_line']
        assert prior < n == source['last_line'] <= len(lines)
        text, spans, _ = decode_line(lines[n - 1].rstrip('\r\n'), positions[n - 1])
        assert paragraph['text'] == text
        assert source['raw_start'] == positions[n - 1]
        assert source['raw_end'] == positions[n - 1] + len(lines[n - 1].rstrip('\r\n'))
        if all(b == a + 1 for a,b in spans):
            assert source['raw_character_offsets'] == [a for a,_ in spans]
        else:
            assert source['raw_character_spans'] == spans
        prior = n
