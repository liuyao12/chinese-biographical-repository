#!/usr/bin/env python3
"""匯出家譜檢視器所需的單一人物來源包；純 Python，無 AI 呼叫。"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
    return people, records


def bundle(person_id, root=ROOT, include_provisional=False, catalog=None):
    people, records = catalog if catalog is not None else load_catalog(root)
    requested_id = person_id
    aliases = {alias: pid for pid, person in people.items() for alias in person.get('id_aliases', [])}
    person_id = aliases.get(person_id, person_id)
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
    table_occurrences, occurrence_cells = [], {}
    name_components = []
    chapters, paragraphs, tables = {}, {}, {}
    for record in records:
        kind = record.get('record_type')
        if kind == 'marked_chapter':
            chapters[record['id']] = record
            ages.extend(a for a in record['annotation'].get('age_assertions', []) if a['person_id'] in ids)
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
        elif kind == 'person_life_event_assertion_set':
            life_events.extend(e for e in record['events'] if e['person_id'] in ids)
        elif kind == 'person_event_assertion_set':
            person_events.extend(e for e in record['events'] if e['person_id'] in ids)
        elif kind == 'title_holding_assertion_set':
            titles.extend(t for t in record['holdings'] if t['person_id'] in ids)
        elif kind == 'person_name_component_set':
            name_components.extend(n for n in record['records'] if n['person_id'] in ids)
        elif 'decisions' in record and kind not in ('person_equivalence_set', 'family_tree_decision_set'):
            identities.extend(d for d in record['decisions'] if d.get('person_id') in ids)
    enriched_names = []
    for name in name_components:
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
    date_decisions = [d for r in records if r.get('record_type') == 'life_event_date_decision_set'
                      for d in r['decisions'] if set(d['person_ids']).issubset(ids)]
    try:
        from .life_event_dates import selected_dates
    except ImportError:
        from life_event_dates import selected_dates
    selected_life_dates = selected_dates(life_events, date_decisions)
    kinship_cases = [case for chapter in chapters.values() for case in chapter['annotation'].get('kinship_interpretation_cases', []) if ids.intersection((case['subject_person_id'], case['object_person_id']))]
    unresolved_cases = [dict(case, chapter_id=chapter['id'], source_id=chapter['source_id']) for chapter in chapters.values() for case in chapter['annotation'].get('unresolved_identity_cases', []) if ids.intersection(case['candidate_person_ids'])]
    title_proposals = [proposal for chapter in chapters.values() for proposal in chapter['annotation'].get('title_proposals', []) if proposal['person_id'] in ids]
    resolved_cases = [dict(case, chapter_id=chapter['id'], source_id=chapter['source_id']) for chapter in chapters.values() for case in chapter['annotation'].get('resolved_identity_cases', []) if case['person_id'] in ids]
    reported_variants = [variant for chapter in chapters.values() for variant in chapter['annotation'].get('reported_variants', []) if ids.intersection(variant['person_ids'])]
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
    excluded = {aid for decision in tree_decisions for aid in decision['excluded_assertion_ids']}
    preferred_relations = []
    for assertion in relations:
        if assertion['id'] in excluded:
            continue
        preferred = dict(assertion)
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
    for record in relations + titles + identities + addresses + life_events + person_events + ages + age_differences + related_equivalences + tree_decisions:
        paragraph_ids.update(e['paragraph_id'] for e in record.get('evidence', []) if e.get('kind') != 'table_cell')
        paragraph_ids.update(e['paragraph_id'] for e in record.get('normalized_date', {}).get('evidence', []))
        paragraph_ids.update(e['paragraph_id'] for e in record.get('normalized_date_range', {}).get('evidence', []))
        for evidence in record.get('evidence', []):
            context = evidence.get('context', {})
            if context.get('paragraph_id'):
                paragraph_ids.add(context['paragraph_id'])
            paragraph_ids.update(context.get('intervening_paragraph_ids', []))
    for holding in titles:
        for attestation in holding.get('attestations', []):
            paragraph_ids.update(e['paragraph_id'] for e in attestation.get('normalized_date', {}).get('evidence', []))
        for boundary in holding['effective_period'].values():
            paragraph_ids.update(e['paragraph_id'] for e in boundary['evidence'])
            paragraph_ids.update(e['paragraph_id'] for e in boundary.get('normalized_date', {}).get('evidence', []))
    passages = []
    for pid in sorted(paragraph_ids):
        chapter, paragraph = paragraphs[pid]
        passages.append(dict(paragraph, chapter_id=chapter['id'], book_id=chapter['book_id'],
                             work_id=chapter['work_id'], source_id=chapter['source_id']))
    chapter_ids = {p['chapter_id'] for p in passages}
    table_passages = dict(occurrence_cells)
    cited_tables = {m['table_id'] for m in table_occurrences}
    for relation in relations:
        for evidence in relation['evidence']:
            if evidence.get('kind') != 'table_cell':
                continue
            try:
                from .table_evidence import table_cell, table_evidence_errors
            except ImportError:
                from table_evidence import table_cell, table_evidence_errors
            errors = table_evidence_errors(evidence, tables, relation['subject_person_id'], relation['object_person_id'])
            if errors:
                raise ValueError('；'.join(errors))
            table = tables[evidence['table_id']]
            cell = table_cell(table, evidence['table_cell_id'])
            cited_tables.add(table['id'])
            table_passages.setdefault(cell['id'], dict(cell, table_id=table['id'],
                work_id=table['source']['work_id'], book_id=table['source']['book_id'],
                chapter_id=table['source']['chapter_id'], source_id=table['source']['id']))
    # Counts describe annotated occurrences, not source authority or independent witnesses.
    source_mentions = {}
    for mention in mentions:
        chapter = chapters[mention['chapter_id']]
        key = chapter['source_id']
        row = source_mentions.setdefault(key, {
            'source_id': key, 'work_id': chapter['work_id'],
            'book_id': chapter['book_id'], 'chapter_id': chapter['id'],
            'mention_count': 0, 'mention_ids': [], 'paragraph_ids': set(), 'table_cell_ids': set()})
        row['mention_count'] += 1
        row['mention_ids'].append(mention['id'])
        row['paragraph_ids'].add(mention['paragraph_id'])
    for mention in table_occurrences:
        key = mention['source_id']
        row = source_mentions.setdefault(key, {
            'source_id': key, 'work_id': mention['work_id'],
            'book_id': mention['book_id'], 'chapter_id': mention['chapter_id'],
            'mention_count': 0, 'mention_ids': [], 'paragraph_ids': set(), 'table_cell_ids': set()})
        row['mention_count'] += 1
        row['mention_ids'].append(mention['id'])
        row['table_cell_ids'].add(mention['table_cell_id'])
    mention_summary = []
    for row in source_mentions.values():
        row['paragraph_ids'] = sorted(row['paragraph_ids'])
        row['table_cell_ids'] = sorted(row['table_cell_ids'])
        row['passage_count'] = len(row['paragraph_ids']) + len(row['table_cell_ids'])
        row['mention_ids'].sort()
        mention_summary.append(row)
    mention_summary.sort(key=lambda row: (-row['mention_count'], row['source_id']))
    maximum = mention_summary[0]['mention_count'] if mention_summary else 0
    most_mentioned = [row['source_id'] for row in mention_summary if row['mention_count'] == maximum]
    neighbor_ids = ids | {a[k] for a in relations for k in ('subject_person_id', 'object_person_id')}
    neighbor_ids.update(p for decision in tree_decisions for p in decision['participant_person_ids'])
    neighbor_ids.update(p for case in unresolved_cases for p in case['candidate_person_ids'])
    neighbor_ids.update(p for case in kinship_cases for p in (case['subject_person_id'], case['object_person_id']))
    date_ranges = [dict(e['normalized_date_range'], record_id=e['id'], person_id=e['person_id'],
                        date_role=role, event_type=e['event_type'])
                   for items, role in ((life_events, 'life_event'), (person_events, 'person_event'))
                   for e in items if 'normalized_date_range' in e]
    date_ranges += [dict(h['effective_period'][endpoint]['normalized_date_range'],
                         record_id=h['id'], person_id=h['person_id'], date_role='title_period',
                         endpoint=endpoint, title=h['title'])
                    for h in titles for endpoint in ('start', 'end')
                    if 'normalized_date_range' in h['effective_period'][endpoint]]
    return {'format_version': '0.1', 'record_type': 'person_source_bundle', 'requested_person_id': requested_id,
            'canonical_person_id': person_id, 'id_aliases': people[person_id].get('id_aliases', []),
            'identity_policy': 'contextual_provisional' if include_provisional else 'exact_id',
            'person_ids': sorted(ids), 'persons': [people[p] for p in sorted(neighbor_ids)],
            'source_mention_summary': mention_summary,
            'most_mentioned_source_ids': most_mentioned,
            'mention_count_policy': {'scope': 'currently_annotated_mentions', 'included_kinds': ['paragraph', 'table_cell'], 'identity_policy': 'contextual_provisional' if include_provisional else 'exact_id', 'ties': 'all_maxima', 'frequency_is_not_authority': True},
            'kinship_interpretation_cases': kinship_cases,
            **({'title_proposals': title_proposals} if title_proposals else {}),
            **({'unresolved_identity_cases': unresolved_cases} if unresolved_cases else {}),
            **({'resolved_identity_cases': resolved_cases} if resolved_cases else {}),
            'reported_variants': reported_variants,
            **({'preferred_title_readings':preferred_titles} if preferred_titles else {}),
            'family_tree_decisions': tree_decisions, 'preferred_relations': preferred_relations,
            'family_tree_policy': {'default': 'editorial_preferred', 'original_assertions_preserved': True,
                                   'unreviewed_conflicts_may_remain': True, 'runtime_ai_required': False},
            'family_paths': [dict(people[pid]['family_path'], person_id=pid) for pid in sorted(ids) if 'family_path' in people[pid]],
            **({'name_components': name_components} if name_components else {}),
            **({'person_events': person_events} if person_events else {}),
            **({'life_events': life_events} if life_events else {}),
            **({'life_event_date_decisions': date_decisions, 'selected_life_event_dates': selected_life_dates} if date_decisions else {}),
            **({'age_assertions': ages} if ages else {}),
            **({'age_difference_assertions': age_differences} if age_differences else {}),
            'mentions': mentions, 'relations': relations, 'title_holdings': titles, 'address_assertions': addresses,
            'table_occurrences': table_occurrences,
            **({'date_range_normalizations': date_ranges} if date_ranges else {}),
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
            'passages': passages,
            **({'table_passages': list(table_passages.values())} if table_passages else {}),
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
                            'normalized_year_numbering': 'astronomical'}}


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
