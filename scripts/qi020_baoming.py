"""核對文安皇后父母各自的贈號與該句的受贈人。"""

CHAPTERS = {
    'c-nanqishu-020-wangbaoming': ('父', 1),
    'c-nanqishu-020-wangbaoming-wyd': ('父', 1),
    'c-nanshi-011-wangbaoming': ('曄之', 0),
    'c-nanshi-011-wangbaoming-izumo': ('曄之', 0),
}


def parent_grant_valid(holding, paragraphs, mentions):
    try:
        basis = holding['posthumous_basis']
        e, = basis['evidence']
        citation, = holding['evidence']
        at, = holding['attestations']
        cid, p = paragraphs[e['paragraph_id']]
        father_name, paragraph_index = CHAPTERS[cid]
        pid = p['id']
        text = p['text']
        prefix = '贈后父' + ('曄之' if father_name == '曄之' else '')
        terms = {
            '金紫光祿大夫': ('e8b_fms_9mk', father_name, prefix + '金紫光祿大夫'),
            '豐安縣君': ('vvf_ol4_jvc', '桓氏', '母桓氏豐安縣君'),
        }
        owner, surface, term = terms[holding['title']]
        marked_cid, marked_pid, marked = mentions[at['person_mention_id']]
        start = text.index(term)
        title_start = start + term.index(holding['title'])
        owner_start = start + term.index(surface)
        return (holding['mode'] == 'posthumous_grant' and holding['person_id'] == marked['person_id'] == owner
                and basis['kind'] == 'qi020_baoming_parent_grant' and basis['source_term'] == e['quote'] == term
                and cid == marked_cid == e['chapter_id'] == citation['chapter_id'] and e['source_id'] == citation['source_id']
                and pid == f'{cid}:p{paragraph_index + 1:03}' == marked_pid == at['paragraph_id'] == citation['paragraph_id']
                and citation['quote'] == text and citation['person_mention_id'] == marked['id']
                and (marked['start'], marked['end'], marked['surface']) == (owner_start, owner_start + len(surface), surface)
                and (at['start'], at['end'], at['surface']) == (title_start, title_start + len(holding['title']), holding['title'])
                and holding['effective_period']['start'] == dict(status='source_event', event_type='posthumous_grant',
                                                               date_expression=None, evidence=[e])
                and prefix + '金紫光祿大夫母桓氏豐安縣君' in text.replace('，', ''))
    except (IndexError, KeyError, TypeError, ValueError):
        return False
