#!/usr/bin/env python3
"""匯出家譜檢視器所需的單一人物來源包；純 Python，無 AI 呼叫。"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_catalog(root=ROOT):
    people = {p['id']: p for p in json.loads((root / 'registry/persons.json').read_text())['persons']}
    records = [json.loads(path.read_text()) for path in sorted((root / 'corpus').glob('*/*.json'))]
    return people, records


def bundle(person_id, root=ROOT, include_provisional=False, catalog=None):
    people, records = catalog if catalog is not None else load_catalog(root)
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
    mentions, relations, titles, identities, addresses = [], [], [], [], []
    chapters, paragraphs = {}, {}
    for record in records:
        kind = record.get('record_type')
        if kind == 'marked_chapter':
            chapters[record['id']] = record
            for paragraph in record['paragraphs']:
                paragraphs[paragraph['id']] = (record, paragraph)
                for mention in paragraph['mentions']:
                    if mention.get('person_id') in ids:
                        mentions.append(dict(mention, paragraph_id=paragraph['id'], chapter_id=record['id']))
        elif kind == 'person_assertion_set':
            relations.extend(a for a in record['assertions'] if a['subject_person_id'] in ids or a['object_person_id'] in ids)
        elif kind == 'person_address_assertion_set':
            addresses.extend(a for a in record['assertions'] if a['person_id'] in ids)
        elif kind == 'title_holding_assertion_set':
            titles.extend(t for t in record['holdings'] if t['person_id'] in ids)
        elif 'decisions' in record and kind != 'person_equivalence_set':
            identities.extend(d for d in record['decisions'] if d.get('person_id') in ids)
    paragraph_ids = {m['paragraph_id'] for m in mentions}
    for record in relations + titles + identities + addresses + related_equivalences:
        paragraph_ids.update(e['paragraph_id'] for e in record.get('evidence', []))
        paragraph_ids.update(e['paragraph_id'] for e in record.get('normalized_date', {}).get('evidence', []))
    passages = []
    for pid in sorted(paragraph_ids):
        chapter, paragraph = paragraphs[pid]
        passages.append(dict(paragraph, chapter_id=chapter['id'], book_id=chapter['book_id'],
                             work_id=chapter['work_id'], source_id=chapter['source_id']))
    chapter_ids = {p['chapter_id'] for p in passages}
    # Counts describe annotated occurrences, not source authority or independent witnesses.
    source_mentions = {}
    for mention in mentions:
        chapter = chapters[mention['chapter_id']]
        key = chapter['source_id']
        row = source_mentions.setdefault(key, {
            'source_id': key, 'work_id': chapter['work_id'],
            'book_id': chapter['book_id'], 'chapter_id': chapter['id'],
            'mention_count': 0, 'mention_ids': [], 'paragraph_ids': set()})
        row['mention_count'] += 1
        row['mention_ids'].append(mention['id'])
        row['paragraph_ids'].add(mention['paragraph_id'])
    mention_summary = []
    for row in source_mentions.values():
        row['paragraph_ids'] = sorted(row['paragraph_ids'])
        row['passage_count'] = len(row['paragraph_ids'])
        row['mention_ids'].sort()
        mention_summary.append(row)
    mention_summary.sort(key=lambda row: (-row['mention_count'], row['source_id']))
    maximum = mention_summary[0]['mention_count'] if mention_summary else 0
    most_mentioned = [row['source_id'] for row in mention_summary if row['mention_count'] == maximum]
    neighbor_ids = ids | {a[k] for a in relations for k in ('subject_person_id', 'object_person_id')}
    return {'format_version': '0.1', 'record_type': 'person_source_bundle', 'requested_person_id': person_id,
            'identity_policy': 'contextual_provisional' if include_provisional else 'exact_id',
            'person_ids': sorted(ids), 'persons': [people[p] for p in sorted(neighbor_ids)],
            'source_mention_summary': mention_summary,
            'most_mentioned_source_ids': most_mentioned,
            'mention_count_policy': {'scope': 'currently_annotated_mentions', 'identity_policy': 'contextual_provisional' if include_provisional else 'exact_id', 'ties': 'all_maxima', 'frequency_is_not_authority': True},
            'family_paths': [dict(people[pid]['family_path'], person_id=pid) for pid in sorted(ids) if 'family_path' in people[pid]],
            'mentions': mentions, 'relations': relations, 'title_holdings': titles, 'address_assertions': addresses,
            'date_normalizations': [dict(a['normalized_date'], record_id=a['id'], person_id=a['person_id']) for a in addresses if 'normalized_date' in a],
            'birth_order_constraints': [dict(a['qualifiers'][key], assertion_id=a['id'], person_id=a['subject_person_id'], evidence=a['evidence'])
                                        for a in relations for key in ('birth_order', 'relative_birth_order')
                                        if key in a.get('qualifiers', {})],
            'identity_decisions': identities, 'equivalence_decisions': related_equivalences,
            'passages': passages,
            'sources': [{'chapter_id': cid, 'work_id': chapters[cid]['work_id'],
                         'book_id': chapters[cid]['book_id'], 'source_id': chapters[cid]['source_id'],
                         'source': chapters[cid]['source']} for cid in sorted(chapter_ids)],
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
