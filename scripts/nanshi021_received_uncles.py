"""Bind the nephew and uncle in two received family introductions, including a titled, named father."""


def valid(claim, paragraphs):
    try:
        evidence, = claim['evidence']
        cid, paragraph = paragraphs[evidence['paragraph_id']]
        marks = {m['id']:m for m in paragraph['mentions'] if m['kind'] == 'person'}
        nephew = marks[evidence['subject_person_mention_id']]
        uncle = marks[evidence['object_person_mention_id']]
        term = claim['qualifiers']['source_term']
        text = paragraph['text']
        if (claim['predicate'] != 'paternal_uncle' or paragraph['source_position']['revision_id'] != 1752646
                or evidence['quote'] != text or cid != evidence['chapter_id'] or paragraph['text_layer'] != 'received_chapter'
                or nephew['person_id'] != claim['subject_person_id'] or uncle['person_id'] != claim['object_person_id']):
            return False
        def bind(name, start, end):
            found = [m for m in marks.values() if (m['surface'],m['start'],m['end']) == (name,start,end)]
            return found[0] if len(found) == 1 and text[start:end] == name else None
        if cid == 'c-nanshi-021-wangsengyou':
            return (text.startswith('遠子僧佑字胤宗，幼聰悟，叔父微撫其首曰：「兒神明意用，當不作率爾人。」')
                    and term == '叔父微' and bind('遠',0,1) and bind('僧佑',2,4)['person_id'] == nephew['person_id']
                    and bind('胤宗',5,7)['person_id'] == nephew['person_id']
                    and bind('微',text.index('叔父微')+2,text.index('叔父微')+3) == uncle)
        if cid == 'c-nanshi-021-wangwei':
            return (text.startswith('微字景玄，弘弟光祿大夫孺之子也。') and term == '弘弟光祿大夫孺之子也'
                    and bind('微',0,1)['person_id'] == nephew['person_id'] and bind('景玄',2,4)['person_id'] == nephew['person_id']
                    and bind('弘',5,6) == uncle and bind('孺',11,12)['person_id'] not in (uncle['person_id'], nephew['person_id']))
        return False
    except (TypeError, ValueError, KeyError, IndexError):
        return False
