"""Read derived person JSON in its expanded, source-rich form for assertions."""
from functools import lru_cache
import json
from pathlib import Path
from scripts.passage_refs import PassageCatalog
from scripts.profile_passages import ReaderPassages

@lru_cache(maxsize=1)
def bundle_catalog(root):
    return PassageCatalog(root)

@lru_cache(maxsize=1)
def profile_catalog(root):
    return ReaderPassages(root)

def read_document(path):
    path = Path(path)
    doc = json.loads(path.read_bytes())
    if path.name == 'index.json':
        return doc
    if path.parts[-3:-1] == ('exports','persons'):
        return bundle_catalog(path.parents[2]).expand(doc)
    if path.parts[-4:-1] == ('data','corpus','profiles'):
        return profile_catalog(path.parents[3]).convert(doc, expand=True)
    return doc
