"""Check the named and titled parties in the fixed Xie Tiao family clauses."""
import hashlib
from pathlib import Path

RAW = {
    1531762: '2f1bbb6150c723a3839e2f5a81f1a7522e3414465b8d8a11e23a164b43368964',
    2311630: 'e7ada4fcb0bc732993f40d1e23f8250e09c37d2e3e42e6e19986d2ab0b3a2f29',
    2438183: '241b419879752537be71f31d3940595b30fbfdbfdeb8af53d2acb614fa007abb',
    2272731: '2459124c61a488a22b5213cfefd1ca38d0015243f9471998260692781a016207',
    1507997: '0dcd8247799793e88edf3bee9a4b72eb5e0b0097a2bd2b84c8888c828c95feac',
    2074177: '2c014418a1f8c5d3ce3fff8502fb7694f4b7266638217fe4f10df10170cb6acc',
    1566494: '21670cf990a423b37ee0c2c543213171ea42439e787c2dd671af5f6868b47e3d',
}
royal_id = 'c-nanqishu-006-xietiao-ming'
wife_id = 'c-nanqishu-020-xietiao-jing'
princess_id = 'c-liangshu-007-xietiao-princesses'
south_id = 'c-nanshi-019-xietiao'
# Titles are checked against actual named people in a second source.
royal = ((2311630, 11, '高宗明皇帝諱鸞'),)
wife = ((2074177, 46, '明敬劉皇后諱惠端'),)
daughters = ((1566494, 27, '生永興公主玉姚，永世公主玉婉'), (1566494, 23, '高祖德皇后郗氏，諱徽'))
wedding = '帝以大女永興公主適叡子鈞，第二女永世公主適朓子謨'
# Main chapter and line, exact clause, predicate, ordered textual endpoints, auxiliary clauses.
CASES = {
    'a-qi-tiao-father-10': ('c-nanqishu-007-xietiao-donghun', 10, '東昏侯寶卷字智藏，高宗第二子也。', 'father', '寶卷', '高宗', royal),
    'a-qi-tiao-father-25': ('c-nanqishu-050-xietiao-princes', 25, '巴陵隱王寶義字智勇，明帝長子也。', 'father', '寶義', '明帝', royal),
    'a-qi-tiao-father-28': ('c-nanqishu-050-xietiao-princes', 28, '江夏王寶玄字智深，明帝第三子也。', 'father', '寶玄', '明帝', royal),
    'a-qi42-tiao-xuan-sister': ('c-nanqishu-042-xietiao-jiang', 76, '敬皇后弟劉暄', 'brother', '劉暄', '敬皇后', wife),
    'a-nanshi019-tiao-yao-father': (south_id, 138, wedding, 'father', '永興公主', '帝', daughters),
    'a-nanshi019-tiao-wan-father': (south_id, 138, wedding, 'father', '永世公主', '帝', daughters),
    'a-nanshi019-tiao-yao-marriage': (south_id, 138, wedding, 'spouse', '永興公主', '鈞', daughters),
    'a-nanshi019-tiao-wan-marriage': (south_id, 138, wedding, 'spouse', '永世公主', '謨', daughters),
}


def raw_lines(root, rel, rev):
    p = (Path(root) / rel).resolve()
    base = Path(root).resolve()
    if Path(rel).is_absolute() or not p.is_relative_to(base) or p != base / rel:
        raise ValueError(rel)
    blob = p.read_bytes()
    if hashlib.sha256(blob).hexdigest() != RAW[rev]:
        raise ValueError(rev)
    return blob.decode('utf-8').splitlines()


def valid(a, chapters, root):
    try:
        cid, line_no, term, pred, subject, obj, supports = CASES[a['id']]
        ch = chapters[cid]
        e, = a['evidence']
        para = next(p for p in ch['paragraphs'] if p['id'] == e['paragraph_id'])
        t = para['text']
        b = a['qualifiers']['reading_basis']
        loc = para['source_position']
        rev = ch['source']['revision_id']
        before = t.index(term)
        if (a['predicate'] != pred or a['qualifiers']['source_term'] != term
                or b['kind'] != 'xietiao_named_or_titled_kin' or b['source_revision'] != rev
                or e['chapter_id'] != cid or e['source_id'] != ch['source_id'] or e['quote'] != t
                or loc['first_line'] != line_no or loc['last_line'] != line_no or t.count(term) != 1
                or term not in raw_lines(root, ch['source']['raw_path'], rev)[line_no-1]
                or b['clause'] != {'start':before, 'end':before+len(term), 'surface':term}
                or len(b['support']) != len(supports)):
            return False
        for ext,(v,n,s) in zip(b['support'],supports):
            line = raw_lines(root,ext['raw_path'],v)[n-1]
            i = line.index(s)
            if (ext['revision_id'], ext['raw_sha256'], ext['line'], ext['start'], ext['end'], ext['surface']) != (v, RAW[v], n, i, i+len(s), s):
                return False
        named = {m['id']:m for m in para['mentions'] if m['kind']=='person'}
        refs = {m['id']:m for m in ch['annotation']['person_reference_occurrences'] if m['paragraph_id']==para['id']}
        ends = b['endpoints']
        if len(ends) != 2:
            return False
        for ep, surf, role in zip(ends, (subject,obj), ('subject_person_id','object_person_id')):
            m = (refs if surf in ('高宗','明帝','敬皇后','永興公主','永世公主','帝') else named)[ep['id']]
            i = before+term.index(surf)
            if (ep!={k:m[k] for k in ('id','surface','start','end','person_id')}
                    or (m['start'],m['end'],m['surface'],m['person_id'])!=(i,i+len(surf),surf,a[role])):
                return False
            if surf in ('高宗','明帝','敬皇后','永興公主','永世公主'):
                other_id, name = {'高宗':(royal_id,'鸞'), '明帝':(royal_id,'鸞'), '敬皇后':(wife_id,'惠端'),
                                  '永興公主':(princess_id,'玉姚'), '永世公主':(princess_id,'玉婉')}[surf]
                if not any(z.get('surface')==name and z.get('person_id')==a[role] and z.get('kind')=='person'
                           for p in chapters[other_id]['paragraphs'] for z in p['mentions']):
                    return False
            if surf=='帝':
                # The same sentence opens with 梁武, then 帝. Verify its fixed
                # antecedent, not any ruler who happens to appear in the chapter.
                if not any(z['surface']=='梁武' and z['person_id']==a[role] and z['start']<i for z in refs.values()):
                    return False
        return a['subject_person_id']!=a['object_person_id']
    except (KeyError, ValueError, IndexError, StopIteration, TypeError, OSError):
        return False
