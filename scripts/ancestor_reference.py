# coding: utf-8
"""Resolve a speaker's 曾祖 from sourced parent edges, never from ID letters."""
try:
    from .ancestry_chain import consecutive_ancestor_parent_valid
except ImportError:
    from ancestry_chain import consecutive_ancestor_parent_valid


def ancestor_reference_valid(decision, chapters, assertions, assemblies):
    ref = decision.get('ancestor_reference', {})
    if (ref.get('kind') != 'speaker_paternal_great_grandfather'
            or ref.get('source_term') != '曾祖'
            or ref.get('generation_distance') != 3
            or decision.get('human_reviewed') is not False):
        return False
    chapter = chapters.get(ref.get('chapter_id'), {})
    p = next((p for p in chapter.get('paragraphs', [])
              if p['id'] == ref.get('paragraph_id')), None)
    if not p or ref.get('quote') != p['text']:
        return False
    ms = {m['id']: m for m in p['mentions']}
    speaker = ms.get(ref.get('speaker_mention_id'), {})
    named = ms.get(ref.get('speaker_name_mention_id'), {})
    ancestor = ms.get(ref.get('ancestor_mention_id'), {})
    speaker_id = ref.get('speaker_person_id')
    if (speaker.get('person_id') != speaker_id or named.get('person_id') != speaker_id
            or speaker.get('surface') != '下官'
            or any(m.get('kind') != 'person' for m in [speaker, named, ancestor])
            or p['text'][named['end']:speaker['start']] != '曰：「'
            or speaker['end'] != ancestor['start']
            or ancestor.get('surface') != '曾祖'
            or ancestor.get('person_id') != decision.get('person_id')
            or decision.get('identification_basis', {}).get('target_mention_ids') != [ancestor['id']]):
        return False
    path, steps = ref.get('person_path'), ref.get('steps')
    if (not isinstance(path, list) or len(path) != 4 or len(set(path)) != 4
            or path[0] != speaker_id or path[-1] != decision.get('person_id')
            or not isinstance(steps, list) or len(steps) != 3):
        return False
    for child, parent, step in zip(path, path[1:], steps):
        if step.get('kind') == 'source_assertion':
            a = assertions.get(step.get('assertion_id'), {})
            if (a.get('predicate') != 'father' or a.get('status') != 'source_attested'
                    or a.get('subject_person_id') != child or a.get('object_person_id') != parent
                    or a.get('qualifiers', {}).get('lineage') != 'paternal'):
                return False
        elif step.get('kind') == 'editorial_parent_between_consecutive_ancestors':
            f = next((f for f in assemblies if f['id'] == step.get('assembly_id')), {})
            rows = {m['person_id']: m for m in f.get('members', [])}
            member = rows.get(child, {})
            if (member.get('parent_person_id') != parent
                    or not consecutive_ancestor_parent_valid(member, rows, assertions, chapters)):
                return False
        else:
            return False
    return True
