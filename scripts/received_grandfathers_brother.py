"""以兄孫兩種具名語序確認兩代旁系，未具名的父及祖父留空。"""
def valid(a, paragraphs, mentions):
    try:
        if a['predicate'] != 'grandfathers_brother':
            return False
        q = a['qualifiers']
        if (q['source_term'] != '兄孫' or q['lineage'] != 'paternal'
                or q['object_generation_relative_to_subject'] != -2
                or q['father_person_id'] is not None or q['grandfather_person_id'] is not None):
            return False
        e, = a['evidence']
        c, p = paragraphs[e['paragraph_id']]
        s = mentions[e['subject_person_mention_id']]
        o = mentions[e['object_person_mention_id']]
        if (s[:2] != o[:2] or s[0] != c or s[1] != p['id'] or e['quote'] != p['text']
                or s[2]['person_id'] != a['subject_person_id'] or o[2]['person_id'] != a['object_person_id']):
            return False
        text = p['text']
        younger, older = s[2], o[2]
        if text[older['end']:older['end']+2] != '兄孫':
            return False
        if younger['start'] == older['end'] + 2:
            return True
        return (younger['end'] < older['start'] and text[older['end']+2:older['end']+4] == '也。'
                and text[younger['end']:older['start']] == '，宋鎮北大將軍')
    except (IndexError,KeyError,ValueError,TypeError):
        return False
