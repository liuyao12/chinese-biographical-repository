"""Validate the adjacent named parent, unnamed female child and marriage verb."""
def married_daughter_valid(assertion, evidence, chapter):
    if assertion.get('predicate') != 'father' or evidence.get('source_id') != chapter['source_id']:
        return False
    paragraph = next((p for p in chapter['paragraphs'] if p['id'] == evidence.get('paragraph_id')), None)
    if not paragraph or paragraph['text'] != evidence.get('quote'):
        return False
    name = next((m for m in paragraph['mentions'] if m['id'] == evidence.get('object_person_mention_id')), None)
    references = chapter['annotation'].get('person_reference_occurrences', [])
    child = next((r for r in references if r['id'] == evidence.get('subject_person_reference_id')
                  and r['paragraph_id'] == paragraph['id']), None)
    if not name or not child:
        return False
    text = paragraph['text']
    return (name.get('kind') == 'person' and name['person_id'] == assertion['object_person_id']
            and child['person_id'] == assertion['subject_person_id']
            and child['person_id'] != name['person_id'] and child['referent_role'] == 'third_person'
            and name['end'] == child['start'] and child['surface'] == text[child['start']:child['end']] == '女'
            and name['surface'] == text[name['start']:name['end']]
            and text[child['end']:child['end'] + 1] == '嫁'
            and assertion['qualifiers']['source_term'] == text[name['start']:child['end'] + 1])
