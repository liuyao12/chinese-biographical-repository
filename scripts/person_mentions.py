"""Distinguish a resolved person reference from a proper-name occurrence.

Pronouns retain their existing referent and evidence anchor, but must never be
used as a personal name or as the reader's interactive name markup.
"""

# These seven source anchors are syntactically clear contextual pronouns that
# were previously misclassified as 王衍's personal alias. Keep this exception
# tied to their stable MID and local wording; this is not a general rule for 其.
APPROVED_QI_PRONOUNS = {
    'c-jinshu-043-wangyan:p001:m0156': ('kwx_czc_d4c_A', '陽狂自免。武帝聞其名，問戎曰：'),
    'c-jinshu-043-wangyan:p001:m0178': ('kwx_czc_d4c_A', '問戎曰：「夷甫當世誰比？」戎曰：「未見其比，'),
    'c-jinshu-043-wangyan:p002:m0069': ('kwx_czc_d4c_A', '為族人所怒，舉樏擲其面。衍初無言'),
    'c-jinshu-043-wangyan:p004:m0141': ('kwx_czc_d4c_A', '謂婢曰：「舉阿堵物卻！」其措意如此。'),
    'c-jinshu-043-wangyan:p009:m0063': ('kwx_czc_d4c_A', '壁立千仞。其為人所尚如此。'),
    'c-jinshu-077-yinhao:p003:m0242': ('kwx_czc_d4c_A', '王夷甫，先朝風流士也，然吾薄其立名非真，而始終'),
    'c-jinshu-077-yinhao:p003:m0323': ('kwx_czc_d4c_A', '高談《莊》《老》，說空終日，雖云談道，實長華競。及其末年，人望猶存，'),
}


def is_person_reference(mention):
    if not isinstance(mention, dict):
        return False
    pid = mention.get('person_id')
    return (isinstance(pid, str) and bool(pid)
            and (mention.get('kind') == 'person'
                 or (mention.get('kind') == 'pronoun'
                     and (mention.get('surface') == '之'
                          or (mention.get('surface') == '其'
                              and APPROVED_QI_PRONOUNS.get(mention.get('id'), (None,))[0]
                                  == mention.get('person_id'))))))


def pronoun_errors(mention, text, person_ids=None):
    start, end = mention.get('start'), mention.get('end')
    valid = (mention.get('kind') == 'pronoun' and is_person_reference(mention)
             and mention.get('work_id') is None
             and type(start) is int and type(end) is int
             and 0 <= start < end <= len(text)
             and (text[start:end] == '之'
                  or (mention.get('id') in APPROVED_QI_PRONOUNS
                      and mention.get('surface') == '其'
                      and APPROVED_QI_PRONOUNS[mention['id']][0] == mention.get('person_id')
                      and APPROVED_QI_PRONOUNS[mention['id']][1] in text
                      and text[start:end] == '其'))
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
