"""核桓偉二贈同列及桓玄傳同人卒贈，按各傳原稱保存。"""
def valid(h, paragraphs, mentions, life):
    try:
        b=h['posthumous_basis'];e,=h['evidence'];cid,p=paragraphs[e['paragraph_id']]
        death=life[b['death_event_id']];de,=death['evidence'];dc,dp=paragraphs[de['paragraph_id']]
        recipient=mentions[b['recipient_person_mention_id']]
        a,=h['attestations'];name=h['title'];clause=b['source_term']
        return (cid=='c-jinshu-098-huanwen' and p['id']==cid+':p030' and e['quote']==p['text']
                and dc=='c-jinshu-099-jin098-huan-children' and dp['text']=='是歲，玄兄偉卒，贈開府、驃騎將軍，以桓脩代之。'
                and death['person_id']==h['person_id']==recipient[2]['person_id'] and recipient[1]==p['id'] and recipient[2]['surface']=='偉'
                and death['source_term']=='玄兄偉卒' and de['quote']==dp['text'] and de['person_mention_id']==next(m['id']for m in dp['mentions']if m['surface']=='偉')
                and name in ('驃騎將軍','開府儀同三司') and clause=='贈驃騎將軍、開府儀同三司' and p['text'].count(clause)==1
                and a['start']==p['text'].index(clause)+clause.index(name) and p['text'][a['start']:a['end']]==a['surface']==name and a['person_mention_id']==recipient[2]['id']
                and h['mode']=='posthumous_grant' and b['evidence']==h['evidence']==h['effective_period']['start']['evidence'])
    except (KeyError,ValueError,StopIteration,TypeError,IndexError):
        return False

def uncle(a,paragraphs):
    try:
        e,=a['evidence'];cid,p=paragraphs[e['paragraph_id']];ms={m['id']:m for m in p['mentions']};s=ms[e['subject_person_mention_id']];o=ms[e['object_person_mention_id']]
        return (cid=='c-jinshu-098-huanwen' and p['id']==cid+':p030' and e['quote']==p['text'] and s['person_id']==a['subject_person_id'] and o['person_id']==a['object_person_id']
                and s['surface']=='熙' and o['surface']=='秘' and p['text'][s['start']:o['end']+3]=='熙與叔秘謀殺沖'
                and a['predicate']=='paternal_uncle' and a['qualifiers']['source_term']=='叔秘')
    except (KeyError,ValueError,StopIteration,TypeError):return False
