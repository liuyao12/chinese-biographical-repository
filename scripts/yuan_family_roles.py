"""Check a named relative or spouse against the role word in Song 50 using its positions."""
def valid(assertion, evidence, chapter):
    if not chapter or chapter['source']['revision_id'] != 2371899 or chapter['book_id'] != 'b-songshu-050':
        return False
    paragraph = next((p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id']),None)
    if not paragraph or evidence['quote'] != paragraph['text']:
        return False
    t = paragraph['text']
    names = {m['id']: m for m in paragraph['mentions']}
    roles = {m['id']: m for m in chapter['annotation']['person_reference_occurrences'] if m['paragraph_id'] == paragraph['id']}
    ids, anchors = [], []
    for k in ('subject','object'):
        m = names.get(evidence.get(k+'_person_mention_id')) or roles.get(evidence.get(k+'_person_reference_id'))
        if not m or m['person_id'] != assertion[k+'_person_id'] or t[m['start']:m['end']] != m['surface']:
            return False
        ids.append(m['person_id'])
        anchors.append((m['surface'],m['start']))
    if ids[0] == ids[1]:
        return False
    anchors = tuple(anchors)
    term = assertion['qualifiers']['source_term']
    if term == '徐遺寶，護之妻弟也' and t.count(term) == 1:
        pos=t.index(term)
        return ((assertion['predicate']=='spouse' and anchors==( ('護之',pos+4), ('妻',pos+6)))
                or (assertion['predicate']=='brother' and anchors==( ('妻',pos+6), ('徐遺寶',pos))))
    if term == '母墓' and t.startswith('遵子閬，') and t.count('。母墓') == 1:
        return assertion['predicate']=='mother' and anchors==(('閬',2),('母',t.index('。母墓')+1))
    return False
