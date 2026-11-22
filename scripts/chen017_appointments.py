"""核《陳書》卷十七任命句所指的人、原官與未赴任字位。"""

TONG = 'c-chenshu-017-wangtong-complete'
MAI = 'c-chenshu-017-wangmai-complete'
CHONG = 'c-chenshu-017-wangchong-complete'
PEOPLE = {TONG: 'q7m_r8k_2vn_ABAC', MAI: 'q7m_r8k_2vn_ABAG', CHONG: '7r6_k52_qji_ABAAAAAABAA'}
GUANG = '乃授使持節、都督廣州等二十州諸軍事、平南將軍、平越中郎將、廣州刺史。未行，改為衡州刺史'
HENG = '改為衡州刺史，持節、都督嵭如故。王琳據有上流，衡、廣攜貳，勱不得之鎮'
COURT = '天嘉元年，徵為侍中、都官尚書，未拜，復為中書令'
RULES = {
    (TONG, '特進'): ('六年，加特進，侍中、將軍、光祿、佐史嵭如故。未拜卒', '加', '未拜'),
    (MAI, '廣州刺史'): (GUANG, '授', '未行'),
    (MAI, '衡州刺史'): (HENG, '改為', '不得之鎮'),
    (MAI, '侍中'): (COURT, '徵為', '未拜'),
    (MAI, '都官尚書'): (COURT, '徵為', '未拜'),
    (CHONG, '左光祿大夫'): ('以本官領左光祿大夫。未拜，改領太子少傅', '以本官領', '未拜'),
}


def valid(proposal, chapter):
    cid = chapter.get('id')
    title = proposal.get('title')
    rule = RULES.get((cid, title))
    if not rule or proposal.get('person_id') != PEOPLE[cid]:
        return False
    clause, verb, result = rule
    paragraphs = [p for p in chapter['paragraphs'] if clause in p['text']]
    if len(paragraphs) != 1:
        return False
    paragraph = paragraphs[0]
    text = paragraph['text']
    if chapter['source'].get('revision_id') != 1544244 or text.count(clause) != 1:
        return False
    named = paragraph
    if cid == CHONG:
        previous = chapter['paragraphs'].index(paragraph) - 1
        if previous < 0 or len(proposal.get('evidence', [])) != 1:
            return False
        named = chapter['paragraphs'][previous]
        context = dict(kind='prior_paragraph_subject', paragraph_id=named['id'],
                       person_mention_id=proposal.get('person_mention_id'),
                       quote='承制以沖為左長史', intervening_paragraph_ids=[])
        evidence = proposal['evidence'][0]
        if evidence.get('context') != context or evidence.get('quote') != clause or context['quote'] not in named['text']:
            return False
    person = next((m for m in named['mentions'] if m['id'] == proposal.get('person_mention_id')), None)
    if not person or person.get('person_id') != PEOPLE[cid] or person['surface'] != {TONG: '通', MAI: '勱', CHONG: '沖'}[cid]:
        return False
    for key, word in [('role_anchor', title), ('appointment_anchor', verb), ('non_assumption_anchor', result)]:
        if clause.count(word) != 1:
            return False
        start = text.index(clause) + clause.index(word)
        if proposal.get(key) != dict(paragraph_id=paragraph['id'], surface=word, start=start, end=start + len(word)):
            return False
    return (proposal.get('appointment_stage') == 'appointment'
            and proposal.get('non_assumption_kind') == 'did_not_take_up'
            and proposal.get('outcome') == 'not_assumed')
