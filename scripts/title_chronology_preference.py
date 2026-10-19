# coding: utf-8
"""A local preference preserves both sourced dates for the same title event."""


def title_chronology_preference_valid(holding, holdings):
    p = holding.get('chronology_preference', {})
    ids = p.get('candidate_holding_ids')
    if (p.get('kind') != 'same_event_source_preference'
            or p.get('preferred_holding_id') != holding.get('id')
            or p.get('status') != 'editorial_provisional'
            or p.get('human_reviewed') is not False
            or not isinstance(p.get('rationale'), str) or not p['rationale'].strip()
            or not isinstance(ids, list) or len(ids) < 2
            or len(set(ids)) != len(ids) or holding['id'] not in ids):
        return False
    candidates = [holdings.get(i) for i in ids]
    if any(not h for h in candidates):
        return False
    normalize = lambda title: title.replace('鎭', '鎮')
    years, chapters = set(), set()
    for h in candidates:
        start = h.get('effective_period', {}).get('start', {})
        date = start.get('normalized_date', {})
        if (h.get('person_id') != holding.get('person_id')
                or h.get('kind') != holding.get('kind')
                or h.get('mode') != holding.get('mode')
                or h.get('mode') not in ['grant', 'posthumous_naming']
                or normalize(h.get('title', '')) != normalize(holding.get('title', ''))
                or start.get('status') != 'source_event'
                or start.get('event_type') != holding['mode']
                or type(date.get('year')) is not int or not h.get('evidence')):
            return False
        years.add(date['year'])
        chapters.update(e.get('chapter_id') for e in h['evidence'])
    return len(years) > 1 and len(chapters) == len(ids)
