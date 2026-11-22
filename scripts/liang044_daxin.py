"""Validate Gaozu's grandson Daxin in the separate Taizong princes and mothers list."""
from pathlib import Path
from hashlib import sha256


def second_mother_group_valid(assertion, evidence, chapter, root):
    try:
        source = chapter['source']
        raw = (Path(root) / source['raw_path']).read_bytes()
        lines = raw.decode().splitlines()
        p, = chapter['paragraphs']
        text = p['text']
        father, = [ref for ref in chapter['annotation']['person_reference_occurrences']
                   if ref['id'] == evidence['object_reference_id']]
        son, = [m for m in p['mentions'] if m['id'] == evidence['subject_person_mention_id']]
        clause = '太宗王皇后生哀太子大器、南郡王大連，陳淑容生尋陽王大心'
        return (chapter['id'] == 'c-liangshu-044-xiaodaxin-parents'
                and source['revision_id'] == 2376749
                and sha256(raw).hexdigest() == source['raw_file_sha256'] == DIGEST
                and lines[9] == '==太宗十一王==' and '陳淑容生尋陽王大心，' in lines[10]
                and lines[11] == '===尋陽王大心===' and lines[12].lstrip().startswith('尋陽王大心字仁恕')
                and p['source_position']['first_line'] == p['source_position']['last_line'] == 11
                and p['id'] == evidence['paragraph_id'] == father['paragraph_id']
                and evidence['quote'] == text == clause + '，'
                and assertion['qualifiers']['source_term'] == clause and assertion['predicate'] == 'father'
                and assertion['object_person_id'] == father['person_id'] == 'rtd_v0b_nyn'
                and assertion['subject_person_id'] == son['person_id'] == 'rtd_v0b_nyn_E'
                and father['start'] == 0 and text[father['start']:father['end']] == father['surface'] == '太宗'
                and son['start'] == text.index('大心') and text[son['start']:son['end']] == son['surface'] == '大心')
    except (KeyError, OSError, UnicodeError, TypeError, ValueError, IndexError):
        return False


DIGEST = '297f209a385e25e5127b86b5529cee3cb92e603135eee46656ac12d53c801401'
