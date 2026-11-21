def valid(event, evidence, chapter):
    """Verify a received death word immediately following its third-person subject."""
    if event.get('event_type') != 'death' or event.get('source_term') not in ('崩','薨','卒'):
        return False
    paragraph = next((p for p in chapter['paragraphs'] if p['id'] == evidence.get('paragraph_id')), None)
    if not paragraph or evidence.get('quote') != paragraph['text']:
        return False
    refs = chapter['annotation'].get('person_reference_occurrences', [])
    matches = [r for r in refs if r['id'] == evidence.get('person_reference_id')]
    if len(matches) != 1:
        return False
    role = matches[0]
    anchor = event.get('source_anchor', {})
    text = paragraph['text']
    if not isinstance(anchor, dict) or not all(type(anchor.get(key)) is int for key in ('start','end')):
        return False
    return (role['paragraph_id'] == anchor.get('paragraph_id') == paragraph['id']
            and role['person_id'] == event['person_id'] and role['referent_role'] == 'third_person'
            and text[role['start']:role['end']] == role['surface'] == evidence.get('reference_surface')
            and role['end'] == anchor.get('start')
            and text[anchor['start']:anchor['end']] == anchor.get('surface') == event['source_term'])
