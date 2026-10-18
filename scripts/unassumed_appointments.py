"""任用後未受或未赴任，與未實行的立號提議分開。"""


def unassumed_appointment_valid(proposal, chapter):
    if (proposal.get('proposal_kind') != 'unassumed_appointment' or proposal.get('outcome') != 'not_assumed'
            or proposal.get('status') != 'contextual_provisional' or proposal.get('human_reviewed') is not False
            or len(proposal.get('evidence', [])) != 1):
        return False
    e = proposal['evidence'][0]
    p = next((p for p in chapter.get('paragraphs', []) if p['id'] == e.get('paragraph_id')), None)
    if (not p or e.get('chapter_id') != chapter.get('id')
            or any(e.get(k) != chapter.get(k) for k in ['work_id', 'book_id', 'source_id'])):
        return False
    quote = e.get('quote')
    if not isinstance(quote, str) or not quote or quote not in p['text']:
        return False
    ms = {m['id']: m for m in p['mentions']}
    person, role = ms.get(proposal.get('person_mention_id')), ms.get(proposal.get('role_mention_id'))
    if (not person or not role or person.get('kind') != 'person'
            or person.get('person_id') != proposal.get('person_id')
            or role.get('kind') != 'unresolved' or role.get('person_id') is not None
            or role.get('surface') != proposal.get('title')):
        return False
    def anchor(value):
        return (isinstance(value, dict) and set(value) == {'paragraph_id','start','end','surface'}
                and value.get('paragraph_id') == p['id'] and type(value.get('start')) is int
                and type(value.get('end')) is int and 0 <= value['start'] < value['end'] <= len(p['text'])
                and p['text'][value['start']:value['end']] == value.get('surface'))
    appointment, refusal = proposal.get('appointment_anchor'), proposal.get('non_assumption_anchor')
    if not anchor(appointment) or not anchor(refusal):
        return False
    verbs = ['引為','引爲','遷','尋加','以'+person['surface']+'為','以'+person['surface']+'爲']
    terms = {'declined':['以疾固辭，未行而卒','苦讓，遂不受'], 'did_not_take_up':['並不行']}
    if (appointment['surface'] not in verbs or refusal['surface'] not in terms.get(proposal.get('non_assumption_kind'), [])
            or person['end'] > role['start'] or appointment['end'] > role['start']
            or role['end'] > refusal['start']):
        return False
    # A different named recipient in the assignment list cannot be silently bypassed.
    if any(m.get('kind') == 'person' and m.get('person_id') != proposal['person_id']
           and appointment['end'] <= m['start'] < role['end'] for m in p['mentions']):
        return False
    return any(i <= min(person['start'], appointment['start']) and refusal['end'] <= i + len(quote)
               for i in range(len(p['text'])) if p['text'].startswith(quote, i))
