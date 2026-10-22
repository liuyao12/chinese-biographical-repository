# coding: utf-8
"""Source-bound 從中表 category; no generation, cousin degree or genealogy path."""
import hashlib
from pathlib import Path

_Q = {'source_term', 'kinship_basis', 'relationship_class', 'source_modifier',
      'lineage', 'generation_difference', 'exact_distance',
      'common_ancestor_person_id', 'connecting_person_ids', 'subject_relative_age',
      'source_clause_binding'}


def _received(*objects):
    for obj in objects:
        if not isinstance(obj, dict):
            return False
        if any(key in obj and obj[key] != 'received_chapter'
               for key in ('source_layer', 'text_layer')):
            return False
        if any(obj.get(key) not in (None, False, [], {}) for key in
               ('annotator', 'attached_note', 'attached_notes', 'is_annotation', 'quotation')):
            return False
    return True


def _anchor(value, paragraph):
    return (isinstance(value, dict)
            and set(value) == {'paragraph_id', 'start', 'end', 'surface'}
            and value['paragraph_id'] == paragraph['id']
            and type(value['start']) is int and type(value['end']) is int
            and 0 <= value['start'] < value['end'] <= len(paragraph['text'])
            and paragraph['text'][value['start']:value['end']] == value['surface'])


def _outside_quotation(text, start):
    # The narrow declaration grammar is narrative, not reported speech or a quoted example.
    stack = []
    pairs = {'「': '」', '『': '』', '“': '”', '‘': '’'}
    for char in text[:start]:
        if char in pairs:
            stack.append(pairs[char])
        elif stack and char == stack[-1]:
            stack.pop()
        elif char in ('"', "'"):
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)
    return not stack


def valid(assertion, paragraphs, chapters, root):
    """Validate an explicit A於B為/爲從中表 claim against actual fixed raw bytes."""
    try:
        a = assertion; q = a['qualifiers']; b = q['source_clause_binding']
        if (a['predicate'] != 'kinship_unspecified' or a['status'] != 'source_attested'
                or a.get('human_reviewed') is not False or set(q) != _Q
                or q['source_term'] != '從中表'
                or q['kinship_basis'] != 'congzhongbiao_named_pair'
                or q['relationship_class'] != 'biao_kinship' or q['source_modifier'] != '從'
                or q['lineage'] != 'unspecified' or q['subject_relative_age'] != 'unknown'
                or any(q[key] is not None for key in ('generation_difference', 'exact_distance',
                       'common_ancestor_person_id', 'connecting_person_ids'))
                or len(a['evidence']) != 1
                or a['subject_person_id'] == a['object_person_id']):
            return False
        if (set(b) != {'kind', 'clause_anchor', 'relationship_anchor', 'source_fingerprint'}
                or b['kind'] != 'named_subject_yu_named_object_congzhongbiao'):
            return False
        e, = a['evidence']; cid, p = paragraphs[e['paragraph_id']]; c = chapters[cid]
        source = c['source']; pos = p['source_position']; text = p['text']
        if (e['chapter_id'] != cid or e['quote'] != text
                or c['id'] != cid or e['work_id'] != c['work_id']
                or e['book_id'] != c['book_id'] or e['source_id'] != c['source_id']
                or not _received(c, source, p, pos)):
            return False
        text_sha = hashlib.sha256('\n\n'.join(x['text'] for x in c['paragraphs']).encode()).hexdigest()
        fp = b['source_fingerprint']
        if (c['text_sha256'] != text_sha
                or set(fp) != {'source_id', 'revision_id', 'raw_sha256', 'text_sha256'}
                or not source.get('revision_id')
                or fp != {'source_id': c['source_id'], 'revision_id': source['revision_id'],
                          'raw_sha256': source['raw_file_sha256'], 'text_sha256': text_sha}):
            return False
        raw_path = Path(source['raw_path'])
        if raw_path.is_absolute() or not raw_path.parts or raw_path.parts[0] != 'sources' or '..' in raw_path.parts:
            return False
        root = Path(root).resolve(); file = root / raw_path
        if any((root / Path(*raw_path.parts[:i])).is_symlink() for i in range(1, len(raw_path.parts) + 1)):
            return False
        data = file.read_bytes(); raw = data.decode('utf-8', errors='strict')
        if (hashlib.sha256(data).hexdigest() != fp['raw_sha256']
                or source.get('raw_sha256', fp['raw_sha256']) != fp['raw_sha256']
                or pos.get('raw_path') != str(raw_path)
                or type(pos['start']) is not int or type(pos['end']) is not int
                or not 0 <= pos['start'] < pos['end'] <= len(raw)
                or raw[pos['start']:pos['end']] != pos['raw']
                or pos['raw'].strip() != text):
            return False
        # Current narrow source contract accepts a literal paragraph after trimming
        # boundary whitespace only, never a borrowed projection or silently removed note.
        mentions = {m['id']: m for m in p['mentions']}
        s = mentions[e['subject_person_mention_id']]; o = mentions[e['object_person_mention_id']]
        for m, key in ((s, 'subject_person_id'), (o, 'object_person_id')):
            if (m['kind'] != 'person' or m['person_id'] != a[key]
                    or type(m['start']) is not int or type(m['end']) is not int
                    or not 0 <= m['start'] < m['end'] <= len(text)
                    or text[m['start']:m['end']] != m['surface']):
                return False
        clause, term = b['clause_anchor'], b['relationship_anchor']
        if not _anchor(clause, p) or not _anchor(term, p):
            return False
        start, end = clause['start'], clause['end']
        paragraph_index = next(i for i, item in enumerate(c['paragraphs']) if item['id'] == p['id'])
        previous = '\n\n'.join(item['text'] for item in c['paragraphs'][:paragraph_index])
        quote_context = previous + ('\n\n' if previous else '') + text
        quote_offset = len(previous) + (2 if previous else 0) + start
        if (start != s['start'] or o['start'] != s['end'] + 1
                or text[s['end']:o['start']] != '於'
                or text[o['end']:o['end'] + 1] not in ('為', '爲')
                or term['start'] != o['end'] + 1 or term['end'] != end
                or term['surface'] != '從中表'
                or clause['surface'] != s['surface'] + '於' + o['surface'] + text[o['end']] + '從中表'
                or (start > 0 and text[start - 1] not in '。！？；')
                or end >= len(text) or text[end] not in '，。；！？'
                or not _outside_quotation(quote_context, quote_offset)):
            return False
        local = [m for m in p['mentions'] if m.get('kind') == 'person'
                 and m['start'] < end and m['end'] > start]
        return {m['id'] for m in local} == {s['id'], o['id']}
    except (KeyError, TypeError, ValueError, UnicodeError, OSError, IndexError, StopIteration):
        return False
