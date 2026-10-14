"""生卒紀年取捨只套用已存決定；原始事件與數字換年各自保留。"""


def date_decision_errors(decision, events, equivalences, people):
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    required = {'id', 'person_ids', 'event_type', 'candidate_event_ids', 'preferred_event_id',
                'status', 'rationale', 'evidence', 'reviewer', 'human_reviewed', 'model'}
    if not isinstance(decision, dict) or set(decision) != required:
        return ['生卒紀年取捨欄位不完整']
    ids = decision['person_ids']; candidates = decision['candidate_event_ids']
    valid_ids = isinstance(ids, list) and bool(ids) and len(set(ids)) == len(ids) and set(ids).issubset(people)
    valid_candidates = (isinstance(candidates, list) and len(candidates) >= 2
                        and len(set(candidates)) == len(candidates) and set(candidates).issubset(events))
    check(valid_ids and valid_candidates, '生卒紀年取捨人物或事件端點無效')
    if not valid_ids or not valid_candidates: return errors
    connected = {ids[0]}
    while True:
        expanded = connected | {pid for eq in equivalences if connected.intersection(eq['person_ids']) for pid in eq['person_ids']}
        if expanded == connected: break
        connected = expanded
    check(set(ids).issubset(connected), '生卒紀年取捨不得跨未判同指人物')
    selected = [events[eid] for eid in candidates]
    check(decision['event_type'] in ('birth', 'death')
          and all(e['event_type'] == decision['event_type'] and e['person_id'] in ids for e in selected)
          and {e['person_id'] for e in selected} == set(ids), '生卒紀年取捨事件種類或人物不符')
    dates = [e.get('normalized_date') for e in selected]
    check(all(isinstance(d, dict) and type(d.get('year')) is int for d in dates)
          and len({d['year'] for d in dates if isinstance(d, dict) and 'year' in d}) >= 2,
          '生卒紀年取捨须有不同的已存數字換年'.replace('须', '須'))
    check((decision['status'] == 'editorial_provisional' and decision['preferred_event_id'] in candidates)
          or (decision['status'] == 'unresolved' and decision['preferred_event_id'] is None),
          '生卒紀年取捨預設須屬候選；未解不得選定')
    check(decision['evidence'] == [evidence for e in selected for evidence in e['evidence']],
          '生卒紀年取捨須完整保留各候選事件證據')
    check(bool(decision['id']) and bool(decision['rationale']) and bool(decision['reviewer'])
          and decision['human_reviewed'] is False
          and (decision['model'] is None or isinstance(decision['model'], str)), '生卒紀年取捨缺判讀與覆核狀態')
    return errors


def selected_dates(events, decisions):
    """未解決定無選定日期；本函數不為未審閱的其他事件猜預設。"""
    by_id = {e['id']: e for e in events}
    selected = []
    for d in decisions:
        if d['status'] != 'editorial_provisional': continue
        e = by_id[d['preferred_event_id']]
        selected.append(dict(e['normalized_date'], record_id=e['id'], person_id=e['person_id'],
                             date_role='life_event', event_type=e['event_type'], selection_decision_id=d['id']))
    return selected
