"""Validate a source-linked surname carried across named paternal assertions.

The seed is an explicit full name in one received chapter; every later
generation must be joined by a separate source-attested father assertion in
the target chapter. Structural person IDs are used only to locate those
assertions, never as evidence by themselves.
"""
import hashlib

KIND = 'contextual_surname_from_cross_chapter_paternal_path'
SEED_CHAPTER = 'c-shiji-008-gaozu'
SEED_SOURCE = 's-shiji-008-gaozu'
PATH_CHAPTER_SOURCES = {
    'c-shiji-010-wendi': 's-shiji-010-wendi',
    'c-shiji-118-huainan': 's-shiji118-huainan',
}
NAME_CHAPTER_SOURCES = {
    'c-shiji-009-lvhou': 's-shiji-009-lvhou',
    'c-shiji-118-huainan': 's-shiji118-huainan',
}


def validate(name, names, chapters, assertions, root=None):
    try:
        b = name['surname_basis']
        assert set(b) == {'kind', 'status', 'human_reviewed', 'rationale',
                          'source_name_record_id', 'source_frames', 'steps'}
        assert b['kind'] == KIND and b['status'] == 'contextual_provisional'
        assert b['human_reviewed'] is False and b['rationale'].strip()
        assert name['status'] == 'contextual_provisional' and name['human_reviewed'] is False

        seeds = [n for n in names if n.get('id') == b['source_name_record_id']]
        assert len(seeds) == 1
        seed = seeds[0]
        assert seed['chapter_id'] == SEED_CHAPTER and seed['surname'] == name['surname']
        assert seed['person_id'] == 'yqp_nlb_p1p_A' and seed['surname'] == '劉'
        assert seed['ming'] == '季' and not seed.get('surname_basis')

        def paragraph(chapter_id, paragraph_id):
            ch = chapters[chapter_id]
            ps = [p for p in ch['paragraphs'] if p['id'] == paragraph_id]
            assert len(ps) == 1
            p = ps[0]
            assert p.get('text_layer') == 'received_chapter'
            return ch, p

        def mark(ch, p, mention_id, person_id):
            ms = [m for m in p['mentions'] if m.get('id') == mention_id]
            assert len(ms) == 1
            m = ms[0]
            assert m.get('kind') == 'person' and m.get('person_id') == person_id
            assert type(m.get('start')) is int and type(m.get('end')) is int
            assert p['text'][m['start']:m['end']] == m['surface']
            return m

        seed_ch, seed_p = paragraph(seed['chapter_id'], seed['paragraph_id'])
        assert seed_ch['source_id'] == SEED_SOURCE and seed['quote'] == seed_p['text']
        assert seed_p['text'].startswith('單父人') and '劉季固多大言' in seed_p['text']
        seed_mark = mark(seed_ch, seed_p, seed['person_mention_id'], seed['person_id'])
        assert seed_mark['surface'] == '劉季'
        seed_frame = b['source_frames'][0]
        assert seed_frame == {
            'chapter_id': SEED_CHAPTER,
            'paragraph_id': seed_p['id'],
            'source_revision': seed_ch['source']['revision_id'],
            'paragraph_sha256': hashlib.sha256(seed_p['text'].encode()).hexdigest(),
        }

        target_ch, target_p = paragraph(name['chapter_id'], name['paragraph_id'])
        assert target_ch['id'] in NAME_CHAPTER_SOURCES
        assert target_ch['source_id'] == NAME_CHAPTER_SOURCES[target_ch['id']]
        assert name['quote'] == target_p['text']
        target = mark(target_ch, target_p, name['person_mention_id'], name['person_id'])
        assert target['surface'].endswith(name['ming'])
        assert name['ming'] and name['surname'] == '劉'

        assertions_by_id = {a['id']: a for a in assertions}
        assert len(assertions_by_id) == len(assertions)
        steps = b['steps']
        assert isinstance(steps, list) and 1 <= len(steps) <= 4
        current = seed['person_id']
        seen = {current}
        frames = [seed_frame]
        for step in steps:
            assert set(step) == {'assertion_id', 'from_person_id', 'to_person_id',
                                 'chapter_id', 'paragraph_id', 'source_term',
                                 'from_mention_id', 'to_mention_id'}
            assert step['from_person_id'] == current and step['to_person_id'] not in seen
            assert step['chapter_id'] in PATH_CHAPTER_SOURCES
            a = assertions_by_id[step['assertion_id']]
            assert a['predicate'] == 'father' and a['status'] == 'source_attested'
            assert a['subject_person_id'] == step['to_person_id']
            assert a['object_person_id'] == current
            q = a.get('qualifiers', {})
            assert q.get('lineage', 'paternal') == 'paternal'
            assert not q.get('adoptive') and not q.get('sworn')
            ev, = a['evidence']
            ch, p = paragraph(step['chapter_id'], step['paragraph_id'])
            assert ch['source_id'] == PATH_CHAPTER_SOURCES[ch['id']] and ev['chapter_id'] == ch['id']
            assert ev['source_id'] == ch['source_id'] and ev['paragraph_id'] == p['id']
            assert ev['quote'] in p['text']
            assert q.get('source_term') == step['source_term']
            assert step['source_term'] in ev['quote']
            assert ev.get('subject_person_mention_id') == step['to_mention_id']
            assert ev.get('object_person_mention_id') == step['from_mention_id']
            child = mark(ch, p, step['to_mention_id'], step['to_person_id'])
            parent = mark(ch, p, step['from_mention_id'], current)
            assert parent['surface'] in p['text'] and child['surface'] in p['text']
            frames.append({
                'chapter_id': ch['id'], 'paragraph_id': p['id'],
                'source_revision': ch['source']['revision_id'],
                'paragraph_sha256': hashlib.sha256(p['text'].encode()).hexdigest(),
            })
            current = step['to_person_id']
            seen.add(current)
        assert current == name['person_id']
        assert b['source_frames'] == frames
    except (AssertionError, KeyError, TypeError, ValueError, StopIteration,
            IndexError, AttributeError):
        raise ValueError('跨篇姓氏須由卷八明載劉姓全名出發，逐代沿卷一一八具名父子原文與來源錨點連接；不得以家族ID、族望或常識代替證據')
