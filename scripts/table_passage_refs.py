"""Resolve a native table cell by its table and cell IDs in this revision."""
try:
    from .table_evidence import load_tables
except ImportError:
    from table_evidence import load_tables


class TablePassages:
    def __init__(self, root):
        self.cells = {}
        self.sources = {}
        for tid, table in load_tables(root).items():
            self.sources[tid] = table['source']
            for fragment in table['fragments']:
                for row in fragment['rows']:
                    for cell in row['cells']:
                        key = tid, cell['id']
                        if key in self.cells:
                            raise ValueError(f'Duplicate table cell {key}')
                        self.cells[key] = cell

    def occurrences(self, items, expand):
        result = []
        for item in items:
            row = dict(item)
            key = row['table_id'], row.get('table_cell_id', row.get('cell_id'))
            if expand and row.pop('quote_ref', None) == 'cell':
                if 'quote' in row:
                    raise ValueError(f'Mixed cell quotation {key}')
                row['quote'] = self.cells[key]['text']
            elif not expand and 'quote' in row:
                if self.cells[key]['text'] != row.pop('quote'):
                    raise ValueError(f'Divergent table cell {key}')
                row['quote_ref'] = 'cell'
            result.append(row)
        return result
