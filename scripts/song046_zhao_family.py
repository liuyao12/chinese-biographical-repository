"""Read both people and the relationship from the fixed Song 46, Song 48 and Nan 57 statements."""
from pathlib import Path
import hashlib
import json


def valid(assertion, evidence, chapter, root):
    try:
        raw = (Path(root) / RULES).read_bytes()
        if hashlib.sha256(raw).hexdigest() != DIGEST:
            return False
        rule = json.loads(raw)[assertion['id']]
        paragraph, = [p for p in chapter['paragraphs'] if p['id'] == rule['paragraph'] == evidence['paragraph_id']]
        source = chapter['source']
        text = paragraph['text']
        if (chapter['id'], source['revision_id'], source['raw_file_sha256']) != (rule['chapter'], rule['rev'], rule['raw_sha256']):
            return False
        if assertion['predicate'] != rule['predicate'] or assertion['qualifiers']['source_term'] != rule['term'] or text.count(rule['term']) != 1:
            return False
        if text != evidence['quote'] or hashlib.sha256(text.encode()).hexdigest() != rule['text_sha256']:
            return False
        refs = [r for r in chapter['annotation'].get('person_reference_occurrences', []) if r['paragraph_id'] == paragraph['id']]
        for endpoint in rule['anchors']:
            anchor, = [m for m in [*paragraph['mentions'], *refs] if m['id'] == evidence[endpoint['field']] == endpoint['id']]
            if assertion[endpoint['role'] + '_person_id'] != anchor['person_id'] or anchor['person_id'] != endpoint['person_id']:
                return False
            if (anchor['start'], anchor['end'], anchor['surface']) != (endpoint['start'], endpoint['end'], endpoint['word']):
                return False
            if text[anchor['start']:anchor['end']] != endpoint['word']:
                return False
        return True
    except (KeyError, OSError, TypeError, ValueError):
        return False

RULES = 'source-evidence/song046-zhang-complete/zhao-kin-rules.json'
DIGEST = 'eaceb5be1a31fa6d61d7a2aa61e613aa287fe3b91c26d5d80f42518f12dba098'
