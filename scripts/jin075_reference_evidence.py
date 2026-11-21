"""核對固定卷七十五傳首所載的婚姻與匿名母親。"""
from hashlib import sha256

FILE = 'source-evidence/jin079-xieyan-xiehun/witnesses/jin075-ws2645530.wikitext'
SHA = '11d2db1eed03a9a461ce48abad661b90ba39911b13da75b3fe593dac197bc957'
P = 'c-jinshu-075-xunsong-families:xunxian-intro:p001'


def reference_evidence_valid(evidence, chapter, person):
    if not chapter or evidence.get('source_id') != chapter['source_id'] or evidence.get('book_id') != chapter['book_id'] or evidence.get('work_id') != chapter['work_id']:
        return False
    refs = chapter.get('annotation', {}).get('person_reference_occurrences', [])
    rows = [r for r in refs if r['id'] == evidence.get('mention_id')]
    return len(rows) == 1 and (rows[0]['person_id'], rows[0]['paragraph_id'], rows[0]['surface']) == (person, evidence.get('paragraph_id'), evidence.get('quote'))


def kin_valid(assertion, evidence, ch, root):
    q = assertion['qualifiers']
    obj = {
        'mother': ('pfb_4h4_0dm', 'm0040', '母', '羨陰白其母', '羨陰白其母'),
        'spouse': ('dkn_ge4_286_AAAAAAAG', 'm0076', '尋陽公主', '乃出尚公主', '年十五，將尚尋陽公主'),
    }.get(assertion['predicate'])
    if not ch or not obj or assertion['subject_person_id'] != 'yoo_ox0_545_BABAAAB' or assertion['object_person_id'] != obj[0] or evidence.get('paragraph_id') != P:
        return False
    raw = (root / FILE).read_bytes()
    if sha256(raw).hexdigest() != SHA or ch['source']['revision_id'] != 2645530:
        return False
    p = next(p for p in ch['paragraphs'] if p['id'] == P)
    refs = ch['annotation']['person_reference_occurrences']
    quote = p['text']
    if raw.decode().splitlines()[153].strip() != quote or evidence['quote'] != quote:
        return False
    return (q['source_term'] in quote and q['source_term'] == obj[3]
            and obj[4] in quote and any(m['id'] == evidence.get('subject_person_mention_id') == P + ':m0000' and m['person_id'] == assertion['subject_person_id'] for m in p['mentions'])
            and any(r['id'] == evidence.get('object_person_reference_id') == P + ':' + obj[1]
                    and r['person_id'] == obj[0] and r['surface'] == obj[2]
                    and quote[r['start']:r['end']] == obj[2] for r in refs))
