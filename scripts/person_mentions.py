"""Distinguish a resolved person reference from a proper-name occurrence.

Pronouns retain their existing referent and evidence anchor, but must never be
used as a personal name or as the reader's interactive name markup.
"""


def _source_first_person(mention, text=None):
    try:
        from scripts.fixed_jin035_contemporary import source_first_person
    except ImportError:
        from fixed_jin035_contemporary import source_first_person
    return source_first_person(mention, text)


def is_person_reference(mention):
    if not isinstance(mention, dict):
        return False
    pid = mention.get('person_id')
    return (isinstance(pid, str) and bool(pid)
            and (mention.get('kind') == 'person'
                 or (mention.get('kind') == 'pronoun' and (mention.get('surface') == '之' or _source_first_person(mention)))))


def pronoun_errors(mention, text, person_ids=None):
    start, end = mention.get('start'), mention.get('end')
    valid = (mention.get('kind') == 'pronoun' and is_person_reference(mention)
             and mention.get('work_id') is None
             and type(start) is int and type(end) is int
             and 0 <= start < end <= len(text) and text[start:end] == mention.get('surface')
             and (mention.get('surface') == '之' or _source_first_person(mention, text))
             and mention.get('status') in (None, 'source_explicit', 'source_attested',
                                          'contextual_provisional', 'resolved_contextual')
             and (person_ids is None or mention.get('person_id') in person_ids))
    return [] if valid else ['代詞共指須保留原字位與已登記人物指涉，不得當姓名或著作']


def identity_surfaces_supported(decision, person, paragraphs, chapters, allowed_chapters=None):
    """Keep scoped source reference forms separate from personal name aliases."""
    supported = {alias['surface'] for alias in person.get('aliases', [])}
    requested = set(decision.get('surfaces', []))
    if requested.issubset(supported):
        return True
    if person.get('id') != decision.get('person_id'):
        return False
    evidence = decision.get('evidence', [])
    allowed = set(allowed_chapters if allowed_chapters is not None else
                  decision.get('chapter_ids', [e.get('chapter_id') for e in evidence]))
    # A pronoun extension cannot excuse corrupt provenance on the decision.
    for reference in evidence:
        hit = paragraphs.get(reference.get('paragraph_id'))
        if not hit:
            return False
        cid, paragraph = hit
        quote = reference.get('quote')
        source_id = chapters.get(cid, {}).get('source_id')
        # Legacy evidence carries a stable paragraph locator without repeated
        # source/chapter fields; resolve those through the validated chapter.
        if (cid not in allowed or not source_id
                or reference.get('chapter_id', cid) != cid
                or reference.get('source_id', source_id) != source_id
                or any(key in reference and reference[key] != chapters[cid].get(key)
                       for key in ('work_id', 'book_id'))
                or not isinstance(quote, str) or not quote or quote not in paragraph['text']):
            return False
    # Existing decisions list chapter-wide forms, with representative quotations.
    # Every additional pronoun form must still have its own reciprocal registry
    # evidence and exact current anchor within that declared chapter scope.
    for reference in person.get('evidence', []):
        hit = paragraphs.get(reference.get('paragraph_id'))
        if not hit:
            continue
        cid, paragraph = hit
        if (cid not in allowed or reference.get('chapter_id') != cid
                or any(key in reference and reference[key] != chapters.get(cid, {}).get(key)
                       for key in ('source_id', 'work_id', 'book_id'))):
            continue
        mention = next((m for m in paragraph['mentions']
                        if m['id'] == reference.get('mention_id')), None)
        if (mention and mention.get('kind') == 'pronoun'
                and mention.get('person_id') == decision.get('person_id')
                and mention.get('surface') == reference.get('quote')
                and not pronoun_errors(mention, paragraph['text'])):
            supported.add(mention['surface'])
    return requested.issubset(supported)
