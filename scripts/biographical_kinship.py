"""核對完整連續傳文中的子嗣承接；不以遠段或補字代替證據。"""
import hashlib
import re


def digital_paratext_errors(chapter):
    """只允許另存的空行與數位節題；不能藉此略去傳文。"""
    errors = []
    records = chapter.get('source', {}).get('normalization', {}).get('omitted_digital_paratext', [])
    if not isinstance(records, list):
        return ['數位節題記錄須為列表']
    occupied = set()
    for record in records:
        if not isinstance(record, dict):
            errors.append('數位節題記錄須為物件'); continue
        span, raw = record.get('source_lines'), record.get('raw_quote')
        valid = (isinstance(span, list) and len(span) == 2
                 and all(type(n) is int and n > 0 for n in span)
                 and span[0] <= span[1] and isinstance(raw, str)
                 and record.get('kind') == 'digital_section_heading'
                 and record.get('not_received_text') is True
                 and record.get('source_revision') == chapter.get('source', {}).get('revision_id'))
        if valid:
            lines = raw.split('\n')
            nonblank = [line.strip() for line in lines if line.strip()]
            valid = (len(lines) == span[1] - span[0] + 1 and bool(nonblank)
                     and all(re.fullmatch(r'(?P<marks>={2,6})[^=\n]+(?P=marks)', line) for line in nonblank)
                     and hashlib.sha256(raw.encode()).hexdigest() == record.get('raw_quote_sha256')
                     and not occupied.intersection(range(span[0], span[1] + 1)))
            if valid:
                for para in chapter.get('paragraphs', []):
                    position = para.get('source_position', {})
                    first, last = position.get('first_line'), position.get('last_line')
                    if type(first) is int and type(last) is int and first <= span[1] and span[0] <= last:
                        valid = False
                occupied.update(range(span[0], span[1] + 1))
        if not valid:
            errors.append('數位節題須有相符固定版本、原行雜湊與純節題文字，不得混入或略去正文')
    return errors


def received_paragraphs_contiguous(chapter, first, second):
    a, b = first.get('source_position', {}), second.get('source_position', {})
    end, start = a.get('last_line'), b.get('first_line')
    if type(end) is not int or type(start) is not int or start <= end:
        return False
    if end + 1 == start:
        return True
    if digital_paratext_errors(chapter):
        return False
    try:
        from .subject_continuation import verified_blank_gap
    except ImportError:
        from subject_continuation import verified_blank_gap
    if verified_blank_gap(chapter, a, b):
        return True
    records = chapter.get('source', {}).get('normalization', {}).get('omitted_digital_paratext', [])
    spans = sorted(record['source_lines'] for record in records
                   if end < record['source_lines'][0] and record['source_lines'][1] < start)
    cursor = end + 1
    for left, right in spans:
        if left != cursor:
            return False
        cursor = right + 1
    return cursor == start

def child_continuation_errors(assertion, chapter):
    errors = []
    context = assertion.get('context', {})
    ids = context.get('paragraph_ids')
    paras = chapter.get('paragraphs', [])
    order = [p['id'] for p in paras]
    byid = {p['id']: p for p in paras}
    evidence = assertion.get('evidence', [])
    valid = (context.get('kind') == 'biographical_child_continuation'
             and assertion.get('predicate') == 'father'
             and isinstance(ids, list) and len(ids) >= 2
             and all(isinstance(i, str) and i in order for i in ids)
             and len(set(ids)) == len(ids)
             and bool(context.get('rationale'))
             and context.get('status') == 'contextual_provisional'
             and context.get('human_reviewed') is False
             and ids == [e.get('paragraph_id') for e in evidence])
    if valid:
        valid = ids == order[order.index(ids[0]):order.index(ids[-1]) + 1]
    if valid:
        for pid, e in zip(ids, evidence):
            p = byid[pid]
            position = p.get('source_position', {})
            valid &= (e.get('chapter_id') == chapter.get('id')
                      and e.get('source_id') == chapter.get('source_id')
                      and e.get('quote') == p.get('text')
                      and p.get('text_layer') == 'received_chapter'
                      and position.get('editorial_excerpt_boundary') is True
                      and type(position.get('first_line')) is int
                      and type(position.get('last_line')) is int
                      and position['first_line'] <= position['last_line']
                      and position.get('revision_id') == chapter.get('source', {}).get('revision_id'))
        if valid:
            for a, b in zip(ids, ids[1:]):
                valid &= received_paragraphs_contiguous(chapter, byid[a], byid[b])
    if not valid:
        return ['傳主子嗣承接須保留同一固定見證的完整連續原段、原行與判讀']
    anchor = next((m for m in byid[ids[0]].get('mentions', [])
                   if m.get('id') == context.get('parent_mention_id')), None)
    child = next((m for m in byid[ids[-1]].get('mentions', [])
                  if m.get('id') == context.get('child_mention_id')), None)
    if (not anchor or anchor.get('kind') != 'person'
            or anchor.get('person_id') != assertion.get('object_person_id')
            or not child or child.get('kind') != 'person'
            or child.get('person_id') != assertion.get('subject_person_id')
            or child.get('start') != 1 or not byid[ids[-1]]['text'].startswith('子')
            or assertion.get('qualifiers', {}).get('source_term') != '子'
            or assertion.get('qualifiers', {}).get('lineage') != 'paternal'):
        errors.append('傳主子嗣承接的父名錨點或段首子某錨點不符')
    return errors
