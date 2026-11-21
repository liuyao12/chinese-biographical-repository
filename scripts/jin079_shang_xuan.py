# coding: utf-8
"""以固定修訂卷七十九原句及同句兩個具名端點查驗承嗣、舅甥、叔侄。"""

CHAPTER = 'c-jinshu-079-xielang-family'
HEIRS = {
    'shang': ('exp-xieshang-p001', 0, '謝尚', '襲父爵咸亭侯', '襲父爵', 'exp-xieshang-p001', 11, '鯤'),
    'kang': ('exp-xieshang-p007', 8, '康', '從弟奕以子康襲爵', '襲爵', 'exp-xieshang-p001', 0, '謝尚'),
    'su': ('exp-xieshang-p007', 21, '肅', '康弟靜復以子肅嗣', '嗣', 'exp-xieshang-p007', 15, '康'),
    'huan': ('exp-xiexuan-p013', 1, '瑍', '子瑍嗣', '嗣', 'exp-xiexuan-p013', 29, '玄'),
    'lingyun': ('exp-xiexuan-p013', 12, '靈運', '子靈運嗣', '嗣', 'exp-xiexuan-p013', 1, '瑍'),
}
KIN = {
    '尚之甥': ('exp-xieshang-p004', 'maternal_uncle', 66, '康獻皇后', 74, '尚', '時康獻皇后臨朝，即尚之甥也'),
    '繼鯤後': ('exp-xieshang-p007', 'ritual_successor_of', 33, '靈佑', 36, '鯤', '靜子虔以子靈佑繼鯤後。'),
    '兄子玩': ('exp-xiexuan-p005', 'paternal_uncle', 359, '玩', 348, '玄', '玄請以先封東興侯賜兄子玩，詔聽之，更封玩豫甯伯'),
    '叔父征虜將軍石': ('exp-xiexuan-p004', 'paternal_uncle', 67, '玄', 100, '石', '詔以玄為前鋒、都督徐兗青三州揚州之晉陵幽州之燕國諸軍事，與叔父征虜將軍石'),
}


def _paragraph(paragraphs, suffix):
    cid, p = paragraphs[CHAPTER + ':' + suffix]
    if (cid != CHAPTER or p['id'] != CHAPTER + ':' + suffix
            or p['text_layer'] != 'received_chapter' or p['source_position']['revision_id'] != 2645985):
        raise ValueError('原文篇、卷或修訂不合')
    return p


def _name(p, start, word):
    end = start + len(word)
    if p['text'][start:end] != word:
        raise ValueError('字位不合')
    m, = [m for m in p['mentions'] if m['kind'] == 'person' and m['start'] == start
          and m['end'] == end and m['surface'] == word]
    return m


def _source(row, p):
    ref, = row['evidence']
    if (row['status'] != 'source_attested' or row['human_reviewed'] is not False or ref['quote'] != p['text']
            or ref['chapter_id'] != CHAPTER or ref['paragraph_id'] != p['id'] or ref['book_id'] != 'b-jinshu-079'
            or ref['work_id'] != 'w-jinshu' or ref['source_id'] != 's-jinshu-079-xielang-family'):
        raise ValueError('來源不合')
    return ref


def succession_valid(row, paragraphs):
    try:
        binding = row['source_clause_binding']
        role = binding['role']
        para, offset, word, clause, term, prior_para, prior_offset, prior_name = HEIRS[role]
        p = _paragraph(paragraphs, para)
        subject = _name(p, offset, word)
        prior = _name(_paragraph(paragraphs, prior_para), prior_offset, prior_name)
        evidence = _source(row, p)
        return (binding == {'kind': 'jin079_shang_xuan_heirs', 'role': role, 'clause': clause}
                and p['text'].count(clause) == 1 and row['event_type'] == 'noble_title_succession'
                and row['mode'] == 'accession' and row['source_term'] == term
                and row['person_id'] == subject['person_id'] and evidence['person_mention_id'] == subject['id']
                and row['predecessor_person_id'] == prior['person_id'] and prior['person_id'] != subject['person_id']
                and all(row[k] is None for k in ('date_expression', 'title', 'holding_id'))
                and 'normalized_date' not in row and 'normalized_date_range' not in row)
    except (KeyError, TypeError, ValueError):
        return False


def kin_valid(row, paragraphs):
    try:
        q = row['qualifiers']
        term = q['source_term']
        para, predicate, offset, word, relative_offset, relative_name, clause = KIN[term]
        p = _paragraph(paragraphs, para)
        relative = _name(p, relative_offset, relative_name)
        subject = _name(p, offset, word)
        evidence = _source(row, p)
        kinds = {
            'maternal_uncle': {'lineage': 'maternal', 'generation_difference': -1, 'mother_person_id': None},
            'paternal_uncle': {'lineage': 'paternal'},
            'ritual_successor_of': {'succession_kind': 'ji_named_predecessor_hou', 'legal_adoption_status': 'not_stated',
                                    'parentage_inference': 'not_inferred'},
        }
        return (q == {'source_term': term, **kinds[predicate]} and row['predicate'] == predicate
                and row['subject_person_id'] == subject['person_id'] and row['object_person_id'] == relative['person_id']
                and subject['person_id'] != relative['person_id'] and evidence['subject_person_mention_id'] == subject['id']
                and evidence['object_person_mention_id'] == relative['id'] and p['text'].count(clause) == 1)
    except (KeyError, TypeError, ValueError):
        return False
