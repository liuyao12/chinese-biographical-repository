"""An explicit noble-rank change may leave the former title unidentified."""


def noble_transfer_errors(holding, holdings, paragraphs, mentions, chapters=None):
    basis = holding.get('transfer_basis')
    keys = {'kind', 'previous_holding_id', 'previous_title_status', 'source_term',
            'actor_mention_id', 'evidence', 'rationale', 'status', 'human_reviewed'}
    if not isinstance(basis, dict) or set(basis) != keys:
        return ['爵號改封須有明示改封原詞、人物錨點及前爵已知狀態']
    start = holding.get('effective_period', {}).get('start', {})
    anchor = mentions.get(basis.get('actor_mention_id'))
    title = holding.get('title')
    term = basis.get('source_term')
    valid = (holding.get('kind') == 'noble_rank' and holding.get('mode') == 'transfer'
             and basis.get('kind') == 'noble_rank_change'
             and basis.get('status') == 'editorial_provisional'
             and basis.get('human_reviewed') is False and bool(basis.get('rationale'))
             and isinstance(title, str) and title.endswith(('公', '侯', '伯', '子', '男'))
             and start.get('status') == 'source_event' and start.get('event_type') == 'transfer'
             and isinstance(basis.get('evidence'), list) and bool(basis['evidence'])
             and basis['evidence'] == start.get('evidence') and bool(anchor)
             and anchor[2].get('person_id') == holding.get('person_id'))
    if not valid:
        return ['爵號改封須屬同人明示爵位變更，不得借王號或官職轉任通過']
    if term not in tuple(v + t for v in ('改封', '更封', '徙封') for t in (title, anchor[2]['surface'] + title)):
        return ['爵號改封原詞與新爵或承敘人物不符']
    for e in basis['evidence']:
        if not isinstance(e, dict):
            return ['爵號改封證據須為原段引句']
        hit = paragraphs.get(e.get('paragraph_id'))
        carried = False
        if anchor[1] != e.get('paragraph_id') and chapters:
            try:
                from scripts.subject_continuation import title_attestation_subject_valid
            except ModuleNotFoundError:
                from subject_continuation import title_attestation_subject_valid
            chapter = chapters.get(e.get('chapter_id'))
            carried = bool(chapter) and any(
                a.get('paragraph_id') == e.get('paragraph_id')
                and a.get('person_mention_id') == basis.get('actor_mention_id')
                and title_attestation_subject_valid(a, holding, chapter)
                for a in holding.get('attestations', []))
        if (not hit or hit[0] != e.get('chapter_id') or (anchor[1] != e.get('paragraph_id') and not carried)
                or not isinstance(e.get('quote'), str) or term not in e['quote']
                or e['quote'] not in hit[1].get('text', '')
                or (not carried and anchor[2]['surface'] not in e['quote'])):
            return ['爵號改封與人物錨點須在同一實存原段']
    previous_id = basis.get('previous_holding_id')
    if previous_id is None:
        return [] if basis.get('previous_title_status') == 'not_identified' else ['前爵未名時不得標成已知']
    previous = holdings.get(previous_id)
    if (not previous or previous_id == holding.get('id')
            or previous.get('person_id') != holding.get('person_id')
            or previous.get('kind') != 'noble_rank'
            or previous.get('mode') in ('posthumous_grant', 'posthumous_enfeoffment', 'posthumous_naming')
            or basis.get('previous_title_status') != 'source_context'):
        return ['已接前爵須屬同人實際爵位，不得借他人或死後諡號']
    end = previous.get('effective_period', {}).get('end', {})
    if (end.get('status') != 'source_event' or end.get('event_type') != 'explicit_end'
            or end.get('evidence') != basis['evidence']
            or any(end.get(k) != start.get(k) for k in ('date_expression', 'normalized_date', 'normalized_date_range'))):
        return ['改封新始與已接前爵終點須同證同日，不以死亡補終點']
    return []
