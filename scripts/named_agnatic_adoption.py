"""明名從叔無後為嗣，連續本傳另明出繼；不把嗣爵當收養。"""

import re


def named_agnatic_adoption_valid(a, paragraphs, assertions):
    q = a.get('qualifiers', {})
    es = a.get('evidence', [])
    if (a.get('predicate') != 'adoptive_father'
            or a.get('status') != 'source_attested'
            or q.get('adoption_basis') != 'named_agnatic_senior_no_heir_as_successor'
            or q.get('modern_legal_status') != 'not_inferred' or len(es) != 2):
        return False
    child_id, parent_id = a.get('subject_person_id'), a.get('object_person_id')
    if not child_id or not parent_id or child_id == parent_id:
        return False
    ps = []
    for e in es:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or hit[0] != e.get('chapter_id'):
            return False
        p = hit[1]
        if p.get('text_layer') != 'received_chapter' or e.get('quote') != p.get('text'):
            return False
        ms = {m['id']: m for m in p.get('mentions', [])}
        c = ms.get(e.get('subject_person_mention_id'), {})
        f = ms.get(e.get('object_person_mention_id'), {})
        if (c.get('kind') != 'person' or f.get('kind') != 'person'
                or c.get('person_id') != child_id or f.get('person_id') != parent_id):
            return False
        for m in (c, f):
            if p['text'][m.get('start', -1):m.get('end', -1)] != m.get('surface'):
                return False
        ps.append((p, ms, c, f))
    p, ms, c, f = ps[0]
    n, nms, nc, nf = ps[1]
    # Same fixed witness and consecutive received paragraphs; intervening narrative is not skipped.
    if any(es[0].get(k) != es[1].get(k) or not es[0].get(k)
           for k in ('work_id', 'book_id', 'chapter_id', 'source_id')):
        return False
    order = [pid for pid, hit in paragraphs.items() if hit[0] == es[0]['chapter_id']]
    if p['id'] not in order or order.index(p['id']) + 1 >= len(order) or order[order.index(p['id']) + 1] != n['id']:
        return False
    pos, nxt = p.get('source_position', {}), n.get('source_position', {})
    if (not pos.get('source_commit') or pos.get('source_commit') != nxt.get('source_commit')
            or not isinstance(pos.get('last_line'), int) or not isinstance(nxt.get('first_line'), int)
            or nxt['first_line'] not in (pos['last_line'], pos['last_line'] + 1)
            or p.get('received_authority') != n.get('received_authority')):
        return False
    # Explicit named relation and adoption clause, not a title succession clause.
    text = p['text']
    if text[max(0, f['start'] - 2):f['start']] != '從叔':
        return False
    if text[c['end']:c['end'] + 2] != '為嗣' or not text[:c['start']].endswith('無後以'):
        return False
    if f['end'] > c['start'] - 3 or q.get('source_term') != text[f['start'] - 2:c['end'] + 2]:
        return False
    # A named biography topic binds the later omitted subject; a different new topic cannot intervene.
    topic = next((m for m in ms.values() if m.get('start') == 0 and m.get('person_id') == child_id), None)
    if not topic or not text.startswith(topic['surface']):
        return False
    nt = n['text']; term = q.get('chuji_source_term')
    if any(m.get('start') == 0 and m.get('kind') == 'person'
           and m.get('person_id') != child_id for m in nms.values()):
        return False
    if not isinstance(term, str) or not re.fullmatch(r'年[一二三四五六七八九十百有]+[歲嵗]出繼', term) or term not in nt or nf.get('surface') != '所繼父':
        return False
    at = nt.index(term)
    if nf['start'] != at + len(term) or nt[nf['end']:nc['start']] != '於' or nt[nc['end']:nc['end'] + 3] != '本緦麻':
        return False
    # Source-attested biological father stays separate; its exact anchors must remain valid.
    b = next((r for r in assertions if r.get('id') == q.get('biological_father_assertion_id')), {})
    if (b.get('predicate') != 'father' or b.get('status') != 'source_attested'
            or b.get('subject_person_id') != child_id or b.get('object_person_id') in (None, child_id, parent_id)
            or len(b.get('evidence', [])) != 1):
        return False
    be = b['evidence'][0]; bm = ms.get(be.get('object_person_mention_id'), {})
    bc = ms.get(be.get('subject_person_mention_id'), {})
    return (all(be.get(k) == es[0].get(k) for k in ('work_id', 'book_id', 'chapter_id', 'source_id', 'paragraph_id', 'quote'))
            and bc.get('person_id') == child_id and bc.get('kind') == 'person'
            and bm.get('person_id') == b.get('object_person_id') and bm.get('kind') == 'person'
            and text[bm.get('start', 0) - 1:bm.get('start', 0)] == '父'
            and q.get('biological_father_preserved') is True)
