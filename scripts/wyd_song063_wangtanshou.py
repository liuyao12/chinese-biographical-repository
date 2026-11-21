"""武英殿刊《宋書》王曇首傳的逐欄轉寫、親屬端點與身後贈諡。"""
import json
from hashlib import sha256
from pathlib import Path

CID = 'c-songshu-063-wangtanshou-wyd'
SID = 's-songshu-063-wangtanshou-wyd1739'
RAW = 'source-evidence/song063-wang/wyd-columns.txt'
DATA = 'source-evidence/song063-wang/wyd-reading.json'
FRAMES = 'source-evidence/song063-wang/wyd-native-frames.json'
RAW_SHA = 'a3ae53ead4a5ba2ebf8aa47e120cc69353f39fd44f82d0cd41d25b5d91fcb275'
DATA_SHA = '742e3eb56bd9805b99b4229f08bf1568daa298e42e4e04cead11edf849cfe7d1'
FRAMES_SHA = '72a33138045e903bd9869850a13600ca5def9cc42a682d25014b21428926c170'
TEXT_SHA = '59752959c8df363d592527a44ea3767a516021f51dba15d7146bf35ef78260c9'
WANG = '7r6_k52_qji_ABAAAAE'
EMPEROR = '3bh_k4m_fg4'


def checked(root,rel,digest):
    root=Path(root).resolve()
    f=root/rel
    if f!=f.resolve() or sha256(f.read_bytes()).hexdigest()!=digest:
        raise ValueError('書影轉寫憑據不符')
    return f.read_text()


def errors(ch,root):
    if ch['id']!=CID:
        return []
    try:
        raw=checked(root,RAW,RAW_SHA)
        checked(root,DATA,DATA_SHA)
        s=ch['source']
        if (ch['source_id']!=SID or s['raw_file_sha256']!=RAW_SHA or s['raw_path']!=RAW
                or s['revision_id']!='cbr-ai-transcription-sha256:'+RAW_SHA
                or s['image_verified'] is not True or ch['annotation']['human_reviewed'] is not False
                or ch['annotation']['print_projection_ref']!=DATA):
            raise ValueError('書影來源')
        cols=dict(t.split() for t in raw.splitlines())
        starts={};i=0
        for k,v in cols.items():starts[k]=i;i+=len(v)
        if i!=994 or len(cols)!=48:raise ValueError('全傳長度')
        pos=0
        for n,p in enumerate(ch['paragraphs'],1):
            if p['id']!=CID+f':p{n:03d}':raise ValueError('非該本段號')
            body=[]
            for a in p['source_position']['column_projection']:
                key=a['column'];lo=a['start'];hi=a['end']
                if not (0<=lo<hi<=len(cols[key]) and cols[key][lo:hi]==a['text']
                        and starts[key]+lo==pos):raise ValueError('欄位缺文或跨欄')
                body.append(a['text']);pos+=hi-lo
            if ''.join(body)!=p['text'] or p['source_position']['revision_id']!=s['revision_id']:
                raise ValueError('段落')
        if (pos!=994 or len(ch['paragraphs'])!=6 or ch['text_sha256']!=TEXT_SHA
                or sha256('\n\n'.join(p['text'] for p in ch['paragraphs']).encode()).hexdigest()!=TEXT_SHA):
            raise ValueError('傳文總長')
    except (KeyError,ValueError,TypeError,OSError):
        return ['宋書卷63王曇首殿本正文、固定分段或48欄的連續字位不符']
    return []


def kin_valid(a,ch,root):
    try:
        if ch['id']!=CID or errors(ch,root):return False
        f=json.loads(checked(root,FRAMES,FRAMES_SHA))['kinship'][a['id']]
        if (a['status']!='source_attested' or f['chapter_id']!=ch['id'] or f['qualifiers']!=a['qualifiers']
                or f['predicate']!=a['predicate'] or a['subject_person_id']==a['object_person_id']):return False
        ps={p['id']:p for p in ch['paragraphs']};ev={}
        for role in f['roles']:
            field=role['field'];pid=role['paragraph_id'];source=role['clause'];s=role['surface'];pers=role['person_id'];p=ps[pid]
            if p['text'].count(source)!=1 or source.count(s)!=1:return False
            i=p['text'].index(source)+source.index(s)
            hits=[r for r in ch['annotation']['person_reference_occurrences'] if r['paragraph_id']==pid and r['referent_role']=='third_person'] if field.endswith('_reference_id') else [m for m in p['mentions'] if m['kind']=='person']
            hit,=[m for m in hits if m['start']==i and m['end']==i+len(s) and m['surface']==s]
            if hit['person_id']!=pers or a[field.split('_')[0]+'_person_id']!=pers:return False
            e=ev.setdefault(pid,dict(work_id=ch['work_id'],book_id=ch['book_id'],source_id=ch['source_id'],chapter_id=ch['id'],paragraph_id=pid,quote=p['text']))
            e[field]=hit['id']
        return a['evidence']==list(ev.values())
    except (KeyError,IndexError,TypeError,ValueError,OSError):
        return False


def reference(ch, p, word, start, person):
    rows = ch['annotation']['person_reference_occurrences']
    row, = (r for r in rows if r['paragraph_id'] == p['id'] and r['start'] == start
            and r['end'] == start + len(word) and r['surface'] == word)
    if (row['person_id'] != person or row['referent_role'] != 'third_person'
            or row['quote'] != p['text'] or p['text'][start:row['end']] != word):
        raise ValueError('稱謂端點')
    return row['id']


def anchor(p, word, start):
    if p['text'][start:start + len(word)] != word:
        raise ValueError('原字不合')
    return dict(paragraph_id=p['id'], start=start, end=start + len(word), surface=word)


def evidence(p, ref):
    return dict(chapter_id=CID, book_id='b-songshu-063', work_id='w-songshu',
                source_id=SID, paragraph_id=p['id'], quote=p['text'], person_reference_id=ref)


def reference_title_valid(h, ch, root):
    try:
        if ch['id'] != CID or errors(ch, root):
            return False
        frame = json.loads(checked(root, FRAMES, FRAMES_SHA))['reference_titles'][h['id']]
        p = ch['paragraphs'][frame['number']-1]
        who, title, mode = frame['person_id'], frame['word'], frame['mode']
        rid = reference(ch, p, frame['role'], frame['role_start'], who)
        cited = [evidence(p, rid)]
        bounds = anchor(p, title, frame['word_start'])
        usage = 'posthumous_usage' if mode.startswith('posthumous_') else 'narrative'
        unknown = dict(status='unknown', date_expression=None, evidence=[])
        start = unknown if mode == 'attestation' else dict(
            status='source_event', event_type=mode, date_expression=frame['date'], evidence=cited)
        att, = h['attestations']
        return (h['printed_title_holder_reference'] == rid and h['person_id'] == who
                and (h['title'], h['mode'], h['kind']) == (title, mode, frame['kind'])
                and att == dict(**bounds, id=h['id']+':a', usage=usage, person_mention_id=None,
                                person_reference_id=rid, date_expression=frame['date'])
                and h['effective_period'] == dict(start=start, end=unknown)
                and h['status'] == 'source_attested' and h['evidence'] == cited)
    except (KeyError, IndexError, ValueError, OSError, TypeError):
        return False


def death_valid(event, cited, ch, root):
    try:
        if ch['id'] != CID or errors(ch, root):
            return False
        p = ch['paragraphs'][5]
        ref = reference(ch, p, '賢者', p['text'].index('賢者先殞'), WANG)
        return (event['id'] == 'le-wyd-song063-wangtanshou' and event['person_id'] == WANG
                and (event['event_type'], event['source_term'], event['date_expression'],
                     event['status']) == ('death', '卒', '七年', 'source_attested')
                and event['source_anchor'] == anchor(p, '卒', p['text'].index('七年卒')+2)
                and event['evidence'] == [cited] and cited == evidence(p, ref))
    except (KeyError, IndexError, ValueError, OSError, TypeError):
        return False


def award_valid(h, ch, events, root):
    try:
        if not reference_title_valid(h, ch, root):
            return False
        f = json.loads(checked(root, FRAMES, FRAMES_SHA))['awards'][h['id']]
        p = ch['paragraphs'][5]
        issuer = reference(ch, p, '太祖', p['text'].index('太祖爲之慟'), EMPEROR)
        holder = h['printed_title_holder_reference']
        word = f['term']
        cited, = h['evidence']
        death = events['le-wyd-song063-wangtanshou']
        return (h['person_id'] == WANG and death_valid(death, cited, ch, root)
                and h[f['basis']] == dict(kind='issued_wyd_song063_award', source_term=word,
                    source_anchor=anchor(p, word, p['text'].index(word)),
                    recipient_person_reference_id=holder, issuer_person_reference_id=issuer,
                    death_event_id=death['id'], death_term='卒', evidence=[cited]))
    except (KeyError, IndexError, ValueError, OSError, TypeError):
        return False
