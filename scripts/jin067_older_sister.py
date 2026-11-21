"""Read a named sister through the husband's name and the quoted Wang family record."""

def valid(assertion, evidence, chapters):
    try:
        chapter = chapters[evidence['chapter_id']]
        paragraph = next(p for p in chapter['paragraphs'] if p['id'] == evidence['paragraph_id'])
        names = {m['id']: m for m in paragraph['mentions'] if m['kind'] == 'person'}
        subject = names[evidence['subject_person_mention_id']]
        husband = names[evidence['husband_person_mention_id']]
        sister = next(r for r in chapter['annotation']['person_reference_occurrences']
                      if r['id'] == evidence['object_reference_id'])
        link = assertion['qualifiers']['reading_basis']
        genealogy = chapters['c-shishuoxinyu-006-jin080-xizhi']
        control = next(p for p in genealogy['paragraphs'] if p['id'] == link['genealogy_paragraph_id'])
        q = paragraph['text']
        return (assertion['predicate'] == 'sister' and evidence['quote'] == q
                and subject['person_id'] == assertion['subject_person_id'] and subject['start'] == 0
                and q.startswith(subject['surface']+'字方回') and subject['surface'] == '愔'
                and sister['surface'] == '姊' and sister['referent_role'] == 'third_person'
                and sister['person_id'] == assertion['object_person_id'] and sister['paragraph_id'] == paragraph['id']
                and q[sister['start']-1:husband['end']] == assertion['qualifiers']['source_term'] == '與姊夫王羲之'
                and husband['start'] == sister['end']+1 and husband['surface'] == '王羲之'
                and control['text_layer'] == 'witness_appended_liuxiaobiao_note'
                and control['attribution']['quoted_work'] == '王氏譜'
                and control['text'].endswith('羲之妻，太傅郗鑒女，名璿，字子房。')
                and any(m['surface'] == '羲之' and m['person_id'] == husband['person_id'] for m in control['mentions'])
                and any(m['surface'] == '璿' and m['person_id'] == sister['person_id'] for m in control['mentions']))
    except (KeyError, TypeError, StopIteration, IndexError):
        return False
