# coding: utf-8
"""Validate an editorial parent edge between two explicitly consecutive paternal ancestors."""

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
    near = assertions.get(c.get('nearer_ancestor_assertion_id'))
    far = assertions.get(c.get('farther_ancestor_assertion_id'))
    witness = rows.get(c.get('chain_subject_person_id'))
    parent = rows.get(member.get('parent_person_id'))
    if (not near or not far or not witness or not parent
            or near.get('status') != 'source_attested' or far.get('status') != 'source_attested'):
        return False
    distance = {'father': 1, 'grandfather': 2, 'great_grandfather': 3}
    n, f = distance.get(near.get('predicate')), distance.get(far.get('predicate'))
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
