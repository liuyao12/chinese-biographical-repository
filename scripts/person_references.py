"""核對篇內非姓名人物指涉。字位以固定原文的 Unicode 碼點計。"""


def reference_errors(chapter, person_ids):
    rows = chapter.get('annotation', {}).get('person_reference_occurrences', [])
    if not isinstance(rows, list):
        return [chapter['id'] + '：人物指涉須為陣列']
    if not rows:
        return []
    paragraphs = {p['id']: p for p in chapter['paragraphs']}
    used = {m['id'] for p in chapter['paragraphs'] for m in p['mentions']}
    positions = set()
    errors = []
    for row in rows:
        if not isinstance(row, dict):
            errors.append(chapter['id'] + '：人物指涉須為物件')
            continue
        key = row.get('id')
        p = paragraphs.get(row.get('paragraph_id'))
        if not p or not isinstance(key, str) or not key.startswith(p['id'] + ':') or key in used:
            errors.append(f'{key}：指涉 ID 或所屬段落無效')
            continue
        used.add(key)
        a, b = row.get('start'), row.get('end')
        text, quote = p['text'], row.get('quote')
        if (type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text)
                or text[a:b] != row.get('surface') or not isinstance(quote, str)
                or not any(text.startswith(quote, i) and b <= i + len(quote)
                           for i in range(max(0, b - len(quote)), a + 1))):
            errors.append(f'{key}：指涉字位或引文未涵蓋該處')
            continue
        position = (p['id'], a, b)
        if position in positions or any(m['start'] < b and a < m['end'] for m in p['mentions']):
            errors.append(f'{key}：指涉與另一處標記重疊')
        positions.add(position)
        if (row.get('person_id') not in person_ids
                or row.get('referent_role') not in ('speaker_self', 'addressee', 'third_person')
                or not isinstance(row.get('note'), str) or not row['note'].strip()):
            errors.append(f'{key}：須記現役人物、在語句中的角色與判讀依據')
    return errors
