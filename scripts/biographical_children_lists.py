"""完整傳主單元的明列子名單；名單次序不是出生排行。"""
import hashlib
import re
try:
    from .biographical_kinship import digital_paratext_errors, received_paragraphs_contiguous
    from .subject_continuation import verified_blank_gap
except ImportError:
    from biographical_kinship import digital_paratext_errors, received_paragraphs_contiguous
    from subject_continuation import verified_blank_gap


def children_list_errors(assertion, chapter, parse_number):
    def fail(message): return ['傳主子名單：' + message]
    ctx = assertion.get('context', {})
    ids = ctx.get('paragraph_ids'); paras = chapter.get('paragraphs', [])
    by = {p['id']: p for p in paras}; order = [p['id'] for p in paras]
    if (ctx.get('kind') != 'biographical_children_list' or assertion.get('predicate') != 'father'
            or assertion.get('status') != 'source_attested'
            or ctx.get('status') != 'contextual_provisional' or ctx.get('human_reviewed') is not False
            or not ctx.get('rationale') or not isinstance(ids, list) or len(ids) < 2
            or len(set(ids)) != len(ids) or any(i not in by for i in ids)
            or ids != [e.get('paragraph_id') for e in assertion.get('evidence', [])]):
        return fail('必須保留完整單元各段、編輯判讀及一段一引文。')
    if ids != order[order.index(ids[0]):order.index(ids[-1])+1]:
        return fail('不得跳過所錄正文。')
    revision = chapter.get('source', {}).get('revision_id')
    if type(revision) is not int or digital_paratext_errors(chapter):
        return fail('缺固定見證或數位節題不純。')
    selected = [by[i] for i in ids]
    for p, e in zip(selected, assertion['evidence']):
        loc = p.get('source_position', {}); text = p.get('text')
        if (p.get('text_layer') != 'received_chapter' or loc.get('editorial_excerpt_boundary') is not True
                or loc.get('revision_id') != revision or type(loc.get('first_line')) is not int
                or type(loc.get('last_line')) is not int or loc['first_line'] > loc['last_line']
                or e.get('paragraph_id') != p['id'] or e.get('quote') != text
                or any(e.get(k) != chapter.get(k) for k in ['work_id','book_id','source_id'])
                or e.get('chapter_id') != chapter.get('id')
                or not isinstance(text, str) or hashlib.sha256(text.encode()).hexdigest() != p.get('text_sha256')):
            return fail('段落、引文、原行、文字層或修訂不符。')
    for a, b in zip(selected, selected[1:]):
        if not (received_paragraphs_contiguous(chapter, a, b)
                or verified_blank_gap(chapter, a['source_position'], b['source_position'])):
            return fail('來源行不能略過正文，只許已驗純空行或數位節題。')
    first, last = selected[0], selected[-1]
    parent = next((m for m in first.get('mentions', []) if m['id'] == ctx.get('parent_mention_id')), None)
    if (not parent or parent.get('kind') != 'person' or parent.get('person_id') != assertion.get('object_person_id')
            or parent.get('start') != 0 or first['text'][:parent.get('end', 0)] != parent.get('surface')):
        return fail('父親須是完整單元開首具名傳主，不能用中間出現的人。')
    # 數位節題只校驗選錄邊界；父親身份仍由正文段首人物錨點給出。
    heading = ctx.get('opening_heading_source_lines')
    records = chapter['source'].get('normalization', {}).get('omitted_digital_paratext', [])
    matching = [x for x in records if x.get('source_lines') == heading]
    if (len(matching) != 1 or not isinstance(heading, list) or len(heading) != 2
            or heading[1] + 1 != first['source_position']['first_line']
            or matching[0]['raw_quote'].strip().strip('=') != parent['surface']):
        return fail('單元開首須有固定原行的同名數位節題；不能從別人的中段開始。')
    unit = ctx.get('unit_id')
    if not unit or any(p.get('unit_id') != unit for p in selected):
        return fail('不得跨傳主單元。')
    match = re.fullmatch(r'有([一二三四五六七八九十百兩]+)子：([^。]+)。', last['text'])
    if not match: return fail('名單須是完整明列有幾子句，不從後續敘事猜子女。')
    count = parse_number(match[1]); names = match[2].split('、')
    mids = ctx.get('list_member_mention_ids')
    if (type(count) is not int or count < 1 or len(names) != count
            or not isinstance(mids, list) or len(mids) != count or len(set(mids)) != count
            or assertion.get('qualifiers', {}).get('source_term') != '有'+match[1]+'子'
            or assertion.get('qualifiers', {}).get('lineage') != 'paternal'):
        return fail('原數、人數、親屬詞或名單錨點數不符。')
    members = []; cursor = match.start(2)
    for name, mid in zip(names, mids):
        m = next((m for m in last.get('mentions', []) if m['id'] == mid), None)
        if (not m or m.get('kind') != 'person' or not m.get('person_id')
                or m.get('surface') != name or m.get('start') != cursor or m.get('end') != cursor+len(name)):
            return fail('名單字面與字位必須逐人相符。')
        members.append(m);cursor += len(name)+1
    if len({m['person_id'] for m in members}) != count or any(m['person_id'] == assertion['object_person_id'] for m in members):
        return fail('明列子女須為不同身份，不能把兩子或父子合併。')
    child = next((m for m in members if m['id'] == ctx.get('child_mention_id')), None)
    if not child or child['person_id'] != assertion.get('subject_person_id'):
        return fail('子女須是本名單中正確錨點及身份。')
    if any(k in assertion.get('qualifiers', {}) for k in ['ordinal','reported_order','birth_order','relative_birth_order']):
        return fail('名單次序不能自動變成出生排行；另有明文應另記。')
    return []
