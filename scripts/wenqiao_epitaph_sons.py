"""Bind the two named sons to the father in the continuous M9 inscription passage."""
from hashlib import sha256
import re


def validate(chapter, records, binding):
    selected = [p for p in chapter['paragraphs'] if p['id'] == binding['paragraph_id']]
    p, = selected
    text = p['text']
    assert binding['source_id'] == chapter['source_id']
    assert binding['paragraph_sha256'] == sha256(text.encode()).hexdigest()
    assert chapter['source']['transcription_witness']['kind'] == 'rubbing_reproduction_excerpts'
    match = re.fullmatch(r'使持節侍中大將軍始安忠武公并州太原祁縣都鄉仁義里(溫嶠)字泰真年卌二夫人高平李氏夫人琅耶王氏夫人廬江何氏息(放之)字弘祖息(式之)字穆祖', text)
    assert match
    names = [next(m for m in p['mentions'] if m['kind'] == 'person' and (m['start'], m['end']) == match.span(i)) for i in (1, 2, 3)]
    assert len({m['person_id'] for m in names}) == 3
    assertions = [a for record in records if record['record_type'] == 'person_assertion_set' for a in record['assertions']]
    assert len(assertions) == 2 and len(records) == 1
    father, *children = names
    for child in children:
        a, = [a for a in assertions if a['subject_person_id'] == child['person_id']]
        assert a['predicate'] == 'father' and a['object_person_id'] == father['person_id']
        assert a['status'] == 'source_attested' and a['human_reviewed'] is False
        assert a['qualifiers'] == {'source_term': '息' + child['surface']}
        e, = a['evidence']
        assert e['paragraph_id'] == p['id'] and e['chapter_id'] == chapter['id'] and e['source_id'] == chapter['source_id']
        assert e['quote'] == text and e['object_person_mention_id'] == father['id'] and e['subject_person_mention_id'] == child['id']
