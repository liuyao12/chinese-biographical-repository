#!/usr/bin/env python3
"""匯出家譜檢視器所需的單一人物來源包；純 Python，無 AI 呼叫。"""
import argparse
import json
from pathlib import Path
try:
    from .identity_alternatives import identity_participant_ids
except ImportError:
    from identity_alternatives import identity_participant_ids

ROOT = Path(__file__).resolve().parents[1]


def validate_clan_style(name, paragraph=None, relations=()):
    """A clan appellation preserves an unknown ming; it is not an unsplit name."""
    if 'clan_style' not in name:
        return
    style = name['clan_style']
    keys = {'kind', 'value', 'source_term', 'assertion_ids', 'status', 'rationale', 'human_reviewed'}
    valid = (isinstance(style, dict) and set(style) == keys
             and isinstance(name.get('surname'), str) and bool(name['surname'])
             and name.get('ming') is None and 'full_name' not in name
             and style.get('value') == name['surname'] + '氏'
             and style.get('human_reviewed') is False and bool(style.get('rationale'))
             and isinstance(name.get('quote'), str)
             and isinstance(style.get('source_term'), str) and bool(style['source_term'])
             and style['source_term'] in name.get('quote', '')
             and isinstance(style.get('assertion_ids'), list) and paragraph is not None
             and name.get('quote') in paragraph.get('text', ''))
    if valid and style['kind'] == 'received_clan_appellation':
        valid = (style['status'] == 'source_attested' and style['assertion_ids'] == []
                 and style['source_term'] == style['value']
                 and any(m.get('person_id') == name.get('person_id')
                         and m.get('surface') == style['source_term'] for m in paragraph.get('mentions', [])))
    elif valid and style['kind'] == 'sibling_clan_appellation':
        selected = [a for a in relations if a.get('id') in style['assertion_ids']]
        valid = (style['status'] == 'editorial_provisional' and bool(selected)
                 and len(selected) == len(style['assertion_ids'])
                 and all(a.get('predicate') == 'sister'
                         and a.get('subject_person_id') == name.get('person_id')
                         and a.get('qualifiers', {}).get('shared_father') is not False
                         and a.get('qualifiers', {}).get('source_term') == style['source_term']
                         and any(e.get('paragraph_id') == name.get('paragraph_id')
                                 and style['source_term'] in e.get('quote', '') for e in a.get('evidence', []))
                         for a in selected)
                 and style['source_term'].startswith(name['surname'])
                 and style['source_term'].endswith(('之妹也', '之妺也')))
    elif valid and style['kind'] == 'source_sibling_group_appellation':
        try:
            from scripts.collateral_kinship import source_sibling_group_valid
            from scripts.chinese_civil_years import numeral
        except ModuleNotFoundError:
            from collateral_kinship import source_sibling_group_valid
            from chinese_civil_years import numeral
        selected = [a for a in relations if a.get('id') in style['assertion_ids']]
        chapter_id = name.get('chapter_id')
        known_people = {m.get('person_id') for m in paragraph.get('mentions', []) if m.get('kind') == 'person'}
        valid = (style['status'] == 'editorial_provisional' and len(selected) == 1
                 and style['assertion_ids'] == [selected[0]['id']] and bool(chapter_id)
                 and selected[0].get('predicate') == 'sister'
                 and selected[0].get('subject_person_id') == name.get('person_id')
                 and selected[0].get('qualifiers', {}).get('shared_father') is not False
                 and selected[0].get('qualifiers', {}).get('source_sibling_group', {}).get('source_term') == style['source_term']
                 and source_sibling_group_valid(selected[0], {paragraph['id']:(chapter_id,paragraph)}, known_people, numeral)
                 and any(m.get('kind') == 'person'
                         and m.get('person_id') == selected[0].get('object_person_id')
                         and m.get('surface') in (style['value'], style['value'] + '女')
                         for m in paragraph.get('mentions', [])))
    elif valid and style['kind'] == 'wife_sibling_clan_appellation':
        selected = [a for a in relations if a.get('id') in style['assertion_ids']]
        valid = (style['status'] == 'editorial_provisional' and len(selected) == 1
                 and style['assertion_ids'] == [selected[0]['id']]
                 and selected[0].get('predicate') == 'sister'
                 and selected[0].get('subject_person_id') == name.get('person_id')
                 and selected[0].get('qualifiers', {}).get('shared_father') is not False
                 and selected[0].get('qualifiers', {}).get('source_term') == style['source_term']
                 and any(e.get('paragraph_id') == paragraph.get('id')
                         and style['source_term'] in e.get('quote', '') for e in selected[0].get('evidence', []))
                 and any(m.get('kind') == 'person' and m.get('person_id') == selected[0].get('object_person_id')
                         and m.get('surface', '').startswith(name['surname'])
                         and style['source_term'] == '妻弟' + m.get('surface', '') for m in paragraph.get('mentions', [])))
    elif valid and style['kind'] == 'bound_named_sister_clan_appellation':
        try:from .received_family_names import clan_valid
        except ImportError:from received_family_names import clan_valid
        valid = clan_valid(name, paragraph, relations)
    else:
        valid = False
    if not valid:
        raise ValueError('氏稱須保留未知本名、原文或具名兄弟的姊妹證據，不得把字作名')


def validate_full_name(name, paragraph=None):
    """An unsegmented source name is not an inferred surname/given-name split."""
    if 'full_name' not in name:
        return
    import re
    value, basis = name.get('full_name'), name.get('full_name_basis')
    valid = (isinstance(value, str) and bool(value) and value == value.strip()
             and name.get('surname') is None and name.get('ming') is None
             and isinstance(basis, dict)
             and set(basis) == {'kind', 'source_term', 'rationale', 'human_reviewed'}
             and basis.get('kind') == 'received_parallel_spelling'
             and isinstance(basis.get('source_term'), str) and bool(basis['source_term'])
             and isinstance(name.get('quote'), str) and basis['source_term'] in name['quote']
             and isinstance(basis.get('rationale'), str) and bool(basis['rationale'].strip()) and basis.get('human_reviewed') is False)
    if paragraph is not None and valid:
        quote = name['quote']; text = paragraph['text']
        starts = [i for i in range(len(text)) if text.startswith(quote, i)]
        valid = any(m.get('person_id') == name.get('person_id') and m.get('kind') == 'person'
                    and m.get('surface') == basis['source_term']
                    and any(i <= m['start'] < m['end'] <= i + len(quote) for i in starts)
                    for m in paragraph['mentions'])
    supported = False
    for ref in name.get('references', []):
        if not isinstance(ref, dict):
            continue
        raw, quote, commit = ref.get('raw_quote', ''), ref.get('quote', ''), ref.get('source_commit', '')
        normalized = re.sub(r'[()/¶\s]', '', re.sub(r'<pb:[^>]*>', '', raw)) if isinstance(raw, str) else ''
        if (isinstance(quote, str) and bool(quote) and quote in normalized
                and isinstance(value, str) and value in quote
                and ref.get('scope') == 'received_parallel_name_spelling'
                and isinstance(commit, str) and re.fullmatch('[0-9a-f]{40}', commit) is not None
                and isinstance(ref.get('url'), str) and ref['url'].startswith('https://') and commit in ref['url'] and ref.get('image_verified') is False):
            supported = True
    if not valid or not supported:
        raise ValueError('未分姓名須有原稱、固定平行原文及判讀，不得暗拆姓與名')


def validate_courtesy_name(name):
    """字須有明示來源，不從顯示名稱推拆或冒作本名。"""
    if 'zi' not in name:
        if 'zi_basis' in name:
            raise ValueError('稱字判讀須有相符字名')
        return
    zi = name['zi']
    quotes = [name.get('quote', '')] + [r.get('quote', '') for r in name.get('references', [])]
    basis = name.get('zi_basis')
    called_by_zi = False
    if basis is not None:
        required = {'kind', 'status', 'human_reviewed', 'rationale', 'subject_anchor', 'marker_anchor'}
        quote = name.get('quote', '')
        called_by_zi = isinstance(basis, dict) and set(basis) == required and isinstance(quote, str)
        if called_by_zi:
            subject, marker = basis['subject_anchor'], basis['marker_anchor']
            def valid_anchor(a):
                return (isinstance(a, dict) and set(a) == {'paragraph_id', 'start', 'end', 'surface'}
                        and a['paragraph_id'] == name.get('paragraph_id')
                        and type(a['start']) is int and type(a['end']) is int
                        and 0 <= a['start'] < a['end'] <= len(quote)
                        and quote[a['start']:a['end']] == a['surface'])
            called_by_zi = (basis['kind'] == 'biographical_subject_called_by_courtesy_name'
                            and basis['status'] == 'source_attested' and basis['human_reviewed'] is False
                            and bool(basis['rationale']) and valid_anchor(subject) and valid_anchor(marker)
                            and subject['start'] == 0 and isinstance(name.get('surname'), str)
                            and isinstance(zi, str) and subject['surface'] == name['surname'] + zi
                            and marker['surface'] == '故稱字' and subject['end'] <= marker['start'])
        if not called_by_zi:
            raise ValueError('稱字記載須連到傳首人物及故稱字原詞，不能據顯示名猜字')
    if (not isinstance(zi, str) or not zi.strip() or zi != zi.strip()
            or name.get('ming') == zi
            or not (called_by_zi or any(isinstance(q, str) and '字' + zi in q for q in quotes))):
        raise ValueError('字須有明示字名的引句且不得冒作名')


def validate_parallel_given_name(name):
    """平行正文首名有原字與固定版本；不從同諱或數位節題截短本名。"""
    import hashlib
    import re
    from urllib.parse import parse_qs, urlparse
    for ref in name.get('references', []):
        if ref.get('scope') != 'primary_parallel_explicit_given_name_and_same_named_ancestors':
            continue
        surname, ming = name.get('surname'), name.get('ming')
        raw, quote = ref.get('raw_context_quote'), ref.get('quote')
        pos, revision = ref.get('source_position', {}), ref.get('source_revision')
        valid = (isinstance(surname, str) and isinstance(ming, str) and bool(ming)
                 and quote == surname + ming and isinstance(raw, str) and raw.startswith(quote + '字')
                 and hashlib.sha256(raw.encode()).hexdigest() == ref.get('raw_context_quote_sha256')
                 and bool(re.fullmatch(r'[0-9a-f]{64}', ref.get('wikitext_sha256', '')))
                 and type(revision) is int and revision > 0 and ref.get('image_verified') is False
                 and type(pos.get('first_line')) is int and pos['first_line'] > 0
                 and pos.get('last_line') == pos['first_line']
                 and type(pos.get('start')) is int and type(pos.get('end')) is int
                 and pos['start'] >= 0 and pos['end'] - pos['start'] == len(quote))
        link = urlparse(ref.get('url', ''))
        if not (valid and link.scheme == 'https' and parse_qs(link.query).get('oldid') == [str(revision)]):
            raise ValueError('平行姓名須完整匹配正文首名與字原詞、原行雜湊及固定修訂，不得截名或以章題補名')


def validate_former_given_name(name, paragraph=None):
    if 'former_ming_basis' in name:
        try:from scripts.fixed_wikisource_units import biography_former_ming_valid
        except ImportError:from fixed_wikisource_units import biography_former_ming_valid
        if not biography_former_ming_valid(name, paragraph):raise ValueError('本名與賜名須綁傳首本人、舊名、君主與完整原句，不得把本字當本名')
        return
    """初名只在同一引句明示名之曰與更名時採用，不從別名猜定。"""
    if 'former_ming' not in name:
        return
    former, current = name['former_ming'], name.get('ming')
    quotes = [name.get('quote', '')] + [r.get('quote', '') for r in name.get('references', [])]
    if (not isinstance(former, str) or not former.strip() or former != former.strip()
            or not isinstance(current, str) or not current.strip() or current != current.strip()
            or former == current
            or not any(isinstance(q, str) and '名之曰' + former in q
                       and '更名' + current in q for q in quotes)):
        raise ValueError('初名須有同一引文內名之曰與更名的明示敘述，不得與現名相同')


def validate_name_component_alternatives(name):
    """Keep separately cited name/zi claims without silently replacing a preferred reading."""
    import re
    for alternative in name.get('component_alternatives', []):
        components = alternative.get('components', {})
        terms = alternative.get('source_terms', {})
        ref = alternative.get('reference', {})
        valid = (set(components) == {'surname', 'ming', 'zi'}
                 and alternative.get('status') == 'source_claim_not_selected'
                 and isinstance(alternative.get('rationale'), str) and bool(alternative['rationale'])
                 and ref.get('image_verified') is False
                 and isinstance(ref.get('url'), str) and ref['url'].startswith('https://')
                 and re.fullmatch('[0-9a-f]{40}', ref.get('source_commit', '')) is not None
                 and ref['source_commit'] in ref['url']
                 and re.fullmatch('[0-9a-f]{40}', ref.get('source_blob_sha', '')) is not None
                 and re.fullmatch('[0-9a-f]{64}', ref.get('response_sha256', '')) is not None)
        raw = ref.get('raw_quote', '')
        quote = ref.get('quote', '')
        normalized = re.sub(r'<pb:[^>]*>', '', raw) if isinstance(raw, str) else ''
        normalized = re.sub(r'[()/¶\s]', '', normalized)
        valid = valid and isinstance(quote, str) and bool(quote) and quote in normalized
        present = {key for key, value in components.items() if value is not None}
        valid = valid and bool(present) and set(terms) == present
        for key in present:
            value, word = components[key], {'surname': '姓', 'ming': '名', 'zi': '字'}.get(key, '')
            allowed = (value + word + '也', word + value) if isinstance(value, str) else ()
            if (key == 'surname' and isinstance(value, str)
                    and isinstance(components.get('ming'), str)
                    and value + '姓' + components['ming'] + '名也' in quote):
                allowed += (value + '姓',)
            valid = (valid and isinstance(value, str) and bool(value) and value == value.strip()
                     and terms[key] in allowed and terms[key] in quote)
        if not valid:
            raise ValueError('姓名組件異說須有固定來源、原引文與相符名／字原詞')


def table_person_occurrences(table, person_ids):
    """保留逐人錨點與原格座標；編者西元欄不轉成人物事件日期。"""
    source = table['source']
    for fragment in table['fragments']:
        for row in fragment['rows']:
            for cell in row['cells']:
                for mention in cell.get('person_mentions', []):
                    if mention.get('person_id') not in person_ids:
                        continue
                    start, end = mention.get('start'), mention.get('end')
                    if (not isinstance(start, int) or not isinstance(end, int)
                            or not 0 <= start < end <= len(cell['text'])
                            or cell['text'][start:end] != mention.get('surface')):
                        raise ValueError('年表人物提及須對應原格字元錨點')
                    location = dict(table_id=table['id'], table_fragment_id=fragment['id'],
                                    table_row_id=row['id'], table_cell_id=cell['id'],
                                    work_id=source['work_id'], book_id=source['book_id'],
                                    chapter_id=source['chapter_id'], source_id=source['id'],
                                    source_revision=source['revision'])
                    passage = dict(cell, **location, source_header=fragment['source_header'],
                                   row_year=row.get('year'))
                    yield dict(mention, **location, kind='table_person_mention', quote=cell['text']), passage


def load_catalog(root=ROOT):
    people = {p['id']: p for p in json.loads((root / 'registry/persons.json').read_text())['persons']}
    records = [json.loads(path.read_text()) for path in sorted((root / 'corpus').glob('*/*.json'))]
    try:
        from .table_evidence import load_tables
    except ImportError:
        from table_evidence import load_tables
    records.extend({'record_type': 'historical_table_source', 'table': table}
                   for table in load_tables(root).values())
    name_path = root / 'data/corpus/profile-names.json'
    if name_path.exists():
        records.append({'record_type': 'person_name_component_set',
                        'records': json.loads(name_path.read_text())['records']})
    try:from scripts.fixed_complete_family_career import errors as fixed_family_career_errors
    except ImportError:from fixed_complete_family_career import errors as fixed_family_career_errors
    fixed_errors=fixed_family_career_errors(root,records)
    if fixed_errors:raise ValueError(';'.join(fixed_errors))
    try:from scripts.fixed_kanripo_fact_slots import errors as fixed_kanripo_fact_errors
    except ImportError:from fixed_kanripo_fact_slots import errors as fixed_kanripo_fact_errors
    fact_errors=fixed_kanripo_fact_errors(root,records)
    if fact_errors:raise ValueError('; '.join(fact_errors))
    try:from scripts.archived_excerpt_facts import errors as archived_excerpt_errors
    except ImportError:from archived_excerpt_facts import errors as archived_excerpt_errors
    excerpt_errors=archived_excerpt_errors(root,records)
    if excerpt_errors:raise ValueError(';'.join(excerpt_errors))
    # Fixed complete-witness facts are checked at the native/export shared boundary.
    try:from scripts.fixed_witness_fact_slots import errors as witness_fact_errors
    except ImportError:from fixed_witness_fact_slots import errors as witness_fact_errors
    fact_errors=witness_fact_errors(root,records)
    if fact_errors:raise ValueError(';'.join(fact_errors))
    try:from scripts.profile_title_preferences import PreferenceCatalog
    except ImportError:from profile_title_preferences import PreferenceCatalog
    return people, PreferenceCatalog(records,people,root)


def bundle(person_id, root=ROOT, include_provisional=False, catalog=None):
    people, records = catalog if catalog is not None else load_catalog(root)
    try:from scripts.profile_title_preferences import choice as profile_title_choice
    except ImportError:from profile_title_preferences import choice as profile_title_choice
    requested_id = person_id
    aliases = {alias: pid for pid, person in people.items() for alias in person.get('id_aliases', [])}
    person_id = aliases.get(person_id, person_id)
    default_profile_title = profile_title_choice(records,people,person_id,root)
    if person_id not in people:
        raise ValueError('未知人物 ID：' + person_id)
    equivalences = [d for r in records if r.get('record_type') == 'person_equivalence_set' for d in r['decisions']]
    ids = {person_id}
    # 明示選用暫定同指時取傳遞閉包；保留每項決定及原始 ID，不改寫權威資料。
    if include_provisional:
        while True:
            expanded = ids | {p for d in equivalences if ids.intersection(d['person_ids']) for p in d['person_ids']}
            if expanded == ids:
                break
            ids = expanded
    related_equivalences = [d for d in equivalences if ids.intersection(d['person_ids'])]
    mentions, relations, titles, identities, addresses, life_events, ages, person_events, age_differences = [], [], [], [], [], [], [], [], []
    family_counts = []
    table_occurrences, occurrence_cells = [], {}
    name_components = []
    chapters, paragraphs, tables = {}, {}, {}
    for record in records:
        kind = record.get('record_type')
        if kind == 'marked_chapter':
            chapters[record['id']] = record
            ages.extend(a for a in record['annotation'].get('age_assertions', []) if a['person_id'] in ids)
            family_counts.extend(a for a in record['annotation'].get('family_count_reports', []) if a['parent_person_id'] in ids)
            age_differences.extend(a for a in record['annotation'].get('age_difference_assertions', []) if ids.intersection((a['person_id'], a['reference_person_id'])))
            for paragraph in record['paragraphs']:
                paragraphs[paragraph['id']] = (record, paragraph)
                for mention in paragraph['mentions']:
                    if mention.get('person_id') in ids:
                        mentions.append(dict(mention, paragraph_id=paragraph['id'], chapter_id=record['id']))
        elif kind == 'person_assertion_set':
            relations.extend(a for a in record['assertions'] if a['subject_person_id'] in ids or a['object_person_id'] in ids)
        elif kind == 'historical_table_source':
            tables[record['table']['id']] = record['table']
            for occurrence, cell in table_person_occurrences(record['table'], ids):
                table_occurrences.append(occurrence)
                occurrence_cells[cell['id']] = cell
        elif kind == 'person_address_assertion_set':
            addresses.extend(a for a in record['assertions'] if a['person_id'] in ids)
        elif kind in ('person_life_event_assertion_set', 'table_person_life_event_assertion_set'):
            life_events.extend(e for e in record['events'] if e['person_id'] in ids)
        elif kind == 'person_event_assertion_set':
            person_events.extend(e for e in record['events'] if e['person_id'] in ids)
        elif kind in ('title_holding_assertion_set', 'table_title_holding_assertion_set'):
            titles.extend(t for t in record['holdings'] if t['person_id'] in ids)
        elif kind == 'person_name_component_set':
            name_components.extend(n for n in record['records'] if n['person_id'] in ids)
        elif 'decisions' in record and kind not in ('person_equivalence_set', 'family_tree_decision_set', 'profile_title_preference_set'):
            identities.extend(d for d in record['decisions'] if d.get('person_id') in ids
                              or (kind == 'person_identity_decision_set'
                                  and ids.intersection(identity_participant_ids(d))))
    distinctions = []
    for record in records:
        if record.get('record_type') != 'person_distinction_set':
            continue
        for decision in record['distinctions']:
            if not ids.intersection(decision['person_ids']):
                continue
            evidence = []
            for item in decision['evidence']:
                chapter, _ = paragraphs[item['paragraph_id']]
                evidence.append(dict(item, chapter_id=chapter['id'], work_id=chapter['work_id'],
                                     book_id=chapter['book_id'], source_id=chapter['source_id']))
            distinctions.append(dict(decision, evidence=evidence))
    enriched_names = []
    for name in name_components:
        name_paragraph = paragraphs.get(name.get('paragraph_id'))
        if 'fixed_biography_name_binding' in name:
            try:from .fixed_biography_names import component_valid
            except ImportError:from fixed_biography_names import component_valid
            if not name_paragraph or not component_valid(name,name_paragraph[0],root,[a for r in records if r.get('record_type')=='person_assertion_set' for a in r['assertions']]):
                raise ValueError('固定完整傳記姓名須綁同人原稱、字、一名與原字見證；不得拼全名冒原稱或任選韓賈姓')
        if 'component_source_binding' in name:
            try:from .received_family_names import source_component_valid
            except ImportError:from received_family_names import source_component_valid
            if not name_paragraph or not source_component_valid(name,name_paragraph[0],root):
                raise ValueError('收到姓名構件須逐原人物錨、緊接字詞與固定見證，不借同段他人字或拼全名冒原稱')
        validate_clan_style(name, name_paragraph[1] if name_paragraph else None, relations)
        validate_full_name(name, name_paragraph[1] if name_paragraph else None)
        validate_courtesy_name(name)
        if 'surname_basis' in name:
            try:
                from .surname_from_father import validate as validate_inferred_surname
            except ImportError:
                from surname_from_father import validate as validate_inferred_surname
            validate_inferred_surname(name,
                [n for r in records if r.get('record_type') == 'person_name_component_set' for n in r['records']],
                {c['id']: c for c, p in paragraphs.values()},
                ([a for r in records if r.get('record_type') == 'person_assertion_set' for a in r['assertions']]
                 if name['surname_basis'].get('kind') in ('contextual_surname_from_received_fact_chain', 'contextual_surname_from_same_source_father_chain', 'contextual_surname_from_bound_paternal_ancestor', 'contextual_surname_from_bounded_named_family_path', 'contextual_surname_from_bound_received_family_units', 'contextual_surname_from_fixed_received_kinship', 'contextual_surname_from_fixed_biography_family', 'contextual_surname_from_fixed_witness_slots') else relations), root=root)
        try:
            from .name_childhood import validate_childhood_name
        except ImportError:
            from name_childhood import validate_childhood_name
        validate_childhood_name(name, name_paragraph[1] if name_paragraph else None)
        try:
            from .name_xiaoming import validate_xiaoming
        except ImportError:
            from name_xiaoming import validate_xiaoming
        validate_xiaoming(name, name_paragraph[1] if name_paragraph else None)
        validate_parallel_given_name(name)
        validate_former_given_name(name, name_paragraph[1] if name_paragraph else None)
        validate_name_component_alternatives(name)
        if name.get('kind') == 'table_cell':
            try:
                from .table_evidence import table_name_component_errors
            except ImportError:
                from table_evidence import table_name_component_errors
            errors = table_name_component_errors(name, tables)
            if errors:
                raise ValueError('；'.join(errors))
            enriched_names.append(dict(name))
            continue
        hit = paragraphs.get(name.get('paragraph_id'))
        if (not hit or hit[0]['id'] != name.get('chapter_id')
                or not isinstance(name.get('quote'), str) or not name['quote']
                or name['quote'] not in hit[1]['text']
                or not any(m.get('person_id') == name['person_id'] for m in hit[1]['mentions'])):
            raise ValueError('姓名組件缺有效人物與來源引句')
        chapter = hit[0]
        enriched_names.append(dict(name, work_id=chapter['work_id'],
                                   book_id=chapter['book_id'], source_id=chapter['source_id']))
    name_components = enriched_names
    try:
        from .preferred_name_components import validated_readings
    except ImportError:
        from preferred_name_components import validated_readings
    preferred_name_components = validated_readings(records,
        [n for r in records if r.get('record_type') == 'person_name_component_set' for n in r['records']],
        chapters, ids)
    date_decisions = [d for r in records if r.get('record_type') == 'life_event_date_decision_set'
                      for d in r['decisions'] if set(d['person_ids']).issubset(ids)]
    try:
        from .life_event_dates import selected_dates
    except ImportError:
        from life_event_dates import selected_dates
    selected_life_dates = selected_dates(life_events, date_decisions)
    kinship_cases = [case for chapter in chapters.values() for case in chapter['annotation'].get('kinship_interpretation_cases', []) if ids.intersection((case['subject_person_id'], case['object_person_id']))]
    unresolved_cases = [dict(case, chapter_id=chapter['id'], source_id=chapter['source_id']) for chapter in chapters.values() for case in chapter['annotation'].get('unresolved_identity_cases', []) if ids.intersection(case['candidate_person_ids'])]
    referent_cases = [dict(case, work_id=chapter['work_id'], book_id=chapter['book_id'], chapter_id=chapter['id'], source_id=chapter['source_id'])
                      for chapter in chapters.values() for case in chapter['annotation'].get('referent_interpretations', [])
                      if any(ids.intersection(a['candidate_person_ids']) for a in case['alternatives'])]
    if referent_cases:
        try:
            from .referent_interpretations import interpretation_errors
        except ImportError:
            from referent_interpretations import interpretation_errors
        for chapter_id in {c['chapter_id'] for c in referent_cases}:
            errors = interpretation_errors(chapters[chapter_id], set(people))
            if errors:
                raise ValueError('；'.join(errors))
    source_reading_cases = [dict(case, chapter_id=chapter['id'], source_id=chapter['source_id']) for chapter in chapters.values() for case in chapter['annotation'].get('source_reading_cases', []) if case['person_id'] in ids]
    title_proposals = [proposal for chapter in chapters.values() for proposal in chapter['annotation'].get('title_proposals', []) if proposal['person_id'] in ids]
    resolved_cases = [dict(case, chapter_id=chapter['id'], source_id=chapter['source_id']) for chapter in chapters.values() for case in chapter['annotation'].get('resolved_identity_cases', []) if case['person_id'] in ids]
    reported_variants = [variant for chapter in chapters.values() for variant in chapter['annotation'].get('reported_variants', []) if ids.intersection(variant['person_ids'])]
    unresolved_titles = [dict(a, chapter_id=ch['id'], source_id=ch['source_id']) for ch in chapters.values() for a in ch.get('annotation', {}).get('unresolved_title_attestations', []) if ids.intersection(a['candidate_person_ids'])]
    preferred_titles = []
    for holding in titles:
        for decision in identities:
            reading = decision.get('preferred_reading', {})
            if (reading.get('received_surface') == holding['title']
                    and any(a['person_mention_id'] == reading.get('person_mention_id')
                            and a['surface'] == holding['title'] for a in holding['attestations'])):
                preferred_titles.append({'holding_id':holding['id'],'person_id':holding['person_id'],
                    'decision_id':decision['id'],'source_mention_id':reading['person_mention_id'],
                    'source_title':holding['title'],'preferred_title':reading['preferred_surface'],
                    'status':reading['status'],'rationale':reading['rationale']})
    tree_decisions = [decision for record in records if record.get('record_type') == 'family_tree_decision_set'
                      for decision in record['decisions'] if ids.intersection(decision['participant_person_ids'])]
    try:
        from .unresolved_relation_identity import relevant_groups
    except ImportError:
        from unresolved_relation_identity import relevant_groups
    unresolved_relation_groups = relevant_groups(chapters, {a['id']: a for record in records for a in record.get('assertions', [])}, set(people), ids)
    excluded = {aid for decision in tree_decisions for aid in decision['excluded_assertion_ids']}
    excluded.update(aid for group in unresolved_relation_groups for aid in group['assertion_ids'])
    try:
        from .relative_birth_order_decisions import relevant_decisions, preferred_relation
    except ImportError:
        from relative_birth_order_decisions import relevant_decisions, preferred_relation
    order_decisions = relevant_decisions(chapters, ids)
    preferred_relations = []
    for assertion in relations:
        if assertion['id'] in excluded:
            continue
        preferred = preferred_relation(assertion, order_decisions)
        if 'relative_age_interpretation' in assertion.get('qualifiers', {}):
            try:
                from scripts.song047_collateral_care import preferred_relation as preferred_age_relation
            except ImportError:
                from song047_collateral_care import preferred_relation as preferred_age_relation
            preferred = preferred_age_relation(preferred)
        for decision in tree_decisions:
            if decision['preferred_assertion_id'] == assertion['id'] and decision['parentage_role'] == 'legal_or_dynastic':
                preferred.update(status='editorial_preferred', source_status=assertion['status'], interpretation_decision_id=decision['id'])
                preferred['qualifiers'] = dict(assertion.get('qualifiers', {}), parentage_role='legal_or_dynastic', biological_parent_status='unknown')
        preferred_relations.append(preferred)
    for case in kinship_cases:
        chosen = next((a for a in case['alternatives'] if a['id'] == case.get('default_alternative_id')), None)
        if chosen is not None:
            qualifiers = dict(chosen['qualifiers'])
            age = qualifiers.get('object_relative_age')
            if chosen['predicate'] in ('brother', 'sister') and age in ('older', 'younger'):
                older, younger = (case['object_person_id'], case['subject_person_id']) if age == 'older' else (case['subject_person_id'], case['object_person_id'])
                qualifiers['relative_birth_order'] = {'older_person_id': older, 'younger_person_id': younger,
                    'operator': 'lt', 'older_ordinal': None, 'younger_ordinal': None, 'scope': 'siblings',
                    'interpretation_status': 'editorial_preferred', 'comparison_basis': 'birth_chronology'}
            preferred_relations.append({'id': 'preferred-' + case['id'], 'subject_person_id': case['subject_person_id'],
                'object_person_id': case['object_person_id'], 'predicate': chosen['predicate'],
                'status': 'editorial_preferred', 'interpretation_case_id': case['id'],
                'alternative_id': chosen['id'], 'qualifiers': qualifiers,
                'evidence': case['evidence'], 'selection': case['selection']})
    paragraph_ids = {m['paragraph_id'] for m in mentions}
    paragraph_ids.update(n['paragraph_id'] for n in name_components if n.get('kind') != 'table_cell')
    paragraph_ids.update(e['paragraph_id'] for case in kinship_cases for e in case['evidence'])
    paragraph_ids.update(e['paragraph_id'] for case in kinship_cases for e in case.get('selection', {}).get('comparative_evidence', []))
    paragraph_ids.update(pid for case in unresolved_cases + resolved_cases for pid in case['paragraph_ids'])
    paragraph_ids.update(v['paragraph_id'] for v in reported_variants)
    paragraph_ids.update(c['paragraph_id'] for c in referent_cases)
    for record in relations + titles + identities + addresses + life_events + person_events + ages + family_counts + age_differences + related_equivalences + tree_decisions + distinctions:
        paragraph_ids.update(e['paragraph_id'] for e in record.get('evidence', []) if e.get('kind') != 'table_cell')
        paragraph_ids.update(e['paragraph_id'] for e in record.get('normalized_date', {}).get('evidence', []) if e.get('kind') != 'table_cell')
        paragraph_ids.update(e['paragraph_id'] for e in record.get('normalized_date_range', {}).get('evidence', []) if e.get('kind') != 'table_cell')
        paragraph_ids.update(e['paragraph_id'] for e in record.get('chinese_civil_year', {}).get('context_evidence', []))
        for evidence in record.get('evidence', []):
            context = evidence.get('context', {})
            if context.get('paragraph_id'):
                paragraph_ids.add(context['paragraph_id'])
            paragraph_ids.update(context.get('intervening_paragraph_ids', []))
    for holding in titles:
        for attestation in holding.get('attestations', []):
            paragraph_ids.update(e['paragraph_id'] for e in attestation.get('normalized_date', {}).get('evidence', []) if e.get('kind') != 'table_cell')
        for boundary in holding['effective_period'].values():
            paragraph_ids.update(e['paragraph_id'] for e in boundary['evidence'] if e.get('kind') != 'table_cell')
            paragraph_ids.update(e['paragraph_id'] for e in boundary.get('normalized_date', {}).get('evidence', []) if e.get('kind') != 'table_cell')
    passages = []
    for pid in sorted(paragraph_ids):
        chapter, paragraph = paragraphs[pid]
        passages.append(dict(paragraph, chapter_id=chapter['id'], book_id=chapter['book_id'],
                             work_id=chapter['work_id'], source_id=chapter['source_id']))
    chapter_ids = {p['chapter_id'] for p in passages}
    table_passages = dict(occurrence_cells)
    cited_tables = {m['table_id'] for m in table_occurrences}
    for event in life_events + person_events:
        table_id = event.get('chinese_civil_year', {}).get('year_equivalence', {}).get('table_id')
        if table_id in tables:
            cited_tables.add(table_id)
    for relation in relations:
        for evidence in relation['evidence']:
            if evidence.get('kind') != 'table_cell':
                continue
            try:
                from .table_evidence import table_cell, table_evidence_errors
            except ImportError:
                from table_evidence import table_cell, table_evidence_errors
            errors = table_evidence_errors(evidence, tables, relation['subject_person_id'], relation['object_person_id'], relation['predicate'])
            if errors:
                raise ValueError('；'.join(errors))
            table = tables[evidence['table_id']]
            cited_tables.add(table['id'])
            points = [evidence['table_cell_id']]
            if evidence.get('subject_table_cell_id'):
                points.append(evidence['subject_table_cell_id'])
            for point in points:
                cell = table_cell(table, point)
                table_passages.setdefault(cell['id'], dict(cell, table_id=table['id'],
                    work_id=table['source']['work_id'], book_id=table['source']['book_id'],
                    chapter_id=table['source']['chapter_id'], source_id=table['source']['id'],
                    source_revision=table['source']['revision']))
    for record in records:
        if record.get('record_type') != 'table_person_life_event_assertion_set':
            continue
        for event in record['events']:
            if event['person_id'] not in ids:
                continue
            try:
                from .table_life_events import native_death_errors
                from .table_evidence import table_cell
            except ImportError:
                from table_life_events import native_death_errors
                from table_evidence import table_cell
            errors = native_death_errors(record, event, tables, set(people))
            if errors:
                raise ValueError('；'.join(errors))
            refs = event['evidence'] + event['normalized_date_range']['references']
            for ref in refs:
                tid = ref.get('table_id')
                if tid not in tables:
                    continue
                table = tables[tid]; cited_tables.add(tid)
                cell = table_cell(table, ref.get('table_cell_id'))
                if cell:
                    table_passages.setdefault(cell['id'], dict(cell, table_id=tid,
                        work_id=table['source']['work_id'], book_id=table['source']['book_id'],
                        chapter_id=table['source']['chapter_id'], source_id=table['source']['id'],
                        source_revision=table['source']['revision']))
    date_columns = {}
    # A table's fief, person/event and year cells are source material, not prose paragraphs.
    for holding in titles:
        if holding.get('source_representation') != 'table_cells':
            continue
        try:
            from .table_title_holdings import table_title_errors
        except ImportError:
            from table_title_holdings import table_title_errors
        errors = table_title_errors(holding, tables, set(people))
        if errors:
            raise ValueError('；'.join(errors))
        refs = []
        for endpoint in ('start', 'end'):
            boundary = holding['effective_period'][endpoint]
            date = boundary.get('normalized_date') or boundary.get('normalized_date_range') or {}
            refs.extend(date.get('references', []))
        for ref in refs:
            tid = ref.get('table_id')
            if tid not in tables:
                continue
            table = tables[tid]; cited_tables.add(tid)
            for fragment in table['fragments']:
                for index, col in enumerate(fragment['columns']):
                    if col['id'] == ref.get('table_column_id'):
                        date_columns[col['id']] = dict(col, table_id=tid,
                            table_fragment_id=fragment['id'], column_index=index,
                            work_id=table['source']['work_id'], book_id=table['source']['book_id'],
                            chapter_id=table['source']['chapter_id'], source_id=table['source']['id'],
                            source_revision=table['source']['revision'])
                for row in fragment['rows']:
                    for cell in row['cells']:
                        if cell['id'] == ref.get('table_cell_id'):
                            table_passages.setdefault(cell['id'], dict(cell, table_id=tid,
                                table_fragment_id=fragment['id'], table_row_id=row['id'],
                                table_cell_id=cell['id'], work_id=table['source']['work_id'],
                                book_id=table['source']['book_id'], chapter_id=table['source']['chapter_id'],
                                source_id=table['source']['id'], source_revision=table['source']['revision'],
                                source_header=fragment['source_header'], row_year=row.get('year'),
                                citation_role='native_table_title_reference'))

    for holding in titles:
        for endpoint in ('start', 'end'):
            boundary = holding['effective_period'][endpoint]
            window = boundary.get('normalized_date_range', {})
            event = window.get('table_event')
            if not isinstance(event, dict):
                continue
            try:
                from .table_evidence import table_title_range_errors
            except ImportError:
                from table_evidence import table_title_range_errors
            errors = table_title_range_errors(window, holding, endpoint, tables, boundary)
            if errors:
                raise ValueError('；'.join(errors))
            points = [(event['table_id'], event['table_cell_id'])]
            for key in ('noble_name_cell_id', 'regnal_year_cell_id', 'digital_year_cell_id'):
                if event.get(key):
                    points.append((event['table_id'], event[key]))
            mapping = event.get('year_mapping', {})
            for key in ('era_anchor_cell_id', 'regnal_year_cell_id', 'digital_year_cell_id'):
                if mapping.get(key):
                    points.append((mapping['table_id'], mapping[key]))
            for ref in window.get('references', []):
                if ref.get('table_cell_id'):
                    points.append((ref.get('table_id', event['table_id']), ref['table_cell_id']))
                if ref.get('table_column_id'):
                    table = tables[ref.get('table_id', event['table_id'])]
                    for fragment in table['fragments']:
                        for index, col in enumerate(fragment['columns']):
                            if col['id'] == ref['table_column_id']:
                                date_columns[col['id']] = dict(col, table_id=table['id'],
                                    table_fragment_id=fragment['id'], column_index=index,
                                    work_id=table['source']['work_id'], book_id=table['source']['book_id'],
                                    chapter_id=table['source']['chapter_id'], source_id=table['source']['id'],
                                    source_revision=table['source']['revision'])
            for tid, cid in points:
                table = tables[tid]
                cited_tables.add(tid)
                for fragment in table['fragments']:
                    for row in fragment['rows']:
                        for cell in row['cells']:
                            if cell['id'] == cid:
                                table_passages.setdefault(cid, dict(cell, table_id=tid,
                                    table_fragment_id=fragment['id'], table_row_id=row['id'],
                                    table_cell_id=cid, work_id=table['source']['work_id'],
                                    book_id=table['source']['book_id'], chapter_id=table['source']['chapter_id'],
                                    source_id=table['source']['id'], source_revision=table['source']['revision'],
                                    source_header=fragment['source_header'], row_year=row.get('year'),
                                    citation_role='title_date_reference'))

    # Directly dated attestations and life/age events cite year rows without
    # pretending that a calendar cell names the person or records an event.
    direct_dates = [h['effective_period'][endpoint].get('normalized_date_range', {})
                    for h in titles for endpoint in ('start', 'end')]
    direct_dates += [a.get('normalized_date_range', {}) for h in titles for a in h['attestations']]
    direct_dates += [e.get('normalized_date_range', {}) for e in life_events + person_events + ages]
    for window in direct_dates:
        proof = window.get('regnal_year_table')
        if not isinstance(proof, dict):
            continue
        try:
            from .table_evidence import table_regnal_range_errors, table_cell
        except ImportError:
            from table_evidence import table_regnal_range_errors, table_cell
        source_reign = proof.get('source_era_name', proof.get('era_name'))
        term = proof.get('year_source_term')
        season = proof.get('season_source_term', '')
        expression = source_reign + term + season if all(isinstance(v, str) for v in (source_reign, term, season)) else None
        # Only a source-specific designation needs another person's source anchor.
        # Resolve it lazily; most person bundles have no such reign claim.
        claim = proof.get('reign_designation')
        mid = claim.get('person_mention_id') if isinstance(claim, dict) else None
        anchor = next(((chapter['id'], paragraph['id'], mention)
                       for chapter, paragraph in paragraphs.values()
                       for mention in paragraph['mentions'] if mention['id'] == mid), None) if mid else None
        reign_mentions = {mid: anchor} if anchor is not None else {}
        errors = table_regnal_range_errors(window, expression, tables, reign_mentions)
        if errors:
            raise ValueError('；'.join(errors))
        table = tables[proof['table_id']]
        cited_tables.add(table['id'])
        for key in ('era_anchor_cell_id', 'regnal_year_cell_id', 'digital_year_cell_id'):
            cell = table_cell(table, proof[key])
            row = next(row for f in table['fragments'] for row in f['rows']
                       if any(c['id'] == cell['id'] for c in row['cells']))
            table_passages.setdefault(cell['id'], dict(cell, table_id=table['id'],
                work_id=table['source']['work_id'], book_id=table['source']['book_id'],
                chapter_id=table['source']['chapter_id'], source_id=table['source']['id'],
                source_revision=table['source']['revision'], table_row_id=row['id'],
                row_year=row.get('year'), citation_role='regnal_year_reference'))

    # Fixed-witness concordance affects counts only; all raw mentions remain.
    try:
        from .occurrence_concordance import summarize_occurrences
    except ImportError:
        from occurrence_concordance import summarize_occurrences
    mention_summary, most_mentioned = summarize_occurrences(mentions, table_occurrences, chapters, root, records, set(people))
    neighbor_ids = ids | {a[k] for a in relations for k in ('subject_person_id', 'object_person_id')}
    neighbor_ids.update(p for decision in tree_decisions for p in decision['participant_person_ids'])
    neighbor_ids.update(p for decision in distinctions for p in decision['person_ids'])
    neighbor_ids.update(p for decision in identities if 'alternatives' in decision
                        for p in identity_participant_ids(decision))
    neighbor_ids.update(p for case in unresolved_cases for p in case['candidate_person_ids'])
    neighbor_ids.update(p for case in referent_cases for a in case['alternatives'] for p in a['candidate_person_ids'])
    neighbor_ids.update(p for case in kinship_cases for p in (case['subject_person_id'], case['object_person_id']))
    for chapter in chapters.values():
        for case in chapter['annotation'].get('unresolved_kinship_references', []):
            if case['person_id'] in ids or ids.intersection(case['reference_person_candidates']):
                neighbor_ids.update([case['person_id']] + case['reference_person_candidates'])
    neighbor_ids.update(h['inheritance']['predecessor_person_id'] for h in titles if 'inheritance' in h)
    date_ranges = [dict(e['normalized_date_range'], record_id=e['id'], person_id=e['person_id'],
                        date_role=role, event_type=e['event_type'])
                   for items, role in ((life_events, 'life_event'), (person_events, 'person_event'))
                   for e in items if 'normalized_date_range' in e]
    date_ranges += [dict(h['effective_period'][endpoint]['normalized_date_range'],
                         record_id=h['id'], person_id=h['person_id'], date_role='title_period',
                         endpoint=endpoint, title=h['title'])
                    for h in titles for endpoint in ('start', 'end')
                    if 'normalized_date_range' in h['effective_period'][endpoint]]
    date_ranges += [dict(a['normalized_date_range'], record_id=h['id'], attestation_id=a['id'],
                         person_id=h['person_id'], date_role='title_attestation', title=h['title'], usage=a['usage'])
                    for h in titles for a in h['attestations'] if 'normalized_date_range' in a]
    date_ranges += [dict(a['normalized_date_range'], record_id=a['id'], person_id=a['person_id'], date_role='age_attestation')
                    for a in ages if 'normalized_date_range' in a]
    def context_ids(value):
        found = set()
        if isinstance(value, dict):
            if isinstance(value.get('calendar_context'), dict):
                found.add(value['calendar_context']['context_id'])
            for item in value.values(): found.update(context_ids(item))
        elif isinstance(value, list):
            for item in value: found.update(context_ids(item))
        return found
    source_details = [d for r in records if r.get('record_type') == 'biographical_source_detail_set' for d in r['records'] if d['person_id'] in ids]
    source_temporal_attestations = [r for record in records if record.get('record_type') == 'source_temporal_attestation_set' for r in record['records'] if r['person_id'] in ids]
    unresolved_kinship_references = [r for chapter in chapters.values() for r in chapter['annotation'].get('unresolved_kinship_references', []) if r['person_id'] in ids or ids.intersection(r['reference_person_candidates'])]
    source_title_uses = [u for chapter in chapters.values() for u in chapter['annotation'].get('source_title_uses', []) if u['person_id'] in ids]
    used_context_ids = context_ids(titles + life_events + person_events)
    calendar_context_assertions = [c for record in records
        if record.get('record_type') == 'calendar_context_assertion_set'
        for c in record['records'] if c['id'] in used_context_ids]
    return {'format_version': '0.1', 'record_type': 'person_source_bundle', 'requested_person_id': requested_id,
            'canonical_person_id': person_id, 'id_aliases': people[person_id].get('id_aliases', []),
            'identity_policy': 'contextual_provisional' if include_provisional else 'exact_id',
            'person_ids': sorted(ids), 'persons': [people[p] for p in sorted(neighbor_ids)],
            'source_mention_summary': mention_summary,
            'most_mentioned_source_ids': most_mentioned,
            'mention_count_policy': {'scope': 'independent_fixed_witness_occurrences', 'raw_mentions_preserved': True, 'passage_count_scope': 'annotation_containers', 'explanation': '頻次依已驗同底本同位置去重；原始錨點完整保留，頻次不代表來源權威度。', 'included_kinds': ['paragraph', 'table_cell'], 'identity_policy': 'contextual_provisional' if include_provisional else 'exact_id', 'ties': 'all_maxima', 'frequency_is_not_authority': True},
            'kinship_interpretation_cases': kinship_cases,
            **({'source_title_uses': source_title_uses} if source_title_uses else {}),
            **({'source_details': source_details} if source_details else {}),
            **({'source_temporal_attestations': source_temporal_attestations} if source_temporal_attestations else {}),
            **({'unresolved_kinship_references': unresolved_kinship_references} if unresolved_kinship_references else {}),
            **({'relative_birth_order_decisions': order_decisions} if order_decisions else {}),
            **({'referent_interpretations': referent_cases} if referent_cases else {}),
            **({'title_proposals': title_proposals} if title_proposals else {}),
            **({'unresolved_title_attestations': unresolved_titles} if unresolved_titles else {}),
            **({'source_reading_cases': source_reading_cases} if source_reading_cases else {}),
            **({'unresolved_identity_cases': unresolved_cases} if unresolved_cases else {}),
            **({'resolved_identity_cases': resolved_cases} if resolved_cases else {}),
            'reported_variants': reported_variants,
            **({'preferred_title_readings':preferred_titles} if preferred_titles else {}),
            **({'default_profile_title':default_profile_title} if default_profile_title is not None else {}),
            **({'unresolved_relation_identity_groups': unresolved_relation_groups} if unresolved_relation_groups else {}),
            'family_tree_decisions': tree_decisions, 'preferred_relations': preferred_relations,
            'family_tree_policy': {'default': 'editorial_preferred', 'original_assertions_preserved': True,
                                   'unreviewed_conflicts_may_remain': True, 'runtime_ai_required': False},
            'family_paths': [dict(people[pid]['family_path'], person_id=pid) for pid in sorted(ids) if 'family_path' in people[pid]],
            **({'name_components': name_components} if name_components else {}),
            **({'preferred_name_component_readings': preferred_name_components} if preferred_name_components else {}),
            **({'person_events': person_events} if person_events else {}),
            **({'life_events': life_events} if life_events else {}),
            **({'chinese_civil_year_normalizations': [dict(e['chinese_civil_year'], record_id=e['id'], person_id=e['person_id'],
                date_role='life_event' if e['event_type'] in ('birth', 'death') else 'person_event', event_type=e['event_type'])
                for e in life_events + person_events if 'chinese_civil_year' in e]}
               if any('chinese_civil_year' in e for e in life_events + person_events) else {}),
            **({'life_event_date_decisions': date_decisions, 'selected_life_event_dates': selected_life_dates} if date_decisions else {}),
            **({'age_assertions': ages} if ages else {}),
            **({'family_count_reports': family_counts} if family_counts else {}),
            **({'age_difference_assertions': age_differences} if age_differences else {}),
            'mentions': mentions, 'relations': relations, 'title_holdings': titles, 'address_assertions': addresses,
            'table_occurrences': table_occurrences,
            **({'date_range_normalizations': date_ranges} if date_ranges else {}),
            **({'calendar_context_assertions': calendar_context_assertions} if calendar_context_assertions else {}),
            'date_normalizations': ([dict(a['normalized_date'], record_id=a['id'], person_id=a['person_id']) for a in addresses if 'normalized_date' in a]
                                    + [dict(e['normalized_date'], record_id=e['id'], person_id=e['person_id'], date_role='person_event', event_type=e['event_type']) for e in person_events if 'normalized_date' in e]
                                    + [dict(e['normalized_date'], record_id=e['id'], person_id=e['person_id'], date_role='life_event', event_type=e['event_type']) for e in life_events if 'normalized_date' in e]
                                    + [dict(a['normalized_date'], record_id=a['id'], person_id=a['person_id'], date_role='age_attestation') for a in ages if 'normalized_date' in a]
                                    + [dict(h['effective_period'][endpoint]['normalized_date'], record_id=h['id'],
                                            person_id=h['person_id'], endpoint=endpoint, title=h['title'])
                                       for h in titles for endpoint in ('start', 'end')
                                       if 'normalized_date' in h['effective_period'][endpoint]]
                                    + [dict(a['normalized_date'], record_id=h['id'], person_id=h['person_id'],
                                            attestation_id=a['id'], date_role='attestation', title=h['title'])
                                       for h in titles for a in h.get('attestations', []) if 'normalized_date' in a]),
            'birth_order_constraints': [dict(a['qualifiers'][key], assertion_id=a['id'], person_id=a['subject_person_id'], evidence=a['evidence'])
                                        for a in relations for key in ('birth_order', 'relative_birth_order')
                                        if key in a.get('qualifiers', {})],
            'preferred_birth_order_constraints': [dict(a['qualifiers'][key], assertion_id=a['id'], person_id=a['subject_person_id'], evidence=a['evidence'])
                                        for a in preferred_relations for key in ('birth_order', 'relative_birth_order')
                                        if key in a.get('qualifiers', {})],
            'identity_decisions': identities, 'equivalence_decisions': related_equivalences,
            **({'identity_distinctions': distinctions} if distinctions else {}),
            'passages': passages,
            **({'table_passages': list(table_passages.values())} if table_passages else {}),
            **({'table_column_references': list(date_columns.values())} if date_columns else {}),
            'sources': [{'chapter_id': cid, 'work_id': chapters[cid]['work_id'],
                         'book_id': chapters[cid]['book_id'], 'source_id': chapters[cid]['source_id'],
                         'source': chapters[cid]['source']} for cid in sorted(chapter_ids)]
                       + [{'chapter_id': tables[tid]['source']['chapter_id'],
                           'work_id': tables[tid]['source']['work_id'],
                           'book_id': tables[tid]['source']['book_id'],
                           'source_id': tables[tid]['source']['id'],
                           'source': tables[tid]['source']} for tid in sorted(cited_tables)],
            'time_policy': {'unknown_is_not_unbounded': True, 'attestation_is_not_tenure': True,
                            'date_expressions_are_not_normalized': False, 'date_normalization_coverage': 'partial',
                            'normalized_year_numbering': 'astronomical',
                            'civil_year_label_field': 'chinese_civil_year',
                            'civil_year_label_coverage': 'partial',
                            'regnal_year_crosses_ce_year_is_gregorian_projection': True}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('person_id')
    parser.add_argument('--include-provisional', action='store_true', help='明示採用已記錄的暫定跨篇同指，仍保留判讀與原 ID')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = bundle(args.person_id, include_provisional=args.include_provisional)
    except ValueError as error:
        parser.error(str(error))
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
