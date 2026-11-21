"""核對王華與孔甯子傳敘的兩種見證及既發稱謂編號。"""
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


DIGITAL = 'c-songshu-063-wanghua-tanshou'
PRINT = 'c-songshu-063-wanghua-wyd'
EVIDENCE = Path('source-evidence/song063-wanghua')
HUA = '7r6_k52_qji_ABAAFAB'
ISSUED_REFERENCES = {
    (10, 224): ('奴子', HUA, 'addressee', '奴子怠懈，行不及我'),
    (10, 232): ('我', '58f_d92_1b5', 'speaker_self', '奴子怠懈，行不及我'),
    (14, 166): ('殿下', '3bh_k4m_fg4', 'third_person', '必是殿下出行'),
    (16, 39): ('廢主', '0ab_f5d_337', 'third_person', '廢主若存'),
    (16, 92): ('少主', '3bh_k4m_fg4', 'third_person', '以少主仰待耳'),
    (16, 120): ('上', '3bh_k4m_fg4', 'third_person', '上即位'),
    (22, 144): ('上', '3bh_k4m_fg4', 'third_person', '上思誅羨之之功'),
}


def issued_references(chapter, paragraph):
    if chapter['id'] != DIGITAL or chapter['source']['revision_id'] != 2118589:
        return []
    refs = chapter['annotation']['person_reference_occurrences']
    found = []
    for (line, start), (word, who, role, clause) in ISSUED_REFERENCES.items():
        pid = DIGITAL + f':line{line:03}'
        if paragraph['id'] != pid or paragraph['text'].count(clause) != 1:
            continue
        if paragraph['text'].index(clause) + clause.index(word) != start:
            continue
        for ref in refs:
            if (ref['id'] == pid + f':m{start:04}' and ref['paragraph_id'] == pid
                    and (ref['start'], ref['end']) == (start, start + len(word))
                    and (ref['surface'], ref['person_id'], ref['referent_role'], ref['quote']) == (word, who, role, clause)):
                found.append(dict(ref, kind='person', original_layer='person_reference'))
    return found


def print_gift_valid(holding, paragraphs, mentions, deaths):
    pid = PRINT + ':p007'
    hit = paragraphs.get(pid)
    basis = holding.get('posthumous_basis', {})
    ev = holding.get('evidence', [])
    if (not hit or hit[0] != PRINT or holding.get('person_id') != HUA
            or holding.get('title') != '衞將軍' or holding.get('mode') != 'posthumous_grant'
            or basis.get('kind') != 'song063_print_coordinated_gift' or len(ev) != 1):
        return False
    paragraph = hit[1]
    term = '四年卒時年四十三追贈散騎常侍衞將軍'
    text = paragraph['text']
    if text.count(term) != 1 or basis.get('source_term') != term:
        return False
    start = text.index(term)
    mid = ev[0].get('person_mention_id')
    holder = mentions.get(mid)
    death = deaths.get(basis.get('death_event_id'), {})
    att = holding['attestations']
    return (holder and holder[1] == pid and holder[2]['person_id'] == HUA
            and ev[0]['paragraph_id'] == pid and ev[0]['quote'] == text
            and ev == basis['evidence'] == holding['effective_period']['start']['evidence']
            and death.get('person_id') == HUA and death.get('event_type') == 'death'
            and death.get('source_anchor') == dict(paragraph_id=pid, start=start + 2, end=start + 3, surface='卒')
            and len(att) == 1 and att[0]['paragraph_id'] == pid and att[0]['person_mention_id'] == mid
            and att[0]['start'] == start + term.index('衞將軍') and att[0]['end'] == start + len(term))


def errors(chapter, root):
    if chapter['id'] not in (DIGITAL, PRINT):
        return []
    def read(path):
        return json.loads((root / path).read_text())
    try:
        if chapter['id'] == PRINT:
            proof = read(EVIDENCE / 'wuying-reading.json')
            if [r['pdf_page'] for r in proof['images']] != [15, 16, 17, 18]:
                return ['王華書影缺頁或倒序']
            download = urlsplit(proof['pdf_download_url'])
            catalog = chapter['source']['permalink']
            if (proof['pdf_url'] != catalog or proof['catalog_permalink'] != catalog
                    or download.scheme != 'https' or download.netloc != 'upload.wikimedia.org'
                    or download.query or download.fragment
                    or unquote(download.path.rsplit('/', 1)[-1]) != catalog.rsplit('File:', 1)[-1]):
                return ['王華書影須連到所核館藏冊及其目錄']
            for row in proof['images']:
                page_url = f"{proof['pdf_download_url']}#page={row['pdf_page']}"
                if (row['source_url'] != page_url
                        or not re.fullmatch('[0-9a-f]{64}', row['capture_sha256'])):
                    return ['王華書影逐頁連結或擷取指紋不合']
            if len(proof['columns']) != 63 or sum(len(c['reading']) for c in proof['columns']) != 1313:
                return ['王華印本全文須覆蓋連續六十三欄']
        else:
            review = read(EVIDENCE / 'reading.json')
            paragraphs = {p['id']: p for p in chapter['paragraphs'][:9]}
            if sum(len(issued_references(chapter, p)) for p in paragraphs.values()) != 7:
                return ['王華傳已發的稱謂須各自保留原人物原字位']
            for row in review['paragraphs']:
                p = paragraphs[row['paragraph_id']]
                if (sha256(p['text'].encode()).hexdigest() != row['text_sha256']
                        or [m['id'] for m in p['mentions']] != row['named_or_unresolved']):
                    return ['王華傳逐段存證與本文不合']
            for row in review['parallel_readings']:
                p = paragraphs[row['paragraph_id']]
                other = row['parallel']
                raw = (root / other['path']).read_bytes()
                line = raw.decode().splitlines()[other['line'] - 1]
                if (p['text'][row['start']:row['end']] != row['surface']
                        or sha256(raw).hexdigest() != other['sha256']
                        or line[other['start']:other['end']] != other['quote']):
                    return ['王華或孔甯子引古未與固定本文及平行來源字位相合']
        ages = {a['source_term']: a for a in chapter['annotation']['age_assertions']}
        juvenile = '年十二' if chapter['id'] == PRINT else '年十三'
        if (set(ages) != {juvenile, '年四十三'} or ages[juvenile]['value'] != (12 if chapter['id'] == PRINT else 13)
                or ages['年四十三']['value'] != 43 or any(a['birth_year'] is not None for a in ages.values())):
            return ['王華兩本軍中報齡各繫原數，生年未載']
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return ['王華傳來源或逐項存證缺失']
    return []
