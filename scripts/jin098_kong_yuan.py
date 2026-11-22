"""Check the named seal recipient and Liu's unquoted identification of Yuan Hu."""
import hashlib


def seal_valid(h, paragraphs, mentions, deaths):
    try:
        b=h['posthumous_basis'];e,=b['evidence'];cid,p=paragraphs[e['paragraph_id']]
        dead=deaths[b['death_event_id']];m=mentions[b['recipient_person_mention_id']][2];att,=h['attestations']
        term='贈臨賀太夫人印綬'
        return (cid=='c-jinshu-098-huanwen' and p['id']==cid+':p010' and e['quote']==p['text']
            and p['text'].startswith('母孔氏卒，') and (m['surface'],m['start'],m['end'])==('孔氏',1,3)
            and p['text'].count(term)==1 and h['kind']=='honorific' and h['mode']=='posthumous_grant'
            and h['title']==att['surface']=='臨賀太夫人' and att['usage']=='posthumous_usage'
            and att['start']==p['text'].index(term)+1 and att['end']==att['start']+len(h['title'])
            and e['person_mention_id']==att['person_mention_id']==m['id'] and b['source_term']==term
            and dead['event_type']=='death' and dead['source_term']=='母孔氏卒'
            and h['person_id']==dead['person_id']==m['person_id'] and dead['evidence']==h['evidence']
            and h['evidence']==b['evidence']==h['effective_period']['start']['evidence'])
    except (KeyError,TypeError,ValueError,IndexError):
        return False


def liu_yuan_note(p,c,root):
    try:
        q=p['source_quote'];s=c['source'];raw=(root/s['raw_path']).read_bytes()
        t=raw.decode();a,b=q['raw_start'],q['raw_end'];rule='{{ProperNoun|虎}}，{{ProperNoun|袁宏}}小字也。'
        return (p['id']=='c-shishuoxinyu-004-jin098-huanwen-luoyang:note' and c['work_id']=='w-shishuoxinyu'
            and p['text_layer']=='witness_appended_liuxiaobiao_note' and p['text']=='虎，袁宏小字也。'
            and p['attribution']==dict(annotator='劉孝標',quoted_work=None)
            and s['revision_id']==2567461 and hashlib.sha256(raw).hexdigest()==s['raw_file_sha256']
            and q['source_layer']=='劉孝標注' and t[a:b]==q['quote']==rule and q['raw_line']==t[:a].count('\n')+1
            and t[:a].endswith('{{ProperNoun|袁虎}}少貧，{{*|') and t[b:].startswith('}}嘗爲人傭載運租。'))
    except (KeyError,TypeError,ValueError,OSError):
        return False
