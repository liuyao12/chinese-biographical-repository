"""Verify the declined appointments recorded in Liang 27 against their source clauses."""
try:
    from scripts.chenshu023_shenjunli import located, named
except ImportError:
    from chenshu023_shenjunli import located, named


QIA = 'c-liangshu-027-daoqia-complete'
QIA_REAPPOINTMENT = '五年，復爲太子中庶子，領步兵校尉，未拜，仍遷給事黃門侍郎'
READINGS = {
    ('c-liangshu-027-yinjun-complete', '五兵尚書'): (
        2, 'ceq_pnr_q0e_A', '鈞體羸多疾', '鈞',
        '服闋，遷五兵尚書，猶以頓瘵經時，不堪拜受，乃更授散騎常侍', '遷', '不堪拜受'),
    ('c-liangshu-027-mingshanbin-complete', '國子博士'): (
        0, 'nbb_y6s_bfz_AA', '父僧紹', '僧紹', '宋末國子博士徵，不就。', '徵', '不就'),
    (QIA, '晉安王國左常侍'): (1, '4mr_j4p_k5h', '洽年十八', '洽', '除晉安王國左常侍，不就。', '除', '不就'),
    (QIA, '太子中庶子'): (3, '4mr_j4p_k5h', '洽兄弟羣從', '洽', QIA_REAPPOINTMENT, '復爲', '未拜'),
    (QIA, '步兵校尉'): (3, '4mr_j4p_k5h', '洽兄弟羣從', '洽', QIA_REAPPOINTMENT, '領', '未拜'),
}


def valid(row, chapter):
    try:
        index, person, named_clause, name, clause, verb, result = READINGS[chapter['id'], row['title']]
        p = chapter['paragraphs'][index]
        e, = row['evidence']
        return (
            chapter['work_id'] == 'w-liangshu' and chapter['book_id'] == 'b-liangshu-027'
            and chapter['source_id'] == 's-' + chapter['id'][2:] + '-ws1511478'
            and chapter['source']['raw_file_sha256'] == 'fcb730ce00423c60dc63e01c4a6d43ecd45cf2669df595850e0abb2339acfb5f'
            and chapter['source']['revision_id'] == p['source_position']['revision_id'] == 1511478
            and all(e[k] == chapter[k] for k in ('work_id', 'book_id', 'source_id'))
            and e['chapter_id'] == chapter['id'] and e['paragraph_id'] == p['id'] and e['quote'] == p['text']
            and row['status'] == 'contextual_provisional' and row['human_reviewed'] is False
            and row['person_id'] == person and row['person_mention_id'] == e['person_mention_id']
            and row['appointment_stage'] == 'appointment' and row['proposal_kind'] == 'unassumed_appointment'
            and row['outcome'] == 'not_assumed' and row['non_assumption_kind'] == 'did_not_take_up'
            and named(p, e, 'person_mention_id', person, named_clause, name)
            and all(anchor['paragraph_id'] == p['id'] and located(anchor, p, clause, word)
                    for anchor, word in [(row['role_anchor'], row['title']), (row['appointment_anchor'], verb),
                                         (row['non_assumption_anchor'], result)])
        )
    except (KeyError, TypeError, ValueError, IndexError):
        return False
