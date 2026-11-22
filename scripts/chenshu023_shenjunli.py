"""Match the Shen family's succession, marriage and appointments in Chen 23."""

CHAPTER = 'c-chenshu-023-shenjunli-complete'
JUNLI = '9wm_vgh_vz1_AA'
JUNGAO = '9wm_vgh_vz1_AD'
DAUGHTER = '9wm_vgh_vz1_ADB'
CHANGSHA = 'icd_mkz_d9n_D'
HEIR = '9wm_vgh_vz1_ADA'
HEIR_SENTENCE = '君理子遵儉早卒，以弟君高子遵禮為嗣。'
MARRIAGE = '出為宣遠將軍、平南長沙王長史、南海太守，行廣州事。以女為王妃，固辭不行，復為衛尉卿。'
FIRST = '其年起君理為信威將軍、左衛將軍。'
SECOND = '又起為持節、都督東衡衡二州諸軍事、仁威將軍、東衡州刺史，領始興內史。'
THIRD = '又起為明威將軍、中書令。'
THREE = '前後奪情者三，並不就。'


def located(anchor, paragraph, clause, word):
    text = paragraph['text']
    if text.count(clause) != 1 or clause.count(word) != 1:
        return False
    pos = text.index(clause) + clause.index(word)
    return (anchor.get('paragraph_id', paragraph['id']) == paragraph['id']
            and (anchor['surface'], anchor['start'], anchor['end']) == (word, pos, pos + len(word)))


def named(paragraph, evidence, field, person, clause, word):
    mention, = (m for m in paragraph['mentions'] if m['id'] == evidence[field])
    return (mention['kind'] == 'person' and mention['person_id'] == person
            and located(mention, paragraph, clause, word))


def fixed(paragraph, evidence):
    return (paragraph['source_position']['revision_id'] == 1514496
            and paragraph['id'] == evidence['paragraph_id'] and evidence['quote'] == paragraph['text']
            and evidence['chapter_id'] == CHAPTER and evidence['source_id'] == 's-chenshu-023-shenjunli-complete-ws1514496')


def daughter_valid(row, evidence, chapter):
    try:
        p = chapter['paragraphs'][5]
        other, clause, word, term = {
            'father': (JUNGAO, '君理第六弟君高，字季高', '君高', '以女為王妃'),
            'spouse': (CHANGSHA, MARRIAGE, '長沙王', '平南長沙王長史、南海太守，行廣州事。以女為王妃'),
        }[row['predicate']]
        q = row['qualifiers']
        ref, = (r for r in chapter['annotation']['person_reference_occurrences'] if r['id'] == evidence['subject_person_reference_id'])
        return (chapter['id'] == CHAPTER and fixed(p,evidence) and row['subject_person_id'] == ref['person_id'] == DAUGHTER
                and row['object_person_id'] == other and row['status'] == 'source_attested'
                and ref['paragraph_id'] == p['id'] and ref['referent_role'] == 'third_person'
                and q['source_term'] == term and q['reading_basis']['kind'] == 'chen023_jungao_daughter'
                and located(ref,p,MARRIAGE,'女') and located(q['reading_basis']['role_anchor'],p,MARRIAGE,'女')
                and named(p,evidence,'object_person_mention_id',other,clause,word))
    except (KeyError,TypeError,IndexError,ValueError):
        return False


def succession_valid(row, paragraphs):
    try:
        evidence, = row['evidence']
        cid, p = paragraphs[evidence['paragraph_id']]
        return (cid == CHAPTER and fixed(p,evidence) and p['source_position']['first_line'] == 17
                and row['predicate'] == 'ritual_successor_of' and row['subject_person_id'] == HEIR and row['object_person_id'] == JUNLI
                and row['qualifiers'] == dict(source_term='以弟君高子遵禮為嗣', succession_kind='chen023_nephew_as_heir', parentage_inference='not_inferred')
                and named(p,evidence,'subject_person_mention_id',HEIR,HEIR_SENTENCE,'遵禮')
                and named(p,evidence,'object_person_mention_id',JUNLI,HEIR_SENTENCE,'君理')
                and any(m['person_id'] == JUNGAO and m['kind'] == 'person' and located(m,p,HEIR_SENTENCE,'君高') for m in p['mentions']))
    except (KeyError,TypeError,IndexError,ValueError):
        return False


def proposal_valid(row, chapter):
    try:
        title = row['title']
        if title in ('宣遠將軍','平南長沙王長史','南海太守'):
            pi,person,clause,verb,result_clause,result = 5,JUNGAO,MARRIAGE,'出為',MARRIAGE,'固辭不行'
        else:
            pi,person = 2,JUNLI
            if title == '左民尚書':
                clause = result_clause = '遷守左民尚書，未拜，為明威將軍'
                verb,result = '遷守','未拜'
            else:
                clause,verb = {
                    '信威將軍': (FIRST,'起'), '左衛將軍': (FIRST,'起'),
                    '仁威將軍': (SECOND,'又起為'), '東衡州刺史': (SECOND,'又起為'), '始興內史': (SECOND,'又起為'),
                    '明威將軍': (THIRD,'又起為'), '中書令': (THIRD,'又起為'),
                }[title]
                result_clause,result=THREE,'並不就'
        p=chapter['paragraphs'][pi]
        e,=row['evidence']
        first,word=('君理因自請往荊州迎喪柩','君理') if person==JUNLI else ('君理第六弟君高，字季高','君高')
        return (chapter['id'] == CHAPTER and fixed(p,e) and row['person_id'] == person and row['person_mention_id'] == e['person_mention_id']
                and row['appointment_stage'] == 'appointment' and row['proposal_kind'] == 'unassumed_appointment'
                and row['outcome'] == 'not_assumed' and row['non_assumption_kind'] == 'did_not_take_up'
                and named(p,e,'person_mention_id',person,first,word)
                and located(row['role_anchor'],p,clause,title) and located(row['appointment_anchor'],p,clause,verb)
                and located(row['non_assumption_anchor'],p,result_clause,result))
    except (KeyError,TypeError,IndexError,ValueError):
        return False
