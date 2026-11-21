# coding: utf-8
"""謝石傳末三次承嗣及國除，各以同段實際名錨定端點。"""
def valid(event, paragraphs):
    try:
        e, = event['evidence']
        chapter, p = paragraphs[e['paragraph_id']]
        if chapter != 'c-jinshu-079-xielang-family' or p['id'] != chapter + ':exp-xieshi-p004':
            return False
        text = '子汪嗣，早卒。汪從兄沖以子明慧嗣，為孫恩所害。明慧從兄喻復以子暠嗣。宋受禪，國除。'
        if p['text'] != text or e['quote'] != text or e['chapter_id'] != chapter:
            return False
        ms = {m['start']: m for m in p['mentions'] if m['kind'] == 'person'}
        heads = {'wang': (1, '汪', '子汪嗣', None), 'minghui': (13, '明慧', '汪從兄沖以子明慧嗣', 7),
                 'hao': (31, '暠', '明慧從兄喻復以子暠嗣', 23),
                 'abolition': (31, '暠', '宋受禪，國除', 31)}
        role = event['source_clause_binding']['role']
        at, word, clause, prev = heads[role]
        subject = ms[at]
        if (event['source_clause_binding'] != {'kind':'jin079_shi_heirs', 'role':role, 'clause':clause}
                or e['person_mention_id'] != subject['id'] or subject['surface'] != word
                or subject['person_id'] != event['person_id'] or event['title'] is not None
                or event['holding_id'] is not None or event['status'] != 'source_attested'):
            return False
        if role == 'abolition':
            return (event['event_type'] == 'noble_state_abolition' and event['source_term'] == '國除'
                    and event['date_expression'] == '宋受禪' and 'predecessor_person_id' not in event)
        if prev is None:
            q = paragraphs[chapter + ':exp-xieshi-p003'][1]
            predecessor = next(m for m in q['mentions'] if m['start'] == 0 and m['surface'] == '石')
        else:
            predecessor = ms[prev]
        return (event['event_type'] == 'noble_title_succession' and event['mode'] == 'accession'
                and event['predecessor_person_id'] == predecessor['person_id']
                and event['source_term'] == '嗣' and event['date_expression'] is None)
    except (AttributeError, KeyError, TypeError, ValueError, StopIteration):
        return False
