"""Resolve the unnamed parent in 王釗's own mourning while serving 建安王."""
import hashlib


def valid(assertion, evidence, chapter, root):
    if not chapter or chapter['source'].get('revision_id') != 1478172:
        return False
    source = root / 'sources/calendar-context/songshu042-fixed1478172.wikitext'
    raw = source.read_bytes()
    p = next((p for p in chapter['paragraphs'] if p['id'] == evidence.get('paragraph_id')), None)
    if not p or p['source_position']['first_line'] != 97 or p['source_position']['last_line'] != 97:
        return False
    text=p['text']
    if (hashlib.sha256(raw).hexdigest() != chapter['source']['wikitext_sha256'] or raw.decode().splitlines()[96].strip() != text or evidence['quote'] != text
        or assertion['predicate'] != 'mother' or assertion['qualifiers']['source_term'] != '居母憂' or '練子釗，' not in text or '隨司徒建安王休仁出赭圻，時居母憂，加冠軍將軍。' not in text):
        return False
    person=next((m for m in p['mentions'] if m['id']==evidence.get('subject_person_mention_id')),None)
    mother=next((m for m in chapter['annotation']['person_reference_occurrences'] if m['id']==evidence.get('object_person_reference_id')),None)
    return (person is not None and mother is not None and person['surface']=='釗' and person['start']==text.index('練子釗')+2 and person['person_id']==assertion['subject_person_id']
        and mother['surface']=='母' and mother['start']==text.index('時居母憂')+2 and mother['end']==mother['start']+1 and mother['paragraph_id']==p['id'] and mother['person_id']==assertion['object_person_id'] and assertion['subject_person_id']!=assertion['object_person_id'])
