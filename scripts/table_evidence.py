"""以既有表格格位核查親屬引句；不重建或改寫原表。"""
import json
from pathlib import Path


def load_tables(root):
    root = Path(root)
    index = root / 'data/historical-tables/index.json'
    if not index.exists():
        return {}
    tables = {}
    directory = index.parent.resolve()
    for item in json.loads(index.read_text())['tables']:
        path = (root / item['path']).resolve()
        if path.parent != directory or path.name != item['id'] + '.json':
            raise ValueError('表格證據路徑與索引不符')
        table = json.loads(path.read_text())
        if table['id'] != item['id'] or table['id'] in tables:
            raise ValueError('表格證據ID與索引不符或重複')
        tables[table['id']] = table
    return tables


def table_cell(table, cell_id):
    return next((cell for fragment in table['fragments']
                 for row in fragment['rows'] for cell in row['cells']
                 if cell['id'] == cell_id), None)


def table_evidence_errors(evidence, tables, subject, object_id):
    table = tables.get(evidence.get('table_id'))
    if not table:
        return ['親屬表格證據不存在']
    source = table['source']
    errors = []
    if (evidence.get('kind') != 'table_cell' or 'paragraph_id' in evidence
            or any(evidence.get(key) != source.get(source_key)
                   for key, source_key in [('work_id', 'work_id'), ('book_id', 'book_id'),
                                           ('chapter_id', 'chapter_id'), ('source_id', 'id'),
                                           ('source_revision', 'revision')])):
        errors.append('親屬表格證據來源或固定修訂不符')
    cell = table_cell(table, evidence.get('table_cell_id'))
    if not cell or not evidence.get('quote') or evidence['quote'] != cell['text']:
        return errors + ['親屬表格引句須完整對應原格']
    mentions = {m['id']: m for m in cell.get('person_mentions', [])}
    for key, pid in [('subject_mention_id', subject), ('object_mention_id', object_id)]:
        mention = mentions.get(evidence.get(key))
        if (not mention or mention.get('person_id') != pid
                or not isinstance(mention.get('start'), int) or not isinstance(mention.get('end'), int)
                or not 0 <= mention['start'] < mention['end'] <= len(cell['text'])
                or cell['text'][mention['start']:mention['end']] != mention.get('surface')):
            errors.append('親屬表格端點須有相符的逐人錨點')
            break
    return errors
