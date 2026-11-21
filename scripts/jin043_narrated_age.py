"""Verify the reported 六七歲 in Wang Rong's fixed opening and the two same-person anchors."""
def age_errors(age, paragraph):
    try:
        text = paragraph['text']
        subject = age['person_id']
        binding = age['subject_scope']
        evidence, = age['evidence']
        named = {m['id']: m for m in paragraph['mentions'] if m.get('kind') == 'person'}
        head = named[evidence['person_mention_id']]
        action = named[binding['resumption_person_mention_id']]
        quote = '年六七歲，于宣武場觀戲，猛獸在檻中虓吼震地，眾皆奔走，戎獨立不動'
        start = text.index(quote)
        reading = age['approximation_interpretation']
        ok = (paragraph['id'] == 'c-jinshu-043-wangrong:p001'
              and binding == {'kind':'narrated_age_between_head_and_action','source_quote':quote,'resumption_person_mention_id':action['id']}
              and paragraph.get('text_layer')=='received_chapter'
              and head['start']==0 and text.startswith('王戎，字濬沖') and head['surface']=='王戎'
              and action['start']==start+quote.index('戎') and text[action['start']:action['end']]==action['surface']=='戎'
              and head['person_id']==action['person_id']==subject
              and evidence['quote']==text and evidence['paragraph_id']==paragraph['id']
              and age['source_term']=='年六七歲' and age['source_number']=='六七'
              and age['approximation']=={'kind':'adjacent_age_numbers','numbers':[6,7]}
              and age.get('value') is None and age.get('birth_year') is None
              and not any(k in age for k in ('bounds','source_number_bounds','group_reference','normalized_date'))
              and age['reporting_status']=='approximate_report' and reading['status']=='editorial_provisional'
              and reading['human_reviewed'] is False and bool(reading['reviewer']) and bool(reading['rationale']))
        return [] if ok else ['王戎觀戲約齡須綁傳首、觀戲與不動的同一人原文，保留六七約數。']
    except (ValueError, KeyError, TypeError, AttributeError):
        return ['王戎觀戲年齡來源不全。']
