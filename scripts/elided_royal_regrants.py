# coding: utf-8
"""明載更封之目的地省王字時，分存實際爵字與封地原詞。"""


def elided_royal_regrant_errors(holding, holdings, paragraphs, mentions):
    b = holding.get('transfer_basis', {})
    keys = {'kind', 'previous_holding_id', 'source_term', 'actor_mention_id',
            'rank_mention_id', 'realm_source_start', 'realm_source_end', 'evidence',
            'status', 'rationale', 'human_reviewed'}
    if (not isinstance(b, dict) or set(b) != keys or b.get('kind') != 'elided_rank_regrant'
            or holding.get('mode') != 'transfer' or holding.get('kind') != 'royal_rank'
            or holding.get('title') != '王' or b.get('status') != 'editorial_provisional'
            or b.get('human_reviewed') is not False or not b.get('rationale')):
        return ['省爵字更封須分存王字、目的地、同人錨點及編輯判讀']
    previous = holdings.get(b.get('previous_holding_id'))
    start = holding.get('effective_period', {}).get('start', {})
    end = previous.get('effective_period', {}).get('end', {}) if previous else {}
    actor, rank = mentions.get(b.get('actor_mention_id')), mentions.get(b.get('rank_mention_id'))
    places = holding.get('jurisdictions', [])
    if (not previous or previous.get('person_id') != holding.get('person_id')
            or previous.get('kind') != 'noble_rank' or previous.get('mode') not in ('grant', 'transfer')
            or not actor or not rank or actor[2].get('person_id') != holding.get('person_id')
            or rank[2].get('person_id') != holding.get('person_id')
            or not isinstance(places, list) or len(places) != 1
            or not isinstance(places[0], dict) or not isinstance(places[0].get('source_name'), str)
            or not places[0]['source_name'] or places[0].get('place_id') is not None
            or places[0].get('modern_identification') is not None
            or not b.get('evidence') or b['evidence'] != holding.get('evidence')
            or b['evidence'] != start.get('evidence') or b['evidence'] != end.get('evidence')
            or start.get('status') != 'source_event' or start.get('event_type') != 'transfer'
            or end.get('status') != 'source_event' or end.get('event_type') != 'explicit_end'
            or any(start.get(k) != end.get(k) for k in ('date_expression', 'normalized_date', 'normalized_date_range'))):
        return ['更封須接同人前爵及同證同日的新始舊終，不能借他人爵號或死亡']
    realm = places[0]['source_name']
    if b.get('source_term') != '更封' + actor[2]['surface'] + realm:
        return ['更封省爵字須保留原句，不得補造琅邪王等目的地字串']
    for e in b['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if (not hit or hit[1].get('text_layer') != 'received_chapter' or e.get('quote') != hit[1]['text']
                or actor[1] != e['paragraph_id'] or rank[1] != e['paragraph_id']
                or e.get('person_mention_id') != actor[2]['id']):
            return ['更封人物、王字與封地須在同一精確原段']
        text = e['quote'];term = b['source_term']
        if text.count(term) != 1:
            return ['更封原句不唯一或不在原段']
        g = text.index(term);rs = g + 2 + len(actor[2]['surface']);re = rs + len(realm)
        if (actor[2]['start'] != g + 2 or b['realm_source_start'] != rs or b['realm_source_end'] != re
                or text[rs:re] != realm or not rank[2]['surface'].startswith(realm)
                or not rank[2]['surface'].endswith('王' + actor[2]['surface']) or rank[2]['end'] > g):
            return ['王字原稱與省略爵字的目的地錨點不合']
        king_at = rank[2]['end'] - len(actor[2]['surface']) - 1
        if not any(a.get('person_mention_id') == rank[2]['id'] and a.get('paragraph_id') == e['paragraph_id']
                   and a.get('surface') == '王' and a.get('start') == king_at and a.get('end') == king_at + 1
                   and a.get('usage') == 'retrospective' and a.get('date_expression') is None
                   for a in holding.get('attestations', [])):
            return ['省略爵字須有原文實際王字用稱，含諡原稱不得作生前授諡']
    return []
