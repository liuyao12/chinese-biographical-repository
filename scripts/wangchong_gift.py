"""Recognize the banquet host, subject, and following death notice in the received Wang Chong account."""
from hashlib import sha256


def valid(holding, paragraphs, mentions, events):
    try:
        basis = holding['posthumous_basis']
        evidence, = holding['evidence']
        event = events[basis['death_event_id']]
        chapter, paragraph = paragraphs[evidence['paragraph_id']]
        _, subject_paragraph, subject = mentions[basis['recipient_person_mention_id']]
        _, host_paragraph, host = mentions[basis['host_mention_id']]
        position = paragraph['source_position']
        text = paragraph['text']
        def bound(mark):
            return text[mark['start']:mark['end']] == mark['surface']
        scope = text[subject['start']:]
        return (chapter == 'c-nanshi-021-wangchong' and position['revision_id'] == 1752646
                and subject_paragraph == host_paragraph == paragraph['id'] and paragraph['text_layer'] == 'received_chapter'
                and basis['paragraph_sha256'] == sha256(text.encode()).hexdigest() and basis['source_term'] == text
                and evidence['quote'] == text and evidence['person_mention_id'] == subject['id']
                and holding['effective_period']['start']['evidence'] == basis['evidence'] == [evidence]
                and holding['kind'] == 'office' and holding['mode'] == 'posthumous_grant' and holding['title'] == '司空'
                and bound(subject) and subject['surface'] == '沖' and subject['person_id'] == event['person_id'] == holding['person_id']
                and bound(host) and host['surface'] == '徐度' and host['person_id'] != subject['person_id']
                and text[host['start']-2:host['end']+1] == '司空徐度宅'
                and scope == '沖前代舊臣，特申長幼之敬。文帝即位，益加尊重，嘗從幸司空徐度宅，宴筵之上，賜以幾。光大元年薨，年七十六，贈司空，諡曰元簡。'
                and event['event_type'] == 'death' and event['evidence'] == [evidence] and event['source_term'] == '薨'
                and event['source_anchor']['start'] == text.index('薨') and bound(event['source_anchor'])
                and all(a['start'] == text.index('贈司空') + 1 and a['paragraph_id'] == paragraph['id']
                        and a['person_mention_id'] == subject['id'] and a['surface'] == '司空'
                        and a['usage'] == 'posthumous_usage' and bound(a) for a in holding['attestations'])
                and len(holding['attestations']) == 1)
    except (KeyError, ValueError, TypeError, IndexError):
        return False
