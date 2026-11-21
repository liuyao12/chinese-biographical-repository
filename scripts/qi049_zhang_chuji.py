"""南齊書四十九「沖出繼從伯侍中景胤」與同卷首句「父柬」分層。"""
def valid(a, paragraphs, assertions):
    try:
        e, = a['evidence']
        chapter, p = paragraphs[e['paragraph_id']]
        q = a['qualifiers']
        if chapter != 'c-nanqishu-049-zhangjingyin' or chapter != e['chapter_id'] or p['source_position']['revision_id'] != 2261984:
            return False
        phrase = '沖出繼從伯侍中景胤'
        if (a['predicate'] != 'adoptive_father' or a['status'] != 'source_attested'
                or q['source_term'] != phrase[1:] or q['modern_legal_status'] != 'not_inferred'
                or e['quote'] != p['text'] or not p['text'].startswith(phrase + '，')):
            return False
        def endpoint(rec, para, ev, side):
            m, = (m for m in para['mentions'] if m['id'] == ev[side + '_person_mention_id'])
            assert m['kind'] == 'person' and m['person_id'] == rec[side + '_person_id']
            assert para['text'][m['start']:m['end']] == m['surface']
            return m
        ch = endpoint(a, p, e, 'subject')
        ad = endpoint(a, p, e, 'object')
        if q['biological_father_assertion_id'] != 'a-qi049-zhangchong-jian':
            return False
        source_id = 'c-nanqishu-049-zhangchong-birth-father'
        base, fp = paragraphs[source_id + ':p001']
        fc, = (m for m in fp['mentions'] if m['kind'] == 'person' and m['surface'] == '張沖')
        fm, = (m for m in fp['mentions'] if m['kind'] == 'person' and m['surface'] == '柬')
        return (ch['start'] == 0 and ch['surface'] == '沖' and ad['start'] == phrase.index('景胤') and ad['surface'] == '景胤'
                and base == source_id and fp['source_position']['revision_id'] == 2261984
                and fp['text'] == '張沖字思約，吳郡吳人。父柬，通直郎。'
                and fc['start'] == 0 and fc['surface'] == '張沖' and fm['surface'] == '柬' and fm['start'] == fp['text'].index('父柬')+1
                and fm['person_id'] == 'd50_8f5_wul_AAACB' and fc['person_id'] == ch['person_id']
                and len({ch['person_id'], ad['person_id'], fm['person_id']}) == 3)
    except (KeyError, ValueError, TypeError, AssertionError):
        return False
