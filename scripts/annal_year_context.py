"""Bind an annal entry to its fixed witness's explicit yearly section.

The section is provenance, not a fabricated continuous biography paragraph.
No Gregorian day or birth year is inferred from the recorded month/day.
"""
import hashlib
import re


def annal_regnal_year_valid(date, parse_number):
    mapping = date.get('regnal_year_mapping', {})
    context = date.get('annal_year_reference', {})
    refs = date.get('references', [])
    if not isinstance(mapping, dict) or not isinstance(context, dict) or not isinstance(refs, list):
        return False
    ri, ci = mapping.get('reference_index'), mapping.get('context_reference_index')
    if (mapping.get('kind') != 'annal_ce_regnal_era_span'
            or any(type(i) is not int or not 0 <= i < len(refs) for i in (ri, ci))
            or ri == ci):
        return False
    modern, primary = refs[ri], refs[ci]
    if not isinstance(modern, dict) or not isinstance(primary, dict):
        return False
    section = primary.get('section', {})
    if not isinstance(section, dict):
        return False
    raw = section.get('raw_quote')
    bounds = section.get('source_lines')
    first, last, n = (mapping.get(k) for k in ('start_ce_year', 'end_ce_year', 'regnal_year'))
    number, name = mapping.get('source_number'), mapping.get('era_name')
    if (not isinstance(raw, str) or not isinstance(bounds, list) or len(bounds) != 2
            or any(type(i) is not int for i in bounds) or not 0 < bounds[0] < bounds[1]
            or not isinstance(name, str) or not name or (1 if number == '元' else parse_number(number)) != n
            or type(n) is not int or n < 1 or mapping.get('target_regnal_year') != n
            or type(first) is not int or type(last) is not int or not 0 < first <= last
            or date.get('era') != 'CE' or date.get('year') != first + n - 1
            or not first <= date['year'] <= last):
        return False
    lines = raw.splitlines()
    term = name + str(number) + '年'
    next_heading = section.get('next_heading', '')
    if not isinstance(next_heading, str):
        return False
    match = re.fullmatch(r'==(.+?)([元一二三四五六七八九十百]+)年==', next_heading)
    line = context.get('event_source_line')
    expression = date.get('source_expression')
    if (len(lines) != bounds[1] - bounds[0] + 1
            or not lines or lines[0] != '==' + term + '=='
            or lines[-1] != next_heading or not match or match[1] != name
            or parse_number(match[2]) != n + 1
            or any(re.fullmatch(r'==.*==', text) for text in lines[1:-1])
            or not next((text for text in lines[1:-1] if text.strip()), '').startswith(str(number) + '年')
            or section.get('year_expression') != term
            or section.get('raw_quote_sha256') != hashlib.sha256(raw.encode()).hexdigest()
            or type(line) is not int or not bounds[0] < line < bounds[1]
            or lines[line - bounds[0]] != date.get('original_quote')
            or not isinstance(expression, str) or not expression or expression not in date['original_quote']
            or context.get('section_id') != section.get('id')):
        return False
    evidence = date.get('evidence', [])
    if (not isinstance(evidence, list) or len(evidence) != 1 or not isinstance(evidence[0], dict)
            or context.get('event_paragraph_id') != evidence[0].get('paragraph_id')
            or date['original_quote'] != evidence[0].get('quote')
            or any(primary.get(k) != evidence[0].get(k) for k in ('work_id', 'book_id', 'chapter_id', 'source_id'))
            or primary.get('quote') != raw or primary.get('scope') != 'primary_annal_year_section_context'
            or primary.get('image_verified') is not False
            or not str(primary.get('url', '')).startswith('https://')
            or primary.get('source_revision') != section.get('source_revision')):
        return False
    return (modern.get('scope') == 'modern_era_year_equivalence_only'
            and modern.get('quote') == name and str(modern.get('url', '')).startswith('https://')
            and isinstance(modern.get('columns'), dict)
            and modern.get('columns', {}).get('era_name') == name
            and modern.get('columns', {}).get('first_year') == str(first)
            and modern.get('columns', {}).get('last_year') == str(last))


def annal_year_binding_valid(date, chapter):
    """The arithmetic check also needs this binding to the marked source file."""
    if not isinstance(chapter, dict):
        return False
    mapping = date.get('regnal_year_mapping', {})
    refs = date.get('references', [])
    if not isinstance(mapping, dict) or not isinstance(refs, list):
        return False
    ci = mapping.get('context_reference_index')
    if type(ci) is not int or not 0 <= ci < len(refs):
        return False
    ref = refs[ci]
    context = date.get('annal_year_reference', {})
    if not isinstance(ref, dict) or not isinstance(context, dict):
        return False
    section = ref.get('section')
    source = chapter.get('source', {})
    paragraph = next((p for p in chapter.get('paragraphs', [])
                      if p['id'] == context.get('event_paragraph_id')), {})
    position = paragraph.get('source_position', {})
    excerpt = next((e for e in source.get('normalization', {}).get('excerpts', [])
                    if e['proposed_paragraph_id'] == paragraph.get('id')), {})
    return (isinstance(section, dict)
            and section in source.get('annal_year_sections', [])
            and source.get('revision_id') == ref.get('source_revision') == section.get('source_revision')
            and all(ref.get(k) == chapter.get(k if k != 'chapter_id' else 'id')
                    for k in ('work_id', 'book_id', 'chapter_id', 'source_id'))
            and position.get('first_line') == position.get('last_line') == context.get('event_source_line')
            and paragraph.get('text') == excerpt.get('raw_quote') == date.get('original_quote')
            and excerpt.get('source_lines') == [context.get('event_source_line')] * 2)
