# coding: utf-8
"""Bind an explicitly stated royal transfer to its source and prior holding."""

def royal_transfer_errors(holding, holdings, paragraphs, mentions):
    basis = holding.get('transfer_basis')
    keys = {'previous_holding_id', 'source_term', 'title_source_term', 'actor_mention_id', 'evidence'}
    if not isinstance(basis, dict) or set(basis) != keys:
        return ['徙王須明示前王號、原詞、人物錨點及同次來源']
    previous = holdings.get(basis['previous_holding_id'])
    start = holding.get('effective_period', {}).get('start', {})
    if not (holding.get('mode') == 'transfer' and holding.get('kind') == 'royal_rank'
            and previous and previous.get('id') != holding.get('id')
            and previous.get('person_id') == holding.get('person_id') and previous.get('kind') == 'royal_rank'
            and previous.get('mode') not in ('posthumous_grant', 'posthumous_naming')
            and start.get('status') == 'source_event' and start.get('event_type') == 'transfer'
            and basis.get('evidence') == start.get('evidence') and bool(basis['evidence'])):
        return ['徙王須指同人的原王號與明示徙封起點，不得當繼位或跨人移接']
    old_end = previous.get('effective_period', {}).get('end', {})
    if not (old_end.get('status') == 'source_event' and old_end.get('event_type') == 'explicit_end'
            and old_end.get('evidence') == basis['evidence']
            and all(old_end.get(k) == start.get(k) for k in ('date_expression', 'normalized_date', 'normalized_date_range'))):
        return ['徙王新始與前號明示終點須為同一事件與同一日期，不得借死亡補終期']
    term, title_term = basis.get('source_term'), basis.get('title_source_term')
    nominal = (isinstance(term, str) and isinstance(title_term, str)
               and title_term == holding['title'] and '徙為' + title_term in term)
    places = holding.get('jurisdictions', [])
    predicative = (holding.get('title') == '王' and isinstance(places, list) and len(places) == 1
                   and isinstance(places[0], dict) and isinstance(places[0].get('source_name'), str)
                   and title_term == '王' + places[0]['source_name'] and isinstance(term, str)
                   and '徙' + previous['title'] + title_term in term)
    if not (nominal or predicative) or previous['title'] == holding['title'] and previous.get('jurisdictions') == holding.get('jurisdictions'):
        return ['徙王原詞須明言新王號或王某地，不得由任意地名重排稱號']
    anchor = mentions.get(basis.get('actor_mention_id'))
    if not (anchor and anchor[2].get('kind') == 'person'
            and anchor[2].get('person_id') == holding['person_id'] and anchor[2].get('surface') == previous['title']):
        return ['徙王人物錨點須指同人的原王號']
    for evidence in basis['evidence']:
        hit = paragraphs.get(evidence.get('paragraph_id'))
        if not hit or anchor[1] != evidence.get('paragraph_id'):
            return ['徙王人物與引句段落不符']
        text = hit[1]['text']; quote = evidence.get('quote')
        starts = [i for i in range(len(text)) if text.startswith(term, i)]
        eligible = [i for i in starts if i <= anchor[2]['start'] < anchor[2]['end'] <= i + len(term)]
        if not (isinstance(quote, str) and quote in text and term in quote and eligible
                and any(not any(m.get('kind') == 'person' and m.get('person_id') != holding['person_id']
                                and i <= m['start'] < i + len(term) for m in hit[1]['mentions']) for i in eligible)):
            return ['徙王原詞須包含原王錨點，不得跨另一人物拼接授任']
    seen = {holding['id']}; cursor = previous
    while cursor:
        if cursor['id'] in seen:
            return ['徙王前職引用不得循環']
        seen.add(cursor['id']); cursor = holdings.get(cursor.get('transfer_basis', {}).get('previous_holding_id'))
    return []
