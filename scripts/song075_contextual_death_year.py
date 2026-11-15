# -*- coding: utf-8 -*-
"""Validate Wang Sengda's context-inferred death year without misusing the revolt date."""


def valid(event, date, chapter):
    try:
        source = chapter.get('source', {})
        if (chapter.get('id') != 'c-songshu-075-wangsengda'
                or chapter.get('work_id') != 'w-songshu'
                or chapter.get('book_id') != 'b-songshu-075'
                or chapter.get('source_id') != 's-songshu-075-wangsengda'
                or source.get('revision_id') != 1997722
                or source.get('permalink') != 'https://zh.wikisource.org/w/index.php?title=宋書/卷75&oldid=1997722'
                or source.get('image_verified') is not False
                or event.get('id') != 'le-song075-wangsengda-death'
                or event.get('event_type') != 'death'
                or event.get('person_id') != '7r6_k52_qji_ABAAAAAB'
                or event.get('source_term') != '於獄賜死'
                or event.get('date_expression') is not None
                or date.get('year') != 458 or date.get('era') != 'CE'
                or date.get('era_year') != 458
                or date.get('precision') != 'year'
                or date.get('calendar') != 'chinese_civil'
                or date.get('year_numbering') != 'astronomical'
                or date.get('status') != 'editorial_provisional'
                or date.get('source_expression') != '二年'
                or date.get('original_quote') is None
                or event.get('interpretation_note', '').find('不把八月一日當死日') < 0):
            return False
        paragraphs = {p['id']: p for p in chapter['paragraphs']}
        p42 = paragraphs['c-songshu-075-wangsengda:line042']
        p44 = paragraphs['c-songshu-075-wangsengda:line044']
        q42, q44 = p42['text'], p44['text']
        expected_source = chapter['source_id']
        if (date['original_quote'] != q42 or '大明元年' not in q42 or '二年，遷中書令' not in q42
                or '二年八月一日' not in q44 or '於獄賜死' not in q44
                or event.get('source_anchor') != {'paragraph_id': p44['id'],
                                                    'start': q44.index('於獄賜死'),
                                                    'end': q44.index('於獄賜死') + len('於獄賜死'),
                                                    'surface': '於獄賜死'}):
            return False
        order = [p['id'] for p in chapter['paragraphs']]
        if order.index(p42['id']) >= order.index(p44['id']):
            return False
        direct = event.get('evidence', [])
        if (len(direct) != 1 or direct[0].get('work_id') != 'w-songshu'
                or direct[0].get('book_id') != 'b-songshu-075'
                or direct[0].get('chapter_id') != chapter['id']
                or direct[0].get('paragraph_id') != p44['id']
                or direct[0].get('quote') != q44 or direct[0].get('source_id') != expected_source
                or direct[0].get('person_mention_id') != 'c-songshu-075-wangsengda:line044:m0145'):
            return False
        mention = next((m for m in p44['mentions'] if m['id'] == direct[0]['person_mention_id']), None)
        if not mention or mention.get('person_id') != event['person_id']:
            return False
        evidence = date.get('evidence', [])
        if ([e.get('paragraph_id') for e in evidence] != [p42['id'], p44['id']]
                or any(e.get('source_id') != expected_source or e.get('quote') != paragraphs[e['paragraph_id']]['text']
                       or e.get('work_id') != 'w-songshu' or e.get('book_id') != 'b-songshu-075'
                       or e.get('chapter_id') != chapter['id'] for e in evidence)):
            return False
        mapping = date.get('regnal_year_mapping', {})
        if (mapping.get('kind') != 'ce_regnal_era_span' or mapping.get('era_name') != '大明'
                or mapping.get('source_number') != '二' or mapping.get('regnal_year') != 2
                or mapping.get('start_ce_year') != 457 or mapping.get('end_ce_year') != 464
                or date.get('references', [{}])[0].get('quote') != '大明'
                or date['references'][0].get('columns', {}).get('first_year') != '457'
                or date['references'][0].get('columns', {}).get('last_year') != '464'
                or date['references'][0].get('image_verified') is not False):
            return False
        binding_record = date.get('contextual_death_year_binding', {})
        if (binding_record != {'kind': 'same_biographical_unit_death_year',
                               'prior_year_expression': '大明元年',
                               'continued_year_expression': '二年',
                               'event_date_expression': None,
                               'contextual_year_source_expression': '二年',
                               'rationale': '年號承接暫定推定；八月一日是謀反起兵計畫日，不是死日。'}):
            return False
        binding = date.get('era_context_binding', {})
        if (binding.get('kind') != 'same_biographical_unit_era_continuation'
                or binding.get('prior_expression') != '大明元年'
                or binding.get('source_expression') != '二年'
                or binding.get('evidence') != [evidence[0]]):
            return False
        if date.get('regnal_year_mapping', {}).get('era_name') != '大明':
            return False
        if event.get('date_context') is not None:
            return False
        return True
    except (KeyError, TypeError, ValueError, IndexError):
        return False
