# coding: utf-8
"""Verify the speaker's two named sons-of-Si clauses in his proposal."""
def valid(a,e,chapter):
    forms = {
        'c-nanqishu-032-wangchang': ('從孫長是故左衞將軍嗣息', '長', '嗣'),
        'c-nanqishu-032-wangtong': ('嗣小息佟', '佟', '嗣'),
    }
    if chapter.get('source', {}).get('revision_id') != 1513918 or chapter['id'] not in forms:
        return False
    term, son, father = forms[chapter['id']]
    p = next((v for v in chapter['paragraphs'] if v['id'] == e.get('paragraph_id')), None)
    if not p or p['source_position']['first_line'] != 19 or p['text'].count(term) != 1:
        return False
    if a['predicate'] != 'father' or a['qualifiers']['source_term'] != term or e['quote'] != p['text']:
        return False
    mentions = {m['id']:m for m in p['mentions']}
    for role, name in [('subject', son), ('object', father)]:
        m = mentions.get(e.get(role + '_person_mention_id'))
        start = p['text'].index(term) + term.index(name)
        if not m or (m['start'], m['end'], m['surface'], m['person_id']) != (start,start + len(name),name,a[role + '_person_id']):
            return False
    return a['qualifiers']['lineage'] == 'paternal'
