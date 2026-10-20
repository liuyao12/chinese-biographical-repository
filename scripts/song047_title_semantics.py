"""Exact elided second appointment and source title with unresolved holder."""
def anchor_valid(a,p):
    return (isinstance(a,dict) and set(a)=={'paragraph_id','start','end','surface'} and a['paragraph_id']==p['id']
            and type(a['start'])is int and type(a['end'])is int and 0<=a['start']<a['end']<=len(p['text'])
            and p['text'][a['start']:a['end']]==a['surface'])

def elided_decline_valid(proposal,chapter):
    try:
        b=proposal['elided_appointment_context'];e,=proposal['evidence'];p=next(p for p in chapter['paragraphs']if p['id']==e['paragraph_id']);ms={m['id']:m for m in p['mentions']}
        if (set(b)!={'kind','first_recipient_mention_id','first_title_anchors','second_recipient_mention_id','second_title_anchors','refusing_mention_id','joint_clause_anchor','human_reviewed'}
                or b['kind']!='second_named_recipient_with_named_refusal' or b['human_reviewed']is not False
                or proposal['proposal_kind']!='unassumed_appointment' or proposal['outcome']!='not_assumed'
                or proposal['non_assumption_kind']!='declined' or proposal['appointment_stage']!='appointment'
                or proposal['status']!='contextual_provisional' or proposal['human_reviewed']is not False
                or any(e[k]!=chapter[k]for k in ('work_id','book_id','source_id')) or e['chapter_id']!=chapter['id']or e['quote']!=p['text']):return False
        first=ms[b['first_recipient_mention_id']];second=ms[b['second_recipient_mention_id']];refusing=ms[b['refusing_mention_id']]
        if (any(m['kind']!='person'or m.get('person_id')is None or p['text'][m['start']:m['end']]!=m['surface']for m in (first,second,refusing))
                or first['person_id']==second['person_id'] or second['person_id']!=refusing['person_id']
                or proposal['person_id']!=second['person_id']or proposal['person_mention_id']!=second['id']):return False
        a1,a2=b['first_title_anchors'],b['second_title_anchors'];joint=b['joint_clause_anchor'];appointment=proposal['appointment_anchor'];refusal=proposal['non_assumption_anchor'];role=proposal['role_anchor']
        if len(a1)!=2 or len(a2)!=2 or not all(anchor_valid(a,p)for a in a1+a2+[joint,appointment,refusal,role]):return False
        if not (all(xs[0]['surface'].endswith('將軍')and xs[1]['surface'].endswith('刺史')for xs in (a1,a2))
                and role in a2 and role['surface']==proposal['title']):return False
        expected='以'+first['surface']+'為'+''.join(a['surface']for a in a1)+second['surface']+''.join(a['surface']for a in a2)+refusing['surface']+'辭不拜'
        if joint['surface']!=expected or proposal['source_term']!=expected:return False
        cursor=joint['start']
        for surface,start,end in [('以',cursor,cursor+1),(first['surface'],first['start'],first['end']),('為',first['end'],first['end']+1)]+[(a['surface'],a['start'],a['end'])for a in a1]+[(second['surface'],second['start'],second['end'])]+[(a['surface'],a['start'],a['end'])for a in a2]+[(refusing['surface'],refusing['start'],refusing['end']),('辭不拜',refusal['start'],refusal['end'])]:
            if start!=cursor or end!=cursor+len(surface):return False
            cursor=end
        return (cursor==joint['end']and appointment['start']==joint['start']and appointment['end']==first['end']+1
                and appointment['surface']=='以'+first['surface']+'為'and refusal['surface']=='辭不拜')
    except (KeyError,ValueError,TypeError,StopIteration):return False

def unresolved_title_errors(chapter,person_ids):
    errors=[];seen=set();ps={p['id']:p for p in chapter['paragraphs']}
    for a in chapter.get('annotation',{}).get('unresolved_title_attestations',[]):
        try:
            assert set(a)=={'id','person_id','title','kind','status','person_mention_id','holder_surface','title_anchor','candidate_person_ids','identity_case_id','evidence','human_reviewed','reviewer','interpretation_note'}
            assert a['id']not in seen;seen.add(a['id'])
            e,=a['evidence'];p=ps[e['paragraph_id']];m=next(m for m in p['mentions']if m['id']==a['person_mention_id'])
            assert a['person_id']is None and a['status']=='identity_unresolved'and a['kind']=='office'and a['human_reviewed']is False and a['reviewer']and a['interpretation_note']
            assert m['kind']=='unresolved'and m['person_id']is None and a['holder_surface']==m['surface']
            assert anchor_valid(a['title_anchor'],p)and a['title']==a['title_anchor']['surface']and a['title_anchor']['end']==m['start']
            assert e['quote']==p['text']and e['chapter_id']==chapter['id']and all(e[k]==chapter[k]for k in ('work_id','book_id','source_id'))
            assert a['candidate_person_ids']==m['candidate_person_ids']and set(a['candidate_person_ids'])<=person_ids
            case=next(c for c in chapter['annotation']['unresolved_identity_cases']if c['id']==a['identity_case_id'])
            assert case['status']=='unresolved'and a['person_mention_id']in case['unresolved_mention_ids']and case['candidate_person_ids']==a['candidate_person_ids']
        except (AssertionError,KeyError,ValueError,TypeError,StopIteration):errors.append('未決官稱須綁原職名與未連人物錨點，不能指定候選為持有人：'+str(a.get('id')))
    return errors


def imperial_gift_valid(h, paragraphs, mentions, life_events):
    """Two explicit named decree recipients, or a single named decree topic with attested death."""
    import hashlib
    try:
        b=h['posthumous_basis'];e,=b['evidence'];cid,p=paragraphs[e['paragraph_id']];text=p['text'];start=h['effective_period']['start']
        common={'kind','source_term','evidence','source_revision','paragraph_sha256','grant_anchor'}
        assert h['mode']=='posthumous_grant'and h['kind']=='office'and h['status']=='source_attested'
        assert e['chapter_id']==cid and e['quote']==text==b['source_term']and p['text_layer']=='received_chapter'
        assert b['evidence']==h['evidence']==start['evidence']and start['status']=='source_event'and start['event_type']=='posthumous_grant'
        assert start['date_expression']is None and 'normalized_date'not in start and 'normalized_date_range'not in start
        assert b['source_revision']==p['source_position']['source_revision']and b['paragraph_sha256']==hashlib.sha256(text.encode()).hexdigest()
        g=b['grant_anchor'];assert anchor_valid(g,p)
        if b['kind']=='imperial_named_serial_gift':
            assert set(b)==common|{'recipient_person_mention_id','recipient_pairs','next_appointment_anchor'}
            assert text.startswith('詔曰')and len(b['recipient_pairs'])==2
            cursor=g['start']+2;assert g['surface'].startswith('可贈');selected=[];seen=set()
            for pair in b['recipient_pairs']:
                assert set(pair)=={'person_mention_id','title_anchor'}
                cc,pp,m=mentions[pair['person_mention_id']];a=pair['title_anchor']
                assert cc==cid and pp==p['id']and m['kind']=='person'and m['person_id']not in seen
                seen.add(m['person_id']);assert m['start']==cursor and m['end']==cursor+len(m['surface'])and text[cursor:m['end']]==m['surface']
                assert anchor_valid(a,p)and a['start']==m['end']and a['surface'].endswith(('將軍','太守'))
                if m['id']==b['recipient_person_mention_id']:selected.append((m,a))
                cursor=a['end']
            assert cursor==g['end'];n=b['next_appointment_anchor'];assert anchor_valid(n,p)and n['start']==cursor and n['surface'].endswith('補')
            following=[m for m in p['mentions']if m['start']==n['start']and m.get('kind')=='person']
            assert len(following)==1 and following[0]['person_id']not in seen and following[0]['surface']+'補'==n['surface']
            m,a=selected[0];assert len(selected)==1 and a['surface']==h['title']
        else:
            assert b['kind']=='imperial_decree_topic_death_gift'and set(b)==common|{'topic_person_mention_id','death_event_id','death_anchor'}
            cc,pp,m=mentions[b['topic_person_mention_id']];d=b['death_anchor'];ev=life_events[b['death_event_id']]
            assert cc==cid and pp==p['id']and m['kind']=='person'and text.startswith('又詔曰故')and m['start']>4
            assert anchor_valid(d,p)and d['surface']=='殞身鋒鏑'and m['end']<d['start']<d['end']<g['start']
            assert g['surface']=='可贈'+h['title']
            assert ev['person_id']==h['person_id']and ev['event_type']=='death'and ev['status']=='source_attested'and ev['source_term']==d['surface']and ev['source_anchor']==d
            assert e in ev['evidence']
            assert all(z.get('person_id')==m['person_id']for z in p['mentions']if z.get('kind')=='person'and z['start']<g['end'])
            a={'paragraph_id':p['id'],'start':g['start']+2,'end':g['end'],'surface':h['title']}
        assert m['person_id']==h['person_id']and e['person_mention_id']==m['id']
        assert any(all(t.get(k)==v for k,v in a.items())and t.get('person_mention_id')==m['id']and t.get('usage')=='posthumous_usage'for t in h['attestations'])
        return True
    except (AssertionError,KeyError,ValueError,TypeError,IndexError):return False
