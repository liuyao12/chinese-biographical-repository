"""A marked biography topic survives only explicitly scoped sovereign replies.

This does not select a recipient by nearest mention or by an unmarked name.
Every intervening other person must be an isolated, non-mortal sovereign reply.
"""
import re


def exact(anchor, p):
    return (isinstance(anchor, dict) and set(anchor) == {'paragraph_id','start','end','surface'}
            and anchor['paragraph_id'] == p.get('id') and type(anchor['start']) is int
            and type(anchor['end']) is int and 0 <= anchor['start'] < anchor['end'] <= len(p['text'])
            and p['text'][anchor['start']:anchor['end']] == anchor['surface'])


def explicit_topic_gift_valid(h, paragraphs, mentions, events):
    b=h.get('posthumous_basis',{})
    if not isinstance(b,dict):return False
    keys={'source_term','kind','topic_person_mention_id','death_event_id','death_anchor','gift_anchor','topic_span','sovereign_replies','evidence'}
    if (set(b)!=keys or b.get('kind')!='explicit_topic_scoped_gift' or h.get('mode')!='posthumous_grant'
            or h.get('kind') not in ('office','honorific') or not b['evidence'] or b['evidence']!=h.get('evidence')
            or b['evidence']!=h.get('effective_period',{}).get('start',{}).get('evidence')):return False
    event=events.get(b['death_event_id']);topic=mentions.get(b['topic_person_mention_id'])
    if (not event or event.get('event_type')!='death' or event.get('person_id')!=h.get('person_id')
            or not topic or topic[2].get('person_id')!=h.get('person_id')):return False
    for e in b['evidence']:
        hit=paragraphs.get(e.get('paragraph_id'))
        if not hit:return False
        p=hit[1];text=p['text'];d=b['death_anchor'];g=b['gift_anchor'];scope=b['topic_span']
        if (topic[1]!=p['id'] or e.get('person_mention_id')!=topic[2]['id'] or e.get('quote')!=text
                or p.get('text_layer')!='received_chapter' or not all(exact(a,p)for a in [d,g,scope]) or b.get('source_term')!=scope['surface']
                or (scope['start']>0 and text[scope['start']-1]not in '。；')
                or d['surface']!=event.get('source_term') or not re.search('[卒薨死]',d['surface'])
                or not any(x.get('paragraph_id')==p['id'] and x.get('quote')==text for x in event.get('evidence',[]))
                or not scope['start']<=topic[2]['start']<topic[2]['end']<=d['start']<d['end']<=g['start']<g['end']<=scope['end']
                or text[scope['start']:topic[2]['start']] not in ('','其後','後','初','先是')
                or not re.fullmatch(r'贈[^，。；、]+(?:、[^，。；、]+)*(?:，加[^，。；、]+(?:、[^，。；、]+)*)*',g['surface'])
                or h['title'] not in re.split(r'、|，加',g['surface'][1:])):return False
        permitted=set();replies=b['sovereign_replies']
        if not isinstance(replies,list):return False
        for reply in replies:
            if not isinstance(reply,dict)or set(reply)!={'person_mention_id','clause_anchor'}:return False
            m=mentions.get(reply['person_mention_id']);a=reply['clause_anchor']
            if (not m or m[1]!=p['id'] or m[2].get('person_id')==h['person_id'] or m[2].get('surface')not in ('上','帝','天子')
                    or not exact(a,p) or a['start']!=m[2]['start'] or not topic[2]['end']<=a['start']<a['end']<=d['start']
                    or (a['start']>0 and text[a['start']-1]not in '，。；') or (a['end']<len(text)and text[a['end']]not in '，。；')
                    or not re.fullmatch(re.escape(m[2]['surface'])+r'(?:輒|乃|遂|特|又)?(?:優詔不許|不許|詔許之|許之)',a['surface'])):return False
            permitted.add(m[2]['id'])
        if len(permitted)!=len(replies):return False
        if any(m.get('kind')=='person' and m.get('person_id')!=h['person_id'] and m['id']not in permitted
               and scope['start']<=m['start']<scope['end']for m in p.get('mentions',[])):return False
        if not any(a.get('paragraph_id')==p['id'] and a.get('person_mention_id')==topic[2]['id']
                   and a.get('surface')==h['title'] and g['start']<a.get('start',-1)<a.get('end',len(text)+1)<=g['end']
                   and text[a['start']:a['end']]==h['title']for a in h.get('attestations',[])):return False
    return True
