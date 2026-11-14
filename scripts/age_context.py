"""Distinguish a source's lifetime age from an explicitly linked death age."""

def age_context_valid(age, events):
    context = age.get('age_context')
    if context is None:
        return True
    if not isinstance(context, dict):
        return False
    if context.get('kind') == 'during_life':
        return set(context) == {'kind'}
    if context.get('kind') != 'at_death' or set(context) != {'kind', 'life_event_id'}:
        return False
    event = events.get(context.get('life_event_id'))
    if (not isinstance(event, dict) or event.get('event_type') != 'death'
            or event.get('status') != 'source_attested'
            or event.get('person_id') != age.get('person_id')):
        return False
    def scope(evidence):
        return tuple(evidence.get(key) for key in ('source_id', 'chapter_id', 'paragraph_id', 'quote'))
    age_scopes = {scope(e) for e in age.get('evidence', [])}
    death_scopes = {scope(e) for e in event.get('evidence', [])}
    return (bool(age_scopes) and age_scopes == death_scopes
            and all(all(isinstance(value, str) and value for value in row) for row in age_scopes))
