"""用王彪之本傳首句和「從伯導謂曰」專名位置核兩人輩行。"""


def biao_congbo_valid(assertion, paragraphs):
    try:
        evidence, = assertion['evidence']
        cid, p = paragraphs[evidence['paragraph_id']]
        term = assertion['qualifiers']['source_term']
        if (cid != 'c-jinshu-076-wangbiaozhi' or evidence['chapter_id'] != cid or
                evidence['paragraph_id'] != cid + ':line055' or term != '從伯導' or
                evidence['quote'] != p['text'] or p['text'].count('從伯導謂曰') != 1):
            return False
        names = {m['id']:m for m in p['mentions'] if m['kind'] == 'person'}
        child = names[evidence['subject_person_mention_id']]
        senior = names[evidence['object_person_mention_id']]
        return (assertion['predicate'] == 'agnatic_senior_kin'
                and p['text'].startswith('彪之字叔武。')
                and child['start'] == 0 and child['end'] == 2 and child['surface'] == '彪之'
                and child['person_id'] == assertion['subject_person_id'] == '7r6_k52_qji_ABDBB'
                and senior['person_id'] == assertion['object_person_id'] == '7r6_k52_qji_ABAA'
                and senior['start'] == p['text'].index('從伯導謂曰') + 2
                and senior['end'] == senior['start'] + 1 and senior['surface'] == '導'
                and assertion['qualifiers']['kinship_structure'] == dict(
                    lineage='paternal', generation_difference=-1, collateral=True, distance=None,
                    common_ancestor_person_id=None, subject_relative_age='unknown'))
    except (KeyError, TypeError, ValueError, IndexError):
        return False
