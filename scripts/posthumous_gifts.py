"""來源先敘死亡、後明贈官的逐字記錄，不補出原文沒有的追字。"""


def posthumous_gift_valid(holding, paragraphs, mentions):
    b = holding.get('posthumous_basis')
    if (not isinstance(b, dict) or set(b) != {'kind', 'source_term', 'death_term', 'grant_term', 'recipient_person_mention_id', 'evidence'}
            or b.get('kind') != 'death_then_explicit_gift' or holding.get('mode') != 'posthumous_grant'
            or holding.get('kind') != 'office' or not b.get('evidence')
            or b['evidence'] != holding.get('evidence')
            or b['evidence'] != holding.get('effective_period', {}).get('start', {}).get('evidence')):
        return False
    death, grant = b.get('death_term'), b.get('grant_term')
    if (not isinstance(death, str) or not any(x in death for x in ['卒', '薨', '死'])
            or not isinstance(grant, str) or not grant.startswith('贈')
            or holding.get('title') not in grant[1:].split('、')):
        return False
    recipient = mentions.get(b.get('recipient_person_mention_id'))
    if not recipient or recipient[2].get('person_id') != holding.get('person_id'):
        return False
    for e in b['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if (not hit or recipient[1] != e.get('paragraph_id') or e.get('person_mention_id') != recipient[2]['id']
                or hit[1].get('text_layer') != 'received_chapter' or e.get('quote') != hit[1]['text']
                or b.get('source_term') != e['quote']):
            return False
        text = e['quote']
        if text.count(death) != 1 or text.count(grant) != 1:
            return False
        d, g = text.index(death), text.index(grant)
        before = [m for m in hit[1].get('mentions', []) if m.get('kind') == 'person' and m['end'] <= d]
        if (recipient[2]['end'] > d or d + len(death) > g or not before
                or max(before, key=lambda m: m['end'])['person_id'] != holding['person_id']):
            return False
        if not any(a.get('paragraph_id') == e['paragraph_id'] and a.get('person_mention_id') == recipient[2]['id']
                   and a.get('surface') == holding['title'] and g < a.get('start', -1) < g + len(grant)
                   for a in holding.get('attestations', [])):
            return False
    return True
