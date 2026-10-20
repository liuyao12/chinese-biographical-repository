"""生卒紀年取捨只套用已存決定；原始事件與數字換年各自保留。"""

import copy
from urllib.parse import urlsplit
try:
    from .date_ranges import year_range_errors, parallel_event_date
except ImportError:
    from date_ranges import year_range_errors, parallel_event_date


def date_window(event):
    """Compare recorded year bounds; never select an endpoint of a range."""
    point = event.get('normalized_date')
    window = event.get('normalized_date_range')
    if (point is None) == (window is None):
        return None
    if point is not None:
        year = point.get('year') if isinstance(point, dict) else None
        return (year, year) if type(year) is int else None
    if not isinstance(window, dict):
        return None
    expression = event.get('date_expression')
    if 'parallel_event' in window:
        if expression is not None or not parallel_event_date(dict(window, basis=window['parallel_event'])):
            return None
        expression = window['parallel_event']['source_event_quote']
    if year_range_errors(window, event.get('evidence', []), expression):
        return None
    return window['earliest']['year'], window['latest']['year']


def date_decision_errors(decision, events, equivalences, people):
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    required = {'id', 'person_ids', 'event_type', 'candidate_event_ids', 'preferred_event_id',
                'status', 'rationale', 'evidence', 'reviewer', 'human_reviewed', 'model'}
    if (not isinstance(decision, dict) or not required.issubset(decision)
            or not set(decision).issubset(required | {'references', 'comparison_scope'})):
        return ['生卒紀年取捨欄位不完整']
    if 'references' in decision:
        refs = decision['references']
        def valid_reference(ref):
            if not isinstance(ref, dict):
                return False
            try:
                url = urlsplit(ref.get('url', ''))
                link_ok = url.scheme in ('http', 'https') and bool(url.hostname)
            except (TypeError, ValueError):
                return False
            return (link_ok and all(isinstance(ref.get(k), str) and ref[k].strip()
                                  for k in ('title', 'quote', 'scope'))
                    and type(ref.get('image_verified')) is bool)
        check(isinstance(refs, list) and bool(refs) and all(valid_reference(r) for r in refs),
              '生卒紀年取捨參考須有來源連結、引文、範圍及書影核驗狀態')
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
    windows = [date_window(e) for e in selected]
    if decision.get('comparison_scope') == 'source_calendar_day':
        try:
            from scripts.song041_source_context import same_year_birth_day_conflict_valid
        except ImportError:
            from song041_source_context import same_year_birth_day_conflict_valid
        check(same_year_birth_day_conflict_valid(decision, selected, windows), '同年生日異說只保兩則明示不同原月日，未解不得任選')
    else:
        check('comparison_scope' not in decision, '未知日期比較範圍')
        check(all(w is not None for w in windows)
              and len({w for w in windows if w is not None}) >= 2,
              '生卒紀年取捨須有不同的已存數字換年')
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
        if date_window(e) is None:
            raise ValueError('已選生卒紀年缺有效單年或範圍，不得補定端點')
        date = e.get('normalized_date') or e['normalized_date_range']
        selected.append(dict(copy.deepcopy(date), record_id=e['id'], person_id=e['person_id'],
                             date_role='life_event', event_type=e['event_type'], selection_decision_id=d['id']))
    return selected


def date_record_scope_errors(record, chapters, works):
    """A cross-work choice declares its evidence works; it never rewrites them."""
    declared = record.get('work_ids', [record.get('work_id')])
    if (not isinstance(declared, list) or not declared
            or not all(isinstance(w, str) for w in declared)
            or len(set(declared)) != len(declared)
            or not set(declared).issubset(works) or record.get('work_id') not in declared):
        return ['生卒紀年取捨著作範圍無效']
    evidence = [e for d in record.get('decisions', []) for e in d.get('evidence', [])]
    actual = {chapters.get(e.get('chapter_id'), {}).get('work_id') for e in evidence}
    if (actual != set(declared)
            or any(e.get('work_id', chapters.get(e.get('chapter_id'), {}).get('work_id'))
                   != chapters.get(e.get('chapter_id'), {}).get('work_id') for e in evidence)):
        return ['生卒紀年取捨證據著作不符']
    return []
