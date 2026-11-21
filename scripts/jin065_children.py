"""王悅傳稱襲導爵。王琨、王嘏與王恢三人各有本句，丹陽尹另為官職。"""
def source_roles(paragraph):
    text = paragraph['text']
    names = {m['start']: m for m in paragraph['mentions'] if m['kind'] == 'person'
             and text[m['start']:m['end']] == m['surface']}
    if text != '悅無子，以弟恬子琨爲嗣，襲導爵丹陽尹，卒，贈太常。子嘏嗣，尚鄱陽公主，歷中領軍、尚書。卒，子恢嗣，義熙末，爲遊擊將軍。':
        raise ValueError('嗣爵原句有異')
    return {m['surface']: m for i,m in names.items() if i in (0,6,8,13,26,46)}

def succession_valid(event, paragraphs):
    try:
        e, = event['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        ms = source_roles(p)
        pairs = {'琨': ('導','襲導爵'), '嘏': ('琨','嗣'), '恢': ('嘏','嗣')}
        recipient, predecessor, term = next((name, before, term) for name,(before,term) in pairs.items()
                                             if ms[name]['id'] == e['person_mention_id'])
        binding = event['source_clause_binding']
        return (cid == e['chapter_id'] == 'c-jinshu-065-wangdao-family'
                and p.get('text_layer') == 'received_chapter' and e['quote'] == p['text']
                and binding == {'kind':'jin065_yue_named_heirs','recipient':ms[recipient]['id'],
                                'predecessor':ms[predecessor]['id']}
                and event.get('source_term') == term and event['person_id'] == ms[recipient]['person_id']
                and event['predecessor_person_id'] == ms[predecessor]['person_id']
                and event.get('title') is None and event.get('holding_id') is None
                and event['event_type'] == 'noble_title_succession' and event.get('mode') == 'accession'
                and event.get('date_expression') is None and event.get('human_reviewed') is False)
    except (KeyError, TypeError, StopIteration, ValueError): return False

def gift_valid(holding, paragraphs, mentions, events):
    try:
        b = holding['posthumous_basis']
        e, = b['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        text = p['text']
        subject = mentions[b['recipient_person_mention_id']][2]
        death = events[b['death_event_id']]
        if holding['title'] == '太常':
            referred = source_roles(p)['琨']
            context = '襲導爵丹陽尹，卒，贈太常。'
        else:
            referenced = [m for m in p['mentions'] if m['kind']=='person' and m['start']==0]
            referred, = referenced
            if referred['surface'] != '恬' or not text.startswith('恬字敬豫。') or not text.endswith('卒，贈中軍將軍，諡曰憲。'):return False
            context = '卒，贈中軍將軍，諡曰憲。'
        clause = '卒，贈' + holding['title']
        a, = holding['attestations']
        return (cid == e['chapter_id'] == 'c-jinshu-065-wangdao-family'
                and text.count(context) == 1 and p.get('text_layer') == 'received_chapter'
                and b['source_term'] == context and e['quote']==text
                and clause in context and holding['kind']=='office' and holding['mode']=='posthumous_grant'
                and b['evidence']==holding['evidence']==holding['effective_period']['start']['evidence']
                and a['start'] == text.index(context)+context.index(clause)+3
                and text[a['start']:a['end']] == a['surface'] == holding['title']
                and a['person_mention_id']==e['person_mention_id']==subject['id']==referred['id']
                and death['event_type']=='death' and death['person_id']==subject['person_id']==holding['person_id']
                and any(x['paragraph_id']==p['id'] and x['quote']==text for x in death['evidence']))
    except (StopIteration, ValueError, TypeError, KeyError, IndexError):return False
