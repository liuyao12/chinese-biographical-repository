"""Narrow validation for contextual death-year readings in Songshu 51."""
from pathlib import Path
import hashlib
import json


CHAPTER_ID = 'c-songshu-051-wyd1739-zongshi'
MOE_URL = 'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&la=0&page=2&powerMode=0&ver=5'
MOE_TITLE = '教育部《重編國語辭典修訂本》中國歷代年號表'
YUANHUI_ROW = 'source-evidence/song051-wyd1739-zongshi/p014-p017-yuanhui-calendar-row.json'
MOE_BASE_URL = 'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2'

_CASES = {
    'le-song051-p014-yizong-death': {
        'person_id': '3qs_nqa_ioa_AABD',
        'paragraph_id': CHAPTER_ID + ':p014',
        'era_name': '元嘉',
        'year': 444,
        'source_expression': '二十一年',
        'context_kind': 'same_biography_omitted_era_year_after_yuanjia_eight',
        'source_term': '二十一年卒',
    },
    'le-song051-p017-m0062-death': {
        'person_id': '3qs_nqa_ioa_AABDB',
        'paragraph_id': CHAPTER_ID + ':p017',
        'era_name': '元徽',
        'year': 477,
        'source_expression': '與二子承俁並死',
        'context_kind': 'same_biography_contextual_shundi_accession_after_yuanhui_four',
        'source_term': '與二子承俁並死',
        'event_context_phrase': '粲敗秉踰城出走於額檐湖見擒與二子承俁並死',
    },
    'le-song051-p017-m0076-death': {
        'person_id': '3qs_nqa_ioa_AABDBA',
        'paragraph_id': CHAPTER_ID + ':p017',
        'era_name': '元徽',
        'year': 477,
        'source_expression': '與二子承俁並死',
        'context_kind': 'same_biography_contextual_shundi_accession_after_yuanhui_four',
        'source_term': '與二子承俁並死',
        'event_context_phrase': '粲敗秉踰城出走於額檐湖見擒與二子承俁並死',
    },
    'le-song051-p017-m0077-death': {
        'person_id': '3qs_nqa_ioa_AABDBB',
        'paragraph_id': CHAPTER_ID + ':p017',
        'era_name': '元徽',
        'year': 477,
        'source_expression': '與二子承俁並死',
        'context_kind': 'same_biography_contextual_shundi_accession_after_yuanhui_four',
        'source_term': '與二子承俁並死',
        'event_context_phrase': '粲敗秉踰城出走於額檐湖見擒與二子承俁並死',
    },
}


def _paragraph(chapter, paragraph_id):
    return next((p for p in chapter.get('paragraphs', []) if p.get('id') == paragraph_id), None)


def _crosswalk(date, expected, root):
    refs = date.get('references')
    if not isinstance(refs, list):
        return False
    match = next((r for r in refs if isinstance(r, dict) and r.get('quote') == expected['era_name']
                  and r.get('url') in (MOE_URL, MOE_BASE_URL)), None)
    if not match or match.get('title') != MOE_TITLE or match.get('url') not in (MOE_URL, MOE_BASE_URL):
        return False
    columns = match.get('columns')
    start, end = (('424', '453') if expected['era_name'] == '元嘉' else ('473', '477'))
    if (not isinstance(columns, dict) or columns != {
            'dynasty': '宋', 'era_name': expected['era_name'],
            'first_year': start, 'last_year': end,
    }):
        return False
    expected_scope = ('modern_era_year_equivalence_only' if expected['era_name'] == '元嘉'
                      else 'digital_editorial_regnal_year_equivalence_only')
    if match.get('scope') != expected_scope:
        return False
    fixed = match.get('fixed_row_reference')
    if not isinstance(fixed, dict) or set(fixed) != {'path', 'sha256'}:
        return False
    if expected['era_name'] == '元徽' and fixed.get('path') != YUANHUI_ROW:
        return False
    try:
        target = (Path(root).resolve() / fixed['path']).resolve()
        evidence_root = (Path(root).resolve() / 'source-evidence').resolve()
        if not target.is_relative_to(evidence_root) or not target.is_file():
            return False
        if hashlib.sha256(target.read_bytes()).hexdigest() != fixed['sha256']:
            return False
        row = json.loads(target.read_text(encoding='utf-8'))
    except (OSError, ValueError, TypeError, KeyError):
        return False
    if expected['era_name'] == '元徽':
        row_columns = row.get('columns')
        return (isinstance(row_columns, dict)
                and all(row_columns.get(k) == v for k, v in columns.items())
                and row.get('record_type') == 'digital_calendar_crosswalk_row'
                and row.get('source_title') == MOE_TITLE and row.get('url') == MOE_URL
                and row.get('accessed_on') == '2026-11-13'
                and row.get('row_text') == '南北朝 (西元386～589) 宋 | 元徽 | 473 | 477'
                and row.get('scope') == '僅作現代年號西元起迄對照，不是古代史料或原始曆日證據。'
                and row.get('human_reviewed') is False
                and 'raw_response_sha256' not in row and 'raw_html_sha256' not in row)
    return (row.get('columns') == columns
            and isinstance(row.get('row_html'), str)
            and row.get('scope') == 'existing_fixed_digital_calendar_row_only_not_ancient_witness')


def valid(date, event, chapters, root, bound_role):
    """Validate only the four fixed events; never infer dates for other records."""
    if bound_role != 'life_event' or not isinstance(date, dict) or not isinstance(event, dict):
        return False
    expected = _CASES.get(event.get('id'))
    if not expected or event.get('person_id') != expected['person_id']:
        return False
    mapping = date.get('regnal_year_mapping')
    if (not isinstance(mapping, dict)
            or set(mapping) != {'kind', 'era_name', 'year', 'source_expression', 'context_kind'}
            or mapping.get('kind') != 'fixed_wyd_song051_p014_p017_life_date'
            or mapping.get('era_name') != expected['era_name']
            or mapping.get('year') != expected['year']
            or mapping.get('source_expression') != expected['source_expression']
            or mapping.get('context_kind') != expected['context_kind']):
        return False
    if (date.get('era') != 'CE' or date.get('year') != expected['year']
            or date.get('era_year') != expected['year']
            or date.get('calendar') != 'chinese_civil'
            or date.get('source_expression') != expected['source_expression']
            or event.get('event_type') != 'death'
            or event.get('date_expression') != expected['source_expression']
            or event.get('source_term') != expected['source_term']):
        return False
    if not _crosswalk(date, expected, root):
        return False
    try:
        evidence, = event['evidence']
        date_evidence, = date['evidence']
        if evidence != date_evidence or evidence.get('chapter_id') != CHAPTER_ID:
            return False
        chapter = chapters.get(CHAPTER_ID)
        paragraph = _paragraph(chapter or {}, expected['paragraph_id'])
        if (not paragraph or evidence.get('paragraph_id') != expected['paragraph_id']
                or evidence.get('quote') != paragraph['text']
                or date.get('original_quote') != paragraph['text']):
            return False
        mention = next(m for m in paragraph.get('mentions', [])
                       if m.get('id') == evidence.get('person_mention_id'))
        if mention.get('kind') != 'person' or mention.get('person_id') != expected['person_id']:
            return False
        text = paragraph['text']
    except (KeyError, TypeError, ValueError, StopIteration):
        return False

    if event['id'] == 'le-song051-p014-yizong-death':
        start = text.find('元嘉八年')
        death = text.find('二十一年卒')
        return start >= 0 and death > start and mention['start'] < start

    if (event.get('contextual_date_basis', {}).get('kind')
            != 'song051_yuanhui_fourth_year_then_shundi_accession'):
        return False
    context = event['contextual_date_basis']
    context_paragraph = _paragraph(chapter, context.get('paragraph_id'))
    prior_paragraph = _paragraph(chapter, CHAPTER_ID + ':p015')
    prior_mention = next((m for m in (prior_paragraph or {}).get('mentions', [])
                          if m.get('kind') == 'person' and m.get('person_id') == '3qs_nqa_ioa_AABDB'), None)
    basis = date.get('basis')
    if (not context_paragraph or context.get('chapter_id') != CHAPTER_ID
            or context_paragraph['id'] != CHAPTER_ID + ':p016'
            or context.get('quote') != context_paragraph['text']
            or context.get('era_year_anchor') != '元徽元年'
            or not prior_paragraph or not prior_mention
            or '元徽元年' not in prior_paragraph['text']
            or context.get('sequence_anchor') != '四年遷中書令'
            or context.get('accession_anchor') != '順帝即位'
            or not (0 <= context_paragraph['text'].find('四年遷中書令')
                    < context_paragraph['text'].find('順帝即位'))
            or not isinstance(basis, dict)
            or basis.get('kind') != 'parallel_event'
            or basis.get('source_event_quote') != expected['source_term']
            or basis.get('reference_event_quote') != '順帝即位'
            or basis.get('reference_year_quote') != '元徽'
            or basis.get('reference_year_url') != MOE_BASE_URL):
        return False
    event_start = text.find(expected['event_context_phrase'])
    participants = {'3qs_nqa_ioa_AABDB', '3qs_nqa_ioa_AABDBA', '3qs_nqa_ioa_AABDBB'}
    event_mentions = {m.get('person_id') for m in paragraph.get('mentions', [])
                      if event_start >= 0 and event_start <= m.get('start', -1)
                      and m.get('end', 0) <= event_start + len(expected['event_context_phrase'])}
    return (event_start >= 0 and mention['start'] >= event_start
            and text[mention['start']:mention['end']] == mention['surface']
            and participants.issubset(event_mentions))
