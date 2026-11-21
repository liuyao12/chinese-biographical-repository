"""王獻之傳「以後父追贈」及「以兄子靜之嗣」的原句與角色。"""


def succession_valid(row, paragraphs):
    try:
        e, = row['evidence']
        cid, p = paragraphs[e['paragraph_id']]
        t = p['text']
        ms = {m['id']:m for m in p['mentions'] if m['kind']=='person'}
        sub, obj = ms[e['subject_person_mention_id']], ms[e['object_person_mention_id']]
        term = '無子，以兄子靜之嗣'
        return (cid == e['chapter_id'] == 'c-jinshu-080-wangxizhi-family'
                and e['paragraph_id'] == cid + ':line116' and t == e['quote']
                and row['predicate'] == 'ritual_successor_of'
                and row['qualifiers'] == dict(source_term=term,succession_kind='w080_brothers_son_si',
                                              legal_adoption_status='not_stated',parentage_inference='not_inferred')
                and t.count(term) == 1 and t.index(term) + 6 == sub['start'] and t[sub['start']:sub['end']]==sub['surface']=='靜之'
                and t.startswith('未幾，獻之遇疾') and t[obj['start']:obj['end']]==obj['surface']=='獻之'
                and obj['start']==3 and sub['person_id']==row['subject_person_id'] and obj['person_id']==row['object_person_id'])
    except (KeyError,TypeError,ValueError,IndexError):
        return False


def gift_valid(holding, paragraphs, mentions, deaths):
    try:
        b=holding['posthumous_basis'];e,=holding['evidence'];cid,p=paragraphs[e['paragraph_id']];t=p['text']
        term='俄而卒於官。安僖皇后立，以後父追贈侍中、特進、光祿大夫、太宰，諡曰憲。'
        person=mentions[b['recipient_person_mention_id']][2];death=deaths[b['death_event_id']]
        roles=[m for m in p['mentions'] if m['surface']=='安僖皇后' and m['person_id']==b['daughter_person_id']]
        titles=('侍中','特進','光祿大夫','太宰');a,=holding['attestations']
        return (cid==e['chapter_id']=='c-jinshu-080-wangxizhi-family' and p['id']==cid+':line116'
                and b['kind']=='w080_empress_father_gift' and b['source_term']==term and t.count(term)==1
                and b['evidence']==holding['evidence']==holding['effective_period']['start']['evidence']
                and e['quote']==t and e['person_mention_id']==person['id']
                and person['person_id']==holding['person_id']==death['person_id'] and t[person['start']:person['end']]=='獻之'
                and person['start']==3 and death['event_type']=='death' and death['source_term']=='卒於官'
                and any(de['paragraph_id']==p['id'] for de in death['evidence']) and len(roles)==1
                and t.index(term)<roles[0]['start']<t.index('以後父追贈') and holding['title'] in titles
                and holding['mode']=='posthumous_grant' and a['surface']==holding['title']==t[a['start']:a['end']]
                and t.index('以後父追贈')<a['start']<t.index('，諡曰憲') and a['person_mention_id']==person['id'])
    except (KeyError,TypeError,ValueError,IndexError):
        return False
