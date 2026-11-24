"""Identify the two endpoints of the named son in the received Northern History roll of Mingyuan's sons."""
def named_son_valid(assertion, evidence, chapter):
    if not chapter or chapter.get('book_id') != 'b-beishi-016' or chapter['source'].get('revision_id') != 1518816:
        return False
    child_id, father_id = assertion['subject_person_id'], assertion['object_person_id']
    if assertion.get('predicate') != 'father' or father_id != '19f_55e_8b2':
        return False
    paragraph_id = evidence['paragraph_id']
    paragraph = next((p for p in chapter['paragraphs'] if p['id'] == paragraph_id), None)
    if not paragraph or paragraph.get('source_position', {}).get('first_line') != 87:
        return False
    text = paragraph['text']
    child = next((m for m in paragraph['mentions'] if m['id'] == evidence.get('subject_person_mention_id')), None)
    father = next((x for x in chapter['annotation'].get('person_reference_occurrences', [])
                   if x['id'] == evidence.get('object_person_reference_id') and x['paragraph_id'] == paragraph_id), None)
    clause = '尹夫人生永昌莊王健'
    return bool(text.startswith('明元皇帝七男：') and text.count(clause) == 1 and evidence.get('quote') == text
                and assertion['qualifiers'].get('source_term') == clause
                and father and father.get('person_id') == father_id and father.get('surface') == '明元皇帝'
                and (father.get('start'), father.get('end')) == (0, 4)
                and child and child.get('person_id') == child_id and child.get('surface') == '健'
                and (child.get('start'), child.get('end')) == (text.index(clause) + len(clause) - 1, text.index(clause) + len(clause)))
