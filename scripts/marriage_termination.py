# coding: utf-8
"""Preserve a marriage that the same source explicitly says ended in divorce."""


def marriage_termination_valid(a, paragraphs):
    q = a.get('qualifiers', {})
    termination = q.get('marriage_termination', {})
    if (a.get('predicate') != 'spouse' or a.get('status') != 'source_attested'
            or termination != {'kind': 'divorce', 'source_term': '遂離婚', 'date': None}
            or len(a.get('evidence', [])) != 1):
        return False
    e = a['evidence'][0]
    hit = paragraphs.get(e.get('paragraph_id'))
    if not hit or hit[0] != e.get('chapter_id') or e.get('quote') != hit[1]['text']:
        return False
    p = hit[1]
    ms = {m['id']: m for m in p['mentions']}
    child = ms.get(e.get('subject_person_mention_id'), {})
    spouse = ms.get(e.get('object_person_mention_id'), {})
    term = q.get('source_term')
    if (child.get('person_id') != a.get('subject_person_id')
            or spouse.get('person_id') != a.get('object_person_id')
            or any(m.get('kind') != 'person' for m in [child, spouse])
            or child['person_id'] == spouse['person_id']
            or not isinstance(term, str) or not term.startswith('尚')
            or not term.endswith(spouse.get('surface', ''))):
        return False
    starts = [i for i in range(len(p['text'])) if p['text'].startswith(term, i)]
    return any(child['end'] <= i < spouse['start']
               and spouse['end'] == i + len(term)
               and any('遂離婚' in sentence for sentence in
                       p['text'][spouse['end']:].split('。', 2)[:2])
               for i in starts)
