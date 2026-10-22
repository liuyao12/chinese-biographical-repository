# coding: utf-8
"""Validate explicit, source-local shortened work-title references; no NLU."""
def chapter_errors(chapter):
    errors = []
    ps = chapter.get('paragraphs', [])
    pids = [p.get('id') for p in ps]
    mids = {m.get('id'): (i, m) for i, p in enumerate(ps) for m in p.get('mentions', [])}
    for i, p in enumerate(ps):
        for m in p.get('mentions', []):
            if 'work_reference_resolution' not in m:
                continue
            r = m['work_reference_resolution']
            prefix = str(m.get('id')) + ': 書名簡稱回指'
            if not isinstance(r, dict) or set(r) != {'kind', 'antecedent_mention_id', 'scope_paragraph_ids', 'reason'}:
                errors.append(prefix + '欄位無效'); continue
            scope = r.get('scope_paragraph_ids'); a = mids.get(r.get('antecedent_mention_id'))
            if (m.get('kind') != 'work' or m.get('person_id') is not None
                    or m.get('status') != 'contextual_provisional' or r.get('kind') != 'shortened_title'
                    or not isinstance(r.get('reason'), str) or not r['reason'].strip()
                    or not isinstance(scope, list) or len(scope) < 1
                    or not all(isinstance(v, str) and v in pids for v in scope)
                    or len(set(scope)) != len(scope) or a is None):
                errors.append(prefix + '端點／作用域無效'); continue
            indices = [pids.index(v) for v in scope]
            ai, am = a
            if (indices != list(range(indices[0], indices[-1] + 1)) or i not in indices or ai not in indices
                    or am.get('kind') != 'work' or am.get('person_id') is not None
                    or am.get('work_id') != m.get('work_id')
                    or am.get('status') != 'source_explicit' or 'work_reference_resolution' in am
                    or not (ai < i or ai == i and am.get('end', -1) <= m.get('start', -1))
                    or not isinstance(m.get('surface'), str) or not isinstance(am.get('surface'), str)
                    or not (0 < len(m['surface']) < len(am['surface']))
                    or m['surface'] not in am['surface']):
                errors.append(prefix + '先行書名或順序無效'); continue
            earlier = [(j, other) for j in indices for other in ps[j].get('mentions', [])
                       if other.get('kind') == 'work' and other.get('work_id') == m.get('work_id')
                       and (j < ai or j == ai and other.get('start', -1) < am.get('start', -1))]
            if earlier:
                errors.append(prefix + '先行詞不是所宣告作用域內首見')
    return errors
