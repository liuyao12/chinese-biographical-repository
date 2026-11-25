"""Store public profile quotations as Unicode code-point ranges in published chapters."""
import argparse
import json
from pathlib import Path
try:
    from .table_passage_refs import TablePassages
    from .quotation_refs import Quotations
except ImportError:
    from table_passage_refs import TablePassages
    from quotation_refs import Quotations


class ReaderPassages:
    def __init__(self, root):
        self.chapters = {}
        self.tables = TablePassages(root)
        self.table_chapters = {s['chapter_id']: tid for tid, s in self.tables.sources.items()}
        for directory in (root / 'data/corpus').iterdir():
            if not directory.is_dir() or directory.name in {'profiles', 'summaries'}:
                continue
            for path in directory.glob('*.json'):
                if path.name == 'index.json':
                    continue
                chapter = json.loads(path.read_bytes())
                if not isinstance(chapter, dict) or chapter.get('record_type') != 'marked_chapter':
                    continue
                cid = chapter['id']
                if cid in self.chapters:
                    raise ValueError(f'Duplicate published chapter {cid}')
                self.chapters[cid] = (path.relative_to(root).as_posix(), chapter,
                                      {p['id']: p for p in chapter['paragraphs']})
        self.quotations = Quotations(((p,c) for p,c,_ in self.chapters.values()), self.tables)

    def convert(self, profile, *, expand=False):
        profile = self.quotations.convert(profile, expand=True) if expand else profile
        out = dict(profile)
        if 'table_occurrences' in out:
            out['table_occurrences'] = self.tables.occurrences(out['table_occurrences'], expand)
        for field in ('sources', 'occurrences'):
            if field not in profile:
                continue
            out[field] = []
            for item in profile[field]:
                row = dict(item)
                chapter = self.chapters.get(row.get('chapter_id'))
                if chapter:
                    path, doc, paragraphs = chapter
                    if row.get('source_id') != doc['source_id'] or row.get('book_id') != doc['book_id'] or row.get('work_id') != doc['work_id']:
                        raise ValueError(f'Wrong witness for {row.get("chapter_id")}')
                    if expand and 'chapter_ref' in row:
                        if row.pop('chapter_ref') != path:
                            raise ValueError('Wrong published chapter path')
                        if field == 'sources':
                            row['source'] = doc['source']
                        else:
                            text = paragraphs[row['paragraph_id']]['text']
                            start, stop = row.pop('quote_span')
                            if not 0 <= start <= stop <= len(text):
                                raise ValueError('Invalid passage offsets')
                            row['quote'] = text[start:stop]
                    elif not expand and field == 'sources' and row.get('source') == doc['source']:
                        del row['source']
                        row['chapter_ref'] = path
                    elif not expand and field == 'occurrences' and 'quote' in row:
                        paragraph = paragraphs[row['paragraph_id']]
                        quote = row.pop('quote')
                        text = paragraph['text']
                        mention = next((m for m in paragraph['mentions'] if m['id'] == row.get('mention_id')), None)
                        start = max(0, mention['start'] - 35) if mention else 0
                        if not text.startswith(quote, start):
                            start = text.find(quote)
                            if start < 0 or text.find(quote, start + 1) >= 0:
                                raise ValueError(f'Unresolved quote in {row["paragraph_id"]}')
                        row.update(chapter_ref=path, quote_span=[start, start + len(quote)])
                elif 'chapter_ref' in row:
                    raise ValueError(f'Unresolved chapter {row.get("chapter_id")}')
                elif field == 'sources' and row.get('chapter_id') in self.table_chapters:
                    tid = self.table_chapters[row['chapter_id']]
                    if expand and 'table_source_ref' in row:
                        if tid != row.pop('table_source_ref') or 'source' in row:
                            raise ValueError(f'Invalid table source {tid}')
                        row['source'] = self.tables.sources[tid]
                    elif not expand and 'source' in row:
                        if row.pop('source') != self.tables.sources[tid]:
                            raise ValueError(f'Divergent table source {tid}')
                        row['table_source_ref'] = tid
                out[field].append(row)
        return out if expand else self.quotations.convert(out, expand=False)


def migrate(root, check=False):
    catalog = ReaderPassages(root)
    changed = 0
    for path in (root / 'data/corpus/profiles').glob('*.json'):
        if path.name == 'index.json':
            continue
        original = json.loads(path.read_bytes())
        compact = catalog.convert(original)
        if catalog.convert(compact, expand=True) != catalog.convert(original, expand=True):
            raise ValueError(f'Profile round-trip mismatch {path}')
        if compact != original:
            if check:
                raise ValueError(f'Inline profile {path}')
            from tempfile import NamedTemporaryFile
            import os
            with NamedTemporaryFile(dir=path.parent, delete=False) as out:
                temp = Path(out.name)
                try:
                    out.write((json.dumps(compact, ensure_ascii=False, indent=2)+'\n').encode())
                    out.flush()
                    os.fchmod(out.fileno(), path.stat().st_mode & 0o777)
                    os.replace(temp, path)
                finally:
                    temp.unlink(missing_ok=True)
            changed += 1
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print('Updated profiles', migrate(args.root, args.check))
