"""Bind the last memorials, the plural referent, and the posthumous office to their source clauses."""


def shared_reference(chapter, row, rows):
    if chapter['id']!='c-jinshu-098-huanwen':
        return False
    p=next((p for p in chapter['paragraphs'] if p['id']==row.get('paragraph_id')),None)
    if not p or p['id']!=chapter['id']+':p029' or '沖問溫以謝安、王坦之所任' not in p['text']:
        return False
    allowed={'伊等':'伊等不為汝所處分','彼':'溫知己存彼不敢異','之':'害之無益於沖'}
    term=allowed.get(row.get('surface'))
    if not term or p['text'].count(term)!=1:
        return False
    a=p['text'].index(term)+term.index(row['surface'])
    b=a+len(row['surface'])
    group_id=row.get('group_reference_id')
    groups=[g for g in chapter['annotation'].get('person_group_references',[]) if g.get('id')==group_id]
    if len(groups)!=1:
        return False
    g=groups[0]
    paired=[r for r in rows if r.get('group_reference_id')==group_id]
    ids=[m.get('person_id') for m in p['mentions'] if m.get('surface') in ('謝安','王坦之')]
    if len(set(ids))!=2 or len(ids)!=2 or len(paired)!=2:
        return False
    return (g.get('person_ids')==ids==[r.get('person_id') for r in paired]
            and len(set(g.get('reference_ids',[])))==2 and g['reference_ids']==[r.get('id') for r in paired]
            and (g.get('paragraph_id'),g.get('start'),g.get('end'),g.get('surface'),g.get('quote'))==(p['id'],a,b,row['surface'],term)
            and all((r.get('paragraph_id'),r.get('start'),r.get('end'),r.get('surface'),r.get('quote'),r.get('referent_role'))==(p['id'],a,b,row['surface'],term,'third_person') for r in paired))


def refused(row,chapter):
    if chapter['id']!='c-jinshu-098-huanwen':
        return False
    try:
        p=chapter['paragraphs'][25]
        assert p['id']==chapter['id']+':p026'
        text=p['text']
        for key,phrase,surface in [('role_anchor','進公丞相','丞相'),('appointment_anchor','今進公丞相','進'),('non_assumption_anchor','溫固辭','固辭')]:
            a=text.index(phrase)+phrase.index(surface)
            assert row[key]==dict(paragraph_id=p['id'],start=a,end=a+len(surface),surface=surface)
        mark=next(m for m in p['mentions']if m['id']==row['person_mention_id'])
        assert mark['person_id']==row['person_id'] and mark['start']==text.index('溫固辭') and mark['surface']=='溫'
        return (row['title'],row['non_assumption_kind'],row['outcome'],row['evidence'][0]['quote'])==('丞相','declined','not_assumed',text)
    except (AssertionError,KeyError,ValueError,StopIteration,IndexError,TypeError):
        return False


def gift(h,paragraphs,mentions,life):
    try:
        b=h['posthumous_basis'];e,=h['evidence'];cid,p=paragraphs[e['paragraph_id']];text=p['text'];a,=h['attestations']
        death=life[b['death_event_id']];de,=death['evidence']
        recipient=mentions[b['recipient_person_mention_id']]
        return (cid==e['chapter_id']=='c-jinshu-098-huanwen' and p['id']==cid+':p028'
                and de['paragraph_id']==p['id'] and de['quote']==e['quote']==text
                and death['event_type']=='death' and death['source_term']=='錫文未及成而薨，時年六十二'
                and text.count(death['source_term'])==1 and text.endswith('追贈丞相。')
                and h['person_id']==death['person_id']==recipient[2]['person_id'] and recipient[1]==p['id']
                and a['person_mention_id']==e['person_mention_id']==b['recipient_person_mention_id']
                and h['title']==a['surface']=='丞相' and (a['start'],a['end'])==(len(text)-3,len(text)-1)
                and h['kind']=='office' and h['mode']=='posthumous_grant' and a['usage']=='posthumous_usage'
                and b['source_term']=='追贈丞相' and h['evidence']==b['evidence']==h['effective_period']['start']['evidence'])
    except (KeyError,ValueError,IndexError,TypeError):
        return False
