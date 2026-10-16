"""以固定表格核查親屬、姓名與稱號紀年；不重建或改寫原表。"""
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


def table_name_component_errors(name, tables):
    """姓名組件須引用同人的固定年表格及原名錨點。"""
    table = tables.get(name.get('table_id'))
    if not table:
        return ['姓名組件表格不存在']
    source = table['source']
    errors = []
    if ('paragraph_id' in name or name.get('kind') != 'table_cell'
            or any(name.get(key) != source.get(source_key) for key, source_key in
                   [('work_id','work_id'), ('book_id','book_id'), ('chapter_id','chapter_id'),
                    ('source_id','id'), ('source_revision','revision')])):
        errors.append('姓名組件表格來源或固定修訂不符')
    cell = table_cell(table, name.get('table_cell_id'))
    if not cell or not name.get('quote') or name['quote'] != cell['text']:
        return errors + ['姓名組件表格引句須完整對應原格']
    mention = next((m for m in cell.get('person_mentions', [])
                    if m['id'] == name.get('person_mention_id')), None)
    spelling = ''.join(name.get(key) or '' for key in ('surname', 'ming'))
    if (not mention or mention.get('person_id') != name.get('person_id')
            or not spelling or mention.get('surface') != spelling
            or type(mention.get('start')) is not int or type(mention.get('end')) is not int
            or not 0 <= mention['start'] < mention['end'] <= len(cell['text'])
            or cell['text'][mention['start']:mention['end']] != spelling):
        errors.append('姓名組件須有同人原名錨點，不得由職爵或他人補名')
    return errors


def table_title_range_errors(value, holding, endpoint, tables):
    errors=[];event=value.get('table_event');parallel=value.get('parallel_event')
    if not isinstance(event,dict)or not isinstance(parallel,dict):return ['稱號平行跨年紀年須有固定表格事件']
    table=tables.get(event.get('table_id'))
    if not table:return ['稱號平行紀年表格不存在']
    source=table['source'];cell=table_cell(table,event.get('table_cell_id'))
    if event.get('kind')!='table_cell'or any(event.get(k)!=source.get(v)for k,v in [('work_id','work_id'),('book_id','book_id'),('chapter_id','chapter_id'),('source_id','id'),('source_revision','revision')]):errors.append('稱號平行紀年表格來源或固定修訂不符')
    if not cell or not event.get('quote')or event['quote']!=cell['text']:return errors+['稱號平行紀年引句須完整對應原格']
    mention=next((m for m in cell.get('person_mentions',[])if m['id']==event.get('person_mention_id')),None);term=event.get('event_source_term')
    valid=(endpoint=='start'and holding.get('kind')=='royal_rank'and holding.get('mode')in ('grant','accession')and event.get('event_type')==holding.get('mode')and isinstance(term,str)and '初王'in term and term in cell['text']and bool(mention)and mention.get('person_id')==holding.get('person_id'))
    if valid:
        valid=(type(mention.get('start'))is int and type(mention.get('end'))is int and cell['text'][mention['start']:mention['end']]==mention.get('surface')and any(i<=mention['start']and mention['end']<=i+len(term)for i in range(len(cell['text']))if cell['text'].startswith(term,i)))
    if not valid:errors.append('稱號平行授封事件須有同人原名錨點與明示初王原詞')
    regnal=table_cell(table,event.get('regnal_year_cell_id'));digital=table_cell(table,event.get('digital_year_cell_id'))
    row=cell['id'].rpartition('-c')[0]
    if not regnal or not digital or regnal.get('column')!=1 or digital.get('column')!=0 or any(c['id'].rpartition('-c')[0]!=row for c in [regnal,digital]):return errors+['稱號平行紀年須引用同列原年欄及數位對照欄']
    text=digital['text'];latest=value.get('latest',{})
    if not text.isascii()or not text.isdigit()or latest.get('era')!='BCE'or latest.get('era_year')!=int(text):errors.append('稱號平行紀年西元對照與範圍端點不符')
    url=source['revision_url']
    if parallel.get('reference_url')!=url or parallel.get('reference_year_url',url)!=url or parallel.get('reference_event_quote')!=cell['text']or parallel.get('reference_year_quote')!=digital['text']:errors.append('稱號平行紀年對讀引句或固定網址不符')
    refs=value.get('references',[])
    for point,scope in [(cell,'received_parallel_event'),(regnal,'received_regnal_year_attestation'),(digital,'digital_editorial_regnal_year_equivalence_only')]:
        if not any(ref.get('url')==url and ref.get('table_cell_id')==point['id']and ref.get('quote')==point['text']and ref.get('scope')==scope for ref in refs):errors.append('稱號平行紀年須分列相符表格事件與年欄')
    for ref in refs:
        if ref.get('table_cell_id'):
            point=table_cell(table,ref['table_cell_id'])
            if not point or ref.get('url')!=url or ref.get('quote')!=point['text']:errors.append('稱號平行紀年表格參照不符原格')
    return errors
