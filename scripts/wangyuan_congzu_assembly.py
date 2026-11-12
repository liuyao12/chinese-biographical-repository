# -*- coding: utf-8 -*-
"""Validate the narrowly sourced Wang Yuan link into the Langye Wang assembly."""

EXPECTED_PATH = [
    'a-song071-sengchuo-006',       # Wang Jian -> Wang Sengchuo
    'a-songshu063-phase5-027',      # Wang Sengchuo -> Wang Tanshou
    'a-jinshu065-wang-019',         # Wang Tanshou -> Wang Xun
]


def congzu_depth_valid(assertion):
    q = assertion.get('qualifiers', {})
    structure = q.get('kinship_structure', {})
    lexical = q.get('lexical_sources', [])
    return (assertion.get('id') == 'a-nanqi046-sengyou-jian-congzu-older'
            and assertion.get('predicate') == 'agnatic_cousin'
            and q.get('source_term') == '從祖兄'
            and structure.get('distance') == {
                'kind': 'paternal_second_cousins',
                'common_ancestor_depth': {'subject': 3, 'reference': 3}}
            and structure.get('common_ancestor_person_id') is None
            and len(lexical) == 1 and lexical[0].get('author') == '鄭玄注、賈公彥疏'
            and lexical[0].get('quote') == '父之從父昆弟之子；己之再從兄弟'
            and lexical[0].get('url', '').startswith('https://'))


def valid(member, rows, assertions):
    c = member.get('ancestor_connection', {})
    yuan = '7r6_k52_qji_ABAAAA*A'
    sengyou = '7r6_k52_qji_ABAAAA*AA'
    xun = '7r6_k52_qji_ABAAAA'
    jian = '7r6_k52_qji_ABAAAAEAA'
    if (member.get('person_id') != yuan or member.get('ancestor_person_id') != xun
            or member.get('connection') != 'grandfather' or member.get('generation_distance') != 2
            or member.get('intermediate_person_ids') != [None] or member.get('parent_person_id') is not None
            or member.get('source_assertion_id') is not None or c.get('type') != 'wangyuan_congzu_shared_ancestor_path'
            or c.get('status') != 'contextual_provisional' or c.get('human_reviewed') is not False
            or c.get('common_ancestor_depth') != 3 or not c.get('rationale')):
        return False
    if yuan.count('*') != 1 or sengyou != yuan + 'A' or xun not in rows or sengyou not in rows:
        return False
    if rows[sengyou].get('parent_person_id') != yuan or rows[sengyou].get('source_assertion_id') != 'a-nanqishu046-sengyou-father':
        return False
    kin = assertions.get('a-nanqi046-sengyou-jian-congzu-older')
    father = assertions.get('a-nanqishu046-sengyou-father')
    if not kin or not father or kin.get('predicate') != 'agnatic_cousin' or kin.get('status') != 'source_attested':
        return False
    if (kin.get('subject_person_id') != sengyou or kin.get('object_person_id') != jian
            or kin.get('qualifiers', {}).get('kinship_structure', {}).get('distance') != {
                'kind': 'paternal_second_cousins', 'common_ancestor_depth': {'subject': 3, 'reference': 3}}
            or kin.get('qualifiers', {}).get('kinship_structure', {}).get('common_ancestor_person_id') is not None):
        return False
    if (father.get('predicate') != 'father' or father.get('subject_person_id') != sengyou
            or father.get('object_person_id') != yuan or father.get('status') != 'source_attested'):
        return False
    # Follow three direct, source-backed father assertions from Jian to Xun.
    current = jian
    for assertion_id in EXPECTED_PATH:
        a = assertions.get(assertion_id)
        if (not a or a.get('predicate') != 'father' or a.get('status') != 'source_attested'
                or a.get('subject_person_id') != current or a.get('qualifiers', {}).get('lineage') != 'paternal'):
            return False
        current = a.get('object_person_id')
    if current != xun:
        return False
    if member.get('interpretation_note', '').find('不新增王遠至王珣的來源斷言') < 0:
        return False
    refs = c.get('references')
    expected = set(EXPECTED_PATH + [kin['id'], father['id']])
    if (c.get('ancestor_path_assertion_ids') != EXPECTED_PATH or not isinstance(refs, list)
            or {r.get('assertion_id') for r in refs} != expected):
        return False
    for ref in refs:
        a = assertions[ref['assertion_id']]
        if not ref.get('scope') or not ref.get('url', '').startswith(('https://', 'http://')) or not any(ref.get('quote') == e.get('quote')
                and ref.get('paragraph_id') == e.get('paragraph_id')
                and ref.get('chapter_id') == e.get('chapter_id')
                and ref.get('source_id') == e.get('source_id') for e in a.get('evidence', [])):
            return False
    return True
