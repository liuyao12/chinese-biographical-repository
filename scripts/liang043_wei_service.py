"""Read the distinct funeral awards made following the Qing-tang fighting."""
from hashlib import sha256

PEOPLE = {'粲':'axs_5y7_p7w_AAAA','助':'axs_5y7_p7w_AAAB','警':'axs_5y7_p7w_AAAC','構':'axs_5y7_p7w_AAAD','尼':'axs_5y7_p7w_AAAAB','昂':'spa_2ae_p2l'}
TERMS = {'粲':'詔贈護軍將軍','助':'追贈助、警、構及尼皆中書郎','警':'追贈助、警、構及尼皆中書郎','構':'追贈助、警、構及尼皆中書郎','尼':'追贈助、警、構及尼皆中書郎','昂':'追贈助、警、構及尼皆中書郎，昂員外散騎常侍'}


def funeral_gift_valid(holding, paragraphs, mentions, events):
    try:
        basis = holding['posthumous_basis']
        event = events[basis['death_event_id']]
        occurrence, = holding['attestations']
        evidence, = holding['evidence']
        chapter, paragraph = paragraphs[occurrence['paragraph_id']]
        name = next(name for name, ident in PEOPLE.items() if ident == holding['person_id'])
        text = paragraph['text']
        death = event['source_anchor']
        source = TERMS[name]
        location = text.index(source)
        title = '護軍將軍' if name == '粲' else '員外散騎常侍' if name == '昂' else '中書郎'
        speaker, subject_paragraph, subject = mentions[occurrence['person_mention_id']]
        subject_context = '賊傳粲首' if name == '粲' else source
        return (chapter == speaker == 'c-liangshu-043-weican' and subject_paragraph == paragraph['id']
                and paragraph['source_position']['revision_id'] == 2087360
                and paragraph['source_position']['first_line'] == paragraph['source_position']['last_line'] == 17
                and sha256(text.encode()).hexdigest() == PARAGRAPH_DIGEST
                and event['person_id'] == subject['person_id'] == holding['person_id']
                and event['event_type'] == 'death' and death['paragraph_id'] == paragraph['id']
                and text[death['start']:death['end']] == event['source_term'] == ('遂見害' if name == '粲' else '皆戰死')
                and death['end'] < location and subject['surface'] == name
                and subject['start'] == text.index(subject_context) + subject_context.index(name)
                and evidence['person_mention_id'] == subject['id'] and evidence['quote'] == text
                and basis['source_term'] == source and basis['evidence'] == [evidence]
                and holding['mode'] == 'posthumous_grant' and holding['kind'] == 'office'
                and occurrence['usage'] == 'posthumous_usage' and holding['title'] == title
                and occurrence['start'] == location + source.index(title)
                and text[occurrence['start']:occurrence['end']] == title)
    except (KeyError, ValueError, TypeError, StopIteration):
        return False


PARAGRAPH_DIGEST = 'b2921bd66eed081d54a41082fc34656f28357484f70a755ef1be142a1fae1865'
