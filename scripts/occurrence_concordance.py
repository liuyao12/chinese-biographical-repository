"""Explicit fixed-witness occurrence aliases; raw annotations are never removed."""
import hashlib
import json
from pathlib import Path


def occurrence_catalog(root, records, person_ids=None):
    for r in records:
        if r.get('record_type') != 'source_occurrence_concordance_set' and any(isinstance(item, dict) and item.get('kind') in ('resolved_person_occurrence_alias','unresolved_text_span_correspondence') for item in r.get('records', [])):
            raise ValueError('來源位置對應：對應集類型不符')
    sets = [r for r in records if r.get('record_type') == 'source_occurrence_concordance_set']
    if not sets:
        return {}, {}
    relevant = {item[end]['chapter_id'] for r in sets for item in r['records'] for end in ('canonical','duplicate')}
    chapters = {r['id']: r for r in records if r.get('record_type') == 'marked_chapter' and r['id'] in relevant}
    mentions = {m['id']: (c, p, m) for c in chapters.values()
                for p in c['paragraphs'] for m in p['mentions']}
    aliases, details, used, record_ids = {}, {}, set(), set()
    if person_ids is None:
        person_ids = {p['id'] for p in json.loads((Path(root)/'registry/persons.json').read_text())['persons']}
    projections = {}
    def need(value, message):
        if not value:
            raise ValueError('來源位置對應：' + message)
    def projection(chapter, paragraph, mode, lines):
        key = (chapter['id'], paragraph['id'], mode)
        if key in projections:
            return projections[key]
        if mode == 'literal_witness_fragments':
            points, text = [], ''
            for f in paragraph['witness_fragments']:
                a, b, n = f['raw_line_start'], f['raw_line_end'], f['line']
                need(type(n) is int and 1 <= n <= len(lines) and type(a) is int
                     and type(b) is int and 0 <= a < b <= len(lines[n-1]), '原行欄位無效')
                need(f['text'] == f['raw_fragment'] == lines[n-1][a:b], 'literal原行不符')
                text += f['text']; points.extend((n, i) for i in range(a, b))
        elif mode == 'kanripo_parenthesized_commentary_body_projection':
            try: from .witness_projection import body_positions
            except ImportError: from witness_projection import body_positions
            points = body_positions(chapter, paragraph, lines); text = paragraph['text']
        elif mode == 'repository_raw_projection_ref':
            try: from .witness_projection import repository_positions
            except ImportError: from witness_projection import repository_positions
            points, digest = repository_positions(root, paragraph, lines)
            need(digest == chapter['source']['response_sha256'], '投影raw SHA不符')
            text = paragraph['text']
        else:
            raise ValueError('來源位置對應：未知projection')
        need(text == paragraph['text'], 'projection不是原段正文')
        projections[key] = points
        return points
    for record in records:
        if record.get('record_type') != 'source_occurrence_concordance_set':
            continue
        need(record.get('format_version') == '0.2' and record.get('human_reviewed') is False,
             '集合格式或覆核狀態無效')
        source = record['source']; path = Path(source['raw_path'])
        need(not path.is_absolute() and path.parts[:2] == ('sources', 'witnesses')
             and '..' not in path.parts, 'raw須在可攜sources/witnesses')
        raw_path = (Path(root)/path).resolve()
        need(raw_path.is_relative_to(Path(root).resolve()), 'raw路徑越界')
        raw = raw_path.read_bytes(); need(hashlib.sha256(raw).hexdigest() == source['raw_file_sha256'], 'raw SHA不符')
        need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == source['source_blob_sha'], 'raw git blob不符')
        lines = raw.decode('utf-8').splitlines()
        for item in record['records']:
            need(item.get('human_reviewed') is False, '單筆覆核狀態不符')
            need(isinstance(item['id'], str) and bool(item['id']) and item['id'] not in record_ids, 'record ID無效或重複'); record_ids.add(item['id'])
            canonical, duplicate = item['canonical_mention_id'], item['duplicate_mention_id']
            need(canonical != duplicate and canonical not in used and duplicate not in used,
                 '自連、循環、鏈式或一對多／重複連結')
            used.update((canonical, duplicate))
            need(canonical in mentions and duplicate in mentions, '未知mention')
            cc, cp, cm = mentions[canonical]; dc, dp, dm = mentions[duplicate]
            need(cc['source_id'] == dc['source_id'] == source['source_id'], '跨source')
            need(cc['source'].get('source_blob_sha') == dc['source'].get('source_blob_sha') == source['source_blob_sha']
                 and cc['source'].get('permalink') == dc['source'].get('permalink') == source['url'], 'chapter/raw固定見證不符')
            need(cc['source']['revision_id'] == dc['source']['revision_id'] == source['revision_id'], '跨revision')
            need(cc['source'].get('response_sha256') == source['raw_file_sha256']
                 and dc['source'].get('response_sha256') == source['raw_file_sha256'], 'chapter/raw SHA不符')
            for endpoint, c, p, m in [('canonical',cc,cp,cm), ('duplicate',dc,dp,dm)]:
                e = item[endpoint]
                need(e == {'chapter_id':c['id'], 'paragraph_id':p['id'], 'start':m['start'], 'end':m['end']}, '雙端span不符')
                need(type(m['start']) is int and type(m['end']) is int and 0 <= m['start'] < m['end'] <= len(p['text'])
                     and p['text'][m['start']:m['end']] == m['surface'], '原surface/span不符')
            need(cm['surface'] == dm['surface'] == item['surface'], '雙端surface不同')
            kind = item['kind']
            if kind == 'resolved_person_occurrence_alias':
                need(cm.get('kind') == dm.get('kind') == 'person' and bool(item['person_id'])
                     and item['person_id'] in person_ids and cm.get('person_id') == dm.get('person_id') == item['person_id'], '錯人、同名異ID或未解個體')
            else:
                need(kind == 'unresolved_text_span_correspondence' and cm.get('kind') == dm.get('kind') == 'unresolved'
                     and cm.get('person_id') is None and dm.get('person_id') is None and item['person_id'] is None,
                     '未解對應不能冒作個人')
            cpoints = projection(cc, cp, item['canonical_projection'], lines)[cm['start']:cm['end']]
            dpoints = projection(dc, dp, item['duplicate_projection'], lines)[dm['start']:dm['end']]
            need(all(type(p['line']) is int and type(p['column']) is int for p in item['literal_character_positions']), '原行欄位須整數')
            declared = [(p['line'],p['column']) for p in item['literal_character_positions']]
            need(cpoints == dpoints == declared, '不同raw位置，不得按同字去重')
            if kind == 'resolved_person_occurrence_alias':
                aliases[duplicate] = canonical
                details[canonical] = {'concordance_id':item['id'], 'source_revision':source['revision_id'],
                    'literal_character_positions':item['literal_character_positions']}
    return aliases, details


def validate(root):
    try:
        records = [json.loads(p.read_text()) for p in (Path(root)/'corpus').glob('*/*.json')]
        occurrence_catalog(root, records)
        return []
    except (ValueError, KeyError, TypeError, OSError, StopIteration, AttributeError, IndexError) as exc:
        return ['來源位置對應無效：' + str(exc)]


def summarize_occurrences(mentions, table_occurrences, chapters, root, records, person_ids=None):
    aliases, details = occurrence_catalog(root, records, person_ids)
    rows = {}
    for mention, table in [(m, False) for m in mentions] + [(m, True) for m in table_occurrences]:
        chapter = None if table else chapters[mention['chapter_id']]
        sid = mention['source_id'] if table else chapter['source_id']
        row = rows.setdefault(sid, {'source_id':sid,
            'work_id':mention['work_id'] if table else chapter['work_id'],
            'book_id':mention['book_id'] if table else chapter['book_id'],
            'chapter_id':mention['chapter_id'] if table else chapter['id'],
            'raw_mention_count':0, 'mention_ids':[], 'paragraph_ids':set(), 'table_cell_ids':set(), '_groups':{}})
        mid = mention['id']; canonical = aliases.get(mid, mid)
        row['raw_mention_count'] += 1; row['mention_ids'].append(mid)
        row['table_cell_ids' if table else 'paragraph_ids'].add(mention['table_cell_id' if table else 'paragraph_id'])
        group = row['_groups'].setdefault(canonical, {'canonical_mention_id':canonical, 'mention_ids':[],
            'kind':'table_cell' if table else 'paragraph', **details.get(canonical,{})})
        group['mention_ids'].append(mid)
    for row in rows.values():
        groups = list(row.pop('_groups').values())
        for group in groups: group['mention_ids'].sort()
        row['occurrence_groups'] = sorted(groups,key=lambda g:g['canonical_mention_id'])
        row['mention_count'] = len(groups)
        row['duplicate_mention_count'] = row['raw_mention_count'] - len(groups)
        row['paragraph_occurrence_count'] = sum(g['kind']=='paragraph' for g in groups)
        row['table_occurrence_count'] = sum(g['kind']=='table_cell' for g in groups)
        for key in ['paragraph_ids','table_cell_ids','mention_ids']: row[key] = sorted(row[key])
        row['passage_count'] = len(row['paragraph_ids']) + len(row['table_cell_ids'])
        row['passage_count_scope'] = 'annotation_containers_not_independent_witness_passages'
        row['count_explanation'] = f"{row['mention_count']}處獨立位置，{row['raw_mention_count']}個原始錨點；{row['duplicate_mention_count']}項為同底本同位置重出。頻次不是來源權威度。"
    result = sorted(rows.values(),key=lambda r:(-r['mention_count'],r['source_id']))
    maximum = result[0]['mention_count'] if result else 0
    return result, [r['source_id'] for r in result if r['mention_count']==maximum]


def index_counts(result):
    rows = result['source_mention_summary']
    return {'mention_count':sum(r['mention_count'] for r in rows),
        'raw_mention_count':len(result['mentions'])+len(result['table_occurrences']),
        'duplicate_mention_count':sum(r.get('duplicate_mention_count',0) for r in rows),
        'paragraph_mention_count':sum(r['paragraph_occurrence_count'] for r in rows),
        'table_mention_count':sum(r['table_occurrence_count'] for r in rows),
        'source_count':len(result['sources']), 'most_mentioned_source_ids':result['most_mentioned_source_ids']}
