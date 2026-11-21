"""Read the last will, beneficiary of the qin, death, and posthumous office at their received positions."""
from hashlib import sha256


def valid(holding, paragraphs, mentions, events):
    try:
        basis=holding['posthumous_basis']; evidence,=holding['evidence']; cid,p=paragraphs[evidence['paragraph_id']]; text=p['text']
        event=events[basis['death_event_id']]; brother_event=events[basis['brother_death_id']]
        def exact(mark):
            return 0 <= mark['start'] < mark['end'] <= len(text) and text[mark['start']:mark['end']]==mark['surface']
        topic=mentions[basis['recipient_person_mention_id']][2]; brother=mentions[basis['brother_mention_id']][2]; musician=mentions[basis['qin_recipient_id']][2]
        section='僧謙卒後四旬而微終，遺令薄葬，不設車需旐鼓挽之屬，施五尺床爲靈，二宿便毀，以常所彈琴置床上，何長史偃來，以琴與之。無子，家人遵之。所著文集傳於世。贈秘書監。'; start=text.index(section)
        return (cid=='c-nanshi-021-wangwei' and p['source_position']['revision_id']==1752646 and p['text_layer']=='received_chapter'
                and basis['source_term']==evidence['quote']==text and basis['paragraph_sha256']==sha256(text.encode()).hexdigest()
                and holding['kind']=='office' and holding['mode']=='posthumous_grant' and holding['title']=='秘書監'
                and [evidence]==basis['evidence']==holding['effective_period']['start']['evidence']==event['evidence']
                and all(exact(m) and mentions[m['id']][1]==p['id'] for m in [topic,brother,musician])
                and topic['person_id']==holding['person_id']==event['person_id'] and topic['id']==evidence['person_mention_id']
                and topic['start']==start+section.index('微終') and topic['surface']=='微'
                and brother['start']==start and brother['surface']=='僧謙' and musician['surface']=='偃' and musician['start']==start+section.index('偃來')
                and len({topic['person_id'],brother['person_id'],musician['person_id']})==3
                and event['source_term']=='終' and event['source_anchor']['start']==topic['end'] and event['event_type']=='death' and exact(event['source_anchor'])
                and brother_event['person_id']==brother['person_id'] and brother_event['event_type']=='death' and brother_event['source_term']=='卒'
                and exact(brother_event['source_anchor']) and brother_event['source_anchor']['start']==text.index('遂卒')+1
                and len(holding['attestations'])==1 and all(exact(a) and a['surface']=='秘書監' and a['start']==text.index('贈秘書監')+1
                and a['person_mention_id']==topic['id'] and a['usage']=='posthumous_usage' for a in holding['attestations']))
    except (KeyError,ValueError,TypeError,IndexError):
        return False
