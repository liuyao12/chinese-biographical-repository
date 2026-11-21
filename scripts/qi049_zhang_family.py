"""Bind the source spelling and role endpoints of Zhang Chong's maternal and collateral family."""
def valid(a, e, chapter):
    cases = {
        ('c-nanshi-032-dai-mother-zhangchong', 'mother'): (1494939, '沖母戴顒女，有儀范，張氏內取則焉。', '沖母戴顒女', ('沖', False, 'd50_8f5_wul_AAACBB'), ('母', True, 'odl_r9a_hli_A')),
        ('c-nanshi-032-dai-mother-zhangchong', 'father'): (1494939, '沖母戴顒女，有儀范，張氏內取則焉。', '戴顒女', ('女', True, 'odl_r9a_hli_A'), ('戴顒', False, 'odl_r9a_hli')),
        ('c-nanqishu-040-ziming-zhangchong', 'father'): (2272748, '西陽王子明字雲光，世祖第十子也。', '世祖第十子也', ('子明', False, 'kix_r92_2ed_H'), ('世祖', True, 'kix_r92_2ed')),
        ('c-songshu-080-zan-zhangchong', 'father'): (2261200, '武陵王贊字仲敷，明帝第九子也。', '明帝第九子也', ('贊', False, 'cti_o52_4nz_E'), ('明帝', True, 'cti_o52_4nz')),
    }
    try:
        rev, text, term, sub, obj = cases[(chapter['id'], a['predicate'])]
        p, = chapter['paragraphs']
        if not (p['id'] == e['paragraph_id'] and p['text'] == e['quote'] == text and a['status'] == 'source_attested'
                and rev == chapter['source']['revision_id'] and a['qualifiers']['source_term'] == term):
            return False
        for side, (surface, ref, person) in [('subject', sub), ('object', obj)]:
            field = '_person_reference_id' if ref else '_person_mention_id'
            pool = chapter['annotation']['person_reference_occurrences'] if ref else p['mentions']
            m, = (m for m in pool if m['id'] == e[side+field])
            if (m['surface'] != surface or m['person_id'] != person or a[side+'_person_id'] != person
                    or m['start'] != text.index(surface) or m['end'] != m['start']+len(surface)
                    or (ref and m['paragraph_id'] != p['id']) or (not ref and m['kind'] != 'person')):
                return False
        return True
    except (KeyError, ValueError, TypeError, IndexError):
        return False


def senior_valid(a, paragraphs):
    try:
        q = a['qualifiers']
        e, = a['evidence']
        cid,p = paragraphs[e['paragraph_id']]
        prefix = '沖亦少有至性，辟州主簿，隨從叔永爲將帥'
        s, = (m for m in p['mentions'] if m['id'] == e['subject_person_mention_id'])
        o, = (m for m in p['mentions'] if m['id'] == e['object_person_mention_id'])
        return (cid == e['chapter_id'] == 'c-nanqishu-049-zhangchong' and p['source_position']['revision_id'] == 2261984
                and p['text'] == e['quote'] and p['text'].startswith(prefix) and a['predicate'] == 'agnatic_senior_kin'
                and q['source_term'] == '從叔' and s['kind'] == o['kind'] == 'person' and s['start'] == 0 and s['end'] == 1 and s['surface'] == '沖'
                and o['start'] == prefix.index('永') and o['end'] == o['start']+1 and o['surface'] == '永'
                and s['person_id'] == a['subject_person_id'] == 'd50_8f5_wul_AAACBB'
                and o['person_id'] == a['object_person_id'] == 'd50_8f5_wul_AAAAE'
                and q['kinship_structure'] == dict(lineage='paternal', generation_difference=-1, collateral=True,
                                                    distance=None, common_ancestor_person_id=None, subject_relative_age='unknown'))
    except (KeyError, ValueError, TypeError, IndexError):
        return False
