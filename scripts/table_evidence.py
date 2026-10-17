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


def table_title_range_errors(value, holding, endpoint, tables, boundary=None):
    """Bind an explicit title event to received table text and a separate year row."""
    errors = []
    event, parallel = value.get('table_event'), value.get('parallel_event')
    if not isinstance(event, dict) or not isinstance(parallel, dict):
        return ['稱號平行跨年紀年須有固定表格事件']
    table = tables.get(event.get('table_id'))
    if not table:
        return ['稱號平行紀年表格不存在']
    source = table['source']
    source_fields = [('work_id', 'work_id'), ('book_id', 'book_id'),
                     ('chapter_id', 'chapter_id'), ('source_id', 'id'),
                     ('source_revision', 'revision')]
    if event.get('kind') != 'table_cell' or any(event.get(k) != source.get(v) for k, v in source_fields):
        errors.append('稱號平行紀年表格來源或固定修訂不符')
    cell = table_cell(table, event.get('table_cell_id'))
    if not cell or not event.get('quote') or event['quote'] != cell['text']:
        return errors + ['稱號平行紀年引句須完整對應原格']
    mention = next((m for m in cell.get('person_mentions', [])
                    if m['id'] == event.get('person_mention_id')), None)
    term = event.get('event_source_term')
    named = (bool(mention) and mention.get('person_id') == holding.get('person_id')
             and type(mention.get('start')) is int and type(mention.get('end')) is int
             and cell['text'][mention['start']:mention['end']] == mention.get('surface')
             and isinstance(term, str) and bool(term) and term in cell['text']
             and any(i <= mention['start'] and mention['end'] <= i + len(term)
                     for i in range(len(cell['text'])) if cell['text'].startswith(term, i)))
    kind, mode, etype = holding.get('kind'), holding.get('mode'), event.get('event_type')
    if boundary is not None and etype != boundary.get('event_type'):
        errors.append('稱號平行事件種類與本文端點不符')
    valid = False
    if named and endpoint == 'start' and etype == mode:
        if kind == 'royal_rank' and mode in ('grant', 'accession'):
            valid = '初王' in term
        elif kind in ('office', 'noble_rank') and mode == 'grant':
            phrase = ('為' if kind == 'office' else '封') + holding['title']
            valid = event.get('title_source_term') == phrase and phrase in term
            if valid:
                # An earlier office in the same cell is not the new office. The
                # named subject must precede this explicit grant, without another
                # marked person becoming the intervening subject.
                occurrences = [i for i in range(len(cell['text']))
                               if cell['text'].startswith(phrase, i)
                               and mention['end'] <= i]
                valid = any(not any(other.get('person_id') != holding['person_id']
                                    and mention['end'] <= other['start'] < i
                                    for other in cell.get('person_mentions', []))
                            for i in occurrences)
        elif kind == 'noble_rank' and mode == 'accession':
            name_cell = table_cell(table, event.get('noble_name_cell_id'))
            valid = (bool(name_cell)
                     and name_cell['id'].rpartition('-c')[0] == cell['id'].rpartition('-c')[0]
                     and name_cell['text'].rstrip('。') + '侯' == holding['title']
                     and '侯' + mention['surface'] + '元年' in term)
    elif named and endpoint == 'end' and kind == 'noble_rank' and etype in ('deposition', 'abolition'):
        name_cell = table_cell(table, event.get('noble_name_cell_id'))
        valid = (bool(name_cell)
                 and name_cell['id'].rpartition('-c')[0] == cell['id'].rpartition('-c')[0]
                 and name_cell['text'].rstrip('。') + '侯' == holding['title']
                 and '侯' + mention['surface'] in term
                 and any(word in term for word in ('國除', '失侯')))
    if not valid:
        errors.append('稱號平行授封事件須有同人原名錨點與明示初王原詞' if kind == 'royal_rank'
                      else '稱號平行事件須有同人錨點及明示授任、嗣侯或失侯原詞')

    def column_for(t, point):
        for fragment in t['fragments']:
            if any(c['id'] == point['id'] for row in fragment['rows'] for c in row['cells']):
                return next((col for i, col in enumerate(fragment.get('columns', []))
                             if i == point.get('column')), None)
        return None

    mapping = event.get('year_mapping')
    if mapping is None:
        year_table = table
        regnal_id, digital_id = event.get('regnal_year_cell_id'), event.get('digital_year_cell_id')
        if event.get('time_axis', 'rows') != 'rows':
            errors.append('按年欄排列表格須有另存紀年對照列')
    elif isinstance(mapping, dict):
        year_table = tables.get(mapping.get('table_id'))
        if not year_table:
            return errors + ['稱號紀年對照表不存在']
        if (event.get('time_axis') != 'columns' or mapping.get('kind') != 'table_year_row'
                or any(mapping.get(k) != year_table['source'].get(v) for k, v in source_fields)):
            errors.append('稱號跨表紀年來源或固定修訂不符')
        regnal_id, digital_id = mapping.get('regnal_year_cell_id'), mapping.get('digital_year_cell_id')
    else:
        return errors + ['稱號紀年對照列格式無效']
    regnal, digital = table_cell(year_table, regnal_id), table_cell(year_table, digital_id)
    if (not regnal or not digital or regnal.get('column') != 1 or digital.get('column') != 0
            or regnal['id'].rpartition('-c')[0] != digital['id'].rpartition('-c')[0]):
        return errors + ['稱號平行紀年須引用同列原年欄及數位對照欄']
    if mapping is None and regnal['id'].rpartition('-c')[0] != cell['id'].rpartition('-c')[0]:
        errors.append('稱號平行紀年須引用事件同列紀年')
    if mapping is not None:
        col = column_for(table, cell)
        anchor = table_cell(year_table, mapping.get('era_anchor_cell_id'))
        year_term = event.get('source_year_term')
        import re
        year_tokens = re.findall(r'(?<![元一二三四五六七八九十百廿卅零〇兩])(?:元|[一二三四五六七八九十百廿卅零〇兩]+)年', cell['text'])
        valid_year = (bool(col) and col.get('kind') == 'source_column'
                      and col.get('id') == event.get('era_column_id')
                      and isinstance(year_term, str) and year_term in year_tokens
                      and isinstance(term, str) and term.startswith(year_term)
                      and bool(anchor) and anchor.get('column') == 1
                      and col['text'] + '元年' in anchor['text'])
        if valid_year:
            label = regnal['text'].rstrip('。')
            valid_year = label == year_term[:-1] or label == col['text'] + year_term
            year_rows = [row for fragment in year_table['fragments'] for row in fragment['rows']]
            ai = next((i for i, row in enumerate(year_rows) if any(c['id'] == anchor['id'] for c in row['cells'])), None)
            yi = next((i for i, row in enumerate(year_rows) if any(c['id'] == regnal['id'] for c in row['cells'])), None)
            valid_year = (valid_year and ai is not None and yi is not None and ai <= yi
                          and not any(c.get('column') == 1 and '元年' in c['text']
                                      for row in year_rows[ai+1:yi+1] for c in row['cells']))
        if not valid_year:
            errors.append('稱號按欄紀年須有相同原年字、事件欄題與對照年號')
        if not any(r.get('url') == source['revision_url']
                   and r.get('table_column_id') == event.get('era_column_id')
                   and col and r.get('quote') == col['text']
                   and r.get('scope') == 'received_regnal_year_attestation'
                   for r in value.get('references', [])):
            errors.append('稱號按欄紀年須引用原年號欄題')
    row = next((row for fragment in year_table['fragments'] for row in fragment['rows']
                if any(c['id'] == digital['id'] for c in row['cells'])), {})
    year = row.get('year') or {}
    latest = value.get('latest', {})
    text = digital['text']
    if (not text.isascii() or not text.isdigit() or year.get('status') != 'digital_editorial_equivalence'
            or year.get('source_cell_id') != digital['id'] or year.get('source_quote') != text
            or year.get('era') not in ('BCE', 'CE') or year.get('value') != int(text)
            or latest.get('era') != year.get('era') or latest.get('era_year') != year.get('value')
            or latest.get('year') != year.get('astronomical_year')):
        errors.append('稱號平行紀年西元對照與範圍端點不符')
    event_url, year_url = source['revision_url'], year_table['source']['revision_url']
    if (parallel.get('reference_url') != event_url
            or parallel.get('reference_year_url', event_url) != year_url
            or parallel.get('reference_event_quote') != cell['text']
            or parallel.get('reference_year_quote') != digital['text']):
        errors.append('稱號平行紀年對讀引句或固定網址不符')
    refs = value.get('references', [])
    for point, url, scope in [(cell, event_url, 'received_parallel_event'),
                              (regnal, year_url, 'received_regnal_year_attestation'),
                              (digital, year_url, 'digital_editorial_regnal_year_equivalence_only')]:
        if not any(ref.get('url') == url and ref.get('table_cell_id') == point['id']
                   and ref.get('quote') == point['text'] and ref.get('scope') == scope for ref in refs):
            errors.append('稱號平行紀年須分列相符表格事件與年欄')
    for ref in refs:
        if ref.get('table_cell_id'):
            ref_table = tables.get(ref.get('table_id', event['table_id']))
            point = table_cell(ref_table, ref['table_cell_id']) if ref_table else None
            if not point or ref.get('url') != ref_table['source']['revision_url'] or ref.get('quote') != point['text']:
                errors.append('稱號平行紀年表格參照不符原格')
        if ref.get('table_column_id'):
            ref_table = tables.get(ref.get('table_id', event['table_id']))
            col = next((col for fragment in ref_table['fragments'] for col in fragment['columns']
                        if col['id'] == ref['table_column_id']), None) if ref_table else None
            if not col or ref.get('url') != ref_table['source']['revision_url'] or ref.get('quote') != col['text']:
                errors.append('稱號紀年原欄題參照不符')
    return errors

def regnal_reign_designation_valid(proof, value, mentions):
    """A source-specific reign designation needs an already resolved person anchor."""
    source = proof.get('source_era_name', proof.get('era_name'))
    table = proof.get('era_name')
    claim = proof.get('reign_designation')
    if not isinstance(source, str) or not source or not isinstance(table, str) or not table:
        return False
    if source == table:
        return claim is None
    contexts = {('漢', '高皇帝'): ('高帝已定天下', '高帝'),
                ('孝文帝', '孝文'): ('及孝文帝元年', '孝文帝')}
    expected = contexts.get((source, table))
    fields = {'kind', 'source_era_name', 'table_era_name', 'person_id',
              'person_mention_id', 'source_context_quote', 'status',
              'rationale', 'human_reviewed'}
    if (expected is None or not isinstance(claim, dict) or set(claim) != fields
            or claim.get('kind') != 'same_reign_source_designations'
            or claim.get('source_era_name') != source or claim.get('table_era_name') != table
            or claim.get('source_context_quote') != expected[0]
            or claim.get('status') != 'editorial_provisional'
            or claim.get('human_reviewed') is not False or not claim.get('rationale')
            or not isinstance(value.get('original_quote'), str)
            or expected[0] not in value['original_quote']):
        return False
    hit = (mentions or {}).get(claim.get('person_mention_id'))
    if (not hit or hit[2].get('kind') != 'person'
            or hit[2].get('person_id') != claim.get('person_id')
            or hit[2].get('surface') != expected[1]):
        return False
    return any(e.get('chapter_id') == hit[0] and e.get('paragraph_id') == hit[1]
               and expected[0] in e.get('quote', '') for e in value.get('evidence', []))


def table_regnal_range_errors(value, expression, tables, mentions=None):
    """Validate a cited year row; it is not a parallel person-event assertion."""
    proof = value.get('regnal_year_table')
    if proof is None:
        return []
    if not isinstance(proof, dict):
        return ['紀年原年列綁定須為物件']
    table = tables.get(proof.get('table_id'))
    if not table:
        return ['紀年原年列所據表格不存在']
    source = table['source']; errors = []
    fields = [('work_id','work_id'),('book_id','book_id'),('chapter_id','chapter_id'),
              ('source_id','id'),('source_revision','revision')]
    if proof.get('kind') != 'table_year_row' or any(proof.get(k) != source.get(v) for k,v in fields):
        errors.append('紀年原年列來源或固定修訂不符')
    regnal = table_cell(table, proof.get('regnal_year_cell_id'))
    digital = table_cell(table, proof.get('digital_year_cell_id'))
    anchor = table_cell(table, proof.get('era_anchor_cell_id'))
    if (not regnal or not digital or not anchor or regnal.get('column') != 1
            or anchor.get('column') != 1 or digital.get('column') != 0
            or regnal['id'].rpartition('-c')[0] != digital['id'].rpartition('-c')[0]):
        return errors + ['紀年原年列須有同列原紀年及數位年格']
    era_name, term = proof.get('era_name'), proof.get('year_source_term')
    source_era_name = proof.get('source_era_name', era_name)
    if not regnal_reign_designation_valid(proof, value, mentions):
        errors.append('紀年帝號異稱須有同篇已辨人物錨點及限定語境，不得任意替換年號')
    label = regnal['text'].rstrip('。'); epoch = anchor['text'].rstrip('。')
    valid = (isinstance(era_name,str) and bool(era_name) and isinstance(term,str)
             and bool(term) and term.endswith('年') and isinstance(source_era_name,str) and expression == source_era_name+term
             and epoch.endswith(era_name+'元年')
             and (label == term[:-1] or label.endswith(era_name+term)))
    rows = [r for f in table['fragments'] for r in f['rows']]
    ai = next((i for i,r in enumerate(rows) if any(c['id']==anchor['id'] for c in r['cells'])),None)
    yi = next((i for i,r in enumerate(rows) if any(c['id']==regnal['id'] for c in r['cells'])),None)
    valid = (valid and ai is not None and yi is not None and ai <= yi
             and not any(c.get('column')==1 and '元年' in c['text']
                         for r in rows[ai+1:yi+1] for c in r['cells']))
    if not valid:
        errors.append('紀年原年字、年號起點或原日期表述不符')
    row = rows[yi] if yi is not None else {}; year = row.get('year') or {}
    text = digital['text']; original_year = year.get('astronomical_year')
    if (not text.isascii() or not text.isdigit() or year.get('status')!='digital_editorial_equivalence'
            or year.get('source_cell_id')!=digital['id'] or year.get('source_quote')!=text
            or year.get('era')!='BCE' or year.get('value')!=int(text)
            or type(original_year) is not int or original_year!=1-int(text)):
        errors.append('紀年數位對照須匹配表內原年列元資料')
    refs = value.get('references',[])
    rule = proof.get('calendar_rule')
    rules = {'han_tenth_month_before_taichu':(-1,0,'建亥'),
             'han_first_month_after_taichu':(0,1,'以正月為歲首')}
    if rule not in rules:
        errors.append('紀年歲首規則未知')
    elif type(original_year) is int:
        a,b,word = rules[rule]
        valid_epoch = (year.get('value',0)>104 if rule=='han_tenth_month_before_taichu'
                       else 0<year.get('value',0)<104)
        if (not valid_epoch or value.get('earliest',{}).get('year')!=original_year+a
                or value.get('latest',{}).get('year')!=original_year+b
                or not any(r.get('scope')=='received_calendar_rule' and word in r.get('quote','')
                           for r in refs)):
            errors.append('紀年範圍須依太初前後實際歲首及其引文換算')
    for point,scope in [(regnal,'received_regnal_year_attestation'),
                        (anchor,'received_regnal_year_attestation'),
                        (digital,'digital_editorial_regnal_year_equivalence_only')]:
        if not any(r.get('table_id')==table['id'] and r.get('table_cell_id')==point['id']
                   and r.get('scope')==scope and r.get('quote')==point['text']
                   and r.get('url')==source['revision_url'] for r in refs):
            errors.append('紀年範圍須分列年號起點、原年字與數位年格')
    return errors
