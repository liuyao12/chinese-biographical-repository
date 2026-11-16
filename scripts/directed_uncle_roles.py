"""叔侄端點依原文角色詞定向；不建立未知父親或改動來源。"""
import re


def _mentions(p, person):
    return [m for m in p.get('mentions', []) if m.get('kind') == 'person'
            and m.get('person_id') == person and type(m.get('start')) is int
            and type(m.get('end')) is int and 0 <= m['start'] < m['end'] <= len(p['text'])
            and p['text'][m['start']:m['end']] == m.get('surface')]


def _biographical_head(p, marks):
    return any(m['start'] == 0 and re.match(r'[，,]?(字|者[，,]|立|[^，。；曰]{1,12}人也祖)', p['text'][m['end']:])
               for m in marks)


def _resumed_child_elder_uncle(p, subjects, objects, term):
    """完整子傳的字名開頭與服喪段復見其名，雙重綁定伯父，不能跨轉主體。"""
    t = p['text']
    for head in subjects:
        if head['surface'] in ('其', '我', '吾', '臣', '父', '子', '弟', '兄'):
            continue
        if not t[head['end']:].startswith('字'):
            continue
        prefix = t[:head['start']]
        if prefix and not re.fullmatch(r'子[^曰。；！？「」『』]{1,12}有名於世', prefix):
            continue
        for obj in objects:
            a = obj['start'] - len('伯父')
            if a < head['end'] or t[a:obj['start']] != '伯父':
                continue
            if term != '伯父' + obj['surface'] + '每譬止之':
                continue
            # A named biography child resumes immediately after the uncle's
            # admonition. The nearby mourning clause remains the same subject;
            # another named person or quoted speech invalidates that binding.
            resumed = [m for m in subjects if m['start'] == obj['end'] + len('每譬止之')]
            if not resumed or not t[obj['end']:resumed[0]['start']].startswith('每譬止之'):
                continue
            local = t.rfind('未拜父在', head['end'], a)
            if local < 0:
                continue
            between = t[local:a]
            if not re.fullmatch(r'未拜父在[^曰。；！？「」『』]{1,12}亡成服[^曰。；！？「」『』]{1,16}𦵏畢[^曰。；！？「」『』]{1,20}遂[^曰。；！？「」『』]{1,12}', between):
                continue
            if any(m.get('kind') == 'person' and m.get('person_id') != head.get('person_id')
                   and local <= m.get('start', -1) < a for m in p.get('mentions', [])):
                continue
            return True
    return False


def _direction(p, subjects, objects, term):
    t = p['text']
    if _resumed_child_elder_uncle(p, subjects, objects, term):
        return True
    # A paragraph resumes its named subject, gives descriptive clauses, then
    # directly coordinates 與叔父某. No other marked person or quoted speech
    # may intervene; the named uncle must immediately follow the literal role.
    for role in ('叔父', '伯父', '季父'):
        for hit in re.finditer(role, t):
            a, b = hit.span()
            for subject in subjects:
                if subject['start'] != 0 or subject['surface'] in ('其', '我', '吾', '臣', '父', '子', '弟', '兄'):
                    continue
                between = t[subject['end']:a]
                if not re.fullmatch(r'[^。；！？「」『』]{0,80}與', between):
                    continue
                if any(m.get('kind') == 'person' and m.get('person_id') != subject.get('person_id')
                       and subject['end'] <= m.get('start', -1) < a for m in p.get('mentions', [])):
                    continue
                for obj in objects:
                    if obj['start'] == b and term == role + obj['surface'] and obj['surface'] not in ('其', '我', '吾', '臣'):
                        return True
    # Explicit child + uncle role + named uncle, allowing transmitted rank/title
    # words between the role and the already marked uncle name.
    for role in ('叔父', '伯父', '季父', '叔'):
        for hit in re.finditer(role, t):
            a, b = hit.span()
            for obj in objects:
                name_start = obj['start'] + len(role) if obj['start'] == a and obj['surface'].startswith(role) else obj['start']
                if name_start < b or name_start - b > 16:
                    continue
                gap = t[b:name_start]
                if any(c in gap for c in '，。；：、曰云也') or '兄子' in gap:
                    continue
                if role not in term or not (term in t[max(0, a-len(term)):obj['end']] or term == role):
                    continue
                # A local named child (not the nearest arbitrary marked person),
                # the biography's attested opening, or explicit 其季父 scope.
                for subject in subjects:
                    between = t[subject['end']:a]
                    if subject['end'] <= a and (
                            between in ('', '之', '謂', '隨', '初繼', '出繼', '之郡以其', '三年，以其')
                            or re.fullmatch(r'年[一二三四五六七八九十百]+疑之謂', between)
                            or (_biographical_head(p, subjects) and subject['start'] == 0)
                            or (role == '季父' and between.endswith('其')
                                and _biographical_head(p, subjects))
                            or (role == '季父' and re.fullmatch(r'大父行[^，。；]+[，,]生捕', between))):
                        return True
    # Copular inverse order: uncle ... child 季父也 / uncle child 叔.
    for s in subjects:
        for o in objects:
            tail = t[s['end']:]
            if o['end'] <= s['start'] and t[o['end']:s['start']] in ('', '者，', '者,'):
                if tail.startswith(('季父也', '叔父也', '叔')) and any(r in term for r in ('季父', '叔')):
                    return True
    try:
        from scripts.inverse_paternal_uncle import inverse_uncle_direction
    except ImportError:
        from inverse_paternal_uncle import inverse_uncle_direction
    if inverse_uncle_direction(p, subjects, objects, term):
        return True
    # A named speaker explicitly says "child之叔父". Bind the uncle to the
    # speaker before 曰 and to 我, rather than an unrelated earlier name.
    for s in subjects:
        if t[s['end']:].startswith('之叔父') and s['surface'] + '之叔父' == term:
            for o in objects:
                segment = t[o['end']:s['start']]
                if o['end'] < s['start'] and re.fullmatch(r'戒[^曰]{1,12}曰：[『「]我[^』」]+', segment):
                    return True
    # Brother's child lists: the child is in the actual role/list span. The
    # uncle is explicit immediately before it, the biography subject, or the
    # source's first-person speaker (not an arbitrary same-paragraph person).
    for hit in re.finditer(r'兄子|弟子|昆弟子', t):
        a, b = hit.span()
        if hit[0] not in term and not (hit[0] == '兄子' and term == '兄子'):
            continue
        # Named/courtesy paired lists have their own literal boundary; do not
        # let an unrelated later child occurrence satisfy a role.
        end = b
        while end < len(t) and t[end] not in '，。；其並為母於在等':
            end += 1
        for s in subjects:
            contained = (a <= s['start'] < end or s['start'] <= a < s['end'])
            if not contained:
                continue
            for o in objects:
                if (o['end'] == a or (s['start'] == a - len(o['surface']) and s['surface'].startswith(o['surface'] + hit[0]))
                        or (o['end'] < a and t[o['end']:a] in ('乃使', '為'))
                        or (_biographical_head(p, objects) and o['start'] == 0)
                        or (o['surface'] in ('其', '臣', '吾', '我') and o['end'] < a
                            and (o['surface'] == '其' and '其為兄子及子作名字' in t[:a]
                                 or o['surface'] == '臣' and '臣' in t[:a] and '云：「' not in t[o['end']:a]))):
                    return True
            # Third-person biography with an earlier explicitly named subject
            # resumes after a quotation; require the named uncle before and
            # after the child, and an explicit personal-name opening sentence.
            for o in objects:
                if (o['end'] < a and o['surface'] not in ('其', '臣', '吾', '我')
                        and t.startswith('兄') and any(x['start'] > s['end'] for x in objects)
                        and t[o['end']:a].endswith('太守')):
                    return True
    # "uncle 弟子也" names the uncle before a biographical child opening.
    for o in objects:
        if t[o['end']:].startswith('弟子也') and '弟子也' in term and _biographical_head(p, subjects):
            return True
    return False


def paternal_uncle_direction_valid(assertion, paragraphs):
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('rule') == 'complete_received_kinship_unit':
        try:from scripts.received_unit_kinship import valid as unit_relation_valid
        except ImportError:from received_unit_kinship import valid as unit_relation_valid
        return unit_relation_valid(assertion, paragraphs)
    if 'source_uncle_ordinal' in assertion.get('qualifiers', {}):
        try:from scripts.fixed_wikisource_units import ordinal_uncle_valid
        except ImportError:from fixed_wikisource_units import ordinal_uncle_valid
        return ordinal_uncle_valid(assertion, paragraphs)
    if assertion.get('qualifiers', {}).get('source_clause_binding', {}).get('kind') == 'biography_head_named_uncle_xiongzi':
        try:
            from scripts.song059_kinship import inverse_xiongzi_valid
        except ImportError:
            from song059_kinship import inverse_xiongzi_valid
        return inverse_xiongzi_valid(assertion, paragraphs)
    if assertion.get('predicate') != 'paternal_uncle' or not assertion.get('evidence'):
        return False
    for e in assertion['evidence']:
        hit = paragraphs.get(e.get('paragraph_id'))
        if not hit or hit[0] != e.get('chapter_id'):
            return False
        p = hit[1]; term = assertion.get('qualifiers', {}).get('source_term')
        quote = e.get('quote')
        if not isinstance(term, str) or not term or term not in p['text'] or not quote or quote not in p['text']:
            return False
        subjects = _mentions(p, assertion.get('subject_person_id'))
        objects = _mentions(p, assertion.get('object_person_id'))
        # References may intentionally select the first full-name occurrence;
        # the same canonical person's local name is valid grammatical evidence.
        for role, marks in (('subject', subjects), ('object', objects)):
            ref = e.get(role + '_person_mention_id')
            if ref is not None and not any(m['id'] == ref for m in marks):
                return False
        if (not subjects or not objects or assertion['subject_person_id'] == assertion['object_person_id']
                or not _direction(p, subjects, objects, term)):
            return False
    return True
