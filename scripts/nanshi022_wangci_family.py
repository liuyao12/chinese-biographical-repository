"""Verify named or titled family roles against an exact span of the fixed witness."""
from hashlib import sha256

# Chapter, clause and predicate determine both endpoints in their source order.
CASES = {
    ('c-nanshi-022-wangci', '慈妻劉彥節女', 'spouse'): ('慈', '妻'),
    ('c-nanshi-022-wangci', '慈妻劉彥節女', 'father'): ('女', '劉彥節'),
    ('c-nanshi-022-wangci', '子觀尚武帝長女吳縣公主', 'spouse'): ('觀', '吳縣公主'),
    ('c-nanshi-022-wangci', '子觀尚武帝長女吳縣公主', 'father'): ('吳縣公主', '武帝'),
    ('c-nanshi-022-wangci', '江夏王鋒為南徐州，王妃，慈女也', 'spouse'): ('鋒', '王妃'),
    ('c-nanshi-022-wangci', '江夏王鋒為南徐州，王妃，慈女也', 'father'): ('女', '慈'),
    ('c-nanshi-022-wangci', '慈妻劉彥節女，子觀', 'father'): ('觀', '慈'),
    ('c-nanshi-022-wangtai', '姊夫齊江夏王鋒', 'spouse'): ('鋒', '姊'),
    ('c-nanqishu-035-wangci-feng', '江夏王鋒，字宣穎，太祖第十二子。', 'father'): ('鋒', '太祖'),
    ('c-nanqishu-040-wangci-ziqing', '廬陵王子卿字雲長，世祖第三子也。', 'father'): ('子卿', '世祖'),
}
REVISIONS = {'b-nanshi-022':1477957, 'b-nanqishu-035':2401782, 'b-nanqishu-040':2272748}

def valid(claim, evidence, chapter, root):
    try:
        qualifiers = claim['qualifiers']
        basis = qualifiers['reading_basis']
        paragraph = next(p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id'])
        source = chapter['source']
        raw = (root / source['raw_path']).read_bytes()
        decoded = raw.decode()
        revision = REVISIONS[chapter['book_id']]
        text = paragraph['text']
        frame = basis['source_quote']
        start, end = basis['start'], basis['end']
        if (revision != source['revision_id'] or sha256(raw).hexdigest() != source['raw_file_sha256']
                or paragraph['source_position']['revision_id'] != revision
                or text != ''.join(decoded[i] for i in paragraph['source_position']['raw_character_offsets'])
                or evidence['quote'] != text or evidence['chapter_id'] != chapter['id']
                or text.count(frame) != 1 or text[start:end] != frame or qualifiers['source_term'] not in frame
                or claim['subject_person_id'] == claim['object_person_id']):
            return False
        marks = {r['id']:r for r in chapter['annotation']['person_reference_occurrences'] if r['paragraph_id'] == paragraph['id']}
        marks.update({m['id']:m for m in paragraph['mentions'] if m['kind'] == 'person'})
        words = CASES[(chapter['id'],frame,claim['predicate'])]
        for side, word in zip(('subject','object'),words):
            mention = marks[basis[side + '_anchor_id']]
            if (mention['person_id'] != claim[side+'_person_id'] or mention['surface'] != word
                    or not start <= mention['start'] < mention['end'] <= end
                    or text[mention['start']:mention['end']] != word):
                return False
        return True
    except (KeyError, ValueError, TypeError, IndexError, StopIteration):
        return False
