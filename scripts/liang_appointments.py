"""Verify unassumed appointments in Liang biographies and their parallel accounts."""
try:
    from scripts.chenshu023_shenjunli import located, named
except ImportError:
    from chenshu023_shenjunli import located, named


QIA = 'c-liangshu-027-daoqia-complete'
QIA_REAPPOINTMENT = '五年，復爲太子中庶子，領步兵校尉，未拜，仍遷給事黃門侍郎'
PEI_SUI_SHIAN = (
    '由是左遷爲始安太守。邃志欲立功邊陲，不願閑遠，乃致書於呂僧珍曰：「昔阮咸、顏延有『二始』之歎。'
    '吾才不逮古人，今爲三始，非其願也，將如之何！」未及至郡')
ZHIPING = '4kt_0ar_aqo_AAB'
ZHIPING_CHEN_OFFICES = '陳文帝初，除光祿大夫、慈訓宮衛尉，並不就'
WITNESSES = {
    'b-liangshu-027': (1511478, 'fcb730ce00423c60dc63e01c4a6d43ecd45cf2669df595850e0abb2339acfb5f'),
    'b-liangshu-028': (1511902, '7dddc5f314909ad5670a3b530f0c1c1c8ecc4f7748c4166a8cb5558a6b8cd080'),
    'b-nanshi-058': (513461, '6ea7470791ba480cec67928464d333afeca6f2bc112d80e79ab526bb6da31983'),
}
READINGS = {
    ('c-liangshu-028-peisui-complete', '始安太守'): (
        4, 'vtp_lo9_0af', '邃與鄉人共入魏武廟', '邃', PEI_SUI_SHIAN, '左遷爲', '未及至郡'),
    ('c-liangshu-028-peisui-complete', '北徐州刺史'): (
        5, 'vtp_lo9_0af', '以邃爲假節', '邃', '除持節、督北徐州諸軍事、信武將軍、北徐州刺史。未之職', '除', '未之職'),
    ('c-liangshu-027-yinjun-complete', '五兵尚書'): (
        2, 'ceq_pnr_q0e_A', '鈞體羸多疾', '鈞',
        '服闋，遷五兵尚書，猶以頓瘵經時，不堪拜受，乃更授散騎常侍', '遷', '不堪拜受'),
    ('c-liangshu-027-mingshanbin-complete', '國子博士'): (
        0, 'nbb_y6s_bfz_AA', '父僧紹', '僧紹', '宋末國子博士徵，不就。', '徵', '不就'),
    (QIA, '晉安王國左常侍'): (1, '4mr_j4p_k5h', '洽年十八', '洽', '除晉安王國左常侍，不就。', '除', '不就'),
    (QIA, '太子中庶子'): (3, '4mr_j4p_k5h', '洽兄弟羣從', '洽', QIA_REAPPOINTMENT, '復爲', '未拜'),
    (QIA, '步兵校尉'): (3, '4mr_j4p_k5h', '洽兄弟羣從', '洽', QIA_REAPPOINTMENT, '領', '未拜'),
    ('c-liangshu-028-peizhili-complete', '長流參軍'): (
        0, 'vtp_lo9_0af_A', '子之禮', '之禮', '王爲南兗，除長流參軍，未行，仍留宿衛，補直閤將軍', '除', '未行'),
    ('c-liangshu-028-peizhiping-complete', '扶風、弘農二郡太守'): (
        0, ZHIPING, '之平字如原', '之平', '歷武陵王常侍、扶風、弘農二郡太守，不行，除譙州長史、陽平太守', '歷', '不行'),
    ('c-nanshi-058-peizhiping-death', '光祿大夫'): (
        0, ZHIPING, '之高第五弟之平', '之平', ZHIPING_CHEN_OFFICES, '除', '並不就'),
    ('c-nanshi-058-peizhiping-death', '慈訓宮衛尉'): (
        0, ZHIPING, '之高第五弟之平', '之平', ZHIPING_CHEN_OFFICES, '除', '並不就'),
}


def valid(row, chapter):
    try:
        index, person, named_clause, name, clause, verb, result = READINGS[chapter['id'], row['title']]
        book = chapter['book_id']
        revision, digest = WITNESSES[book]
        p = chapter['paragraphs'][index]
        e, = row['evidence']
        return (
            chapter['id'].startswith('c-' + book[2:] + '-') and chapter['work_id'] == 'w-' + book.split('-')[1]
            and chapter['source_id'] == 's-' + chapter['id'][2:] + '-ws' + str(revision)
            and chapter['source']['raw_file_sha256'] == digest
            and chapter['source']['revision_id'] == p['source_position']['revision_id'] == revision
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
