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
    if not isinstance(context, dict) or set(context) != {'kind', 'paragraph_id', 'person_mention_id', 'quote', 'intervening_paragraph_ids'}:
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
        if any(not verified_blank_gap(chapter, a, b) for a, b in zip(positions, positions[1:])):
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
