"""Read Zhang Shao's specific sheng designation in the burial narrative."""
def valid(a, paragraphs):
    try:
        e, = a['evidence']
        ch, p = paragraphs[e['paragraph_id']]
        named = {m['id']: m for m in p['mentions'] if m['kind'] == 'person'}
        s, o = named[e['subject_person_mention_id']], named[e['object_person_mention_id']]
        q = a['qualifiers']
        text = p['text']
        clause = '劭，駿甥也'
        at = text.index(clause)
        return (ch == e['chapter_id'] == 'c-jinshu-044-shijian'
                and p['source_position']['revision_id'] == 1775345 and e['quote'] == text
                and text.count(clause) == 1 and q['source_term'] == clause
                and q['named_intermediate_parent'] is None and a['predicate'] == 'kinship_unspecified'
                and (s['start'], s['end'], s['surface'], s['person_id']) == (at, at+1, '劭', a['subject_person_id'])
                and (o['start'], o['end'], o['surface'], o['person_id']) == (at+2, at+3, '駿', a['object_person_id'])
                and any(x['surface']=='張劭' and x['person_id']==s['person_id'] for x in named.values())
                and any(x['surface']=='楊駿' and x['person_id']==o['person_id'] for x in named.values()))
    except (ValueError, TypeError, KeyError):
        return False
