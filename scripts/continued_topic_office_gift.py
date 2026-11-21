"""Bind the unexpressed recipient of a coordinated posthumous office award."""
try:
    from scripts.subject_continuation import title_attestation_subject_valid, prior_subject_valid
except ImportError:
    from subject_continuation import title_attestation_subject_valid, prior_subject_valid


def valid(holding, paragraphs, mentions, events):
    try:
        basis = holding['posthumous_basis']
        if set(basis) != {'kind','source_term','death_term','death_event_id','evidence'} or basis['kind'] != 'continued_topic_named_offices_after_death':
            return False
        evidence, = basis['evidence']
        record, = holding['attestations']
        start = holding['effective_period']['start']
        if (holding['mode'] != 'posthumous_grant' or holding['kind'] != 'office' or holding['status'] != 'source_attested'
            or basis['evidence'] != holding['evidence'] or start != dict(status='source_event',event_type='posthumous_grant', date_expression=None,evidence=basis['evidence'])):
            return False
        chapter_id, paragraph = paragraphs[evidence['paragraph_id']]
        ordered = [p for cid,p in paragraphs.values() if cid == chapter_id]
        chapter = dict(id=chapter_id, source_id=evidence['source_id'],paragraphs=ordered)
        text = paragraph['text']
        if (paragraph['text_layer'] != 'received_chapter' or paragraph['source_position']['revision_id'] != 1752646
            or evidence['quote'] != text or basis['source_term'] != '其年薨。贈太保、中書監' or basis['death_term'] != '薨'
            or text.count(basis['source_term']) != 1 or not text.startswith('九年進位太保，領中書監，餘如故。' + basis['source_term'] + '，')
            or holding['title'] not in ('太保','中書監') or paragraph['mentions'] or ordered[0]['mentions'][0]['person_id'] != holding['person_id']):
            return False
        prior = mentions[evidence['person_mention_id']]
        if prior[2]['surface'] != '弘' or ordered[0]['mentions'][0]['surface'] != '王弘' or prior[2]['person_id'] != holding['person_id']:
            return False
        event = events[basis['death_event_id']]
        death_evidence, = event['evidence']
        if (event['person_id'] != holding['person_id'] or event['event_type'] != 'death' or event['status'] != 'source_attested'
            or event['source_term'] != basis['death_term'] or event['source_anchor']['start'] != text.index(basis['source_term'])+2
            or death_evidence['paragraph_id'] != paragraph['id'] or death_evidence['quote'] != text or death_evidence['person_mention_id'] != prior[2]['id']
            or not prior_subject_valid(death_evidence['context'], death_evidence, holding['person_id'], chapter)):
            return False
        position = text.index(holding['title'], text.index('。贈')+2)
        return (record['start'] == position and record['end'] == position+len(holding['title']) and record['surface'] == holding['title']
                and record['usage'] == 'posthumous_usage' and title_attestation_subject_valid(record,holding,chapter))
    except (KeyError, TypeError, ValueError, IndexError):
        return False
