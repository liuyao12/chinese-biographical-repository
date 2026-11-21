"""核對謝琰、肇、峻同死後官諡各歸何人。"""
def valid(holding, paragraphs, mentions, deaths):
    basis = holding.get('posthumous_basis') or holding.get('naming_basis') or {}
    if basis.get('kind') != 'named_jin079_family_death_award':
        return False
    try:
        evidence, = basis['evidence']
        cid, paragraph = paragraphs[evidence['paragraph_id']]
        recipient = mentions[basis['recipient_mid']][2]
        death = deaths[basis['death_event_id']]
        if (cid != 'c-jinshu-079-xielang-family' or evidence['quote'] != paragraph['text']
                or evidence['chapter_id'] != cid or evidence['person_mention_id'] != recipient['id']
                or recipient['person_id'] != holding['person_id'] or death['person_id'] != holding['person_id']
                or death['event_type'] != 'death' or death['source_term'] != '琰墮地，與二子肇、峻俱被害'
                or not any(e['chapter_id']==cid and e['paragraph_id'].endswith('phase6-line065')
                           and death['source_term'] in e['quote'] for e in death['evidence'])
                or holding['effective_period']['start']['evidence'] != [evidence]
                or holding['evidence'] != [evidence]):
            return False
        if paragraph['id'].endswith('phase6-line065'):
            clause='贈琰侍中、司空，諡曰忠肅。'
            roles={'侍中':('琰','posthumous_grant'), '司空':('琰','posthumous_grant'), '忠肅':('琰','posthumous_naming')}
        elif paragraph['id'].endswith('phase6-line067'):
            clause='及沒於賊，詔贈肇散騎常侍，峻散騎侍郎。'
            roles={'散騎常侍':('肇','posthumous_grant'),'散騎侍郎':('峻','posthumous_grant')}
        else:
            return False
        word, mode = roles[holding['title']]
        text = paragraph['text']
        a = text.index(clause)
        use, = holding['attestations']
        return (text.count(clause) == 1 and clause == basis['source_term']
                and mode == holding['mode'] and recipient['surface'] == word
                and recipient['start'] == a + clause.index(word)
                and use['start'] == a + clause.index(holding['title'])
                and use['end'] == use['start'] + len(holding['title'])
                and use['surface'] == holding['title'] and use['usage'] == 'posthumous_usage'
                and use['person_mention_id'] == recipient['id'])
    except (KeyError, TypeError, ValueError, IndexError):
        return False

def succession_valid(event, paragraphs):
    """核關係主語及兩種主語承接，保持親屬、爵名、爵國各欄的界線。"""
    try:
        e, = event['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        if (cid != 'c-jinshu-079-xielang-family' or e['chapter_id'] != cid or e['quote'] != p['text']
                or event['status'] != 'source_attested' or event['title'] is not None or event['holding_id'] is not None
                or event.get('date_expression') is not None or any(k in event for k in ('normalized_date','normalized_date_range'))):
            return False
        a = next(m for m in p['mentions'] if m['id'] == e['person_mention_id'])
        b=event['source_clause_binding'];role=b['role'];t=p['text']
        if b['kind']!='jin079_named_noble_successor' or a['person_id']!=event['person_id'] or t.count(b['clause'])!=1:
            return False
        if role=='son_succeeds' and p['id'].endswith('xieyao-line057'):
            first,son=[next(m for m in p['mentions'] if m['surface']==s) for s in ('瑤','該')]
            return (t.startswith('瑤襲爵，官至琅邪王友，早卒。子該嗣，終東陽太守。') and a==son
                    and b['clause']=='早卒。子該嗣，終東陽太守。' and event['source_term']=='嗣'
                    and event['event_type']=='noble_title_succession' and event['mode']=='accession'
                    and first['person_id']==event['predecessor_person_id'])
        if not p['id'].endswith('phase6-line071') or a['surface']!='混' or a['start']!=t.index('混竟尚主，襲父爵。'):
            return False
        if role=='abolished':
            return (b['clause']=='以党劉毅誅，國除。' and event['source_term']=='國除'
                    and event['event_type']=='noble_state_abolition' and 'predecessor_person_id' not in event
                    and 'mode' not in event)
        line = paragraphs[cid+':phase6-line065'][1]
        pos = line['text'].index('送琰小子混')
        father = next(m for m in line['mentions'] if m['start']==pos+1 and m['surface']=='琰')
        son = next(m for m in line['mentions'] if m['start']==pos+4 and m['surface']=='混')
        return (role=='inherits_father' and b['clause']=='混竟尚主，襲父爵。' and event['source_term']=='襲父爵'
                and event['event_type']=='noble_title_succession' and event['mode']=='accession'
                and son['person_id']==a['person_id'] and father['person_id']==event['predecessor_person_id'])
    except (KeyError, TypeError, ValueError, IndexError, StopIteration):
        return False
