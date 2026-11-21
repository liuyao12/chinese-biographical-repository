"""The named nephew in Wang Tai's paragraph follows the death of his sister's husband."""
from hashlib import sha256

def valid(assertion, chapters, root):
    try:
        evidence, = assertion['evidence']
        chapter = chapters[evidence['chapter_id']]
        paragraph = next(p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id'])
        source = chapter['source']
        raw = (root / source['raw_path']).read_bytes()
        decoded = raw.decode()
        text = paragraph['text']
        terms = assertion['qualifiers']
        clause = '姊夫齊江夏王鋒為齊明帝害，外生蕭子友並孤弱，泰資給撫訓，逾于子侄。'
        offset = text.index(clause)
        marks = {m['id']:m for m in paragraph['mentions'] if m['kind'] == 'person'}
        for side, word in [('subject','蕭子友'), ('object','泰')]:
            m = marks[evidence[side+'_person_mention_id']]
            start = offset + clause.index(word)
            if (m['person_id'] != assertion[side+'_person_id'] or m['start'] != start
                    or m['end'] != start + len(word) or m['surface'] != word):
                return False
        return (chapter['id'] == 'c-nanshi-022-wangtai' and source['revision_id'] == 1477957
                and sha256(raw).hexdigest() == source['raw_file_sha256']
                and ''.join(decoded[i] for i in paragraph['source_position']['raw_character_offsets']) == text
                and evidence['quote'] == text and text.count(clause) == 1
                and terms['source_term'] == '外生蕭子友' and terms['lineage'] == 'maternal'
                and terms['generation_difference'] == -1 and terms['mother_person_id'] is None
                and assertion['predicate'] == 'maternal_uncle')
    except (KeyError, ValueError, TypeError, IndexError, StopIteration):
        return False
