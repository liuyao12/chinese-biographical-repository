"""Narrow literal mother clauses; no biological, paternal, or marriage inference."""
def maternal_clause_valid(a, paragraphs):
    try:
        q = a['qualifiers']; e, = a['evidence']; cid, p = paragraphs[e['paragraph_id']]
        t = p['text']; ms = {m['id']: m for m in p['mentions']}
        s = ms[e['subject_person_mention_id']]; o = ms[e['object_person_mention_id']]
        b = q['maternal_clause']; start, end = b['start'], b['end']; term = q['source_term']
        if (set(q) != {'source_term','role','biological_mother','father_person_id','maternal_clause'}
                or set(b) != {'kind','start','end'} or a['predicate'] != 'maternal_role'
                or a.get('status') != 'source_attested' or a.get('human_reviewed') is not False
                or q['role'] != 'mother_unspecified' or q['biological_mother'] is not None
                or q['father_person_id'] is not None or e['chapter_id'] != cid or e['quote'] != t
                or s['kind'] != 'person' or o['kind'] != 'person'
                or s['person_id'] != a['subject_person_id'] or o['person_id'] != a['object_person_id']
                or s['person_id'] == o['person_id'] or type(start) is not int or type(end) is not int
                or not 0 <= start < end <= len(t) or t[start:end] != term):
            return False
        for m in [s,o]:
            if (type(m['start']) is not int or type(m['end']) is not int
                    or not 0 <= m['start'] < m['end'] <= len(t)
                    or t[m['start']:m['end']] != m['surface']):
                return False
        kind = b['kind']
        if kind == 'opening_grandchild_mother':
            ancestor = next((m for m in p['mentions'] if m.get('kind') == 'person'
                            and m['start'] == s['end'] and m['end'] < o['start']), None)
            return (s['start'] == 0 and ancestor is not None
                    and ancestor['person_id'] not in (s['person_id'],o['person_id'])
                    and t[ancestor['start']:ancestor['end']] == ancestor['surface']
                    and t[ancestor['end']:o['start']] == '孫也母'
                    and term == '母' + o['surface'] and start == o['start'] - 1 and end == o['end'])
        if kind == 'named_child_yisui_mother':
            return (o['surface'] == '母' and s['end'] < o['start']
                    and t[s['end']:o['start']] == '亦隨'
                    and term == s['surface'] + '亦隨母' and start == s['start'] and end == o['end'])
        if kind == 'named_child_xianwei_qimu':
            return (t[s['end']:o['start']] == '賢謂其母'
                    and term == '其母' + o['surface'] and start == o['start'] - 2 and end == o['end'])
        if kind == 'named_child_selfinjury_qimu_calls':
            return (o['surface'] == '母'
                    and t[s['end']:o['start']] == '於是竊入寢室以刀斷鼻䝉被而卧其'
                    and t[o['end']:o['end']+5] == '呼與語不應'
                    and term == '其母呼與語' and start == o['start'] - 1 and end == o['end'] + 3)
        return False
    except (KeyError, TypeError, ValueError, StopIteration):
        return False
