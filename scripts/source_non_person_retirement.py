"""Finite source-bound non-person reading and negative ID reservation.

This module does not resolve a person or infer a reading from free text.
"""
import json
import hashlib
from pathlib import Path
try:
    from .person_ids import valid_person_id
except ImportError:
    from person_ids import valid_person_id

REVIEW_PATH = 'source-evidence/shiji130-weiqing-nonperson/review.json'
RECEIPT_PATH = 'source-evidence/shiji130-weiqing-nonperson/annotation-chain.json'
REVIEW_ID = 'nr-shiji130-weiqing-polity-predicate'
REVIEW_FIXED = {'record_type': 'source_non_person_interpretation_review', 'id': 'nr-shiji130-weiqing-polity-predicate', 'status': 'contextual_provisional', 'human_reviewed': False, 'image_verified': False, 'model': None, 'source_mention_id': 'c-shiji-130-taishigong:m049-0025', 'source_scope': '固定130p049同一MID/原span，非所有衛頃文字的全域規則', 'interpretation': 'polity_predicate', 'source_contexts': [{'path': 'corpus/shiji/130.json', 'chapter_id': 'c-shiji-130-taishigong', 'work_id': 'w-shiji', 'book_id': 'b-shiji-130', 'source_id': 's-shiji130-taishigong', 'source': {'title': '史記／卷130', 'provider': '維基文庫', 'url': 'https://zh.wikisource.org/wiki/史記/卷130', 'permalink': 'https://zh.wikisource.org/w/index.php?title=史記/卷130&oldid=2609362', 'revision_id': 2609362, 'accessed_on': '2026-10-11', 'extent': '固定修訂全文143段，全部篇文。', 'image_verified': False, 'rights': '古代原文；數位轉錄依維基文庫CC BY-SA 4.0，保留署名及固定版本。', 'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/', 'normalization': {'character_conversion': {}, 'editorial_readings': [], 'extraction_note': '去header2及現代節標，移除維基引文縮排冒號，保留原字，未核影像。', 'note': '全文入庫不等於全部提及已標註；目錄段落仍待逐段處理。'}}, 'paragraph_id': 'c-shiji-130-taishigong:p049', 'quote': '收殷餘民，叔封始邑，申以商亂，酒材是告，及朔之生，衛頃不寧；南子惡蒯聵，子父易名。周德卑微，戰國既彊，衛以小弱，角獨後亡。喜彼康誥，作衛世家第七。', 'text_layer': 'received_chapter'}, {'path': 'corpus/shiji/037.json', 'chapter_id': 'c-shiji-037-wei', 'work_id': 'w-shiji', 'book_id': 'b-shiji-037', 'source_id': 's-shiji-037-wei', 'source': {'title': '史記／卷037', 'provider': '維基文庫', 'url': 'https://zh.wikisource.org/wiki/史記/卷037', 'permalink': 'https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124', 'revision_id': 5977124, 'accessed_on': '2026-10-09', 'extent': '53段傳世正文，自衞康叔名封至太史公論贊，另保留1段數位見證附載索隱述贊並分層；排除2個dd導覽。', 'image_verified': False, 'rights': '古代原文；數位轉錄依維基文庫CC BY-SA 4.0，保留署名及固定版本。', 'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/', 'normalization': {'character_conversion': {'绖': '絰'}, 'editorial_readings': [{'paragraph_id': 'c-shiji-037-wei:p027', 'rendered': '史Template:按', 'wikitext': '史{{按|魚}}', 'transcribed': '史魚', 'reason': '同一固定版本的按模板失效；取原始標記明示的魚字恢復轉錄，不是依模型補名或底本校勘。'}], 'extraction_note': '固定版本與實讀HTML一致。第31段绖轉絰；第27段失效模板按同版原始標記修復。衞、偼、呉、徴、盂黶等其餘原字不默改。末段標題在h2索隱述贊，另層保留，不把標題添加到原段。', 'note': '未核可靠古籍底本及影像，原紀年、世系及異體保留。未以後世研究摘要直接修改親屬或身份。'}}, 'paragraph_id': 'c-shiji-037-wei:p005', 'quote': '康叔卒，子康伯代立。康伯卒，子考伯立。考伯卒，子嗣伯立。嗣伯卒，子偼伯立。偼伯卒，子靖伯立。靖伯卒，子貞伯立。貞伯卒，子頃侯立。', 'text_layer': 'received_chapter'}, {'path': 'corpus/shiji/037.json', 'chapter_id': 'c-shiji-037-wei', 'work_id': 'w-shiji', 'book_id': 'b-shiji-037', 'source_id': 's-shiji-037-wei', 'source': {'title': '史記／卷037', 'provider': '維基文庫', 'url': 'https://zh.wikisource.org/wiki/史記/卷037', 'permalink': 'https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124', 'revision_id': 5977124, 'accessed_on': '2026-10-09', 'extent': '53段傳世正文，自衞康叔名封至太史公論贊，另保留1段數位見證附載索隱述贊並分層；排除2個dd導覽。', 'image_verified': False, 'rights': '古代原文；數位轉錄依維基文庫CC BY-SA 4.0，保留署名及固定版本。', 'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/', 'normalization': {'character_conversion': {'绖': '絰'}, 'editorial_readings': [{'paragraph_id': 'c-shiji-037-wei:p027', 'rendered': '史Template:按', 'wikitext': '史{{按|魚}}', 'transcribed': '史魚', 'reason': '同一固定版本的按模板失效；取原始標記明示的魚字恢復轉錄，不是依模型補名或底本校勘。'}], 'extraction_note': '固定版本與實讀HTML一致。第31段绖轉絰；第27段失效模板按同版原始標記修復。衞、偼、呉、徴、盂黶等其餘原字不默改。末段標題在h2索隱述贊，另層保留，不把標題添加到原段。', 'note': '未核可靠古籍底本及影像，原紀年、世系及異體保留。未以後世研究摘要直接修改親屬或身份。'}}, 'paragraph_id': 'c-shiji-037-wei:p006', 'quote': '頃侯厚賂周夷王，夷王命衞爲侯。頃侯立十二年卒，子釐侯立。', 'text_layer': 'received_chapter'}, {'path': 'corpus/shiji/037.json', 'chapter_id': 'c-shiji-037-wei', 'work_id': 'w-shiji', 'book_id': 'b-shiji-037', 'source_id': 's-shiji-037-wei', 'source': {'title': '史記／卷037', 'provider': '維基文庫', 'url': 'https://zh.wikisource.org/wiki/史記/卷037', 'permalink': 'https://zh.wikisource.org/w/index.php?title=史記/卷037&oldid=5977124', 'revision_id': 5977124, 'accessed_on': '2026-10-09', 'extent': '53段傳世正文，自衞康叔名封至太史公論贊，另保留1段數位見證附載索隱述贊並分層；排除2個dd導覽。', 'image_verified': False, 'rights': '古代原文；數位轉錄依維基文庫CC BY-SA 4.0，保留署名及固定版本。', 'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/', 'normalization': {'character_conversion': {'绖': '絰'}, 'editorial_readings': [{'paragraph_id': 'c-shiji-037-wei:p027', 'rendered': '史Template:按', 'wikitext': '史{{按|魚}}', 'transcribed': '史魚', 'reason': '同一固定版本的按模板失效；取原始標記明示的魚字恢復轉錄，不是依模型補名或底本校勘。'}], 'extraction_note': '固定版本與實讀HTML一致。第31段绖轉絰；第27段失效模板按同版原始標記修復。衞、偼、呉、徴、盂黶等其餘原字不默改。末段標題在h2索隱述贊，另層保留，不把標題添加到原段。', 'note': '未核可靠古籍底本及影像，原紀年、世系及異體保留。未以後世研究摘要直接修改親屬或身份。'}}, 'paragraph_id': 'c-shiji-037-wei:p013', 'quote': '十八年，初，宣公愛夫人夷姜，夷姜生子伋，以爲太子，而令右公子傅之。右公子爲太子取齊女，未入室，而宣公見所欲爲太子婦者好，説而自取之，更爲太子取他女。宣公得齊女，生子壽、子朔，令左公子傅之。太子伋母死，宣公正夫人與朔共讒惡太子伋。宣公自以其奪太子妻也，心惡太子，欲廢之。及聞其惡，大怒，乃使太子伋於齊而令盜遮界上殺之，與太子白旄，而告界盜見持白旄者殺之。且行，子朔之兄壽，太子異母弟也，知朔之惡太子而君欲殺之，乃謂太子曰：「界盜見太子白旄，卽殺太子，太子可毋行。」太子曰：「逆父命求生，不可。」遂行。壽見太子不止，乃盜其白旄而先馳至界。界盜見其驗，卽殺之。壽已死，而太子伋又至，謂盜曰：「所當殺乃我也。」盜并殺太子伋，以報宣公。宣公乃以子朔爲太子。十九年，宣公卒，太子朔立，是爲惠公。', 'text_layer': 'received_chapter'}], 'classification': {'id': 'c-shiji-130-taishigong:m049-0025', 'start': 25, 'end': 27, 'surface': '衛頃', 'kind': 'non_person', 'person_id': None, 'status': 'contextual_provisional', 'lexical_role': 'polity_predicate', 'basis_quote': '及朔之生，衛頃不寧；南子惡蒯聵，子父易名。', 'components': [{'role': 'polity', 'surface': '衛', 'start': 25, 'end': 26}, {'role': 'predicate', 'surface': '頃', 'start': 26, 'end': 27, 'editorial_reading': '傾', 'sense': '傾覆'}], 'human_reviewed': False, 'reviewer': 'AI source-context review', 'interpretation_note': '編輯首選衛國傾覆的事勢述語；保索隱釋衛頃公的競爭讀法。原字頃不改，非人物同指決定。', 'non_person_review': 'source-evidence/shiji130-weiqing-nonperson/review.json'}, 'competing_readings': [{'author': '司馬貞', 'title': '史記索隱', 'container': '史記三家註／卷130', 'url': 'https://zh.wikisource.org/wiki/史記三家註/卷130', 'read_scope': '太史公自序衛世家提要古注', 'quote': '衛頃公也。', 'printed_edition': None, 'image_verified': False}, {'author': '沈家本', 'title': '史記瑣言', 'chapter': '卷三', 'section': '自序', 'url': 'https://www.shidianguji.com/zh/book/CADAL02121458/chapter/1lmduzx7u6sky', 'provider': '識典古籍', 'catalogue_id': 'CADAL02121458', 'page_heading': '諸史瑣言卷三／史記三', 'quote': '衛頃不寧，索隱：衛頃公也。按：頃讀爲傾，傾覆也。謂朔讒殺太子而衛亂也。衛無頃公，索隱誤。', 'composition_date': None, 'earliest_extant_edition': None, 'printed_edition': None, 'digital_revision': None, 'reference_only': True, 'qualification': '實讀網頁頁首作者及頁末自序完整短條；未核影像、原印本或成書年份，不以此替換CBR底本，亦不宣稱已驗證其全部論斷。', 'image_verified': False}], 'prior_editorial_record_role': 'retired_source_annotation_not_historical_person', 'current_reading_mirrors': ['source-evidence/shiji130-stage3-identity/context-reading.json', 'source-evidence/shiji130-early-identity/context-reading.json', 'source-evidence/shiji130-remaining11-identity/context-reading.json']}
PRIOR_WITHOUT_ID_SHA256 = '1eeb90d1f0a080ccfd142c02a2a37815bdd1e4fb726d2331dd7f5fc6c38e5df8'
MIRRORS = ('source-evidence/shiji130-stage3-identity/context-reading.json', 'source-evidence/shiji130-early-identity/context-reading.json', 'source-evidence/shiji130-remaining11-identity/context-reading.json')

def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def _hash(data):
    return hashlib.sha256(data).hexdigest()

def _read(root, relative):
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError('Non-person review cannot escape root')
    return json.loads(target.read_text(encoding='utf-8'))

def _review(root, receipt=None):
    """Return the reserved annotation ID only after the complete fixed proof."""
    if root is None:
        raise ValueError('Non-person classification needs a source root')
    root = Path(root).resolve()
    review = _read(root, REVIEW_PATH)
    if not isinstance(review, dict):
        raise ValueError('Malformed non-person source review')
    fixed = {k: v for k, v in review.items()
             if k not in ('prior_editorial_record', 'prior_editorial_record_sha256')}
    if _canonical(fixed) != _canonical(REVIEW_FIXED):
        raise ValueError('Non-person source scope or qualification drift')
    prior = review.get('prior_editorial_record')
    if not isinstance(prior, dict) or not valid_person_id(prior.get('id')):
        raise ValueError('Negative review needs the former editorial record')
    old = prior['id']
    if _hash(_canonical({k: v for k, v in prior.items() if k != 'id'})) != PRIOR_WITHOUT_ID_SHA256:
        raise ValueError('Former annotation record no longer matches the bound source role')
    encoded = (json.dumps(prior, ensure_ascii=False, indent=2) + '\n').encode()
    if review.get('prior_editorial_record_sha256') != _hash(encoded):
        raise ValueError('Former annotation record audit hash drift')
    people = _read(root, 'registry/persons.json')
    if not isinstance(people, dict) or not isinstance(people.get('persons'), list):
        raise ValueError('Missing current registry')
    def contains(value):
        if isinstance(value, str):
            return value == old
        if isinstance(value, list):
            return any(contains(x) for x in value)
        if isinstance(value, dict):
            return any(k == old or contains(x) for k, x in value.items())
        return False
    if any(not isinstance(p, dict) or not valid_person_id(p.get('id')) for p in people['persons']):
        raise ValueError('Malformed current registry person')
    if any(p['id'].startswith(old + '_') for p in people['persons']):
        raise ValueError('Negative reservation cannot orphan structural descendants')
    if contains(people):
        raise ValueError('Non-person reservation cannot leave a current person or redirect')
    classification = review['classification']
    for position, support in enumerate(review['source_contexts']):
        chapter = _read(root, support['path'])
        if not isinstance(chapter, dict) or chapter.get('record_type') != 'marked_chapter' or not isinstance(chapter.get('paragraphs'), list) or any(not isinstance(p, dict) for p in chapter['paragraphs']):
            raise ValueError('Malformed source chapter')
        for key in ('id', 'work_id', 'book_id', 'source_id'):
            expected = support['chapter_id'] if key == 'id' else support[key]
            if chapter.get(key) != expected:
                raise ValueError('Non-person source identity drift')
        if _canonical(chapter.get('source')) != _canonical(support['source']):
            raise ValueError('Non-person source metadata drift')
        paragraphs = [p for p in chapter['paragraphs'] if p.get('id') == support['paragraph_id']]
        if len(paragraphs) != 1:
            raise ValueError('Non-person source paragraph missing or repeated')
        paragraph = paragraphs[0]
        if paragraph.get('text') != support['quote'] or paragraph.get('text_layer') != support['text_layer']:
            raise ValueError('Non-person complete quote or text layer drift')
        if position == 0:
            if not isinstance(paragraph.get('mentions'), list) or any(not isinstance(m, dict) for m in paragraph['mentions']):
                raise ValueError('Malformed source mentions')
            marks = [m for m in paragraph['mentions'] if m.get('id') == review['source_mention_id']]
            if _canonical(marks) != _canonical([classification]):
                raise ValueError('Non-person source mention or classification drift')
    for relative in MIRRORS:
        data = _read(root, relative)
        if relative == 'source-evidence/shiji130-remaining11-identity/context-reading.json':
            support = REVIEW_FIXED['source_contexts'][0]
            if (not isinstance(data, dict) or data.get('record_type') != 'source_context_identity_reading'
                    or data.get('human_reviewed') is not False or data.get('image_verified') is not False or data.get('model') is not None
                    or not isinstance(data.get('complete_units'), list)):
                raise ValueError('Third current mirror source qualification drift')
            units = [u for u in data['complete_units'] if isinstance(u, dict) and isinstance(u.get('paragraph'), dict)
                     and u['paragraph'].get('id') == support['paragraph_id']]
            if len(units) != 1:
                raise ValueError('Third current mirror complete unit missing or repeated')
            unit = units[0]
            if (unit.get('path') != support['path'] or unit.get('chapter_id') != support['chapter_id']
                    or _canonical(unit.get('source')) != _canonical(support['source'])
                    or unit['paragraph'].get('text') != support['quote'] or unit['paragraph'].get('text_layer') != support['text_layer']):
                raise ValueError('Third current mirror full quote/source scope drift')
        hits = []
        def visit(v):
            if isinstance(v, dict):
                if v.get('id') == review['source_mention_id']:
                    hits.append(v)
                for x in v.values():
                    visit(x)
            elif isinstance(v, list):
                for x in v:
                    visit(x)
        visit(data)
        if _canonical(hits) != _canonical([classification]):
            raise ValueError('Current source reading mirror classification drift')
    # Only the two validated negative records may carry this old annotation ID.
    # No directory-wide historical bypass and no hidden current ledger endpoint.
    for dirname in ('corpus', 'source-evidence', 'data/historical-tables'):
        for path in (root / dirname).rglob('*.json'):
            relative = path.relative_to(root).as_posix()
            if relative in (REVIEW_PATH, RECEIPT_PATH):
                continue
            if contains(_read(root, relative)):
                raise ValueError('Old non-person annotation remains a current endpoint: ' + relative)
    if receipt is None:
        receipt = _read(root, RECEIPT_PATH)
    expected_receipt = {
        'record_type': 'source_non_person_retirement_receipt',
        'non_person_review_id': REVIEW_ID,
        'review_path': REVIEW_PATH,
        'review_sha256': _hash((root / REVIEW_PATH).read_bytes()),
        'retired_person_ids': [old],
        'retirement_policy': 'audit_only_not_person_not_alias_not_reusable',
        'person_aliases_created': False,
    }
    if not isinstance(receipt, dict) or _canonical(receipt) != _canonical(expected_receipt):
        raise ValueError('Non-person reservation must bind its exact negative source review')
    return old

def ensure_receipt_complete(root):
    """A declared fixed non-person reading cannot silently lose its reservation."""
    root = Path(root).resolve()
    review_present = (root / REVIEW_PATH).is_file()
    receipt_present = (root / RECEIPT_PATH).is_file()
    declared = False
    source = root / 'corpus/shiji/130.json'
    if source.is_file():
        data = _read(root, 'corpus/shiji/130.json')
        if isinstance(data, dict) and isinstance(data.get('paragraphs'), list):
            for paragraph in data['paragraphs']:
                if not isinstance(paragraph, dict) or not isinstance(paragraph.get('mentions'), list):
                    continue
                declared = declared or any(isinstance(m, dict)
                    and m.get('id') == REVIEW_FIXED['source_mention_id']
                    and m.get('kind') == 'non_person' for m in paragraph['mentions'])
    if (declared or review_present or receipt_present) and not (review_present and receipt_present):
        raise ValueError('Declared non-person reading requires both its negative review and reservation')

def reservation_ids(root, path, receipt):
    if (not Path(path).resolve().is_relative_to(Path(root).resolve())
            or Path(path).resolve() != (Path(root).resolve() / RECEIPT_PATH).resolve()):
        raise ValueError('Unknown non-person reservation owner')
    return [_review(root, receipt)]

def polity_predicate_valid(mention, text, context=None):
    if not isinstance(mention, dict) or not isinstance(text, str) or not isinstance(context, dict):
        return False
    chapter, paragraph = context.get('chapter'), context.get('paragraph')
    if not isinstance(chapter, dict) or not isinstance(paragraph, dict):
        return False
    try:
        _review(context.get('root'))
        support = REVIEW_FIXED['source_contexts'][0]
        return (_canonical(mention) == _canonical(REVIEW_FIXED['classification'])
                and text == support['quote']
                and paragraph.get('id') == support['paragraph_id']
                and paragraph.get('text') == text
                and chapter.get('record_type') == 'marked_chapter'
                and chapter.get('id') == support['chapter_id']
                and chapter.get('source_id') == support['source_id']
                and _canonical(chapter.get('source')) == _canonical(support['source']))
    except (OSError, ValueError, KeyError, TypeError):
        return False
