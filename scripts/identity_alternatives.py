"""Keep source-scoped, unexcluded identity alternatives distinct from equivalence."""

def identity_participant_ids(decision):
    ids = {decision['person_id']} if isinstance(decision.get('person_id'), str) else set()
    alternatives = decision.get('alternatives', [])
    if isinstance(alternatives, list):
        ids.update(a['person_id'] for a in alternatives
                   if isinstance(a, dict) and isinstance(a.get('person_id'), str))
    return ids


def identity_alternative_errors(decision, known_person_ids):
    if 'alternatives' not in decision:
        return []
    alternatives = decision['alternatives']
    if (decision.get('status') != 'contextual_provisional'
            or decision.get('human_reviewed') is not False
            or not isinstance(alternatives, list) or not alternatives):
        return ['未排除身份候選須保留暫定判斷及非人工覆核狀態']
    seen = {decision.get('person_id')}
    for a in alternatives:
        if (not isinstance(a, dict) or set(a) != {'person_id', 'status', 'rationale'}
                or not isinstance(a.get('person_id'), str)
                or a.get('person_id') not in known_person_ids or a.get('person_id') in seen
                or a.get('status') != 'not_preferred_but_not_excluded'
                or not isinstance(a.get('rationale'), str) or not a['rationale'].strip()):
            return ['未排除身份候選須為不同已登記人物，保留理由，不能當同指或確定排除']
        seen.add(a['person_id'])
    return []
