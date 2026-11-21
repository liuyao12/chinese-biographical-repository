"""Bind the name in an inscription's introduction to its separate family list."""

import re


def valid(assertion, chapter):
    try:
        context = assertion['context']
        head_id, list_id = context['paragraph_ids']
        paragraphs = {p['id']: p for p in chapter['paragraphs']}
        head, relatives = paragraphs[head_id], paragraphs[list_id]
        if head is not chapter['paragraphs'][0] or head is relatives:
            return False
        first, second = assertion['evidence']
        for entry, paragraph in ((first, head), (second, relatives)):
            if (any(entry[k] != chapter[k] for k in ('source_id', 'book_id', 'work_id'))
                    or entry['chapter_id'] != chapter['id'] or entry['paragraph_id'] != paragraph['id']
                    or entry['quote'] != paragraph['text']):
                return False
        def selected(p, mid):
            m = next(m for m in p['mentions'] if m['id'] == mid and m['kind'] == 'person')
            assert p['text'][m['start']:m['end']] == m['surface']
            return m
        principal = selected(head, context['head_mention_id'])
        member = selected(relatives, context['member_mention_id'])
        if not head['text'].startswith('君諱' + principal['surface'] + '，字') or principal['start'] != 2:
            return False
        term = assertion['qualifiers']['source_term']
        if not term.endswith(member['surface']):
            return False
        start = member['end'] - len(term)
        if start < 0 or relatives['text'][start:member['end']] != term:
            return False
        role = term[:-len(member['surface'])]
        predicate = assertion['predicate']
        member_is_subject = (
            predicate == 'brother' and role in ('君次弟', '君第四弟')
            or predicate == 'father' and role in ('君長息', '次息', '君長女')
            or predicate == 'spouse' and role == '夫人南陽' and start == 0
        )
        member_is_object = ((predicate, role) in (('father', '亡父'), ('grandfather', '亡祖')))
        if not (member_is_subject or member_is_object):
            return False
        if role == '次息':
            # The member must belong to the uninterrupted list begun by 君長息.
            if not re.search(r'君長息[^。]+。(?:次息[^。]+。)*$', relatives['text'][:start]):
                return False
        main_role, member_role = ('object', 'subject') if member_is_subject else ('subject', 'object')
        return (assertion[main_role + '_person_id'] == principal['person_id']
                and assertion[member_role + '_person_id'] == member['person_id']
                and first[main_role + '_person_mention_id'] == principal['id']
                and second[member_role + '_person_mention_id'] == member['id'])
    except (KeyError, ValueError, TypeError, StopIteration, AssertionError):
        return False
