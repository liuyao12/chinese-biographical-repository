"""Resolve person-export passage IDs against the same revision of the marked corpus."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
try:
    from .table_passage_refs import TablePassages
    from .quotation_refs import Quotations
except ImportError:
    from table_passage_refs import TablePassages
    from quotation_refs import Quotations


class PassageCatalog:
    def __init__(self, root):
        self.root = Path(root)
        self.chapters = {}
        self.paragraphs = {}
        self.sources = {}
        snapshot_path = self.root / 'exports/passage-annotations.json'
        self.annotations = json.loads(snapshot_path.read_bytes())['records'] if snapshot_path.exists() else {}
        self.tables = TablePassages(self.root)
        self.table_chapters = {s['chapter_id']: tid for tid, s in self.tables.sources.items()}
        public = []
        for path in sorted((self.root / 'corpus').glob('*/*.json')):
            chapter = json.loads(path.read_bytes())
            if chapter.get('record_type') != 'marked_chapter':
                continue
            cid = chapter['id']
            if cid in self.chapters:
                raise ValueError(f'Duplicate chapter {cid}')
            relative = path.relative_to(self.root).as_posix()
            self.chapters[cid] = relative
            self.sources[relative] = chapter['source']
            public.append((f'data/corpus/{chapter["work_id"].removeprefix("w-")}/{path.name}', chapter))
            location = {key: chapter[key] for key in ('work_id', 'book_id', 'source_id')}
            for paragraph in chapter['paragraphs']:
                key = relative, paragraph['id']
                if key in self.paragraphs:
                    raise ValueError(f'Duplicate passage {key}')
                self.paragraphs[key] = dict(paragraph, chapter_id=cid, **location)
        self.quotations = Quotations(public, self.tables)

    @staticmethod
    def fingerprint(paragraph):
        payload = json.dumps(paragraph, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(payload.encode()).hexdigest()

    def paragraph(self, ref):
        native = self.paragraphs[ref['chapter'], ref['id']]
        if 'annotation_ref' not in ref:
            return native
        key = ref['annotation_ref']
        record = self.annotations[key]
        if (record['chapter'], record['id']) != (ref['chapter'], ref['id']) or not record['fields'].keys() <= {'mentions','annotation_status'}:
            raise ValueError(f'Invalid archived annotation {key}')
        result = dict(native, **record['fields'])
        if self.fingerprint(result) != key:
            raise ValueError(f'Archived annotation digest mismatch {key}')
        return result

    def compact(self, bundle):
        if 'passage_refs' in bundle:
            bundle = self.expand(bundle)
        output = dict(bundle)
        refs = []
        for paragraph in output.pop('passages'):
            path = self.chapters[paragraph['chapter_id']]
            pid = paragraph['id']
            ref = {'chapter': path, 'id': pid}
            if self.paragraph(ref) != paragraph:
                key = self.fingerprint(paragraph)
                if key not in self.annotations:
                    raise ValueError(f'Divergent passage {path} {pid}')
                ref['annotation_ref'] = key
                if self.paragraph(ref) != paragraph:
                    raise ValueError(f'Unresolved historical annotation {key}')
            refs.append(ref)
        output['passage_refs'] = refs
        if 'table_passages' in output:
            output['table_passage_refs'] = []
            for passage in output.pop('table_passages'):
                key = passage['table_id'], passage['id']
                cell = self.tables.cells[key]
                if any(k not in passage or passage[k] != v for k,v in cell.items()):
                    raise ValueError(f'Divergent table passage {key}')
                detail = {k:v for k,v in passage.items() if k not in cell}
                output['table_passage_refs'].append(dict(detail, id=key[1]))
        if 'table_occurrences' in output:
            output['table_occurrences'] = self.tables.occurrences(output['table_occurrences'], False)
        output['sources'] = []
        for item in bundle['sources']:
            path = self.chapters.get(item['chapter_id'])
            if path is None:
                tid = self.table_chapters[item['chapter_id']]
                if self.tables.sources[tid] != item['source']:
                    raise ValueError(f'Divergent table source {tid}')
                output['sources'].append({**{k:v for k,v in item.items() if k != 'source'}, 'table_source_ref': tid})
                continue
            if self.sources[path] != item['source']:
                raise ValueError(f'Divergent source {path}')
            output['sources'].append({**{k:v for k,v in item.items() if k != 'source'}, 'source_ref': path})
        return self.quotations.convert(output, expand=False)

    def expand(self, bundle):
        if 'passage_refs' not in bundle:
            return bundle
        if 'passages' in bundle:
            raise ValueError('Mixed passage representations')
        output = self.quotations.convert(bundle, expand=True)
        output['passages'] = [self.paragraph(r) for r in output.pop('passage_refs')]
        if 'table_passage_refs' in output:
            if 'table_passages' in output:
                raise ValueError('Mixed table passage representations')
            output['table_passages'] = []
            for ref in output.pop('table_passage_refs'):
                cell = self.tables.cells[ref['table_id'], ref['id']]
                if (cell.keys() & ref.keys()) - {'id'}:
                    raise ValueError('Table reference overrides native cell fields')
                output['table_passages'].append({**cell, **ref})
        if 'table_occurrences' in output:
            output['table_occurrences'] = self.tables.occurrences(output['table_occurrences'], True)
        output['sources'] = []
        for item in bundle['sources']:
            row = dict(item)
            if 'table_source_ref' in row:
                tid = row.pop('table_source_ref')
                if self.table_chapters[row['chapter_id']] != tid or 'source' in row:
                    raise ValueError(f'Invalid table source {tid}')
                row['source'] = self.tables.sources[tid]
            if 'source_ref' in row:
                path = row.pop('source_ref')
                if path != self.chapters[row['chapter_id']] or 'source' in row:
                    raise ValueError(f'Invalid source reference {path}')
                row['source'] = self.sources[path]
            output['sources'].append(row)
        return output


def write_json(path, data, *, indent=None):
    options = {'indent': indent} if indent else {'separators': (',', ':')}
    encoded = (json.dumps(data, ensure_ascii=False, **options) + '\n').encode()
    if path.is_file() and path.read_bytes() == encoded:
        return
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    with NamedTemporaryFile(dir=path.parent, delete=False) as f:
        temp = Path(f.name)
        try:
            f.write(encoded)
            f.flush()
            os.fchmod(f.fileno(), mode)
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['migrate', 'check', 'expand'])
    parser.add_argument('file', type=Path, nargs='?')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    catalog = PassageCatalog(args.root)
    if args.action == 'expand':
        if args.file is None:
            parser.error('expand requires a person JSON file')
        print(json.dumps(catalog.expand(json.loads(args.file.read_bytes())), ensure_ascii=False))
        return
    count = 0
    for path in sorted((args.root / 'exports/persons').glob('*.json')):
        if path.name == 'index.json':
            continue
        original = json.loads(path.read_bytes())
        compact = catalog.compact(original)
        if args.action == 'check' and compact != original:
            raise ValueError(f'Inline passage export {path}')
        if catalog.expand(compact) != catalog.expand(original):
            raise ValueError(f'Round-trip mismatch {path}')
        if args.action == 'migrate':
            write_json(path, compact)
        count += 1
    print(f'Verified {count} person exports')


if __name__ == '__main__':
    main()
