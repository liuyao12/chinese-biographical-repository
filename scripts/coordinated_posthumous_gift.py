"""受者列於追贈動詞與官名間、封爵續同一受者的證據。"""

def validate(holding, paragraphs, mentions, events):
    try:
        mode = holding['mode']
        basis_name, kind = {
            'posthumous_enfeoffment': ('enfeoffment_basis', 'noble_rank'),
            'posthumous_grant': ('posthumous_basis', 'office'),
        }[mode]
        b = holding[basis_name]
        if b['kind'] != 'named_posthumous_recipient_coordinated_gift' or holding['kind'] != kind:
            return False
        title = holding['title']
        evidence, = holding['evidence']
        occurrence, = holding['attestations']
        if b['evidence'] != [evidence] or holding['effective_period']['start']['evidence'] != [evidence]:
            return False
        chapter, p = paragraphs[evidence['paragraph_id']]
        indexed_chapter, indexed_paragraph, m = mentions[b['recipient_mention_id']]
        if (indexed_chapter != chapter or indexed_paragraph != p['id']
                or m['kind'] != 'person' or m['person_id'] != holding['person_id']
                or occurrence['person_mention_id'] != m['id'] or evidence['person_mention_id'] != m['id']
                or occurrence['usage'] != 'posthumous_usage' or evidence['quote'] != p['text']):
            return False
        source = b['source_term']
        recipient = m['surface']
        text = p['text']
        if text.count(source) != 1 or not source.startswith('追贈' + recipient):
            return False
        pos = text.index(source)
        if m['start'] != pos + 2 or m['end'] != m['start'] + len(recipient):
            return False
        grant, enfeoff = source[len('追贈'+recipient):].split('，封')
        if not grant or not enfeoff or any(ch in grant + enfeoff for ch in '，。！？；「」'):
            return False
        if ((mode == 'posthumous_grant' and title != grant)
                or (mode == 'posthumous_enfeoffment' and title != enfeoff)
                or occurrence['start'] != pos + source.index(title)
                or occurrence['end'] != occurrence['start'] + len(title)
                or text[occurrence['start']:occurrence['end']] != title):
            return False
        if any(person['id'] != m['id'] and person['kind'] == 'person'
               and pos <= person['start'] < pos + len(source) for person in p['mentions']):
            return False
        death = events[b['death_event_id']]
        if death['event_type'] != 'death' or death['person_id'] != m['person_id']:
            return False
        d = death['source_anchor']
        if (d['paragraph_id'] != p['id'] or d['end'] >= pos
                or text[d['start']:d['end']] != death['source_term']):
            return False
        term = death['source_term']
        if not term.endswith('所誅'):
            # 南史王叡傳作「元德為玄誅」，以句中具名者核「為＋施事＋誅」。
            if not (term.startswith('為') and term.endswith('誅') and any(
                    x['kind'] == 'person' and x['person_id'] != m['person_id']
                    and x['start'] == d['start'] + 1 and x['end'] == d['end'] - 1
                    and x['surface'] == term[1:-1] for x in p['mentions'])):
                return False
        return any(x['kind'] == 'person' and x['person_id'] == m['person_id']
                   and x['end'] == d['start'] for x in p['mentions'])
    except (KeyError, TypeError, ValueError, IndexError):
        return False
