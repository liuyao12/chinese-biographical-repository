"""Fixed source bindings for two explicit Xie-clan kinship clauses in Songshu."""

V58 = 'c-songshu-058-xiehongwei'
P58 = V58 + ':p003'
V67 = 'c-songshu-067-xielingyun'
P67 = V67 + ':p001'
KINSHIP = {
    'lineage': 'paternal',
    'generation_difference': -1,
    'collateral': True,
    'distance': None,
    'common_ancestor_person_id': None,
    'subject_relative_age': 'unknown',
}
GROUP = '族子靈運瞻曜𢎞微'
GROUP_MEMBERS = {
    'a-song058-xiehun-lingyun-zuzi': ('aa6_83c_juy_CDAA', P58 + ':m0013'),
    'a-song058-xiehun-zhan-zuzi': ('aa6_83c_juy_AAAD', P58 + ':m0015'),
    'a-song058-xiehun-yao-zuzi': ('aa6_83c_juy_DBAA', P58 + ':m0016'),
    'a-song058-xiehun-hongwei-zuzi': ('aa6_83c_juy_DBAB', P58 + ':m0017'),
}
HUN58 = 'aa6_83c_juy_BAC'
LINGYUN = 'aa6_83c_juy_CDAA'
HUN67 = 'aa6_83c_juy_BAC'


def _person(mentions, mention_id, person_id):
    mention = mentions.get(mention_id)
    return (mention if mention and mention.get('kind') == 'person'
            and mention.get('person_id') == person_id else None)


def _quote_contains(text, quote, start, end):
    return (isinstance(quote, str) and bool(quote)
            and any(text.startswith(quote, i) and i <= start and end <= i + len(quote)
                    for i in range(len(text) + 1)))


def valid(assertion, paragraphs):
    """Accept only the exact vol. 58 collective 族子 list or vol. 67 從叔 clause."""
    q = assertion.get('qualifiers', {})
    binding = q.get('source_clause_binding', {})
    if (assertion.get('predicate') != 'agnatic_senior_kin'
            or assertion.get('status') != 'source_attested'
            or q.get('kinship_structure') != KINSHIP
            or set(q) != {'source_term', 'kinship_structure', 'source_clause_binding'}
            or not isinstance(binding, dict)):
        return False

    if binding.get('kind') == 'song058_xiehun_collective_zuzi':
        person = GROUP_MEMBERS.get(assertion.get('id'))
        subject_id, subject_mid = person if person else (None, None)
        hit = paragraphs.get(P58)
        if not hit:
            return False
        chapter, paragraph = hit
        text = paragraph.get('text', '')
        mentions = {m.get('id'): m for m in paragraph.get('mentions', [])}
        subject = _person(mentions, subject_mid, subject_id)
        obj = _person(mentions, P58 + ':m0000', HUN58)
        ev = assertion.get('evidence', [])
        if (chapter != V58 or paragraph.get('id') != P58
                or assertion.get('subject_person_id') != subject_id
                or assertion.get('object_person_id') != HUN58
                or q.get('source_term') != '族子'
                or set(binding) != {'kind', 'start', 'end', 'surface'}
                or (binding.get('start'), binding.get('end'), binding.get('surface')) != (11, 19, GROUP)
                or not subject or not obj or not ev
                or (subject['start'], subject['end']) not in ((13, 15), (15, 16), (16, 17), (17, 19))
                or text[subject['start']:subject['end']] != subject['surface']
                or (obj['start'], obj['end'], obj['surface']) != (0, 1, '混')
                or text[11:19] != GROUP or text[:subject['start']].find('混') < 0
                or not any(m.get('id') == subject_mid for m in paragraph.get('mentions', []))):
            return False
        for evidence in ev:
            if (evidence.get('work_id') != 'w-songshu'
                    or evidence.get('book_id') != 'b-songshu-058'
                    or evidence.get('source_id') != 's-songshu-058-xiehongwei'
                    or evidence.get('chapter_id') != V58
                    or evidence.get('paragraph_id') != P58
                    or evidence.get('subject_person_mention_id') != subject_mid
                    or evidence.get('object_person_mention_id') != P58 + ':m0000'
                    or evidence.get('relationship_anchor') != {
                        'paragraph_id': P58, 'start': 11, 'end': 19, 'surface': GROUP}
                    or not _quote_contains(text, evidence.get('quote'), subject['start'], obj['end'])):
                return False
        return True

    if binding.get('kind') == 'song067_lingyun_congshu':
        hit = paragraphs.get(P67)
        if not hit:
            return False
        chapter, paragraph = hit
        text = paragraph.get('text', '')
        mentions = {m.get('id'): m for m in paragraph.get('mentions', [])}
        subject = _person(mentions, P67 + ':m00000', LINGYUN)
        obj = _person(mentions, P67 + ':m00071', HUN67)
        ev = assertion.get('evidence', [])
        if (chapter != V67 or paragraph.get('id') != P67
                or assertion.get('id') != 'a-song067-lingyun-congshu-hun'
                or assertion.get('subject_person_id') != LINGYUN
                or assertion.get('object_person_id') != HUN67
                or q.get('source_term') != '從叔混'
                or set(binding) != {'kind', 'start', 'end', 'surface'}
                or (binding.get('start'), binding.get('end'), binding.get('surface')) != (69, 72, '從叔混')
                or not subject or not obj or not ev or text[69:72] != '從叔混'
                or (subject.get('start'), subject.get('end'), subject.get('surface')) != (0, 3, '謝靈運')
                or (obj.get('start'), obj.get('end'), obj.get('surface')) != (71, 72, '混')
                or text[subject['start']:subject['end']] != subject['surface']
                or text[obj['start']:obj['end']] != obj['surface']):
            return False
        for evidence in ev:
            if (evidence.get('work_id') != 'w-songshu'
                    or evidence.get('book_id') != 'b-songshu-067'
                    or evidence.get('source_id') != 's-songshu-067-xielingyun'
                    or evidence.get('chapter_id') != V67
                    or evidence.get('paragraph_id') != P67
                    or evidence.get('subject_person_mention_id') != subject['id']
                    or evidence.get('object_person_mention_id') != obj['id']
                    or evidence.get('relationship_anchor') != {
                        'paragraph_id': P67, 'start': 69, 'end': 72, 'surface': '從叔混'}
                    or not _quote_contains(text, evidence.get('quote'), subject['start'], 76)):
                return False
        return True
    return False
