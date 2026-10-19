"""Validate a nearby omitted subject without manufacturing a textual name."""
import hashlib


def verified_blank_gap(chapter, before, after):
    """A fixed-witness extraction may omit blank source lines, never prose."""
    lo, hi = before.get("last_line"), after.get("first_line")
    if type(lo) is not int or type(hi) is not int or hi <= lo:
        return False
    if hi == lo + 1:
        return True
    gaps = chapter.get("source", {}).get("normalization", {}).get("verified_blank_line_gaps", [])
    for gap in gaps:
        if not isinstance(gap, dict) or set(gap) != {"source_lines", "raw_quote", "raw_quote_sha256", "revision_id"}:
            continue
        raw = gap.get("raw_quote")
        if (gap.get("source_lines") == [lo + 1, hi - 1]
                and gap.get("revision_id") == chapter.get("source", {}).get("revision_id")
                and isinstance(raw, str) and len(raw.split("\n")) == hi - lo - 1
                and all(ch in " \t\r\n\u3000" for ch in raw)
                and hashlib.sha256(raw.encode()).hexdigest() == gap.get("raw_quote_sha256")):
            return True
    return False


def prior_subject_valid(context, evidence, person_id, chapter):
    required = {'kind', 'paragraph_id', 'person_mention_id', 'quote', 'intervening_paragraph_ids'}
    if not isinstance(context, dict) or set(context) not in (required, required | {'source_continuity'}):
        return False
    order = [p['id'] for p in chapter.get('paragraphs', [])]
    before, target = context.get('paragraph_id'), evidence.get('paragraph_id')
    ids = context.get('intervening_paragraph_ids')
    if (context.get('kind') != 'prior_paragraph_subject' or before not in order or target not in order
            or not isinstance(ids, list) or len(ids) > 1
            or order.index(target) - order.index(before) != len(ids) + 1
            or ids != order[order.index(before) + 1:order.index(target)]
            or evidence.get('chapter_id') != chapter.get('id') or evidence.get('source_id') != chapter.get('source_id')):
        return False
    paras = chapter['paragraphs'][order.index(before):order.index(target) + 1]
    positions = [p.get('source_position', {}) for p in paras]
    if (all(p.get('editorial_excerpt_boundary') is True for p in positions)
            and any(type(p.get('first_line')) is not int or type(p.get('last_line')) is not int
                    or p['first_line'] > p['last_line'] for p in positions)):
        return False
    if all(p.get('editorial_excerpt_boundary') is True for p in positions):
        if 'source_continuity' in context:
            if len(paras) != 2 or not shared_line_subject_bridge(chapter, paras[0], paras[1], context, person_id):
                return False
        elif any(not verified_blank_gap(chapter, a, b) for a, b in zip(positions, positions[1:])):
            return False
    elif 'source_continuity' in context:
        return False
    p = paras[0]
    m = next((m for m in p.get('mentions', []) if m.get('id') == context.get('person_mention_id')), None)
    quote = context.get('quote')
    return (bool(m) and m.get('kind') == 'person' and m.get('person_id') == person_id
            and isinstance(quote, str) and bool(quote)
            and any(i <= m['start'] < m['end'] <= i + len(quote)
                    for i in range(len(p['text'])) if p['text'].startswith(quote, i)))


def title_attestation_subject_valid(attestation, holding, chapter):
    """Keep a title's actual location and its preceding named subject separate."""
    context = attestation.get('context')
    if (not isinstance(context, dict)
            or set(context) != {'kind', 'paragraph_id', 'person_mention_id', 'quote'}
            or context.get('kind') != 'previous_paragraph_subject'
            or attestation.get('person_mention_id') != context.get('person_mention_id')):
        return False
    for evidence in holding.get('evidence', []):
        if (evidence.get('paragraph_id') != attestation.get('paragraph_id')
                or evidence.get('context') != context):
            continue
        carried = dict(context, kind='prior_paragraph_subject', intervening_paragraph_ids=[])
        if prior_subject_valid(carried, evidence, holding.get('person_id'), chapter):
            return True
    return False


def shared_line_subject_bridge(chapter, before, after, context, person_id):
    """Opt-in continuation across two exact adjacent fragments of one source line.

    Same line numbers alone prove nothing. Both entire extraction units, their
    shared-line offsets and an explicit named resumption are independently bound.
    """
    try:
        proof = context['source_continuity']
        if set(proof) != {'kind', 'source_revision', 'boundary_raw_line', 'target_prefix_anchor', 'target_resumption_mention_id', 'subject_person_id', 'human_reviewed'}:
            return False
        if (proof['kind'] != 'same_raw_line_nonoverlapping_fragments'
                or proof['subject_person_id'] != person_id or proof['human_reviewed'] is not False
                or proof['source_revision'] != chapter['source']['revision_id']):
            return False
        units = chapter['source']['normalization']['selected_source_line_units']
        a = next(u for u in units if u['proposed_paragraph_id'] == before['id'])
        b = next(u for u in units if u['proposed_paragraph_id'] == after['id'])
        if units.index(b) != units.index(a) + 1 or a['body_end'] != b['body_start']:
            return False
        for u, p in [(a, before), (b, after)]:
            if (u['text'] != p['text'] or u['text_sha256'] != hashlib.sha256(p['text'].encode()).hexdigest()
                    or u['body_end'] - u['body_start'] != len(p['text'])
                    or ''.join(f['selected_text'] for f in u['source_fragments']) != p['text']):
                return False
            for f in u['source_fragments']:
                if (hashlib.sha256(f['raw_line_text'].encode()).hexdigest() != f['raw_line_sha256']
                        or type(f['source_start']) is not int or type(f['source_end']) is not int
                        or not 0 <= f['source_start'] < f['source_end'] <= len(f['raw_line_text'])
                        or f['raw_line_text'][f['source_start']:f['source_end']] != f['selected_text']):
                    return False
        left, right = a['source_fragments'][-1], b['source_fragments'][0]
        line = proof['boundary_raw_line']
        if (type(line) is not int or before['source_position']['last_line'] != line
                or after['source_position']['first_line'] != line
                or left['raw_line'] != right['raw_line'] or line != left['raw_line']
                or left['raw_line_text'] != right['raw_line_text']
                or left['source_end'] != right['source_start']):
            return False
        prefix = proof['target_prefix_anchor']; text = after['text']
        if (set(prefix) != {'paragraph_id','start','end','surface'} or prefix['paragraph_id'] != after['id']
                or prefix['start'] != 0 or type(prefix['end']) is not int or not 0 < prefix['end'] <= len(text)
                or text[:prefix['end']] != prefix['surface']):
            return False
        named = [m for m in after['mentions'] if m.get('kind') == 'person']
        resumed = next(m for m in named if m['id'] == proof['target_resumption_mention_id'])
        # The event prefix must contain no competing named subject. Resumption is
        # explicit and first, not a nearest-person search or a biography heading.
        if (not named or resumed != min(named, key=lambda m: m['start'])
                or resumed.get('person_id') != person_id or resumed['start'] < prefix['end']
                or any(m['start'] < prefix['end'] for m in named)):
            return False
        return True
    except (KeyError, ValueError, TypeError, IndexError, StopIteration):
        return False
