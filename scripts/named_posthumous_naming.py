"""明文追號、具名施號者與受者；不得將普通號稱當死後命名。"""
import re

def named_posthumous_naming_valid(holding, paragraphs, mentions, life_events):
    b = holding.get('naming_basis')
    keys = {'kind', 'source_term', 'death_event_id', 'death_anchor',
            'death_subject_mention_id', 'naming_anchor', 'issuer_person_mention_id',
            'recipient_person_mention_id', 'evidence'}
    if (not isinstance(b, dict) or set(b) != keys
            or b.get('kind') != 'named_recipient_after_death'
            or holding.get('mode') != 'posthumous_naming'
            or holding.get('kind') != 'honorific'
            or not isinstance(b.get('evidence'), list) or not b['evidence']
            or b['evidence'] != holding.get('evidence')
            or b['evidence'] != holding.get('effective_period', {}).get('start', {}).get('evidence')):
        return False
    death = life_events.get(b.get('death_event_id'))
    recipient = mentions.get(b.get('recipient_person_mention_id'))
    issuer = mentions.get(b.get('issuer_person_mention_id'))
    subject = mentions.get(b.get('death_subject_mention_id'))
    if (not death or death.get('event_type') != 'death'
            or death.get('person_id') != holding.get('person_id')
            or not recipient or not issuer or not subject
            or recipient[2].get('kind') != 'person' or subject[2].get('kind') != 'person'
            or issuer[2].get('kind') != 'person' or not issuer[2].get('person_id')
            or recipient[2].get('person_id') != holding.get('person_id')
            or subject[2].get('person_id') != holding.get('person_id')
            or issuer[2].get('person_id') == holding.get('person_id')):
        return False
    da, na = b.get('death_anchor'), b.get('naming_anchor')
    def exact(a, text):
        return (isinstance(a, dict) and set(a) == {'start', 'end', 'surface'}
                and type(a['start']) is int and type(a['end']) is int
                and 0 <= a['start'] < a['end'] <= len(text)
                and text[a['start']:a['end']] == a['surface'])
    for e in b['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit:
            return False
        text = hit[1].get('text', '')
        pid = e['paragraph_id']
        if (e.get('chapter_id') != hit[0] or e.get('quote') != text
                or b.get('source_term') != text or e.get('person_mention_id') != recipient[2]['id']
                or any(m[0] != hit[0] or m[1] != pid for m in (recipient, issuer, subject))
                or not exact(da, text) or not exact(na, text)
                or da['surface'] not in ('卒', '及卒', '薨', '及薨', '死', '及死')
                or da['end'] > issuer[2]['start']
                or subject[2]['end'] > da['start']
                or not any(x.get('paragraph_id') == pid and x.get('quote') == text
                           and x.get('source_id') == e.get('source_id') for x in death.get('evidence', []))):
            return False
        before = [m for m in hit[1].get('mentions', [])
                  if m.get('kind') == 'person' and m.get('end', len(text) + 1) <= da['start']]
        if not before or max(before, key=lambda m: m['end'])['id'] != subject[2]['id']:
            return False
        expected = '追號' + recipient[2]['surface'] + '曰' + holding.get('title', '')
        title_start = recipient[2]['end'] + 1
        if (not holding.get('title') or na['surface'] != expected
                or issuer[2]['end'] != na['start']
                or recipient[2]['start'] != na['start'] + 2
                or not any(a.get('paragraph_id') == pid and a.get('person_mention_id') == recipient[2]['id']
                           and a.get('start') == title_start and a.get('end') == na['end']
                           and a.get('surface') == holding['title']
                           and a.get('usage') == 'posthumous_usage'
                           for a in holding.get('attestations', []))):
            return False
    return True
