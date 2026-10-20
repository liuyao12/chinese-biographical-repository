# coding: utf-8
"""Validate an editorial parent edge between two explicitly consecutive paternal ancestors."""

def explicit_four_ancestor_sequence_valid(near, far, assertions, chapters):
    """Only a full same-subject 髙祖/曾祖/祖/父 named sequence adds distance4."""
    if (near.get('predicate') != 'great_grandfather' or far.get('predicate') != 'ancestor'
            or far.get('qualifiers', {}).get('generation_distance') != 4
            or near.get('subject_person_id') != far.get('subject_person_id')):
        return False
    subject = far.get('subject_person_id')
    candidates = [[a for a in assertions.values() if a.get('predicate') == kind
                   and a.get('subject_person_id') == subject
                   and a.get('status') == 'source_attested'
                   and a.get('qualifiers', {}).get('lineage') == 'paternal']
                  for kind in ('grandfather', 'father')]
    shared = {(e.get('chapter_id'), e.get('paragraph_id'), e.get('source_id'), e.get('quote'))
              for e in near.get('evidence', [])} & {
              (e.get('chapter_id'), e.get('paragraph_id'), e.get('source_id'), e.get('quote'))
              for e in far.get('evidence', [])}
    for cid, paraid, sid, quote in shared:
        ch = chapters.get(cid, {})
        p = next((p for p in ch.get('paragraphs', []) if p['id'] == paraid), None)
        if (not p or p.get('text_layer') != 'received_chapter' or p.get('text') != quote
                or ch.get('source_id') != sid
                or not any(m.get('kind') == 'person' and m.get('person_id') == subject
                           and m.get('start') == 0 for m in p.get('mentions', []))):
            continue
        for grand in candidates[0]:
            for father in candidates[1]:
                chain = [far, near, grand, father]
                if len({subject} | {a.get('object_person_id') for a in chain}) != 5:
                    continue
                if not all(any((e.get('chapter_id'),e.get('paragraph_id'),e.get('source_id'),e.get('quote'))
                               == (cid,paraid,sid,quote) for e in a.get('evidence', [])) for a in chain):
                    continue
                bound = []; previous = -1
                for a, roles in zip(chain, [('髙祖', '高祖'), ('曾祖',), ('祖',), ('父',)]):
                    options = []
                    for m in p.get('mentions', []):
                        if (m.get('kind') != 'person' or m.get('person_id') != a.get('object_person_id')
                                or m.get('surface') in ('其','我','吾','臣','父','祖','曾祖','髙祖','高祖')
                                or quote[m.get('start',0):m.get('end',0)] != m.get('surface')):
                            continue
                        for role in roles:
                            start = m['start'] - len(role)
                            term = role + m['surface']
                            if (start >= previous and quote[start:m['start']] == role
                                    and a.get('qualifiers', {}).get('source_term','').startswith(term)):
                                options.append((start, m['end']))
                    if not options:
                        break
                    chosen = min(options);bound.append(chosen);previous = chosen[1]
                if len(bound) != 4:
                    continue
                # A different named person or quoted transfer inside the four
                # explicit role clauses invalidates a single genealogical list.
                segment = quote[bound[0][0]:bound[-1][1]]
                ancestors = {a['object_person_id'] for a in chain}
                if (any(c in segment for c in '曰「」『』。；！？')
                        or any(term in segment for term in ('非','未','不','或云','一云','又云'))):
                    continue
                if any(m.get('kind') == 'person' and m.get('person_id') not in ancestors
                       and bound[0][0] <= m.get('start',-1) < bound[-1][1]
                       for m in p.get('mentions', [])):
                    continue
                return True
    return False


def consecutive_ancestor_parent_valid(member, rows, assertions, chapters):
    c = member.get('parent_connection')
    if not isinstance(c, dict):
        return False
    if (c.get('type') != 'parent_between_consecutive_ancestors'
            or c.get('status') != 'contextual_provisional'
            or c.get('human_reviewed') is not False
            or not isinstance(c.get('rationale'), str) or not c['rationale'].strip()
            or member.get('source_assertion_id') is not None):
        return False
    if c.get('interpretation_basis') == 'biographical_zu_fu_sequence':
        try:
            from .biographical_ancestry import biographical_zu_fu_parent_valid
        except ImportError:
            from biographical_ancestry import biographical_zu_fu_parent_valid
        return biographical_zu_fu_parent_valid(member, rows, assertions, chapters)
    near = assertions.get(c.get('nearer_ancestor_assertion_id'))
    far = assertions.get(c.get('farther_ancestor_assertion_id'))
    witness = rows.get(c.get('chain_subject_person_id'))
    parent = rows.get(member.get('parent_person_id'))
    if (not near or not far or not witness or not parent
            or near.get('status') != 'source_attested' or far.get('status') != 'source_attested'):
        return False
    distance = {'father': 1, 'grandfather': 2, 'great_grandfather': 3}
    n, f = distance.get(near.get('predicate')), distance.get(far.get('predicate'))
    if n == 3 and explicit_four_ancestor_sequence_valid(near, far, assertions, chapters):
        f = 4
    if (n is None or f != n + 1
            or near.get('subject_person_id') != far.get('subject_person_id')
            or near.get('subject_person_id') not in witness['source_person_ids']
            or near.get('object_person_id') not in member['source_person_ids']
            or far.get('object_person_id') not in parent['source_person_ids']
            or near.get('qualifiers', {}).get('lineage') != 'paternal'
            or far.get('qualifiers', {}).get('lineage') != 'paternal'
            or len({near['subject_person_id'], near['object_person_id'], far['object_person_id']}) != 3):
        return False
    # The two distances must be asserted in the same received passage, not joined
    # across competing source accounts or an unspecified maternal grandparent.
    near_e = {(e.get('chapter_id'), e.get('paragraph_id'), e.get('source_id'), e.get('quote')) for e in near.get('evidence', [])}
    far_e = {(e.get('chapter_id'), e.get('paragraph_id'), e.get('source_id'), e.get('quote')) for e in far.get('evidence', [])}
    shared = near_e & far_e
    if not shared:
        return False
    for a in assertions.values():
        if (a.get('predicate') == 'father' and a.get('subject_person_id') in member['source_person_ids']
                and a.get('object_person_id') not in parent['source_person_ids']):
            return False
    refs = c.get('references')
    if (not isinstance(refs, list) or len(refs) != 2
            or any(not isinstance(ref, dict) for ref in refs)
            or {ref.get('assertion_id') for ref in refs} != {near['id'], far['id']}):
        return False
    for ref in refs:
        key = tuple(ref.get(k) for k in ('chapter_id', 'paragraph_id', 'source_id', 'quote'))
        chapter = chapters.get(ref.get('chapter_id'), {})
        para = next((p for p in chapter.get('paragraphs', []) if p['id'] == ref.get('paragraph_id')), None)
        if (key not in shared or not ref.get('scope') or not para
                or para.get('text_layer') != 'received_chapter'
                or ref.get('quote') != para.get('text')
                or not {near['subject_person_id'], near['object_person_id'], far['object_person_id']}.issubset(
                    {m.get('person_id') for m in para.get('mentions', []) if m.get('kind') == 'person'})
                or ref.get('source_id') != chapter.get('source_id')
                or ref.get('url') not in [chapter.get('source', {}).get('url'), chapter.get('source', {}).get('permalink')]):
            return False
    return True
