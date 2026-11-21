"""核齊書四十九兩條贈官原句、同人卒事與受者字位。"""
def valid(h, paragraphs, mentions, events):
    try:
        b = h['posthumous_basis']
        e, = h['evidence']
        att, = h['attestations']
        cid, p = paragraphs[e['paragraph_id']]
        c, pid, m = mentions[b['recipient_mention_id']]
        event = events[b['death_event_id']]
        d = event['source_anchor']
        dc, dp = paragraphs[d['paragraph_id']]
        term, titles, subject = {
            'c-nanqishu-049-fangsengji': ('贈僧寄益州刺史', ('益州刺史',), '僧寄'),
            'c-nanqishu-049-zhangchong': ('東昏詔贈沖散騎常侍、護軍將軍', ('散騎常侍','護軍將軍'), '沖'),
        }[cid]
        start = p['text'].index(term)
        recipient = start + term.index(subject)
        pos = start + term.index(h['title'])
        return (cid == e['chapter_id'] == c == dc and pid == p['id'] and p['source_position']['revision_id'] == dp['source_position']['revision_id'] == 2261984
                and h['mode'] == 'posthumous_grant' and h['kind'] == 'office' and h['title'] in titles
                and e['quote'] == p['text'] and p['text'].count(term) == 1 and b['source_term'] == term
                and b['evidence'] == [e] == h['effective_period']['start']['evidence']
                and m['kind'] == 'person' and m['person_id'] == h['person_id'] == event['person_id']
                and event['event_type'] == 'death' and event['status'] == 'source_attested'
                and dp['text'][d['start']:d['end']] == d['surface'] == event['source_term'] == '病死'
                and any(z['kind'] == 'person' and z['person_id'] == h['person_id'] and z['end'] == d['start'] for z in dp['mentions'])
                and dp['source_position']['raw_character_offsets'][d['end']-1] < p['source_position']['raw_character_offsets'][start]
                and e['person_mention_id'] == att['person_mention_id'] == m['id'] and m['start'] == recipient and m['end'] == recipient+len(subject)
                and att['usage'] == 'posthumous_usage' and att['start'] == pos and att['end'] == pos+len(h['title']) and att['surface'] == h['title'])
    except (KeyError, TypeError, ValueError, IndexError):
        return False
