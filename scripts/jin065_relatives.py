"""Validate serial and revised gifts in the three received notices after the named person's death."""
def gift_valid(h,paragraphs,mentions,events):
    try:
        b=h['posthumous_basis'];e,=h['evidence'];cid,p=paragraphs[e['paragraph_id']]
        corpus='c-jinshu-065-wangdao-family'
        choices={
            ('line086','開府'):('追贈車騎將軍、開府','le-wangdao4-86-11-9','珣'),
            ('line086','司徒'):('玄輔政，改贈司徒','le-wangdao4-86-11-9','珣'),
            ('line102','司徒'):('追贈侍中、司徒','le-wangdao4-102-226-12','謐'),
            ('line106','車騎將軍'):('卒，贈車騎將軍','le-wangdao4-106-83-13','劭')}
        term,death_id,name=choices[(p['id'].split(':')[-1],h['title'])];t=p['text'];a,=h['attestations'];m=mentions[e['person_mention_id']][2];death=events[death_id]
        return (cid==e['chapter_id']==corpus and b['kind']=='jin065_relatives_gift' and e['quote']==t and p['text_layer']=='received_chapter'
                and t.count(term)==1 and term==b['source_term'] and h['mode']=='posthumous_grant'
                and m['id']==b['recipient_person_mention_id']==a['person_mention_id'] and m['surface']==name
                and h['person_id']==m['person_id']==death['person_id'] and death['event_type']=='death'
                and death_id==b['death_event_id'] and any(s['paragraph_id']==p['id'] for s in death['evidence'])
                and a['start']==t.index(term)+term.index(h['title']) and t[a['start']:a['end']]==h['title']==a['surface']
                and b['evidence']==h['evidence']==h['effective_period']['start']['evidence'])
    except (KeyError, TypeError, ValueError, IndexError):return False

def succession_valid(event, paragraphs):
    try:
        e,=event['evidence'];cid,p=paragraphs[e['paragraph_id']];b=event['source_clause_binding'];a=b['source_attestation']
        m=next(m for m in p['mentions'] if m['id']==e['person_mention_id'])
        return (cid==e['chapter_id']=='c-jinshu-065-wangdao-family' and p['id']==a['paragraph_id'] and e['quote']==p['text']
                and p['text_layer']=='received_chapter' and p['text'].startswith('謐字稚遠。') and m['surface']=='稚遠'
                and event['person_id']==m['person_id'] and event['source_term']=='襲父爵'
                and p['text'][a['start']-2:a['end']]=='襲父爵' and p['text'][a['start']:a['end']]==a['surface']=='爵'
                and a['person_mention_id']==m['id'] and a['id']=='ta-wangdao4-100-30-111'
                and event['id']=='th-wangdao4-100-30-111' and event['event_type']=='noble_title_succession'
                and event['mode']=='accession' and event['predecessor_person_id'] is None
                and event['title'] is None and event['holding_id'] is None and event['date_expression'] is None)
    except (KeyError,TypeError,StopIteration,ValueError,IndexError):return False
