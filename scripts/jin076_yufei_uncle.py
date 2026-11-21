"""Verify 虞潭 as the younger brother of the unnamed father in two received texts."""

def valid(a,pars):
    try:
        ev,=a['evidence'];cid,p=pars[ev['paragraph_id']];t=p['text']
        expected={
            'c-jinshu-076-yufei:line111':('𩦎字思行，潭之兄子也。','潭之兄子也'),
            'c-shishuoxinyu-009-jin076-yufei:yu':('𩦎字思行，會稽餘姚人。虞翻曾孫，右光祿潭兄子也。','右光祿潭兄子也'),
        }
        prefix,term=expected[p['id']]
        if a.get('predicate')!='paternal_uncle' or a['qualifiers']['source_term']!=term or not t.startswith(prefix) or ev['quote']!=t or ev['chapter_id']!=cid:
            return False
        ms={m['id']:m for m in p['mentions'] if m.get('kind')=='person'}
        for role,start,surface in [('subject',0,'𩦎'),('object',prefix.index('潭'),'潭')]:
            m=ms[ev[role+'_person_mention_id']]
            if (m['start'],m['end'],m['surface'],m['person_id'])!=(start,start+len(surface),surface,a[role+'_person_id']):return False
        return a['subject_person_id']!=a['object_person_id']
    except (ValueError,KeyError,TypeError):
        return False


def pei_layer(p,c,root):
    from hashlib import sha256
    try:
        s=c['source'];q=p['source_quote'];data=(root/s['raw_path']).read_bytes();text=data.decode()
        a,b=q['raw_start'],q['raw_end']
        expected='固与陆凯、孟宗同心忧国，年七十六卒。子弥，字钦远，仕晋，至梁州刺史。孙潭，光禄大夫。'
        if not (p['id']=='c-sanguozhi-057-jin076-yufei:ding' and c['work_id']=='w-sanguozhi'
                and s['revision_id']==2638131 and sha256(data).hexdigest()==s['raw_file_sha256']
                and q['source_layer']=='裴注引会稽典录' and p['attribution']==dict(annotator='裴松之',quoted_work='会稽典录')
                and text[a:b]==q['quote']==p['text']==expected and q['raw_line']==text[:a].count('\n')+1):
            return False
        prefix=text[text.rfind('{{*|',0,a):a]
        return prefix.startswith('{{*|《会稽典录》曰：') and '}}' not in prefix and '览子固，字子贱' in prefix
    except (KeyError,ValueError,IndexError,OSError):
        return False
