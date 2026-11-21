"""核《南史》卷二十二僧綽傳記的王妃、帝女及親屬指代。"""
from hashlib import sha256

CHAPTER = 'c-nanshi-022-wangsengchuo'
SOURCE = 's-nanshi-022-wangsengchuo-ws1477957'
FRAMES = {
    'princess-marriage': (18, '僧綽幼有大成之度', '僧綽', '尚文帝長女東陽獻公主', '東陽獻公主', 'spouse'),
    'princess-father': (18, '尚文帝長女東陽獻公主', '東陽獻公主', '尚文帝長女東陽獻公主', '文帝', 'father'),
    'sui-marriage': (22, '誕妃即湛之女', '妃', '誕妃即湛之女', '誕', 'spouse'),
    'sui-father': (22, '誕妃即湛之女', '女', '誕妃即湛之女', '湛之', 'father'),
    'nanping-marriage': (22, '鑠妃湛妹也', '妃', '鑠妃湛妹也', '鑠', 'spouse'),
    'nanping-sibling': (22, '鑠妃湛妹也', '妹', '鑠妃湛妹也', '湛', 'sister'),
}
ROLES = {
    '東陽獻公主': '3bh_k4m_fg4_A', '文帝': '3bh_k4m_fg4', '僧綽': '7r6_k52_qji_ABAAAAEA',
    '誕': '9d4_1cb_fb9', '湛之': 'spx_gk1_rrr', '鑠': 'ece_336_e4c', '湛': 'o1i_tao_gu1',
}
WIVES = {'誕': 'spx_gk1_rrr_A', '鑠': 'vwx_acg_r0a'}


def valid(a, chapter, root):
    try:
        from scripts.fixed_wikisource_units import source_errors
    except ImportError:
        from fixed_wikisource_units import source_errors
    try:
        q = a['qualifiers']
        key = q['royal_kin_frame']
        line, first, subject, second, obj, predicate = FRAMES[key]
        e, = a['evidence']
        print_witness = chapter['id'] == CHAPTER + '-wyd'
        if print_witness:
            try:
                from scripts.nanshi022_print import errors as print_errors
            except ImportError:
                from nanshi022_print import errors as print_errors
            if print_errors(chapter, root):
                return False
            first = first.replace('即', '卽')
            second = second.replace('即', '卽')
        elif (chapter['id'] != CHAPTER or chapter['source_id'] != SOURCE
                or chapter['source']['revision_id'] != 1477957 or source_errors(chapter, root)
                ):
            return False
        cid = CHAPTER + ('-wyd' if print_witness else '')
        srcid = 's-nanshi-022-wangsengchuo-wyd1739' if print_witness else SOURCE
        prefix = 'a-nanshi022-wyd-' if print_witness else 'a-nanshi022-'
        if (chapter['source_id'] != srcid or e['source_id'] != srcid or e['chapter_id'] != cid
                or e['work_id'] != 'w-nanshi' or e['book_id'] != 'b-nanshi-022'
                or a['predicate'] != predicate or a['id'] != prefix + key
                or a['status'] != 'source_attested'):
            return False
        p, = (r for r in chapter['paragraphs'] if r['id'] == e['paragraph_id'])
        if print_witness:
            if p['id'] != cid + (':p001' if line == 18 else ':p003'):
                return False
        elif (p['source_position']['first_line'] != line or p['source_position']['last_line'] != line
                or p['source_position']['revision_id'] != 1477957):
            return False
        if (e['quote'] != p['text'] or q['source_term'] not in (first, second)
                ):
            return False
        refs = [r for r in chapter['annotation']['person_reference_occurrences']
                if r['paragraph_id'] == p['id'] and r['referent_role'] == 'third_person']
        for role, phrase, word in [('subject', first, subject), ('object', second, obj)]:
            referential = word in ('東陽獻公主', '文帝', '妃', '妹', '女')
            if p['text'].count(phrase) != 1 or phrase.count(word) != 1:
                return False
            i = p['text'].index(phrase) + phrase.index(word)
            hit, = (z for z in (refs if referential else p['mentions']) if
                    z['start'] == i and z['end'] == i + len(word) and z['surface'] == word)
            pid = WIVES[phrase[0]] if word in ('妃', '妹', '女') else ROLES[word]
            if (hit['person_id'] != pid or a[role+'_person_id'] != pid
                    or e[role+('_person_reference_id' if referential else '_person_mention_id')] != hit['id']):
                return False
        return a['subject_person_id'] != a['object_person_id']
    except (KeyError, ValueError, TypeError, OSError):
        return False
