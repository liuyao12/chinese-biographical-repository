"""Share whole-passage quotations in nested, derived evidence records."""
class Quotations:
    def __init__(self, chapters, tables):
        self.loci = {}
        for path, chapter in chapters:
            witness = {key: chapter[key] for key in ('work_id','book_id','source_id')}
            witness['chapter_id'] = chapter['id']
            for paragraph in chapter['paragraphs']:
                key = paragraph['id']
                if key in self.loci:
                    raise ValueError(f'Ambiguous paragraph ID {key}')
                self.loci[key] = (path, witness, paragraph['text'])
        self.tables = tables

    def locus(self, row):
        if row.get('paragraph_id'):
            return self.loci.get(row['paragraph_id'])
        tid = row.get('table_id')
        cid = row.get('table_cell_id') or row.get('cell_id')
        if tid and cid:
            cell = self.tables.cells.get((tid,cid))
            if cell is not None:
                source = self.tables.sources[tid]
                witness = {k:source[k] for k in ('chapter_id','work_id','book_id')}
                witness.update(source_id=source['id'], source_revision=source['revision'])
                return f'data/historical-tables/{tid}.json', witness, cell['text']

    def convert(self, value, *, expand):
        if isinstance(value, list):
            return [self.convert(x, expand=expand) for x in value]
        if not isinstance(value, dict):
            return value
        row = {k:self.convert(v, expand=expand) for k,v in value.items()}
        if 'quote_passage_ref' not in row and (expand or not isinstance(row.get('quote'), str)):
            return row
        locus = self.locus(row)
        matching = locus and all(row.get(k,v)==v for k,v in locus[1].items())
        if 'quote_passage_ref' in row:
            if not matching or row['quote_passage_ref'] != locus[0] or 'quote' in row:
                raise ValueError('Dangling or mixed quotation reference')
            if expand:
                del row['quote_passage_ref']
                row['quote'] = locus[2]
        elif matching and row['quote'] == locus[2]:
            del row['quote']
            row['quote_passage_ref'] = locus[0]
        return row
