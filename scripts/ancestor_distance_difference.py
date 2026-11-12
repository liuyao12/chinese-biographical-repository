"""Validate a narrowly derived family edge from two exact kinship distances."""


DISTANCE = {
    'father': 1,
    'grandfather': 2,
    'great_grandfather': 3,
}


def _source_frame(assertion):
    evidence = assertion.get('evidence', [])
    if len(evidence) != 1:
        return None
    item = evidence[0]
    return (item.get('work_id'), item.get('book_id'), item.get('chapter_id'),
            item.get('source_id'), item.get('paragraph_id'), item.get('quote'))


def _distance(assertion):
    predicate = assertion.get('predicate')
    if predicate == 'ancestor':
        return assertion.get('qualifiers', {}).get('generation_distance')
    return DISTANCE.get(predicate)


def _proofs_valid(connection, member, parent, rows, assertions, chapters):
    if (connection.get('status') != 'contextual_provisional'
            or connection.get('human_reviewed') is not False
            or not connection.get('rationale')):
        return False
    proof_ids = connection.get('assertion_ids')
    refs = connection.get('references')
    if (not isinstance(proof_ids, list) or len(proof_ids) != 2
            or len(set(proof_ids)) != 2 or not isinstance(refs, list)
            or len(refs) != 2 or {r.get('assertion_id') for r in refs} != set(proof_ids)):
        return False
    proofs = [assertions.get(aid) for aid in proof_ids]
    if any(not a or a.get('status') != 'source_attested' for a in proofs):
        return False
    frames = [_source_frame(a) for a in proofs]
    if not frames[0] or frames[0] != frames[1]:
        return False
    frame = frames[0]
    if frame[0] is None or frame[3] is None or frame[4] is None or frame[5] is None:
        return False
    if any(a.get('subject_person_id') != proofs[0].get('subject_person_id') for a in proofs):
        return False
    if proofs[0]['subject_person_id'] not in rows and all(
            proofs[0]['subject_person_id'] not in row.get('source_person_ids', [])
            for row in rows.values()):
        return False
    if any(a.get('qualifiers', {}).get('lineage') != 'paternal'
           or a.get('qualifiers', {}).get('adopted_for_family_tree') is False
           for a in proofs):
        return False
    distances = [_distance(a) for a in proofs]
    if any(type(d) is not int or d < 1 for d in distances) or distances[0] == distances[1]:
        return False
    longer_i = 0 if distances[0] > distances[1] else 1
    shorter_i = 1 - longer_i
    longer, shorter = proofs[longer_i], proofs[shorter_i]
    delta = distances[longer_i] - distances[shorter_i]
    if delta < 1:
        return False
    longer_target = longer.get('object_person_id')
    shorter_target = shorter.get('object_person_id')
    if longer_target not in rows.get(parent, {}).get('source_person_ids', []):
        return False
    if shorter_target not in member.get('source_person_ids', []):
        return False
    if member.get('source_assertion_id') is not None:
        return False
    chapter = chapters.get(frame[2], {})
    if chapter.get('source_id') != frame[3]:
        return False
    valid_refs = set()
    for ref in refs:
        if (not ref.get('scope') or ref.get('url') not in
                (chapter.get('source', {}).get('url'), chapter.get('source', {}).get('permalink'))):
            return False
        if (ref.get('quote'), ref.get('paragraph_id'), ref.get('chapter_id'), ref.get('source_id')) != (
                frame[5], frame[4], frame[2], frame[3]):
            return False
        valid_refs.add(ref['assertion_id'])
    return delta, shorter_i, longer_i


def ancestor_path_valid(member, rows, assertions, chapters):
    """One missing generation derived by subtracting same-descendant claims."""
    connection = member.get('ancestor_connection', {})
    ancestor = member.get('ancestor_person_id')
    if connection.get('type') != 'same_descendant_distance_difference' or ancestor not in rows:
        return False
    result = _proofs_valid(connection, member, ancestor, rows, assertions, chapters)
    if result is False:
        return False
    delta, _, _ = result
    if member.get('connection') != 'ancestor' or member.get('generation_distance') != delta:
        return False
    if member.get('parent_person_id') is not None:
        return False
    if member.get('intermediate_person_ids') != [None] * (delta - 1):
        return False
    # This narrow rule currently represents only a two-generation path with
    # exactly one unnamed intermediate person.
    return delta == 2


def parent_edge_valid(member, rows, assertions, chapters):
    """One inferred father edge from adjacent distances to a shared descendant."""
    connection = member.get('parent_connection', {})
    parent = member.get('parent_person_id')
    if connection.get('type') != 'same_descendant_distance_difference' or parent not in rows:
        return False
    result = _proofs_valid(connection, member, parent, rows, assertions, chapters)
    return result is not False and result[0] == 1
